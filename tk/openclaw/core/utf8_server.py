#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir(os.path.expanduser("~"))
PORT = 8080

class UTF8Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        super().end_headers()

# 用默认端口和目录
os.chdir('~')
httpd = socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
print(f"Server started on port {PORT}")
httpd.serve_forever()
