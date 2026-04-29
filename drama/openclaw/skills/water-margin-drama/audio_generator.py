"""
多角色配音生成器 (FR-DR-007) — v2.0 NLS-only

配音方案:
  1. Aliyun NLS TTS → 使用资源包 NLSTTSBAG-xxx (唯一方案)

用法:
  python3 audio_generator.py --script drama_script.json --roles role_library.json
  python3 audio_generator.py --text "台词内容" --voice "武松" --output out.mp3
"""
import json, os, sys, subprocess, argparse
from pathlib import Path
from datetime import datetime

from aliyun_nls import synthesize, VOICE_MAP


def generate_voice(text: str, character: str, output_dir: str = None) -> str:
    if output_dir is None:
        output_dir = "/tmp"
    voice = VOICE_MAP.get(character, VOICE_MAP["default"])
    output_path = f"{output_dir}/audio_{character}_{datetime.now().strftime('%H%M%S')}.mp3"
    result = synthesize(text, voice, output_path)
    if result:
        return result
    print(f"❌ 无法为 {character} 生成配音")
    return ""


def batch_generate(script_data: dict, output_dir: str = None) -> list:
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
                "duration": len(text) * 0.25,
            })
    return results


def main():
    parser = argparse.ArgumentParser(description="多角色配音生成器 (FR-DR-007) — NLS-only")
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
