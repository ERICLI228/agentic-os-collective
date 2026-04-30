"""
SFX Engine - 短剧环境音效自动混音系统

功能:
1. freesound.org API 搜索/下载 CC0 音效
2. 按场景自动匹配音效 (风雪/虎啸/刀剑/脚步/雨声/柴火)
3. 自动混音到旁白音频流
4. 本地缓存避免重复下载

用法:
    python3 shared/core/sfx_engine.py --test           # 测试环境
    python3 shared/core/sfx_engine.py --download       # 预下载音效库
    python3 shared/core/sfx_engine.py --episode 03     # 为EP03生成SFX混音
"""

import os
import json
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── 配置 ──
FREESOUND_API_KEY = os.environ.get("FREESOUND_API_KEY", "")
FREESOUND_BASE = "https://freesound.org/apiv2"

# 本地音效库缓存
SFX_LIBRARY_DIR = Path(os.path.expanduser("~/.agentic-os/sfx_library"))
SFX_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

# FFmpeg
FFMPEG = "/opt/homebrew/Cellar/ffmpeg/8.1_1/bin/ffmpeg"
FFMPEG = FFMPEG if Path(FFMPEG).exists() else "ffmpeg"

# ── 场景→音效映射 ──
SCENE_SFX_MAP = {
    "风雪": {
        "keywords": ["wind howling", "snow storm", "blizzard", "cold wind"],
        "volume": 0.15,
        "fade_in": 1.0,
        "fade_out": 1.0,
    },
    "柴火": {
        "keywords": ["fire crackling", "campfire", "wood burning", "fireplace"],
        "volume": 0.20,
        "fade_in": 0.5,
        "fade_out": 0.5,
    },
    "虎啸": {
        "keywords": ["tiger roar", "animal growl", "wild cat"],
        "volume": 0.25,
        "fade_in": 0.2,
        "fade_out": 0.5,
    },
    "刀剑": {
        "keywords": ["sword clash", "metal hit", "weapon swing", "knife"],
        "volume": 0.18,
        "fade_in": 0.1,
        "fade_out": 0.3,
    },
    "脚步": {
        "keywords": ["footsteps walking", "boots on ground", "walking gravel"],
        "volume": 0.12,
        "fade_in": 0.3,
        "fade_out": 0.3,
    },
    "雨声": {
        "keywords": ["rain heavy", "thunderstorm", "rain falling"],
        "volume": 0.15,
        "fade_in": 1.0,
        "fade_out": 1.0,
    },
    "鸟鸣": {
        "keywords": ["birds chirping", "forest ambience", "nature sounds"],
        "volume": 0.10,
        "fade_in": 0.5,
        "fade_out": 0.5,
    },
    "水声": {
        "keywords": ["river flowing", "water stream", "creek"],
        "volume": 0.12,
        "fade_in": 0.5,
        "fade_out": 0.5,
    },
}

# ── 各集场景配置 ──
EPISODE_SFX = {
    "03": {  # 林冲风雪山神庙
        "shots": [
            {"scene": "风雪", "start": 0, "duration": None},  # 全程
            {"scene": "柴火", "start": 8, "duration": 7},     # 山神庙内
        ]
    },
    "04": {  # 宋江杀阎婆惜
        "shots": [
            {"scene": "脚步", "start": 0, "duration": 5},
            {"scene": "刀剑", "start": 12, "duration": 3},
        ]
    },
    "05": {  # 李逵沂岭杀四虎
        "shots": [
            {"scene": "脚步", "start": 0, "duration": 5},
            {"scene": "虎啸", "start": 8, "duration": 8},
            {"scene": "刀剑", "start": 10, "duration": 6},
        ]
    },
    "06": {  # 智取生辰纲
        "shots": [
            {"scene": "鸟鸣", "start": 0, "duration": 5},
            {"scene": "脚步", "start": 5, "duration": 5},
            {"scene": "水声", "start": 12, "duration": 6},
        ]
    },
}


class SFXEngine:
    """音效引擎: 搜索→下载→缓存→混音"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or FREESOUND_API_KEY
        self.cache_file = SFX_LIBRARY_DIR / "cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            with open(self.cache_file) as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    def search_sfx(self, query: str, license: str = "cc0", max_results: int = 5) -> List[Dict]:
        """搜索 freesound 音效 (需 API Key)"""
        if not self.api_key:
            print("  ⚠️ 未设置 FREESOUND_API_KEY, 跳过搜索")
            return []

        params = urllib.parse.urlencode({
            'query': query,
            'filter': f'license:{license}',
            'fields': 'id,name,duration,previews,license,download',
            'page_size': max_results,
        })
        url = f"{FREESOUND_BASE}/search/text/?{params}"

        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Token {self.api_key}")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                return data.get("results", [])
        except Exception as e:
            print(f"  ⚠️ freesound 搜索失败: {e}")
            return []

    def download_sfx(self, sound_id: int, name: str, preview_url: str = None) -> Optional[Path]:
        """下载音效到本地缓存 (优先 preview, 其次 full download)"""
        cache_key = str(sound_id)
        if cache_key in self.cache:
            cached_path = Path(self.cache[cache_key]["path"])
            if cached_path.exists():
                return cached_path

        # 优先用 preview (低延迟, 免OAuth)
        download_url = preview_url
        if not download_url:
            download_url = f"{FREESOUND_BASE}/sounds/{sound_id}/download/"

        # 生成文件名
        safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in name)
        filename = f"{sound_id}_{safe_name[:40]}.mp3"
        filepath = SFX_LIBRARY_DIR / filename

        req = urllib.request.Request(download_url)
        if "download" in download_url:
            req.add_header("Authorization", f"Token {self.api_key}")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                with open(filepath, "wb") as f:
                    f.write(resp.read())

            self.cache[cache_key] = {
                "name": name,
                "path": str(filepath),
                "id": sound_id,
            }
            self._save_cache()
            print(f"  ✅ 下载: {name} ({filepath.stat().st_size // 1024}KB)")
            return filepath
        except Exception as e:
            print(f"  ⚠️ 下载失败 {name}: {e}")
            return None

    def find_or_download(self, scene_type: str) -> Optional[Path]:
        """查找或下载指定场景类型的音效"""
        scene_cfg = SCENE_SFX_MAP.get(scene_type)
        if not scene_cfg:
            print(f"  ⚠️ 未知场景类型: {scene_type}")
            return None

        # 先查缓存是否有该类型的音效
        for sid, info in self.cache.items():
            if scene_type.lower() in info.get("name", "").lower():
                p = Path(info["path"])
                if p.exists():
                    return p

        # 搜索并下载
        for keyword in scene_cfg["keywords"]:
            results = self.search_sfx(keyword)
            if results:
                best = results[0]
                preview = best.get("previews", {}).get("preview-hq-mp3") or best.get("previews", {}).get("preview-lq-mp3")
                path = self.download_sfx(
                    sound_id=best["id"],
                    name=f"{scene_type}_{best['name'][:30]}",
                    preview_url=preview,
                )
                if path:
                    return path

        return None

    def mix_sfx(
        self,
        audio_file: Path,
        sfx_file: Path,
        output_file: Path,
        start_offset: float = 0,
        duration: float = None,
        volume: float = 0.15,
        fade_in: float = 0.5,
        fade_out: float = 0.5,
    ):
        """将音效混入主音频流"""
        if not sfx_file or not sfx_file.exists():
            return audio_file

        # 获取主音频时长
        probe = subprocess.run(
            [FFMPEG, "-i", str(audio_file), "-f", "null", "-"],
            capture_output=True, text=True
        )
        duration_match = [l for l in probe.stderr.split("\n") if "Duration:" in l]
        if duration_match:
            parts = duration_match[0].split("Duration:")[1].strip().split(",")[0]
            h, m, s = parts.split(":")
            audio_duration = int(h) * 3600 + int(m) * 60 + float(s)
        else:
            audio_duration = 23  # 默认

        # 构建 ffmpeg 混音命令
        # 主音频 + 音效叠加, 音效在指定时间淡入淡出
        sfx_duration = duration or (audio_duration - start_offset)

        cmd = [
            FFMPEG, "-y",
            "-i", str(audio_file),
            "-i", str(sfx_file),
            "-filter_complex",
            f"[1]volume={volume},"
            f"afade=t=in:st={start_offset}:d={fade_in},"
            f"afade=t=out:st={start_offset + sfx_duration - fade_out}:d={fade_out},"
            f"atrim=0:{sfx_duration}[sfx];"
            f"[0][sfx]amix=inputs=2:duration=longest:dropout_transition=0",
            "-c:a", "aac",
            str(output_file),
        ]

        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  🎵 混音: {sfx_file.name} @ {start_offset}s, vol={volume}")
        return output_file

    def process_episode(self, ep_id: str, audio_dir: Path, output_dir: Path) -> Optional[Path]:
        """处理整集的音效混音"""
        ep_sfx = EPISODE_SFX.get(ep_id)
        if not ep_sfx:
            print(f"  ℹ️ EP{ep_id} 无预配置音效")
            return None

        # 找到主旁白音频文件 (合并后的)
        main_audio = output_dir / "_temp_audio.aac"
        if not main_audio.exists():
            # 找第一个旁白文件
            narrations = sorted(audio_dir.glob("narration_*.mp3")) or sorted(audio_dir.glob("narration_*.aiff"))
            if not narrations:
                print("  ⚠️ 无旁白音频, 跳过SFX")
                return None
            main_audio = narrations[0]

        output_audio = output_dir / "final_with_sfx.aac"

        for shot_cfg in ep_sfx["shots"]:
            scene_type = shot_cfg["scene"]
            start = shot_cfg["start"]
            dur = shot_cfg.get("duration")

            sfx_file = self.find_or_download(scene_type)
            if not sfx_file:
                continue

            scene_cfg = SCENE_SFX_MAP[scene_type]
            temp_out = output_dir / "_sfx_temp.aac"

            try:
                self.mix_sfx(
                    main_audio, sfx_file, temp_out,
                    start_offset=start,
                    duration=dur,
                    volume=scene_cfg["volume"],
                    fade_in=scene_cfg["fade_in"],
                    fade_out=scene_cfg["fade_out"],
                )
                main_audio = temp_out
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ 混音失败: {e}")
                continue

        if main_audio != output_dir / "_temp_audio.aac":
            main_audio.rename(output_audio)
            print(f"  ✅ SFX 混音完成 → {output_audio.name}")
            return output_audio

        return None


def test_environment():
    """测试环境配置"""
    results = {}

    # FFmpeg
    try:
        subprocess.run([FFMPEG, "-version"], capture_output=True, timeout=5)
        results["ffmpeg"] = True
    except Exception:
        results["ffmpeg"] = False

    # freesound API
    if FREESOUND_API_KEY:
        results["freesound_api_key"] = True
    else:
        results["freesound_api_key"] = False

    # 本地缓存
    cache_count = len(list(SFX_LIBRARY_DIR.glob("*.mp3")))
    results["sfx_cached"] = f"{cache_count} 文件"

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SFX 音效引擎")
    parser.add_argument("--test", action="store_true", help="测试环境")
    parser.add_argument("--download", action="store_true", help="预下载音效库")
    parser.add_argument("--episode", type=str, help="处理指定集数 (03-06)")
    parser.add_argument("--audio-dir", type=str, help="旁白音频目录")
    parser.add_argument("--output-dir", type=str, help="输出目录")
    args = parser.parse_args()

    engine = SFXEngine()

    if args.test:
        print("🔍 SFX 环境测试:")
        results = test_environment()
        for k, v in results.items():
            status = "✅" if v else "⚠️"
            print(f"  {status} {k}: {v}")

    elif args.download:
        print("📥 预下载音效库...")
        for scene_type in SCENE_SFX_MAP:
            print(f"\n  [{scene_type}]")
            engine.find_or_download(scene_type)

    elif args.episode:
        ep_id = args.episode
        audio_dir = Path(args.audio_dir) if args.audio_dir else Path(f"~/.agentic-os/episode_{ep_id}/audio").expanduser()
        output_dir = Path(args.output_dir) if args.output_dir else Path(f"~/.agentic-os/episode_{ep_id}").expanduser()

        print(f"🎬 处理 EP{ep_id} SFX 混音...")
        result = engine.process_episode(ep_id, audio_dir, output_dir)
        if result:
            print(f"✅ 输出: {result}")
        else:
            print("ℹ️ 无音效处理")

    else:
        parser.print_help()
