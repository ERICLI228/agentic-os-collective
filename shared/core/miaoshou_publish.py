#!/usr/bin/env python3
"""
妙手ERP 发布模块 — v3.5 Sprint 2.2

API 清单 (2026-04-29 浏览器抓包确认):

  认领(1688→妙手采集箱):
    POST /api/move/common_collect_box/claimed
    body: detailSerialNumberPlatformList[0][detailId]=<id>&detailSerialNumberPlatformList[0][platform]=tiktok&detailSerialNumberPlatformList[0][serialNumber]=1

  发布到店铺:
    POST /api/platform/tiktok/move/collect_box/claimToShop
    body: detailIds[0]=<tk_collect_id>&shopIds[0]=<shop_id>

  店铺映射:
    7795399 → MagicPockets (tiktokGlobal)
    8371977 → MagicPockets (菲律宾)
    7795400 → MagicPockets (其他)
    8460401 → MagicPockets (其他)
    8460416 → MagicPockets (其他)
    8460434 → MagicPockets (其他)

用法:
  from shared.core.miaoshou_publish import MiaoshouClient
  client = MiaoshouClient()
  client.login()
  client.claim_to_tiktok(common_detail_id=2253352686, platform='tiktok')
  client.publish_to_shop(tk_detail_id=2912284562, shop_ids=[7795399])

注意: 启动前必须确保 MIAOSHOW_PUBLISH_ENABLED=true 且已通过 publish_gate 审批
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
import subprocess
from pathlib import Path
from http.cookiejar import CookieJar

# AES-128-CBC, zero IV, PKCS7 padding
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

AES_KEY = "@3438jj;siduf832"
BASE_URL = "https://erp.91miaoshou.com"
OCR_SCRIPT = "/tmp/ocr_captcha3.swift"


def aes_encrypt(plaintext: str) -> str:
    """AES-128-CBC 加密 (zero IV, PKCS7)"""
    key = AES_KEY.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv=b"\x00" * 16)
    return cipher.encrypt(pad(plaintext.encode("utf-8"), 16)).hex()


class MiaoshouClient:
    """妙手ERP API 客户端"""

    def __init__(self):
        self.cookies = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )
        self.token = None

    def _request(self, method, path, data=None, extra_headers=None):
        url = f"{BASE_URL}{path}"
        headers = {
            "accept": "application/json, text/plain, */*",
            "bx-v": "2.5.11",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        }
        if extra_headers:
            headers.update(extra_headers)

        body = None
        if data:
            if isinstance(data, dict):
                body = urllib.parse.urlencode(data).encode("utf-8")
                headers.setdefault("content-type", "application/x-www-form-urlencoded")
            else:
                body = data.encode("utf-8") if isinstance(data, str) else data
                headers.setdefault("content-type", "application/json")

        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        resp = self.opener.open(req, timeout=15)
        return json.loads(resp.read())

    def _ocr_captcha(self):
        """调用 Apple Vision Swift OCR"""
        try:
            subprocess.run(["swift", OCR_SCRIPT], capture_output=True, timeout=10)
            result_file = "/tmp/ocr_result.txt"
            if os.path.exists(result_file):
                with open(result_file) as f:
                    return f.read().strip()
        except Exception:
            pass
        return None

    def _get_login_captcha(self):
        """获取登录验证码图片"""
        timestamp = int(time.time() * 1000)
        url = f"{BASE_URL}/api/auth/captcha/getCaptcha?v={timestamp}"
        resp = self.opener.open(url, timeout=10)
        captcha_path = "/tmp/miaoshou_captcha.png"
        with open(captcha_path, "wb") as f:
            f.write(resp.read())
        return captcha_path

    def login(self):
        """登录妙手ERP (OCR验证码 + AES加密)"""
        # 获取验证码
        captcha_path = self._get_login_captcha()
        time.sleep(1)

        # OCR识别
        captcha = self._ocr_captcha()
        if not captcha or len(captcha) != 4:
            raise RuntimeError(f"OCR验证码失败: {captcha}")

        # AES加密密码
        encrypted = aes_encrypt("A@magic9")

        result = self._request("POST", "/api/auth/account/login", data={
            "mobile": "19864839993",
            "password": encrypted,
            "captcha": captcha,
        })

        if result.get("result") != "success":
            raise RuntimeError(f"登录失败: {result}")

        self.token = result.get("data", {}).get("token", "")
        return result

    def claim_to_tiktok(self, common_detail_id: int, platform: str = "tiktok"):
        """
        认领：从公用采集箱 → TikTok采集箱
        
        Args:
            common_detail_id: 公用采集箱详情ID (commonCollectBoxDetailId)
            platform: 平台 (默认 tiktok)
        """
        return self._request("POST", "/api/move/common_collect_box/claimed", data={
            "detailSerialNumberPlatformList[0][detailId]": str(common_detail_id),
            "detailSerialNumberPlatformList[0][platform]": platform,
            "detailSerialNumberPlatformList[0][serialNumber]": "1",
        }, extra_headers={"x-breadcrumb": "item-common-commonCollectBox"})

    def publish_to_shop(self, tk_detail_id: int, shop_ids: list):
        """
        发布：TikTok采集箱 → 店铺
        
        Args:
            tk_detail_id: TikTok采集箱详情ID
            shop_ids: 店铺ID列表
                7795399 = MagicPockets (全球店)
                8371977 = MagicPockets (菲律宾)
                7795400 = MagicPockets
                8460401 = MagicPockets
                8460416 = MagicPockets
                8460434 = MagicPockets
        
        Returns:
            {"result": "success", "data": {...}}
        """
        data = {f"detailIds[{i}]": str(tk_detail_id) for i in range(1)}
        for i, sid in enumerate(shop_ids):
            data[f"shopIds[{i}]"] = str(sid)

        return self._request("POST", "/api/platform/tiktok/move/collect_box/claimToShop",
            data=data,
            extra_headers={
                "x-breadcrumb": "item-tiktok-collectBox",
                "x-timestamp": str(int(time.time() * 1000)),
            })

    def publish_single(self, common_detail_id: int, shop_ids: list = None):
        """
        一键认领+发布 (完整流程)
        
        1. 认领到 TikTok 采集箱
        2. 发布到指定店铺
        
        Args:
            common_detail_id: 公用采集箱详情ID
            shop_ids: 店铺ID列表，默认 [7795399] 全球店
        
        Returns:
            {"claimed": {...}, "published": {...}}
        """
        if shop_ids is None:
            shop_ids = [7795399]  # 默认全球店

        if os.environ.get("MIAOSHOW_PUBLISH_ENABLED") != "true":
            raise RuntimeError("发布被阻止: MIAOSHOW_PUBLISH_ENABLED != true")

        # 1. 认领
        claim_result = self.claim_to_tiktok(common_detail_id)
        if claim_result.get("result") != "success":
            raise RuntimeError(f"认领失败: {claim_result}")

        # 2. 发布 (认领后需要获取 TikTok 采集箱的 detailId)
        time.sleep(2)

        # 搜索刚认领的商品
        search_result = self._request("POST", "/api/platform/tiktok/move/collect_box/searchCollectBoxDetail",
            data=json.dumps({"pageNo": 1, "pageSize": 5, "sort": {"gmtClaimed": "desc"}}),
            extra_headers={"x-breadcrumb": "item-tiktok-collectBox"})

        detail_list = search_result.get("data", {}).get("detailList", [])
        if not detail_list:
            raise RuntimeError("认领后未找到商品")

        tk_detail_id = detail_list[0]["id"]

        # 3. 发布到店铺
        publish_result = self.publish_to_shop(tk_detail_id, shop_ids)
        return {"claimed": claim_result, "published": publish_result}


# ── CLI ──

if __name__ == "__main__":
    print("用法: python3 shared/core/miaoshou_publish.py")
    print()
    print("发布前检查:")
    print(f"  MIAOSHOW_PUBLISH_ENABLED = {os.environ.get('MIAOSHOW_PUBLISH_ENABLED', 'false')}")
    print()
    print("店铺ID对照:")
    for sid, name in [
        (7795399, "MagicPockets 全球店"),
        (8371977, "MagicPockets 菲律宾"),
        (7795400, "MagicPockets"),
        (8460401, "MagicPockets"),
        (8460416, "MagicPockets"),
        (8460434, "MagicPockets"),
    ]:
        print(f"  {sid} → {name}")
