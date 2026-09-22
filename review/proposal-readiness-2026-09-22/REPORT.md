# Proposal readiness — phase report

Session date: 2026-09-22. Work branch: `SNode.C-2.0-refinement`, created directly
from `SNode.C-2.0` with a clean working tree. The phase records below are chronological. Phase 5i is completed after freshly rerunning the Phase 5h exit gate. Parts I–VIII and the approved front-matter work are complete. Phase 5j has not started.
The author request is preserved in [PROMPT.md](PROMPT.md). Its initial block was
subsequently unescaped in a separate Phase 0 commit; the teaching-book amendment
was subsequently unescaped by deliberate author work; its teaching requirements govern Phase 2.

| Phase | Status | Commit | Date | Evidence |
| --- | --- | --- | --- | --- |
| 0 — scope and measurement | completed | Separate scope revision; Phase 0 completion commit containing this report (subjects below) | 2026-09-22 | AGENTS.md:18; EDITORIAL-WORK-PLAN.md:32; PROMPT.md; metrics-before.json; metrics-after-phase-0.json; measurement-checks.log; metrics-tests.log |
| 1 — book-wide hygiene | completed | `proposal-readiness: phase 1 — refine manuscript hygiene and preserve teaching principles` (containing this report); separate author-amendment commit | 2026-09-22 | Phase 1 evidence below; metrics-after-phase-1.json; phase-1-source-hygiene.log; phase-1-source-alignment.log; phase-1-companion-build.log; phase-1-pdf-final.log |
| 2 — five sample chapters and author follow-up | completed | `proposal-readiness: phase 2 follow-up — sample chapter strengthening` (containing this report); initial Phase 2 commit retained | 2026-09-22 | chapter-ledger.md; metrics-after-phase-2.json; phase-2-exit-checks.json; phase-2-follow-up-labs.log; phase-2-follow-up-pdf-final-build.log; phase-2-follow-up-visual-review.md |
| 3 — proposal package | completed | `proposal-readiness: phase 3 — prepare teaching-book proposal package` (containing this report) | 2026-09-22 | Phase 3 evidence below; metrics-after-phase-3.json; phase-3-bibliography.json; phase-3-exit-checks.json; phase-3-package-final.log; phase-3-archive-labs.log; phase-3-visual-review.md |
| 4 — restructure plan | approved with author changes | `proposal-readiness: phase 4 — propose consolidated teaching-book structure` (containing this report) | 2026-09-22 | RESTRUCTURE-PLAN.md; phase-4-reference-map.md; phase-4-plan-checks.json; metrics-after-phase-4.json; Phase 4 evidence below |
| 5a — approved TOC | completed | `proposal-readiness: phase 5a — apply approved teaching-book structure` (containing this report) | 2026-09-22 | phase-5a-approved-structure.json; phase-5a-reference-register.json; phase-5a-exit-checks.json; metrics-after-phase-5a.json; Phase 5a evidence below |
| 5b — Part I | completed | `proposal-readiness: phase 5b — refine Part I and establish the measurement checkpoint` (containing this report); separate prerequisite repair retained | 2026-09-22 | metrics-after-phase-5b.json; phase-5b-exit-checks.json; chapter-ledger.md; phase-5b-final-*.log; phase-5b-visual-review.md; completion account below |
| 5c — Part II | completed | `proposal-readiness: phase 5c follow-up — remove triple name/component explanation`; initial Phase 5c commit retained | 2026-09-22 | metrics-after-phase-5c.json; phase-5c-exit-checks.json; chapter-ledger.md; phase-5c-final-*.log; phase-5c-visual-review.md; completion account below |
| 5d — Part III | completed | `proposal-readiness: phase 5d follow-up — relocate stranded Unix-socket introduction`; initial Phase 5d commit retained | 2026-09-22 | metrics-after-phase-5d.json; phase-5d-exit-checks.json; chapter-ledger.md; phase-5d-final-*.log; phase-5d-visual-review.md; completion account below |
| 5e — Part IV | completed | `proposal-readiness: phase 5e — refine Part IV and verify protocol framing` (containing this report) | 2026-09-22 | metrics-after-phase-5e.json; phase-5e-exit-checks.json; chapter-ledger.md; phase-5e-final-*.log; phase-5e-visual-review.md; completion account below |
| 5f — Part V | completed | `proposal-readiness: phase 5f — refine Part V and verify configuration diagnostics` (containing this report) | 2026-09-22 | metrics-after-phase-5f.json; phase-5f-exit-checks.json; chapter-ledger.md; phase-5f-entry-*.log; phase-5f-final-*.log; phase-5f-visual-review.md; completion account below |
| 5g — Part VI | completed | `proposal-readiness: phase 5g follow-up — move TLS fixture into companion material`; initial Phase 5g commit retained | 2026-09-22 | metrics-after-phase-5g.json; phase-5g-exit-checks.json; chapter-ledger.md; phase-5g-entry-*.log; phase-5g-final-*.log; phase-5g-visual-review.md; completion account below |
| 5h — Part VII | completed | `proposal-readiness: phase 5h — refine Part VII and verify web protocol boundaries` (containing this report) | 2026-09-22 | metrics-after-phase-5h.json; phase-5h-exit-checks.json; chapter-ledger.md; phase-5h-final-*.log; phase-5h-visual-review.md; completion account below |
| 5i — Part VIII | completed | `proposal-readiness: phase 5i — refine Part VIII and verify MQTT delivery boundaries` (containing this report) | 2026-09-22 | metrics-after-phase-5i.json; phase-5i-exit-checks.json; chapter-ledger.md; phase-5i-entry-*.log; phase-5i-final-*.log; phase-5i-visual-review.md; completion account below |
| 5j — Part IX | not started | — | — | Author-approved schedule; see Phase 5a handoff below |
| 5k — Part X | not started | — | — | Author-approved schedule; see Phase 5a handoff below |
| 5l — Part XI only | not started | — | — | Author-approved schedule; see Phase 5a handoff below |
| 5m — appendix, closing material and global audit | not started | — | — | Author-approved schedule; see Phase 5a handoff below |
| 6 — proposal refresh | not started | — | — | Author-approved schedule; see Phase 5a handoff below |

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

## Phase 1 — book-wide hygiene, completed 2026-09-22

**Entry gate:** reran Phase 0 metrics and all listed checks before editing; all
passed. Evidence: `phase-1-prerequisite.log`. The initial working tree was clean.
This session executed Phase 1 only.

**Author amendment:** appended verbatim to PROMPT.md and recorded in
EDITORIAL-WORK-PLAN.md, with the standing AGENTS.md reference updated. These scope
records were committed separately as
`proposal-readiness: author amendment — teaching book`. Only the amended rule-box
criterion is implemented now. Objectives, tiered exercises, solutions, and learning
path changes remain in their assigned Phases 2–5. No approval to restructure is
recorded. The amended rule cap is **20**; earlier references to 12 are historical.

### Editorial outcomes and preserved teaching

Edited and reread locally in context: the changed passages and their neighboring
explanations, examples, and closing transitions. This is not a claim of a new
end-to-end reading of all 62 inputs. The Phase 1 commit diff and per-file records
in `phase-1-integrity.json` identify the exact changed scope.

- Removed all five guarded authoring notes in Chapters 11, 21, 29 and 34. Also
  removed similar author-facing commentary in Chapters 6, 7, 9, 10 and 28.
  The guard now uses the existing metric implementation as its single phrase
  authority: `ci/check-source-hygiene.sh:75`. Its actual entry point rejects all
  nine case-varied, line-wrapped fixture phrases (`phase-1-guard-tests.log`).
- Removed all 15 closing-section headings. Chapters 1, 6, 9 and 37 retain their
  measurement reminder, dispatcher-tracing exercise, lifecycle classification
  exercise, and transition to extension as final prose before the remember box.
  The epilogue retains its concrete closing advice in the preceding section.
  The summaries removed from Chapters 12, 15, 16, 20, 24, 26, 27, 28, 31 and 38
  repeat explanations or recaps already present; their examples remain.
- Collapsed mirrored explanations in Chapter 10 (IP convenience calls, address
  forms, local/remote choices), Chapter 12 (L2CAP address surface and local/remote
  Bluetooth identity), Chapter 19 (server/client TLS configuration), and Chapter
  29 (JSON client/server comparison). Concrete code examples and differences in
  endpoint selection remain. See those chapter diffs and the rendered tables in
  `phase-1-visual-review-3.png` and `phase-1-visual-review-8.png`.
- Consolidated book-specific verification limits in
  `manuscript/frontmatter/conventions.md:11`, including compilation versus
  execution and native MQTT versus WebSocket/broker checks. Chapters 19, 25, 26,
  28, 31, 33 and 34 retain runnable instructions and service prerequisites while
  losing repeated process commentary. Protocol cautions about delivery, replay,
  trust, persistence, and timeout behavior remain where they affect a decision.
- Normalized four top-level `shell` fences to `sh`, plus two nested `bash` fences
  in Chapter 35's printed README excerpt. The latter are synchronized with
  `companion/examples/MiniGateway/README.md`. No command text changed.

### Rule boxes restored after the author clarification

The first editing pass reduced rule boxes to 12. Reassessment under the amended
criterion restored these eight boxes, with their original principle text. Their
introductory restatement was not needed. Final rule-box count: **20**.

| Restored box | Final source anchor | Principle the reader applies |
| --- | --- | --- |
| Runtime registration rule | manuscript/chapters/03-your-first-working-program-the-echo-pair.md:368 | Separate registering a listening flow from runtime execution. |
| Reading rule | manuscript/chapters/04-reading-the-codebase-with-confidence.md:17 | Follow layers and responsibilities when navigating the source tree. |
| Instance/context boundary | manuscript/chapters/05-the-mental-model-of-snodec.md:148 | Keep runtime-facing role policy separate from per-connection protocol behavior. |
| Runtime-flow rule | manuscript/chapters/05-the-mental-model-of-snodec.md:483 | Treat activation flows and their runtime progress as distinct from the immediate call. |
| Layer-reading rule | manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:100 | Read a communication type as a stack description. |
| Lifecycle responsibility rule | manuscript/chapters/09-servers-clients-and-connections.md:612 | Put lifecycle observation and protocol behavior in their respective callbacks. |
| Architectural principle | manuscript/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md:299 | Keep meaning available until the responsible layer can act on it. |
| Extension rule | manuscript/chapters/38-extending-the-framework-safely.md:524 | Extend the responsibility that actually changes. |

All eight restored boxes were also visually inspected; see the page inventory in
`phase-1-pdf-checks.json` and `phase-1-visual-review-1.png` through
`phase-1-visual-review-8.png`.

The ten remaining box removals are duplicates or near-tautologies:

| Removed box | Reason and retained explanation |
| --- | --- |
| Ch. 1 Separation rule | Repeats the preceding protocol/carrier distinction and explicit family consequences. |
| Ch. 6 Runtime-state rule | “Not background decoration” adds no guidance beyond the preceding runtime-state explanation. |
| Ch. 10 Family-independent pattern | Repeats the immediately preceding list of shared roles and unchanged application shape. |
| Ch. 13 Context responsibility rule | The definition remains verbatim as ordinary text, followed by the table unpacking it; the box duplicates that definition's function. |
| Ch. 16 Configuration rule | The definition remains verbatim in the introduction and is applied by the next paragraph. |
| Ch. 19 TLS boundary rule | Repeats the opening explanation of connection-layer specialization. |
| Ch. 22 Express-layer rule | Repeats the opening sentence and immediately following HTTP/application distinction. |
| Ch. 27 Multi-protocol boundary rule | Repeats the adjacent statement that the design task is deciding where each protocol belongs. |
| Ch. 32 Build-policy rule | The slogan adds no decision beyond the preceding concrete reasons for strict diagnostics. |
| Ch. 36 MiniGateway extension rule | Duplicates the adjacent callback warning and the retained extension principle in Chapter 38. |

### Metrics and exit evidence

Evidence: `metrics-after-phase-0.json` versus `metrics-after-phase-1.json`;
`check-phase-1-integrity.py` regenerates the latter independently and checks
preservation. Its executed output is `phase-1-integrity.log`.

| Metric | Before | After | Delta / Phase 1 result |
| --- | ---: | ---: | --- |
| Total whitespace tokens | 151,924 | 150,566 | −1,358 |
| Prose tokens | 136,829 | 135,586 | −1,243 |
| Fenced tokens, including markers | 15,095 | 14,980 | −115; only explanatory text blocks condensed |
| C++ fences | 205 | 205 | All contents unchanged |
| Chapter headings, level 3+ | 1,020 | 1,005 | −15 closing-section headings |
| Average chapter section prose | 124.13 | 124.71 | +0.58 |
| Closing perspective sections | 15 | 0 | Pass |
| Forbidden-phrase hits | 5 | 0 | Pass, guards active |
| snodec-rule boxes | 30 | 20 | Pass under author amendment |
| snodec-remember boxes | 38 | 38 | Unchanged |
| Top-level shell labels | sh / shell | sh | Pass; nested bash labels also normalized |
| text fences | 478 | 465 | −13 |
| does not prove | 13 | 4 | −9; necessary behavioral cautions retained |
| does not by itself | 8 | 6 | −2 |
| PDF pages | 490 | 482 | −8, against recorded Phase 0 baseline |

Global targets remain later-phase requirements: total words are **35,566** above
115,000 (45,566 above the stretch target), chapter subheadings **455** above 550,
and text fences **215** above 250. Average section prose remains below 250.
The existing remember-box bullet counts and exercise/objective requirements are
not declared complete in Phase 1; those belong to the specified later phases.

| Verification | Result | Executed evidence |
| --- | --- | --- |
| Phase 0 prerequisite rerun | Passed before editing | phase-1-prerequisite.log |
| Source hygiene | Passed on final manuscript | phase-1-source-hygiene.log |
| Source alignment | Passed; 36 exact marked complete listings | phase-1-source-alignment.log |
| Nine authoring-note guards | Passed through actual hygiene script | phase-1-guard-tests.log; check-phase-1-guards.py |
| Five metrics regression tests | Passed | phase-1-metrics-tests.log |
| Metrics and manuscript integrity | Passed across all 62 inputs | phase-1-integrity.log; phase-1-integrity.json |
| Companion examples | Built all configured targets, 57 compile/link steps | phase-1-companion-build.log |
| PDF configure and target | Passed | phase-1-pdf-configure.log; phase-1-pdf-final.log |
| Final LaTeX warnings / bad boxes | 0 / 0 in final three-pass console and all 20 final LaTeX logs | phase-1-latex-final.log; phase-1-pdf-checks.json |
| Visual review | 16 representative pages inspected, including all restored boxes and the new tables | phase-1-pdf-checks.json; eight phase-1-visual-review PNGs |

The companion run used an existing installation, configured a fresh companion
build directory, and compiled every selected example. This was a **local build**;
no hosted CI execution or runtime/deployment test is claimed. The integrity check
compares executable and raw-LaTeX fence contents, listing markers, figure
references, index entries, non-closing headings, and manuscript order. All remain
unchanged. The README excerpt's shell labels change; its commands do not.

The initial fresh PDF build and the build after restoring rules are retained in
`phase-1-pdf-initial.log` and `phase-1-pdf-restored-rules.log`. Intermediate
reference-convergence warnings are historical to those builds. The final ordinary
build has no warnings or bad boxes across all three passes. Warning settings and
production styles were not changed. Archived logs normalize trailing horizontal
whitespace only; no diagnostic lines were removed. Visual inspection is
representative, not a full 482-page visual audit.

Accounting is in `phase-1-accounting.json`: no application production-code changes;
CI hygiene support is +12/−0 lines, reusing the existing phrase authority.
Report-local regression/integrity scripts are **+82/−0** test-support lines.
Manuscript changes are **+64/−305** lines; companion README documentation is
**+2/−2**. No Phase 2–5 implementation is included.

### Re-verify before Phase 2

Read PROMPT.md, including the amendment, and the accepted scope in the work plan.
Run each command below from the repository root, retaining fresh logs separately;
one failed check must not suppress the other checks. Stop before Phase 2 if any
Phase 1 criterion fails. The source installation used below must still be available.

```sh
python3 -B review/proposal-readiness-2026-09-22/check-phase-1-integrity.py
python3 -B review/proposal-readiness-2026-09-22/check-phase-1-guards.py
python3 -B ci/test-manuscript-metrics.py
bash ci/check-source-hygiene.sh
python3 ci/check-source-alignment.py
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc" BOOK_EXAMPLES_BUILD_DIR="$PWD/build/proposal-readiness-phase-1-examples" bash ci/build-companion-examples.sh
cmake -S . -B build/proposal-readiness-phase-1 -G Ninja
cmake --build build/proposal-readiness-phase-1 --target pdf
pdfinfo dist/pdf/snodec-book.pdf
```

Require zero warnings/bad boxes in the fresh PDF console and final LaTeX logs,
and recheck the measured 482 pages. Confirm both the separate author-amendment
commit and the Phase 1 completion commit, and a clean working tree. Phase 1 ends
here; Phase 2 has not begun.

## Phase 2 — five teaching samples (initial completion)

The following results are historical to the initial Phase 2 commit. Its final
metrics are preserved in `metrics-before-phase-2-follow-up.json`; the current
ledger, `metrics-after-phase-2.json`, and `phase-2-exit-checks.json` include the
author follow-up recorded at the end of this report. Original logs remain intact.

Completed 2026-09-22, after the Phase 1 prerequisite checks below. This phase
applies the teaching-book amendment to Chapters 1, 3, 23, 35, and 37 only.
No Phase 3 proposal rewrite or later phase was started.

### Phase 1 exit re-verification and accepted author change

Fresh `metrics-before-phase-2.json` differs from `metrics-after-phase-1.json`
only in `manuscript/chapters/epilogue.md`: +39 prose/total words from the deliberate
`author edit: restore epilogue closing`. Entry total: 150,605. This is the expected
author change named in the session request, not a failed editorial criterion.
The exact historical JSON-equality assertion initially detected that difference;
`phase-2-prerequisite-integrity.log` records the reconciliation, then checks against
the fresh entry metrics while retaining all original code/structure checks.
The historical checker and Phase 1 evidence files were not rewritten.

Re-executed evidence:

| Phase 1 prerequisite | Evidence in this directory | Result |
| --- | --- | --- |
| Four hygiene thresholds and manuscript preservation | `phase-2-prerequisite-integrity.log`, `phase-2-prerequisite-integrity.json` | forbidden 0, closing 0, rule 20, shell label sh; executable code and non-closing structure preserved |
| Actual forbidden-phrase guard entry point | `phase-2-prerequisite-guards.log` | all nine case-varied, wrapped guard fixtures rejected |
| Metrics counter tests | `phase-2-prerequisite-metrics-tests.log` | 5 passed |
| Source hygiene and alignment | `phase-2-prerequisite-hygiene.log`, `phase-2-prerequisite-alignment.log` | passed |
| Companion build | `phase-2-prerequisite-companion.log` | passed with supplied installation |
| PDF target | `phase-2-prerequisite-pdf.log` | 482 pages; final LaTeX log had no warnings or bad boxes |

### Editorial results and exit criteria

`chapter-ledger.md` gives exact before/after figures, all 15 objective↔exercise
mappings, solution paths, and reread notes. All five chapters were **edited and
reread in context**, including the destinations of the Chapter 3 vocabulary
handoff and Chapter 37 extension transition. Each now opens with three observable
objectives and closes with one recap of at most five bullets followed by three
exercises: review, lab, design. No recap bullet restates its chapter title.
The public README solutions give the conceptual answers, reproducible lab commands
with expected outcomes, and justified design discussions.

| Chapter | Prose before → after | Reduction | Average section prose after |
| --- | ---: | ---: | ---: |
| 1 | 2,343 → 1,604 | 31.54% | 303.40 |
| 3 | 2,674 → 1,934 | 27.67% | 306.67 |
| 23 | 3,664 → 2,843 | 22.41% | 390.29 |
| 35 | 2,378 → 1,752 | 26.32% | 275.83 |
| 37 | 2,395 → 1,868 | 22.00% | 292.50 |

All prose totals include the new objectives, recaps, exercises, and formatting
markup. Code cannot inflate the section averages. `check-phase-2.py` regenerated
and checked the metrics, 20% cuts, 250-word averages, callout positions, three tiers,
and objective coverage; see `phase-2-exit-checks.log` and `.json`.

Chapter 1's side-by-side EchoPair/Asio comparison is 514 words. Its platform,
runtime, and ecosystem statements and primary sources are documented in
`phase-2-comparison-evidence.md`. The ecosystem assessment is qualitative;
no adoption or performance number is asserted. The standalone Asio build passed
without SNode.C (`phase-2-asio-standalone.log`).

All complete printed companion listings still match their files (36 complete
listings checked by `phase-2-alignment.log`). Chapter 35 preserves **every fenced
block byte-for-byte**, including its nested README; see `phase-2-exit-checks.json`.
Chapter 3 removes eight isolated extracts of code already printed in full along
with their repeated explanation, while retaining every complete source/build
listing. The remaining fence reductions remove explanatory text diagrams and
repeated framing. No program logic or complete listing was cut to meet the prose
budget. The five samples preserve their figure, index, and source markers; every
other ordered manuscript input is unchanged from phase entry, including the
restored epilogue. Input order is unchanged. `STRUCTURE.md` records the sample
pedagogy and section grouping; no chapter consolidation occurred.

### Build, run, and visual evidence

| Check | Evidence | Result |
| --- | --- | --- |
| Hygiene and complete listing alignment | `phase-2-hygiene.log`, `phase-2-alignment.log` | passed |
| Metrics regression, including objectives | `phase-2-metrics-tests.log` | 5 passed |
| All companion programs and C++ lab solutions | `phase-2-companion.log`, `phase-2-companion-final.log` | built with GCC and supplied installation |
| Public labs, actual execution | `phase-2-labs.log` | 5/5 CTest cases passed with expected observable outputs |
| Asio independent configuration and compilation | `phase-2-asio-standalone.log` | passed |
| Full PDF target | `phase-2-pdf-final.log`, `phase-2-pdf-checks.json` | 470 pages, zero LaTeX warnings, zero bad boxes |
| Rendered sample pages and contents | `phase-2-rendered-pages.json`, `phase-2-visual-review.md` | inspected; label orphan corrected and affected pages re-rendered |

The initial sandbox run compiled the examples but could not open local sockets.
A permitted local run then caught a test-harness assumption: SNode.C's handled
SIGINT returns `-stopsig` (`EventLoop.cpp:318`), observed as status 254. The harness
now accepts that value only when it actually requests shutdown, still rejecting
unexpected exits and timeouts. It also explicitly closes the streaming response
before its HTTP connection. `phase-2-companion-runtime.log` retains the first
failure; `phase-2-labs.log` records final successful observations. No application
behavior or expected payload was weakened to obtain a pass.

The CI workflow installs standalone Asio headers and invokes these same five CTest
cases in both existing compiler jobs. Its lab step is separate from compilation
and the other smoke-test steps, so a lab failure does not suppress unrelated tests.
See the diff of `.github/workflows/companion-examples.yml`, root and companion
CMake files, and `companion/exercises/*/CMakeLists.txt`. Remote CI was **not run**
in this session; local GCC build/run is the executed evidence. The Chapter 35 lab
intentionally uses no broker and claims no broker-delivery validation.

Callouts use the existing palette and breakable box style in
`production/filters/snodec-callouts.lua:13` and
`production/latex/snodec-callouts.tex:81`. The shorter TOC exposed one underfull
vertical box; `production/metadata/metadata.yaml:42` gives its existing section-row
spacing modest stretch. This fixes layout without suppressing warnings. Filename
labels in Chapters 3 and 35 stay with their listings through a local `\Needspace`
constraint. The final build preserves the existing warning thresholds.

### Metrics delta and implementation accounting

| Metric | Phase 2 entry | Phase 2 exit | Delta |
| --- | ---: | ---: | ---: |
| Total words | 150,605 | 146,525 | -4,080 |
| Prose words | 135,625 | 132,172 | -3,453 |
| Fenced words, including markers | 14,980 | 14,353 | -627 |
| Chapter subheadings | 1,005 | 921 | -84 |
| Average section prose, book-wide | 124.75 | 132.53 | +7.78 |
| text fences | 465 | 434 | −31 |
| rule boxes | 20 | 20 | 0 |
| objectives / exercise callouts | 0 / 0 | 5 / 5 | +5 / +5 |
| Full PDF pages | 482 | 470 | −12 |

Remaining global distance: 31,525 words above 115,000 (41,525 above the stretch
105,000), 371 chapter subheadings above 550, and 184 text fences above 250.
Those are Phase 5 targets, not unmet sample-chapter criteria. Forbidden phrases
and closing-perspective sections remain zero. Shell fences remain `sh`.

New executable companion application code: **117 C++ lines** (85 Asio server,
32 greeting client); existing companion application sources: **0 added/removed**.
New lab verification code: **262 lines** (27 C++ model experiment and 235 Python
harness/observation lines). Counter regression support adds **2 lines**; the phase
exit checker and CMake/CI/style support are accounted separately from application
code. The explicitly requested Asio comparison needs an independent implementation;
the other labs reuse canonical examples and the canonical model rather than copy
those implementations. The greeting solution inherits reflection and changes only
initiation. This is authorized teaching material, not a fix requiring production
framework expansion.

### Recheck before Phase 3

Run the following from the repository root; use the actual installed prefix.
Do not substitute file existence for successful command execution:

```sh
python3 ci/manuscript-metrics.py --output /tmp/phase-2-recheck.json
cmp /tmp/phase-2-recheck.json review/proposal-readiness-2026-09-22/metrics-after-phase-2.json
python3 review/proposal-readiness-2026-09-22/check-phase-2.py
python3 ci/test-manuscript-metrics.py
bash ci/check-source-hygiene.sh
python3 ci/check-source-alignment.py
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc" BOOK_EXAMPLES_BUILD_DIR="$PWD/build/proposal-readiness-phase-2-examples"   bash ci/build-companion-examples.sh
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc"   ctest --test-dir build/proposal-readiness-phase-2-examples --output-on-failure --no-tests=error
cmake --build build/proposal-readiness-phase-2 --target pdf
```

Check the final LaTeX log for `Warning`, `Overfull`, and `Underfull`; all counts
must remain zero. Read `chapter-ledger.md` to recheck pedagogical coverage and
public solution quality. The scripted metrics comparison will surface later
author edits explicitly; reconcile an authorized change without rewriting this
historical baseline. Stop here: Phase 3 remains unstarted.


## Phase 2 follow-up — sample chapter strengthening

Completed 2026-09-22 under the author's same-phase request. Phase 3 remains
unstarted. The entry working tree was clean. Before editing, reran the current
Phase 2 checker, hygiene/alignment, companion build, all five existing labs, and
PDF target: `phase-2-follow-up-entry-{checks,hygiene,build,labs,pdf}.log`.
`metrics-before-phase-2-follow-up.json` reproduces the previously saved current
metrics; the intentional epilogue restoration is still preserved.

### Edited and reread

- Chapter 1: `manuscript/chapters/01-why-snodec-exists.md:71` adds clearly labeled,
  side-by-side function excerpts, 12 and 16 lines. Both are whitespace-only
  reflows of the companion functions; `check-phase-2.py` now checks that equality.
  The existing comparison table stays. The revised layer argument starts at
  line 141: carrier/security changes, protocol-specific interpretation, shared
  acceptance, then C++ expression and the connected node.js comparison. The
  protocol inventory is removed. O2 at line 10 is a reading-time trace objective;
  both Chapter 1 labs explicitly follow Chapter 2.
- All five exercise callouts now have five exercises: two review, two labs, one
  design. Chapter 3:542; Chapter 23:441; Chapter 35 and Chapter 37 final callouts.
  `chapter-ledger.md:18` records all 25 objective↔exercise mappings, including
  public solutions. Each README has corresponding numbered answers/discussions
  and two reproducible lab commands. The checker requires matching IDs, counts,
  tiers, objective coverage, and public answer sections.
- Chapter 35: `manuscript/chapters/35-building-minigateway.md:135` adds a four-step
  source assembly order before the source tree. Small `Needspace` directives keep
  the shared-model introduction and final recap together. Every original fenced
  block remains byte-identical, as checked in `phase-2-exit-checks.json`.
- Chapter 37 trims repeated framing to accommodate the new exercises. The
  decision tables and rule boxes remain. The five revised endings and public
  answers were reread together, with the surrounding chapter arguments and listing
  locations checked in context; ledger notes distinguish this from rendering.

### Current measurable exits

Original Phase 2 entry remains the denominator for the prose-reduction target.
All added objectives, exercises, and prose count toward the result; code does not.

| Chapter | Original prose → current | Reduction | Average section prose | Exercises |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2,343 → 1,723 | 26.46% | 327.00 | 5 |
| 3 | 2,674 → 1,987 | 25.69% | 315.50 | 5 |
| 23 | 3,664 → 2,897 | 20.93% | 398.00 | 5 |
| 35 | 2,378 → 1,863 | 21.66% | 294.33 | 5 |
| 37 | 2,395 → 1,859 | 22.38% | 291.00 | 5 |

The full comparison section is 638 whitespace tokens, including excerpts
and layout markup, below 1,200. Whole-book words: 146,525 → 146,950
(+425); prose: 132,172 → 132,500; fenced tokens:
14,353 → 14,450. Chapter subheadings remain 921; text fences 434;
rule boxes 20; forbidden phrases and closing-perspective sections 0; shell label
`sh`. All non-sample manuscript inputs remain unchanged. Global condensation
remains later-phase work: 31,950 words above 115,000, 371 chapter subheadings
above 550, and 184 text fences above 250. PDF pages remain **470 → 470**.

### Built and run

| Check | Result | Evidence in this directory |
| --- | --- | --- |
| Editorial exits, excerpts, objective/answer mappings, preservation | passed | phase-2-follow-up-exit-checks.log; phase-2-exit-checks.json |
| Source hygiene and 36 complete marked listings | passed | phase-2-follow-up-hygiene.log; phase-2-follow-up-alignment.log |
| Authoring-note guards and metrics regression | 9 guard fixtures; 5 counter tests passed | phase-2-follow-up-guards.log; phase-2-follow-up-metrics-tests.log |
| Companion build including Asio and both new C++ lab executables | passed, supplied installation | phase-2-follow-up-companion.log |
| All public labs | 10/10 passed, including five new cases | phase-2-follow-up-labs.log |
| Full PDF target | passed; 470 pages | phase-2-follow-up-pdf-final-build.log; pdfinfo-phase-2-follow-up.txt |
| Final LaTeX log and three-pass console | zero warnings, overfull boxes, underfull boxes | phase-2-follow-up-latex-final.log; phase-2-follow-up-pdf-final-build.log |
| Rendered layout | 49 pages inspected, including all five samples and TOC tail | phase-2-follow-up-visual-review.md; phase-2-follow-up-rendered-pages.json |

The added lab evidence is concrete: independent peers on both echo servers;
second-listener bind failure with continued reflection from the original server;
matching SSE observations and continued operation after one observer closes;
rejected invalid input without state/notification changes; and shared versus
separate model-instance ordering. The C++ labs link the canonical model/codec
sources, and Python labs use the existing socket/HTTP programs. No application
implementation was duplicated or changed. Existing CI discovers the ten tests
through CTest (`.github/workflows/companion-examples.yml`, “Run public exercise
labs”). **Hosted CI was not executed**; the compilation and runtime claims here
refer to the local run. Broker delivery, hardware, and deployment are not verified.

The first generated LaTeX exposed Pandoc escaping a code-style attribute.
The final version uses a locally scoped listings style in Chapter 1 and explicit
style selection, without changing global production styles. Subsequent visual
review corrected the two Chapter 35 page-break issues. Early build evidence stays
in `phase-2-follow-up-pdf-build.log`; the final log above is authoritative. Archived
logs normalize trailing horizontal whitespace only; diagnostic lines are retained.

Application production code: **+0/−0**. New lab/test support: **+176/−4** lines
(130 lines of public lab solutions, +28/−2 CMake registration, +18/−2 editorial
checker). The additions implement the explicitly requested extra exercises and
reuse existing test helpers and canonical application code. Documentation,
manuscript layout, metrics, and evidence are counted separately in the diff.

### Re-verify before a later phase

Use the Phase 2 re-verification commands above with the current checker and metrics;
CTest must now discover and pass **ten** tests. Compare with the current
`metrics-after-phase-2.json`, retaining fresh logs separately. Require the current
five-exercise/three-tier mappings, exact excerpts, 20% prose reductions, 250-word
section averages, preserved complete listings, and a PDF free of warnings/bad
boxes. Stop here: this commit completes only the requested Phase 2 follow-up.


## Phase 3 — teaching-book proposal package

### Entry gate and scope

Phase 2 was re-verified before the proposal edits. Fresh metrics exactly match
`metrics-after-phase-2.json`; see `phase-3-entry-metrics.json`. The current
`check-phase-2.py` passed all five prose reductions, section averages, objectives,
25 exercise mappings, public answer paths, paired excerpt comparisons, and
listing-preservation checks (`phase-3-entry-checks.log`). The ledger and public
solution descriptions were reread against those requirements. The author's
restored epilogue remains part of this accepted baseline.

Executed entry checks: hygiene, 36 complete-listing alignments, five metrics
regression tests, nine authoring-note guard fixtures, companion compilation,
all ten local labs, and the full PDF build. Evidence is in
`phase-3-entry-{hygiene,alignment,metrics-tests,guards,companion,labs,pdf,latex}.log`.
The rebuilt full manuscript has 470 pages and zero warnings/bad boxes.

The session supplied no new author facts: its field was the placeholder
`<your facts>`. The author explicitly answered **“Continue with [AUTHOR TO
SUPPLY]”**. Missing biography, platform, adoption, statistics, endorsements, and
delivery-date evidence therefore remain marked placeholders. Public project
facts and their limits are identified separately; no quotation is attributed
to an author-supplied biography.

### Edited and reread: proposal, evidence sheet, and sample guide

All three proposal documents were edited and reread in full. The seven required
components are evidenced in `review/proposal/book-proposal-package.md`:

| Required component | Evidence and resulting treatment |
| --- | --- |
| Single-paragraph pitch | Line 1: problem, independent learner, multi-protocol outcome, first-party design perspective |
| Teaching-book reader and path | Line 18: stated prerequisites, no SNode.C knowledge, learning without a lecturer; one secondary course-use sentence; one cumulative path and one optional shortcut |
| Verified comparables | Line 36: five real titles, authors, publishers, dates, and scope-based distinctions; primary records below |
| TOC and measured extent | Line 46: all 38 current chapter titles; measured pages for each Part, preliminary matter, epilogue, and references; total 470 |
| Measurable revision plan | Line 118: completed sample work versus remaining prose, headings, boxes, exercises, and progression targets; no unapproved consolidation represented as complete |
| Author platform and market evidence | Line 134: documented project relationship distinguished from independent adoption, with explicit missing-evidence items |
| Clear external-facing language | Lines 148–152: short local compilation/lab facts and their limits; no review-pass, agent-workflow, or CI-history narrative |

`review/proposal/evidence-sheet.md:9` separates public project facts from local
book-package evidence (line 15) and missing author material (line 24).
`review/proposal/sample-chapters.md:9` explains what each selection demonstrates
and what the reader can observe. Its introduction explains original chapter
numbers versus the combined PDF's navigation numbers. Sample membership remains
1, 3, 23, 35, and 37; the existing CMake sample list remains authoritative.

Public source inspection used the [SNode.C project introduction and copyright](https://github.com/SNodeC/snode.c)
and [MQTTSuite README](https://github.com/SNodeC/mqttsuite), read on 22 September
2026. These support the course origin, public framework, named copyright holder,
and first-party application roles. The creator/maintainer description is explicitly
attributed to `manuscript/frontmatter/author-note.md`; it is not offered as an
independently checked CV. No readership, adoption, sales, or deployment figure
is inferred from these sources.

### Bibliographic verification

Publisher product pages were opened and read on 22 September 2026. Their displayed
bibliographic details and contents support the proposal's facts and scope
comparisons. Machine-readable details, ISBNs, and URLs are in
`phase-3-bibliography.json`.

| Title and authors | Publisher, edition, publication | Primary record |
| --- | --- | --- |
| UNIX Network Programming, Volume 1: The Sockets Networking API — W. Richard Stevens, Bill Fenner, Andrew M. Rudoff | Addison-Wesley Professional; 3rd; 2003-11-14 | [Publisher; ISBN 9780131411555](https://www.informit.com/store/unix-network-programming-volume-1-the-sockets-networking-9780131411555) |
| Boost.Asio C++ Network Programming Cookbook — Dmytro Radchuk | Packt Publishing; 1st; 2016-01-25 | [Publisher; ISBN 9781783986545](https://www.packtpub.com/en-au/product/boostasio-c-network-programming-cookbook-9781783986545) |
| Hands-On Network Programming with C — Lewis Van Winkle | Packt Publishing; 1st; 2019-05-13 | [Publisher; ISBN 9781789349863](https://www.packtpub.com/en-gb/product/hands-on-network-programming-with-c-9781789349863) |
| Node.js Design Patterns — Luciano Mammino, Mario Casciaro | Packt Publishing; 4th; 2025-09-25 | [Publisher; ISBN 9781803238944](https://www.packtpub.com/en-au/product/nodejs-design-patterns-9781803238944) |
| C++ Concurrency in Action — Anthony Williams | Manning Publications; 2nd; 2019-02 | [Publisher; ISBN 9781617294693](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition) |

The Stevens/Fenner/Rudoff record distinguishes publication in November 2003
from copyright 2004; the proposal prints both. Node.js Design Patterns uses the
verified fourth edition and its listed Mammino/Casciaro author order. Five
comparables satisfy the requested range; no unverified candidate is included.

### Built, packaged, and run

The delivery invariant is that the archive contains the same public solutions,
companion sources, and PDFs that the proposal promises. Inspection found the
package directory list covered only `companion/examples`, omitting the new
exercise tree. `packaging/cmake/MakeProposalPackage.cmake` now copies the existing
canonical `companion` root instead and excludes Python cache directories through
the existing exclusion list. `packaging/PACKAGE-CONTENTS.txt` identifies the
public solutions. No separate solution copy or implementation is introduced.

The proposal profile now uses the book's existing bold/bold-italic monospaced
font mapping and caption-option cleanup. Its redundant document contents page
is removed; the proposed book TOC remains in the text. The sample guide starts
each selection on a fresh page, keeps short teaching callouts together, and
reserves room after subheadings. These changes apply to proposal artifacts.

| Artifact | Entry PDF pages | Final pages | Evidence |
| --- | ---: | ---: | --- |
| Proposal plus evidence sheet | 11 | 6 | phase-3-book-proposal-package-pdfinfo.txt |
| Proposal plus guide and five samples | 65 | 54 | phase-3-book-proposal-sample-package-pdfinfo.txt |
| Full manuscript | 470 | 470 | phase-3-snodec-book-pdfinfo.txt |

Entry proposal/sample counts refer to the existing PDFs observed before this
phase's builds; the entry full manuscript was freshly rebuilt. Final Part
extents come from the generated full-book TOC and actual PDF count;
`phase-3-pagination.json` records physical and printed boundaries. Preliminary
matter is 20 pages, the main pagination is 450 pages, and all extents sum to 470.
These are present A4 estimates, not an invented final publisher page count.

Executed `proposal`, `proposal-sample-pdf`, and `proposal-package`; the final
package target also rebuilt all three PDF dependencies. `phase-3-package-final.log`
and the three `phase-3-*-latex.log` files have **zero warnings and zero bad boxes**.
The initial font/caption diagnostics and intermediate pagination convergence are
retained in the earlier Phase 3 build logs rather than concealed.
`phase-3-pdf-checks.json` records final PDF digests and counts.

The archive was extracted to a fresh temporary directory, configured against the
installed SNode.C prefix, and all companion/example/exercise targets compiled.
All ten CTest labs then ran and passed. Exact commands and output are in
`phase-3-archive-companion-build.log` and `phase-3-archive-labs.log`.
`phase-3-archive-check.json` records the extraction and confirms that every tracked
companion source in the final archive is byte-identical both to the workspace
and to that compiled extraction; all three final PDFs match the delivered files.
The archive has unique entries and contains no Python caches. Later typography
builds changed only PDF/package bytes, not the compiled companion sources.

Final hygiene and complete-listing alignment pass (`phase-3-hygiene.log`,
`phase-3-alignment.log`). `check-phase-3.py` rechecks document coverage, recorded
bibliographic facts, current metrics, Part totals, clean final PDF logs, and
archive/file identity; execution is recorded in `phase-3-exit-checks.log` and JSON.
This mechanical check supplements the editorial and source-page reread above.
Rendered PDF inspection is recorded in `phase-3-visual-review.md`.

### Metrics, accounting, and limits

`metrics-after-phase-3.json` is identical to the Phase 2 exit and the fresh Phase
3 entry. There are no edits under `manuscript/`; `git diff --name-only -- manuscript`
is empty for this phase. Total words remain 146,950; prose 132,500; fenced words
14,450; chapter subheadings 921; average section length 132.89; text fences 434;
rule boxes 20; closing sections and forbidden hits zero. Every manuscript metric
delta is zero. Global condensation and all remaining chapter pedagogy await their
specified phases.

Application production code: **+0/−0**. Companion/test implementation: **+0/−0**.
Package build support: **+2/−1**; PDF metadata: **+5/−1**. Proposal/sample layout,
package contents documentation, and editorial/evidence records are documentation;
the 72-line Phase 3 checker is review-only validation support (+72/−0). No new application
architecture or second source of companion solutions is added.

Phase 3 is **completed** against its explicit exits. Missing author/platform facts
are the authorized placeholders, not fabricated evidence; delivery timing and the
strength of the market case remain unresolved. Hosted CI, broker delivery,
hardware, deployment certification, and publisher acceptance are not newly
verified. No Phase 4 plan, chapter consolidation, or approval is implied.

### Recheck before Phase 4

Re-run these commands independently so one failure does not suppress another:

```sh
python3 ci/manuscript-metrics.py --output /tmp/phase-3-recheck.json
cmp /tmp/phase-3-recheck.json review/proposal-readiness-2026-09-22/metrics-after-phase-3.json
python3 review/proposal-readiness-2026-09-22/check-phase-2.py
bash ci/check-source-hygiene.sh
python3 ci/check-source-alignment.py
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc" BOOK_EXAMPLES_BUILD_DIR="$PWD/build/proposal-readiness-phase-2-examples" bash ci/build-companion-examples.sh
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc" ctest --test-dir build/proposal-readiness-phase-2-examples --output-on-failure --no-tests=error
cmake --build build/proposal-readiness-phase-2 --target proposal proposal-sample-pdf proposal-package
python3 review/proposal-readiness-2026-09-22/check-phase-3.py
```

Re-read the proposal's seven required components, the publisher records above,
and the teaching path; inspect any newly changed PDF pages. Check the rebuilt
console and final LaTeX logs for zero warnings/bad boxes. Stop on a failed exit.
Phase 4 remains a planning-only session ending **awaiting author approval**;
no changes under `manuscript/` are authorized by that phase. This session stops
with the Phase 3 commit.


## Phase 4 — consolidated teaching-book plan (awaiting author approval)

### Previous-phase gate: executed again

The working tree was clean on entry. Fresh `phase-4-entry-metrics.json` exactly
matches `metrics-after-phase-3.json`; the comparison ran successfully.
`phase-4-entry-source-checks.json` records successful metrics, comparison,
Phase 2 sample exits, hygiene, and complete-listing alignment, with the individual
`phase-4-entry-{metrics,metrics-comparison,samples,hygiene,alignment}.log` files.
The companion build passed (`phase-4-entry-companion.log`).

The initial sandboxed runtime check passed three model-only labs but could not
create sockets for the other seven (`phase-4-entry-labs.log`: `PermissionError`,
operation not permitted). The same unmodified tests were rerun with approved
local socket access: **all ten passed**, exit 0, recorded in
`phase-4-entry-labs-local.log`. This is a resolved execution-environment restriction,
not a suppressed test or a changed runtime implementation.

All three required targets (`proposal`, `proposal-sample-pdf`, `proposal-package`)
were executed; the package dependency also rebuilt the full manuscript. The
console (`phase-4-entry-package.log`) and each preserved
`phase-4-entry-*-latex.log` have zero warnings and zero bad boxes. Actual PDF
counts remain proposal/evidence **6**, combined samples **54**, full manuscript
**470**. The previous phase's checker passed against the fresh artifacts and
archive. Its output is captured as `phase-4-entry-proposal-checks.json` and log;
its output filename was redirected in memory so the Phase 3 evidence is preserved.
No PDF layout inputs changed; no new visual reread is claimed.

The proposal's seven components and independent-learning path were reread.
The five bibliographic records were rechecked against primary publisher results;
`phase-4-entry-bibliography.json` records the details. InformIT direct opens timed
out, but its returned publisher search record confirmed the same print ISBN,
authors, edition, publication date, and copyright year. The Asio record was read
through Packt's US URL when the AU page did not load. Sources:
[InformIT](https://www.informit.com/store/unix-network-programming-volume-1-the-sockets-networking-9780131411555),
[Packt: Asio cookbook](https://www.packtpub.com/en-us/product/boostasio-c-network-programming-cookbook-9781783986545),
[Packt: C networking](https://www.packtpub.com/en-gb/product/hands-on-network-programming-with-c-9781789349863),
[Packt: Node.js](https://www.packtpub.com/en-au/product/nodejs-design-patterns-9781803238944),
and [Manning](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition).
The approved [AUTHOR TO SUPPLY] items remain unchanged. The Phase 3 entry gate
therefore passes; no manuscript prerequisite gap was found.

### Plan written and reread

`RESTRUCTURE-PLAN.md` was written and reread as a proposal for approval, not an
executed restructuring. Structural inspection used the Markdown inputs, their
headings and measures, the candidate chapters' explanatory passages, adjacent
prerequisites, source markers, and existing companion/lab surfaces. This is not
a claim of a fresh line-by-line editorial reread of all 38 chapters.

| Required planning item | Evidence and conclusion |
| --- | --- |
| All five candidate merges argued | RESTRUCTURE-PLAN.md:31; each is accepted with stated teaching boundaries; old 4's minimum introduction stays on the main path |
| Consolidated TOC and per-chapter budgets | RESTRUCTURE-PLAN.md:128; 30 numbered chapters, 11 named Parts, Appendix A, epilogue, and all supporting matter total 112,250 words |
| Complete old→new map | RESTRUCTURE-PLAN.md:245; all 38 old numbered chapters have destinations; sample identities remain distinct |
| Every affected manual reference | phase-4-reference-map.md:1 and phase-4-reference-inventory.json; 374 occurrences, 326 migration treatments; all 276 metrics-counted singular manuscript references covered |
| Index/figure impact | RESTRUCTURE-PLAN.md:348; 18 retained figure labels/assets, 1,033 index insertions / 821 keys, five hardcoded page marks, and 30 Part-reference occurrences |
| Early MiniGateway milestones and Part checkpoints | RESTRUCTURE-PLAN.md:395; eleven runnable checkpoint plans with explicit expected outcomes and existing-versus-future evidence |
| Cumulative-path risks and implementation sequencing | RESTRUCTURE-PLAN.md:438 and 453; protects prerequisites, canonical model, complete capstone listings, public solutions, and intent-aware reference validation |

The plan reduces numbered chapters by consolidating repeated treatments and
moves the contributor material into a counted appendix. The old final judgment
chapter joins the capstone Part. Every source input is allocated once; the small
source-reading transfer remains within the destination budgets. The 112,250-word
plan requires **34,700 fewer total words**, leaving 2,750 below the hard ceiling.
All 14,450 current fenced tokens are retained in its conservative arithmetic;
new teaching apparatus is budgeted within, not above, the totals. Proposed heading
ceilings sum to 269, with actual section averages still required to reach 250.
The plan does not claim these future prose or pedagogical results are achieved.

The reference register records singular/plural mentions, ranges, line-wrapped
lists, printed README references, current publication/companion documentation,
and relevant tool messages. It explicitly distinguishes the legacy authoring-note
guard from reader references. A range containing old Chapter 4 is not blindly
mapped into a prerequisite on the contributor appendix. References between merged
chapters require meaningful section targets, and numerical validity alone will
not suffice for Phase 5a's planned reference check.

`check-phase-4.py` ran successfully (`phase-4-plan-checks.log` and JSON). It checks
all 62 ordered inputs are accounted once, current row totals/fenced counts,
complete chapter mapping, budget arithmetic, sample prose-budget limits against
the original Phase 2 thresholds, inventory coverage and current source locations,
figure assets, and one checkpoint for each proposed Part. This review-only checker
validates a proposed plan; it is not Phase 5a's unimplemented reference validator.

### Unchanged manuscript and phase exit

`metrics-after-phase-4.json` is byte-identical to the Phase 3 exit and Phase 4
entry measurements. Total words **146,950**, prose **132,500**, fenced words
**14,450**, chapter subheadings **921**, average section length **132.89**, text
fences **434**, rule boxes **20**, closing sections **0**, forbidden hits **0**:
all deltas are zero. PDF pages before/after are 6/6, 54/54, and 470/470.

`git diff HEAD --name-only -- manuscript` produced no paths; the check also runs
inside `check-phase-4.py`. The final changed-file audit is captured in
`phase-4-scope-check.log`: only the active plan/report/evidence directory and
EDITORIAL-WORK-PLAN.md are changed. The proposal, manuscript, companion, production
configuration, and existing CI implementations receive no edits in this phase.

Application production code **+0/−0**; companion/test implementation **+0/−0**;
existing build/CI support **+0/−0**. The new 82-line checker is review validation
support; all other additions are planning documents, measurements, or execution
evidence. No new milestone program or solution is implemented. No new broker,
database, hardware, deployment, or hosted-CI result is claimed.

The Phase 4 document and no-manuscript-change exits are satisfied. Its required
status is **awaiting author approval**, not completed. Approval has not been
recorded and Phase 5a has not started. The next session must first obtain/record
approval of the concrete TOC, budgets, and milestone plan. Before implementation,
rerun `check-phase-4.py`, the Phase 3 entry commands above (capturing new output
separately), and the no-manuscript-change/plan coverage checks against this phase's
recorded inputs. If the author requests a different plan, revise the plan and its
arithmetic in Phase 4 before applying it. Stop after this Phase 4 commit.


## Phase 5a — approved structure applied, 2026-09-22

### Approval and entry gate

**Authorization:** `review/EDITORIAL-WORK-PLAN.md:894` records the author's approval
of the 30 chapters, eleven Parts, Appendix A, 112,250-word plan, merge boundaries,
and MiniGateway milestones, with four amendments. `phase-5a-approved-structure.json`
records that map and its current paths, chapter budgets, Part membership, protected
cut chapters, reserve, and amended session schedule. The Phase 4 proposal and
inventory remain historical planning evidence; their closing approval request is
superseded by the author's recorded approval, not silently treated as permission.

Before manuscript changes, the Phase 4 checker reran successfully against the
unchanged manuscript: `phase-5a-entry-plan-checks.json` verifies its arithmetic,
all 62 old inputs, inventory coverage, and empty manuscript diff. The Phase 4
commit's manuscript diff was also empty. Fresh metrics in
`phase-5a-entry-metrics.log` equal `metrics-after-phase-4.json`. The author approval
changes session ownership and pedagogical constraints, not the approved map or
112,250-word arithmetic; no reserve was consumed.

The previous phase's listed implementation checks were executed anew: hygiene,
source alignment, companion build, ten labs, all three proposal/package targets,
and the Phase 3 exit checker. Evidence: `phase-5a-entry-hygiene.log`,
`phase-5a-entry-alignment.log`, `phase-5a-entry-companion.log`,
`phase-5a-entry-labs.log`, `phase-5a-entry-package.log`, and
`phase-5a-entry-proposal-checks.json`. Its checker output was redirected in memory
so historical Phase 3 evidence stayed untouched. The seven proposal sections and
five recorded publisher bibliography records still pass the content check.
No new live publisher-site verification is claimed in this structural phase.
Entry PDF counts were proposal 6, samples 54, manuscript 470, with clean logs.

### Applied structure and editorial limits

**Edited and reread:** the moved chapter headings, merged section boundaries,
changed references and prerequisite sentences, Part introductions, reading guide,
README positioning, STRUCTURE table, sample bridge, and companion navigation.
The author-approved map is now the manifest order: 30 numbered chapters in eleven
Parts, followed by the unnumbered epilogue and Appendix A before reference material.
Current source paths and all old→new identities are in
`phase-5a-approved-structure.json`; the source diff shows the moves and joins.

The five approved consolidations preserve the constituent technical sections.
Their former chapter headings become named sections. Duplicate recap shells are
joined into one five-point recap per consolidated chapter. The small existing
public-type/header/component explanation moves from old 4 into current 4; it is
not duplicated in Appendix A. Current 4 starts from EchoPair, rather than assuming
that the learner has read the contributor appendix. References in current 6 now
introduce current 7's connection-lifecycle discussion as upcoming work. The final
judgment chapter belongs to Part XI and points to Appendix A for extension.

The existing two running-head mechanisms use shorter navigation labels after
renumbering; the runtime section label uses its actual section counter. The
unnumbered epilogue opener resets the running head to EPILOGUE. The epilogue essay
itself remains byte-identical. No objectives, recap, or exercises were added to it.
The environment reconstruction passage is also unchanged; its ordinary later
chapter references follow the new numbering (`check-phase-5a.py`).

**Not claimed:** a new line-by-line editorial reread of all retained manuscript
prose, completed condensation, newly implemented MiniGateway milestones, or new
teaching apparatus. Those belong to the author-approved later sessions. The
larger merged chapters deliberately retain detailed explanations and listings
until their dedicated Part review; their budgets are not yet met.

### Cross-references and consumers

`ci/check-chapter-references.py` checks the ordered chapter and Part identities,
39 unique topic anchors, and **360 current references** across all manuscript
inputs, README, STRUCTURE, and companion Markdown. Numeric, plural/range,
appendix, and relocated section references retain intended subject anchors from
the approved old→new map. The main-path source-reading introduction has its own
explicit destination. A valid number alone cannot satisfy the check.

`phase-5a-reference-register.json` provides a disposition for **all 374** original
inventory occurrences. Nine disappear or are rephrased with explicit reasons:
old 5's prerequisite/closing (R086/R090), old 7's two fixed running heads and
backward prerequisite (R096/R097/R099), old 37's two running heads
(R342/R343), and the removed Part XII opener (R366/R367). Original authoring-note
policy strings remain guards. The approved Phase 3 proposal/evidence snapshot is
explicitly outside current-manuscript renumbering until Phase 6; the sample bridge
explains the old/current identities and its selection table uses current numbers.

Five regression tests exercise the current structure, an unregistered reference,
reordered chapters, a missing topic anchor, and a **valid-but-wrong number even
when its display label is mechanically updated in the register**. Evidence:
`phase-5a-reference-tests.log`. Hygiene runs the checker and its regression tests;
the companion workflow also runs the checker. The archive includes its two
required identity/register JSON files. `phase-5a-archive-hygiene.log` proves the
packaged copy runs without relying on an unshipped working-tree file.

`ci/check-source-alignment.py` now gets chapter/appendix coverage from the ordered
manifest, replacing its hardcoded 38-chapter check. Current source-claim records
are remapped by union of their contracts and anchors; historical evidence is not
rewritten. All **36 marked complete listings**, **293 executable/configuration
fences**, **1,033 index insertions**, and **18 figure labels** are preserved.
Evidence: `phase-5a-hygiene.log` and `phase-5a-exit-checks.json`.

The sample identities are **1, 3, 18, 28, 30**. CMake's sample inputs and public
exercise folders/targets/tests move with them. The twelve lab implementation files
remain byte-identical across the moves. `chapter-ledger.md` records the identity
translation without rewriting Phase 2's historical measures or objective IDs.
All five samples retain their ≥20% original prose reduction, ≥250 section average,
three objectives, five mapped exercises in all three tiers, and public answers.
The exact current figures are in `phase-5a-exit-checks.json`.

### Builds, runtime checks, and visual review

**Built and run successfully:**

- Source hygiene, alignment, chapter-reference check and five negative/positive
  regression tests: `phase-5a-hygiene.log` and `phase-5a-reference-tests.log`.
- Measurement regression tests: `phase-5a-metrics-tests.log`.
- Full companion build including standalone Asio and renamed sample lab targets:
  `phase-5a-companion-build.log`.
- All ten public labs: `phase-5a-labs.log`.
- Teaching, behavioral, and lifetime/echo checks:
  `phase-5a-teaching-smoke.log`, `phase-5a-behavior-smoke.log`, and
  `phase-5a-lifetime.log`.
- `proposal`, `proposal-sample-pdf`, `proposal-package` (including full `pdf`):
  `phase-5a-package-final.log`. The initial build logs retain the observed running
  header and first-pass convergence warnings; those were resolved. All three
  preserved `phase-5a-*-latex.log` files (trailing whitespace normalized) and the final build console contain
  **zero LaTeX warnings and zero bad boxes**.
- Package source refresh after CI/register documentation changes:
  `phase-5a-package-source-refresh.log`. `check-phase-5a.py` verifies every one of
  the **289** archived files against its current source/PDF, with no duplicates
  or Python cache files (`phase-5a-exit-checks.json`). The extracted archive also
  passes hygiene and reference tests (`phase-5a-archive-hygiene.log`).

Local runtime checks used approved local socket access. These are executed local
results, not a claim of hosted-CI execution or new deployment/hardware validation.
Changed chapter openings, merge boundaries, headers, appendix placement, and the
sample bridge received targeted rendered review, recorded in
`phase-5a-visual-review.md`. This is not an all-page visual reread.

| PDF | Before | After |
| --- | ---: | ---: |
| Proposal/evidence snapshot | 6 | 6 |
| Proposal with five current samples | 54 | 54 |
| Full manuscript | 470 | 458 |

The proposal/evidence source documents remain byte-identical to the approved entry
snapshot. The author explicitly assigns their TOC, positioning/evidence, and page
refresh to **Phase 6**. Their earlier extent is therefore not presented as the
new manuscript's pagination. The sample bridge is a necessary navigation repair,
not an early proposal rewrite.

### Metrics and phase exit

Evidence: `metrics-after-phase-5a.json` versus `metrics-after-phase-4.json`.

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Total words | 146,950 | 146,210 | −740 |
| Prose words | 132,500 | 131,744 | −756 |
| Fenced words | 14,450 | 14,466 | +16 |
| Chapter headings, level 3 and deeper | 921 | 934 | +13 |
| Average section prose | 132.89 | 130.30 | −2.59 |
| Text fences | 434 | 434 | 0 |
| Rule boxes | 20 | 20 | 0 |
| Remember boxes | 38 | 31 | −7 |
| Closing-perspective sections / forbidden hits | 0 / 0 | 0 / 0 | 0 / 0 |

The new section shells make the retained source treatments identifiable; the
heading increase is reported rather than hidden by relabeling. Fenced-word
changes are text-reference wording and LaTeX navigation, not executable-code cuts.
The book remains **31,210 words above 115,000**, 41,210 above the stretch target,
384 headings above 550, and 184 text fences above 250. These are later condensation
requirements, not Phase 5a exits. The approved planned total remains **112,250**;
reserve used **0**, reserve remaining **2,750**.

`check-phase-5a.py` passes (`phase-5a-exit-checks.log` and JSON): approved TOC,
references, preservation, sample pedagogy, rendered numbering, clean final PDFs,
and archive contents. Full build and all listed local checks pass. Phase 5a is
**completed**; Phase 5b has not started. The commit is
`proposal-readiness: phase 5a — apply approved teaching-book structure`.

Application production code **+0/−0**; existing lab implementation **+0/−0**
(exact moves). The new reference checker is **98 lines** of CI support and its
regression tests are **73 lines** of test support; the report-local exit checker
is **122 lines** of verification support. Small existing CI/build edits replace
fixed chapter assumptions and register renamed targets. Documentation, narrative
joins, source-claim mapping, and evidence are accounted separately from application
code. No production architecture or framework implementation is added.

### Handoff: recheck before Phase 5b

Read PROMPT.md, the recorded author approval, and the approved structure JSON.
Before the next Part edit, regenerate metrics and rerun:

```sh
bash ci/check-source-hygiene.sh
python3 ci/test-manuscript-metrics.py
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc" BOOK_EXAMPLES_BUILD_DIR="$PWD/build/proposal-readiness-phase-5a-examples" bash ci/build-companion-examples.sh
SNODEC_PREFIX="$PWD/build/ci-fix-2026-09-22/install-gcc" ctest --test-dir build/proposal-readiness-phase-5a-examples --output-on-failure --no-tests=error
cmake --build build/proposal-readiness-phase-2 --target proposal proposal-sample-pdf proposal-package
python3 review/proposal-readiness-2026-09-22/check-phase-5a.py
```

Capture fresh evidence under the next phase's prefix. The Phase 5a checker uses
its recorded metrics and old approval snapshot; do not rewrite historical Phase
2–4 checkers to accept the new structure. Rerun the three existing runtime smoke
commands recorded above if their inputs change; their Phase 5a results are fresh.
If an entry exit fails, report the gap and stop before Part edits.

Phase 5b covers Part I only, its opener/checkpoint, public solutions, and the
approved front-matter allowance. It must add Chapter 2's short Lab environment
section listing optional MQTT broker, MariaDB, TLS fixture, and Bluetooth needs
by Part. Mark dependent labs as equipped labs and provide local-only alternatives
where possible. Do not add those in Phase 5a.

The stop rule protects current chapters **4, 6, 12, 24, 25, 26, 27**: qualify the
Part instead of removing teaching content to hit its budget. Justified reserve
use must be recorded here and never make the 2,750-word reserve negative or the
115,000 ceiling exceedable. Phase **5l is Part XI only**, including the integrated
checkpoint transferred from the epilogue to current Chapter 30. Phase **5m** owns
Appendix A, the essay-only epilogue (budget 1,900), back matter, and final global
audit. Phase **6** owns the proposal refresh. Stop after the Phase 5a commit.


## Phase 5b — blocked at the previous-phase entry gate, 2026-09-22

**No Part I editing began.** PROMPT.md, Execution control, requires: “Before
starting, re-verify that the previous phase meets its exit criteria by re-running
metrics and the listed checks … If it does not, report the gap and stop.”
The working tree was clean on entry. The author's subsequent commit
`author edit: fix two 5a seam references` remains intact.

### Exact gap

At `manuscript/chapters/22-designing-iot-systems-with-multiple-protocols.md:313`,
the author merged two redundant Chapter 12 mentions into one sentence. The
current reference register still expects two occurrences: R275 targets
`configuration-philosophy-in-snodec`; R276 targets
`application-and-instance-configuration-in-detail`. Both subjects now belong to
the single surviving Chapter 12 reference. The checker therefore reports
“unregistered/removed reference; review its intended topic”. Evidence:
`phase-5b-entry-hygiene.log` and the author commit's manuscript diff.

This is stale navigation bookkeeping, not a finding that the author correction
is wrong. Its repair needs one current occurrence retaining both topic targets
and both original migration identities. The author's Chapter 4 wording correction
also remains intact and retains its Chapter 6 destination.

Fresh metrics differ from the recorded Phase 5a exit by **−5 prose/total words**:
Chapter 4 is 7,809 rather than 7,811 words; Chapter 22 is 3,964 rather than 3,967.
Current totals are **146,205 words**, **131,739 prose**, **14,466 fenced**. These
changes come entirely from the two author edits. They should be recorded as an
authorized post-Phase-5a baseline when repairing the gate, preserving the original
Phase 5a measurements as historical evidence. Merely merging the register rows
would leave the historical Phase 5a checker's strict metrics equality unresolved.

### Executed checks and limits

| Check | Result | Evidence |
| --- | --- | --- |
| Fresh metrics, repeated independently | Same current result on both runs; differs from historical Phase 5a | phase-5b-entry-metrics.log; metrics-after-phase-5b-blocked-entry.json |
| Source hygiene | Failed at chapter-reference check | phase-5b-entry-hygiene.log |
| Source alignment, run separately | Passed | phase-5b-entry-alignment.log |
| Measurement regression tests | Passed | phase-5b-entry-metrics-tests.log |
| Companion build command | Passed | phase-5b-entry-companion.log |
| Proposal, samples, package/full PDF targets | Passed | phase-5b-entry-package.log |
| Previous Phase 5a exit checker | Failed at the same reference check; its historical output was not overwritten | phase-5b-entry-exit.log |
| Public runtime labs | Not run after failed entry gate | phase-5b-entry-results.json |

Independent entry commands already dispatched before the failure were allowed to
finish. Final PDF page counts remain **6 / 54 / 458** (proposal / combined samples /
manuscript); each current final LaTeX log has zero warnings and bad boxes. These
build results do not waive the failing semantic reference gate. No new rendered
visual review or hosted-CI result is claimed. `phase-5b-entry-results.json` records
the commands' outcomes and observed PDF counts.

Only this entry evidence, REPORT.md, and EDITORIAL-WORK-PLAN.md change in this
session. `git diff HEAD -- manuscript companion ci review/proposal` is empty.
No chapters were edited/reread as a completed refinement, no exercises or lab
solutions were added, and no reserve was used. `metrics-after-phase-5b-blocked-entry.json` is
identical to the fresh entry measurement; it is a blocked-session snapshot, not
an assertion that Part I meets its exit criteria. Application production code,
CI implementation, and test implementation all change **+0/−0**.

**Status: blocked at entry.** Record-only commit:
`proposal-readiness: phase 5b — record failed prerequisite check`.
The prerequisite reference/metric bookkeeping must be reconciled with the author
edits and the Phase 5a exit checks rerun before retrying Phase 5b. Do not revert the
author's prose or overwrite historical Phase 5a evidence. Part I's budgets,
Chapter 2 Lab environment section, mapped exercises/public solutions, and running
project checkpoint all remain pending. This session stops at the entry gate.


## Authorized prerequisite repair before Phase 5b — 2026-09-22

The author explicitly requested this repair as a separate commit before resuming
Part I. The two edits in `author edit: fix two 5a seam references` are the
authorized post-Phase-5a baseline: **146,205 total / 131,739 prose / 14,466 fenced
words**, a five-word prose reduction. `author-seam-baseline.json` records the two
files and delta; `metrics-after-author-seam-edits.json` records the fresh counts.
The reference-register diff joins R275 and R276, with both original topic anchors,
on the single Chapter 12 mention in Chapter 22:313. All 374 historical migration
dispositions remain; there are now 359 current occurrences.

**Run and passed:** hygiene (including references and source alignment), metric
regressions, companion build, all ten public labs, proposal/sample/package targets,
and all original Phase 5a exit assertions. Evidence: `author-seam-hygiene.log`,
`author-seam-metrics-tests.log`, `author-seam-companion.log`, `author-seam-labs.log`,
`author-seam-package.log`, `author-seam-exit-checks.log`, and
`phase-5a-author-seam-exit-checks.json`. The small review-only wrapper
`check-author-seam-baseline.py` first verifies the authorized delta and joined
identities, then executes the unchanged historical checker with only its metrics
input and result destination substituted in memory. The historical checker,
metrics and exit JSON are unchanged. All 289 packaged inputs match current files.
PDF pages: manuscript 458, samples 54, proposal 6; final warnings/bad boxes: zero.
No new PDF visual-review claim is made for this unchanged-prose repair.

`git diff -- manuscript` is empty for the repair. No application or lab
implementation changes. The register, baseline records and repair documentation
were edited and reread. The earlier failed-entry evidence above remains historical.
**Gate repaired; Part I may now begin** under the author's explicit continuation
request. Separate commit: `proposal-readiness: reconcile 5a register with author seam edits`.


## Phase 5b — Part I completed, 2026-09-22

The prerequisite repair above was committed separately before any manuscript
edit. Its full Phase 5a checks passed against the authorized author-seam baseline.
The earlier failed-entry snapshot is preserved byte-for-byte as
`metrics-after-phase-5b-blocked-entry.json`; `metrics-after-phase-5b.json` now holds
the completed Part I measurement. Historical Phase 5a outputs remain unchanged.

### Edited and reread

- `manuscript/chapters/02-preparing-your-environment.md:8`: three observable
  objectives; the existing preparation treatment is joined into eight sections
  instead of sixteen. Commands and public component explanations remain.
  `:412` adds the approved Lab environment section, listing MQTT broker, MariaDB,
  local TLS fixture and Bluetooth hardware by Part, and separating equipped runs
  from narrower local observations. `:434` and `:442` supply one five-bullet recap
  and five mapped exercises, with public review/design answers and two build labs.
- `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:14`: removes
  two redundant text blocks and keeps the connected runtime/factory/context
  explanation. `:526` extends existing Lab 3 into the Part I checkpoint: two
  measurement peers, exact bytes including an invalid value, and continued service
  after one peer closes. `companion/exercises/ch03/solution.py:20` checks these
  observations using the existing canonical server and harness. No accepted model
  or parser is implied by reflection.
- `manuscript/chapters/01-why-snodec-exists.md` is **reread, unchanged**: comparison
  table/excerpts, applied principles, objective O2 and after-environment labs already
  meet the approved budget and teaching contract. Its two labs were rerun.
- `manuscript/frontmatter/preface.md:10`, `how-to-read-this-book.md:3`, and
  `conventions.md:13` now address the independent learner, public solutions,
  one learning path and two shortcuts, and equipped-lab terminology.
  `manuscript/parts/part-01-getting-oriented.md:7` points to the mapped checkpoint.
  The existing Part II transition is retained. All edited reader text and public
  solutions were reread; there is no edited-but-unread manuscript remainder.

The new `companion/exercises/ch02/solution.py` builds the canonical EchoPair as an
external consumer in a temporary tree. It verifies `snodec_DIR`, builds both
executables, and runs the server against a bounded peer. Its second mode first
introduces a component typo in a temporary copy, requires configuration failure
naming that component, restores the original file and verifies build/exchange.
The governing invariant is that the installation selected by the consumer, and
the stage at which a failure occurs, must be observable. Reusing the canonical
example and shared process/socket harness avoids a second application implementation.

### Measured exit criteria

| Chapter | Total before → after | Budget | Headings before → after / ceiling | Mean section prose words |
| --- | --- | --- | --- | --- |
| 1 | 1,821 → 1,821 | 1,850 | 5 → 5 / 5 | 327.00 |
| 2 | 2,945 → 3,006 | 3,350 | 16 → 8 / 9 | 331.50 |
| 3 | 2,566 → 2,568 | 2,650 | 6 → 6 / 6 | 321.83 |

Part I totals **7,395 / 7,850 words**. Chapter 2 grows by 61 total words because
its condensed framing makes room for the teaching apparatus and lab guidance;
Chapter 3 grows by two while incorporating the checkpoint. Chapter 2 apparatus
contains 286 content words, or 301 including callout syntax (ceiling 400).
Front matter: **1,981 / 2,500**; all Part/epilogue openers: **1,017 / 1,650**.
No reserve drawn: **0 used; 2,750 remaining**.

Each Part I chapter has three objectives, one recap of at most five bullets, two
review questions, two labs, one design problem, and public answers. The complete
bidirectional mapping and lab commands are in `chapter-ledger.md` and the public
`companion/exercises/ch01`, `ch02`, and `ch03` READMEs. The sample prose reductions
remain 26.42% (Chapter 1) and 24.23% (Chapter 3); later samples also retain ≥20%.

Full manuscript: **145,973 total / 131,598 prose / 14,375 fenced words**, down
**232 total / 141 prose / 91 fenced** from the authorized seam baseline. The 91
fenced-word reduction is entirely removed/rephrased `text` blocks. All 293
executable/configuration fences, complete-listing markers, index entries and
figures are preserved by the exit check. Headings: **934 → 926**; text fences:
**434 → 429**; rules: **20 → 20**; forbidden phrases and closing sections: **0**;
shell fence label remains `sh`.

Global ceilings are due later: 30,973 words, 376 chapter subheadings, and 179 text
fences remain above their final ceilings; global mean section prose is 131.59.
This session certifies Part I only. No later Part is condensed or claimed to have
its future labs implemented; the proposal refresh remains Phase 6.

### Built, run, and inspected

| Check | Executed result | Evidence |
| --- | --- | --- |
| Fresh metrics and Phase 5b assertions | Pass: budgets, pedagogy, scope and preservation | metrics-after-phase-5b.json; check-phase-5b.py; phase-5b-exit-checks.json; phase-5b-final-exit.log |
| Metric regression tests | Pass | phase-5b-final-metrics-tests.log |
| Hygiene, semantic references, five reference regression tests | Pass; 360 current references, all 374 original dispositions | phase-5b-final-hygiene.log |
| Source alignment, separately | Pass | phase-5b-final-alignment.log |
| Companion build | Pass; existing comparison and all sample targets included | phase-5b-final-companion.log |
| Public labs | **12/12 pass**, including both new environment labs and extended checkpoint | phase-5b-final-labs.log |
| Teaching smoke tests | Pass | phase-5b-final-teaching.log |
| Behavioral smoke tests | Pass | phase-5b-final-behavior.log |
| SSE lifetime and WebSocket cases | Pass | phase-5b-final-lifetime.log |
| Proposal, sample and full PDF/package targets | Pass | phase-5b-final-package.log |
| Archive inputs and extracted hygiene | 292 packaged files match; extracted hygiene passes | phase-5b-exit-checks.json; phase-5b-final-extracted-hygiene.log |
| Final PDF logs / targeted visual inspection | Zero warnings/bad boxes; reviewed changed-page layout | phase-5b-exit-checks.json; phase-5b-visual-review.md |

Pages (before → after): **manuscript 458 → 454; samples 54 → 54; proposal 6 → 6**.
The first environment-lab run incorrectly assumed `--help` returned zero. Both
new cases failed on status 2 while the other ten passed. The final labs instead
exercise the installed server's actual byte interface; the shared harness and
its exit assertions are unchanged. Initial evidence: `phase-5b-initial-labs.log`.
These are local executions of the CI workflow commands; no hosted run or newly
executed broker, database, or Bluetooth deployment is claimed.

Navigation bookkeeping is updated only for the changed passages: three removed
route references (R353/R354/R361) retain documented dispositions; four new pointers
have explicit topic targets. The repaired R275/R276 entry remains joined. Diff
review found no application duplication, alternate model, new production state,
or change to the approved TOC. Application production implementation: **+0/−0**;
lab Python: **+58/−0**; lab CMake registration: **+8/−1**; review-only exit automation:
**+124/−0**. New test support is necessary for the two requested environment labs;
it builds canonical sources and reuses the existing runtime harness. Documentation
and generated metrics/logs are accounted separately from implementation.

**Status: completed.** Commit:
`proposal-readiness: phase 5b — refine Part I and establish the measurement checkpoint`.
Stop here. Phase 5c is the next Part session, after rerunning the current Phase 5b
metrics/assertions, hygiene/alignment, companion build, twelve labs, smoke/lifetime
checks, PDF/package targets, and extracted-package hygiene. Do not run the historical
5a checker as a Part I exit: it intentionally asserts the uncondensed prior state.


## Phase 5c — Part II completed, 2026-09-22

### Previous-phase gate, rerun before editing

The working tree was clean at entry. Fresh metrics exactly reproduced the Phase
5b snapshot (145,973 total words). The Phase 5b checker ran with only its output
path redirected to `phase-5c-entry-previous-exit-checks.json`, retaining its original
assertions and historical evidence. It passed all Part I budgets, mappings, scope,
preservation, archive identity and PDF checks. Fresh hygiene/reference regressions,
source alignment, metric regressions, companion build, all twelve existing labs,
teaching/behavior/lifetime tests, PDF/package targets and extracted-package hygiene
also passed. Evidence: `phase-5c-entry-results.json`,
`phase-5c-entry-runtime-results.json`, `phase-5c-entry-*.log` and the redirected exit
JSON. Entry page counts were **454 / 54 / 6** (full / samples / proposal).

### Edited and reread

- `manuscript/chapters/04-the-mental-model-and-layers-in-practice.md:11` now connects
  the merged mental-model and layer material through fourteen sections. Repeated
  definitions, inventories and twenty-eight text blocks become connected prose
  or comparison tables. All substantive lifetime, callback, factory, address,
  component, TLS, protocol-carrier and cross-layer explanations remain. The
  ≤300-word public-name introduction is at `:192`. The canonical measurement
  owner is introduced at `:111`, then applied in the mapped exercises at `:427`.
- `manuscript/chapters/05-core-runtime-and-event-processing.md:14` retains all
  runtime source excerpts while consolidating forty-seven headings into ten.
  State versus status, the public stepping restriction, capture/thread ownership,
  event publication, descriptor lifecycle, timers, and coordinated shutdown remain
  explicit. The new mapped Part II checkpoint is at `:250` and its lab at `:270`.
- `manuscript/parts/part-02-the-snodec-architecture.md:7` points to the model
  checkpoint and separate deferred-callback experiment. Both chapters open with
  three objectives and close with one five-bullet recap, then five exercises.
  The public `companion/exercises/ch04/README.md` and `ch05/README.md` provide all
  answers, commands and expected observations. Edited reader text and solutions
  were reread; the unchanged Part III transition was reread in context.

The Chapter 4 content-preservation stop rule was applied: no distinct teaching
explanation needed removal to meet the budget, and no reserve is drawn.
`chapter-ledger.md`, the Phase 5c content-preservation table, identifies the final
location of each retained topic. All original C++ blocks remain byte-identical
and in order in both chapters. The exit checker also preserves all 293 book-wide
executable/configuration fences, complete-listing markers, index entries and
figure declarations. Applied rule boxes are retained, not reduced to meet a quota.

### Measured exit criteria

| Chapter | Total before → after / budget | Prose before → after | Headings before → after / ceiling | Mean section prose |
| --- | --- | --- | --- | --- |
| 4 | 7,809 → 4,338 / 5,300 | 7,296 → 4,290 | 55 → 14 / 15 | 294.50 |
| 5 | 5,188 → 2,983 / 3,700 | 5,089 → 2,908 | 47 → 10 / 11 | 278.10 |

Part II: **7,321 / 9,000 words**. Each chapter has two review questions, two labs
and one design problem, complete objective↔exercise coverage, and public solutions.
The ledger records the ten forward mappings and both reverse maps. Front matter:
**1,980 / 2,500**; all Part/epilogue openers: **1,057 / 1,650**. Reserve:
**0 used; 2,750 remaining**. All five original samples retain their ≥20% prose
reductions and section-length targets; their manuscript text is unchanged here.

Full manuscript: **140,336 total / 126,451 prose / 13,885 fenced words**, down
**5,637 total / 5,147 prose / 490 fenced**. Of the fenced decrease, 489 tokens are
removed text blocks; one is the existing page-bottom directive moved out of the
manifest into metadata. Executable listings are not shortened. Chapter subheadings:
**926 → 848**; text fences: **429 → 399**; C++ fences: **199 → 199**; rules:
**20 → 20**; forbidden phrases and closing sections: **0**; shell label: `sh`.

The global limits are due in the final audit, not this Part session: 25,336 words,
298 chapter subheadings and 149 text fences remain above their final ceilings;
global mean section prose is 138.0. Later Parts, Appendix A, and the final audit
remain pending. The author-approved proposal refresh remains Phase 6.

### Built, run, and inspected

The governing lab invariants are one canonical accepted-state owner, observer
removal before captured state dies, and deferred callbacks that execute after
registration and after the current callback returns. Three new CTest entries reuse
existing sources: shared/separate model instances, independent EchoPair peers,
and model ownership/removal. The sole new C++ test, `companion/exercises/ch05/deferred-work.cpp:7`,
observes the installed public API; all captured local state outlives `start()`.
Its explicit assertions execute in release builds. This avoids another model,
protocol parser, or application implementation. The model checkpoint executes
acceptance/removal between calls; it does not claim runtime scheduling, removal
during notification, transport teardown, durability or cross-process ordering.

| Check | Executed result | Evidence |
| --- | --- | --- |
| Fresh metrics and Part II assertions | Pass: budgets, pedagogy, mappings, sample retention, scope and preservation | metrics-after-phase-5c.json; check-phase-5c.py; phase-5c-exit-checks.json; phase-5c-final-exit.log |
| Metric regression tests | Pass | phase-5c-final-metrics-tests.log |
| Hygiene and reference regression tests | Pass; 360 current references, 39 stable topics, all 374 original dispositions | phase-5c-final-hygiene.log |
| Source alignment | Pass, 36 exact complete listings | phase-5c-final-alignment.log |
| Companion build | Pass using supplied installation; all examples and labs built | phase-5c-final-companion.log |
| Public labs | **16/16 pass**, including four Part II entries | phase-5c-final-labs.log; phase-5c-runtime-results.json |
| Teaching and behavioral smoke tests | Pass | phase-5c-final-teaching.log; phase-5c-final-behavior.log |
| SSE lifetime and WebSocket cases | Pass | phase-5c-final-lifetime.log |
| Proposal, sample, full PDF and package | Pass | phase-5c-final-package.log; phase-5c-build-results.json |
| Archive input identity / extracted hygiene | All 297 packaged files match; hygiene passes from extraction | phase-5c-exit-checks.json; phase-5c-final-extracted-hygiene.log |
| PDF logs and targeted rendered-page review | Zero warnings/bad boxes; edited chapters and contents inspected | phase-5c-exit-checks.json; phase-5c-visual-review.md |

Pages (before → after): **full manuscript 454 → 438; samples 54 → 54; proposal
6 → 6**. The build directory for examples is `build/proposal-readiness-phase-5c-examples`;
PDF targets use `build/proposal-readiness-phase-2`. These are local executions of
CI workflow checks, not a hosted run or new equipped-hardware/deployment validation.

The first companion configuration failed because the imported core target was
visible only in a sibling CMake directory. The lab now explicitly finds its own
required core component; no duplicate target or implementation is introduced.
The failure remains in `phase-5c-initial-companion.log`. The initial PDF target
built but recorded one underfull contents-page box. The existing `\raggedbottom`
setting moved from `manuscript/frontmatter/mainmatter.md` into
`production/metadata/metadata.yaml` after `\makeindex`, making the book's existing
natural-bottom policy apply to the contents too. This is the only change outside
Part II manuscript text; no prose, warning threshold or suppression changed.
`check-phase-5c.py` asserts that exact one-line relocation. The initial log is
retained as `phase-5c-initial-package.log`; the final logs are clean.

Reference-register maintenance follows the edited passages: R088 and R098 have
explicit retirement dispositions for duplicate pointers; one other redundant
Phase 5a pointer is removed, and three new Part/opener/solution pointers have
explicit topic targets. Existing retained references only receive new line evidence.
The author's combined R275/R276 entry remains intact. No TOC, chapter numbering,
framework source, application implementation or historical result changes.

Diff accounting: application production implementation **+0/−0**; new lab C++
**+36/−0**; lab CMake registration **+19/−1**; book page-bottom policy **+1/−1**;
review-only exit automation **+134/−0**. Documentation and generated evidence are
separate. New test support is required to observe the requested callback contract;
it uses the existing public API and canonical examples rather than duplicating
application state or behavior. The completed diff was reviewed for duplication,
lifetime mistakes, scope expansion and accidental listing changes.

**Status: completed.** Commit:
`proposal-readiness: phase 5c — condense Part II and teach shared measurement ownership`.
Stop here. Phase 5d is next, covering Part III only. Before editing, rerun the
current Phase 5c metrics/assertions, hygiene/alignment, metric/reference tests,
companion build, sixteen labs, teaching/behavior/lifetime checks, PDF/package
targets and extracted-package hygiene. Use `check-phase-5c.py` as the current
exit checker; historical Phase 5b assertions intentionally describe the earlier
uncondensed Part II state and are not the next entry gate.


## Author-requested Phase 5c follow-up — 2026-09-22

The author requested one Part II correction before Phase 5d: merge the duplicated
public-type/name treatment, retain its stable anchor and registered references,
and leave the build section as an applied legacy-to-TLS comparison. Implemented
and reread in `manuscript/chapters/04-the-mental-model-and-layers-in-practice.md:192`.
The merged treatment is 256 whitespace tokens including its heading and syntax;
all index occurrences, code excerpts (including order), and the Layer-reading
rule remain. The build comparison now asks for separate build, handshake/identity,
and byte-reflection observations. No exercises, applications or other chapters change.

Chapter 4: 4,338 → 4,075 words, 14 → 13 sections; Part II: 7,321 → 7,058.
Fresh Phase 5c assertions pass, including the original budgets and pedagogy, source
intro cap, reference targets, all executable fences, index and figure preservation.
Hygiene/alignment, metric/reference tests, companion build, all sixteen labs,
teaching/behavior/lifetime checks, PDF/package builds, archive identity and
extracted-package hygiene pass. See `phase-5c-follow-up-results.json`,
`phase-5c-follow-up-*.log`, `metrics-after-phase-5c-follow-up.json` and
`phase-5c-follow-up-exit-checks.json`. The wrapper `check-phase-5c-follow-up.py`
retains historical assertions and redirects only metrics/log/result paths;
historical Phase 5c evidence remains unchanged. The reference register updates
only line evidence; the source-reading anchor's registered targets remain intact.

Rendered physical pages 44–45 and 47–48 were inspected after rebuilding: the merged
mapping, Layer-reading rule, applied table, recap and exercises fit without clipping
or overlap. Images are local build outputs in `build/phase-5c-follow-up-visual/`.

PDF pages: full 438 → 436; samples 54 and proposal 6 unchanged.
All final PDF warnings/bad boxes are zero. Full words: 140,336 → 140,073.
No reserve used; 2,750 remains. Application/test code growth: zero.

Separate commit: `proposal-readiness: phase 5c follow-up — remove triple name/component explanation`.
This freshly passed follow-up is the authorized Phase 5d entry baseline; the author
explicitly requests Phase 5d next in the same session.


## Phase 5d — Part III completed, 2026-09-22

### Entry gate and scope

Before Part III edits, completed the author-requested Part II repair and separately
committed it as `proposal-readiness: phase 5c follow-up — remove triple name/component explanation`.
Its freshly executed Phase 5c assertions, sixteen public labs, full checks and
PDF/package targets passed: `phase-5c-follow-up-results.json`,
`phase-5c-follow-up-exit-checks.json`, and `phase-5c-follow-up-*.log`.
`metrics-after-phase-5c-follow-up.json` is this session's entry baseline (140,073
words; full PDF 436 pages). Historical Phase 5c evidence remains unchanged.

Edited and reread: Chapters 6–8 and the Part III opener; all public answers in
`companion/exercises/ch06/README.md`, `ch07/README.md`, and `ch08/README.md`.
The unchanged Part IV opener was reread for the transition. Scope/preservation
assertions in `check-phase-5d.py` compare the current manuscript against the
separate follow-up commit: only those four Part III inputs change. All original
C++ excerpts remain byte-identical and in order; book-wide executable/configuration
fences (293), source markers, index occurrences and figure markers are preserved.
Proposal text, structure/order and production styling are unchanged in this phase.

The condensation combines repeated family introductions, mirrored endpoint
explanations and text arrows. Chapter 6's author-required content-preservation
audit is in `chapter-ledger.md`, with final section locations for every substantive
topic. Its network-family, resolution, dual-stack, Unix ownership, credential and
authorization teaching remains. Chapter 7 retains the distinct lifetimes and
callback stages; Chapter 8 retains controller/service preparation and the two
interactive Bluetooth command blocks. No reserve is needed and no teaching topic
was cut to force a budget pass.

### Budgets and pedagogy

Evidence: `metrics-after-phase-5d.json`, `phase-5d-exit-checks.json`, and the
Phase 5d chapter-ledger tables (including all fifteen exercise mappings and reverse
objective mappings).

| Chapter | Words before → after / budget | Sections / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| 6 | 8,080 → 4,168 / 5,200 | 12 / 15 | 319.25 |
| 7 | 4,859 → 3,084 / 3,650 | 9 / 10 | 324.67 |
| 8 | 2,613 → 2,170 / 2,200 | 5 / 5 | 393.40 |

Part III: **15,552 → 9,422 / 11,050 words**. Each chapter has three observable
objectives, one five-bullet recap, then two review questions, two labs and one
design problem. Every objective has an exercise and every exercise has an objective;
all fifteen public answers exist and were reread. Apparatus tokens are included
in these budgets. Front matter remains 1,980 / 2,500; all Part/epilogue openers
are 1,100 / 1,650. Reserve used: **0**; remaining: **2,750**.

| Whole-book metric | Entry → after | Delta |
| --- | ---: | ---: |
| Total words | 140,073 → 133,986 | −6,087 |
| Prose words | 126,188 → 120,567 | −5,621 |
| Fenced words | 13,885 → 13,419 | −466, explanatory text blocks only |
| Chapter headings ≥3 | 847 → 753 | −94 |
| Average chapter-section prose | 137.85 → 147.98 | +10.13 |
| Text fences | 399 → 348 | −51 |
| C++ fences | 199 → 199 | 0 |
| Rule boxes | 20 → 20 | 0 |
| Objectives / exercise callouts | 8 / 8 → 11 / 11 | +3 each |
| Forbidden phrases / Closing perspective | 0 / 0 → 0 / 0 | 0 |

The difference between the Part reduction and global reduction is the 43-word
Part III checkpoint addition. Global ceilings are not yet phase requirements:
18,986 words, 203 headings and 98 text fences remain above the final ceilings;
book-wide mean section prose is still below 250. Later Parts and the final audit
remain pending. The five earlier samples retain their required prose reductions
and section density; the current assertion results record those values.

### Companion responsibility, builds and execution

The governing invariant is one protocol implementation across carriers, with
family-specific endpoint identity and explicit resource ownership. The canonical
EchoPair context/factory remains the sole echo implementation. One 26-line thin
`companion/exercises/ch06/family-server.cpp` selects a public family type/header
at compilation, reports copied identities during the borrowed-pointer callback,
and uses the existing listen/runtime path. Five carrier targets reuse that driver.
The fixture owns its client path; the server owns its service path; assertions
run before temporary-directory cleanup. Nothing adds measurement acceptance to echo.

Existing peer and occupied-port fixtures are reused directly for Chapter 7.
The additional 27-line Bluetooth selector test opens no socket and checks public
configuration/initialization. These test additions supply observations not exposed
by the existing CLI-only echo example; they do not add an application architecture
or a second model, parser, or lifecycle owner. Existing application and prior lab
implementation files remain unchanged, as checked against the entry commit.

All **22/22** public lab registrations ran and passed locally, including the six
new Chapter 6–8 registrations. `phase-5d-final-labs.log` records actual endpoint
identities, exact-byte observations, default/selected Bluetooth fields and cleanup.
The Part III checkpoint is Chapter 8 exercise 4 and uses loopback IPv4 plus a
private Unix path. The separate family lab also executes IPv6. Public README
commands configure/build through the existing CMake/CI discovery path.

Both optional radio drivers compile. The two-host RFCOMM procedure is public but
**not run**; physical radio delivery and pairing remain **not verified**. L2CAP
physical delivery is not claimed. The mandatory selector/local-checkpoint labs
need installed Bluetooth components/development dependencies, but no radio.
IPv6 loopback is required and is not silently skipped. No hosted CI run is claimed.

| Check executed | Result / evidence |
| --- | --- |
| Source hygiene and reference checker/regressions | Pass; `phase-5d-final-hygiene.log` (five reference regression cases) |
| Complete-listing alignment | Pass, 36 exact listings; `phase-5d-final-alignment.log` |
| Metrics regression tests | Pass; `phase-5d-final-metrics-tests.log` |
| Companion build and public exercise targets | Pass; `phase-5d-final-companion.log` |
| All public labs | 22/22 pass; `phase-5d-final-labs.log` |
| Teaching / behavior / lifetime execution | Pass; corresponding `phase-5d-final-*.log` |
| Proposal, sample PDF and full package builds | Pass; `phase-5d-final-package.log` |
| Extracted-package hygiene | Pass; `phase-5d-final-extracted-hygiene.log` |
| Budgets, mappings, scope, artifact preservation | Pass; `phase-5d-final-exit.log`, `phase-5d-exit-checks.json` |

`phase-5d-final-results.json` records zero exits for every executed command group.
The command/environment paths appear in the logs: example build directory
`build/proposal-readiness-phase-5d-examples`, configured install prefix
`build/ci-fix-2026-09-22/install-gcc`, and PDF build directory
`build/proposal-readiness-phase-2`.

Initial failures are retained, not represented as passing evidence:

- `phase-5d-initial-companion.log`: unsupported top-level Bluetooth component names;
  corrected to the supported public legacy-stream components used by the chapter.
- `phase-5d-initial-labs.log`: assumed wildcard text from the default getter;
  corrected the lab and the two reader passages to distinguish the empty configured
  string from an explicit wildcard address.
- `phase-5d-initial-identity-check.log` and
  `phase-5d-initial-rendered-name-attempt.log`: numeric-only display assumptions;
  the final fixture resolves rendered names within the selected family and compares
  actual endpoint tuples. It still asserts both directions of identity.
- `phase-5d-initial-package.log`: an underfull line in a compressed slash-separated
  constructor phrase; normal prose fixed the line without suppressing diagnostics.

### References, PDF evidence and accounting

The current reference register retains all **39 stable topics** and **374 original
migration dispositions**. There are **343 current references**, previously 360.
Twenty redundant framing/self-references are explicitly retired:
`R106 R120 R121 R122 R125 R126 R127 R128 R129 R130 R131 R132 R133 R135 R136 R140 R141 R112 R114 R116`.
Three public solution title references are newly registered. The register diff
records each retirement and its replacement evidence; surviving target identities
remain. The author's combined R275/R276 reference remains intact. The checker
passes after refreshing line evidence, without changing the old→new mapping.

Pages: **full 436 → 418**, samples **54 → 54**, proposal **6 → 6**.
All three final LaTeX logs have **zero warnings and zero bad boxes**. The package
contains 306 files, each byte-identical to its current source/artifact, including
new public labs and answers. `phase-5d-exit-checks.json` records hashes, page counts,
archive identity and diagnostic checks. Targeted visual review covered physical
pages 2–4, 9 and 57–84; see `phase-5d-visual-review.md`. It is not a whole-book
visual recertification. Proposal content/page-table refresh remains Phase 6.

Implementation line accounting: existing application production **+0/−0**;
new test C++ **+53/−0**, test Python **+72/−0**, test CMake **+36/−1**;
phase-specific review checker **+132/−0**. Public README procedures and all
manuscript/report evidence are documentation, counted separately from production
and executable test support. No production-code growth occurred.

Commit: `proposal-readiness: phase 5d — refine Part III and verify endpoint-family labs`.
**Stop after Phase 5d. Phase 5e is not started.** Its entry gate must freshly rerun
metrics and `check-phase-5d.py`, the 22 public labs, hygiene/alignment and regression
checks, companion/runtime checks, PDF/package builds and extracted-package hygiene.
Use fresh entry log/output paths so the evidence above remains historical.


## Author-requested Phase 5d follow-up — 2026-09-22

Edited and reread `manuscript/chapters/06-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:409`:
the stream/datagram introduction, public headers/component and lab orientation now
open the Unix-domain section. The credentials section ends with authorization
policy. The introduction names only context/factory separation and event-loop
execution from Chapters 3–5, and points ahead to Chapter 7 for connection lifetimes.
All index occurrences and original registered target/migration identities remain;
two explicit teaching-path references were added (345 current references).
No other manuscript input changes in this follow-up.

Fresh Phase 5d exit checks pass. `check-phase-5d-follow-up.py` retains all previous
assertions, redirects evidence paths, and permits only the author's relocation in
Chapter 6's excerpt order; an exact expected-text assertion checks that relocation
and the one sentence correction against the Phase 5d commit. All excerpt bytes
remain unchanged. Evidence: `metrics-after-phase-5d-follow-up.json`,
`phase-5d-follow-up-exit-checks.json`, `phase-5d-follow-up-results.json`, and
`phase-5d-follow-up-*.log`. Historical Phase 5d evidence remains unchanged.

Chapter 6: 4,168 → 4,175 words; twelve sections; mean section prose 319.83.
Part III: 9,422 → 9,429 / 11,050; book: 133,986 → 133,993. Reserve remains 2,750.
Hygiene/alignment, metric/reference regressions, companion build, all 22 labs,
teaching/behavior/lifetime checks, PDF/package targets and extracted-package hygiene
pass. Full PDF remains 418 pages, samples 54 and proposal 6; warnings/bad boxes are
zero. Physical pages 64–68 were rendered and inspected: the relocated introduction,
headers, credentials, recap and exercises fit without clipping or overlap.
Local images: `build/phase-5d-follow-up-visual/`. No application/test implementation
changes. Initial logs retain a corrected registered-anchor name and sandbox-denied
socket execution; the required local network tests subsequently passed with socket
access. No physical Bluetooth execution is claimed.

Separate commit: `proposal-readiness: phase 5d follow-up — relocate stranded Unix-socket introduction`.
This freshly passed gate is the authorized Phase 5e entry baseline. The author also
clarifies that budgets are ceilings: remove repetition, preserving explanations,
examples and technical qualifications instead of cutting merely to undershoot.


## Phase 5e — Part IV completed, 2026-09-22

### Entry gate and author scope

First completed and separately committed the author-requested Unix introduction
relocation as `proposal-readiness: phase 5d follow-up — relocate stranded Unix-socket introduction`.
Before Part IV editing, freshly reran its Phase 5d assertions, metrics, all 22
public labs, hygiene/alignment and regressions, companion/runtime checks and
PDF/package targets. All passed: `phase-5d-follow-up-results.json`,
`phase-5d-follow-up-exit-checks.json`, and `phase-5d-follow-up-*.log`.
The authorized baseline is `metrics-after-phase-5d-follow-up.json` (133,993 words;
full PDF 418 pages). Historical Phase 5d evidence remains unchanged.

The author's current instruction makes budgets explicit ceilings. Removed repeated
role/responsibility summaries and arrow blocks, while keeping distinct explanation,
examples and technical qualifications. No further cuts were made merely to use
less than the available budget. The retained-content audit in `chapter-ledger.md`
cites the final locations of parser accounting, length limits, queue admission,
attachment and ownership, dependency lifetimes, carrier qualification and all
worked examples.

Edited and reread: Chapters 9–11, Part IV opener, common solution guide and public
answers in `companion/exercises/ch09/README.md`, `ch10/README.md`, `ch11/README.md`.
The unchanged Part V opener was reread for continuity. `check-phase-5e.py` compares
against the separate follow-up commit: only those four Part IV manuscript inputs
change. Every executable/configuration fence (293), index occurrence, figure marker
and source marker is preserved; each affected chapter's C++ excerpts remain
byte-identical and in order. No application implementation, proposal text, approved
chapter order or production styling changes in Phase 5e.

### Metrics and teaching contract

Evidence: `metrics-after-phase-5e.json`, `phase-5e-exit-checks.json` and the Phase 5e
ledger. Each chapter has three objectives, five exercises in all three tiers,
complete objective↔exercise mappings and public solutions. Recaps have five bullets
in Chapters 9–10 and four in Chapter 11, immediately before exercises.

| Chapter | Words before → after / ceiling | Sections / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| 9 | 4,298 → 3,089 / 3,200 | 8 / 8 | 345.75 |
| 10 | 3,867 → 2,265 / 2,800 | 6 / 7 | 328.33 |
| 11 | 3,626 → 2,555 / 2,800 | 7 / 7 | 312.57 |

Part IV: **11,791 → 7,909 / 8,800 words**, with all teaching apparatus included.
Front matter remains 1,980 / 2,500; all Part/epilogue openers are 1,149 / 1,650.
Reserve used: **0**; remaining: **2,750**. The five earlier samples retain their
required reductions/density, as checked in `phase-5e-exit-checks.json`.

| Whole-book metric | Entry → after | Delta |
| --- | ---: | ---: |
| Total words | 133,993 → 130,160 | −3,833 |
| Prose words | 120,574 → 117,152 | −3,422 |
| Fenced words | 13,419 → 13,008 | −411 (explanatory text only) |
| Chapter headings ≥3 | 753 → 691 | −62 |
| Mean chapter-section prose | 147.99 → 156.38 | +8.39 |
| Text fences | 348 → 323 | −25 |
| C++ fences | 199 → 199 | 0 |
| Objectives / exercise callouts | 11 / 11 → 14 / 14 | +3 each |
| Rule boxes | 20 → 20 | 0 |
| Forbidden phrases / Closing perspective | 0 / 0 → 0 / 0 | 0 |

The Part's reduction is 3,882 words; its opener adds 49, producing the global
−3,833. Global ceilings are not required until the final sub-phase: 15,160 words,
141 headings and 73 text fences remain above them, and mean section prose remains
below 250. Later Parts and the global audit remain pending.

### Implementation, execution and limits

Invariant: one canonical protocol implementation, one independent parser state per
context, and equivalent framing results across the selected byte-stream carriers.
Construction refusal must close before protocol readiness; carrier establishment
failure must remain distinguishable from command rejection. This Part supplies
public observations of those existing behaviors rather than adding another parser.

`companion/exercises/ch09/protocol.py` reuses the common bounded process/configuration
harness and existing line server. It tests framing, length, fresh contexts, refusal,
transfer and endpoint failure via peers. The 24-line `ch10/refusal.cpp` test driver
returns `nullptr` once, then delegates to the canonical factory without deleting
the supplied connection or duplicating protocol behavior. The `ch11` build applies
the three worked entry-point substitutions to the original `main.cpp` and links the
Unix component; it compiles the original context source and uses the original
factory. A configure dependency keeps that generated entry point current.
Existing applications and earlier lab implementations remain unchanged, asserted
by the phase checker. These additions are public test/teaching support, with no
production-code growth or parallel protocol authority.

Six new registrations pass within **28/28** public labs:

- 26 two-piece command segmentations, coalesced input, CRLF/empty/unknown-command
  handling, bounded partial-prefix silence and QUIT closure;
- 4096/4097-byte admission boundary including carriage return, with and without a
  newline, and closure before overlong-command interpretation;
- independent pending input, fresh replacement context and surviving peer progress;
- null factory result closes without READY; subsequent valid creation yields PONG;
- Part IV checkpoint reconstructs identical replies over IPv4 and a private Unix
  path, with server-owned cleanup before fixture-directory cleanup;
- nonexistent path fails before readiness; a valid endpoint can reject a command
  and continue serving the same peer.

Exact commands/output: `phase-5e-final-labs.log`. The lab solutions explain that
application writes do not dictate kernel callback segmentation. They do not claim
all schedules, saturation/deadline execution, physical radio behavior, TLS trust
validation or measurement-model acceptance. The checkpoint teaches input framing;
CSV validation and domain acceptance remain in the later MiniGateway extension.
The labs use the existing CMake/CI discovery path and passed locally; no hosted CI
execution is claimed.

| Required check executed | Result / evidence |
| --- | --- |
| Hygiene and chapter references/regressions | Pass; `phase-5e-final-hygiene.log` |
| Complete-listing alignment | 36 exact listings pass; `phase-5e-final-alignment.log` |
| Metrics regressions | Pass; `phase-5e-final-metrics-tests.log` |
| Companion and public lab builds | Pass; `phase-5e-final-companion.log` |
| Public lab execution | 28/28 pass; `phase-5e-final-labs.log` |
| Teaching, behavior and lifetime checks | Pass; corresponding `phase-5e-final-*.log` |
| Proposal, sample PDF and full package targets | Pass; `phase-5e-final-package.log` |
| Fresh extracted-package hygiene | Pass; `phase-5e-final-extracted-hygiene.log` |
| Budgets, pedagogy, preservation and artifact consistency | Pass; `phase-5e-final-exit.log`, `phase-5e-exit-checks.json` |

`phase-5e-final-results.json` records zero exits for every command group. The example
build is `build/proposal-readiness-phase-5e-examples`, using the configured install
prefix `build/ci-fix-2026-09-22/install-gcc`; PDF target build directory remains
`build/proposal-readiness-phase-2`.

Initial evidence is retained. `phase-5e-part-labs.log` contains a failed assertion
that overlong-line closure must deliver the queued diagnostic. The existing server
calls close immediately, so queueing does not establish delivery. The corrected
peer requires EOF and permits only the diagnostic's prefix (including no bytes),
never an interpreted unknown-command reply. This preserves the stated framing
invariant; no server behavior was changed. The chapter and solution now teach that
qualification explicitly. All six tests then passed in
`phase-5e-part-labs-corrected.log` and the final 28-test run. The final exercise uses
the installed public enum spelling `WouldExceedLimit`. An intermediate artifact
check caught a stale package during that last wording correction
(`phase-5e-initial-exit.log`); rebuilding, re-extracting and rerunning the check
produced the passing final evidence. No PDF diagnostic suppression was needed.

### Reference register, PDF review and accounting

All **39 stable topics** and **374 migration dispositions** remain. Current
references are **333**, previously 345: fifteen duplicate framing references are
explicitly retired and three public solution title references are added. Retired
identities: `R151 R156 R157 R158 R159 R160 R161 R162 R163 R165 R166 R167 R168 R173 R174`.
Surviving targets/identities are retained, including the deliberate combined
R275/R276 reference; moved references are reordered with their existing identities
and line evidence. The reference checker and its five regression tests pass.

Full PDF: **418 → 406 pages**; samples **54 → 54**; proposal **6 → 6**.
All three final LaTeX logs have **zero warnings and zero bad boxes**.
The archive contains **314 files**, byte-identical to current source/artifacts.
Hashes and diagnostic counts are in `phase-5e-exit-checks.json`. Rendered physical
pages 2–4 and 84–107 were inspected; `phase-5e-visual-review.md` records the 27-page
targeted visual review and its limits. All affected objectives, exercises, tables,
listings and the transfer figure fit. Proposal content/page-table refresh remains
Phase 6; later chapters are not visually or editorially recertified here.

Implementation line changes: application production **+0/−0**; new test C++
**+24/−0**, test Python **+135/−0**, test CMake **+36/−1**; review checker
**+132/−0**. Manuscript, public answers and report/log evidence are documentation
accounted separately. Final diff review found no duplicated parser, old/new
application overlap, or unused fixture mode; all six new modes execute in the
public test registrations.

Commit: `proposal-readiness: phase 5e — refine Part IV and verify protocol framing`.
**Stop after Phase 5e. Phase 5f is not started.** Before Phase 5f, freshly rerun
metrics and `check-phase-5e.py`, all 28 labs, hygiene/alignment and regressions,
companion/runtime checks, PDF/package targets and fresh extracted-package hygiene.
Use new evidence paths so this completed phase's evidence remains historical.


## Phase 5f — Part V completed (2026-09-22)

### Entry gate: Phase 5e re-executed before editing

Started from a clean working tree on the refinement branch. Fresh manuscript
metrics exactly matched `metrics-after-phase-5e.json`: 130,160 words. The adapted
`check-phase-5f-entry.py` reruns the previous phase assertions without replacing
its historical results: Part IV budgets and pedagogy, retained samples, scope,
listings, index/figure preservation, references, artifacts and package contents.
See `phase-5f-entry-gate.log` and `phase-5f-entry-exit-checks.json`.

All ten execution groups returned zero in `phase-5f-entry-results.json`, with
separate command-bearing logs: hygiene/reference regression, source alignment,
metrics tests, companion build, all 28 existing public labs, teaching, behavior,
lifetime, publication targets and extracted-package hygiene. The entry build
reproduced 406 full-manuscript, 54 sample and 6 proposal pages, zero final warnings
and bad boxes, and 314 package files matching their current inputs. Thus Phase 5e
was verified from current inputs and execution, not its completed status alone.

### Edited and reread

Refined only current Chapters 12–13 and the Part V opener among ordered manuscript
inputs. Chapter 12 merges the duplicate configuration introductions and catalogues
while retaining the three input paths, scoped help, one echo precedence experiment,
shared endpoint settings, explicit reparse/failure consequences, persistence,
structured discovery and control-tool limits. Chapter 13 tightens framing around
the existing logging API, scope/lifetime, errors, frozen policy and presentation
examples. The Diagnostic responsibility rule remains.

Both chapters now open with three objectives and close with five recap bullets,
then five exercises (two review, two labs, one design). All objectives are assessed;
all exercise mappings and public solutions are listed in the Phase 5f section of
`chapter-ledger.md`. Manuscript evidence: Ch12:3, :615, :623; Ch13:3, :328, :330,
:338, with full paths and a retained-content audit in that ledger.

The full changed chapters, solution READMEs and Part transitions were reread.
The manuscript diff is saved as `phase-5f-manuscript.diff`. This is refinement of
the existing explanations and examples, not replacement chapters. Chapter 12’s
>35% author stop rule was applied by auditing the distinct teaching before and
after, rather than treating the ceiling as a reason to discard qualifications.
No reserve draw is needed: **0 used, 2,750 remaining**.

| Current chapter | Words before → after | Ceiling | Prose before → after | Headings before → after / ceiling | Mean section prose after |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12 — configuration | 8,615 → 4,273 | 5,400 | 8,104 → 4,023 | 73 → 10 / 16 | 391.20 |
| 13 — diagnostics | 3,779 → 2,698 | 2,750 | 3,479 → 2,481 | 20 → 7 / 7 | 340.43 |

Part V totals **6,971 / 8,150** words. Figures, every index occurrence, all
293 book-wide executable/configuration fences, each chapter’s C++ listing sequence
and all 36 marked complete listings are preserved (`check-phase-5f.py`,
`phase-5f-final-alignment.log`, `phase-5f-exit-checks.json`). The 25 removed `text`
fences were repeated diagrams/questions/vocabulary, not executable code. No
production formatting, chapter order or proposal positioning changes were made.

### Built and run

| Check | Fresh evidence | Result |
| --- | --- | --- |
| Hygiene and chapter-reference regression checks | phase-5f-final-hygiene.log; phase-5f-final-closing-hygiene.log | pass; 326 current references, 39 stable topics, all 374 migration identities accounted |
| Complete source-listing alignment | phase-5f-final-alignment.log | pass; 36 exact complete listings |
| Metrics regression tests | phase-5f-final-metrics-tests.log | pass |
| All companion targets, including reused lab executables | phase-5f-final-companion.log | build passes |
| All public exercises | phase-5f-final-labs.log:322–354, :404 | 32/32 pass; four new registrations |
| Teaching observations, behavior and lifetime checks | phase-5f-final-teaching.log; phase-5f-final-behavior.log; phase-5f-final-lifetime.log | pass |
| Full PDF, proposal, samples and package | phase-5f-final-package.log; phase-5f-final-artifact-refresh.log | build passes; final refresh includes the visual-review sentence fix |
| Extracted package hygiene | phase-5f-final-extracted-hygiene.log; phase-5f-final-closing-hygiene.log | pass |
| Phase budgets, pedagogy, mappings, preservation and final artifacts | phase-5f-exit-checks.log; phase-5f-exit-checks.json | pass |

New lab behavior is observed at existing public executable boundaries. Chapter 12
checks 8080/18091/18092 precedence, unchanged persistent file, inspection status 2,
hierarchical help and invalid-port rejection. Chapter 13 checks the four canonical
JSON records and the Part V checkpoint: the CLI-selected loopback listener echoes
under both global and scoped logging policies, while narrow overrides expose the
correct application/component/context/identity records. The invalid-value diagnostic
names `--port`; the invocation and local help locate its scope. It does not print
the full instance/section path, and the solution does not claim otherwise.

No application implementation was added or changed: **production code +0/−0**.
The lab/test support changes are **+144/−25 lines (net +119)** across the two new
Python fixtures, their CMake registrations, common environment extraction and
teaching smoke integration. The JSON contract was moved into its public solution
and reused by the smoke check, preserving all old assertions and adding absence
of invented identity. Environment construction was extracted from the existing
bounded harness so inspection and runtime peers share it. Existing chapter-specific
lab implementations stay unchanged. This support growth implements the requested
observable exercises, not a second echo, parser, logger or runtime.

Verification limits: these runs use the installed dependency and local loopback.
No new hosted CI run, broker, hardware, TLS deployment, runtime reparse, live
listener replacement or control-tool UI execution is claimed. The corresponding
technical qualifications remain in the text; the public READMEs distinguish them
from the startup observations that were run.

### Final artifacts, global deltas, and handoff

Full manuscript **406 → 392** pages; samples **54 → 54**; proposal **6 → 6**.
All three final LaTeX logs contain zero warnings and zero bad boxes. Final hashes
and the **320-file** package/source equality check are in `phase-5f-exit-checks.json`.
Rendered contents and the complete affected Part were visually reviewed; see
`phase-5f-visual-review.md`. A stranded punctuation line in Chapter 13’s boundary
enumeration was removed by rewording its lead-in without changing the enumeration.
No formatting workaround or warning suppression was introduced.

Whole-book metrics (`metrics-after-phase-5f.json` versus `metrics-after-phase-5e.json`):

| Measure | Before | After | Delta / remaining global work |
| --- | ---: | ---: | --- |
| Total words | 130,160 | 124,770 | −5,390; 9,770 above final ceiling |
| Prose words | 117,152 | 112,106 | −5,046 |
| Fenced words | 13,008 | 12,664 | −344 from text diagrams/vocabulary; executable fences unchanged |
| Chapter headings at ### or deeper | 691 | 615 | −76; 65 above final ceiling |
| Mean chapter-section prose | 156.38 | 167.98 | below final global 250; this Part passes individually |
| Text fences | 323 | 298 | −25; 48 above final ceiling |
| Objectives / exercise callouts | 14 / 14 | 16 / 16 | both chapters added |
| Rule boxes | 20 | 20 | cap met |
| Forbidden phrases / Closing perspective | 0 / 0 | 0 / 0 | gates retained |

Front matter stays 1,980 / 2,500 words; all Part openers are 1,182 / 1,650.
The five samples retain their original ≥20% prose reductions and section-density
gates (`phase-5f-exit-checks.json`). Nine redundant Chapter 12 migration occurrences
R177, R179–R182, R184–R185, R187–R188 are explicitly retired with evidence;
surviving references keep their original topic targets and identities. Two new
solution headings are registered against their intended chapter topics. The
approved stable anchors remain in place.

**Stop after Phase 5f.** Next is Phase 5g, Part VI only, after freshly rerunning the
current Phase 5f exit checks. Its runtime and artifact commands are recorded in
the final logs; `check-phase-5f.py` supplies the metrics/preservation assertions.
Preserve historical evidence when recording that new gate. Proposal source refresh
remains Phase 6; the whole-book targets are not yet met or claimed complete.


## Phase 5g — Part VI completed (2026-09-22)

### Entry gate: Phase 5f re-executed before editing

Started from a clean refinement branch. Fresh metrics exactly matched
`metrics-after-phase-5f.json`: 124,770 words. `check-phase-5g-entry.py` reruns the
previous phase assertions with new output paths, preserving historical evidence.
Part V budgets, pedagogy, sample gates, scope, references and listing/index/figure
preservation passed (`phase-5g-entry-gate.log`, `phase-5g-entry-exit-checks.json`).

All ten execution groups passed in `phase-5g-entry-results.json`: hygiene/reference
regressions, source alignment, metrics tests, companion build, all 32 existing
public labs, teaching, behavior, lifetime, publication targets and extracted-package
hygiene. Their command-bearing `phase-5g-entry-*.log` files record execution.
Entry PDFs reproduce 392 full-manuscript, 54 sample and 6 proposal pages, zero
warnings/bad boxes, and 320 package files identical to their inputs. The recorded
status was therefore independently reverified before Part VI editing.

### Edited and reread

The ordered manuscript edits are limited to Chapters 14–15 and the Part VI opener.
The diff consolidates repeated layer descriptions, lifecycle definitions, mirrored
role explanations and summary questions. Trust versus expected identity versus
SNI, early callback timing, bounded TLS shutdown, activation-flow ownership,
retry-count semantics, queue admission, protocol deadlines and uncertain delivery
remain fully explained. Both retained rules state principles the reader applies.
No explanation, example or qualification was removed merely to undershoot a ceiling.
See `phase-5g-manuscript.diff` and the line-cited preservation audit in
`chapter-ledger.md`, Phase 5g.

Both complete chapters and solution READMEs were reread with the Part transitions.
Each chapter opens with three observable objectives and ends with five recap
bullets then five exercises: two reviews, two labs, one design. Every exercise
maps to objectives and every objective is assessed; public answers and commands
exist. Evidence: `manuscript/chapters/14-tls-across-the-framework.md`:3, :244, :252;
`manuscript/chapters/15-timeouts-retries-and-failure-modes.md`:3, :323, :331;
`companion/exercises/ch14/README.md`; `companion/exercises/ch15/README.md`;
the ledger's two mapping tables; `phase-5g-exit-checks.json`.

| Chapter | Words before → after / ceiling | Prose before → after | Headings before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: |
| 14 — TLS | 3,789 → 2,576 / 2,950 | 3,592 → 2,511 | 21 → 8 / 8 | 292.62 |
| 15 — failure and recovery | 4,534 → 2,990 / 3,400 | 4,220 → 2,922 | 37 → 8 / 9 | 339.88 |

Part VI: **5,566 / 6,350** words. Reserve: **0 used, 2,750 remaining**. Neither
approved chapter budget triggers the >35% stop rule; the preservation audit still
checks their distinct teaching. All 293 executable/configuration fences, each
chapter's C++ listing sequence, all index occurrences, figure captions/IDs and
36 marked complete listings remain unchanged (`check-phase-5g.py`, alignment log).
The 25 removed text fences contain repeated diagrams/questions, not executable code.
Chapter order, stable anchors, production formatting and proposal sources are unchanged.

### Built and run

| Check | Evidence | Result |
| --- | --- | --- |
| Hygiene and chapter-reference regressions | phase-5g-final-hygiene.log; phase-5g-final-closing-hygiene.log | pass; 327 current references, 39 stable topics, 374 original dispositions |
| Complete source-listing alignment | phase-5g-final-alignment.log | pass; 36 exact complete listings |
| Metrics regression | phase-5g-final-metrics-tests.log | pass |
| Companion and public lab targets | phase-5g-final-companion.log | build passes through existing CI path |
| Public exercises | phase-5g-final-labs.log | 36/36 pass, including four new registrations |
| Teaching, behavior and lifetime | phase-5g-final-teaching.log; phase-5g-final-behavior.log; phase-5g-final-lifetime.log | pass |
| Full PDF, proposal, sample and package | phase-5g-final-package.log; phase-5g-final-artifact-refresh.log | pass; final refresh includes layout corrections |
| Extracted-package hygiene | phase-5g-final-extracted-hygiene.log | pass on final package |
| Budgets, teaching contract, mappings, preservation and artifacts | phase-5g-exit-checks.log; phase-5g-exit-checks.json | pass |

All ten final execution groups return zero (`phase-5g-final-results.json`).
The Part VI checkpoint first repeats the trust/name fixture's three outcomes,
then observes a controlled peer's initial refusal, first attachment, loss,
failed recovery attempt and second attachment with a distinct connection identity.
The fresh greeting and exact echo establish the restored stream's behavior.
The recovery half uses legacy TCP: it does not claim TLS reconnect or replay of
an earlier application request. A separate TLS echo lab observes binary reflection
and reciprocal close-notify. The public solutions state these boundaries.

New labs reuse canonical EchoPair and the existing TLS policy probe/fixture.
CMake derives the TLS server entry point by the taught include/namespace change,
linking the unchanged context. No application implementation was added or changed:
**production code +0/−0**. Requested lab/test support is **+171/−1 lines, net +170**
(two Python fixtures and CMake registrations). This supplies independent peers and
observations, not another echo algorithm, TLS policy or recovery state machine.
Public README answers are documentation and counted separately.

The initial secure-echo fixture used incorrect certificate option names; installed
local help supplied `--cert` and `--cert-key`. `phase-5g-lab-development-run.log`
retains the failure; `phase-5g-lab-corrected-run.log` and final labs pass. The first
full suite's native deferred-work lab needed an explicit runtime search path to
the selected installation (`phase-5g-initial-full-labs.log`). The final command
records that path and all 36 pass; no existing lab or application was changed.
Use the same runtime environment when rerunning this phase's gate.

Verification limits: local installed dependency and loopback only; no hosted CI
run, production PKI, authorization deployment, TLS reconnect, stalled TLS peer or
complete concurrent shutdown matrix is claimed. The protocol-deadline and replay
policies are explained and discussed, not implemented by these labs. Temporary
certificate/key generation, process/socket bounds and dependencies are documented
in the public solutions.

### Artifacts, global deltas and handoff

Full manuscript **392 → 382** pages; sample package **54 → 54**; proposal **6 → 6**.
All three final LaTeX logs contain zero warnings and zero bad boxes. Final hashes
and **326-file** package/source equality are recorded in `phase-5g-exit-checks.json`.
Nineteen rendered pages were inspected: contents, complete affected Part and the
following Part opener. The corrected recap and failure-visibility sentence were
rendered and rechecked; see `phase-5g-visual-review.md`. No warning suppression or
formatting workaround was added.

| Measure | Phase 5f | Phase 5g | Delta / remaining global work |
| --- | ---: | ---: | --- |
| Total words | 124,770 | 122,049 | −2,721; 7,049 above final ceiling |
| Prose words | 112,106 | 109,763 | −2,343 |
| Fenced words | 12,664 | 12,286 | −378 from text blocks; executable fences unchanged |
| Chapter headings at ### or deeper | 615 | 573 | −42; 23 above final ceiling |
| Mean chapter-section prose | 167.98 | 176.09 | final global 250 still pending; both Part VI chapters pass |
| Text fences | 298 | 273 | −25; 23 above final ceiling |
| Objective / exercise callouts | 16 / 16 | 18 / 18 | both chapters added |
| Rule boxes | 20 | 20 | cap met |
| Forbidden phrases / Closing perspective | 0 / 0 | 0 / 0 | gates retained |

Metrics: `metrics-after-phase-5g.json` against `metrics-after-phase-5f.json`.
Front matter stays 1,980 / 2,500; all Part openers are 1,218 / 1,650. The original
five samples retain their ≥20% prose reductions and section-density gates.
R204, a redundant Chapter 15 self-reference, is explicitly retired with evidence
in `phase-5a-reference-register.json`; the timing explanation remains. Other topic
targets and migration identities survive. Both new solution headings are registered.

**Stop after Phase 5g.** Next is Phase 5h, Part VII only, after freshly rerunning
this phase's metrics and listed exit checks. `check-phase-5g.py` supplies the
preservation/teaching/artifact assertions; final logs record execution commands
and the required runtime environment. Preserve historical evidence. Proposal
source refresh remains Phase 6, and the whole-book targets remain unfinished.


## Phase 5g author follow-up — companion TLS fixture (2026-09-22)

The author requires the reader-facing trust/identity fixture to live in companion
material and authorizes changing the printed lab commands. Moved `tls-runtime.cpp`
and `run-tls.py` byte-for-byte from the current refinement probes to
`companion/exercises/ch14/`. Its existing CMake registration (included by
`companion/exercises/CMakeLists.txt`) now compiles that local source; `tls.py`
uses the local fixture. The existing review CMake target points to the same
companion files, so there is one implementation. Historical evidence is unchanged.

Edited and reread Chapter 14's fixture paragraph and commands at
`manuscript/chapters/14-tls-across-the-framework.md`:151 and the public solution at
`companion/exercises/ch14/README.md`:33. The book-meta sentence is replaced by a
direct companion reference, with ordinary root-project lab configuration,
`ch14-lab`, and `exercise-ch14-trust-identity`. Three identity outcomes and the early
null-SSL observation remain unchanged. Reference positions were refreshed without
changing intended targets or migration identities.

All ten required execution groups pass (`phase-5g-follow-up-results.json` and
command-bearing `phase-5g-follow-up-*.log`): 36/36 public labs, companion build,
hygiene/reference regression, alignment, metrics tests, teaching/behavior/lifetime,
PDF/proposal/sample/package and extracted-package checks. The existing review
consumer also builds and runs the relocated fixture (`phase-5g-follow-up-review-consumer.log`).
`check-phase-5g-follow-up.py` reruns the Phase 5g budget, teaching, preservation and
artifact assertions, allowing precisely the author-requested shell-block change
and checking byte-identical fixture relocation. Its output is
`phase-5g-follow-up-exit-checks.json` and `.log`.

Metrics: Chapter 14 **2,576 → 2,579 / 2,950**, mean section prose **292.25**;
Part VI **5,569 / 6,350**; whole book **122,049 → 122,052**. The +3 tokens are the
net effect of the direct reference and runnable commands. Other chapter metrics,
headings, index entries, figures, all C++ listings and source markers are unchanged.
No reserve used; 2,750 remains. `metrics-after-phase-5g-follow-up.json` is the
**authorized Phase 5h entry baseline**; original Phase 5g metrics remain historical.

PDFs remain **382 / 54 / 6 pages**, zero final warnings and bad boxes; 326 package
files match their inputs. Physical page 132 was rendered and inspected in
`build/phase-5g-follow-up-visual/page-132.png`: command lines, policy sketch and
surrounding explanation fit without clipping. The moved test implementation adds
no production or test logic; excluding exact file moves, CMake/Python wiring is
+5/−5 lines. No broader TLS deployment validation is claimed.

Separate commit: `proposal-readiness: phase 5g follow-up — move TLS fixture into companion material`.
The freshly passed follow-up gate permits Phase 5h to begin in this session.


## Phase 5h — Part VII completed (2026-09-22)

### Entry gate, scope and editorial result

The separate author-requested TLS-fixture follow-up was completed and committed
before Part VII editing. Its freshly rerun Phase 5g checks, 36 public labs, review
consumer and clean artifacts are recorded in `phase-5g-follow-up-results.json`,
`phase-5g-follow-up-exit-checks.json` and command-bearing follow-up logs. The
entry metrics are `metrics-after-phase-5g-follow-up.json`; original Phase 5g
records remain historical. This satisfies the previous-phase entry gate.

Applied only the approved Part VII scope, Chapters 16–19, plus its opener/checkpoint
and public solutions. Budgets are ceilings, not targets. Edited and reread Chapters
16, 17 and 19 in context; reread Chapter 18 and retained it byte-for-byte because
it already meets the gates. The prose revision consolidates repeated stack,
context/factory and upgrade explanations and removes arrow-chain restatement.
The content-preservation audit in chapter-ledger.md cites retained explanations,
examples and qualifications by source line; `phase-5h-manuscript.diff` records the
actual changes. No structure, chapter order or production styling was changed.

| Chapter | Words before → after / ceiling | Prose before → after | Fenced words before → after | Deep headings before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: |
| 16 | 3,514 → 2,471 / 2,600 | 3,124 → 2,305 | 390 → 166 | 24 → 6 / 6 | 368.17 |
| 17 | 3,059 → 2,065 / 2,350 | 2,806 → 1,999 | 253 → 66 | 26 → 5 / 5 | 382.80 |
| 18 | 3,269 → 3,269 / 3,300 | 2,898 → 2,898 | 371 → 371 | 7 → 7 / 7 | 398.00 |
| 19 | 3,983 → 3,000 / 3,050 | 3,432 → 2,638 | 551 → 362 | 23 → 7 / 7 | 363.14 |

Part VII: **13,825 → 10,805 / 11,300**. No reserve draw; **2,750 remains**.
All four chapters meet their word/headings ceilings and ≥250 mean section prose.
Each has three observable objectives, five recap bullets, two review questions,
two labs and one design problem. All objective↔exercise mappings and public answers
are recorded in chapter-ledger.md and `companion/exercises/ch16`, `ch17`, `ch18`,
`ch19`. The checker compares the exercise IDs directly with the solution headings.

The Part checkpoint follows two accepted measurements through POST results and
independent SSE streams, then verifies WebSocket negotiation/message behavior
separately (`manuscript/chapters/19-websocket-and-protocol-upgrade.md:393`;
`companion/exercises/ch19/README.md:44`). It uses existing accepted-state and
observer ownership, preparing the capstone without adding another state store.
The SSE program has no `/status` route; POST results and events are the actual
observable boundary.

### Execution evidence and architecture accounting

All ten required execution groups pass in `phase-5h-final-results.json`:

| Group | Execution evidence |
| --- | --- |
| Hygiene, reference/topic check and regression | `phase-5h-final-hygiene.log` |
| Marked complete-listing alignment | `phase-5h-final-alignment.log` |
| Measurement regression | `phase-5h-final-metrics-tests.log` |
| Installed-package companion and exercise compilation | `phase-5h-final-companion.log` |
| 42/42 public labs, including six new tests | `phase-5h-final-labs.log` |
| Existing teaching smoke checks | `phase-5h-final-teaching.log` |
| Existing behavior smoke checks | `phase-5h-final-behavior.log` |
| SSE lifetime and dynamic WebSocket checks | `phase-5h-final-lifetime.log` |
| Full manuscript, proposal, samples and package | `phase-5h-final-package.log` |
| Final extracted source-package hygiene | `phase-5h-final-extracted-hygiene.log` |

`check-phase-5h.py` independently reruns metrics, chapter budgets, pedagogy and
solution mappings, retained sample gates, references, scope, listing/index/figure
preservation, LaTeX warning checks and package equality. Output is
`phase-5h-exit-checks.json` and `.log`. All 293 executable/configuration fences,
all C++ excerpt order, source markers, index occurrences and figure IDs survive.
The original application and earlier lab implementations remain unchanged.

The governing invariant is one owner for parsing/routing/echo behavior and one
implementation of each reused test observation. Public HTTP/Express labs share a
37-line synchronous route fixture and one independent peer script. WebSocket labs
reuse canonical subprotocol sources and derive linked entry points. Existing wire
assertions move intact into `companion/exercises/ch19/wire.py`, imported by the
CI lifetime test; syntax-tree comparisons verify that every earlier wire assertion
and the SSE lifetime-test function remains. No production fix or growth is needed:
**production +0/−0; requested test support +278/−68, net +210 lines**. New README
solutions and review checkers are accounted as documentation/review support.

The six new tests observe incomplete-header quietness then completion; valid HTTP
versus malformed/over-limit rejection before application entry; mounted-route
order and unmounted 404; middleware 403 without continuation; selected echo versus
unsupported subprotocol; and the SSE/WebSocket checkpoint. The actual malformed
and over-limit statuses are 405/431, and unsupported subprotocol returns 404 in
this run. Assertions require the relevant boundary behavior, not universal status
codes for all possible invalid input. The unchanged client also receives hello
and closes; independent peers test counted binary payloads and fragmentation.

Initial failures and their corrections are retained:

- `phase-5h-lab-development-build.log`: missing imported WebSocket targets;
  explicit component discovery in the lab CMake fixes configuration. Corrected
  compilation is in `phase-5h-lab-corrected-build.log` and final companion output.
- `phase-5h-initial-lifetime.log`: extracting WebSocket helpers also removed the
  `struct` import still needed by SSE reset checks. Restored the import; final
  lifetime output passes all existing cases, with no assertion removed.
- `phase-5h-missing-prefix-labs.log`: a later test invocation omitted the documented
  `SNODEC_PREFIX` for two existing environment labs. The final invocation records
  that prefix and its runtime search path and passes 42/42. No lab was weakened.

These are local installed-package builds and loopback observations, not a hosted
CI run or deployment certification. Full parser-policy matrices, descriptor
streaming errors, invalid WebSocket frames, receiver-limit failures and deployment
TLS were not newly run. Explanations and qualifications remain in their sections.

### Artifacts, metrics and handoff

Full manuscript **382 → 368 pages**; samples **54 → 54**; proposal **6 → 6**.
Final LaTeX warnings and bad boxes: **zero** for all three. PDF hashes and
**336-file** package/source equality appear in `phase-5h-exit-checks.json`.
Targeted visual review covered physical pages 142–174 and contents page 5, with
Chapter 19 re-rendered after the final table-continuation correction. All listings,
tables, figure/caption and callouts fit. Details and initial layout corrections
are recorded in `phase-5h-visual-review.md`. No production-formatting changes or
warning suppression were introduced.

| Global measure | Entry baseline | Phase 5h | Delta / remaining |
| --- | ---: | ---: | --- |
| Total words | 122,052 | 119,068 | −2,984; 4,068 above final hard ceiling |
| Prose words | 109,760 | 107,376 | −2,384 |
| Fenced words | 12,292 | 11,692 | −600 from text blocks; executable fences unchanged |
| Chapter deep headings | 573 | 518 | −55; final numerical ceiling met |
| Mean chapter-section prose | 176.08 | 190.53 | global 250 gate remains pending |
| Text fences | 273 | 229 | −44; final numerical ceiling met |
| Objective / exercise callouts | 18 / 18 | 21 / 21 | three chapters added |
| Rule boxes | 20 | 20 | cap retained |
| Forbidden phrases / Closing perspective | 0 / 0 | 0 / 0 | gates retained |

Metrics are saved as `metrics-after-phase-5h.json`. Front matter stays 1,980 / 2,500;
all Part openers are 1,254 / 1,650. The original five samples retain their ≥20%
prose reductions and density criteria (`phase-5h-exit-checks.json`). The reference
checker covers **319 current occurrences**, 39 stable topics and all 374 original
migration dispositions. Redundant occurrences R210, R217, R218, R222–R224,
R226–R228, R244 and R246 are explicitly retired with evidence in the register;
remaining topic targets/identities are retained and three new solution headings
registered. This is reference retirement with prose condensation, not renumbering.

Commit: `proposal-readiness: phase 5h — refine Part VII and verify web protocol boundaries`.
**Stop after Phase 5h.** Phase 5i (Part VIII) has not started. Before it starts,
rerun this gate using the final logs' selected installation and runtime environment.
The remaining Part sessions, final global audit and Phase 6 proposal-source refresh
remain pending; passing the heading/text-fence counts alone does not complete them.


## Phase 5i — Part VIII completed, 2026-09-22

### Entry gate and editorial scope

Before editing, freshly reran all Phase 5h exit checks. Metrics exactly reproduced
`metrics-after-phase-5h.json`; all ten execution groups passed, including all 42
existing public labs and fresh PDF/package builds. `phase-5i-entry-results.json`,
`phase-5i-entry-*.log` and `phase-5i-entry-exit-checks.json` record the run. The
unchanged Phase 5h checker logic was rerun with entry-log/output paths redirected;
historical Phase 5h evidence remains intact. Entry PDFs: **368/54/6 pages**
(manuscript/samples/proposal), zero warnings and bad boxes.

Used the same selected installation and runtime setup as that gate:
`SNODEC_PREFIX=build/ci-fix-2026-09-22/install-gcc` (absolute path in the process),
`BOOK_EXAMPLES_BUILD_DIR=build/proposal-readiness-phase-5i-examples`, parallelism 4,
and all selected prefix shared-library directories in `LD_LIBRARY_PATH` (recorded
in each final execution log). PDF targets use `build/proposal-readiness-phase-2`.

Edited and reread Chapters 20–22, their solutions and the Part VIII opener. Budgets
were ceilings: removed repeated layer diagrams, duplicate comparisons, restated
framing and summaries. Kept the full client excerpt, MQTT packet/acknowledgement
vocabulary, carrier and session lifetimes, adapter buffer/scheduling mechanics,
all component snippets, costs, scientific examples and partial-failure contracts.
The ledger supplies a source-line preservation audit; `phase-5i-manuscript.diff`
records the edits. No structural change or production formatting change occurred.

| Chapter | Words before → after / ceiling | Prose before → after | Fenced words before → after | Deep headings before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20 | 2,997 → 2,005 / 2,350 | 2,709 → 1,878 | 288 → 127 | 22 → 5 / 5 | 359.60 |
| 21 | 2,731 → 1,782 / 2,100 | 2,353 → 1,716 | 378 → 66 | 17 → 4 / 4 | 409.25 |
| 22 | 3,964 → 2,922 / 2,950 | 3,780 → 2,899 | 184 → 23 | 24 → 8 / 8 | 348.50 |

Part VIII: **6,709 / 7,400**, from 9,692 words. Reserve used **0**; **2,750 remains**.
Each chapter has three objectives, five recap bullets and five exercises: two
review, two labs and one design. The ledger records both directions of the mapping;
`check-phase-5i.py` verifies coverage and matching public solution headings.

The Part checkpoint is at
`manuscript/chapters/22-designing-iot-systems-with-multiple-protocols.md:269` and
`companion/exercises/ch22/README.md:39`. It separately observes broker/subscriber
delivery and MiniGateway acceptance with unavailable MQTT. It does not pretend
that the gateway was attached to that first broker or that a live disconnect was
tested. The expected boundary map distinguishes session, subscription, delivery,
accepted state and observation (`companion/exercises/ch22/README.md:56`).

### Execution evidence and architecture accounting

All ten groups in `phase-5i-final-results.json` pass:

| Group | Evidence |
| --- | --- |
| Hygiene, chapter/topic references and reference regression | `phase-5i-final-hygiene.log` |
| Complete-listing alignment | `phase-5i-final-alignment.log` |
| Measurement regression | `phase-5i-final-metrics-tests.log` |
| Installed-package companion and lab compilation | `phase-5i-final-companion.log` |
| 48/48 public labs, including six new registrations | `phase-5i-final-labs.log` |
| Teaching smoke checks | `phase-5i-final-teaching.log` |
| Behavior smoke checks | `phase-5i-final-behavior.log` |
| Existing SSE/WebSocket lifetime checks | `phase-5i-final-lifetime.log` |
| Full manuscript, proposal, sample PDF and package | `phase-5i-final-package.log` |
| Extracted source-package hygiene | `phase-5i-final-extracted-hygiene.log` |

`check-phase-5i.py` independently checks budgets, pedagogy, references, scope,
retained sample gates, all 293 executable/configuration fences, C++ block order,
source markers, index entries and figure IDs. Existing companion applications,
earlier lab implementations and CI lifetime tests are unchanged. Results are
`phase-5i-exit-checks.json` and `.log`.

The governing invariant is that installed MQTT roles/adapters own protocol behavior
and the existing model owns gateway acceptance. The native client/broker launchers
and WebSocket factory attach those existing owners; bounded peers observe their
public behavior. A broker fixture is needed for subscriber delivery evidence,
which a controlled packet peer alone cannot provide. The author-requested public
lab support adds no replacement broker, adapter, parser or model implementation.
**Production +0/−0; requested fixture/test support +300/−2, net +298 lines**,
including CMake registration. README answers and review checkers are separate
from production/test logic.

The new WebSocket consumer exposed duplicate configure dependency paths for the
same canonical client main. Moved registration from the Chapter 19 directory to
one normalized root registration shared by both consumers
(`companion/exercises/CMakeLists.txt:2`). This fixes the dependency owner instead
of copying a second canonical main. Existing Chapter 19 tests still pass.

New runtime observations: CONNECT and bounded quietness before CONNACK; canonical
SUBSCRIBE/PUBLISH and command callback; real installed-broker SUBACK plus exact
independent subscriber delivery; WebSocket upgrade/mqtt selection, binary CONNECT,
fragmented binary CONNACK and command; text-opcode error with close 1002; and the
accepted-state/outage checkpoint. The equipped broker lab uses a disposable local
installed server fixture. Fixed canonical topics and client ID are isolated by a
fresh private broker/port and temporary session directory, not falsely described
as a unique topic prefix. Public solutions state each fixture's scope and cleanup.

Initial failures remain recorded:

- `phase-5i-lab-development-build.log`: Ninja duplicate configure dependency;
  corrected by the single normalized registration described above.
- `phase-5i-lab-corrected-build.log`: C++ factory-selector deduction rejected a
  lambda object; unary `+` supplies the required function pointer. Corrected full
  compilation is in `phase-5i-lab-final-build.log` and the final companion log.
- `phase-5i-lab-development-run.log`: the WebSocket test peer assumed a space after
  every HTTP header colon. Parsing now splits at the colon and strips optional
  whitespace. Both adapter tests pass in `phase-5i-adapter-corrected-run.log`, then
  all 48 pass together in the final run. No behavior assertion was removed.

Local installed-package builds and loopback execution are verified. Hosted CI,
third-party broker interoperability, deployment TLS, durability, QoS 1/2 recovery,
full malformed-packet/overload matrices and live gateway reconnection are **not
newly verified**. The chapters retain the associated technical qualifications.

### Artifacts, metrics and handoff

Full manuscript **368 → 358 pages**; samples **54 → 54**; proposal **6 → 6**.
All three have **zero final LaTeX warnings and bad boxes**. PDF hashes and
**347-file** package/source equality are in `phase-5i-exit-checks.json`. Physical
pages 174–193 (complete Part VIII and next Part transition) and contents pages
5–6 were rendered and visually reviewed; details are in `phase-5i-visual-review.md`.
All figures, listings, tables and callouts fit; no formatting changes or warning
suppression were needed. Proposal source refresh remains the authorized Phase 6 task.

| Global measure | Entry baseline | Phase 5i | Delta / remaining |
| --- | ---: | ---: | --- |
| Total words | 119,068 | 116,122 | −2,946; 1,122 above final hard ceiling |
| Prose words | 107,376 | 105,064 | −2,312 |
| Fenced words | 11,692 | 11,058 | −634 from text blocks; executable fences unchanged |
| Chapter deep headings | 518 | 472 | −46; numerical ceiling retained |
| Mean chapter-section prose | 190.53 | 204.45 | final global 250 gate remains pending |
| Text fences | 229 | 192 | −37; numerical ceiling retained |
| Objective / exercise callouts | 21 / 21 | 24 / 24 | all three chapters added |
| Rule boxes | 20 | 20 | cap retained |
| Forbidden phrases / Closing perspective | 0 / 0 | 0 / 0 | gates retained |

Metrics: `metrics-after-phase-5i.json`. Front matter remains **1,980 / 2,500**;
Part openers **1,291 / 1,650**. The original five samples retain their ≥20% prose
reduction and density gates. References: **309 current occurrences**, 39 topics,
all 374 original migration dispositions. Redundant references R248, R250, R251,
R253, R254, R256–R259, R262, R265, R266, R269 and R271 are explicitly retired with
reasons in `phase-5a-reference-register.json`; remaining targets/identities are
preserved, three solution headings and one checkpoint reference registered.
The single author seam reference still carries both R275/R276 identities and both
topic targets. This is retirement of repeated prose references, not renumbering.

Commit: `proposal-readiness: phase 5i — refine Part VIII and verify MQTT delivery boundaries`.

**Stop after Phase 5i.** Phase 5j (Part IX) has not started. Before it starts,
rerun this exit gate with the recorded installation/runtime environment. Remaining
Part sessions, the final global audit and Phase 6 proposal refresh remain pending.
