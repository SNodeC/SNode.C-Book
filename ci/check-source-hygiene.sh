#!/usr/bin/env bash
set -euo pipefail

# Run from repository root, regardless of the caller's current directory.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

fail=0

# Keep this list focused on files that belong to the source manuscript/package.
# Do not scan generated build trees, archived packages, logs, or historical review notes.
scan_roots=(
  "CMakeLists.txt"
  "README.md"
  "STRUCTURE.md"
  "manuscript"
  "review/proposal"
  "production/metadata"
  "production/filters"
  "production/latex"
  "packaging"
  "companion"
)

existing_roots=()
for path in "${scan_roots[@]}"; do
  if [[ -e "$path" ]]; then
    existing_roots+=("$path")
  fi
done

check_absent() {
  local pattern="$1"
  local label="$2"

  if grep -RInE \
      --exclude-dir=.git \
      --exclude-dir=build \
      --exclude-dir=dist \
      --exclude='*.pdf' \
      --exclude='*.tar.gz' \
      --exclude='*.zip' \
      --exclude='*.log' \
      "$pattern" "${existing_roots[@]}"; then
    echo "ERROR: found forbidden pattern: ${label}" >&2
    fail=1
  fi
}

check_absent '@fig:' '@fig references; use the established Figure~\\ref{...} style'
check_absent 'MiniGateway-Base|MiniGateway Base|base MiniGateway|basic MiniGateway' 'forbidden MiniGateway base naming'
check_absent 'startWebInstance|startMeasurementSocketServer|startMqttClient' 'old MiniGateway factory names'
check_absent '\bwebApp\b|\bmeasurementSocketServer\b|\bmqttClient\b' 'old MiniGateway role variable names'
check_absent 'sendMeasurementEvent' 'removed SSE helper/highlight name'
check_absent 'accept\.find\("text/event-stream"\)' 'case-sensitive SSE Accept check'
check_absent 'retry: 1000' 'old SSE retry output'
check_absent 'id:2' 'old compact SSE id output'
check_absent 'TODO|FIXME|PLACEHOLDER' 'authoring markers'

# Ordered chapter coverage and intended reference topics share one check.
python3 ci/check-chapter-references.py
python3 ci/test-chapter-references.py

python3 - <<'PY'
from pathlib import Path
import re
import runpy
import sys

# Reuse the measurement authority for reader-facing authoring-note guards.
metrics = runpy.run_path("ci/manuscript-metrics.py")
authoring_errors = 0
for name, item in metrics["manuscript_metrics"](Path.cwd(), Path("manuscript/book-files.txt").resolve())["files"].items():
    for phrase, hits in item["forbidden_phrase_hits"].items():
        for hit in hits:
            print(f"ERROR: {name}:{hit['line']}: forbidden authoring phrase: {phrase}", file=sys.stderr)
    authoring_errors += item["forbidden_phrase_hit_count"]
if authoring_errors:
    sys.exit(1)

roots = [Path("manuscript"), Path("review/proposal")]
files = []
for root in roots:
    if root.exists():
        files.extend(root.rglob("*.md"))

label_re = re.compile(r"\{[^}]*#(fig:[A-Za-z0-9_.:-]+)(?=[\s}])[^}]*\}")
ref_re = re.compile(r"\\ref\{(fig:[^}]+)\}")
labels = {}
refs = {}

def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1

for path in files:
    text = path.read_text(encoding="utf-8")
    for match in label_re.finditer(text):
        labels.setdefault(match.group(1), []).append((str(path), line_number(text, match.start())))
    for match in ref_re.finditer(text):
        refs.setdefault(match.group(1), []).append((str(path), line_number(text, match.start())))

missing = sorted(set(refs) - set(labels))
duplicates = {name: locs for name, locs in labels.items() if len(locs) > 1}

if missing:
    print("ERROR: missing figure labels for references:", file=sys.stderr)
    for name in missing:
        print(f"  {name}", file=sys.stderr)
        for file, line in refs[name]:
            print(f"    referenced at {file}:{line}", file=sys.stderr)

if duplicates:
    print("ERROR: duplicate figure labels:", file=sys.stderr)
    for name, locs in sorted(duplicates.items()):
        print(f"  {name}", file=sys.stderr)
        for file, line in locs:
            print(f"    defined at {file}:{line}", file=sys.stderr)

if missing or duplicates:
    sys.exit(1)
PY

if [[ "$fail" -ne 0 ]]; then
  exit "$fail"
fi

python3 ci/check-source-alignment.py

echo "Source hygiene checks passed."
