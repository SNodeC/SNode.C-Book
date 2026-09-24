#!/usr/bin/env bash
set -euo pipefail
cd /workspace
export SNODEC_SOURCE_DIR=/workspace/external/snode.c
export SNODEC_PREFIX=/workspace/install/snodec
export BOOK_EXAMPLES_BUILD_DIR=/workspace/build/ci-book-examples
export SNODEC_BUILD_DIR=/workspace/build/snodec
mkdir -p build/verification-logs
{
  cat /etc/os-release
  "$CC" --version
  "$CXX" --version
} > build/verification-logs/toolchain.txt
python3 ci/check-chapter-references.py
python3 ci/check-source-alignment.py --framework "$SNODEC_SOURCE_DIR"
bash ci/build-companion-examples.sh
ctest --test-dir build/ci-book-examples --output-on-failure --no-tests=error | tee build/verification-logs/companion-ctest.txt
python3 ci/run-teaching-smoke-tests.py | tee build/verification-logs/teaching-smoke.txt
bash ci/run-behavior-smoke-tests.sh | tee build/verification-logs/behavior-smoke.txt
python3 ci/run-example-lifetime-tests.py --prefix "$SNODEC_PREFIX" --build "$BOOK_EXAMPLES_BUILD_DIR" --work build/example-lifetime-checks | tee build/verification-logs/example-lifetime-checks.txt
