#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

export BOOK_EXAMPLES_BUILD_DIR="${BOOK_EXAMPLES_BUILD_DIR:-${REPO_ROOT}/build/ci-book-examples}"
export SNODEC_PREFIX="${SNODEC_PREFIX:-${REPO_ROOT}/install/snodec}"

python3 "${SCRIPT_DIR}/run-behavior-smoke-tests.py"
