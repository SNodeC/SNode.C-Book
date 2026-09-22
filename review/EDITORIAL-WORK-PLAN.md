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
