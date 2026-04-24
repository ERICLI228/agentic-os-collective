#!/usr/bin/env python3
"""多目录文件服务器"""
import http.server
import socketserver
from pathlib import Path

PORT = 8083
BASE_DIR = Path.home()

class MultiDirHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

with socketserver.TCPServer(("", PORT), MultiDirHandler) as httpd:
    print(f"📁 文件服务器已启动: http://localhost:{PORT}")
    httpd.serve_forever()
