# Proposal readiness — phase report

Session date: 2026-09-22. Work branch: `SNode.C-2.0-refinement`, created directly
from `SNode.C-2.0` with a clean working tree. The phase records below are chronological; the latest completed phase is Phase 2.
The author request is preserved in [PROMPT.md](PROMPT.md). Its initial block was
subsequently unescaped in a separate Phase 0 commit; the teaching-book amendment
was subsequently unescaped by deliberate author work; its teaching requirements govern Phase 2.

| Phase | Status | Commit | Date | Evidence |
| --- | --- | --- | --- | --- |
| 0 — scope and measurement | completed | Separate scope revision; Phase 0 completion commit containing this report (subjects below) | 2026-09-22 | AGENTS.md:18; EDITORIAL-WORK-PLAN.md:32; PROMPT.md; metrics-before.json; metrics-after-phase-0.json; measurement-checks.log; metrics-tests.log |
| 1 — book-wide hygiene | completed | `proposal-readiness: phase 1 — refine manuscript hygiene and preserve teaching principles` (containing this report); separate author-amendment commit | 2026-09-22 | Phase 1 evidence below; metrics-after-phase-1.json; phase-1-source-hygiene.log; phase-1-source-alignment.log; phase-1-companion-build.log; phase-1-pdf-final.log |
| 2 — five sample chapters | completed | `proposal-readiness: phase 2 — refine teaching samples and publish exercise solutions` (containing this report) | 2026-09-22 | chapter-ledger.md; metrics-after-phase-2.json; phase-2-exit-checks.json; phase-2-labs.log; phase-2-pdf-final.log; phase-2-visual-review.md |
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

## Phase 2 — five teaching samples

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
