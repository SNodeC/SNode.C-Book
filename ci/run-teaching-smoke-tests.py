#!/usr/bin/env python3
"""Observe the complete Chapter 3 and 18 companions, without external services."""
from __future__ import annotations

import contextlib
import json
import os
import pathlib
import signal
import socket
import subprocess
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = pathlib.Path(os.environ.get("BOOK_EXAMPLES_BUILD_DIR", ROOT / "build/ci-book-examples"))
PREFIX = pathlib.Path(os.environ.get("SNODEC_PREFIX", ROOT / "install/snodec"))
LOGS = ROOT / "build/teaching-smoke-logs"


def executable(name: str) -> pathlib.Path:
    matches = [p for p in BUILD.rglob(name) if p.is_file() and os.access(p, os.X_OK)]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one {name} below {BUILD}, found {matches}")
    return matches[0]


def environment(config_home: str) -> dict[str, str]:
    env = dict(os.environ)
    env["XDG_CONFIG_HOME"] = config_home
    directories = sorted({str(p.parent) for p in PREFIX.rglob("*.so*") if p.is_file()})
    env["LD_LIBRARY_PATH"] = ":".join(directories + [env.get("LD_LIBRARY_PATH", "")])
    return env


def receive_exact(peer: socket.socket, size: int) -> bytes:
    result = bytearray()
    while len(result) < size:
        chunk = peer.recv(size - len(result))
        if not chunk:
            raise RuntimeError(f"Peer closed after {len(result)} of {size} bytes")
        result.extend(chunk)
    return bytes(result)


@contextlib.contextmanager
def running(name: str, args: list[str], env: dict[str, str]):
    path = LOGS / f"{name}.log"
    with path.open("wb") as output:
        process = subprocess.Popen([str(executable(name)), *args], env=env,
                                   stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT)
        try:
            yield process
        finally:
            if process.poll() is None:
                process.send_signal(signal.SIGINT)
                try:
                    process.wait(timeout=12)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
                    raise RuntimeError(f"{name} did not stop after SIGINT; see {path}")


def logging_check(env: dict[str, str]) -> None:
    run = subprocess.run([str(executable("semantic-logging"))], env=env, capture_output=True,
                         text=True, timeout=10, check=True)
    (LOGS / "semantic-logging.jsonl").write_text(run.stdout)
    records = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    if len(records) != 4:
        raise RuntimeError(f"Expected four demonstration records, got {len(records)}")
    for record in records:
        for key, expected in {"origin": "application", "boundary": "application",
                              "component": "gateway.measurements", "instance": "measurement-input"}.items():
            if record.get(key) != expected:
                raise RuntimeError(f"Semantic field {key} differs: {record}")
    if [r["level"] for r in records] != ["info", "info", "debug", "warn"]:
        raise RuntimeError("Semantic severity/component override result differs")
    if records[1].get("event") != "measurement.accepted":
        raise RuntimeError("Stable event identity missing")
    if not records[3].get("error") or "no file operation" not in records[3]["message"]:
        raise RuntimeError("Explicit demonstration error missing")
    print("PASS: Chapter 13 public logging fields, event, override, and typed error")


def server_check(env: dict[str, str]) -> None:
    with socket.socket() as reserved:
        reserved.bind(("127.0.0.1", 0))
        port = reserved.getsockname()[1]
    args = ["--monochrom=true", "--log-level=5", "echoserver", "local", "--host", "127.0.0.1", "--port", str(port)]
    with running("echoserver", args, env) as process:
        deadline = time.monotonic() + 10
        peer = None
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError("Echo server exited before accepting the controlled peer")
            try:
                peer = socket.create_connection(("127.0.0.1", port), timeout=0.3)
                break
            except OSError:
                time.sleep(0.05)
        if peer is None:
            raise RuntimeError("Echo server did not become reachable")
        with peer:
            peer.settimeout(5)
            payload = b"book-echo-\x00-boundary\n" * 5
            peer.sendall(payload)
            if receive_exact(peer, len(payload)) != payload:
                raise RuntimeError("Echo server changed the byte sequence")
    print("PASS: Chapter 3 server reflects a controlled byte sequence")


def client_check(env: dict[str, str]) -> None:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(10)
        args = ["--monochrom=true", "--log-level=5", "echoclient", "remote", "--host", "127.0.0.1",
                "--port", str(listener.getsockname()[1])]
        with running("echoclient", args, env):
            peer, _ = listener.accept()
            with peer:
                peer.settimeout(5)
                greeting = b"Hello peer! Nice to see you!!!"
                if receive_exact(peer, len(greeting)) != greeting:
                    raise RuntimeError("Echo client greeting differs from the complete listing")
                payload = b"response-from-controlled-peer"
                peer.sendall(payload)
                if receive_exact(peer, len(payload)) != payload:
                    raise RuntimeError("Echo client changed the reflected bytes")
    print("PASS: Chapter 3 client initiates and reflects with a controlled peer")


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="snodec-book-teaching-") as temp:
        env = environment(temp)
        logging_check(env)
        server_check(env)
        client_check(env)


if __name__ == "__main__":
    main()
