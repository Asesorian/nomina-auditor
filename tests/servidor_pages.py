"""Servidor local que imita las cabeceras de caché de GitHub Pages.

GitHub Pages sirve index.html con "Cache-Control: max-age=600" y ETag. Sirve para
comprobar que, tras publicar, la app carga la versión nueva a la primera.

Uso: python tests/servidor_pages.py <carpeta> [puerto]
"""
import hashlib
import http.server
import os
import sys

ROOT = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8766


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "max-age=600")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        self._etag = None
        if os.path.isfile(path):
            with open(path, "rb") as f:
                etag = '"' + hashlib.md5(f.read()).hexdigest() + '"'
            if self.headers.get("If-None-Match") == etag:
                self.send_response(304)
                self.send_header("ETag", etag)
                self.end_headers()
                return None
            self._etag = etag
        return super().send_head()

    def send_response(self, code, message=None):
        super().send_response(code, message)
        if code == 200 and getattr(self, "_etag", None):
            self.send_header("ETag", self._etag)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
