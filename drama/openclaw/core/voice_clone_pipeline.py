#!/usr/bin/env python3
"""
GPT-SoVITS 自动化声音克隆管线 v1.0

用法:
    # 注册新声音 (录 3-10s → 标注文本)
    python3 voice_clone_pipeline.py register --char luzhishen --audio ~/ref.wav --text "你这厮，吃洒家一拳！"

    # 测试已注册的声音
    python3 voice_clone_pipeline.py test --char luzhishen --text "鲁智深大喝一声，举起禅杖"

    # 从 episode 剧本批量生成角色台词
    python3 voice_clone_pipeline.py batch --episode 02

    # 列出所有角色状态
    python3 voice_clone_pipeline.py list

工作流:
    1. register → 录音 → 标注 → 更新配置
    2. test     → 单句验证声音质量
    3. batch    → 批量生成剧集台词
"""

import argparse
import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = PROJECT_ROOT / "drama" / "openclaw" / "skills" / "water-margin-drama" / "character_voices.json"
REF_AUDIO_DIR = Path.home() / ".agentic-os" / "character_voices" / "reference"
OUTPUT_DIR = Path.home() / ".agentic-os" / "character_voices" / "output"
SOVITS_API = "http://localhost:9880"

DEFAULT_PARAMS = {
    "how_to_cut": "不切",
    "top_k": 5,
    "top_p": 0.9,
    "temperature": 0.8,
    "speed": 1.0,
    "sample_steps": 32,
}

CHARACTER_NAMES = {
    "wusong": "武松",
    "luzhishen": "鲁智深",
    "linchong": "林冲",
    "songjiang": "宋江",
    "likui": "李逵",
    "wuyong": "吴用",
}

VOICE_DESC = {
    "wusong": "男声，有力豪迈",
    "luzhishen": "男声，洪亮爽朗",
    "linchong": "男声，儒雅沉稳",
    "songjiang": "男声，沉稳内敛",
    "likui": "男声，粗犷暴烈",
    "wuyong": "男声，清朗智慧",
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"characters": {}, "gpt_sovits_config": {}}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"  💾 配置已保存: {CONFIG_PATH}")


def check_api() -> bool:
    try:
        urllib.request.urlopen(f"{SOVITS_API}/control", timeout=3)
        return True
    except Exception:
        return False


def tts_api(ref_wav: str, prompt_text: str, text: str,
            prompt_lang: str = "zh", text_lang: str = "zh",
            **params) -> Optional[bytes]:
    """调用 GPT-SoVITS API (端口 9880)"""
    import urllib.parse
    qs = {
        "refer_wav_path": ref_wav,
        "prompt_text": prompt_text,
        "prompt_language": prompt_lang,
        "text": text,
        "text_language": text_lang,
        **params,
    }
    url = f"{SOVITS_API}/?{urllib.parse.urlencode(qs)}"
    try:
        resp = urllib.request.urlopen(url, timeout=120)
        return resp.read()
    except Exception as e:
        print(f"  ❌ API 错误: {e}")
        return None


def cmd_list(args):
    config = load_config()
    chars = config.get("characters", {})
    api_ok = check_api()
    print(f"GPT-SoVITS API: {'✅ 就绪' if api_ok else '❌ 未运行 (端口 9880)'}")
    print(f"\n{'角色ID':<12} {'名称':<8} {'状态':<10} {'参考音频':<30} {'描述'}")
    print("-" * 85)
    for cid in CHARACTER_NAMES:
        c = chars.get(cid, {})
        name = CHARACTER_NAMES[cid]
        ref = c.get("ref_audio", "")
        ready = bool(ref and os.path.exists(os.path.expanduser(ref)))
        status = "✅ 已配置" if ready else "⏳ 待录音"
        ref_short = os.path.basename(ref) if ref else "(未设置)"
        desc = VOICE_DESC.get(cid, "")
        print(f"  {cid:<10} {name:<6} {status:<8} {ref_short:<28} {desc}")
    print(f"\n总计: {sum(1 for cid in CHARACTER_NAMES if chars.get(cid,{}).get('ref_audio'))} / {len(CHARACTER_NAMES)} 已配置")


def cmd_register(args):
    char_id = args.char
    audio_path = os.path.expanduser(args.audio)
    prompt_text = args.text

    if char_id not in CHARACTER_NAMES:
        print(f"❌ 未知角色: {char_id}. 可用: {list(CHARACTER_NAMES.keys())}")
        sys.exit(1)

    if not os.path.exists(audio_path):
        print(f"❌ 参考音频不存在: {audio_path}")
        sys.exit(1)

    size_kb = os.path.getsize(audio_path) / 1024
    print(f"🎤 注册角色声音: {CHARACTER_NAMES[char_id]} ({char_id})")
    print(f"  📁 参考音频: {audio_path} ({size_kb:.0f} KB)")
    print(f"  📝 参考文本: {prompt_text}")

    if not check_api():
        print("❌ GPT-SoVITS API 未运行，请先启动: cd ~/GPT-SoVITS && ./venv/bin/python api.py")
        sys.exit(1)

    # Copy reference audio to managed directory
    REF_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    ext = os.path.splitext(audio_path)[1] or ".wav"
    managed_path = REF_AUDIO_DIR / f"{char_id}_reference{ext}"
    shutil.copy2(audio_path, managed_path)
    print(f"  📁 已复制到: {managed_path}")

    # Verify: generate a test sample
    print(f"  🎵 测试生成: '{prompt_text}'")
    test_text = prompt_text
    audio_bytes = tts_api(
        ref_wav=str(managed_path),
        prompt_text=prompt_text,
        text=test_text,
        **DEFAULT_PARAMS
    )

    if not audio_bytes:
        print("  ❌ 测试生成失败，请检查 API 日志")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    test_out = OUTPUT_DIR / f"{char_id}_register_test.wav"
    with open(test_out, "wb") as f:
        f.write(audio_bytes)
    print(f"  ✅ 测试生成成功: {test_out} ({len(audio_bytes)/1024:.0f} KB)")

    # Update config
    config = load_config()
    config.setdefault("characters", {})
    config["characters"][char_id] = {
        "name": CHARACTER_NAMES[char_id],
        "voice_desc": VOICE_DESC.get(char_id, ""),
        "ref_audio": str(managed_path),
        "prompt_text": prompt_text,
        "prompt_language": "Chinese",
        "gpt_params": DEFAULT_PARAMS,
        "ready": True,
        "registered_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_config(config)
    print(f"\n✅ {CHARACTER_NAMES[char_id]} 声音已注册!")
    print(f"   参考音频: {managed_path}")
    print(f"   测试音频: {test_out}")
    print(f"   下一步: python3 voice_clone_pipeline.py test --char {char_id} --text '自定义台词'")


def cmd_test(args):
    char_id = args.char
    text = args.text
    config = load_config()
    c = config.get("characters", {}).get(char_id)

    if not c or not c.get("ref_audio"):
        print(f"❌ 角色 '{char_id}' 未注册，请先运行 register")
        sys.exit(1)

    ref = os.path.expanduser(c["ref_audio"])
    if not os.path.exists(ref):
        print(f"❌ 参考音频不存在: {ref}")
        sys.exit(1)

    if not check_api():
        print("❌ GPT-SoVITS API 未运行")
        sys.exit(1)

    print(f"🎤 测试: {CHARACTER_NAMES[char_id]} ({char_id})")
    print(f"  📝 台词: {text}")

    t0 = time.time()
    params = dict(c.get("gpt_params", DEFAULT_PARAMS))
    audio_bytes = tts_api(ref_wav=ref, prompt_text=c["prompt_text"], text=text, **params)
    elapsed = time.time() - t0

    if not audio_bytes:
        print("  ❌ 生成失败")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{char_id}_test_{int(time.time())}.wav"
    with open(out_file, "wb") as f:
        f.write(audio_bytes)

    print(f"  ✅ 完成 ({elapsed:.1f}s) | 大小: {len(audio_bytes)/1024:.0f} KB")
    print(f"  📁 输出: {out_file}")
    return out_file


def cmd_batch(args):
    ep_id = args.episode
    script_path = Path.home() / ".agentic-os" / f"episode_{ep_id}" / "script" / f"script_ep{ep_id}.json"

    if not script_path.exists():
        print(f"❌ 剧本不存在: {script_path}")
        sys.exit(1)

    with open(script_path, "r") as f:
        script = json.load(f)

    if not check_api():
        print("❌ GPT-SoVITS API 未运行")
        sys.exit(1)

    config = load_config()
    chars = config.get("characters", {})

    # Collect lines by speaker from narration shots
    ep_character = script.get("character", "")
    lines_by_char: Dict[str, List[str]] = {}
    for shot in script.get("shots", []):
        text = shot.get("narration", "")
        char_name = shot.get("character") or ep_character
        if char_name and text.strip():
            cid = None
            for cid_key, cn in CHARACTER_NAMES.items():
                if cn == char_name:
                    cid = cid_key
                    break
            if cid and cid in chars and chars[cid].get("ref_audio"):
                lines_by_char.setdefault(cid, []).append(text)

    if not lines_by_char:
        print("⚠️ 剧本中无已配置角色的台词")
        return

    ep_output_dir = OUTPUT_DIR / f"ep{ep_id}"
    ep_output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for cid, lines in lines_by_char.items():
        c = chars[cid]
        ref = os.path.expanduser(c["ref_audio"])
        prompt_text = c["prompt_text"]
        params = dict(c.get("gpt_params", DEFAULT_PARAMS))
        name = CHARACTER_NAMES[cid]

        print(f"\n{'='*50}")
        print(f"🎤 {name} ({cid}): {len(lines)} 句")
        print(f"   参考: {os.path.basename(ref)}")

        for i, text in enumerate(lines):
            text = text.strip()
            if not text:
                continue
            t0 = time.time()
            audio_bytes = tts_api(ref_wav=ref, prompt_text=prompt_text, text=text, **params)
            elapsed = time.time() - t0

            out_file = ep_output_dir / f"{cid}_{i+1:03d}.wav"
            if audio_bytes:
                with open(out_file, "wb") as f:
                    f.write(audio_bytes)
                print(f"  [{i+1}/{len(lines)}] ✅ {elapsed:.1f}s | {text[:30]}... → {out_file.name}")
                total += 1
            else:
                print(f"  [{i+1}/{len(lines)}] ❌ {text[:30]}...")

    print(f"\n✅ 批量生成完成! {total} 个文件 → {ep_output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPT-SoVITS 自动化声音克隆管线")
    sub = parser.add_subparsers(dest="command")

    sp_list = sub.add_parser("list", help="列出所有角色声音状态")
    sp_list.set_defaults(func=cmd_list)

    sp_reg = sub.add_parser("register", help="注册新声音")
    sp_reg.add_argument("--char", required=True, help="角色 ID (wusong/luzhishen/...)")
    sp_reg.add_argument("--audio", required=True, help="参考音频路径 (3-10s)")
    sp_reg.add_argument("--text", required=True, help="参考音频对应的文本")
    sp_reg.set_defaults(func=cmd_register)

    sp_test = sub.add_parser("test", help="测试已注册的声音")
    sp_test.add_argument("--char", required=True, help="角色 ID")
    sp_test.add_argument("--text", required=True, help="测试台词")
    sp_test.set_defaults(func=cmd_test)

    sp_batch = sub.add_parser("batch", help="从剧集剧本批量生成台词")
    sp_batch.add_argument("--episode", required=True, help="剧集编号 (01-06)")
    sp_batch.set_defaults(func=cmd_batch)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
    else:
        args.func(args)
