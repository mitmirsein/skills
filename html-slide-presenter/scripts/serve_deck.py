#!/usr/bin/env python3
"""
🎙️ HTML Dual Slide & Presenter Server (Ultra-Fast Local Wireless Sync)
-----------------------------------------------------------------------
Zero-cache, ultra-reliable real-time sync between:
- MacBook Screen (Projector): http://localhost:<PORT>/slides
- iPhone / iPad (Remote):     http://<LOCAL_IP>:<PORT>/presenter
"""

import argparse
import http.server
import json
import socket
import socketserver
import sys
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

# Global In-Memory Presentation State
state_lock = threading.Lock()
deck_state = {
    "slide": 1,
    "version": 1,
    "timestamp": time.time()
}


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def create_handler(serve_dir: Path, slides_file: str, presenter_file: str):
    class SlideSyncHTTPHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(serve_dir), **kwargs)

        def end_headers(self):
            # Force browser never to cache presentation files
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)

            # Route aliases
            if parsed.path in ('/', '/slides', '/slide'):
                self.path = f"/{slides_file}"
                return super().do_GET()

            if parsed.path in ('/presenter', '/mobile', '/p'):
                self.path = f"/{presenter_file}"
                return super().do_GET()

            # State API (Fast Polling)
            if parsed.path in ('/api/state', '/api/poll'):
                with state_lock:
                    data = json.dumps(deck_state).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

            # Server & Network Info API (used for on-screen QR Code generation)
            if parsed.path == '/api/info':
                local_ip = get_local_ip()
                port = self.server.server_address[1]
                info = {
                    "localIp": local_ip,
                    "port": port,
                    "presenterUrl": f"http://{local_ip}:{port}/presenter",
                    "slidesUrl": f"http://localhost:{port}/slides"
                }
                data = json.dumps(info).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

            return super().do_GET()

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)

            # Slide Change Command
            if parsed.path in ('/api/slide', '/api/sync'):
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length).decode('utf-8')

                try:
                    data = json.loads(body)
                    slide_num = int(data.get('slide', 1))

                    with state_lock:
                        deck_state['slide'] = slide_num
                        deck_state['version'] += 1
                        deck_state['timestamp'] = time.time()
                        resp = dict(deck_state)

                    resp_bytes = json.dumps(resp).encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Content-Length', str(len(resp_bytes)))
                    self.end_headers()
                    self.wfile.write(resp_bytes)
                    print(f"🚀 [SYNC] Slide changed -> #{slide_num} (Version {deck_state['version']})")
                except Exception as e:
                    err = json.dumps({"error": str(e)}).encode('utf-8')
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Content-Length', str(len(err)))
                    self.end_headers()
                    self.wfile.write(err)
                return

            self.send_response(404)
            self.end_headers()

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Cache-Control')
            self.end_headers()

        def log_message(self, format, *args):
            try:
                msg = format % args
                if '/api/state' not in msg and '/api/poll' not in msg:
                    sys.stderr.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
            except Exception:
                pass

    return SlideSyncHTTPHandler


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser(description="Serve HTML presentation deck with mobile remote sync & QR code")
    parser.add_argument("dir", nargs="?", default=".", help="Directory containing the HTML slide deck (default: .)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to serve on (default: 8080)")
    parser.add_argument("--slides", default="", help="Main slides HTML filename")
    parser.add_argument("--presenter", default="", help="Presenter view HTML filename")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open browser")
    args = parser.parse_args()

    serve_dir = Path(args.dir).resolve()

    slides_file = args.slides
    presenter_file = args.presenter

    if not slides_file:
        for f in sorted(serve_dir.glob("*_slides.html")):
            slides_file = f.name
            break
        if not slides_file:
            for f in sorted(serve_dir.glob("*.html")):
                if "presenter" not in f.name:
                    slides_file = f.name
                    break

    if not presenter_file:
        for f in sorted(serve_dir.glob("*_presenter.html")):
            presenter_file = f.name
            break

    slides_file = slides_file or "index.html"
    presenter_file = presenter_file or "presenter.html"

    local_ip = get_local_ip()
    port = args.port

    handler_class = create_handler(serve_dir, slides_file, presenter_file)

    try:
        httpd = ThreadedTCPServer(('0.0.0.0', port), handler_class)
    except OSError:
        port += 1
        httpd = ThreadedTCPServer(('0.0.0.0', port), handler_class)

    mac_url = f"http://localhost:{port}/slides"
    phone_url = f"http://{local_ip}:{port}/presenter"

    print("\n" + "═" * 68)
    print(" 🎙️  HTML DUAL SLIDE & WIRELESS PRESENTER SERVER ")
    print("═" * 68)
    print(f"\n 💻 [맥북 프로젝터 송출 화면]")
    print(f"    👉 {mac_url}")
    print(f"\n 📱 [아이폰 / 아이패드 발표자 리모컨]")
    print(f"    👉 {phone_url}")
    print("\n" + "─" * 68)
    print(" 💡 [연결 및 QR 코드 안내]")
    print(f"  1. 맥북 화면에서 'Q' 키를 누르면 모바일 접속용 QR 코드가 팝업됩니다.")
    print(f"  2. 스마트폰 카메라로 QR 코드를 비추거나 아래 주소로 접속하세요:")
    print(f"     ★  {phone_url}  ★")
    print("  3. 폰에서 스와이프하거나 버튼을 터치하면 맥북 화면이 실시간으로 전환됩니다.")
    print("═" * 68 + "\n")

    if not args.no_browser:
        threading.Thread(target=lambda: (time.sleep(0.3), webbrowser.open(mac_url)), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
        httpd.shutdown()


if __name__ == '__main__':
    main()
