#!/usr/bin/env python3
"""Runtime smoke tests for selected SNode.C book companion examples.

The companion CI already proves that every example compiles against the pinned
SNode.C release.  This script adds a deliberately small behavior check for the
showcase paths that matter to the manuscript package:

* SSE-Server emits a well-formed measurement event stream.
* MiniGateway Extended accepts a measurement through its Unix-domain input role
  and exposes the resulting model state through HTTP/SSE.

These are smoke tests, not broad integration tests.  They avoid external MQTT
brokers, OpenWrt packaging, long-running services, and timing-sensitive load
checks.
"""

from __future__ import annotations

import json
import os
import pathlib
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD_DIR = pathlib.Path(os.environ.get("BOOK_EXAMPLES_BUILD_DIR", REPO_ROOT / "build" / "ci-book-examples"))
SNODEC_PREFIX = pathlib.Path(os.environ.get("SNODEC_PREFIX", REPO_ROOT / "install" / "snodec"))
LOG_DIR = pathlib.Path(os.environ.get("SNODEC_BOOK_SMOKE_LOG_DIR", REPO_ROOT / "build" / "behavior-smoke-logs"))
HOST = "127.0.0.1"
PORT = 8080
MEASUREMENT_SOCKET = pathlib.Path("/tmp/minigateway-measurements.sock")


class SmokeError(RuntimeError):
    pass


@dataclass
class ManagedProcess:
    label: str
    process: subprocess.Popen
    log_path: pathlib.Path

    def stop(self) -> None:
        if self.process.poll() is not None:
            return
        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.process.wait(timeout=3)

    def assert_alive(self) -> None:
        rc = self.process.poll()
        if rc is not None:
            raise SmokeError(f"{self.label} exited unexpectedly with status {rc}\n{tail(self.log_path)}")


def tail(path: pathlib.Path, lines: int = 80) -> str:
    if not path.exists():
        return f"log file not found: {path}"
    text = path.read_text(errors="replace").splitlines()
    return "\n".join(text[-lines:])


def smoke_env() -> Dict[str, str]:
    env = os.environ.copy()
    library_dirs = [SNODEC_PREFIX / "lib", SNODEC_PREFIX / "lib64"]
    existing = env.get("LD_LIBRARY_PATH", "")
    entries = [str(path) for path in library_dirs if path.is_dir()]
    if existing:
        entries.append(existing)
    if entries:
        env["LD_LIBRARY_PATH"] = ":".join(entries)
    return env


def find_executable(name: str) -> pathlib.Path:
    if not BUILD_DIR.is_dir():
        raise SmokeError(f"example build directory not found: {BUILD_DIR}")

    candidates = sorted(path for path in BUILD_DIR.rglob(name) if path.is_file() and os.access(path, os.X_OK))
    if not candidates:
        raise SmokeError(f"built example executable not found below {BUILD_DIR}: {name}")
    if len(candidates) > 1:
        # Prefer the direct target path if CMake has also staged/deployed a copy.
        direct = [path for path in candidates if "companion/examples" in str(path)]
        if direct:
            return direct[0]
    return candidates[0]


def start_process(executable: pathlib.Path, label: str) -> ManagedProcess:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{label}.log"
    log_file = log_path.open("w")
    process = subprocess.Popen(
        [str(executable)],
        cwd=str(executable.parent),
        env=smoke_env(),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    # The child owns the file descriptor now; closing our handle avoids leaks.
    log_file.close()
    managed = ManagedProcess(label=label, process=process, log_path=log_path)
    time.sleep(0.2)
    managed.assert_alive()
    return managed


def wait_for_tcp(host: str, port: int, process: ManagedProcess, timeout: float = 8.0) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        process.assert_alive()
        try:
            with socket.create_connection((host, port), timeout=0.4):
                return
        except OSError as exc:
            last_error = exc
            time.sleep(0.1)
    raise SmokeError(f"timed out waiting for {process.label} on {host}:{port}: {last_error}\n{tail(process.log_path)}")


def wait_for_unix_socket(path: pathlib.Path, process: ManagedProcess, timeout: float = 8.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        process.assert_alive()
        if path.exists():
            try:
                client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client.settimeout(0.4)
                client.connect(str(path))
                client.close()
                return
            except OSError:
                time.sleep(0.1)
        else:
            time.sleep(0.1)
    raise SmokeError(f"timed out waiting for Unix-domain socket: {path}\n{tail(process.log_path)}")


def raw_http(path: str, *, accept: str = "*/*", timeout: float = 5.0, read_stream: bool = False) -> Tuple[str, Dict[str, str], bytes]:
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Accept: {accept}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii")

    with socket.create_connection((HOST, PORT), timeout=timeout) as sock:
        sock.settimeout(0.4)
        sock.sendall(request)
        deadline = time.time() + timeout
        data = bytearray()

        while b"\r\n\r\n" not in data:
            if time.time() >= deadline:
                raise SmokeError(f"timed out reading HTTP headers for {path}")
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                continue
            if not chunk:
                break
            data.extend(chunk)

        header_blob, _, body = bytes(data).partition(b"\r\n\r\n")
        header_lines = header_blob.decode("iso-8859-1", errors="replace").split("\r\n")
        status_line = header_lines[0] if header_lines else ""
        headers: Dict[str, str] = {}
        for line in header_lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        if read_stream:
            while time.time() < deadline:
                if b"event: measurement" in body and b"data:" in body:
                    break
                try:
                    chunk = sock.recv(4096)
                except socket.timeout:
                    continue
                if not chunk:
                    break
                body += chunk
            return status_line, headers, body

        content_length = headers.get("content-length")
        if content_length is not None:
            try:
                expected_length = int(content_length)
            except ValueError:
                expected_length = None
            if expected_length is not None:
                while len(body) < expected_length and time.time() < deadline:
                    try:
                        chunk = sock.recv(4096)
                    except socket.timeout:
                        continue
                    if not chunk:
                        break
                    body += chunk
        else:
            # For non-stream responses without a declared length, read until the
            # peer closes or a short timeout leaves the body stable.
            while time.time() < deadline:
                try:
                    chunk = sock.recv(4096)
                except socket.timeout:
                    break
                if not chunk:
                    break
                body += chunk

        return status_line, headers, body

def assert_status(status_line: str, expected: int, path: str) -> None:
    needle = f" {expected} "
    if needle not in status_line:
        raise SmokeError(f"unexpected HTTP status for {path}: {status_line!r}")


def json_get(path: str) -> Dict[str, object]:
    status_line, headers, body = raw_http(path, accept="application/json")
    assert_status(status_line, 200, path)
    if "application/json" not in headers.get("content-type", ""):
        raise SmokeError(f"unexpected content type for {path}: {headers.get('content-type')!r}")
    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise SmokeError(f"invalid JSON body for {path}: {body!r}") from exc


def assert_sse_measurement(body: bytes, *, expected_sequence: int | None = None) -> Dict[str, object]:
    text = body.decode("utf-8", errors="replace")
    if "event: measurement" not in text:
        raise SmokeError(f"SSE response does not contain measurement event:\n{text}")
    if "id:" not in text or "data:" not in text:
        raise SmokeError(f"SSE response does not contain id/data fields:\n{text}")

    data_line = next((line for line in text.replace("\r\n", "\n").split("\n") if line.startswith("data:")), None)
    if data_line is None:
        raise SmokeError(f"SSE response has no data line:\n{text}")
    try:
        payload = json.loads(data_line.removeprefix("data:").strip())
    except json.JSONDecodeError as exc:
        raise SmokeError(f"SSE data line is not JSON: {data_line!r}") from exc

    if expected_sequence is not None and payload.get("sequence") != expected_sequence:
        raise SmokeError(f"unexpected SSE sequence: {payload!r}")
    return payload


def test_sse_server() -> None:
    executable = find_executable("sse-server")
    server = start_process(executable, "sse-server")
    try:
        wait_for_tcp(HOST, PORT, server)
        status_line, headers, body = raw_http("/events", accept="text/event-stream", read_stream=True)
        assert_status(status_line, 200, "/events")
        if "text/event-stream" not in headers.get("content-type", ""):
            raise SmokeError(f"unexpected SSE content type: {headers.get('content-type')!r}")
        payload = assert_sse_measurement(body, expected_sequence=1)
        if payload.get("sensor") != "temperature" or payload.get("value") != 23.5:
            raise SmokeError(f"unexpected initial SSE payload: {payload!r}")
    finally:
        server.stop()
        time.sleep(0.3)
    print("SSE-Server runtime smoke test passed.")


def send_measurement_line(line: str) -> None:
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.settimeout(2.0)
    try:
        client.connect(str(MEASUREMENT_SOCKET))
        client.sendall(line.encode("utf-8"))
    finally:
        client.close()


def wait_for_status_sequence(expected_sequence: int, process: ManagedProcess, timeout: float = 5.0) -> Dict[str, object]:
    deadline = time.time() + timeout
    last_payload: Dict[str, object] | None = None
    while time.time() < deadline:
        process.assert_alive()
        try:
            payload = json_get("/status")
            last_payload = payload
            if payload.get("sequence") == expected_sequence:
                return payload
        except Exception:
            pass
        time.sleep(0.1)
    raise SmokeError(f"timed out waiting for /status sequence {expected_sequence}; last payload: {last_payload!r}\n{tail(process.log_path)}")


def test_minigateway_extended_unix_input() -> None:
    try:
        MEASUREMENT_SOCKET.unlink()
    except FileNotFoundError:
        pass

    executable = find_executable("minigateway-extended")
    gateway = start_process(executable, "minigateway-extended")
    try:
        wait_for_tcp(HOST, PORT, gateway)
        wait_for_unix_socket(MEASUREMENT_SOCKET, gateway)

        health = json_get("/health")
        if health.get("ok") is not True:
            raise SmokeError(f"unexpected /health payload: {health!r}")

        send_measurement_line("21.5,45.0,3.8\n")
        status = wait_for_status_sequence(1, gateway)
        expected = {"temperature": 21.5, "humidity": 45.0, "voltage": 3.8, "sequence": 1}
        for key, value in expected.items():
            if status.get(key) != value:
                raise SmokeError(f"unexpected /status payload after Unix input: {status!r}")

        status_line, headers, body = raw_http("/events", accept="text/event-stream", read_stream=True)
        assert_status(status_line, 200, "/events")
        if "text/event-stream" not in headers.get("content-type", ""):
            raise SmokeError(f"unexpected MiniGateway SSE content type: {headers.get('content-type')!r}")
        sse_payload = assert_sse_measurement(body, expected_sequence=1)
        for key, value in expected.items():
            if sse_payload.get(key) != value:
                raise SmokeError(f"unexpected MiniGateway SSE payload after Unix input: {sse_payload!r}")
    finally:
        gateway.stop()
        try:
            MEASUREMENT_SOCKET.unlink()
        except FileNotFoundError:
            pass
        time.sleep(0.3)
    print("MiniGateway Extended Unix-input runtime smoke test passed.")


def main() -> int:
    print(f"Using example build directory: {BUILD_DIR}")
    print(f"Using SNode.C install prefix: {SNODEC_PREFIX}")
    test_sse_server()
    test_minigateway_extended_unix_input()
    print("Behavioral smoke tests passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SmokeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
