#!/usr/bin/env bash
set -uo pipefail
cd /workspace
export SNODEC_SOURCE_DIR=/workspace/external/snode.c
export SNODEC_PREFIX=/workspace/install/snodec
export BOOK_EXAMPLES_BUILD_DIR=/workspace/build/ci-book-examples
export SNODEC_BUILD_DIR=/workspace/build/snodec
result=0
python3 ci/run-teaching-smoke-tests.py | tee build/verification-logs/teaching-smoke.txt || result=1
bash ci/run-behavior-smoke-tests.sh | tee build/verification-logs/behavior-smoke.txt || result=1
python3 ci/run-example-lifetime-tests.py --prefix "$SNODEC_PREFIX" --build "$BOOK_EXAMPLES_BUILD_DIR" --work build/example-lifetime-checks | tee build/verification-logs/example-lifetime-checks.txt || result=1
ctest --test-dir build/ci-book-examples --output-on-failure --no-tests=error --repeat until-fail:50 -R '^exercise-ch07-' | tee build/verification-logs/ch07-repeat50.txt || result=1
exit "$result"
