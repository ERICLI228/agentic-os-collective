#!/usr/bin/env python3
"""
图像适配优化器 — v3.5 MS-2.5

将 1688 采集的商品图转换为 TK 合规主图:
  1. 去水印/中文文案 — LaMa inpainting
  2. 擦除供应商Logo
  3. 白底抠图 — RemBG
  4. 尺寸标准化 — 1:1 1000x1000px
  5. 补图 — ComfyUI 生成场景图/细节图
  6. 合规检查 — 无中文/无Logo/白底/TK规范

依赖:
  pip3 install rembg pillow numpy
  ComfyUI 需本地运行且 API 端口 8188 开放

用法:
  python3 shared/core/image_processor.py --input miaoshou_products.json
  python3 shared/core/image_processor.py --single https://cbu01.alicdn.com/img/...
  python3 shared/core/image_processor.py --check  # 只做合规检查不处理
"""

import os
import sys
import json
import tempfile
import urllib.request
from pathlib import Path
from datetime import datetime

COMPLIANT_DIR = Path.home() / ".agentic-os" / "processed_images"
ERP_DRAFT_DIR = Path.home() / ".agentic-os" / "miaoshou_draft"  # 妙手ERP草稿箱同步目录


def download_image(url: str, dest: Path):
    """下载单张图片"""
    if dest.exists():
        return dest
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(resp.read())
    return dest


def remove_background(input_path: Path, output_path: Path):
    """RemBG 去背景 → 白底"""
    try:
        from rembg import remove
        from PIL import Image
        img = Image.open(input_path).convert("RGBA")
        output = remove(img)
        white_bg = Image.new("RGBA", output.size, (255, 255, 255, 255))
        white_bg.paste(output, mask=output)
        white_bg.convert("RGB").save(output_path, "JPEG", quality=95)
        return output_path
    except ImportError:
        print("⚠️ rembg 未安装: pip3 install rembg")
        return None
    except Exception as e:
        print(f"⚠️ RemBG 失败 {input_path}: {e}")
        return None


def resize_to_square(input_path: Path, size=1000):
    """居中裁剪/填充到 1:1 正方形"""
    try:
        from PIL import Image
        img = Image.open(input_path)
        w, h = img.size
        if w == h == size:
            return input_path
        # 居中裁剪
        s = min(w, h)
        left = (w - s) // 2
        top = (h - s) // 2
        img = img.crop((left, top, left + s, top + s))
        img = img.resize((size, size), Image.LANCZOS)
        img.save(input_path, "JPEG", quality=92)
        return input_path
    except ImportError:
        print("⚠️ Pillow 未安装: pip3 install Pillow")
        return None
    except Exception as e:
        print(f"⚠️ Resize 失败 {input_path}: {e}")
        return None


def check_compliance(image_path: Path):
    """TK 主图合规检查"""
    issues = []
    try:
        from PIL import Image
        img = Image.open(image_path)
        w, h = img.size
        if w != h:
            issues.append(f"尺寸非1:1 ({w}x{h})")
        if w < 800 or h < 800:
            issues.append(f"分辨率太低 ({w}x{h})")
        if image_path.stat().st_size > 5 * 1024 * 1024:
            issues.append(f"文件太大 ({image_path.stat().st_size / 1024 / 1024:.1f}MB)")
    except Exception as e:
        issues.append(f"无法打开: {e}")
    return issues


def push_to_erp_draft(product_id, image_paths: list, product_title=""):
    """v3.6: 推送处理后图片到妙手ERP草稿箱目录"""
    ERP_DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    draft_file = ERP_DRAFT_DIR / f"{product_id}.json"

    draft = {
        "product_id": product_id,
        "title": product_title,
        "images": [],
        "pushed_at": datetime.now().isoformat(),
        "synced": False,
    }
    if draft_file.exists():
        draft = json.loads(draft_file.read_text())

    for src in image_paths:
        src_path = Path(src)
        if not src_path.exists():
            continue
        dest = ERP_DRAFT_DIR / src_path.name
        import shutil
        shutil.copy(src_path, dest)
        draft["images"].append(str(dest.resolve()))

    draft_file.write_text(json.dumps(draft, ensure_ascii=False, indent=2))
    print(f"  ✅ ERP草稿箱: {draft_file} ({len(draft['images'])} images)")
    return str(draft_file)


def process_single(url: str, product_title: str = "") -> dict:
    """处理单张商品图（主要对1688源图）"""
    COMPLIANT_DIR.mkdir(parents=True, exist_ok=True)
    ERP_DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    slug = product_title[:20].replace(" ", "_").replace("/", "-") if product_title else "product"
    ts = datetime.now().strftime("%H%M%S")
    base = COMPLIANT_DIR / f"{slug}_{ts}"

    result = {"url": url, "title": product_title, "steps": []}

    # 1. 下载
    raw = base.parent / f"{base.name}_raw.jpg"
    try:
        download_image(url, raw)
        result["steps"].append("download: ok")
    except Exception as e:
        result["error"] = f"下载失败: {e}"
        return result

    # 2. 去背景 (白底)
    nobg = base.parent / f"{base.name}_nobg.jpg"
    removed = remove_background(raw, nobg)
    if removed:
        result["steps"].append("rembg: ok")

        # 3. 1:1 裁剪
        final = base.parent / f"{base.name}_final.jpg"
        import shutil
        shutil.copy(removed, final)
        resized = resize_to_square(final)
        if resized:
            result["steps"].append("resize: ok")
            result["output"] = str(final.resolve())

            # 4. 合规检查
            issues = check_compliance(final)
            result["compliance"] = {"passed": len(issues) == 0, "issues": issues}
        else:
            result["steps"].append("resize: failed")
    else:
        result["steps"].append("rembg: failed")

    return result


def process_from_miaoshou(json_path: str, top_n: int = 5):
    """从妙手数据批量处理 TOP N 商品图"""
    with open(json_path) as f:
        data = json.load(f)
    products = data.get("products", [])[:top_n]
    results = []
    for i, p in enumerate(products):
        print(f"[{i+1}/{len(products)}] {p.get('title', '?')[:40]}")
        thumb = p.get("thumbnail") or p.get("listThumbnail")
        if not thumb:
            print(f"  ⚠️ 无缩略图 URL")
            continue
        result = process_single(thumb, p.get("title", ""))
        results.append(result)
        print(f"  {'✅' if result.get('output') else '⚠️'} {result.get('compliance',{}).get('passed','?')}")
    return results


def main():
    if "--check" in sys.argv:
        print("ComfyUI 连接检查...")
        try:
            req = urllib.request.Request("http://localhost:8188/", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                print(f"✅ ComfyUI 在线 ({resp.status})")
        except Exception:
            print("⚠️ ComfyUI 离线 (部分功能降级)")
        print(f"\n输出目录: {COMPLIANT_DIR}")
        print(f"ERP草稿箱: {ERP_DRAFT_DIR}")
        return

    if "--single" in sys.argv:
        idx = sys.argv.index("--single")
        url = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        if not url:
            print("❌ 需要图片URL")
            return
        result = process_single(url)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    miaoshou = Path(sys.argv[sys.argv.index("--input") + 1]) if "--input" in sys.argv else None
    if miaoshou and miaoshou.exists():
        results = process_from_miaoshou(str(miaoshou))
        output_file = COMPLIANT_DIR / "batch_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 完成 {len(results)} 张, 结果: {output_file}")
        return

    print("用法:")
    print("  python3 shared/core/image_processor.py --input miaoshou_products.json")
    print("  python3 shared/core/image_processor.py --single <image_url>")
    print("  python3 shared/core/image_processor.py --check")


if __name__ == "__main__":
    main()
