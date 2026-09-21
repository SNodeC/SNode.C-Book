#!/usr/bin/env python3
"""Rehearse the Chapter 17 and 32 exercises against an installed current tree."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--book", type=Path, required=True)
parser.add_argument("--prefix", type=Path, required=True)
parser.add_argument("--echo", type=Path, required=True)
args = parser.parse_args()

with tempfile.TemporaryDirectory(prefix="snodec-editorial-config-") as directory:
    scratch = Path(directory)
    config = scratch / "echo.conf"
    config.write_text("echoserver.local.port = 18091\n")
    env = dict(os.environ, XDG_CONFIG_HOME=str(scratch / "config-base"))
    failures = []
    for label, options, expected in (
        ("C++ default", [], 8080),
        ("file override", ["--config-file", str(config)], 18091),
        ("command-line override", ["--config-file", str(config),
          "echoserver", "local", "--port=18092"], 18092),
    ):
        result = subprocess.run([str(args.echo), "--show-config", *options],
                                env=env, capture_output=True, text=True, timeout=15)
        active = re.findall(r"^\s*echoserver\.local\.port\s*=\s*(\d+)",
                            result.stdout, re.MULTILINE)
        defaults = re.findall(r"^\s*#echoserver\.local\.port\s*=\s*(\d+)",
                              result.stdout, re.MULTILINE)
        values = active or defaults
        okay = result.returncode == 2 and values == [str(expected)]
        print(f"{label}: exit={result.returncode}, values={values}, expected={expected}: "
              f"{'PASS' if okay else 'FAIL'}", flush=True)
        if not okay:
            print(result.stdout, result.stderr)
            failures.append(label)
    assert config.read_text() == "echoserver.local.port = 18091\n"
    print("Command-line inspection leaves the file unchanged: PASS", flush=True)

    source = scratch / "EchoPair"
    shutil.copytree(args.book / "companion/examples/EchoPair", source)
    cmake = source / "CMakeLists.txt"
    original = cmake.read_text()
    cmake.write_text(original.replace("COMPONENTS net-in-stream-legacy",
                                     "COMPONENTS book-missing-component", 1))
    result = subprocess.run(["cmake", "-S", str(source), "-B", str(scratch / "missing"),
                             f"-DCMAKE_PREFIX_PATH={args.prefix}"],
                            capture_output=True, text=True, timeout=60)
    output = result.stdout + result.stderr
    okay = result.returncode != 0 and "book-missing-component" in output
    print(output, flush=True)
    print(f"Unsupported required component fails during configuration: {'PASS' if okay else 'FAIL'}",
          flush=True)
    if not okay:
        failures.append("missing component")
    cmake.write_text(original)
    for command in (
        ["cmake", "-S", str(source), "-B", str(scratch / "restored"),
         f"-DCMAKE_PREFIX_PATH={args.prefix}"],
        ["cmake", "--build", str(scratch / "restored"), "--parallel", "2"],
    ):
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        print(result.stdout, result.stderr, flush=True)
        if result.returncode:
            failures.append("restored component configure/build")
            break
    assert not failures, failures
    print("Configuration precedence and component exercises: PASS", flush=True)
