#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

GENERATOR="${CMAKE_GENERATOR:-Ninja}"
SNODEC_PREFIX="${SNODEC_PREFIX:-$REPO_ROOT/install/snodec}"
SNODEC_BUILD_DIR="${SNODEC_BUILD_DIR:-$REPO_ROOT/build/snodec}"
BOOK_EXAMPLES_BUILD_DIR="${BOOK_EXAMPLES_BUILD_DIR:-$REPO_ROOT/build/ci-book-examples}"

if [[ -n "${SNODEC_SOURCE_DIR:-}" ]]; then
  if [[ ! -d "$SNODEC_SOURCE_DIR" ]]; then
    echo "ERROR: SNODEC_SOURCE_DIR does not exist: $SNODEC_SOURCE_DIR" >&2
    exit 1
  fi

  cmake -S "$SNODEC_SOURCE_DIR" -B "$SNODEC_BUILD_DIR" -G "$GENERATOR" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$SNODEC_PREFIX"
  cmake --build "$SNODEC_BUILD_DIR"
  cmake --install "$SNODEC_BUILD_DIR"
fi

if [[ ! -d "$SNODEC_PREFIX" ]]; then
  echo "ERROR: SNode.C install prefix not found: $SNODEC_PREFIX" >&2
  echo "Set SNODEC_PREFIX to an installed SNode.C prefix, or set SNODEC_SOURCE_DIR so this script can build and install it." >&2
  exit 1
fi

cmake -S . -B "$BOOK_EXAMPLES_BUILD_DIR" -G "$GENERATOR" \
  -DSNODEC_BOOK_BUILD_PDFS=OFF \
  -DSNODEC_BOOK_BUILD_COMPANION_EXAMPLES=ON \
  -DCMAKE_PREFIX_PATH="$SNODEC_PREFIX"
cmake --build "$BOOK_EXAMPLES_BUILD_DIR"

echo "Companion example build passed."
