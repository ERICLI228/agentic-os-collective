#!/usr/bin/env python3
"""
多角色配音生成器 (FR-DR-007) — v1.0 可用版

配音方案 (优先级):
  1. macOS say → 本地 TTS，零成本，单角色
  2. ElevenLabs API → 高质量多角色 (需 API Key)
  3. MiniMax TTS → 降级方案 (需 API Key)

用法:
  python3 audio_generator.py --script drama_script.json --roles role_library.json
  python3 audio_generator.py --text "台词内容" --voice "武松" --output out.m4a
"""
import json, os, sys, subprocess, argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from shared.config import config

# ── 角色→macOS系统语音映射 ──
VOICE_MAP = {
    "武松": "Tingting",       # 普通话女声 (刚毅)
    "宋江": "Sin-ji",         # 粤语→用普通话替代
    "李逵": "Tingting",       # 粗犷
    "林冲": "Sin-ji",
    "鲁智深": "Tingting",
    "旁白": "Sin-ji",
    "default": "Tingting",
}

# ElevenLabs 角色→Voice ID 映射 (需配置 API Key)
ELEVENLABS_VOICES = {
    "武松":  os.environ.get("ELEVENLABS_VOICE_WUSONG", ""),
    "宋江":  os.environ.get("ELEVENLABS_VOICE_SONGJIANG", ""),
    "旁白":  os.environ.get("ELEVENLABS_VOICE_NARRATOR", ""),
}


def generate_macos_tts(text: str, voice: str = "Tingting", output_path: str = None) -> str:
    """使用 macOS say 命令生成 TTS"""
    if output_path is None:
        output_path = f"/tmp/tts_{datetime.now().strftime('%H%M%S')}.m4a"
    cmd = ["say", "-v", voice, "-o", output_path.replace(".m4a", ".aiff"), text]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        # 转换 aiff → m4a
        aiff = output_path.replace(".m4a", ".aiff")
        if Path(aiff).exists():
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", aiff, output_path],
                          check=True, capture_output=True, timeout=15)
            Path(aiff).unlink(missing_ok=True)
        return output_path
    except Exception as e:
        print(f"⚠️  macOS TTS 失败: {e}")
        return ""


def generate_elevenlabs_tts(text: str, voice_id: str, output_path: str = None) -> str:
    """ElevenLabs TTS (需 API Key)"""
    api_key = config.MINIMAX_API_KEY or os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key or not voice_id:
        return ""
    if output_path is None:
        output_path = f"/tmp/tts_el_{datetime.now().strftime('%H%M%S')}.mp3"
    try:
        import urllib.request
        data = json.dumps({
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }).encode('utf-8')
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            data=data,
            headers={"xi-api-key": api_key, "Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=30)
        Path(output_path).write_bytes(resp.read())
        return output_path
    except Exception as e:
        print(f"⚠️  ElevenLabs TTS 失败: {e}")
        return ""


def generate_voice(text: str, character: str, output_dir: str = None) -> str:
    """
    为指定角色生成配音 (自动选择最优方案)
    返回生成的音频文件路径
    """
    if output_dir is None:
        output_dir = "/tmp"

    output_path = f"{output_dir}/audio_{character}_{datetime.now().strftime('%H%M%S')}.m4a"

    # 尝试 ElevenLabs
    el_voice = ELEVENLABS_VOICES.get(character, "")
    if el_voice:
        result = generate_elevenlabs_tts(text, el_voice, output_path.replace(".m4a", ".mp3"))
        if result:
            return result

    # 降级到 macOS say
    mac_voice = VOICE_MAP.get(character, "Tingting")
    result = generate_macos_tts(text, mac_voice, output_path)
    if result:
        return result

    print(f"❌ 无法为 {character} 生成配音")
    return ""


def batch_generate(script_data: dict, output_dir: str = None) -> list:
    """
    批量生成所有角色配音
    script_data 格式: {"scenes": [{"lines": [{"character": "武松", "text": "..."}]}]}
    """
    if output_dir is None:
        output_dir = str(Path(__file__).parent / "output" / "audio")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    results = []
    scenes = script_data.get("scenes", []) or script_data.get("episodes", [])

    for scene in scenes:
        for line in scene.get("lines", []) or scene.get("dialogue", []):
            character = line.get("character", line.get("speaker", "旁白"))
            text = line.get("text", line.get("line", ""))
            if not text:
                continue
            audio_path = generate_voice(text, character, output_dir)
            results.append({
                "character": character,
                "text": text[:80],
                "audio": audio_path,
                "duration": len(text) * 0.25,  # 估算: ~4字/秒
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="多角色配音生成器 (FR-DR-007)")
    parser.add_argument("--script", help="剧本 JSON 文件")
    parser.add_argument("--text", help="直接传入台词文本")
    parser.add_argument("--voice", default="武松", help="目标角色 (用于 --text 模式)")
    parser.add_argument("--output", default=None, help="输出音频路径")
    args = parser.parse_args()

    if args.text:
        path = generate_voice(args.text, args.voice)
        if path:
            print(f"✅ {args.voice}: {path}")
        else:
            print("❌ 生成失败")
            sys.exit(1)

    elif args.script:
        script = json.loads(Path(args.script).read_text())
        results = batch_generate(script)
        for r in results:
            status = "✅" if r["audio"] else "❌"
            print(f"  {status} {r['character']}: {r['text'][:50]}...")
        print(f"\n生成完成: {sum(1 for r in results if r['audio'])}/{len(results)} 成功")

    else:
        print("用法: --script FILE 或 --text TEXT --voice 角色名")
        sys.exit(1)


if __name__ == "__main__":
    main()
