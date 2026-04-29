"""Aliyun NLS TTS shared module — water-margin-drama only TTS provider"""

import os, sys, json, time, hmac, hashlib, base64, uuid
from datetime import datetime
from urllib.parse import quote, urlencode
from pathlib import Path

ACCESS_KEY_ID = os.environ.get("ALIYUN_ACCESS_KEY_ID", "")
ACCESS_KEY_SECRET = os.environ.get("ALIYUN_ACCESS_KEY_SECRET", "")
APP_KEY = os.environ.get("ALIYUN_APP_KEY", "")

VOICE_MAP = {
    "武松": "zhiming",
    "宋江": "zhiyuan",
    "李逵": "zhihao",
    "林冲": "zhiming",
    "鲁智深": "zhihao",
    "旁白": "zhiqi",
    "default": "zhiming",
}

def _encode(s):
    return quote(str(s), safe='~').replace('+', '%20').replace('*', '%2A').replace('%7E', '~')

def _get_token():
    ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = str(uuid.uuid4())
    params = [
        ('AccessKeyId', ACCESS_KEY_ID), ('Action', 'CreateToken'), ('Format', 'JSON'),
        ('SignatureMethod', 'HMAC-SHA1'), ('SignatureNonce', nonce),
        ('SignatureVersion', '1.0'), ('Timestamp', ts), ('Version', '2019-02-28'),
    ]
    canonical = '&'.join(sorted(_encode(k) + '=' + _encode(v) for k, v in params))
    sign_str = 'GET&' + _encode('/') + '&' + _encode(canonical)
    sig = base64.b64encode(hmac.new((ACCESS_KEY_SECRET + '&').encode(), sign_str.encode(), hashlib.sha1).digest()).decode()
    params.append(('Signature', sig))
    qs = urlencode([(k, v) for k, v in params], quote_via=quote)
    import urllib.request
    resp = urllib.request.urlopen(f'https://nls-meta.cn-shanghai.aliyuncs.com/?{qs}', timeout=10)
    data = json.loads(resp.read())
    return data['Token']['Id']

def synthesize(text, voice="zhiming", output_path=None):
    if output_path is None:
        output_path = f"/tmp/tts_nls_{datetime.now().strftime('%H%M%S')}_{uuid.uuid4().hex[:6]}.mp3"
    try:
        token = _get_token()
        qs = urlencode([
            ('appkey', APP_KEY), ('token', token), ('text', text),
            ('voice', voice), ('format', 'mp3'), ('sample_rate', '16000'),
            ('volume', '50'), ('speech_rate', '0'), ('pitch_rate', '0'),
        ], quote_via=quote)
        import urllib.request
        resp = urllib.request.urlopen(f'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts?{qs}', timeout=30)
        data = resp.read()
        Path(output_path).write_bytes(data)
        return output_path
    except Exception as e:
        print(f"⚠️  NLS TTS 失败 (voice={voice}): {e}")
        return ""
