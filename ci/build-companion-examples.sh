#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

GENERATOR="${CMAKE_GENERATOR:-Ninja}"
SNODEC_PREFIX="${SNODEC_PREFIX:-$REPO_ROOT/install/snodec}"
SNODEC_BUILD_DIR="${SNODEC_BUILD_DIR:-$REPO_ROOT/build/snodec}"
BOOK_EXAMPLES_BUILD_DIR="${BOOK_EXAMPLES_BUILD_DIR:-$REPO_ROOT/build/ci-book-examples}"
PARALLEL="${CMAKE_BUILD_PARALLEL_LEVEL:-2}"
LOG_DIR="$REPO_ROOT/build/verification-logs"
mkdir -p "$LOG_DIR"
python3 ci/check-source-alignment.py

if [[ -n "${SNODEC_SOURCE_DIR:-}" ]]; then
  echo "Observed SNode.C master HEAD: $(git -C "$SNODEC_SOURCE_DIR" rev-parse HEAD)"
  python3 ci/check-source-alignment.py --framework "$SNODEC_SOURCE_DIR"
  cmake -S "$SNODEC_SOURCE_DIR" -B "$SNODEC_BUILD_DIR" -G "$GENERATOR" \
    -DCMAKE_BUILD_TYPE=Debug \
    -DSNODEC_BUILD_TESTS=ON -DSNODEC_BUILD_APPS=ON \
    -DCMAKE_INSTALL_PREFIX="$SNODEC_PREFIX"
  cmake --build "$SNODEC_BUILD_DIR" --parallel "$PARALLEL"
  ctest --test-dir "$SNODEC_BUILD_DIR" --show-only=json-v1 > "$LOG_DIR/framework-test-inventory.json"
  ctest --test-dir "$SNODEC_BUILD_DIR" --output-on-failure --no-tests=error \
    | tee "$LOG_DIR/framework-ctest.txt"
  cmake --install "$SNODEC_BUILD_DIR"

  ECHO_BUILD="$REPO_ROOT/build/framework-external-echo"
  cmake -S "$SNODEC_SOURCE_DIR/examples/echo" -B "$ECHO_BUILD" -G "$GENERATOR" \
    -DCMAKE_BUILD_TYPE=Debug -DBUILD_TESTING=ON \
    -DCMAKE_PREFIX_PATH="$SNODEC_PREFIX"
  cmake --build "$ECHO_BUILD" --parallel "$PARALLEL"
  LD_LIBRARY_PATH="$SNODEC_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    ctest --test-dir "$ECHO_BUILD" --output-on-failure --no-tests=error \
    | tee "$LOG_DIR/framework-external-echo-ctest.txt"
else
  echo "NOTICE: using a supplied installation; this run does not verify its framework commit or run framework CTests."
fi

if [[ ! -d "$SNODEC_PREFIX" ]]; then
  echo "ERROR: SNode.C install prefix not found: $SNODEC_PREFIX" >&2
  exit 1
fi

cmake -S . -B "$BOOK_EXAMPLES_BUILD_DIR" -G "$GENERATOR" \
  -DSNODEC_BOOK_BUILD_PDFS=OFF \
  -DSNODEC_BOOK_BUILD_COMPANION_EXAMPLES=ON \
  -DCMAKE_PREFIX_PATH="$SNODEC_PREFIX"
cmake --build "$BOOK_EXAMPLES_BUILD_DIR" --parallel "$PARALLEL"
echo "Companion example build passed."
