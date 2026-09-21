#!/usr/bin/env python3
"""Check edition declarations and exact, explicitly marked complete listings."""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def baseline() -> dict[str, str]:
    values: dict[str, str] = {}
    for line in (ROOT / "source-baseline/book-source-baseline.env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            key, separator, value = line.partition("=")
            if not separator or not re.fullmatch(r"SNODEC_[A-Z_]+", key):
                raise ValueError(f"Invalid baseline assignment: {line!r}")
            values[key] = value
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=pathlib.Path,
                        help="Also verify this framework checkout's HEAD and project version")
    args = parser.parse_args()
    errors: list[str] = []
    values = baseline()
    sha = values.get("SNODEC_COMMIT", "")
    version = values.get("SNODEC_VERSION", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        errors.append("Framework pin is not a full immutable commit SHA")
    if values.get("SNODEC_REF") != sha:
        errors.append("Checkout ref differs from the authoritative commit")
    if version != "2.0.0":
        errors.append("This migration's declared project version must be 2.0.0")
    for name in ["README.md", "source-baseline/SOURCE-VERSION.md",
                 "source-baseline/book-source-baseline.md",
                 "manuscript/frontmatter/preface.md", "review/proposal/book-proposal-package.md"]:
        text = (ROOT / name).read_text()
        if sha not in text or version not in text:
            errors.append(f"Missing current source pin/version in {name}")
    chapters = sorted((ROOT / "manuscript/chapters").glob("[0-9][0-9]-*.md"))
    if len(chapters) != 38:
        errors.append(f"Expected 38 numbered chapters, found {len(chapters)}")
    sources = list((ROOT / "manuscript").rglob("*.md"))
    sources += list((ROOT / "review/proposal").glob("*.md"))
    sources += list((ROOT / "assets/figures/src").glob("*.tex"))
    marked = re.compile(r"<!-- snodec-source: ([^\n]+?) -->\s*\n```(?:cpp|cmake)\n(.*?)\n```", re.S)
    count = 0
    for path in sources:
        text = path.read_text()
        if re.search(r"\b(?:LOG|PLOG|VLOG)\s*\(", text):
            errors.append(f"Removed macro logging surface remains in {path.relative_to(ROOT)}")
        if "v1.0.2" in text or "6e475262084ae2dab2daef8781ab9e4adb82d18e" in text:
            errors.append(f"Old reader-facing baseline remains in {path.relative_to(ROOT)}")
        for match in marked.finditer(text):
            source = (ROOT / match[1]).resolve()
            if not source.is_relative_to(ROOT / "companion/examples") or not source.is_file():
                errors.append(f"Invalid companion source marker: {match[1]}")
                continue
            count += 1
            if match[2].rstrip("\n") != source.read_text().rstrip("\n"):
                errors.append(f"Complete listing differs: {path.relative_to(ROOT)} -> {match[1]}")
    if count < 30:
        errors.append(f"Unexpectedly few checked complete listings: {count}")
    for name in (ROOT / "manuscript/book-files.txt").read_text().splitlines():
        if name.strip() and not (ROOT / name.strip()).is_file():
            errors.append(f"Manuscript input does not exist: {name}")
    workflow = (ROOT / ".github/workflows/companion-examples.yml").read_text()
    if "source-baseline/book-source-baseline.env" not in workflow:
        errors.append("Companion workflow does not read the baseline authority")
    if re.search(r"ref:\s*[0-9a-f]{40}", workflow):
        errors.append("Companion workflow duplicates a literal framework SHA")
    if args.framework:
        head = subprocess.check_output(["git", "-C", str(args.framework), "rev-parse", "HEAD"], text=True).strip()
        if head != sha:
            errors.append(f"Framework checkout is {head}, expected {sha}")
        cmake = (args.framework / "CMakeLists.txt").read_text()
        if not re.search(r"\bVERSION\s+" + re.escape(version) + r"\b", cmake):
            errors.append("Framework CMake project version differs from the declared version")
    if errors:
        print("\n".join("ERROR: " + error for error in errors), file=sys.stderr)
        return 1
    print(f"Source alignment passed: 38 chapters, {count} exact complete listings; SNode.C {version} at {sha}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Source alignment check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
