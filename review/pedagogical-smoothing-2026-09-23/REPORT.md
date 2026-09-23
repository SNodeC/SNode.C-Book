# Pedagogical smoothing — stopped at P0b

Date: 2026-09-23. Work branch: `book/pedagogical-smoothing-2026-09-23`.

The run stopped under §14: **“An entry check or lab fails for a reason other
than the P−1 defect.”** The explicit working-tree source-alignment check failed:
9 anchor checks (8 distinct locations) and 11 framework file-content comparisons.
This is unrelated to the C++20 target declarations. No repair was attempted and
P1 was not started. Evidence: `P0b-source-alignment.log:8`,
`P0b-stop-condition.json`, and `P0b-results.json`.

## Gates and source authority

| Gate | Status | Commit | Evidence in this directory |
| --- | --- | --- | --- |
| P0a | passed | `371a1b09738cb23e3981f2f15c9de9f037390e9c` | preflight.json; P0a-checks.log; framework-freeze-P0a.json |
| P−1 | passed | `c70d9d1ca422bf57dbb7940b5112a31896efe8c6` | P-minus-1-build.log; commit diff |
| P0b | failed; stopped under §14 | containing evidence commit, `review: stop pedagogical smoothing at P0b source-alignment gate` | P0b-results.json; P0b-stop-condition.json; all P0b logs |
| P1, P2, P3, P4+P5, P6, P7 | not started | — | manuscript diff empty; P0b-preservation.json |

The containing evidence commit records a failed gate; it does not certify P0b.
Its SHA is available in git history and the final handoff. Only the work branch
is designated for push to origin; no merge or source-branch push is authorized.

Entry was clean at `a5e51a204d79caef8c288d5e7b7cec2b8e87d09f`.
The only difference from `c7b76c108db43de7326a1a63756cf02eed3dbb31`
was the author-installed PROMPT.md commit. No unexpected book drift was found
(`preflight.json`). The prompt remains byte-for-byte unchanged, SHA-256
`c34bbab40ac13289e993af8504344f8d1435e1ec5ca87d4fb7ad6dfac8020155`.

The read-only framework at `/home/voc/projects/snodec/snode.c` was clean at
`8b8da56e0349191d4658ca8f820a490539eccd4d`. Its HEAD, porcelain status,
binary HEAD-diff digest and untracked-file hashes are identical at entry and
stop (`framework-freeze-P0a.json`, `framework-freeze-P0b-stop.json`, and the
corresponding untracked SHA-256 lists). The freeze did not change. The failed
alignment is between the existing book evidence and that frozen tree, not a
mid-run source mutation. Repository facts prevail over any expectation that
previous source-alignment evidence still passes. Historical evidence was not
rewritten. No substitute framework was used for source inspection.

## P−1 change and verification

The prescribed fix declares C++20 at each affected exercise target. It adds ten
`target_compile_features(... PRIVATE cxx_std_20)` declarations in eight files:

| File | Added declaration lines |
| --- | --- |
| companion/exercises/ch06/CMakeLists.txt | 4 |
| companion/exercises/ch08/CMakeLists.txt | 7 |
| companion/exercises/ch10/CMakeLists.txt | 4 |
| companion/exercises/ch11/CMakeLists.txt | 11 |
| companion/exercises/ch14/CMakeLists.txt | 4, 14 |
| companion/exercises/ch19/CMakeLists.txt | 13 |
| companion/exercises/ch20/CMakeLists.txt | 4, 8 |
| companion/exercises/ch21/CMakeLists.txt | 10 |

Inspected the declarations and commit diff; compiled all 14 concrete targets
with Clang 19 whose default `__cplusplus` is 201703. All 21 targeted compilation
commands explicitly request C++20. See `P-minus-1-build.log:1` and its final PASS
line. The existing ch08 bluetooth-selectors declaration was retained. Production
C++ and test-driver implementation changes: +0/−0 each. Exercise build declarations:
+10/−0. New scripts in this review directory are evidence support only.

## Entry checks

Each row was executed freshly; exact commands, environment and output are in
the linked log. `run-checks.py` collected every independent result despite the
alignment failure; it did not advance the editorial phase.

| Check | Result | Log |
| --- | --- | --- |
| manuscript-metrics.py | PASS | P0b-metrics.log |
| check-chapter-references.py | PASS | P0b-references.log |
| check-source-alignment.py --framework /home/voc/projects/snodec/snode.c | **FAIL** | P0b-source-alignment.log |
| check-source-hygiene.sh | PASS | P0b-hygiene.log |
| build-companion-examples.sh | PASS | P0b-companion.log |
| build-book-package.sh (PDFs and archive) | PASS | P0b-package.log |
| test-chapter-references.py | PASS | P0b-test-chapter-references.log |
| test-manuscript-metrics.py | PASS | P0b-test-manuscript-metrics.log |
| Public labs, CTest | PASS: 62/62 | P0b-labs.log |
| run-teaching-smoke-tests.py | PASS | P0b-teaching.log |
| run-behavior-smoke-tests.sh | PASS | P0b-behavior.log |
| run-example-lifetime-tests.py | PASS | P0b-lifetime.log |
| Extracted-package source hygiene | PASS | P0b-extracted-hygiene.log |
| check-smoothing.py | **NOT RUN; not created before stop** | P0b-stop-condition.json |

Twelve of thirteen executed entry groups passed. Source hygiene uses the recorded
snapshot and does not replace the explicit working-tree alignment check.
Compilation and runtime checks use the previously installed package at
`build/ci-fix-2026-09-22/install-gcc`, following the recorded Phase 5m environment.
They demonstrate builds and runs against that installation; with source alignment
failing, they do not certify compatibility with the frozen current framework.
No new framework build, hosted CI run or deployment verification is claimed.
Logs retain command output; only trailing horizontal whitespace was normalized.

## Outcome and preservation

`metrics-before.json` and `metrics-after.json` are identical: **100,338 → 100,338
raw whitespace tokens**, delta **0**. No manuscript prose was changed or reread
as an editorial refinement.

| Threshold | Required | Current difference |
| --- | ---: | ---: |
| Must | 107,338 | 7,000 below |
| Wish | 112,338 | 12,000 below |
| Hard ceiling | 115,000 | 14,662 below |

`P0b-preservation.json` and the empty manuscript diff against the entry baseline
confirm unchanged fenced tokens (8,151), exact source markers (37), index entries
(1,033), figure IDs (18), and rule boxes (20). The manifest still has 30 numbered
chapters plus Appendix A. All 62 existing labs pass. No listing, figure, index,
structure-sensitive registry or historical review record was changed.

## Deferred work and waivers

D1–D6 are accepted scope but none was applied before the entry stop. Chapter
splits, ranked prose additions, terminology changes, apparatus changes and
check-smoothing.py remain unimplemented. No floor or cap waiver was requested or
granted. Chapter budgets have not been adjudicated as completed work; no chapter
has been declared refined. Per-file baseline measurements remain available in
metrics-before.json. No post-pass chapter table, terminology allowlist, new
objective/lab mapping, or 8-dimension self-assessment has been manufactured for
work that never began.

- **Blocked:** P0b source alignment, with every failed anchor and file enumerated
  in P0b-stop-condition.json. Reconciliation is outside this stopped pass under §14.
- **Open:** P1–P7, all pedagogical deliverables and the 7,000-token global-must gap.
- **Qualified:** successful build/runtime evidence applies to the existing installed
  framework package; it is not verification of the present frozen source.
- **Completed:** P0a scope installation and the narrowly prescribed P−1 C++20 fix.

This run ends at P0b; no unrelated source-evidence repair is authorized by this run.
