#!/usr/bin/env python3
"""
GPT-SoVITS 批量 TTS 管线 v1.0

用法:
    # 方式1: 单句测试
    python3 batch_tts.py --char wusong --text "武松大喝一声，手提哨棒"

    # 方式2: 从 JSON 脚本文件批量生成
    python3 batch_tts.py --script drama_script.json

    # 方式3: 从角色-台词映射生成
    python3 batch_tts.py --lines '{"wusong":["台词1","台词2"],"luzhishen":["台词3"]}'

输入脚本格式 (drama_script.json):
{
  "scenes": [
    {
      "id": "scene_01",
      "dialogues": [
        {"speaker": "wusong", "text": "武松大步走上景阳冈，风声呼啸。", "emotion": "坚定"},
        {"speaker": "wusong", "text": "远处传来虎啸，武松握紧哨棒。", "emotion": "警觉"}
      ]
    }
  ]
}
"""

import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

CHARACTER_VOICES_PATH = Path(__file__).parent / "character_voices.json"


def load_config() -> dict:
    with open(CHARACTER_VOICES_PATH, "r") as f:
        return json.load(f)


def _check_character_ready(char_id: str, config: dict) -> Tuple[bool, str]:
    chars = config.get("characters", {})
    if char_id not in chars:
        all_ids = list(chars.keys())
        return False, f"角色 '{char_id}' 不在配置中。可用角色: {all_ids}"
    c = chars[char_id]
    if not c.get("ref_audio") or not c.get("prompt_text"):
        todo = c.get("_todo", "需补充 ref_audio 和 prompt_text")
        return False, f"角色 '{char_id}' 参考音频未配置: {todo}"
    ref_path = os.path.expanduser(c["ref_audio"])
    if not os.path.exists(ref_path):
        return False, f"参考音频不存在: {ref_path}"
    return True, ""


class GPTSoVITS:
    def __init__(self, config: dict):
        sovits_cfg = config["gpt_sovits_config"]
        root = os.path.expanduser(sovits_cfg["GPT_SOVITS_ROOT"])
        sys.path.insert(0, os.path.join(root, "GPT_SoVITS", "GPT_SoVITS"))
        sys.path.insert(0, os.path.join(root, "GPT_SoVITS"))

        self.gpt_path = os.path.expanduser(sovits_cfg["gpt_path"])
        self.sovits_path = os.path.expanduser(sovits_cfg["sovits_path"])
        self.bert_path = os.path.expanduser(sovits_cfg["bert_path"])
        self.output_dir = os.path.expanduser(sovits_cfg.get("output_dir", "~/GPT-SoVITS/output/drama"))

        os.environ.update({
            "gpt_path": self.gpt_path,
            "sovits_path": self.sovits_path,
            "bert_path": self.bert_path,
        })
        os.chdir(root)

        import inference_webui as w
        self.w = w

        gen = w.change_sovits_weights(self.sovits_path)
        list(gen)

        print(f"[GPT-SoVITS] 模型就绪 (device={w.device}, is_half={w.is_half})")

    def generate(self, char_config: dict, text: str) -> Tuple[int, np.ndarray]:
        w = self.w
        ref_wav = os.path.expanduser(char_config["ref_audio"])
        prompt_text = char_config["prompt_text"]
        prompt_lang = char_config.get("prompt_language", "Chinese")

        params = dict(char_config.get("gpt_params", {}))
        params.setdefault("how_to_cut", "不切")
        params.setdefault("top_k", 5)
        params.setdefault("top_p", 0.9)
        params.setdefault("temperature", 0.8)
        params.setdefault("speed", 1.0)
        params.setdefault("sample_steps", 32)

        gen = w.get_tts_wav(
            ref_wav, prompt_text, prompt_lang,
            text, "Chinese",
            **params
        )
        sr, audio = next(gen)
        return sr, audio

    def generate_batch(self, char_config: dict, lines: List[str], char_id: str) -> List[str]:
        os.makedirs(self.output_dir, exist_ok=True)
        outputs = []
        n = len(lines)
        for i, text in enumerate(lines):
            text = text.strip()
            if not text:
                continue
            t0 = time.time()
            try:
                sr, audio = self.generate(char_config, text)
            except Exception as e:
                print(f"  [{i+1}/{n}] ❌ {text[:20]}... => {e}")
                continue

            dur = len(audio) / sr
            filename = f"{char_id}_{i+1:03d}.wav"
            out_path = os.path.join(self.output_dir, filename)
            import soundfile
            soundfile.write(out_path, np.clip(audio, -32768, 32767).astype(np.int16), sr)
            elapsed = time.time() - t0
            print(f"  [{i+1}/{n}] ✅ {dur:.1f}s / {elapsed:.0f}s | {text[:30]}... → {filename}")
            outputs.append(out_path)
        return outputs


def run(args):
    config = load_config()
    chars = config.get("characters", {})

    if args.list:
        print("可用角色:")
        for cid, c in chars.items():
            ready, _ = _check_character_ready(cid, config)
            status = "✅ 就绪" if ready else "⏳ 待配置"
            ref = c.get("ref_audio", "") or "(未设置)"
            print(f"  {status}  {cid} ({c['name']}): {c['voice_desc']}  | 参考: {ref}")
        return

    if args.char and args.text:
        char_id = args.char
        ready, err = _check_character_ready(char_id, config)
        if not ready:
            print(f"❌ {err}")
            sys.exit(1)

        print(f"[单句测试] {char_id}: {args.text}")
        tts = GPTSoVITS(config)
        sr, audio = tts.generate(chars[char_id], args.text)

        out = os.path.join(tts.output_dir, f"{char_id}_test.wav")
        os.makedirs(tts.output_dir, exist_ok=True)
        import soundfile
        soundfile.write(out, np.clip(audio, -32768, 32767).astype(np.int16), sr)
        print(f"✅ 输出: {out} ({len(audio)/sr:.1f}s)")
        return

    tts = None

    if args.script:
        with open(args.script, "r") as f:
            script = json.load(f)
    elif args.lines:
        script = json.loads(args.lines)
    else:
        print("用法: batch_tts.py --char wusong --text '台词'")
        print("      batch_tts.py --script drama_script.json")
        print("      batch_tts.py --lines '{\"wusong\":[\"台词1\",\"台词2\"]}'")
        print("      batch_tts.py --list")
        sys.exit(1)

    tts = GPTSoVITS(config)

    if "scenes" in script:
        char_lines: Dict[str, List[str]] = {}
        for scene in script["scenes"]:
            for d in scene.get("dialogues", []):
                speaker = d.get("speaker", "")
                if speaker not in char_lines:
                    char_lines[speaker] = []
                char_lines[speaker].append(d["text"])
        batch = char_lines
    elif isinstance(script, dict):
        batch = script
    else:
        print("❌ 无法识别的脚本格式")
        sys.exit(1)

    for char_id, lines in batch.items():
        ready, err = _check_character_ready(char_id, config)
        if not ready:
            print(f"⚠️ 跳过 {char_id}: {err}")
            continue

        print(f"\n{'='*50}")
        print(f"🎤 {chars[char_id]['name']} ({char_id}): {len(lines)} 条台词")
        print(f"   参考: {os.path.basename(chars[char_id]['ref_audio'])}")
        tts.generate_batch(chars[char_id], lines, char_id)

    print(f"\n✅ 全部完成! 输出目录: {tts.output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPT-SoVITS 批量 TTS")
    parser.add_argument("--char", help="角色 ID (wusong/luzhishen/...)")
    parser.add_argument("--text", help="单句台词")
    parser.add_argument("--script", help="剧本 JSON 文件路径")
    parser.add_argument("--lines", help="JSON 格式角色→台词映射")
    parser.add_argument("--list", action="store_true", help="列出所有角色及其配置状态")
    run(parser.parse_args())
