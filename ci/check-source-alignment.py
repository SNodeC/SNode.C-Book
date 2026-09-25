#!/usr/bin/env python3
"""Check edition declarations and exact, explicitly marked complete listings."""
from __future__ import annotations

import argparse
import hashlib
import json
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


def content_drift(framework, manifest):
    names = subprocess.check_output(
        ["git", "-C", str(framework), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        text=True).split("\0")
    actual = {name: hashlib.sha256((framework / name).read_bytes()).hexdigest()
              for name in sorted(set(filter(None, names))) if (framework / name).is_file()}
    return [name for name in sorted(set(actual) | set(manifest["files"]))
            if actual.get(name) != manifest["files"].get(name)]


def checkout_tag(framework, tag):
    return subprocess.check_output(
        ["git", "-C", str(framework), "describe", "--tags", "--exact-match", "--match", tag, "HEAD"],
        stderr=subprocess.PIPE, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=pathlib.Path,
                        help="Also verify this framework working tree against the recorded source contents")
    args = parser.parse_args()
    errors: list[str] = []
    values = baseline()
    version = values.get("SNODEC_VERSION", "")
    manifest = json.loads((ROOT / values["SNODEC_WORKTREE_MANIFEST"]).read_text())
    patch = ROOT / values["SNODEC_WORKTREE_PATCH"]
    if manifest["project_version"] != version:
        errors.append("Working-tree manifest differs from the baseline declaration")
    if hashlib.sha256(patch.read_bytes()).hexdigest() != manifest["patch_sha256"]:
        errors.append("Captured framework patch differs from its recorded digest")
    recorded_tree = "".join(f"{digest}  {name}\n" for name, digest in sorted(manifest["files"].items()))
    if hashlib.sha256(recorded_tree.encode()).hexdigest() != manifest["tree_sha256"]:
        errors.append("Framework file manifest differs from its recorded tree digest")
    if values.get("SNODEC_REF") != "Book-1.0" or "SNODEC_COMMIT" in values:
        errors.append("Framework source must use the Book-1.0 edition tag")
    if version != "2.0.0":
        errors.append("This migration's declared project version must be 2.0.0")
    for name in ["README.md", "source-baseline/SOURCE-VERSION.md",
                 "source-baseline/book-source-baseline.md",
                 "manuscript/frontmatter/preface.md", "review/proposal/book-proposal-package.md"]:
        text = (ROOT / name).read_text()
        if version not in text or "manifest" not in text.lower():
            errors.append(f"Missing edition manifest/version in {name}")
    chapters = [ROOT / name for name in (ROOT / "manuscript/book-files.txt").read_text().splitlines()
                if re.match(r"manuscript/chapters/(?:\d\d-|appendix-)", name)]
    claims = json.loads((ROOT / "review/verification/source-claims.json").read_text())
    if claims["framework_manifest"] != values["SNODEC_WORKTREE_MANIFEST"]:
        errors.append("Chapter evidence does not reference the authoritative source manifest")
    if claims["reviewed_tree_sha256"] != manifest["tree_sha256"]:
        errors.append("Chapter evidence was reviewed against a different content manifest")
    records = claims["chapters"]
    if [ROOT / record["manuscript"] for record in records] != chapters:
        errors.append("Chapter evidence must cover each ordered chapter and appendix exactly once")
    for record in records:
        manuscript = ROOT / record["manuscript"]
        identity = (f"{record['chapter']:02}-" if isinstance(record['chapter'], int)
                    else f"appendix-{record['chapter'].lower()}-")
        if manuscript not in chapters or not manuscript.name.startswith(identity):
            errors.append(f"Invalid chapter evidence target: {record['manuscript']}")
        for anchor in record["framework_sources"]:
            if anchor["path"] not in manifest["files"]:
                errors.append(f"Source anchor is outside the recorded tree: {anchor['path']}")
            elif args.framework:
                source = args.framework / anchor["path"]
                lines = source.read_text().splitlines() if source.is_file() else []
                line = anchor["line"]
                if not 1 <= line <= len(lines) or anchor["needle"] not in lines[line - 1]:
                    errors.append(f"Source anchor differs: {anchor['path']}:{line}")
        for companion in record["companion_sources"]:
            if not (ROOT / companion).is_file():
                errors.append(f"Missing companion evidence: {companion}")
    sources = list((ROOT / "manuscript").rglob("*.md"))
    sources += list((ROOT / "review/proposal").glob("*.md"))
    sources += list((ROOT / "assets/figures/src").glob("*.tex"))
    marked = re.compile(r"<!-- snodec-source: ([^\n]+?) -->\s*\n```(?:cpp|cmake|python)\n(.*?)\n```", re.S)
    count = 0
    for path in sources:
        text = path.read_text()
        if re.search(r"\b(?:LOG|PLOG|VLOG)\s*\(", text):
            errors.append(f"Removed macro logging surface remains in {path.relative_to(ROOT)}")
        if "v1.0.2" in text or "6e475262084ae2dab2daef8781ab9e4adb82d18e" in text:
            errors.append(f"Old reader-facing baseline remains in {path.relative_to(ROOT)}")
        for match in marked.finditer(text):
            source = (ROOT / match[1]).resolve()
            if not any(source.is_relative_to(ROOT / "companion" / area) for area in ("examples", "exercises")) or not source.is_file():
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
        checkout_tag(args.framework, values["SNODEC_REF"])
        cmake = (args.framework / "CMakeLists.txt").read_text()
        if not re.search(r"\bVERSION\s+" + re.escape(version) + r"\b", cmake):
            errors.append("Framework CMake project version differs from the declared version")
        for name in content_drift(args.framework, manifest):
            errors.append(f"Book-1.0 checkout differs from the edition manifest: {name}")
    if errors:
        print("\n".join("ERROR: " + error for error in errors), file=sys.stderr)
        return 1
    print(f"Source alignment passed: {len(records)} chapter/appendix evidence records, {count} exact complete listings; "
          f"SNode.C {version}, Book-1.0 content manifest")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Source alignment check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
