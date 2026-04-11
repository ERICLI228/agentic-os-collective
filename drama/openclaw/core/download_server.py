#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir(os.path.expanduser("~"))
PORT = 8080

class DownloadHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        path = self.path
        if path.endswith('.txt') or path.endswith('.mp4') or path.endswith('.json'):
            filename = os.path.basename(path)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        super().end_headers()

httpd = socketserver.TCPServer(("", PORT), DownloadHandler)
print(f"Server with download headers on port {PORT}")
httpd.serve_forever()
