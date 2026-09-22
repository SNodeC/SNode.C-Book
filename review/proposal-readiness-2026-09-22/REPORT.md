# Proposal readiness — phase report

Session date: 2026-09-22. Work branch: `SNode.C-2.0-refinement`, created directly
from `SNode.C-2.0` with a clean working tree. This session executes Phase 0 only.
The full author request is preserved in [PROMPT.md](PROMPT.md), including its
original escaped Markdown and HTML space entities. No preceding phase exists.

| Phase | Status | Commit | Date | Evidence |
| --- | --- | --- | --- | --- |
| 0 — scope and measurement | completed | Separate scope revision; Phase 0 completion commit containing this report (subjects below) | 2026-09-22 | AGENTS.md:18; EDITORIAL-WORK-PLAN.md:32; PROMPT.md; metrics-before.json; metrics-after-phase-0.json; measurement-checks.log; metrics-tests.log |
| 1 — book-wide hygiene | not started | — | — | No Phase 1 edits or builds executed |
| 2 — five sample chapters | not started | — | — | No sample-chapter edits or exercise solutions executed |
| 3 — proposal package | not started | — | — | No proposal rewrite or package builds executed |
| 4 — restructure plan | not started | — | — | No plan or author approval recorded |
| 5a — approved TOC | not started | — | — | Gated on recorded author approval |
| 5b onward — one Part per session | not started | — | — | Instantiate one row per approved Part before executing it; final sub-phase must meet all global targets |

Commit subjects (resolve with `git log --oneline --grep='^proposal-readiness: phase 0'`):

- `proposal-readiness: phase 0 — record author scope revision`
- `proposal-readiness: phase 0 — establish manuscript metrics and baseline`

The completion row identifies its containing commit by subject to avoid a
self-referential identifier. Keep the scope-revision commit separate permanently.

## Scope and measurement contract

Edited and reread: `AGENTS.md:15` and `review/EDITORIAL-WORK-PLAN.md:32` now record
the shortening target, preservation of teaching depth and MiniGateway, approval
gate for consolidation, and one-phase execution control. The first commit stores
these changes and PROMPT.md before measurement implementation. The new report
and tool documentation were reread; no manuscript editorial reread is claimed.

Measurement authority: `manuscript/book-files.txt`, all 62 entries in order.
`ci/manuscript-metrics.py` is the sole reusable measurement implementation;
`ci/test-manuscript-metrics.py` supplies counter regression fixtures. No existing
reusable manuscript-metrics implementation was found in the tooling inventory.
The invariant is reproducible counts from exactly the ordered inputs, with no
code content misclassified as headings, callouts, or reader-facing phrases.
The explicitly requested measurement tool is new CI support, not companion
application code. No application architecture changes are made.

Words are Python whitespace tokens in the raw Markdown, including markup.
`prose_words + code_words = total_words`; code words include both fence lines.
The separate `code_content_words` and `fence_marker_words` fields expose this
partition. Inline code remains in prose. Raw LaTeX fences count as fenced code.
These are source counts, not rendered editorial word counts.

Headings, callouts, phrases, and manual references exclude fenced code. Phrase
matches ignore case and allow line-wrapped whitespace. Singular `role`, exact
`visible`, and combined `boundary`/`boundaries` use whole-word matching. Nine
non-overlapping forbidden guards cover the named examples and additional patterns;
five actual hits are recorded with source lines. Similar phrasing still requires
editorial review in Phase 1; no comprehensive semantic scan is claimed here.

Average section length counts non-code body tokens between successive headings,
excluding heading lines and chapter preambles. Each level 3–6 chapter heading
starts a section, including empty parent sections; the epilogue is included.
This avoids double-counting nested sections and prevents code from inflating the
prose-density measure. Definition and per-file measurements are saved in both JSONs.
Manual references count literal singular `Chapter N`; plural references and ranges
still need editorial inventory during the Phase 4 cross-reference assessment.

## Baseline and Phase 0 delta

Evidence: `metrics-before.json` and `metrics-after-phase-0.json`, keys `totals`,
`files`, and `requested_baseline_comparison`. Both independent executions produced
byte-identical JSON. Phase 0 changes every listed manuscript metric by zero.

| Metric | Supplied baseline | Measured before and after | Difference from supplied |
| --- | ---: | ---: | ---: |
| Total words | 151,922 | 151,924 | +2 |
| Chapter headings, level 3 and deeper | 1,020 | 1,020 | 0 |
| Closing perspective sections | 15 | 15 | 0 |
| snodec-remember | 38 | 38 | 0 |
| snodec-rule | 30 | 30 | 0 |
| text fences | 478 | 478 | 0 |
| cpp fences | 205 | 205 | 0 |
| snodec-exercise | 0 | 0 | 0 |

The two-token difference is recorded, not explained by an unverified cause.
An independent `\S+` count confirms 151,924 in the current ordered inputs.
No earlier input snapshot was substituted to force agreement.

Additional baseline measurements:

- Prose: 136,829 tokens. Fenced code including markers: 15,095 tokens;
  code contents: 13,527; fence markers: 1,568.
- Average chapter section prose: 124.13 tokens across 1,020 sections.
- Forbidden phrase hits: 5. Their file/line locations appear in
  `measurement-checks.log` and each affected file's JSON entry.
- Shell fence labels: `sh` 55, `shell` 4.
- Terms: role 719; boundary/boundaries 525; visible 220; is not a 74;
  does not prove 13; does not by itself 8.
- Manual Chapter N references: 275, with matched text and line locations.
- Distance to final targets: total words +36,924 over 115,000 (+46,924 over
  stretch 105,000); chapter subheadings +470 over 550; text fences +228 over 250;
  rule boxes +18 over 12. These are later-phase work, not Phase 0 failures.

PDF baseline: existing `dist/pdf/snodec-book.pdf` has **490 pages**, confirmed with
`pdfinfo`; see `pdfinfo-phase-0.txt`. The artifact was not regenerated or modified
in this phase, so its observed before/after count is 490/490. Correspondence to a
fresh build and LaTeX warning/box status are **not verified in Phase 0**.

## Executed checks and limits

- **Run, passed:** five regression tests in `ci/test-manuscript-metrics.py`, covering
  longer closing fences, nested fence text, tilde fences, exclusion of code from
  structure and phrases, line-wrapped phrase locations, whole-word matches,
  attributed callouts, invalid unclosed fences, manifest membership, and duplicate
  input rejection. Output: `metrics-tests.log`.
- **Run, passed:** `verify-phase-0.py` regenerates metrics, compares before/after,
  independently counts current source tokens/headings/callouts/key fences/closing
  sections, checks all word partitions, verifies the scope commit and status
  table, checks the empty manuscript diff, and runs `git diff --check`.
  Output: `measurement-checks.log`.
- An initial ad hoc independent closing-heading check omitted attributed headings
  and failed on the epilogue's `{.unnumbered}` heading. The corrected check includes
  attributes; the metric implementation already counted it. This did not require
  a manuscript or metric change.
- **Built:** no PDF, proposal, or companion targets in this phase.
- **Not verified:** Phase 1 hygiene guards, source alignment, companion compilation,
  runtime behavior, and current PDF warning/box status. No listing changes occurred.

Accounting from the Phase 0 diff: application production code **+0/−0**;
CI measurement tool **+177/−0**; regression test support **+75/−0**.
The report-local verification runner is **+52/−0** additional evidence-support
lines, accounted separately from application production code. Manuscript **+0/−0**. Scope documents,
prompt, JSON measurements, logs, and this report are documentation/evidence.

## Re-verification required before Phase 1

Read PROMPT.md and this report, then run from the repository root:

```sh
python3 -B review/proposal-readiness-2026-09-22/verify-phase-0.py
git log --oneline --grep='^proposal-readiness: phase 0'
git ls-files --error-unmatch AGENTS.md review/EDITORIAL-WORK-PLAN.md ci/manuscript-metrics.py review/proposal-readiness-2026-09-22/PROMPT.md review/proposal-readiness-2026-09-22/REPORT.md review/proposal-readiness-2026-09-22/metrics-before.json review/proposal-readiness-2026-09-22/metrics-after-phase-0.json
```

Confirm both separate Phase 0 commits and their recorded scope; the runner is
intentionally strict about the unchanged Phase 0 inputs. If fresh measurements
or any exit check disagree, report the gap and stop before Phase 1. Do not treat
the completed status alone as proof. Phase 0 ends here; Phase 1 has not begun.
