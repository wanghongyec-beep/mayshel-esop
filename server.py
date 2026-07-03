#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MES 操作指导书 - HTTP 服务器
在局域网内共享 HTML 操作手册
"""

import http.server
import socket
import sys
import os

PORT = 8000
DIR = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def log_message(self, format, *args):
        sys.stderr.write("[%s] %s - %s\n" % (
            self.log_date_time_string(),
            self.client_address[0],
            format % args
        ))

if __name__ == "__main__":
    local_ip = get_local_ip()

    print("=" * 55)
    print("  MES 操作指导书 - HTTP 服务器")
    print("=" * 55)
    print(f"\n  本机地址:    http://localhost:{PORT}")
    print(f"  局域网地址:  http://{local_ip}:{PORT}")
    print(f"  共享目录:    {DIR}")
    print(f"\n  其他设备访问方法：")
    print(f"  ① 确保手机/电脑连接同一个 WiFi/网络")
    print(f"  ② 浏览器打开: http://{local_ip}:{PORT}")
    print(f"\n  按 Ctrl+C 停止服务器")
    print("=" * 55)

    try:
        server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.server_close()
    except PermissionError:
        print(f"\n❌ 端口 {PORT} 被占用，尝试其他端口...")
        for port in range(PORT + 1, PORT + 10):
            try:
                server = http.server.HTTPServer(("0.0.0.0", port), Handler)
                print(f"✅ 已使用端口 {port}")
                print(f"   访问地址: http://{local_ip}:{port}")
                server.serve_forever()
            except:
                continue
            break
