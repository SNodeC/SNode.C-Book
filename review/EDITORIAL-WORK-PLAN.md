# Agreed manuscript refinement work plan

Established: 21 September 2026.
Status: the authorized four-item follow-up pass is complete. Checkpoint `884dbfe`
records the preceding combined refinement. SSE lifetime, WebSocket echo,
Bluetooth preparation in principle, and closure evidence are complete below.
OpenWrt and publication completion remain deferred. Broader runtime validation
is intentionally omitted by the author's decision; the book is not declared finished.
The subsequent authorized PDF box-fix pass is complete: all 25 audited warnings
are resolved in the ordinary 490-page build, with every word and code listing
preserved. See `review/pdf-box-fixes-2026-09-21/REPORT.md` for verification.
The subsequent font and caption cleanup is also complete: the approved companion
bold/bold-oblique mapping is applied to the book's Latin Modern Mono selection,
and the unused table-caption spacing option is removed. The verified build still
has 490 pages and zero bad boxes, with no font-shape or unused-table-caption
warnings. See `review/pdf-font-fix-2026-09-22/REPORT.md`. Checkpoint `cb7fce2`
records these refinements. The subsequently authorized package-order fix is also
complete: the ordinary rebuild has zero LaTeX warnings and zero bad boxes, with
all 490 pages unchanged. See `review/pdf-package-order-2026-09-22/REPORT.md`.
The author's subsequent epilogue-title refinement uses the numbered part pages'
centered label size, title size, and vertical separation. This changes only the
epilogue opening page; see `review/pdf-epilogue-title-2026-09-22/REPORT.md`.
The following chapter is now titled "The Principles Behind the Programs", as
selected by the author; see `review/pdf-epilogue-chapter-2026-09-22/REPORT.md`.
Publication completion remains deferred.

This plan records the author's accepted remaining work. It persists across
conversations through the repository's `AGENTS.md`. It is self-contained; the
previous publisher review and technical-refinement report provide additional
context when available.

## Author scope revision — proposal readiness, 2026-09-22

The author explicitly authorized the proposal-readiness pass recorded verbatim in
`review/proposal-readiness-2026-09-22/PROMPT.md`. This revision supersedes conflicting
AGENTS.md instructions, governing constraints 1–2 below, earlier no-shortening
acceptance criteria, and previous completion statements for this new pass.
Historical progress records below remain historical.

A shortening target now applies: total whitespace tokens at most 115,000 (stretch
105,000). Remove redundant prose, duplicate summaries, and restated framing;
do not cut code listings to reach the target. Preserve the author's voice,
teaching approach, technical depth of explanations and code, cumulative
progression, and MiniGateway capstone. Chapter consolidation is permitted only
after explicit author approval of RESTRUCTURE-PLAN.md at the Phase 4 gate.

Execute exactly one phase per session on SNode.C-2.0-refinement. The full prompt
sets the measurable targets, scope exclusions, paths, ordered phases, checks,
and exit criteria. Later sessions must read it, consult REPORT.md, and rerun the
previous phase's exit checks before starting. Missing criteria require stopping;
record qualified or blocked work accurately. Phase 4 ends awaiting author approval;
Phase 5a and each subsequent Part condensation run in separate sessions. Never
squash away the separate scope-revision commit.

Phase 0 completed on 22 September 2026. The separate scope-revision commit
precedes measurement. The new metrics tool measures all 62 ordered inputs:
151,924 whitespace tokens (two above the supplied baseline), 1,020 chapter
subheadings, 15 closing sections, 38 remember boxes, 30 rule boxes, 478 text
fences, 205 cpp fences, and zero exercise callouts. Before/after measurements
are identical; manuscript content is unchanged. Five counter regression tests
and independent counts pass. The existing PDF has 490 pages; it was not rebuilt
in Phase 0. Evidence, exact definitions, exit-check commands, and the phase status
table are in `review/proposal-readiness-2026-09-22/REPORT.md`.

Phase 1 completed on 22 September 2026 after freshly rechecking Phase 0.
The teaching-book amendment below is recorded in its own commit. This phase
applies only its rule-box criterion: eight applicable principles were restored,
leaving 20 rule boxes; every restoration is listed in REPORT.md. There are zero
forbidden phrases and closing sections, and shell fences use `sh`. Useful closing
exercises remain in their chapters; repeated verification claims are consolidated
in Conventions. No chapter consolidation or later-phase pedagogical work occurred.

The manuscript has 150,566 words (−1,358), 1,005 chapter subheadings (−15), and
465 text fences (−13). Hygiene, source alignment, guard regression, and companion
compilation pass. The final PDF has 482 pages (Phase 0 baseline: 490), zero LaTeX
warnings and bad boxes; 16 representative rendered pages were inspected. Complete
listing contents, figures, index entries, and input order are preserved. Exact
checks and limits are in `review/proposal-readiness-2026-09-22/REPORT.md`, Phase 1.

Phase 2 completed on 22 September 2026 after re-executing the Phase 1 exits.
The author's restored epilogue is preserved; its +39 prose words are the expected
entry difference, recorded in REPORT.md. Chapters 1, 3, 23, 35, and 37 now each
have three observable objectives, a recap of at most five bullets, and review,
lab, and design exercises with public solutions. Prose reductions are 22–32%
including the new teaching material; average section lengths all exceed 250.
`chapter-ledger.md` records every objective↔exercise mapping and the contextual
reread. Chapter 35 retains every listing unchanged.

The Asio comparison and all lab dependencies compile; five public labs pass.
Hygiene, source alignment, and metrics regression pass. The full PDF has 470
pages (entry 482), zero LaTeX warnings, and zero bad boxes. Visual evidence and
all command results are in the Phase 2 section of REPORT.md. The manuscript has
146,525 words and 921 chapter subheadings; global condensation remains future work.
The five sample chapters are the only manuscript files changed in this phase.

Stop after Phase 2. Phase 3 is next; rerun the Phase 2 checks listed in REPORT.md
before starting. Proposal positioning and learning-path work remain Phase 3;
no restructuring approval is recorded.

## Phase 2 follow-up — author scope and completion, 2026-09-22

The author requested strengthening within Phase 2, explicitly excluding Phase 3:
retain Chapter 1's table and add approximately 15-line paired source excerpts;
connect its layered-architecture argument; make O2 achievable in Chapter 1 while
labeling its lab after Chapter 2; give all five samples 5–6 exercises comprising
two review questions, two labs, and one or two design problems, with objective
mappings and public solutions; add Chapter 35's source build order. This follow-up
supersedes the initial three-exercise sample sets, without starting another phase.

Completed: each sample now has five exercises and 25 mappings are recorded in
`chapter-ledger.md`. Chapter 1's 12/16-line excerpts are checked against companion
functions; its O2 is a reading-time trace, and both labs follow Chapter 2. Chapter
35 has a four-step build order and retains all listings. Ten local labs build and
pass using canonical companion programs/model/codec; hosted CI was not executed.
Hygiene, alignment, guard fixtures, metrics tests, and updated editorial exits pass.
Prose reductions remain 20.93–26.46%, with average sections 291–398 words.
Current whole-book words: 146,950; PDF: 470 pages, zero warnings/bad boxes.
The 49-page rendered review and all evidence are in REPORT.md's Phase 2 follow-up
section. Earlier Phase 2 figures above remain historical to its initial commit.

Commit: `proposal-readiness: phase 2 follow-up — sample chapter strengthening`.
Stop after this commit. Phase 3 remains unstarted; future sessions must recheck
these current Phase 2 exits before proceeding.

## Phase 3 — teaching-book proposal package, 2026-09-22

Completed after fresh Phase 2 metrics, editorial exits, source checks, companion
builds, all ten labs, and the full PDF build passed. The author supplied no new
biographical facts and explicitly requested **“Continue with [AUTHOR TO SUPPLY]”**;
missing credentials, audience/adoption evidence, statistics, endorsements, and
delivery date remain visibly marked. Documented public project facts are kept
separate from independent market evidence.

The proposal now has a one-paragraph pitch, one independent learner as its primary
reader, a secondary course-use sentence with the framework's Hagenberg teaching
origin, one cumulative learning path and one optional shortcut, five publisher-
verified comparable titles, the actual 38-chapter TOC with measured Part extents,
and a measurable completed-versus-remaining revision plan. The evidence sheet
and five-chapter guide were rewritten and reread to match.

All three required targets build. Proposal/evidence: 6 pages; combined samples:
54 pages; full manuscript: 470 pages. Final logs and build console have zero
LaTeX warnings and bad boxes. Proposal font/caption settings reuse the book's
existing configuration; sample openings and callouts were visually reviewed.
The archive now includes the complete companion tree, including public exercises.
A fresh extraction built all companion targets and passed all ten labs; final
archive sources are byte-identical to that tested extraction.

Manuscript metrics are unchanged at 146,950 total words and 921 chapter
subheadings. No manuscript edits or chapter restructuring occurred. Evidence,
bibliographic source links, PDF counts, archive checks, and the next entry checks
are in `review/proposal-readiness-2026-09-22/REPORT.md`, Phase 3;
`metrics-after-phase-3.json` records the unchanged manuscript.

Commit: `proposal-readiness: phase 3 — prepare teaching-book proposal package`.
Stop after this commit. Phase 4 is next, limited to RESTRUCTURE-PLAN.md and ending
awaiting author approval. It must evaluate early MiniGateway milestones and
runnable Part checkpoints; no restructuring approval is recorded.

## Phase 4 — restructure plan awaiting author approval, 2026-09-22

Phase 3's entry checks were re-executed successfully: unchanged metrics, sample
exits, hygiene/alignment, companion compilation, all ten labs, and all proposal
package targets. Socket-based labs initially met a sandbox restriction; the same
tests passed with local socket access. The PDFs remain 6, 54, and 470 pages with
zero warnings/bad boxes. Primary publisher records and the teaching path were
rechecked; evidence is in REPORT.md's Phase 4 section.

The concrete proposal is `review/proposal-readiness-2026-09-22/RESTRUCTURE-PLAN.md`:
30 numbered chapters in 11 Parts, a contributor Appendix A, the preserved epilogue,
and a 112,250-word total budget including all supporting and pedagogical material.
All five candidate merges are evaluated; the minimum source-reading introduction
stays on the main learning path. The final construction/extension chapters remain
adjacent (new 28–29) and are followed by architectural judgment (new 30).

The plan includes an old→new map, chapter budgets, 374 chapter-reference records,
figure/index impact, early MiniGateway milestones, and a runnable checkpoint for
every Part. The plan check accounts for all 62 manuscript inputs exactly once and
confirms the budget arithmetic. The unchanged manuscript remains 146,950 words;
`metrics-after-phase-4.json` and the scope diff prove this is planning only.

**Status: awaiting author approval. Approval has not been given.** The author must
approve this concrete plan before Phase 5a; record that decision here. The proposed
Part sessions are 5b–5l, with the final Part owning the associated appendix,
epilogue, reference material, and global/proposal refresh. No restructuring,
new objectives/exercises, or milestone implementation occurred in Phase 4.

Commit: `proposal-readiness: phase 4 — propose consolidated teaching-book structure`.
Stop after this commit. Do not begin Phase 5a on the basis of this plan's existence.

## Author amendment — teaching book, 2026-09-22

Accepted during Phase 1; the full amendment is appended to
`review/proposal-readiness-2026-09-22/PROMPT.md` and supersedes conflicting earlier
requirements. The primary reader is an advanced student or C++ developer with
the stated prerequisites and no SNode.C knowledge, learning from the book without
a lecturer. Phase 3 must position the book around that learning, with course use
as one secondary-benefit sentence mentioning the framework's origin in "Network
and Distributed Systems" at FH Upper Austria, Hagenberg. Course adoption is not
the proposal's organizing premise.

For the five Phase 2 samples, and all other chapters in Phase 5: open with 3–5
observable objectives in `.snodec-objectives`; close with at most five remember
bullets followed by review questions, labs with expected outcomes, and design
problems. Map every objective to exercises and every exercise to objectives in
chapter-ledger.md. Public lab solutions belong in `companion/exercises/<chapter>/`
and must build in CI; public conceptual answers and design discussions belong
there in README.md or in the back-matter "Solutions and discussion" section.

The rule-box cap and Phase 1 exit criterion are now **20**, retaining principles
the learner must apply. Phase 3 presents one learning path and at most two
shortcuts. Phase 4 evaluates early MiniGateway milestones culminating in Chapters
35–36, and a runnable, verifiable checkpoint at the end of every Part. The final
Phase 5 sub-phase must meet every pedagogical requirement. These additions do not
start another phase during this Phase 1 session.
The author's subsequent execution clarification applies only the rule-box change
in Phase 1: restore previously removed applicable principles, remove only
near-tautologies and duplicates, and list every restoration in REPORT.md. The
verbatim amendment and this scope record receive their own commit, titled
`proposal-readiness: author amendment — teaching book`. No objectives, exercises,
solutions, or learning-path implementation belongs in Phase 1.

## Governing constraints

1. Refine the existing book in its established voice and depth. Do not rewrite
   whole parts, replace the teaching approach, or reorganize the 38 chapters.
2. Do not pursue shortening. Remove or reshape repetition only when doing so
   improves the teaching; preserve purposeful reinforcement and substantive detail.
3. Work from the current Markdown manuscript, including front matter, part
   introductions, epilogue, and back matter, in `manuscript/book-files.txt` order.
   Do not use the PDF as the content authority.
4. Prove technical alignment through current SNode.C source, including the author's
   uncommitted changes, relevant companion builds, and appropriate behavioral tests.
   Do not use the remote branch or base commit alone as a substitute.
5. Preserve unrelated work. The first technical pass is the starting point for
   editorial work, not permission to overwrite the author's subsequent changes.
6. Distinguish finished work from a documented limitation or an unexecuted test.
   A stronger technical baseline is not a completed publisher-level editorial pass.

## Starting point: completed technical work

The earlier pass corrected segmentation-dependent line limits, private MQTT
CONNECT-extension use, overstated SSE Accept handling, setup instructions,
state-changing GET routes, and unconditional Bluetooth-pairing language. It
strengthened TLS teaching with verified identity-policy examples and aligned
endpoint/flow terminology, public tick behavior, and logging commands with the
current framework source. It added source evidence and selected runtime checks.

Those changes are useful foundations. They do not establish that the full
manuscript has received systematic repetition removal, prose editing, or practical
chapter-depth refinement. In particular, SSE idle-subscriber retention and the
WebSocket example's unsupported-input behavior were qualified rather than fixed.

## Work sequence and acceptance criteria

### Accepted execution method — 21 September 2026

The author authorized the proposed combined pass: first map repetition across
the whole book, then refine coherent chapter groups across all six editorial
dimensions together, and finally reread the integrated manuscript. Track the six
dimensions separately; grouping the work does not merge their acceptance criteria.
The remaining example fixes and broader runtime validation stay separate workstreams.

The initial map and chapter groups are recorded in
`review/editorial/repetition-map.md`. It distinguishes the structural inventory
from the full contextual reading that follows. The editorial starting snapshot is
recorded in `review/editorial/pass-baseline-2026-09-21.json`.

### Author scope revision — follow-up pass, 21 September 2026

The author explicitly requested a checkpoint commit followed immediately by four
items: a simple, obvious SSE code example; an equally clear WebSocket echo example;
Bluetooth hardware prerequisites and preparation/pairing in principle without a
new addressing tour; and final closure of this refinement pass. Put those texts
in Chapters 23, 24 and 12 respectively. Synchronize dependent capstone examples
where the same lifetime contract occurs. Preserve the established voice and depth.

OpenWrt remains deferred because its integration is not updated and is expected to
fail compilation/installation. Broader Bluetooth hardware, database, broker,
MQTTSuite deployment and sustained-load validation is intentionally omitted from
scope: the reader is expected to apply the book's explanations to those programs.
This is a scope decision, not a successful test result. Focused checks required to
verify the changed examples and their source alignment remain part of this pass.
PDF regeneration and visual production review remain deferred; the book is not
being declared finished. These accepted decisions supersede the earlier pending
acceptance requirements below; historical checkpoint records remain unchanged.

### 1. Repetition and manuscript-wide progression — done

- Read all manuscript inputs, including framing material, as one continuous book.
- Inventory recurring explanations, especially layer boundaries, role/instance/
  flow distinctions, ownership, configuration, and architecture-first conclusions.
- Record the primary teaching location and the purpose of each significant repeat.
  Keep repeats that introduce a new context, consequence, example, or necessary reminder.
- Refine repeated openings, transitions, conclusions, lists, and slogans that add
  no new teaching value. Do not mechanically replace explanations with cross-references.
- Edit in coherent chapter groups and reread the neighboring transitions.

Done when every chapter and framing section has been assessed, significant
redundant clusters have been resolved or intentionally retained with a reason,
and the chapter ledger contains actual editorial outcomes. Word-count reduction
is not an acceptance criterion.

### 2. Prose and voice — done

- Review sentence-level redundancy, abstract wording, unnecessary emphasis, vague
  claims, and repeated conclusions within paragraphs and sections.
- Preserve the author's pace, vocabulary, explanatory layering, and depth.
- Make changes locally; avoid generic replacement prose or blanket style rules
  that flatten the book's distinctive teaching voice.
- Review edited passages in context, not only as isolated diffs.

Done when all manuscript inputs have received a prose pass and a contextual reread.
Track issues actually improved; do not count new paragraphs as proof of cleanup.

### 3. Reader positioning and learning progression — done

- Sharpen the primary reader and prerequisites using the existing audience and
  teaching approach; do not reposition the book for a different market by assumption.
- Check front matter, chapter promises, introduced terminology, and assumed skills
  for consistency with that reader.
- Make the movement from guided examples to independent application clearer.
- Preserve useful alternative reading routes without making competing audiences
  equally primary throughout every chapter.

Done when reading guidance, prerequisites, chapter introductions, and exercises
form one consistent learning progression without unsupported assumptions.

### 4. Practical depth and exercises — done within revised scope; OpenWrt deferred

- Identify chapters whose titles or promises exceed their demonstrated practice.
- Strengthen the existing treatment with reproducible exercises, observable
  outcomes, and failure cases where these add understanding.
- Complete the Linux service-operation treatment. Keep the OpenWrt walkthrough
  conditional; its recipe port, cross-build and deployment remain deferred by
  the author until the integration is updated.
- Verify runnable instructions and clearly identify prerequisites and platform
  requirements. Do not present an unexecuted deployment recipe as tested.

Done within the revised scope: identified writing gaps and focused example checks
are complete. The original hardware/service acceptance was explicitly removed by
the author; OpenWrt is deferred. Neither scope decision counts as a successful
hardware, service or deployment test.

### 5. Architectural alternatives and tradeoffs — done

- Develop concrete decisions already present in the book by comparing plausible
  alternatives, their costs, and the conditions favoring each.
- Prioritize ownership/lifetime, endpoint versus flow policy, process boundaries,
  protocol selection, persistence, and recovery.
- Avoid inventing weak alternatives solely to make the preferred design look good.
- Replace repeated endorsements with reasoning where that improves the passage.

Done when the relevant decisions teach judgment through credible alternatives
and consequences, rather than merely reiterating the preferred boundary.

### 6. References, diagrams, and captions — done

- Check every diagram's explanatory claims, labels, arrows, scope, and caption
  against surrounding prose and current source.
- Inspect editable diagram sources; the PDF is not the manuscript authority.
- Review cross-references, terminology, source pointers, and companion navigation
  across the whole book, beyond the specific corrections already made.
- Preserve established figure identifiers and references unless a justified edit
  updates every dependent reference coherently.

Done when all figures and references have been checked for content consistency
and automated reference checks pass. Visual production QA is a separate status.

### 7. Remaining example behavior — done

**SSE subscriber lifetime:** trace the existing response, connection, and publisher
ownership and disconnection hooks. Correct idle disconnected-subscriber retention
at its ownership boundary, and test client churn with no new measurements.
Documentation of publication-driven cleanup alone does not complete this item.

**WebSocket unsupported input:** preserve the compact example's intended teaching
contract. Either explicitly reject unsupported binary input for a text-only
protocol or preserve message type if a general echo is justified. Exercise both
text and binary input; a prose disclaimer alone does not complete this item.

For both changes, first look for existing mechanisms and a solution by reduction
or modification. If a correct implementation requires net production-code growth,
prepare the concrete design, justification, expected growth and verification plan,
then obtain the approval required by the user's engineering instructions before
implementing that addition. Do not reduce line counts through formatting tricks.

Completed: the small SSE publisher and both capstone models now remove subscriptions
through the existing HTTP-context disconnect callback. Explicit unsubscribe
replaces publication-time pruning. The WebSocket server preserves text/binary type
and exact bytes with its existing whole-message teaching structure. Code and
printed examples agree; idle FIN/RST churn and complete message exchanges passed.
The earlier checkpoint reproduces the idle-retention failure under the same test.
Details and precise test limits are in [the follow-up report][P].

### 8. Broader validation — intentionally omitted; OpenWrt deferred

The original verification inventory remains below for provenance. The author has
removed these broader runs from the current acceptance scope; OpenWrt alone is
deferred for a future integration update. No successful execution is implied:

- Bluetooth exchanges on suitable hardware and relevant operating-system policy.
- OpenWrt build, deployment, service operation, and restart behavior.
- Live MariaDB service integration and relevant asynchronous failure behavior.
- Full MQTT broker interoperability for the teaching scenarios, beyond CONNECT bytes.
- Sustained-load and long-duration behavior for the relevant application boundaries.

If the author later restores a broader check to scope, define its scenario,
expected result, facilities and bounded resource use before execution. Until then,
retain the distinction between source inspection and an actual runtime result;
do not count intentionally omitted runs as passes.

### 9. Integration and final review — done for the authorized refinement passes

- Reread the refined manuscript end to end for progression, repetition, voice,
  depth, terminology, and consistency between claims and examples.
- Reconcile the source baseline and evidence with the current framework tree;
  preserve prior results with their original source identity.
- Run appropriate source/listing/reference checks and affected builds/tests.
- Report production-code, test-support, and manuscript changes separately.
- Report which publisher-review recommendations are completed and which remain
  pending or blocked. Full completion requires every required item to be resolved
  or an explicit user decision changing its scope.

The combined manuscript reread and its evidence remain recorded in
`review/editorial/refinement-2026-09-21.md`. The four-item follow-up is now closed
under the author's explicit revised scope; its report and current evidence are in
`review/followup-2026-09-21/`. The affected sections, companion code and current
source were reconciled. OpenWrt and production are deferred; the book remains
open to further refinement. Broader validation is intentionally omitted, not passed.

PDF regeneration and visual review remain outstanding production work. Do not
read the PDF or silently add a PDF review while the author's Markdown-only reading
instruction remains in force; establish that separate scope when requested.

## Chapter ledger

### Current authority — pedagogical smoothing, Follow-up 11

The 32-chapter structure below supersedes the historical ledger that follows.
Progress and evidence are maintained in the current pass’s chapter-ledger.md.

| New | Old | Before | After | Floor | Cap | Rows | Change and dimension evidence | Remaining qualification |
|---|---|---:|---:|---:|---:|---|---|---|
| 1 | 1 | 1,821 | 2,402 | 2,400 | 2,670 | 2, 25, 18, 1, 15, 27 | Problem runway precedes terminology; Asio comparison points ahead. E/G: `manuscript/chapters/01-why-snodec-exists.md:14` | No runtime capacity claim. |
| 2 | 2 | 3,006 | 3,194 | 3,006 | 3,250 | 5, 18, 1, 15, 27 | Setup route first; one source sidebar contains pin and alignment. G/L: `manuscript/chapters/02-preparing-your-environment.md:18` | Compiler/package prerequisites remain substantial. |
| 3 | 3 | 2,568 | 3,001 | 3,000 | 3,270 | 2, 25, 16, 1, 15, 27 | Chronological echo trace before file walkthrough and vocabulary. E/G/T: `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:21` | Full C++ files intentionally retain identifiers. |
| 4 | 4a | 1,992 | 2,908 | 2,700 | 3,050 | 3, 2, 16, 1, 15, 27 | Runtime taxonomy separated; lifetimes, examples and log checkpoint. S/G/C: `manuscript/chapters/04-the-snodec-runtime-mental-model.md:13` | Flow versus connection still needs deliberate practice. |
| 5 | 4b | 2,083 | 2,882 | 2,875 | 3,325 | 3, 2, 1, 15, 27 | Layer changes spaced through concrete comparisons and build observations. S/G: `manuscript/chapters/05-layers-in-practice.md:9` | TLS security details explicitly deferred to Ch15. |
| 6 | 5 | 2,983 | 3,502 | 3,500 | 3,850 | 4, 28, 18, 1, 15, 27 | Wait/dispatch/work/timeout/cleanup model precedes source; model interface printed. G/E/C: `manuscript/chapters/06-core-runtime-and-event-processing.md:18` | Runtime source remains identifier-rich. |
| 7 | 6 | 4,175 | 4,206 | 4,175 | 4,250 | 26, 1, 15, 27 | Comparison is introduced before use; preserved address treatment. S: `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:254` | Bluetooth/device behavior is conditional on equipment. |
| 8 | 7 | 3,084 | 3,184 | 3,150 | 3,334 | 31, 16, 1, 15, 27 | Single-peer timeline replaces repeated runtime taxonomy. T/C: `manuscript/chapters/08-servers-clients-and-connections.md:15` | Callback layers require careful reading. |
| 9 | 8 | 2,170 | 2,173 | 2,120 | 2,220 | 1, 15, 1, 15, 27 | Canonical vocabulary and surrounding seams; structure preserved. L/C: `manuscript/chapters/09-bluetooth-in-snodec-rfcomm-and-l2cap.md:6` | No Bluetooth hardware certification. |
| 10 | 9 | 3,089 | 3,087 | 3,040 | 3,140 | 1, 15, 1, 15, 27 | Context/connection wording checked in place; source-close reference model preserved. L/C: `manuscript/chapters/10-writing-socketcontext-classes-well.md:1` | No replacement treatment. |
| 11 | 10 | 2,265 | 2,258 | 2,215 | 2,315 | 1, 15, 1, 15, 27 | Factory/object wording checked; lifetime treatment preserved. L/C: `manuscript/chapters/11-writing-socketcontextfactory-classes-well.md:1` | Shared state ownership remains explicit. |
| 12 | 11 | 2,555 | 2,581 | 2,505 | 2,605 | 1, 15, 1, 15, 27 | Network-family and connection-variant distinctions normalized. L: `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:292` | Old anchor/figure IDs intentionally preserved. |
| 13 | 12 | 4,273 | 4,475 | 4,300 | 4,673 | 10, 16, 1, 15, 27 | One running port/configuration example; duplicate taxonomy removed. G/C: `manuscript/chapters/13-configuring-applications-and-named-instances.md:22` | Full configuration vocabulary remains. |
| 14 | 13 | 2,698 | 2,793 | 2,650 | 2,800 | 20, 18, 1, 15, 27 | Logging wording simplified; construction precedes inventory; migration voice removed. X/L: `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:59` | Reference API table retains density. |
| 15 | 14 | 2,579 | 2,754 | 2,700 | 2,900 | 24, 15, 1, 15, 27 | Trust/identity distinction and application setup now visible before lab. T/C: `manuscript/chapters/15-tls-across-the-framework.md:50` | Local certificate fixtures are not deployment certification. |
| 16 | 15 | 2,990 | 3,200 | 3,200 | 3,390 | 14, 1, 15, 27 | Application setters and CLI before internal recovery model. T: `manuscript/chapters/16-timeouts-retries-and-failure-modes.md:108` | Identifier increase is the requested compilable example. |
| 17 | 16 | 2,471 | 2,478 | 2,450 | 2,600 | 17, 1, 15, 27 | Build housekeeping boxed; prose transition into Express. S: `manuscript/chapters/17-the-http-layer.md:307` | Protocol reference treatment preserved. |
| 18 | 17 | 2,065 | 2,218 | 2,050 | 2,315 | 7, 16, 17, 1, 15, 27 | Complete dispatch followed by request trace; reference inventory follows mechanism. T/D/G: `manuscript/chapters/18-the-express-like-framework.md:23` | Identifier density increases for concrete routing explanation. |
| 19 | 18 | 3,269 | 3,305 | 3,220 | 3,370 | 17, 1, 15, 27 | Build note followed by an SSE-to-WebSocket transition. S: `manuscript/chapters/19-server-sent-events-and-real-time-http.md:425` | Long-lived response reference model preserved. |
| 20 | 19 | 3,000 | 3,001 | 2,950 | 3,100 | 1, 15, 1, 15, 27 | Terminology/seams checked; upgrade mechanism preserved. L/C: `manuscript/chapters/20-websocket-and-protocol-upgrade.md:21` | Negotiated protocol lifetime remains a key distinction. |
| 21 | 20 | 2,005 | 3,015 | 3,000 | 3,405 | 8, 17, 19, 1, 15, 27 | Conversation precedes class inventory; five distinct outcomes and carrier definition. D/E/G: `manuscript/chapters/21-mqtt-support-in-snodec.md:5` | Local broker evidence is not fleet-scale evidence. |
| 22 | 21 | 1,782 | 2,119 | 2,100 | 2,282 | 30, 17, 19, 1, 15, 27 | Native/composed traces separate failure evidence; Build note and transition. T/X: `manuscript/chapters/22-mqtt-over-websocket.md:20` | Layer tables retained as references after explanation. |
| 23 | 22 | 2,922 | 3,141 | 3,100 | 3,222 | 29, 19, 1, 15, 27 | Concrete before/after HTTP/MQTT adapter decision grounds system design. T/X: `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:26` | Design vocabulary remains frequent; see diagnostic review. |
| 24 | 23 | 3,826 | 3,857 | 3,826 | 3,926 | 15, 1, 15, 27 | Persistence conclusion leads to reading complete applications. C: `manuscript/chapters/24-database-support-and-application-state.md:13` | Local restart lab does not certify production durability. |
| 25 | 24a | 2,018 | 2,560 | 2,450 | 2,600 | 6, 15, 1, 15, 27 | Target-to-contract reading cycle; incidental inventory removed; final apparatus. S/E: `manuscript/chapters/25-reading-complete-snodec-applications.md:4` | Application catalog intentionally not expanded. |
| 26 | 24b | 3,573 | 3,843 | 3,750 | 3,941 | 6, 15, 18, 19, 1, 15, 27 | Process-oriented publication trace, evidence limits and Part IX checkpoint. S/E/C: `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:6` | MQTTSuite deployment itself was not run. |
| 27 | 25 | 3,903 | 3,748 | 3,700 | 4,000 | 9, 19, 1, 15, 27 | Minimal consumer first; 15-line consumer graph replaces build inventory. T/E/G: `manuscript/chapters/27-cmake-components-and-linking-strategy.md:19` | Installed component contracts remain source-specific. |
| 28 | 26 | 3,596 | 3,586 | 3,546 | 3,646 | 15, 1, 15, 27 | Operational handoff to testing; provenance phrase removed locally. C/L: `manuscript/chapters/28-deployment-on-linux-and-openwrt.md:340` | No OpenWrt device deployment certification. |
| 29 | 27 | 4,169 | 4,360 | 4,300 | 4,500 | 21, 22, 18, 1, 15, 27 | Problem-first entry and explicit measurement stance. E/D: `manuscript/chapters/29-testing-debugging-and-benchmarking.md:20` | No performance capacity figures or claims. |
| 30 | 28 | 3,818 | 4,587 | 4,400 | 4,618 | 11, 15, 1, 15, 27 | Every complete listing separated by interpretation; capstone ownership unchanged. T: `manuscript/chapters/30-building-minigateway.md:473` | Listing interpretation is concise by design. |
| 31 | 29 | 2,541 | 2,834 | 2,650 | 2,841 | 12, 1, 15, 27 | 147-line marked source becomes three explained excerpts; full companion preserved. T: `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:338` | CMake blank-line formatting approved by author. |
| 32 | 30 | 1,850 | 3,108 | 3,100 | 3,350 | 13, 1, 15, 27 | Three added worked decisions apply the five questions and state consequences. D: `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:38` | Verdicts depend on the stated requirements. |
| A | A | 3,694 | 3,968 | 3,900 | 3,994 | 23, 4, 1, 15, 27 | Flexible entry and relocated descriptor-population source reading. E/C: `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:322` | Source-reading detail intentionally dense. |

### Historical ledger — before pedagogical smoothing

The statuses below concern the outstanding editorial pass. They do not erase the
previous technical work. Use `pending`, `in progress`, `done`, `blocked`, `deferred`, or `omitted` with a
specific reason. A completed row needs a short outcome and evidence reference,
including any repetition deliberately retained. Update a row only after reading
and editing or explicitly assessing that chapter; do not mark an entire range done
from a sample.

All chapter rows include full reading and the integrated contextual reread. A
`done` practice cell means the chapter's identified editorial gap was assessed
and its appropriate evidence recorded, not that every suggested deployment was
executed. The later author decision omits service-dependent validation; OpenWrt is deferred. The
[evidence report][E] distinguishes source reading, builds and actual exchanges;
the [repetition map][R] records deliberately retained reinforcement.

[E]: editorial/refinement-2026-09-21.md
[R]: editorial/repetition-map.md
[P]: followup-2026-09-21/REPORT.md

| Chapter | 1 Repetition | 2 Prose | 3 Progression | 4 Practice | 5 Tradeoffs | 6 References/figures | Outcome/evidence |
|---|---|---|---|---|---|---|---|
| 01 | done | done | done | done | done | done | Consolidated scope; concrete closing decision; Figure 1 caption. [Evidence][E]; [repetition decisions][R]. |
| 02 | done | done | done | done | done | done | Repeated directory recap becomes installed-package diagnosis. [Evidence][E]; [repetition decisions][R]. |
| 03 | done | done | done | done | done | done | Configuration/activation distinction; controlled echo exercise; credible blocking-loop tradeoff. [Evidence][E]; [repetition decisions][R]. |
| 04 | done | done | done | done | done | done | Repeated model recap becomes a source trace and prediction exercise. [Evidence][E]; [repetition decisions][R]. |
| 05 | done | done | done | done | done | done | Primary model retained; flow lifetime explicit in Figure 2; dependency lifetime developed. [Evidence][E]; [repetition decisions][R]. |
| 06 | done | done | done | done | done | done | Duplicate tick summary replaced by ordering; actual event publication semantics; Figure 3 corrected; checked runtime reconfiguration source reconciled and tests passed. [Evidence][E]; [repetition decisions][R]. |
| 07 | done | done | done | done | done | done | Repeated type/component expansion becomes a conversion check; cross-layer failure diagnosis. [Evidence][E]; [repetition decisions][R]. |
| 08 | done | done | done | done | done | done | Default/path semantics qualified; address-classification exercise. [Evidence][E]; [repetition decisions][R]. |
| 09 | done | done | done | done | done | done | Concrete callback timing and borrowed disconnect pointer; fresh-state test; Figure 5 activation paths. [Evidence][E]; [repetition decisions][R]. |
| 10 | done | done | done | done | done | done | Repeated role inventories consolidated; separate versus dual-stack listener choice. [Evidence][E]; [repetition decisions][R]. |
| 11 | done | done | done | done | done | done | Duplicate model lists refined into pathname/credential consequences; input/rendering distinction. [Evidence][E]; [repetition decisions][R]. |
| 12 | done | done | done | done | done | done | Hardware/controller/service prerequisites and conditional pairing preparation refined in Chapter 12; existing addressing treatment not expanded. Hardware exchange intentionally omitted. [Follow-up][P]. |
| 13 | done | done | done | done | done | done | Consumed bytes versus complete messages; framing and peer-isolation cases; factory transition. [Evidence][E]; [repetition decisions][R]. |
| 14 | done | done | done | done | done | done | Dependency lifetime alternatives; observable factory behavior tests; less repeated construction summary. [Evidence][E]; [repetition decisions][R]. |
| 15 | done | done | done | done | done | done | Runnable two-carrier line-protocol exercise added; Figure 4 separates behavior from construction. [Evidence][E]; [repetition decisions][R]. |
| 16 | done | done | done | done | done | done | Replaced obsolete startup-only claim with explicit runtime reparse boundaries; separated server/client configuration keys and operational choices. [Evidence][E]; [repetition decisions][R]. |
| 17 | done | done | done | done | done | done | Added verified three-source precedence exercise and current reconfigure lifecycle/failure semantics; consolidated duplicate scope/name inventories. [Evidence][E]; [repetition decisions][R]. |
| 18 | done | done | done | done | done | done | Preserved detailed logging treatment; distinguished reparsed options from frozen effective logging; documented and checked the new scoped binary dump surface. [Evidence][E]; [repetition decisions][R]. |
| 19 | done | done | done | done | done | done | Developed carrier-specific trust consequences and in-process/proxy tradeoff; replaced repeated architecture inventory with failure observations. [Evidence][E]; [repetition decisions][R]. |
| 20 | done | done | done | done | done | done | Clarified retry counts, inactivity versus message deadlines, replay uncertainty, and one-flow recovery diagram. [Evidence][E]; [repetition decisions][R]. |
| 21 | done | done | done | done | done | done | Replaced repeated stack inventories with request-admission trace and controlled parser-policy cases. [Evidence][E]; [repetition decisions][R]. |
| 22 | done | done | done | done | done | done | Added executable middleware order/short-circuit exercise from current tests; explained counts and response evidence. [Evidence][E]; [repetition decisions][R]. |
| 23 | done | done | done | done | done | done | Complete compact SSE example now shows explicit subscribe/unsubscribe and connection-owned cleanup. Idle churn releases responses without publishing; framing and observation exercise retained. [Follow-up][P]. |
| 24 | done | done | done | done | done | done | Whole-message echo preserves text/binary type and exact bytes; redundant buffer resets removed. Teaching client and independent empty, binary, sequential and fragmented exchanges passed. [Follow-up][P]. |
| 25 | done | done | done | done | done | done | Connection/session/subscription/delivery explanation complete; full broker rehearsal intentionally omitted by author. [Evidence][E]. |
| 26 | done | done | done | done | done | done | Binary CONNECT payload and carrier trace retained; full MQTT-over-WebSocket broker exchange intentionally omitted by author. [Evidence][E]. |
| 27 | done | done | done | done | done | done | Fan-out, partial-failure exercise and process costs refined; live-broker rehearsal intentionally omitted by author. [Evidence][E]. |
| 28 | done | done | done | done | done | done | SQL-error queue and commit limitations explained from source; live MariaDB failure rehearsal intentionally omitted by author. [Evidence][E]. |
| 29 | done | done | done | done | done | done | Consolidated repeated imported-target/category material; added JSON pair source exercise and executable-variant tradeoff. [Evidence][E]; [repetition decisions][R]. |
| 30 | done | done | done | done | done | done | Replaced repeated role/protocol inventories with compatibility and restart reasoning; distinguished carrier recovery from operation outcomes. [Evidence][E]; [repetition decisions][R]. |
| 31 | done | done | done | done | done | done | Current suite source and raw/projection write boundaries inspected; suite deployment intentionally omitted by author. [Evidence][E]. |
| 32 | done | done | done | done | done | done | Qualified link visibility and runtime defaults; added installed-component failure exercise. [Evidence][E]; [repetition decisions][R]. |
| 33 | done | done | done | deferred | done | done | Linux walkthrough and bounded rehearsal complete. OpenWrt integration is not updated and is expected to fail build/install; further OpenWrt work deferred by author. [Evidence][E]; [scope decision][P]. |
| 34 | done | done | done | done | done | done | Added checked-reconfiguration test guidance and executable bounded latency experiment; distinguished diagnostic formatter tests from actual wire exchanges and service assertions. [Evidence][E]; [repetition decisions][R]. |
| 35 | done | done | done | done | done | done | Printed model/web/MQTT listings synchronized to explicit unsubscribe; current-source and focused idle-cleanup/HTTP/CONNECT checks passed. Broader broker delivery/restart runs intentionally omitted. [Follow-up][P]. |
| 36 | done | done | done | done | done | done | Existing new-role explanation retained; Extended companion uses the same corrected model and SSE ownership as Chapter 35. Unix input and idle cleanup passed. [Follow-up][P]. |
| 37 | done | done | done | done | done | done | Replaced weak alternatives with credible HTTP/MQTT/Unix/separate-service decisions; consolidated opening inventory. [Evidence][E]; [repetition decisions][R]. |
| 38 | done | done | done | done | done | done | Added runtime-option effect boundary and extension design exercise; integrated per-flow invariant before the summary. [Evidence][E]; [repetition decisions][R]. |

| Other manuscript input | Editorial status | Outcome/evidence |
|---|---|---|
| Front matter | done | Prerequisites and reading routes refined; all inputs contextually reread. [Evidence][E]. |
| Part introductions | done | All read and reread with surrounding chapters; Parts I–II refined; other transitions intentionally retained. [Evidence][E]; [repetition decisions][R]. |
| Epilogue | done | Locally refined abstraction tradeoff and concluding claims; integrated reread complete; useful synthesis retained. [Evidence][E]. |
| Back matter and further reading | done | All inputs assessed; primary standards/tool references added; external-link and visual-QA limits recorded. [Evidence][E]. |

## Session record and handoff

At the end of each refinement session, append a concise entry containing:

- items and chapters actually assessed or changed;
- important repetitions removed, developed, or intentionally retained;
- source identity and checks executed, with links to durable evidence;
- remaining uncertainties or blockers;
- the next concrete unfinished action.

Update work-item status and chapter rows as well as the session entry. Do not
silently redefine acceptance criteria to match whatever work happened to finish.
No automatic background work or scheduled execution is implied by this plan.

### 21 September 2026 — plan established

Recorded the author's accepted unfinished scope and persistent instructions.
No additional manuscript refinement was performed while establishing this plan.
All editorial ledger rows remain pending. Existing technical changes and evidence
remain in the working tree. Next: inventory repetition in manuscript order and
identify its primary teaching locations before the first editorial batch.

### 21 September 2026 — combined pass, first checkpoint

Mapped whole-book repetition and captured an editorial starting snapshot before
edits. Read Chapters 1–15 in full and refined local passages across the six
dimensions; the ledger records outcomes without treating this checkpoint as the
final contextual reread. All front matter, part introductions, and back matter
were read during the inventory. Edited figure sources 2–5 and Figure 1's caption.
No PDF was read or generated. Complete companion listings remain unchanged.

Source hygiene and listing/reference checks passed against the recorded package.
The framework author committed the previously captured changes as `15ddc04c7`
with identical file contents, then began further runtime-configuration changes.
The full working-tree comparison correctly detected those later differences.
Current-source reconciliation, refreshed source anchors, and affected runtime
validation are pending; the earlier manifest and runtime results remain dated
evidence, not proof for those newer changes. The checker no longer requires HEAD
to equal the reconstruction base, but retains complete file-content verification.

The Chapter 15 Unix variant builds against the earlier verified installation;
the IPv4 variant and independent-peer exercise are being checked. Next: finish
that exercise verification, then read/refine Chapters 16–20 against the current
configuration and TLS/runtime sources. Remaining example behavior and broader
validation are still separate workstreams, as authorized.

### 21 September 2026 — combined pass, second checkpoint

Read Chapters 16–31 in full and refined them locally across the six dimensions.
Inspected figure sources 6–10 and 13–17; edited 10, 15–17 and related captions.
The transfer exercise passed for both carriers, including fragmented input, two-peer
isolation, and owned Unix-path cleanup. The configuration precedence experiment
passed (8080 / 18091 / 18092); corrected its reading instructions to distinguish
commented defaults from active assignments and the display action’s exit status 2.
Logs are in `review/editorial/`. Those probes used the earlier verified installation.

The current framework’s new runtime reconfiguration implementation and tests were
read; Chapters 6, 16–18, 22, and 24 now reflect its boundaries. A framework rebuild
against the changed author source is in progress. Source-manifest refresh, affected
checks, and integrated reread remain pending. No framework files were edited.

The MariaDB source shows that a usable connection advances its command queue after
a SQL error; prequeued commit is not conditional on earlier success. Chapter 28 now
explains that constraint. Current MQTTSuite is a separate clean checkout at
`f96daffdbae8f95531a73fb52c9d22d410044211`; its store submits raw and projection writes
separately. Chapter 31 and Figure 10 now distinguish those outcomes. No live suite
or database deployment is claimed. Next: Chapters 32–34, followed by the capstone
and judgment/extension chapters; then end-to-end reread and fresh source evidence.


### 21 September 2026 — combined pass, third checkpoint

Completed full reading and local refinement through Chapter 38 and the epilogue.
All 18 editable figure sources have been inspected for content. The new Linux
service rehearsal passed with temporary paths, an isolated configuration base,
and a transient systemd user unit. The persistent unit was syntax-checked; it
was not installed or enabled. The initial harness tried to restart an already
discarded transient definition; that harness error and the corrected successful
run are both retained. The bounded measurement example executed successfully.

Current local framework HEAD is `2e52b6b7337f21812932eb1e097fb3c27c8228a9`,
clean, tree digest `3eac377ad4ca4a3786577763ec2a9ca0f8fc1e256e6defd7e80580a1d28023b7`.
All 183 framework tests passed after rebuild. The installed external echo tests
(4), contract probes (3), teaching checks and four behavior scenarios passed.
The Chapter 15 transfer exercise passed again against the rebuilt installation.
The refreshed base-plus-patch reconstruction reproduces all 1,447 recorded files.
Earlier source manifest/patch copies now accompany the earlier verification logs.

The inspected OpenWrt feed (`c9378fe95f7c015752c748fc4ab012b585d294d1`) still
targets framework 1.0.1 and its OpenWRT branch. Chapter 33 explicitly requires a
2.0 recipe port, matching SDK and test device; no old source substitution or
cross-build claim was made. Those unavailable facilities qualify practical-depth
completion and remain part of the separately tracked deployment validation.
Next: contextual integration review, final source/listing/reference checks and
separate accounting of manuscript, figure, companion and verification changes.

### 21 September 2026 — combined pass, final checkpoint

All 62 manuscript inputs and all 38 chapters received the combined pass and the
integrated contextual reread. All 18 editable figures received content review.
The final reread covered prose, tables, exercises and unmarked code sketches in
manuscript order; exact marked listings had already been fully read and were
independently compared with their companion sources. The small integration edits
were then reread in place. No PDF was read or regenerated.

Dimensions 1, 2, 3, 5 and 6 now meet their criteria. Dimension 4 remains in progress
because its actual platform/service requirements have not all been executed.
Linux, transfer, configuration, component selection, bounded measurement and
WebSocket negotiation rehearsals passed. Unsupported WebSocket selection returned
404 and attached no echo subprotocol; this does not resolve binary-input behavior.
The first WebSocket harness used debug level 5, which hid the example's trace
observations; the corrected level 6 run passed and the chapter now specifies it.

The final author-source capture is HEAD
`2e52b6b7337f21812932eb1e097fb3c27c8228a9` plus 25 changed paths, exact tree digest
`df2fbdbe844f3368f5ed142973d82c0008a057c13d87dda6b7670e45cc3eacb8`.
The framework was rebuilt and installed; all 183 framework tests passed, as did
4 installed-echo tests, 3 contract probes, 3 teaching groups and 4 companion
behavior scenarios. Exact source reconstruction, 38 chapter evidence records,
35 complete listings and reference/source hygiene checks passed. Binary logging
changes made by the author during the session were reviewed and reflected in
Chapters 18 and 34. Earlier source cohorts and their failures remain historical.

The report, precise verification limits and separate change accounting are in
`review/editorial/refinement-2026-09-21.md`; exact identities and log hashes are in
`review/editorial/evidence-2026-09-21.json`. Repetition decisions and figure outcomes
are in `review/editorial/repetition-map.md`. There was no shortening target;
manuscript additions develop the agreed practical depth. Companion production
C++ was unchanged during this editorial pass; earlier technical changes remain.

Remaining: item 4's OpenWrt/hardware/service evidence, item 7's two implementation
fixes, item 8's broader runtime validation, and subsequent full-plan closure.
The next independent action is the ownership/lifetime trace for idle SSE removal,
followed by a reduction/modification design; request approval only if a correct
implementation needs net production-code growth under the existing instructions.
Do not use the old OpenWrt feed as a substitute for a 2.0 recipe port. PDF production
and visual review remain separate scope. No background continuation is scheduled.

### 21 September 2026 — four-item follow-up completed

Created checkpoint `884dbfe` before changing the examples. The author then asked
that each new text be placed in its corresponding chapter: Bluetooth in Chapter
12, SSE in Chapter 23, and WebSocket in Chapter 24. Chapter 35's dependent printed
listings and both capstone source trees were kept consistent.

SSE now uses a stable subscription handle and the existing HTTP-context disconnect
callback to erase that listener. This replaces the boolean callback result and
publication-time pruning; the unused compact-publisher forwarding overload was
removed. WebSocket echo retains the incoming type alongside its message bytes
and calls the existing typed send operation. Redundant buffer resets were removed.
Production C++ changed by 64 added / 67 removed lines: no net production growth.

Focused tests passed for idle FIN/RST churn in all three SSE examples, a surviving
observer's delivery, final response release, the unchanged teaching WebSocket
client, text/binary byte equality, empty/sequential/fragmented messages, ping
interleaving and close. Test-only weak observers expose retained response owners;
no observer-count endpoint was added to production. The same probe against the
checkpoint detects the original idle retention in all three programs. Existing
bounded companion behavior checks also passed. No hardware or external service
was needed for these focused checks.

The current local framework is clean at
`bb63e8a87aeda88123e8c0d72cb6d298908a9fe6`, with the same exact file-content digest
`df2fbdbe844f3368f5ed142973d82c0008a057c13d87dda6b7670e45cc3eacb8` as the prior
verified source capture. The author's commit changed provenance, not contents.
No framework files were edited. Source anchors and all 36 marked complete listings
were checked; the SSE listing is newly complete. Primary BlueZ documentation and
the current family/build sources support the preparation guidance.

The four requested items are closed. See `review/followup-2026-09-21/REPORT.md`,
`evidence.json`, and `change-accounting.json` for outcomes, hashes and limits.
OpenWrt and PDF production remain deferred. Broader runtime validation is omitted
by the author's explicit decision, not represented as successful verification.
This closes the authorized pass, not the book. No background work is scheduled.

### 21 September 2026 — local PDF build and box-warning audit completed

The author explicitly authorized a local PDF build, an exhaustive report of
overfull/underfull boxes, and proposed fixes. This supersedes the prior PDF-work
deferral for this audit only. The ordinary clean build from checkpoint `fcbe51a`
succeeded: 490 PDF pages, all 18 figures rebuilt, and the figure contact sheet
regenerated. No manuscript or production configuration was edited.

The final book log contains 2 overfull horizontal boxes, 12 underfull horizontal
boxes and 11 underfull vertical boxes, with no overfull vertical boxes. The same
25 warnings repeat in all three book passes; the console's 75 emissions are not
75 distinct defects. The 19 figure/contact-sheet logs contain no box warnings.
All 23 actual affected pages were rendered and inspected; one callout's location
was corrected from the next logged shipout to its actual rendered page.

Separate native-width paragraph proofs support fixes for all horizontal warnings
without changing words or code: discretionary slash breaks, four paragraph breaks
at existing sentence boundaries, ragged-right recap bullets, and inset-preserving
ragged-right part-introduction text. A separate full-book diagnostic proof using
ragged-bottom setting eliminated all 11 vertical warnings and retained 490 pages.
Those proofs did not replace the ordinary rebuilt PDF in `dist`.

The detailed inventory, source anchors, exact measurements, proposed fixes,
diagnostic logs and hashes are in `review/pdf-box-audit-2026-09-21/REPORT.md`,
`warnings.json` and `evidence.json`. Combining and implementing the proposals,
resolving Figure 34.1's table interruption, and any broader production cleanup
remain proposals, not completed work. A complete integrated rebuild and index/
reference/visual review are required after implementation. OpenWrt remains deferred;
broader runtime validation remains omitted. The book is not declared finished.

### 21 September 2026 — integrated PDF box fixes completed

The author authorized fixing all bad boxes, then requested reporting the font
shape warning while continuing those fixes. Later questions asked how to handle
the font shape and what the unused table-caption warning means; those questions
were treated as analysis requests, not permission to alter either setting.

All 25 audited box warnings are now resolved: zero overfull/underfull horizontal
or vertical boxes in the final book log and all three book passes. The 18 figure
logs and contact-sheet log also have zero box warnings. Warning thresholds were
not weakened. The PDF remains 490 pages, and all chapter starting pages remain
unchanged. The historical audit directory was preserved.

The shared recap style now uses hyphenation-aware ragged-right text; part
introductions retain their insets with natural right edges. Main-matter pages
use natural bottom spacing, with the original back-matter setting restored.
Targeted slash breaks and four paragraph divisions preserve the exact wording.
Figure 34.1 now follows the completed table and introduction on the same page.
Every one of the 62 manuscript inputs is unchanged after normalizing only those
formatting edits and whitespace: 151,914 source words before and after. All 779
non-LaTeX fenced blocks and all 36 marked complete listings are unchanged.

The ordinary integrated build, final index regeneration comparison, all 1,092
generated contents destinations, source hygiene, and alignment with the current
clean SNode.C tree at `bb63e8a87aeda88123e8c0d72cb6d298908a9fe6` passed.
Visual checks cover every affected page, every recap and continuation, all part
introductions, Chapter 4's closure, the Chapter 34 table/figure sequence, contents,
and index. See `review/pdf-box-fixes-2026-09-21/REPORT.md` and `evidence.json` for
the exact verification scope and durable evidence.

The missing Latin Modern Mono bold shape still falls back to regular weight;
an isolated proof supports an explicit companion-font mapping as a subsequent
candidate fix. The unused table-caption setup is harmless because all 165 tables
are uncaptioned. Both remain unchanged in the delivered PDF. The pre-existing
tocloft warning also remains outside this scope. No application or test code was
changed and no layout-change commit was made. OpenWrt and publication completion
remain deferred; broader runtime validation remains omitted by author decision.

### 22 September 2026 — font and unused-caption cleanup completed

After reviewing the companion font shapes, the author authorized applying the
font scheme. During verification, the author also requested eliminating the
unused table-caption setup warning. These explicit requests supersede the prior
report-only scope for those two warnings.

The book's existing metadata now registers Latin Modern Mono's companion bold and
bold-oblique files through standard Pandoc font options. Regular and ordinary
italic selection remain unchanged. The unused table-caption spacing option from
Pandoc's default template is removed through the caption package's existing
interface; all 165 current tables are uncaptioned. No warning filters or copied
templates were added.

The ordinary integrated build has zero font-shape warnings, zero unused-table-
caption warnings, and zero overfull/underfull boxes, with 490 pages and unchanged
chapter starting pages. All 62 manuscript files are byte-identical to the pass's
starting snapshot. Four-shape font proofs, representative page renders, final
contents destinations, index regeneration, source alignment, and source hygiene
were verified. See `review/pdf-font-fix-2026-09-22/REPORT.md` and `evidence.json` for
the exact scope, optical-size measurements, hashes, and logs.

Only the book metadata and review records changed in this pass: five configuration
lines added, no application or test implementation changes, and no manuscript
changes. The separate proposal profile and pre-existing tocloft warning were not
changed. No commit was made. The established OpenWrt, runtime-validation, and
publication-completion scope decisions remain in force.

### 22 September 2026 — checkpoint and package loading order completed

The author requested committing the current modifications before correcting the
package loading order. Commit `cb7fce2` records the preceding layout, font, and
caption refinements with their evidence. The subsequent change is separate and
uncommitted.

Pandoc previously loaded `parskip` before the book header loaded `tocloft`, so
`tocloft` could not install its contents hooks. The existing book metadata now
disables Pandoc's automatic paragraph-package loading through its standard
`indent` option and loads `tocloft,parskip` in that order. Explicit `parskip`
retains the existing unindented, spaced paragraphs. No copied template, warning
filter, or replacement of package internals was introduced. The independent
proposal profile does not load `tocloft` and is unaffected.

The clean three-pass build finishes without warnings; its initial reference and
table-width convergence messages are preserved in the evidence. A subsequent
ordinary three-pass build has zero warnings in its complete console output and
final log, zero bad boxes, and zero failed package patches. The PDF retains 490
pages. All page content streams, all page labels, the contents file, and the
index are unchanged. All 1,092 contents destinations and all 38 chapter starting
pages were checked, and independent MakeIndex regeneration matches. All 21
rendered comparison pages are pixel-identical; eight representative pages were
visually inspected. All 62 manuscript inputs are byte-identical, and current-tree
source alignment and hygiene checks pass.

See `review/pdf-package-order-2026-09-22/REPORT.md` and `evidence.json` for precise
checks and hashes. Configuration accounting: four lines added, one replaced;
application production code, test/CI implementation, and manuscript text have no
changes. OpenWrt and publication completion remain deferred; broader runtime
validation remains intentionally omitted.

### 22 September 2026 — epilogue opening aligned with part pages

The author requested a separate "Epilogue" label above "What to Take Away from
SNode.C", then clarified that both must be centered and that the label's font
size and the vertical gap must match the numbered part pages. The canonical
framework spelling is retained.

The epilogue opening now uses the existing unnumbered LaTeX part command with
the book class's `\huge` label and 20 pt vertical separation, followed by its
existing `\Huge` title. The shared part-page start and introduction formatting
remain in effect. The existing contents entry, bookmark, and label are retained;
the prose and following chapter are unchanged. This replaces the superseded
inline-break attempt without adding a new formatter or changing shared styles.

The final heading was visually compared with Part XII. PDF measurements confirm
identical label/title fonts and sizes, identical vertical positions and gap, and
centering of both lines. Only PDF page 474 (printed 452) changes. The book remains
490 pages with unchanged contents destinations, page labels, chapter starting
pages, and index. Source hygiene and alignment checks pass. The final ordinary
three-pass rebuild remains free of warnings and bad boxes.

See `review/pdf-epilogue-title-2026-09-22/REPORT.md` for measurements and build
evidence. The package-order and epilogue changes remain uncommitted after
checkpoint `cb7fce2`. All previously deferred or omitted work retains its status.

### 22 September 2026 — concluding chapter heading selected by the author

The author selected "The Principles Behind the Programs" for the chapter after
the epilogue part page. Only the heading in `manuscript/chapters/epilogue.md`
changes. The approved part-page title and formatting, all prose, and all other
manuscript inputs remain unchanged.

The ordinary three-pass rebuild retains 490 pages. Its final log has zero warnings
and zero bad boxes; the first pass has one expected label-convergence message.
The contents entry and bookmark use the new title. All 1,092 contents destinations,
page labels, chapter starting pages, and the unchanged index were checked. Only
PDF pages 12 and 475 have changed content streams. The contents, epilogue part
page, and following chapter page were rendered and visually inspected. Source
alignment against the current framework tree and source hygiene pass.

See `review/pdf-epilogue-chapter-2026-09-22/REPORT.md` and `evidence.json`.
Accounting: one manuscript heading line added and one removed; no prose,
application production code, or test/CI implementation changes. No commit was
requested or made. The established deferred and omitted scopes remain unchanged.

### 22 September 2026 — CI toolchain repair locally verified

The author authorized fixing both red workflows and using TeX Live 2026. The
publication job now pins a TeX Live 2026 container and Pandoc 3.10.1, matching the
locally verified generator. In the current SNode.C working tree, the existing
C++20 policy moves to the common project root so tests inherit it. The book's
source patch, manifest, provenance and affected anchor lines capture that exact
change; no manuscript or application/test C++ is changed. Focused compiler
regression, reconstruction and source checks pass. Full image/build/runtime
verification now passes: all three PDFs, the package rebuild/archive checks,
183 framework tests and four installed-echo tests per compiler, both companion
builds and all existing teaching/behavior/SSE/WebSocket checks. The book remains
490 pages with identical page content streams and zero warnings/bad boxes.
Independent proposal-profile warnings are recorded separately. Fresh hosted CI
runs remain pending; see `review/ci-fix-2026-09-22/REPORT.md`.

### 22 September 2026 — staged installation test environment

The first repaired hosted publication run passes with TeX Live 2026; the GCC
companion job also passes. Clang exposed an additional missing runtime search
path in the staged installed-consumer test. The author requested `LD_LIBRARY_PATH`;
the test now points it at its own temporary installation. Both complete local
framework suites pass all 183 tests with `/usr/local/lib` hidden, correcting the
initial local validation's accidental dependence on system SNode.C libraries.
The source capture includes this two-line test-support change against the
author's current HEAD `37b3a1e16de436c818eed807ee8a962f7cbbf43b`. Fresh hosted
verification of this follow-up remains pending. Application code, manuscript,
typography, and all deferred scopes remain unchanged; see the CI repair report.

### 22 September 2026 — CI repair complete on GitHub

Book commit `8497bc1ce34a79805f650e4abc4bbfa78d3fcb98` passes publication run
`35671387324` and both GCC/Clang jobs in companion run `35671387353`. TeX Live
2026 publication builds and uploads successfully; each compiler passes all 183
framework tests, four installed echo tests, and all existing companion and
runtime checks. The staged epoll loading failure is fixed by the test-local
library path. Final local source-package and PDF checks also pass, with the book
unchanged at 490 pages and zero final LaTeX warnings/bad boxes. Evidence is in
`review/ci-fix-2026-09-22/REPORT.md` and `followup-evidence.json`. Only review
records change in the closing evidence commit; no previously deferred scope is
completed or reopened by this CI repair.

## Author approval — restructure plan (Phase 4)
Approved: RESTRUCTURE-PLAN.md (commit f666e66) — 30 chapters in 11 Parts,
Appendix A, 112,250-word plan, merge boundaries, and MiniGateway milestones —
with these changes:
1. Epilogue stays a closing essay: no objectives, recap, or exercises. Its planned
   integrated-checkpoint exercise moves to new Ch. 30. Its budget stays 1,900.
2. The Ch. 24 stop rule applies to every chapter whose budget cuts more than 35%
   (new 4, 6, 12, 24, 25, 26, 27): qualify the Part rather than remove teaching
   content. A Part may draw from the 2,750-word reserve with a justification
   recorded in REPORT.md; the reserve may not go negative, and 115,000 stays hard.
3. Session 5l covers Part XI only. New session 5m covers Appendix A, the epilogue,
   back matter, and the final global audit. Proposal refresh remains Phase 6.
4. Session 5b adds a short "Lab environment" section to Ch. 2 listing optional lab
   dependencies (MQTT broker, MariaDB, TLS fixture, Bluetooth hardware) and the
   Parts that need them. Broker-, database-, and hardware-dependent labs are marked
   as equipped labs, with a local-only alternative observation where possible.
Phase 5a may start.


## Phase 5a — approved structure applied, 2026-09-22

Completed the author-approved 30-chapter, eleven-Part TOC and Appendix A, including
the merged chapter boundaries and Part XI's final architectural-judgment chapter.
Updated manuscript order, headings, Part openings, STRUCTURE, README, current
cross-references, sample inputs, and public solution paths/targets. The previous
Phase 4 gate was rerun before editing; evidence is in REPORT.md's Phase 5a section.

The operational map is
`review/proposal-readiness-2026-09-22/phase-5a-approved-structure.json`.
`ci/check-chapter-references.py` checks all 360 current references against topic
anchors and the approved map, with all 374 old occurrences accounted in the
migration register. Five regression tests include a valid-but-wrong number.
All 36 marked complete listings, 293 executable/configuration fences, 1,033 index
insertions, 18 figures, and the twelve existing lab implementation files survive
the moves. Sample objective IDs and exercises are unchanged; chapter-ledger.md
maps old 23/35/37 to current 18/28/30 and the corresponding public solutions.

Hygiene/alignment, companion build, ten labs, existing teaching/behavior/lifetime
checks, all PDF/package targets, and extracted-package hygiene pass locally.
Final PDF warnings and bad boxes are zero. Pages: proposal 6 → 6, combined samples
54 → 54, manuscript 470 → 458. Metrics: 146,210 total words, 131,744 prose,
14,466 fenced, 934 chapter subheadings, 434 text fences, 20 rules, zero forbidden
phrases/closing sections. No Part condensation or new teaching apparatus is
claimed; the epilogue essay and environment reconstruction remain unchanged.
See `metrics-after-phase-5a.json`, `phase-5a-exit-checks.json`, and cited build logs.

Author changes govern the remaining sessions: Phase 5b adds the Lab environment
section and equipped-lab labeling; the content-preservation stop rule applies to
new 4, 6, 12, 24, 25, 26, and 27. Planned words remain 112,250, reserve used 0,
reserve remaining 2,750, hard ceiling 115,000. Any later draw requires a recorded
justification and nonnegative balance. Phase 5l covers Part XI only, with current
Chapter 30 receiving the integrated checkpoint. Phase 5m covers Appendix A,
epilogue (closing essay only; budget 1,900), back matter, and final global audit.
Proposal refresh remains Phase 6; the dossier and evidence source stay at their
Phase 3 snapshot and the sample bridge explains the current numbering.

Commit: `proposal-readiness: phase 5a — apply approved teaching-book structure`.
Stop here. Next session: Phase 5b only, after rerunning the Phase 5a entry checks
listed in REPORT.md. No later Part session or Phase 6 begins in this session.


## Phase 5b — entry blocked after author seam edits, 2026-09-22

The requested Part I session stopped before editing, as required by PROMPT.md's
previous-phase re-verification gate. The author commit `author edit: fix two 5a
seam references` is preserved. Its Chapter 22 sentence now contains one Chapter
12 reference, while `phase-5a-reference-register.json` still has two occurrences
(R275 and R276). Their two intended topic anchors need to be retained on the one
surviving reference. Hygiene and the Phase 5a exit checker fail at this mismatch.

The same two author edits reduce the measured manuscript by five prose words to
146,205 total / 131,739 prose / 14,466 fenced. A gate repair must record that
post-Phase-5a baseline explicitly without overwriting the historical Phase 5a
metrics. Source alignment, measurement tests, companion build, and the already
started PDF/package targets pass; runtime labs were not run after the gate failed.
PDF counts remain 6 / 54 / 458 with clean final LaTeX logs.

Evidence: `review/proposal-readiness-2026-09-22/phase-5b-entry-results.json`,
`phase-5b-entry-hygiene.log`, `phase-5b-entry-exit.log`, and
`metrics-after-phase-5b-blocked-entry.json`; REPORT.md contains the exact gap and command results.
Only records change; Part I condensation, Lab environment guidance, exercises,
solutions, and the checkpoint remain pending. Reserve use remains zero.

Status: **blocked at entry**, not completed. Commit:
`proposal-readiness: phase 5b — record failed prerequisite check`.
Stop here. Reconcile the reference/metric gate with the author edits, then recheck
Phase 5a before retrying Phase 5b; do not revert the author's prose.


## Author-authorized seam repair and Phase 5b resumption — 2026-09-22

The author requests the register/baseline repair and then Phase 5b in this session.
R275/R276 now share the single Chapter 12 occurrence, retaining both topics and
identities. The two author seam edits (−5 prose words) establish the authorized
146,205-word entry baseline. Historical Phase 5a evidence is unchanged; fresh
metrics and all original exit assertions are recorded separately in
`review/proposal-readiness-2026-09-22/author-seam-baseline.json`,
`metrics-after-author-seam-edits.json`, and `phase-5a-author-seam-exit-checks.json`.
Hygiene/alignment, metrics tests, companion build, ten labs and all PDF/package
targets pass. Pages remain 458 / 54 / 6, with zero final warnings/bad boxes.
REPORT.md cites every command log and explains the historical-checker wrapper.
No manuscript prose changed for this repair. The earlier entry failure remains
in the chronological record; its gate is now passed.

Separate commit: `proposal-readiness: reconcile 5a register with author seam edits`.
Next, execute Phase 5b only: Part I and its approved front-matter work.


## Phase 5b — Part I and front matter completed, 2026-09-22

The author-requested seam repair was committed separately first, with all Phase
5a checks passing and the authorized −5-word baseline recorded. Part I then met
its approved budgets and teaching requirements: Chapter 1 remains 1,821 words;
Chapter 2 is 3,006 (eight sections), Chapter 3 is 2,568; total 7,395 / 7,850.
Mean section prose is 327.00 / 331.50 / 321.83. Front matter is 1,981 / 2,500.
The two samples retain their original ≥20% prose reductions. No reserve is used;
2,750 words remain available under the existing author-approved stop rules.

Chapter 2 has three objectives, one recap, and five mapped exercises, including
two independently built/run external-consumer labs. Its Lab environment section
lists MQTT broker, MariaDB, TLS fixture and Bluetooth dependencies by Part,
identifies equipped labs and explains the narrower local alternatives. Every
Part I chapter now has public answers and complete objective↔exercise coverage.
Chapter 3's existing greeting lab is the mapped Part I checkpoint: independent
measurement peers reflect exact bytes, including invalid input, without implying
acceptance. The canonical EchoPair remains the sole application implementation.
Later equipped labs remain for the corresponding Part sessions.

All twelve public labs, hygiene/alignment, metrics/reference regressions,
companion builds, teaching/behavior/lifetime checks, full PDF/package targets,
archive identity checks and extracted-package hygiene pass locally. Final PDF
warnings and bad boxes are zero. Pages: full 458 → 454, samples 54 → 54, proposal
6 → 6. Edited text and public solutions were reread; targeted rendered-page review
is recorded separately. An initial help-exit test assumption and the subsequent
bounded-exchange correction are documented without discarding the failure log.

Full counts: 145,973 words, 926 chapter subheadings, 429 text fences, 20 rules,
zero forbidden phrases/closing sections. Remaining global reductions are for
later Parts. Evidence under `review/proposal-readiness-2026-09-22/`: REPORT.md,
chapter-ledger.md, metrics-after-phase-5b.json, phase-5b-exit-checks.json,
phase-5b-final-*.log, phase-5b-visual-review.md. The blocked entry snapshot is
preserved as metrics-after-phase-5b-blocked-entry.json; historical Phase 5a evidence
is unchanged except the explicitly current reference register.

Commit: `proposal-readiness: phase 5b — refine Part I and establish the measurement checkpoint`.
**Stop after Phase 5b.** Next session: Phase 5c (Part II only), first rerunning the
current Phase 5b gate listed in REPORT.md. Author-approved content-preservation
stop rules, reserve accounting, 5l/5m split and Phase 6 proposal refresh still apply.


## Phase 5c — Part II completed, 2026-09-22

Freshly reran the Phase 5b metrics, all exit assertions, twelve labs, companion and
runtime checks, PDF/package targets and extracted-package hygiene before editing.
All passed; historical evidence remains unchanged. Part II now meets its budgets:
Chapter 4 is 4,338 / 5,300 words with fourteen sections, Chapter 5 is 2,983 / 3,700
with ten. Mean section prose is 294.50 and 278.10; total 7,321 / 9,000. The Chapter
4 content-preservation stop rule is satisfied: substantive explanations remain,
with the retained-topic audit in chapter-ledger.md. No reserve used; 2,750 remains.

Both chapters have three objectives, one five-bullet recap, two review questions,
two labs and one design problem, complete mappings and public solutions. The
Part II checkpoint reuses the canonical measurement model: incoming sequence
numbers 900,2,1 become accepted order 1,2,3; removing one observer between calls
leaves the other receiving new values. This is explicitly a model experiment.
A separate new public-API lab observes deferred callback execution and lifetime;
the other three labs reuse existing model/peer test implementations. No duplicate
application owner or protocol implementation was added.

All sixteen public labs, hygiene/alignment, metrics/reference regressions,
companion build, teaching/behavior/lifetime checks, PDF/package builds, archive
identity and extracted-package hygiene pass locally. Full PDF pages: 454 → 438;
samples remain 54 and proposal 6. Final warnings/bad boxes: zero. The book's existing
ragged-bottom setting was moved into its preamble to fix a contents-page underfull
box without diagnostic suppression; no front-matter prose changed. Both chapters,
solutions and transitions were reread, and all Part II rendered pages plus the
contents were inspected. Initial configuration/layout failures remain documented.

Full counts: 140,336 words, 848 chapter subheadings, 399 text fences, 20 rules,
zero forbidden phrases/closing sections. All executable listings, figure/index
markers and existing sample reductions remain. Evidence under
`review/proposal-readiness-2026-09-22/`: REPORT.md, chapter-ledger.md,
metrics-after-phase-5c.json, check-phase-5c.py, phase-5c-exit-checks.json,
phase-5c-entry-*.log, phase-5c-final-*.log and phase-5c-visual-review.md.

Commit: `proposal-readiness: phase 5c — condense Part II and teach shared measurement ownership`.
**Stop after Phase 5c.** Next: Phase 5d (Part III only), after rerunning the current
Phase 5c gate listed in REPORT.md. Author-approved stop rules, reserve accounting,
5l/5m split and Phase 6 proposal refresh still apply.


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

After the separately committed author-requested Phase 5c follow-up, its fresh exit
checks, sixteen labs and full build/runtime/package checks passed before Part III
editing. The authorized baseline is `metrics-after-phase-5c-follow-up.json`.
Historical Phase 5c evidence remains unchanged.

Chapters 6–8 now meet their budgets: 4,168 / 5,200; 3,084 / 3,650; 2,170 / 2,200
words. They have 12, 9 and 5 sections, respectively, with mean section prose of
319.25, 324.67 and 393.40. Part III totals 9,422 / 11,050 words. The Chapter 6
content-preservation stop rule is satisfied; its retained-topic audit is in
chapter-ledger.md. Every original C++ excerpt, index occurrence and figure remains.
No reserve used; 2,750 remains.

Each chapter has three objectives, one five-bullet recap and five mapped exercises
(two review, two labs, one design), with public answers. One thin family driver
reuses the canonical EchoPair context/factory for five carriers; earlier peer and
occupied-port fixtures are reused unchanged. The Part III checkpoint observes
identical bytes over loopback IP and a private Unix path, opposite endpoint
identities and owned-path cleanup before fixture cleanup. Bluetooth selector
configuration is tested without radio hardware. Optional RFCOMM/L2CAP drivers
build; the public equipped RFCOMM procedure was not run and radio delivery remains
unverified. No existing application implementation changed.

All 22 public labs, hygiene/alignment, metrics/reference regressions, companion
build, teaching/behavior/lifetime checks, PDF/package builds, archive identity
and extracted-package hygiene pass locally. Final LaTeX warnings/bad boxes: zero.
Pages: full 436 → 418; samples 54 and proposal 6 unchanged. Chapters, solutions
and transitions were reread; targeted rendered pages were visually inspected.
The initial component, test-assumption and layout failures remain documented.

Whole-book counts: 133,986 words (−6,087), 753 chapter subheadings (−94), 348 text
fences (−51), 20 rules and zero forbidden phrases/closing sections. Later Parts
still owe the global reductions. Front matter remains within 2,500 words and all
Part openers within 1,650. The reference register preserves all migration identities
and stable topics, with explicit dispositions for removed framing references.

Evidence in `review/proposal-readiness-2026-09-22/`: REPORT.md, chapter-ledger.md,
metrics-after-phase-5d.json, check-phase-5d.py, phase-5d-exit-checks.json,
phase-5d-final-results.json, phase-5d-final-*.log and phase-5d-visual-review.md.
Commit: `proposal-readiness: phase 5d — refine Part III and verify endpoint-family labs`.
**Stop after Phase 5d.** Next is Phase 5e (Part IV only), after freshly rerunning
the current Phase 5d gate in REPORT.md. Author-approved preservation stop rules,
reserve accounting, 5l/5m split and Phase 6 proposal refresh still apply.


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

The separately committed author-requested Phase 5d follow-up passed a fresh gate
before Part IV edits, including all 22 previous labs and full checks/builds. Its
metrics are the authorized entry baseline. Historical Phase 5d evidence remains.
The author's clarification governs the editorial pass: budgets are ceilings;
remove repetition without removing explanations, examples or qualifications merely
to undershoot. The retained-content audit is in chapter-ledger.md.

Chapters 9–11 meet their ceilings at 3,089 / 3,200; 2,265 / 2,800; 2,555 / 2,800
words. They have 8, 6 and 7 sections, with mean prose lengths 345.75, 328.33 and
312.57. Part IV is 7,909 / 8,800 words including all pedagogical apparatus.
No reserve used; 2,750 remains. All executable excerpts, index entries, figures
and stable topic anchors survive. Three objectives per chapter map to five
exercises (two review, two labs, one design), with public solutions and recaps.

The Part IV checkpoint runs the canonical line protocol over IPv4 and a private
Unix path, comparing reconstructed replies under fragmented/coalesced writes.
Other labs cover length admission, fresh parser state, construction refusal and
endpoint-versus-command failure. One test-only refusing factory delegates normal
creation to the existing factory; the Unix entry point is derived from the worked
carrier substitutions. No application or parallel parser implementation was added.
The observed immediate-close behavior is now explicit: a queued error diagnostic
is not guaranteed to arrive. The initial incorrect delivery assertion remains
recorded with its correction; no production change was required.

All 28 public labs, companion build, hygiene/alignment, metric/reference regressions,
teaching/behavior/lifetime checks, PDF/package builds, archive consistency and
extracted-package hygiene pass locally. Full PDF: 418 → 406 pages; samples 54 and
proposal 6 unchanged. Final warnings and bad boxes: zero. Text/solutions were
reread in context, and 27 rendered pages were inspected. No hosted CI or further
carrier/security behavior is claimed. Proposal refresh remains Phase 6.

Global counts: 130,160 words (−3,833), 691 subheadings (−62), 323 text fences (−25),
20 rules and zero forbidden phrases/closing sections. Remaining global reductions
belong to later Parts. Front matter stays within 2,500 words and all Part openers
within 1,650. Evidence in `review/proposal-readiness-2026-09-22/`: REPORT.md,
chapter-ledger.md, metrics-after-phase-5e.json, check-phase-5e.py,
phase-5e-exit-checks.json, phase-5e-final-results.json, phase-5e-final-*.log and
phase-5e-visual-review.md.

Commit: `proposal-readiness: phase 5e — refine Part IV and verify protocol framing`.
**Stop after Phase 5e.** Next: Phase 5f, Part V only, after freshly rerunning the
current Phase 5e gate in REPORT.md. Author preservation rules, reserve accounting,
5l/5m split and Phase 6 proposal refresh still apply.


## Phase 5f — Part V completed, 2026-09-22

Freshly reran the Phase 5e entry gate before editing: exact metric equality,
Part IV budgets/pedagogy, reference and preservation checks, all 28 existing labs,
companion/runtime checks and clean publication builds. New evidence is in
REPORT.md’s Phase 5f entry account and `phase-5f-entry-*`; prior evidence remains
historical and unchanged.

Edited and reread Chapters 12–13 and the Part V opener. Configuration’s repeated
merged introductions/catalogues are consolidated around the existing echo
precedence experiment. Diagnostics retains its scope, lifetime, error, frozen-policy
and output qualifications while tightening framing. Every executable/configuration
fence, marked complete listing, index occurrence and figure remains unchanged.
The recorded author instruction applies: budgets are ceilings, not targets;
explanations, examples and technical qualifications were not cut merely to fit.
Chapter 12’s preservation stop rule is accounted for by the ledger’s topic audit.

| Chapter | Final words / ceiling | Headings / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| 12 | 4,273 / 5,400 | 10 / 16 | 391.20 |
| 13 | 2,698 / 2,750 | 7 / 7 | 340.43 |

Part V: **6,971 / 8,150**. Reserve remains **2,750**, none used. Both chapters have
three objectives, a five-bullet recap, two review questions, two labs and one design
problem, with complete objective↔exercise mappings and public solutions. The Part V
checkpoint checks reproducible endpoint selection and scoped runtime diagnostics
using canonical EchoPair and SemanticLogging, without introducing another app.

All 32 public labs pass, including four new registrations. Hygiene/reference
regression, alignment, metrics tests, companion build, teaching/behavior/lifetime,
PDF/proposal/sample/package and extracted-package checks pass. Runtime reparse,
live listener replacement and deployment behavior are explained, not newly exercised.
Production code growth is zero; the requested lab/test support is +119 net lines.

Full PDF: **392 pages** (was 406), zero warnings/bad boxes; samples 54, proposal 6.
Targeted rendered pages were reviewed, including objectives/recaps/exercises, both
figures and preserved listings. Final metrics, hashes and checks are in
`metrics-after-phase-5f.json`, `phase-5f-exit-checks.json` and REPORT.md. Whole book:
**124,770 words, 615 deep headings, 298 text fences**; final global targets remain
pending. The reference checker covers 326 current occurrences and all 374 old
migration identities; retirements in this Part are explicitly justified.

**Stop after Phase 5f.** Next: Phase 5g, Part VI only, after freshly rerunning this
phase’s exit criteria with new evidence. Author preservation rules, reserve
accounting, 5l/5m split and Phase 6 proposal refresh remain in force.


## Phase 5g — Part VI completed, 2026-09-22

Re-executed the Phase 5f gate before editing, with exact fresh metric equality,
all 32 existing labs, required runtime checks and clean publication builds.
Historical evidence remains unchanged; `phase-5g-entry-*` and REPORT.md record
the new verification. The author instruction remains controlling: budgets are
ceilings, not targets; remove repetition while preserving explanations, examples
and technical qualifications.

Edited and reread Chapters 14–15, the Part VI opener and public solutions. Repeated
layer summaries and lifecycle definitions are consolidated. The ledger records
preservation of trust/name/SNI, early SSL policy, bounded shutdown, flow ownership,
retry/count/jitter policy, queue admission, deadlines and replay uncertainty.
Every executable/configuration fence, marked listing, index occurrence and figure
remains unchanged; chapter structure and production formatting are unchanged.

| Chapter | Final words / ceiling | Headings / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| 14 | 2,576 / 2,950 | 8 / 8 | 292.62 |
| 15 | 2,990 / 3,400 | 8 / 9 | 339.88 |

Part VI: **5,566 / 6,350**; reserve **2,750 remaining**, none used. Three objectives
per chapter map to five exercises (two review, two labs, one design); each closes
with five recap bullets. All solutions are public under `companion/exercises/ch14`
and `ch15`. The checkpoint distinguishes three TLS identity outcomes from controlled
retry/reconnect observations. It prepares MiniGateway uplink diagnostics without
claiming application delivery from restored connectivity.

All 36 public labs, companion build, hygiene/reference regression, source alignment,
metrics tests, teaching/behavior/lifetime checks and PDF/package targets pass.
Final full PDF **382 pages** (was 392), samples 54 and proposal 6; zero warnings and
bad boxes. Nineteen affected/contents pages were visually reviewed. Existing TLS
policy and EchoPair implementations are reused; production growth is zero and
public test support is +170 net lines. Initial fixture-option and local runtime
lookup failures are retained with corrected passing evidence. No hosted CI or
production deployment is claimed.

Book-wide counts: **122,049 words, 573 deep headings, 273 text fences**, 20 rules,
zero forbidden phrases/closing sections. Global targets remain pending. Front
matter is 1,980 / 2,500 and Part openers 1,218 / 1,650. The five sample gates survive.
Evidence: REPORT.md, chapter-ledger.md, metrics-after-phase-5g.json,
check-phase-5g.py, phase-5g-exit-checks.json, phase-5g-final-results.json,
phase-5g-final-*.log and phase-5g-visual-review.md, all under
`review/proposal-readiness-2026-09-22/`.

Commit: `proposal-readiness: phase 5g — refine Part VI and verify secure recovery outcomes`.
**Stop after Phase 5g.** Next: Phase 5h, Part VII only, after freshly rerunning this
phase's exit gate using the final logs' selected runtime environment. Preservation
rules, reserve accounting, the 5l/5m split and Phase 6 proposal refresh remain in force.


## Author-requested Phase 5g follow-up — companion TLS fixture, 2026-09-22

The author requires the TLS trust/identity lab to be public companion material.
Moved both unchanged fixture files into `companion/exercises/ch14/`, updated its
existing lab registration and runner, and redirected the current review target to
that single implementation. Chapter 14 now points directly to the companion fixture
and shows the ordinary lab build/test commands. Its public solution was updated.
Three trust/name outcomes and the early null-SSL check remain intact.

All Phase 5g exit checks, all 36 labs and the existing review consumer pass; final
PDFs remain 382/54/6 pages with zero warnings/bad boxes. The changed page was
rendered and inspected. Chapter 14 is 2,579 words; Part VI 5,569 / 6,350; whole book
122,052 (+3). No reserve used. No production/test logic growth; the fixture move
is exact and wiring is line-neutral. REPORT.md and `phase-5g-follow-up-*` record
fresh evidence; historical Phase 5g evidence is unchanged.

Separate commit: `proposal-readiness: phase 5g follow-up — move TLS fixture into companion material`.
The authorized Phase 5h entry baseline is `metrics-after-phase-5g-follow-up.json`;
`check-phase-5g-follow-up.py` supplies the current gate. Continue with Part VII only,
keeping budgets as ceilings and preserving technical teaching. Stop after Phase 5h.


## Phase 5h — Part VII completed, 2026-09-22

Entered after the separately committed author-requested companion TLS-fixture
follow-up freshly reran the Phase 5g exit gate. Its authorized metrics baseline
is `metrics-after-phase-5g-follow-up.json`; original Phase 5g evidence is historical.

Edited and reread Chapters 16, 17 and 19 and the Part VII opener. Reread Chapter 18
and kept it unchanged: its teaching apparatus and detailed SSE treatment already
meet the gates. Budgets were ceilings; repetitions and restated layer diagrams
were removed while parser/streaming policy, dispatch lifetimes, deployment and
WebSocket resource qualifications remain. Every executable/configuration fence,
marked listing, index entry and figure is preserved. No structural or formatting
change was required. The ledger supplies a source-line content audit.

| Chapter | Words before → after / ceiling | Prose before → after | Fenced words before → after | Deep headings before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: |
| 16 | 3,514 → 2,471 / 2,600 | 3,124 → 2,305 | 390 → 166 | 24 → 6 / 6 | 368.17 |
| 17 | 3,059 → 2,065 / 2,350 | 2,806 → 1,999 | 253 → 66 | 26 → 5 / 5 | 382.80 |
| 18 | 3,269 → 3,269 / 3,300 | 2,898 → 2,898 | 371 → 371 | 7 → 7 / 7 | 398.00 |
| 19 | 3,983 → 3,000 / 3,050 | 3,432 → 2,638 | 551 → 362 | 23 → 7 / 7 | 363.14 |

Part VII: **10,805 / 11,300**; reserve **2,750 remains**, none used. Three objectives
per chapter map completely to two review questions, two public labs and one design
problem. Each chapter closes with five recap bullets and the exercises. Six new
registrations bring the public suite to **42/42 passing**. The checkpoint observes
two accepted SSE measurements and independent subscriber lifetime, then separately
checks WebSocket negotiation and typed/fragmented messages, ping and close.

HTTP/Express labs share one synchronous route fixture. WebSocket labs compile
canonical echo sources and generate linked-factory mains; the existing dynamic
lifetime test shares the same unchanged wire assertions. Production growth is zero;
requested test support is +278/−68 lines (net +210). No second parser, routing
engine, echo algorithm or application state store was added.

Hygiene/reference regression, listing alignment, measurement tests, installed
companion build, all labs, teaching/behavior/lifetime, PDF/proposal/sample/package
and extracted-package checks pass. Initial component-import, Python-import and
invocation-environment failures are retained with their corrections in REPORT.md.
Local loopback behavior is verified; hosted CI and deployment TLS are not claimed.

Full PDF: **368 pages** (was 382), samples 54, proposal 6; zero final warnings and
bad boxes. Complete affected Part, transition and contents pages were rendered
and visually checked; layout corrections were prose-only. Final metrics, artifact
hashes and the 336-file package equality check are in `metrics-after-phase-5h.json`,
`phase-5h-exit-checks.json`, `phase-5h-final-results.json` and REPORT.md.

Whole book: **119,068 words**, 518 deep headings, 229 text fences, 20 rules and
zero forbidden/closing hits. The final word and global section-density targets
and remaining chapter pedagogy are still pending. Front matter is 1,980 / 2,500;
Part openers 1,254 / 1,650. Sample gates remain valid. The reference register covers
319 current occurrences, 39 stable topics and all 374 old migration dispositions.

Commit: `proposal-readiness: phase 5h — refine Part VII and verify web protocol boundaries`.
**Stop after Phase 5h.** Next is Phase 5i, Part VIII only, after freshly rerunning
this gate with the recorded installation/runtime environment. Author preservation
rules, reserve accounting, the 5l/5m split and Phase 6 proposal refresh remain in force.


## Phase 5i — Part VIII completed, 2026-09-22

The Phase 5h entry gate was freshly rerun before editing: exact metrics agreement,
all 42 prior labs, all other checks and clean PDF/package builds. Historical
Phase 5h evidence is unchanged; `phase-5i-entry-*` supplies fresh evidence.

Edited and reread Chapters 20–22, public solutions and the Part VIII opener.
Budgets were ceilings: removed duplicated stacks, comparisons and framing while
retaining packet/carrier mechanics, all executable examples, component fragments,
costs, lifetimes and partial-failure qualifications. The ledger contains the
source-line preservation audit; all index entries, figures and source markers
are mechanically preserved. No structural or production-formatting changes.

| Chapter | Words before → after / ceiling | Prose before → after | Fenced words before → after | Deep headings before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: |
| 20 | 2,997 → 2,005 / 2,350 | 2,709 → 1,878 | 288 → 127 | 22 → 5 / 5 | 359.60 |
| 21 | 2,731 → 1,782 / 2,100 | 2,353 → 1,716 | 378 → 66 | 17 → 4 / 4 | 409.25 |
| 22 | 3,964 → 2,922 / 2,950 | 3,780 → 2,899 | 184 → 23 | 24 → 8 / 8 | 348.50 |

Part VIII: **6,709 / 7,400**. Reserve used **0**, remaining **2,750**. Each chapter
has three objectives, five recap bullets and five exercises (two review, two labs,
one design), with full bidirectional mapping and public solutions. Six new test
registrations bring the suite to **48/48 passing**. The Part checkpoint distinguishes
real local broker/subscriber delivery from a separate MiniGateway outage test that
keeps accepted HTTP/status/SSE state observable. Broker labs are marked equipped;
packet-peer and outage observations provide local alternatives.

Native launchers and the WebSocket factory reuse installed MQTT and canonical
SensorClient ownership; the outage lab reuses the unchanged gateway and observer.
Production growth is zero; requested fixture/test support is +300/−2 lines, net
+298. One normalized configure dependency registration serves both generated
WebSocket consumers. Initial dependency, lambda conversion and test-header parsing
failures are retained with their corrections in REPORT.md.

All hygiene/reference, listing alignment, metric regression, companion/lab builds,
48 labs, teaching/behavior/lifetime, PDF/proposal/sample/package and extracted
package checks pass. These are local installed-package/loopback observations;
third-party interoperability, hosted CI, deployment TLS, persistence and reconnect
replay are not newly claimed.

Full PDF **358 pages**, down from 368; samples 54, proposal 6; zero warnings/bad
boxes. Complete Part VIII, next transition and relevant contents pages were
rendered and visually checked. Evidence: `metrics-after-phase-5i.json`,
`phase-5i-exit-checks.json`, `phase-5i-final-results.json`, `phase-5i-final-*.log`,
`phase-5i-visual-review.md`, REPORT.md and chapter-ledger.md under
`review/proposal-readiness-2026-09-22/`.

Whole book **116,122 words**, 472 deep headings, 192 text fences, 20 rules, zero
forbidden/closing hits. The final word/density targets and remaining chapter
pedagogy are pending. Front matter **1,980 / 2,500**; Part openers **1,291 / 1,650**.
The five sample gates remain valid. The reference register covers 309 current
occurrences, 39 topics and all 374 original dispositions; R275/R276 retain both
author seam topic targets and identities.

Commit: `proposal-readiness: phase 5i — refine Part VIII and verify MQTT delivery boundaries`.

**Stop after Phase 5i.** Next is Phase 5j, Part IX only, after freshly rerunning
this gate with the recorded installation/runtime setup. Author preservation rules,
reserve accounting, the 5l/5m split and Phase 6 proposal refresh remain in force.


## Phase 5j — Part IX completed, 2026-09-22

The Phase 5i exit gate was freshly rerun before editing: exact metrics agreement,
48/48 prior labs, all ten check groups and clean PDF/package builds. Historical
evidence remains unchanged; `phase-5j-entry-*` supplies the fresh gate.

Edited and reread Chapters 23–24, public solutions and the Part IX opener. Budgets
were ceilings: removed repeated component/role explanations, stacks and summary
endorsements. Preserved all executable examples, dependency graph, figures, index
entries, source markers, transaction ordering and partial-failure qualifications.
Chapter 24 satisfies the preservation stop rule; the ledger records its source-line
audit. No reserve used; **2,750 remains**.

| Chapter | Words before → after / ceiling | Prose before → after | Fenced words before → after | Deep headings before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: |
| 23 | 5,197 → 3,826 / 3,900 | 4,697 → 3,460 | 500 → 366 | 31 → 10 / 10 | 334.80 |
| 24 | 10,556 → 5,591 / 6,200 | 9,518 → 5,329 | 1,038 → 262 | 70 → 17 / 17 | 304.35 |

Part IX: **9,417 / 10,100**. Both chapters have three objectives, five recap bullets
and five exercises (two review, two labs, one design), mapped both ways with public
answers. Four new registrations bring the suite to **52/52 passing**. Equipped
MariaDB labs independently read autocommitted state after client exit/restart and
observe SQL error with a still-usable connection. The Part checkpoint contrasts
that with MiniGateway's in-memory restart, then applies the public raw/projection
outcome map. It does not claim server crash recovery or an MQTTStore deployment.

The lab derives its client from the unchanged canonical example; HTTP and gateway
observers are reused. Production growth is zero; lab/test/CI support is +156/−3,
net +153. CI installs database tools. A reference regression now checks complete
registration instead of an obsolete count floor and rejects missing migration
identities. Host database signal/space failures were resolved with author cleanup,
bounded fixture storage and SQL SHUTDOWN; no private servers remain. REPORT.md
retains the failed attempts and final execution evidence.

All hygiene/reference, alignment, measurement, installed companion/lab, teaching,
behavior/lifetime, PDF/proposal/sample/package and extracted-package checks pass.
Full PDF **338 pages**, down from 358; samples 54 and proposal 6, all with zero
warnings/bad boxes. Complete affected Part, contents and transition pages were
rendered and inspected. Final metrics, artifact hashes and 352-file package check
are in `metrics-after-phase-5j.json`, `phase-5j-exit-checks.json`,
`phase-5j-final-results.json`, REPORT.md and chapter-ledger.md.

Whole book **109,822 words**, 398 deep headings, 136 text fences, 20 rules and zero
forbidden/closing hits. Mean section prose 229.58 and remaining chapter pedagogy
still require the later phases/global audit. Front matter **1,980 / 2,500**; Part
openers **1,327 / 1,650**. All five sample gates remain valid. The register covers
298 current references, 39 topics and all 374 original dispositions, including
the author's combined seam identities and topic targets.

Commit: `proposal-readiness: phase 5j — refine Part IX and verify persistence boundaries`.
**Stop after Phase 5j.** Next is Phase 5k, Part X only, after freshly rerunning this
gate with the recorded environment. Preservation stop rules, reserve accounting,
the 5l/5m split and Phase 6 proposal refresh remain in force.


## Phase 5k — Part X completed, 2026-09-22

Freshly reran the Phase 5j exit gate before editing: ten groups and 52 labs pass,
metrics reproduce exactly and prior preservation, chapter, PDF and package gates
hold (`phase-5k-entry-results.json`, `phase-5k-entry-exit-checks.json`). Historical
Phase 5j records are unchanged.

Edited and reread Chapters 25–27, their public solutions and the Part X opener.
Repeated component/include framing, deployment catalogues and testing endorsements
are condensed. The complete component graph/header matrix, Linux/OpenWrt worked
paths, test taxonomy, sanitizer qualifications, regression recipe and bounded
measurement remain. The chapter ledger records a source-line preservation audit
for all three chapters subject to the author's stop rule.

| Chapter | Words / ceiling | Deep headings / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| 25 | 3,903 / 4,100 | 10 / 10 | 328.00 |
| 26 | 3,596 / 3,700 | 10 / 10 | 327.30 |
| 27 | 4,169 / 4,200 | 10 / 10 | 376.60 |

**Reserve draw: 400 to Chapter 27**, raising its original 3,800 ceiling to 4,200
so concrete test distinctions and benchmark/sanitizer limits remain intact.
REPORT.md records the justification. Part X is **11,668 / 12,000**; planned total
**112,650**, reserve **2,350 remaining**, hard ceiling **115,000**. Other budgets
remain ceilings; they are not invitations to remove useful teaching.

Each chapter has three objectives, five recap bullets and five mapped exercises
(two review, two labs, one design). All public answers and expected observations
are in `companion/exercises/ch25`–`ch27`; mappings run both ways in the ledger.
The Part X checkpoint builds and installs the canonical consumer, distinguishes
component failure from endpoint refusal and records 200 exact-payload samples.
One shared driver owns temporary installation and observations; previous consumer
labs and the printed Python calculation are reused. Production code growth is
zero; fixture/registration/alignment support is +174/−3, net +171 lines.

All **58 public labs**, teaching/behavior/lifetime checks, hygiene/reference
regressions, source alignment, metric tests, companion builds and full PDF/package
builds pass locally (`phase-5k-final-results.json` and cited logs in REPORT.md).
The 37th exact source marker covers the unchanged Python benchmark; a negative
mutation check confirms mismatch rejection. All 293 executable/configuration
fences, index entries, figure IDs and prior markers are preserved. No private
fixture servers remain after the run. Hosted CI, actual systemd/procd deployment,
OpenWrt SDK execution, ASan execution and production load are not newly verified.

Full PDF **338 → 322 pages**, sample **54**, proposal **6**, all with zero final
warnings and bad boxes. All 360 package files match working sources. The full
Part, contents and next transition were rendered and visually reviewed; see
`phase-5k-visual-review.md`. A long-name paragraph and two literal Markdown
headings were corrected; the phase checker now checks Pandoc heading recognition.
No production styles changed. Proposal-source refresh stays in Phase 6.

Whole manuscript **109,822 → 103,934 words**, deep chapter headings **398 → 307**,
mean section prose **229.58 → 281.20**, text fences **136 → 97**, rules **20**,
forbidden/closing hits **0**. Front matter **1,980 / 2,500**; Part openers
**1,362 / 1,650**. These numerical thresholds are currently met; remaining
pedagogy and the final global audit are not complete. References: 294 current
occurrences, 39 topics, all 374 migration dispositions, author seam identities
and targets retained (`phase-5k-reference-audit.md`).

Commit: `proposal-readiness: phase 5k — refine Part X and verify installed consumers`.
**Stop after Phase 5k.** Next is Phase 5l, Part XI only, after freshly rerunning
this gate with the logged environment. Then 5m covers Appendix A, closing material
and the global audit; Phase 6 refreshes the proposal. Preserve the remaining
2,350-word reserve and all author teaching-content stop rules.


## Phase 5l — blocked at the previous-phase entry gate, 2026-09-22

Fresh execution of the Phase 5k gate gives **55/58 public labs passing**.
`exercise-ch23-durable`, `exercise-ch23-error` and
`exercise-ch24-part-checkpoint` fail the existing minimum **512 MiB free temporary
space** prerequisite before database initialization. `/tmp` had about 467 MiB
free in the recorded post-check observation. Evidence:
`review/proposal-readiness-2026-09-22/phase-5l-entry-labs.log:543`, `:575`, `:615`,
`phase-5l-entry-results.json` and `phase-5l-entry-exit-checks.json`.

The other nine check groups pass, including companion/PDF/package builds,
hygiene, alignment and teaching/behavior/lifetime execution. Metrics reproduce
Phase 5k exactly: **103,934 words**, delta zero. The unchanged Phase 5k checker,
redirected in memory to fresh entry logs, passes its static and preservation
checks before rejecting the failed lab group. PDFs remain **322 / 54 / 6 pages**
with zero final warnings/bad boxes; 360 package files match their source inputs.
See the detailed blocked account in REPORT.md and `metrics-after-phase-5l.json`.

No manuscript, companion, CI or production files were edited. Part XI editorial
work, its chapter ledger and the 2,350-word reserve remain unchanged. Historical
Phase 5k completion evidence is preserved. Per the explicit phase-entry rule,
**stop here**; do not begin Phase 5l implementation, 5m or 6. Restore sufficient
temporary capacity (or select a sufficiently sized temporary directory) and
rerun the entry gate before retrying Phase 5l. No cleanup or weakened check was
applied in this session.

Commit: `proposal-readiness: phase 5l — record blocked prerequisite gate`.


### Author execution constraint and Phase 5l workspace retry, 2026-09-22

Author instruction: “Continue and do not use /tmp for anything - i took back full
access - just workspace access ...”. From that instruction onward, temporary
files and test data use workspace `build/t`; `TMPDIR`, `TMP`, `TEMP` and the behavior
smoke test's Unix-socket override are set accordingly. Keep this constraint for
future runs. The preceding temporary-space blocker is superseded by the following
fresh evidence; the earlier attempt remains recorded as history.

The restricted attempt could not create local sockets. A scoped retry with socket
access, still using workspace-only files, passes **55/58 labs and the other nine
check groups**. The three database labs pass the space prerequisite but fail to
create files inside their private workspace data directories (Errcode 13,
Permission denied). Evidence: `phase-5l-workspace-permitted-entry-labs.log:580–581`,
`:684–685`, `:796–797`, `phase-5l-workspace-permitted-entry-results.json`, and
`phase-5l-workspace-permitted-entry-exit-checks.json` in the current review folder.
The workspace temporary directory is empty after cleanup. The saved
`run-phase-5l-entry-checks.py` reproduces the workspace-only environment.

The MariaDB host profile is consistent with this restriction, but the exact policy
decision was not established from kernel logs. No host policy, system service or
framework was modified. The remaining prerequisite is permission for the database
server to initialize its private data under the workspace. Do not skip that test,
move data outside the workspace or weaken confinement to claim completion.

Phase 5l remains **blocked before Part XI edits**. Metrics are unchanged at
103,934 words; PDFs remain 322 / 54 / 6 pages with zero warnings/bad boxes. The
historical Phase 5k evidence, ledger and 2,350-word reserve are unchanged. The
latest REPORT.md retry account supersedes the earlier temporary-space handoff.
Commit: `proposal-readiness: phase 5l — record blocked prerequisite gate`.


### Phase 5l — full access restored; temporary files remain in workspace

Author instruction: “OK, you get again full access - but never use /tmp for
temporary files - only work in workspace as long as possible!”

The focused database retry still fails. Kernel evidence now confirms AppArmor's
`mariadbd` profile denies file creation in the private workspace data directory
(`phase-5l-workspace-apparmor-denial.log`). A two-rule owner-only exception for
workspace `build/t/book-db-*` is prepared and syntax-checked; installation into
`/etc/apparmor.d/local/mariadbd` and profile reload await the author's specific
approval. No host policy change or Part XI edit has yet been made. Keep the
workspace-only temporary environment in all subsequent checks and rerun the full
entry gate before beginning Phase 5l implementation.


### Author execution constraint revised — `/tmp` authorized again

The author directed: “No, not with apparmor - /tmp now has plenty of space. Use it
again!” This supersedes the preceding temporary-directory restriction and withdraws
the pending AppArmor proposal. No host policy was installed or reloaded. Temporary
fixtures may again use `/tmp`; scripts and review evidence remain in the workspace.
The fresh `phase-5l-restored-entry-*` run passes all ten groups and 58 labs, then the
unaltered Phase 5k checker passes against those fresh logs. Phase 5k metrics reproduce
exactly; the historical blocked attempts remain evidence, not the active handoff.
Phase 5l Part XI editing may proceed under the approved scope and budgets.


## Phase 5l — Part XI completed, 2026-09-23

The latest author instruction restores `/tmp` use and rejects an AppArmor change.
No host policy was modified. After restoring the temporary fixture path, all ten
Phase 5k entry groups and 58 labs pass; the unchanged checker confirms the exact
baseline, preservation, chapter and artifact gates (`phase-5l-restored-entry-*`).
Earlier blocked attempts remain historical evidence, superseded by this completed
phase. The runner `run-phase-5l-restored-checks.py` records the active environment.

Edited and reread Chapters 28–30, the Part XI opener and relevant public answers.
Ch29 consolidates nineteen headings into six connected sections, removes repeated
arrow chains/endorsements and moves full parsing/sequence qualifications beside
the source. The comparison table, figure, complete listings, diagnostic walkthrough
and deployment limitations remain. Ch28 keeps its build order and all source;
Ch30 keeps every decision table and applied rule while trimming restated framing.

| Chapter | Words / ceiling | Deep headings / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| 28 | 3,818 / 3,850 | 6 / 6 | 291.50 |
| 29 | 2,541 / 3,150 | 6 / 6 | 279.50 |
| 30 | 1,850 / 1,900 | 6 / 6 | 287.00 |

Part XI **8,209 / 8,900 words**. No reserve draw; **2,350 remains**. Each chapter
has three objectives, one recap and five exercises with all three tiers. The
ledger records both mapping directions and public solutions. Ch29's two new labs
use the unchanged extended gateway: valid/invalid/fragmented/bounded CSV, shared
HTTP/Unix acceptance with MQTT unavailable, SSE disconnect/reconnect and restart.
Ch30's approved integrated checkpoint reuses six Part XI tests, followed by the
process-boundary design discussion. No duplicate application implementation.

All **60 public labs** and the nine other check groups pass; the public checkpoint
target builds. Source/reference/preservation checks retain 293 executable/config
fences, 37 complete markers, all indices/figures, previous implementations and all
374 migration dispositions. The new solution heading gives 295 current references
with 39 stable topics; the author seam identities/targets are unchanged. See
`phase-5l-final-results.json`, `phase-5l-exit-checks.json` and REPORT.md's cited logs.

Full/sample/proposal PDFs remain **322 / 54 / 6 pages**, zero final warnings or
bad boxes; all 363 archive files match working sources. Part XI, contents, closing
transition and affected samples were visually reviewed; listing spacing was
adjusted locally without changing production styles (`phase-5l-visual-review.md`).
Production +0/−0; public test/registration support +136/−1. No fixture process remains.
The manual broker-enabled extension and hosted CI are not newly verified; the
public answers distinguish those from the local mandatory observations.

Global words **103,934 → 103,461**; deep chapter headings **307 → 294**; mean
section prose **292.51**; text fences **92**; rules **20**; forbidden/closing hits
**0**. Front matter **1,980 / 2,500**, all Part openers **1,356 / 1,650**. All five
sample gates remain valid. These numbers do not replace the final global audit.

Commit: `proposal-readiness: phase 5l — refine Part XI and verify the integrated gateway`.
**Stop after Phase 5l.** Phase 5m covers Appendix A, epilogue, back matter and the
final audit; Phase 6 refreshes the proposal. Preserve the remaining reserve and
all author teaching-content stop rules. The epilogue remains a closing essay.


## Phase 5m — closing material and final manuscript audit completed, 2026-09-23

The fresh Phase 5l entry run passes all ten groups and 60 labs, reproduces its
metrics exactly and passes the unchanged exit assertions against new entry logs.
Evidence: `review/proposal-readiness-2026-09-22/phase-5m-entry-*`. The author-approved
scope remains Appendix A, epilogue, back matter and final global audit only.

Edited and reread the appendix into nine connected sections, merging repeated
source maps/navigation advice and extension-point introductions. Preserved the
MiniGateway excerpts, shell searches, index entries, source/topic anchors and
reconfiguration, failure, queue-admission and flow-lifetime qualifications. Added
three objectives and five mapped exercises, with public answers under
`companion/exercises/appendix-a/`. Its two labs reuse the existing installed-consumer
and line-carrier experiments; no new application or parser implementation.

The epilogue remains a closing essay without teaching callouts. Four sections
connect its argument; the philosophical section and final author closing stay
verbatim. Further Reading now points to all public solutions; existing references,
epilogue opener, reference divider and index source remain. No numbered chapter,
Part opener, manuscript order or proposal source changes in this phase.

| Material | Words / ceiling | Deep headings / ceiling | Mean section prose |
| --- | ---: | ---: | ---: |
| Appendix A | 3,694 / 4,700 | 9 / 10 | 389.00 |
| Epilogue essay | 1,388 / 1,900 | 4 / 4 | 338.75 |
| Back matter | 781 / 1,000 | Not a chapter gate | — |

No reserve draw. Chapter 27 retains its earlier 400-word allocation; planned
allocation 112,650, reserve **2,350**, hard ceiling **115,000**.

All **62 public labs** and the other nine check groups pass. The public appendix
target builds; the source-reading steps were independently inspected and run.
The final checker certifies all 30 numbered chapters plus Appendix A: three
objectives, one recap, five tiered exercises, complete mappings and public answer
sections, chapter budgets and heading/mean-section targets. The audit reread
teaching callouts, all twenty rules and eleven checkpoint pointers; previous
Parts' complete prose and lab implementations remain as previously reviewed.
The integrated MiniGateway checkpoint stays in Chapter 30.

Global words **103,461 → 100,338**; deep headings **294 → 252**; mean section prose
**334.87**; text fences **45**; rules **20**; forbidden/closing hits **0**; one shell
label. Both hard and stretch word ceilings are met. Front matter **1,980 / 2,500**;
Part openers **1,356 / 1,650**. All five sample reduction gates remain valid.

Preservation checks retain 293 executable/config fences, 37 exact source markers,
1,033 index entries, 18 figure IDs and all prior reference identities. The register
passes **298 references / 39 topics / 374 migration dispositions**, including the
author's combined seam. Production +0/−0; lab registration +10/−1, no new driver.

PDFs: full **322 → 310**, samples **54**, proposal **6**; final warnings/bad boxes
**zero**. All 365 archive files match working inputs. Closing pages, contents and
index were visually reviewed; sentence wrapping and exercise-box spacing were
corrected with existing facilities. No host policy or framework changes. No new
hosted CI, radio/OpenWrt deployment or capacity claim. Evidence and execution
limits: REPORT.md, chapter-ledger.md, metrics-after-phase-5m.json,
phase-5m-global-audit.md, phase-5m-exit-checks.json and phase-5m-visual-review.md.

Commit: `proposal-readiness: phase 5m — refine closing material and complete the manuscript audit`.
**Phase 5 manuscript work is complete. Stop here.** Phase 6 proposal refresh remains
not started: update proposal TOC/page extents, revision status, sample guide and
conservative evidence after a fresh Phase 5m entry check. The whole proposal pass
is not yet complete, and no subsequent phase is authorized by this completion.


## Phase 6 — final proposal refresh completed, 2026-09-23

Accepted the author's current Phase 6 instructions: collect SNodeC/snode.c and
SNodeC/mqttsuite figures directly on the session day, record the method/date,
interpret them conservatively, and use the supplied teaching portfolio as evidence
of responsibility for the book's prerequisite chain. Use only the supplied author
facts; unresolved items remain **[AUTHOR TO SUPPLY]**. The supplied course name
**Networked and Distributed Systems** governs the revised proposal wording.
No manuscript or companion implementation was authorized or needed in this phase.

The fresh Phase 5m entry run passes all ten groups, all **62 labs**, and the
unchanged Phase 5m exit assertions, with evidence redirected to `phase-6-entry-*`.
Historical phase evidence is preserved. Edited and reread the three proposal
sources: the pitch and teaching case, current 30-chapter/11-Part/Appendix A TOC,
measured Part pages, completed revision targets, sample guide, author evidence
and its limits. The five verified comparable-title entries remain unchanged.

The faculty page corroborates the professorship; Ars Electronica's catalogues
corroborate selected Graz/Futurelab background and the TeleZone programmer credit.
Teaching responsibilities and the Hartbeespoort application are attributed to the
author. Research-institution/collaborator names and public citation of the lecture
deck are withheld pending permission. No secondary technical education was
misrepresented as a university degree. Missing audience/project counts, public
links, detailed appointment dates and founding semester, and revision weeks/hours
remain marked for the author.

Live GitHub REST collection took place **23 September 2026, 00:58–00:59
Europe/Vienna**, or 22 September 22:58–22:59 UTC. SNode.C / MQTTSuite: **6,318 /
1,156** reachable master commits; **11 / 2** stars; **27 / 6** forks; **0 / 2**
watching subscribers; **3 / 2** published releases. Returned contributor accounts
are **4 User + 1 Bot / 3 User**, excluding anonymous identities by default; this
is not asserted to be a unique-human or adoption count. Endpoints, timestamps,
response headers, head-specific counting and pagination are recorded in
`phase-6-repository-figures.json` and its collection script/log.

Final builds and source/extracted-package hygiene pass. The dossier checker
validates the current TOC, sample set, figure consistency, unchanged manuscript,
zero warnings/bad boxes, and all **365** archive files against current artifacts.
Proposal/evidence PDF **6 → 8 pages**; combined sample package **54 → 56**;
full manuscript remains **310**. All eight proposal pages plus seven sample-guide,
opening and closing pages were visually inspected. Full manuscript and sample-body
extracted text remain unchanged apart from page footers/whitespace.

`metrics-after-phase-6.json` exactly reproduces Phase 5m: **100,338 words**,
**252 deep chapter headings**, **334.87** average section prose words, **45 text
fences**, **20 rules**, zero forbidden phrases and closing-perspective sections.
All manuscript targets remain met. Production code and test implementation each
have **+0/−0** changes; the new collection/checker scripts are review support only.
No fresh hosted run, hardware deployment, independent field validation or sales
estimate is claimed.

Evidence under `review/proposal-readiness-2026-09-22/`: REPORT.md Phase 6 account,
metrics-after-phase-6.json, phase-6-entry-*, phase-6-author-source-checks.json,
phase-6-repository-figures.json, phase-6-manuscript-pagination.json,
phase-6-package-release-links-build.log, phase-6-final-*.log,
phase-6-exit-checks.json, phase-6-pdf-text-preservation.json and
phase-6-visual-review.md. The chapter ledger and historical records are unchanged.

Commit: `proposal-readiness: phase 6 — refresh final proposal and dated author evidence`.
**Phase 6 and the recorded editorial/package work are complete. Stop here.**
The explicit author-supply items still limit the submission's market evidence and
prevent a delivery commitment; completing the phase does not assert publisher
acceptance or fill those items by inference.


## Author scope revision — pedagogical smoothing, 2026-09-23

Active specification: `review/pedagogical-smoothing-2026-09-23/PROMPT.md`, read
in full and retained byte-for-byte as installed by the author. SHA-256:
`c34bbab40ac13289e993af8504344f8d1435e1ec5ca87d4fb7ad6dfac8020155`.
The current author instruction authorizes one autonomous run through P0a, P−1,
P0b, P1, P2, P3, P4+P5, P6 and P7, with separate unsquashed gate commits and no
approval questions. Stop only under §14, report the reached state, and push only
`book/pedagogical-smoothing-2026-09-23` to origin whether completed or stopped.
Do not merge or push the source branch.

The new must/wish/hard-ceiling budget is **107,338 / 112,338 / 115,000** raw
whitespace tokens. Chapter floors/caps and waiver rules follow §§4/6. The two
specified splits are approved (32 numbered chapters plus Appendix A). Canonical
vocabulary, prose growth tied to ranked rows, per-chapter teaching apparatus,
all preserved anchors, 20-rule cap, listing/index/figure preservation, and the
P0a–P7 verification gates follow this specification. This replaces the former
105,000 stretch target, structure freeze, one-phase-per-session execution and
proposal-readiness phase checkers as active gates. Historical records stay intact.
No code or substantive technical teaching may be removed merely to meet a budget.
The Markdown manifest remains authoritative. The framework working tree at
`/home/voc/projects/snodec/snode.c`, including uncommitted files, is read-only;
record and compare its freeze at P0a, before the first P3 API check, and P7.
Repository/source facts prevail over a conflicting prompt example, with the
conflict recorded instead of changing the underlying technical claim.

P0a preflight: the book entered clean at `a5e51a204d79caef8c288d5e7b7cec2b8e87d09f`.
The only drift from `c7b76c108db43de7326a1a63756cf02eed3dbb31` is the
commit installing this prompt; no other drift exists. New branch created at that
tip. Evidence: `review/pedagogical-smoothing-2026-09-23/preflight.json`,
`P0a-checks.log`, `framework-freeze-P0a.json`, and `framework-untracked-P0a.sha256`.
The framework freeze includes HEAD, porcelain status, the binary HEAD-diff digest
and a sorted content-hash list of every untracked non-ignored file. No manuscript
or companion text changed in P0a. Next: the exact P−1 C++20 target declarations,
then all entry checks before any pedagogical edits.


### Pedagogical smoothing — stopped at P0b, 2026-09-23

P0a passed in `371a1b09738cb23e3981f2f15c9de9f037390e9c`; P−1 passed in
`c70d9d1ca422bf57dbb7940b5112a31896efe8c6`. The latter adds only the ten
prescribed C++20 target declarations; all 14 concrete targets build with Clang 19
(default C++17), and 21 targeted compile commands explicitly select C++20.

**Stop under §14:** the explicit entry source-alignment check against the frozen
working tree fails on nine anchor checks and eleven file-content comparisons.
This is unrelated to P−1. The framework freeze is unchanged. No repair was
attempted and P1–P7 were not started. Every other entry group passed, including
all 62 public labs, the companion and package builds, teaching/behavior/lifetime
runs, both ci/test-*.py scripts, references, metrics and source/extracted hygiene.
Build/runtime evidence uses the existing installed package and does not certify
the current frozen source. check-smoothing.py was not created or run before stop.

Manuscript tokens remain **100,338 → 100,338** against the new
**107,338 / 112,338 / 115,000** thresholds. No manuscript changes or waivers.
The entry gate blocks further pedagogical work; its unrelated source-evidence
reconciliation must occur outside this stopped pass. The failed-gate evidence
commit is `review: stop pedagogical smoothing at P0b source-alignment gate`.
Only `book/pedagogical-smoothing-2026-09-23` is designated for push; no merge or
source-branch push. Full status and evidence: `review/pedagogical-smoothing-2026-09-23/REPORT.md`,
`P0b-results.json`, `P0b-stop-condition.json`, `P0b-*.log`, `P-minus-1-build.log`,
`metrics-before.json`, `metrics-after.json`, and `framework-freeze-P0b-stop.json`.


### Follow-up 01 — source re-baseline and resumed smoothing

Author instruction: `review/pedagogical-smoothing-2026-09-23/FOLLOWUP-01.md`,
stored verbatim. PROMPT.md remains byte-for-byte unchanged. Resume from
965bcbc on the existing work branch; P0a and P−1 remain complete and unsquashed.
The author accepts the clean, public 8b8da56e0349191d4658ca8f820a490539eccd4d
source, version 2.0.0, as the pin with no reader patch. Phase R authorizes the
manifest/pin, exact nine anchor corrections, local corrections to claims changed
by asynchronous logging, and a fresh framework installation under the book build
directory. The author tree stays read-only. R0, P3 and P7 freezes must match P0a.
Only the new installation supports resumed build/runtime evidence. Run R, repeat
P0b with -resume logs, then P1–P7 autonomously with gate commits. Absolute budgets
and all unaffected requirements remain. Follow-up 01's R stop conditions and
PROMPT §14 apply. Push only the work branch on completion or stop.
The original stop report is preserved in REPORT-P0b-stopped.md; original P0b logs
and metrics remain historical. R0 passes; see R0-preconditions.json and
framework-freeze-R0.json.

### Follow-up 01 result — stopped at R4

R0 passed: clean public 8b8da56, freeze equal to P0a. R1 committed in
`e67295c2dfa4e09dd2ea14cdf11e66c08d2eaf52`; R2 in
`e4f8a612695afeb957293920ea92350e4012aede`; local R3 logging corrections in
`fa62fa1bf554f4efa7a5c71527cb15b67ead1492`. Source alignment now passes with
zero errors. The former P0b source-drift stop is resolved by the authorized pin.

**New stop at R4:** the exported pinned source compiles, but framework CTest
passes 181/183 and fails EndpointLifetimeCountersTest and
InetLegacyClientConnectFailureTest. Both reproduce. These tests read logs before
async delivery completes; expected attempt records are visible after process
exit. Follow-up 01 permits companion-driver timing corrections only; this
framework test/log-visibility mismatch cannot be repaired within that scope.
No framework code, tests or assertions were changed. The build script stopped
before completing the new install/companion stages; 0/62 labs were run against
the new installation. P0b-resume and P1–P7 have not started. No successful R
evidence gate is claimed. Stop evidence commit: `review: stop re-baseline at framework logging checks`.

Tokens: 100,338 → 100,323 (−15), still 7,015 below the absolute must. No waivers.
The original prompt, P0b logs/metrics and report content are preserved; the report
content is copied verbatim to REPORT-P0b-stopped.md. Both later freezes match R0.
Proposal verification claims now distinguish historical lab passes from pending
verification of the public pin. Final status/evidence:
`review/pedagogical-smoothing-2026-09-23/REPORT.md`, `R-claim-review.md`,
`R4-build.log`, `R4-failure-recheck.log`, `R4-log-after-exit.json`,
`R-stop-checks.json`, `R-stop-artifacts.json`, `metrics-after-R.json`.
Push only the existing work branch; no merge or source-branch push.

### Follow-up 02 — continue past the two framework CTest failures

The author explicitly instructs continuation despite the two framework CTest
failures; verbatim instruction is in FOLLOWUP-02.md. This supersedes the R4 stop
above for EndpointLifetimeCountersTest and InetLegacyClientConnectFailureTest.
Preserve both failures as an accepted verification exception; do not change or
weaken framework tests. Complete installation manually after the failed CTest
stage, run the remaining external/companion checks against that new prefix, and
resume R evidence, P0b-resume and P1–P7. All other scope and preservation rules
remain. R's framework test result stays qualified rather than relabeled passing.

R continuation evidence: new prefix installed; external echo 4/4, companion
compilation and all smoke suites pass. Full companion CTest passes 51/62: ten
SIGINT shutdown timeouts and one log snapshot race. The latter's driver now
waits for the record without weakening assertions; its rerun encountered the
independent shutdown failure. Following the author's explicit continuation,
keep these CTests qualified and proceed; no framework changes or shutdown
workarounds. R-results.json and REPORT.md distinguish every result. R evidence
commit subject: `review: re-baseline evidence` (qualified, not all tests passed).


### Follow-up 03 — allow normal SIGINT shutdown more time

Author instruction stored verbatim in FOLLOWUP-03.md. Raise the shared public
lab and teaching-smoke SIGINT grace periods to 60 seconds (previously 5/12),
and existing enclosing exercise timeouts below 180 seconds to 180 (retaining
10-second non-process model tests and existing 300-second build tests). Keep
all graceful-exit assertions and forced-kill failures. No signal targeting or
framework workaround. Re-run P0b-resume with the new limits, recording actual
outcomes. This is an explicit timeout amendment to the previous constraints.

### Follow-up 04 — repair diagnosed lab-driver defects

The author explicitly requests lab fixes where their cause is known; verbatim
instruction is in FOLLOWUP-04.md. Review asynchronous-output observations and
shutdown ownership across their consumers. Repair driver timing and enclosing
timeout defects without weakening observable assertions. Framework source stays
read-only and frozen; do not hide a framework shutdown failure with a different
signal, thread targeting, or a forced-kill success. Continue the editorial run
under Follow-up 02, keeping remaining framework failures qualified.

P0b-resume now executed: 51/62 labs pass with 60-second grace; all eleven failures
are SIGINT shutdown. All other twelve check groups pass. The author-requested
lab repairs preserve assertions; 3/3 focused regression tests and 11/12 integration
rechecks pass, with the remaining logging checkpoint stopped by framework shutdown.
Evidence: P0b-resume-results.json and lab-repair-review.md. Framework freeze matches
R0. Entry remains qualified under Follow-up 02; continue P1. Manuscript remains
100,323 tokens and unchanged since R3.

### Follow-up 05 — revert test adaptations and pause for framework repair

The author's latest instruction (verbatim in FOLLOWUP-05.md) supersedes the
continuation and test-adaptation instructions above. The author identifies a
framework shutdown issue involving late spdlog delivery after main terminates
when receiving signals. Revert the test adaptations rather than accommodating
that issue in the book's labs. Further smoothing and runtime checks are paused
until the framework is fixed and its source authority is reconciled.

All 33 affected ci/companion paths are restored exactly to fa62fa1 (before the
R evidence test adaptation): this includes the initial configuration-log polling,
the shared complete-record waiting, partial-JSON handling, added regression test,
and all SIGINT, CTest and nested checkpoint timeout changes. The earlier P−1
C++20 declarations remain. Evidence: test-revert-verification.json. No framework
or manuscript files changed in this revert; the incomplete P1 vocabulary work
and its untracked metrics remain uncommitted. Historical logs remain evidence
of the earlier runs, not certification of the restored tests. No runtime tests
or package rebuild were run for this revert.

### Follow-up 06 — verify the accepted framework change, then stop

The author accepts framework HEAD drift and requests verification before further
book refinement, followed by a full report and a stop. The verbatim instruction
is in FOLLOWUP-06.md. This session is verification only, not a resumption of P1.
The author tree entered clean at 9746d1862b30a5104d3590aaa4ed79752ba9aa6a
("Drain asynchronous logs during shutdown"). The previous freeze difference is
authorized. Record a fresh before/after freeze for this check; leave the earlier
freeze and source-baseline records historical until an explicit resumed
reconciliation. No framework edits and no test adaptations or timeout increases.

Build a verified archive of all 1,448 source files under the book build directory,
install to a fresh prefix, and run the complete framework CTests, external echo
checks, all 62 public labs and existing smoke/lifetime suites. Preserve all
manuscript edits exactly. Evidence is collected under
`review/pedagogical-smoothing-2026-09-23/shutdown-recheck-9746d186/`.

Follow-up 06 result: verification complete, refinement stopped as requested.
Fresh 9746d186 build/install passes; framework 184/184 and external echo 4/4
pass, with zero skips. All 62 public labs execute: 50 pass, 12 fail on the
original five-second SIGINT shutdown grace. Teaching, behavior and lifetime
suites pass. The new 4,096-record drain regression and both previously failing
framework tests pass. A separate reproduction records STOPPING/SIGINT while
main remains in epoll_pwait, before free()/Logger::shutdown. No test/timeouts or
framework/manuscript files changed. Before/after freezes match. Full results,
all 250 test names and diagnosis: shutdown-recheck-9746d186/REPORT.md,
all-tests.md, summary.json and sigint-backtrace.log under this pass's review
folder. Current book pin stays 8b8da56; the accepted new source needs formal
reconciliation when refinement is explicitly resumed. No continuation now.

### Follow-up 07 — investigate the failing exercises; no repairs

The author requests detailed source-aligned investigation of the failing public
exercises (verbatim instruction in FOLLOWUP-07.md). This remains a narrow
investigation, not a resumption of smoothing or permission to adapt tests.

Direct current-source tracing confirms process-directed SIGINT delivered to the
async logging worker while the event-loop owner remains in epoll. A diagnostic
listener connection releases the stalled echo process, which exits normally with
254. The unmodified twelve failing CTests were rerun under tracing: eight pass,
four fail at the original five-second SIGINT deadline. Every new failure traces
the signal to the worker and main waiting until harness cleanup kills it. No
framework/test/timeout/manuscript edits. Source freeze and tracked input hashes
match; 25 ignored Desktop_GCC-Debug build outputs differ from the earlier broad
snapshot and were neither used nor rebuilt here. The full prior suite remains
184/184 framework, 4/4 external echo, 50/62 labs; no whole-suite rerun is claimed
here. The separate restored ch13 log snapshot timing concern remains unverified
behind shutdown. Book work stays paused. Per-exercise assertions reached, source
path, suite-coverage limitations and raw traces:
shutdown-investigation-9746d186/REPORT.md under this pass.

### Follow-up 08 — verify the new signal-ownership fix, then report

The author requests another check after the framework changes (verbatim in
FOLLOWUP-08.md). Verification-only scope: no manuscript refinement or repair.
Read-only author tree clean at 55c36e418a831573ac9b5284830f4bd0d5074bac.
A verified fresh 1,448-file export/build/install passes all 185 framework CTests,
all four external echo tests, all 62 public exercises and teaching/behavior/
lifetime suites, with zero skips. All twelve previously failing exercises pass
with their restored drivers and timeouts. The new framework signal-wait
regression passes in 0.11 seconds; the 4,096-record drain regression also passes.

The prior idle-listener SIGINT reproduction passes 100/100 fresh processes,
alternating disabled/default logging and three signal-delivery delays, retaining
the five-second grace. Every worker mask blocks SIGINT; normal status 254 in all
trials, maximum observed shutdown 7.74 ms. No wake-up traffic or timeout extension.
The old shutdown failure no longer reproduces. The scoped logging checkpoint
passes in this run; this does not certify arbitrary early async log snapshots.

Source freeze and tracked/non-ignored manuscript/ci/companion hashes are unchanged.
No test or timeout edits; ci/companion still match fa62fa1. No runtime failures or
skips remain in this check. Formal source-baseline reconciliation to the new HEAD
and unfinished P1 editorial work remain pending explicit resumption. Evidence:
shutdown-recheck-55c36e41/REPORT.md, all-tests.md, summary.json, raw logs and
sigint-stress.json under this pass. Verification complete; stop and report.

### Follow-up 09 — verify synchronization simplification; report only

The author requests another check after removal of logging synchronization
constructs (verbatim in FOLLOWUP-09.md). Read-only source clean at
07ca9a2936ee72582df7d159cb06666fe23e30f8; no book refinement or repairs.
The author change removes backend/sink locks (+5/−19 lines); source inspection
confirms the one-worker queue, captured sink lifetimes, signal masks and join
before final flush remain. No arbitrary multithreaded API guarantee is claimed.

Fresh verified build/install: framework 185/185 PASS, external echo 4/4 PASS,
public labs 61/62 PASS, teaching/behavior/lifetime PASS, zero skips. Sole failure:
ch13 checkpoint snapshots the log before shutdown and asserts against that old
snapshot. Separate unchanged-harness observations reproduce the payload absent
before shutdown in 14/40 cases and present after normal shutdown in 40/40.
This is the previously recorded open async log observation race, not the old
SIGINT hang. No driver or assertion has been altered. SIGINT stress remains
100/100 PASS with the original five-second grace (maximum observed 7.65 ms).

Framework freeze and manuscript/ci/companion hashes remain unchanged; original
tests and timeouts preserved. Verification complete but qualified by ch13's
snapshot timing failure. Formal source reconciliation and P1 work remain pending;
book refinement stays paused. Complete suite results, ownership inspection,
before/after log observations and preservation evidence:
shutdown-recheck-07ca9a29/REPORT.md under this pass. Stop and report.

### Follow-up 10 — fix only the checkpoint verification timing

The author explicitly requests the fix and requires usage/API preservation
(FOLLOWUP-10.md). Only companion/exercises/ch12/configuration.py, the Python
driver for exercise-ch13-part-checkpoint, changes. It retains a read-only log
handle across existing harness cleanup and reads after normal shutdown has
drained the async queue. All assertions, function signatures, CLI arguments,
CMake registrations and timeouts remain unchanged. No framework, C++ example,
lab/exercise program or manuscript change. Production code +0/−0; verification
driver +12/−7. No polling, extra delay or alternative shutdown path.

Against unchanged clean 07ca9a29 and its previously verified installation:
40/40 consecutive checkpoint runs and 62/62 public exercises PASS, zero skips.
Assertion ASTs match and all other recorded book inputs are preserved. Framework
and other suite results from Follow-up 09 remain historical same-source evidence,
not reruns in this fix. Identified snapshot race resolved; API and user invocation
unchanged. Evidence: checkpoint-log-fix/REPORT.md, results.json, summary.json,
preservation.json and verbose CTest logs under this pass. Refinement stays paused;
source reconciliation and unfinished P1 work remain pending explicit resumption.

### Author handoff — snapshot for independent review

The author requests committing and pushing the complete current book state for
Claude to review the status and next steps. Preserve the unfinished P1 manuscript
edits and existing P1 JSON evidence as a work-in-progress snapshot. This is not a
P1 completion/gate commit. No manuscript content changes or new verification are
performed for the handoff. Work remains paused; no next phase starts. Current
state, evidence locations and pending source reconciliation are summarized in
review/pedagogical-smoothing-2026-09-23/HANDOFF.md. Push only the existing work
branch, without merging or updating SNode.C-2.0-refinement.


### Follow-up 11 — consolidated scope and Phase R2

Author instruction stored verbatim in
`review/pedagogical-smoothing-2026-09-23/FOLLOWUP-11.md`. Active authority is
PROMPT.md, FOLLOWUP-01 §5 (07ca9a29 replaces 8b8da56), and FOLLOWUP-11.
Follow-ups 02–10 and their verification tasks are historical and complete.
Continue from clean a2ecd9c; keep every commit and the 2e71f2a checkpoint fix.
No timeout changes or test adaptations. Capture framework-freeze-R2.json and
keep that same source state through P7; stop immediately on drift, a framework
defect, or a false claim that cannot be locally corrected. Do not investigate
framework changes after a stop.

Phase R2 re-pins the live source records, changes only the three specified
anchors, reviews signal/shutdown claims locally, and builds a fresh archive and
installation for the complete P0b check set. Then finish P1 by contextual reread
of the snapshot changes, counts/allowlist and fresh metrics; execute P2–P7 under
the unchanged absolute 107,338 / 112,338 / 115,000 budgets. No gate is complete
yet in this resumed run. Push the work branch on completion or stop; do not merge.

R2 result: public pin commit 4762369, anchor commit 69ac502, local dispatch claim
commit cfd65ab. Fresh 1,448-file archive/build/install passes framework 185/185,
external Echo 4/4, public labs 62/62 (zero skips), teaching/behavior/lifetime
suites and the full static/package entry set. R2-results.json records outcomes;
R2-build/ holds new runtime evidence and identical before/after source freezes.
reviewed_tree_sha256 now records the new digest. No framework, existing driver,
assertion or timeout changed. Separate P0b-R2-resume gate follows before P1.

P0b-R2-resume passes all thirteen check groups, including 62/62 labs against
the fresh R2 installation and package/extracted hygiene. Logs are named
P0b-R2-resume-*; old P0b and P0b-resume records are untouched. Fresh metrics
are metrics-before-R2-resume.json: 100,777 tokens. P1 can now be completed.

P1 completed from a2ecd9c after contextual reread. Corrected handle/instance/flow
precision, per-connection context ownership and network-family versus connection-
variant wording. Retained only system-design context-dependent roles; every
carrier use is in the MQTT chapters, glossary or two preserved IDs. Evidence:
P1-context-review-notes.md, terminology-counts.md, terminology-allowlist.md,
metrics-after-P1.json and P1-{references,source-alignment,hygiene}.log. Fresh
count 100,780; all three checks pass. No companion/CI test/assertion/timeout
changes and no production-code changes. Next is the mechanical P2 split.

### Follow-up 11 — P2 mechanical gate

P1 committed as `c603b8f`. P2 splits, topic-based references, ordered source records, public exercise migration and live registries are complete. Reference checker, six regression tests, source alignment (zero errors), hygiene, companion build and 62/62 labs pass. Fresh total: 100,916 tokens. Evidence: `pedagogical-smoothing-2026-09-23/P2-registry-review.md` and P2 logs. Apparatus placeholders intentionally await P3. Framework freeze unchanged before P3 API review.

### Follow-up 11 — P3 teaching and apparatus gate

P2 committed as `9df7d00`. Tier 1 work and all four split-chapter apparatus sets are complete. The framework freeze remains identical to R2. All 33 apparatus units, source alignment (37 exact listings), references, hygiene, companion build and 66/66 labs pass. No test assertion or timeout changed. Fresh total: 108,701 tokens. Evidence: `pedagogical-smoothing-2026-09-23/P3-gate-notes.md`, API review, apparatus JSON, build and lab logs/XML. Next: P4 and P5, then seams and full exit gate.

Author clarification during P3: explicitly approved the 67-line complete CMake listing adjustment. Seven blank separator lines were removed from canonical source and printed copy; all statements are unchanged and the exact-listing and build checks pass.

### Follow-up 11 — P4/P5 gate

P3 committed as `0deb8b3`. Tier 2 and tier 3 work complete, including both optional rows because the pre-P5 projection was below 113,500. Core-mechanism sweep covers all 33 units. Fresh total 109,970; source alignment, references, hygiene, checker regressions and eight affected labs pass. The new retry setter excerpt compiles against the R2 installation in an isolated consumer copy. No companion application/driver/assertion/timeout changes. Evidence: `pedagogical-smoothing-2026-09-23/P4-P5-api-review.md`, `P5-core-mechanism-review.md`, phase metrics and logs. Next: every consecutive seam, then P7.

### Follow-up 11 — P6 seam gate

P4/P5 committed as `6683818`. Read all 55 consecutive manifest pairs, including Part openers, Epilogue and Appendix A; local handoffs are recorded in `pedagogical-smoothing-2026-09-23/seam-log.md` with final snapshots. References, source alignment and hygiene pass. Fresh total: 110,177. All 33 unit floors and caps are met without waivers. P7 full exit checks, diagnostic checker, final accounting and report remain.


### Follow-up 11 — completed P7 exit

P6 is `6b7d7c0`; P7 is `c1db599`. R2 and P0b-resume through P7 are complete on public 07ca9a29. Final raw tokens: 110,177; must 107,338, wish 112,338, ceiling 115,000. Every unit and group meets its floor/cap without waiver. P7 passes 66/66 labs and all smoke/lifetime/static/checker suites. The source package now includes the two active chapter registries; its extracted hygiene check is required final evidence. Framework freeze matches R2. All 16 smoothing assertion groups pass, with mutation regressions. Full evidence, qualifications, phase commits, chapter ledger and self-assessment are in `pedagogical-smoothing-2026-09-23/REPORT.md`. Earlier progress entries are historical. No merge; push only the work branch.

### Follow-up 12 — final polish authorized; stopped at entry

The author instruction is preserved verbatim in
`pedagogical-smoothing-2026-09-23/FOLLOWUP-12.md`. It adds only P1–P9
to the governing PROMPT.md, FOLLOWUP-01 and FOLLOWUP-11: terminology,
the Ch8 table, Ch2 commands, Ch13 running value, MQTT fundamentals/diagram,
Ch18 reference placement, Ch23/26 concrete wording, verification phrasing,
and publisher proposal consistency, followed by the specified evidence.
No companion or structural changes are authorized. The hard ceiling is
115,000 tokens, with an aim of 112,500 or less; chapter floors and the
specified cap/waiver rules remain in force. One commit per item in order,
then evidence, and push without merge are the requested completion sequence.

Entry is the requested `9b82ea4668f96e2b577b2c474a337e02fbb61ae0` on
`book/pedagogical-smoothing-2026-09-23`. The required P0a-method capture
does not match `framework-freeze-R2.json`: HEAD and the tracked binary-diff
digest are unchanged, but there are 22 untracked, non-ignored files under
`porting/` in the author's framework tree. Follow-up 12 §0 and PROMPT.md §14
therefore stop this run before P1. No manuscript, companion, framework or
structure change; no re-pin or investigation of framework behavior.

P1–P9 and their checks remain unstarted. No new matrix cells are certified.
The previous completed P7 report remains historical. The untracked publisher
review from the preceding task is preserved separately. Stop evidence is in
`pedagogical-smoothing-2026-09-23/POLISH-REPORT.md`, the polish start/end
freeze records and `polish-freeze-comparison.json`. This stop does not waive
the freeze or authorize automatic resumption.

### Follow-up 12 — authorized resumption from 9172e99

The author resumes all nine items and the evidence/push from `9172e99`.
`FOLLOWUP-12.md` is already installed and stays unchanged. The earlier stop
report is renamed `POLISH-REPORT-entry-stop.md` and remains historical.
The author's untracked `porting/` directory is outside source authority:
do not read, move, exclude through Git configuration, or modify it. Compare
HEAD, porcelain status with only `?? porting/` removed, the binary HEAD-diff
digest, and untracked nonignored files outside `porting/` to R2. Every other
difference still stops the run. The filtered entry record equals R2.

For source alignment and source inspection, the author explicitly authorizes
a fresh public clone in `build/polish-07ca9a29-public`, detached at
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. No checker alteration or author-tree
mutation is authorized. Complete P1–P9 in order with one commit per item,
then the evidence commit. No companion changes or additional review items.
The matrix is a register-row assessment (32 rows including the new verification
register row), distinct from the historical chapter-score matrix.

### Follow-up 12 — resumption delivered with one qualified condition

The resumption from `9172e99` has P1–P9 commits in order:
`f8df09d`, `40aed6c`, `be2179d`, `5cefd5c`, `505d6d6`, `7368aa0`,
`82a908d`, `ff995b8`, `f5ba856`. The final evidence commit closes two
in-scope omissions (Ch24 terminology and Ch18's observation-table formatting),
refreshes the P2 reference registry and terminology inventory, and records the
new checker, regression tests and full report. No companion, existing test,
timeout, source pin, approved chapter structure or author instruction changed.

The reader receives 110,767 raw whitespace tokens (+590 from entry), with
all floors/caps satisfied, 1,571 below 112,338 and 4,233 below 115,000.
The rebuilt book is 330 pages at `dist/pdf/snodec-book.pdf`; proposal and
sample PDFs are 9 and 60 pages. The exact verification regex is back to 46.
Both author-filtered freeze snapshots equal R2; the fresh public clone is clean
at `07ca9a2936ee72582df7d159cb06666fe23e30f8` and passes source alignment.

The new polish checker passes **8/9 groups**; all 16 existing smoothing groups,
16 new checker mutation tests, chapter references, source alignment, hygiene,
figure build and twice-built package checks pass. Labs were not rerun because
companion files are unchanged.

**Qualified, not fully closed:** register row 16 / C remains ◐. The Ch8 table
is corrected, but the global taxonomy assertion also flags the existing
Conventions glossary and Appendix A's reading-path table. Follow-up 12 P2
only authorizes the Ch8 edit, while the governing scope requires the glossary.
Those two tables were not changed or exempted from the checker. All other
register cells are ● on the scoped issue-closure basis explained in
`pedagogical-smoothing-2026-09-23/POLISH-REPORT.md`: E/D/G/X/T/L/S each 32 ●;
C 31 ● and 1 ◐; no ○. Historical chapter ratings remain separate.

`POLISH-REPORT-entry-stop.md` preserves the old report byte-for-byte;
`POLISH-REPORT.md`, `POLISH-CLAIMS.md`, the fresh metrics and check logs now
record the resumed outcome. Push the work branch without merging, then stop
for the author's reading. Do not treat this qualification as permission for
another manuscript pass or silently broaden P2.

### Follow-up 13 — final polish and publisher freeze gate

The verbatim instruction is `pedagogical-smoothing-2026-09-23/FOLLOWUP-13.md`.
Start from `b98eb4a` on the existing work branch; perform only A–I, one commit
per group followed by one evidence commit, preserving all prior history. The
initial author-tree freeze equals R2 after ignoring only `?? porting/`;
`porting/` is outside source authority and is not read or modified. A fresh
public clone at `build/final-polish-public-07ca9a29` supplies source verification.

A–H authorize the specified local corrections, selective repetition reduction,
apparatus placement and cadence changes. I authorizes one shared companion
build/test loader-policy correction, with unchanged test assertions, timeouts
and test logic, verified through the workflow commands under GCC and Clang.
The new scope explicitly permits the two precise taxonomy-table exemptions and
requires the final checker, current proposal figures, rebuilt PDF and a 37-row
status matrix in FINAL-POLISH-REPORT.md. Hosted results must be observed or
labelled pending. Push without merging, then freeze for publisher submission.

The relationship between requested compression and the old chapter floors has
been raised with the author; A–C and source/CI diagnosis can proceed meanwhile.
No padding or unrelated expansion is authorized to compensate for these cuts.

Author clarification: **keep the old floors; qualify cuts that would cross them**.
Apply this to D and all other edits; do not pad elsewhere or waive a floor.

Further author clarification: **“Did i select cut down? I do not want to cut the
manuscript down!”** This overrides Follow-up 13's requested compression.
Do not carry out the shortening portions of D (or remove prose under E/H).
Retain substantive explanations and listings. Continue local factual and
terminology corrections, non-cutting synthesis/cross-reference improvements,
apparatus, cadence, checkers and CI verification. Record the requested cuts as
withdrawn by the author, not as completed compression or a technical blocker.
No compression edits had been made when this instruction arrived.

### Follow-up 13 — stopped at the frozen-framework Clang build

A–I commits: `49c8ba7`, `f390b8c`, `7a92b21`, `e458f2d`, `ab0a145`,
`ae145cb`, `443e24d`, `99ca720`, `f19a658`. The author withdrew compression
before any such edit; all targeted teaching explanations and listings remain.
Current extent is 110,955 tokens (+188), all chapter floors/caps satisfied;
the rebuilt reading PDF is 328 pages. Local corrections, apparatus, cadence,
precise taxonomy exceptions and the new final checker are recorded in
`FINAL-POLISH-REPORT.md`. The checks pass: smoothing 16 groups, polish 9 groups,
final guards, 30 editorial checker tests, reference/hygiene and frozen alignment.

The shared companion configuration uses the existing lifecycle-lab inherited
RPATH policy on Linux. Both affected binaries pass focused checks with the
separate host installation hidden and LD_LIBRARY_PATH unset. Application code,
existing test logic, assertions and timeouts are unchanged.

The fresh Clang 21.1.8 framework build failed at
`src/tools/snodec-control/src/ConfigActions.cpp:296` with `-Werror,-Wnrvo`.
The GCC workflow build was stopped under the author’s framework stop rule.
Neither fresh 66-lab run nor its smoke/lifetime suites is certified. No framework
fix, flag change, alternate compiler experiment or behavioral investigation
followed. Both author-tree freeze records equal R2, ignoring only `?? porting/`.

The 37-row matrix has 36 ● and 1 ◐ in each dimension (288 ●, 8 ◐): row 33
records the withdrawn compression criterion, not authorized unfinished cuts.
The publisher submission gate is not passed because fresh executable verification
is incomplete. A–I were pushed; hosted run 36002150169 was in progress.
Commit and push the final evidence without merging, then end this run. No further
broad manuscript refinement is authorized.

### Follow-up 14 — local corrections, explicit reinforcement and CI closure

The verbatim authority is `pedagogical-smoothing-2026-09-23/FOLLOWUP-14.md`.
Continue from `d4ff44d` with one commit for A–D and one evidence commit.
No teaching passages, examples, listings or explanations may be cut. Correct
the article and swapped exercise references, resolve the specified terminology,
and add local links making seven repetitions explicit. Aim for 100–400 net
new tokens while preserving chapter caps and the 115,000 ceiling.

The initial author freeze matches R2, ignoring only the `?? porting/` entry;
its contents remain unread and the author tree remains unmodified. Use a fresh
public clone at 07ca9a29 for alignment and local verification. The known local
Clang 21 incompatibility is explicitly outside the book; this follow-up permits
verification with the hosted compiler version and, only if required by hosted
framework compilation, a workflow pin to the working Ubuntu distribution Clang.
No framework patch, warning suppression, assertion, timeout or test-logic change.

Read both prior hosted runs, record compiler versions and job conclusions, run
the workflow build and all 66 labs with GCC and matching Clang, push and inspect
hosted results. Record the 37×8 matrix, all checks, token/page measurements,
unchanged freeze and remaining qualifications in FOLLOWUP-14-REPORT.md. No
aggregate-build-option changes from the preceding discussion are authorized
by this narrow follow-up. Push without merging and end the manuscript pass.


### Follow-up 14 — complete; publisher freeze gate passed

A–D commits are `94e4838`, `d27b2ef`, `859fd61`, `ca2f768`.
The article, exercise mappings and terminology residues are corrected; all
seven repetition links are explicit. No teaching passage, example, listing
or explanation was cut. All 130 fenced blocks in touched files are unchanged.
The manuscript has 111,070 tokens (+115), within every chapter cap and the
115,000 ceiling. PDFs: book 328 pages, proposal 9, sample 61.

The matrix is now 37 ● / 0 ◐ / 0 ○ in each of eight dimensions (296 ●).
Smoothing, polish, final regression, reference, source alignment, hygiene,
metrics and twice-built package checks pass. All 34 editorial checker tests
and the six hygiene tests pass. Start/end author-tree freeze records equal
R2, ignoring only `?? porting/`; the fresh public clone is clean at 07ca9a29.

Local Ubuntu 24.04 runs with GCC 13.3.0 and Clang 18.1.3 each pass 185/185
framework tests, 4/4 external-consumer tests, 66/66 labs, and all teaching,
behavior and lifetime suites. Hosted run 36039311975 on pushed ca2f768 passes
both compiler jobs with those versions and results. No new companion/workflow
change was required. Historical run 36002150169's GCC Ch7 log-interleaving
failure is recorded, not claimed repaired; its successor and current runs pass.
Clang 21's frozen-framework -Wnrvo compatibility issue remains outside this
branch for the next SNode.C release, as expressly scoped by Follow-up 14.

`FOLLOWUP-14-REPORT.md` contains the full matrix, changed-cell evidence,
chapter counts, commit mapping, local/hosted logs and freeze gate. Commit and
push this final evidence without merging, then end the manuscript pass. No
further broad refinement is authorized; publisher-submission freeze now applies.
