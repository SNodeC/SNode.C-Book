#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

BUILD_DIR="${BOOK_BUILD_DIR:-build/ci-book}"
GENERATOR="${CMAKE_GENERATOR:-Ninja}"

cmake -S . -B "$BUILD_DIR" -G "$GENERATOR"

# Build twice intentionally. The second build verifies that LaTeX auxiliary
# state is preserved and recurring first-pass undefined-reference warnings do
# not reappear in the final logs.
cmake --build "$BUILD_DIR" --target proposal-package
cmake --build "$BUILD_DIR" --target proposal-package

logs=(
  "$BUILD_DIR/book-proposal-package.log"
  "$BUILD_DIR/book-proposal-sample-package.log"
  "$BUILD_DIR/snodec-book.log"
)

for log in "${logs[@]}"; do
  if [[ ! -f "$log" ]]; then
    echo "ERROR: expected LaTeX log not found: $log" >&2
    exit 1
  fi
  if grep -nE "undefined references|Reference .* undefined" "$log"; then
    echo "ERROR: unresolved LaTeX references remain in $log" >&2
    exit 1
  fi
done

pdfs=(
  "dist/pdf/book-proposal-package.pdf"
  "dist/pdf/book-proposal-sample-package.pdf"
  "dist/pdf/snodec-book.pdf"
)

for pdf in "${pdfs[@]}"; do
  if [[ ! -s "$pdf" ]]; then
    echo "ERROR: expected generated PDF missing or empty: $pdf" >&2
    exit 1
  fi
done

echo "Book package build passed."
