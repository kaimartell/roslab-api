from __future__ import annotations

import argparse
from http import HTTPStatus
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import signal
from typing import Any
from urllib.parse import parse_qs, urlparse

from roslab_api.system_metadata import build_system_metadata


UNSUPPORTED_LAUNCH_ERROR = (
    "Demo launch is not configured in this connector package. "
    "This package only exposes the existing ROS environment."
)


def _unsupported_demo_status(demo_id: str | None = None) -> dict[str, object]:
    return {
        "id": demo_id or "",
        "status": "not_configured",
        "detail": UNSUPPORTED_LAUNCH_ERROR,
    }


class BridgeApiHttpServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int]) -> None:
        super().__init__(server_address, BridgeApiRequestHandler)
        self.system_metadata = build_system_metadata()


class BridgeApiRequestHandler(BaseHTTPRequestHandler):
    server: BridgeApiHttpServer

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._write_json(
                HTTPStatus.OK,
                {"ok": True, "service": "bridge_api", "version": 1},
            )
            return

        if parsed.path == "/api/launch/demos":
            self._write_json(HTTPStatus.OK, {"demos": [], "count": 0})
            return

        if parsed.path == "/api/launch/status":
            params = parse_qs(parsed.query)
            demo_id = params.get("demo_id", [None])[0]
            if demo_id is None:
                self._write_json(HTTPStatus.OK, {"statuses": []})
            else:
                self._write_json(
                    HTTPStatus.OK,
                    {"status": _unsupported_demo_status(str(demo_id))},
                )
            return

        if parsed.path == "/api/launch/logs":
            params = parse_qs(parsed.query)
            demo_id = params.get("demo_id", [""])[0]
            self._write_json(
                HTTPStatus.OK,
                {
                    "demo_id": str(demo_id),
                    "status": _unsupported_demo_status(str(demo_id)),
                    "lines": [],
                    "line_count": 0,
                    "available_line_count": 0,
                },
            )
            return

        if parsed.path == "/api/system/metadata":
            self._write_json(
                HTTPStatus.OK,
                {"system_metadata": self.server.system_metadata},
            )
            return

        if parsed.path == "/api/system/code":
            self._write_json(
                HTTPStatus.NOT_FOUND,
                {
                    "ok": False,
                    "error": "No curated node code is bundled with this connector package.",
                },
            )
            return

        if parsed.path == "/api/concept-code/templates":
            self._write_json(HTTPStatus.OK, {"templates": [], "count": 0})
            return

        if parsed.path == "/api/concept-code/sessions":
            self._write_json(HTTPStatus.OK, {"sessions": [], "count": 0})
            return

        if parsed.path == "/api/concept-code/session":
            self._write_json(
                HTTPStatus.NOT_FOUND,
                {
                    "ok": False,
                    "error": "Concept-code sessions are not configured in this connector package.",
                },
            )
            return

        if parsed.path == "/api/concept-code/events":
            params = parse_qs(parsed.query)
            session_id = str(params.get("session_id", [""])[0])
            self._write_json(
                HTTPStatus.OK,
                {
                    "session_id": session_id,
                    "events": [],
                    "count": 0,
                    "next_after_sequence": 0,
                },
            )
            return

        self._write_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found."})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {
            "/api/launch/start",
            "/api/launch/restart",
            "/api/launch/stop",
            "/api/concept-code/sessions/start",
            "/api/concept-code/sessions/stop",
        }:
            self._write_json(
                HTTPStatus.NOT_IMPLEMENTED,
                {"ok": False, "error": UNSUPPORTED_LAUNCH_ERROR},
            )
            return

        self._write_json(HTTPStatus.NOT_FOUND, {"ok": False, "error": "Not found."})

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def log_message(self, format: str, *args: Any) -> None:
        del format, args

    def _write_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the minimal bridge API server.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    httpd = BridgeApiHttpServer((args.host, args.port))

    def _shutdown(_signum: int, _frame: Any) -> None:
        httpd.shutdown()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
