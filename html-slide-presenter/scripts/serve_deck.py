#!/usr/bin/env python3
"""
🎙️ HTML Dual Slide Presenter - Zero-Dependency Local Wireless Sync Server
-------------------------------------------------------------------------
Runs on your presentation machine (MacBook):
- Projector: Fullscreen slides at http://localhost:8080/slides
- Mobile Phone/iPad: Touch remote & speaker notes at http://<MAC_IP>:8080/presenter
"""

import argparse
import http.server
import json
import socket
import socketserver
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path

# Global Presentation State
state_lock = threading.Lock()
deck_state = {
    "currentSlide": 1,
    "timestamp": time.time()
}
subscribers = []


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

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)

            if parsed.path in ('/', '/slides', '/slide'):
                self.path = f"/{slides_file}"
                return super().do_GET()

            if parsed.path in ('/presenter', '/mobile', '/p'):
                self.path = f"/{presenter_file}"
                return super().do_GET()

            if parsed.path == '/api/state':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                with state_lock:
                    data = json.dumps(deck_state)
                self.wfile.write(data.encode('utf-8'))
                return

            if parsed.path == '/api/events':
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                queue = []
                with state_lock:
                    subscribers.append(queue)
                    init_msg = f"data: {json.dumps(deck_state)}\n\n"

                try:
                    self.wfile.write(init_msg.encode('utf-8'))
                    self.wfile.flush()

                    while True:
                        time.sleep(0.05)
                        if queue:
                            msg = queue.pop(0)
                            self.wfile.write(f"data: {json.dumps(msg)}\n\n".encode('utf-8'))
                            self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    with state_lock:
                        if queue in subscribers:
                            subscribers.remove(queue)
                return

            return super().do_GET()

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)

            if parsed.path == '/api/sync':
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length).decode('utf-8')
                try:
                    data = json.loads(body)
                    slide_num = int(data.get('slide', 1))

                    with state_lock:
                        deck_state['currentSlide'] = slide_num
                        deck_state['timestamp'] = time.time()
                        payload = dict(deck_state)

                        for q in subscribers:
                            q.append(payload)

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(b'{"status":"ok"}')
                except Exception as e:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                return

            self.send_response(404)
            self.end_headers()

        def log_message(self, format, *args):
            if '/api/' not in args[0]:
                super().log_message(format, *args)

    return SlideSyncHTTPHandler


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main():
    parser = argparse.ArgumentParser(description="Serve Dual Slide Presentation with Wireless Mobile Presenter Sync")
    parser.add_argument("dir", nargs="?", default=".", help="Directory containing the HTML slide deck (default: .)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to serve on (default: 8080)")
    parser.add_argument("--slides", default="", help="Main slides HTML filename")
    parser.add_argument("--presenter", default="", help="Presenter view HTML filename")
    args = parser.parse_args()

    serve_dir = Path(args.dir).resolve()
    
    # Auto-detect filenames if not provided
    slides_file = args.slides
    presenter_file = args.presenter

    if not slides_file:
        for f in serve_dir.glob("*_slides.html"):
            slides_file = f.name
            break
        if not slides_file:
            for f in serve_dir.glob("*.html"):
                if "presenter" not in f.name:
                    slides_file = f.name
                    break

    if not presenter_file:
        for f in serve_dir.glob("*_presenter.html"):
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
    print(" 🎙️  DUAL SLIDE & WIRELESS PRESENTER SERVER ")
    print("═" * 68)
    print(f"\n 💻 [맥북 프로젝터 송출 주소]")
    print(f"    👉 {mac_url}")
    print(f"\n 📱 [스마트폰/아이패드 발표자 리모컨 주소]")
    print(f"    👉 {phone_url}")
    print("\n" + "─" * 68)
    print(" 💡 [스마트폰 연결 방법]")
    print(f"  1. 휴대폰을 맥북과 동일한 Wi-Fi (또는 맥북 핫스팟)에 연결합니다.")
    print(f"  2. 모바일 사파리/크롬 주소창에 아래 주소를 입력하세요:")
    print(f"     ★  {phone_url}  ★")
    print("  3. 폰에서 스와이프하거나 버튼을 누르면 맥북 화면이 즉시 넘어갑니다!")
    print("═" * 68 + "\n")

    threading.Thread(target=lambda: (time.sleep(0.5), webbrowser.open(mac_url)), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 서버를 종료합니다.")
        httpd.shutdown()


if __name__ == "__main__":
    main()
