"""Minimal HTTP API over the DriftMonitor (Python stdlib only — no web framework).

  POST /baseline  {"feature": "age", "values": [...]}   -> register a baseline
  POST /check     {"feature": "age", "values": [...]}   -> DriftResult
  GET  /features                                          -> registered features
  GET  /health
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .monitor import DriftMonitor

monitor = DriftMonitor()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):  # keep the test/demo output clean
        pass

    def _send(self, code: int, obj) -> None:
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        length = int(self.headers.get("content-length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:
        if self.path == "/health":
            return self._send(200, {"ok": True})
        if self.path == "/features":
            return self._send(200, {"features": monitor.features})
        self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        try:
            data = self._body()
            feature, values = data.get("feature"), data.get("values")
            if not feature or not isinstance(values, list) or not values:
                return self._send(400, {"error": "feature and non-empty values[] required"})
            if self.path == "/baseline":
                monitor.set_baseline(feature, values)
                return self._send(200, {"feature": feature, "baseline_size": len(values)})
            if self.path == "/check":
                return self._send(200, monitor.check(feature, values).to_dict())
            self._send(404, {"error": "not found"})
        except KeyError as e:
            self._send(404, {"error": str(e)})
        except Exception as e:  # noqa: BLE001 - surface a clean error to the client
            self._send(500, {"error": str(e)})


def main(port: int = 8000) -> None:
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"DriftWatch Pro listening on :{port}")
    server.serve_forever()


if __name__ == "__main__":
    import os

    main(int(os.environ.get("PORT", "8000")))
