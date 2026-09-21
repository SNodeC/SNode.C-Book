# Agreed manuscript refinement work plan

Established: 21 September 2026.
Status: active; the combined editorial pass and integrated reread are complete.
Dimensions 1, 2, 3, 5 and 6 meet their criteria. Dimension 4 remains in progress:
its written treatment and local rehearsals are complete, but platform/service
acceptance is explicitly pending. Example behavior and broader validation remain
separate unfinished workstreams; the full plan is not closed.
Next action: trace the idle SSE subscriber ownership and prepare the smallest
correct change under item 7. OpenWrt execution requires a matching SDK, a 2.0
recipe port and a disposable target. See the final checkpoint and evidence below.

This plan records the author's accepted remaining work. It persists across
conversations through the repository's `AGENTS.md`. It is self-contained; the
previous publisher review and technical-refinement report provide additional
context when available.

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

### 4. Practical depth and exercises — in progress

- Identify chapters whose titles or promises exceed their demonstrated practice.
- Strengthen the existing treatment with reproducible exercises, observable
  outcomes, and failure cases where these add understanding.
- Complete practical Linux service-operation and OpenWrt deployment walkthroughs,
  aligned with the actual framework/application packaging and available tooling.
- Verify runnable instructions and clearly identify prerequisites and platform
  requirements. Do not present an unexecuted deployment recipe as tested.

Done when the identified gaps are addressed at the existing chapter depth and
runnable material has suitable evidence. Hardware or service-dependent checks
that cannot be executed must remain explicitly pending or blocked.

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

### 7. Remaining example behavior — pending

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

Done when the selected behavior is implemented, explained, synchronized with
printed examples, and verified at the user-visible boundary.

### 8. Broader validation — pending

Track these individually; a passing source check or compiler run cannot close them:

- Bluetooth exchanges on suitable hardware and relevant operating-system policy.
- OpenWrt build, deployment, service operation, and restart behavior.
- Live MariaDB service integration and relevant asynchronous failure behavior.
- Full MQTT broker interoperability for the teaching scenarios, beyond CONNECT bytes.
- Sustained-load and long-duration behavior for the relevant application boundaries.

Before execution, define the scenario, expected result, prerequisites, and bounded
resource use. When facilities are unavailable, record the precise missing facility
and continue independent work. Do not invent successful results or relabel a
source-only inspection as runtime validation.

### 9. Integration and final review — in progress (editorial integration done)

- Reread the refined manuscript end to end for progression, repetition, voice,
  depth, terminology, and consistency between claims and examples.
- Reconcile the source baseline and evidence with the current framework tree;
  preserve prior results with their original source identity.
- Run appropriate source/listing/reference checks and affected builds/tests.
- Report production-code, test-support, and manuscript changes separately.
- Report which publisher-review recommendations are completed and which remain
  pending or blocked. Full completion requires every required item to be resolved
  or an explicit user decision changing its scope.

The combined manuscript reread, source reconciliation, checks and accounting are
complete; the final report is `review/editorial/refinement-2026-09-21.md`. Full-plan
closure remains pending items 4, 7 and 8. Their unresolved criteria are not waived.

PDF regeneration and visual review remain outstanding production work. Do not
read the PDF or silently add a PDF review while the author's Markdown-only reading
instruction remains in force; establish that separate scope when requested.

## Chapter ledger

The statuses below concern the outstanding editorial pass. They do not erase the
previous technical work. Use `pending`, `in progress`, `done`, or `blocked` with a
specific reason. A completed row needs a short outcome and evidence reference,
including any repetition deliberately retained. Update a row only after reading
and editing or explicitly assessing that chapter; do not mark an entire range done
from a sample.

All chapter rows include full reading and the integrated contextual reread. A
`done` practice cell means the chapter's identified editorial gap was assessed
and its appropriate evidence recorded, not that every suggested deployment was
executed. Service-dependent exercises remain pending below and in item 8. The
[evidence report][E] distinguishes source reading, builds and actual exchanges;
the [repetition map][R] records deliberately retained reinforcement.

[E]: editorial/refinement-2026-09-21.md
[R]: editorial/repetition-map.md

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
| 12 | done | done | done | blocked | done | done | Duplicate lists replaced by service-selection consequences; hardware exercise remains unexecuted. Suitable Bluetooth hardware/policy unavailable. [Evidence][E]; [repetition decisions][R]. |
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
| 23 | done | done | done | done | done | done | Clarified restricted Accept policy, quiet-stream observation, replay limits, and retained subscriber issue; consolidated repeated SSE summaries. [Evidence][E]; [repetition decisions][R]. |
| 24 | done | done | done | done | done | done | Refined comparison around admission evidence; verified negotiation, hello exchange, closure and unsupported-name rejection; binary-echo behavior remains unresolved. [Evidence][E]; [repetition decisions][R]. |
| 25 | done | done | done | pending | done | done | Added connection/session/subscription/delivery exercise; clarified ownership and private extension boundaries. Full broker/subscription/delivery rehearsal pending. [Evidence][E]; [repetition decisions][R]. |
| 26 | done | done | done | pending | done | done | Added concrete binary CONNECT payload/source-trace exercise and complete endpoint prerequisites; consolidated repeated stack lists. CONNECT bytes checked; full MQTT-over-WebSocket broker exchange pending. [Evidence][E]; [repetition decisions][R]. |
| 27 | done | done | done | pending | done | done | Corrected serial-looking fan-out diagram; added partial-failure exercise and process/operating-cost tradeoffs. Partial-failure exercise involving a live broker pending. [Evidence][E]; [repetition decisions][R]. |
| 28 | done | done | done | blocked | done | done | Corrected transaction-queue error behavior and premature durability implications; added isolated persistence checks; refined persistence figure. Controlled live MariaDB failure rehearsal unavailable. [Evidence][E]; [repetition decisions][R]. |
| 29 | done | done | done | done | done | done | Consolidated repeated imported-target/category material; added JSON pair source exercise and executable-variant tradeoff. [Evidence][E]; [repetition decisions][R]. |
| 30 | done | done | done | done | done | done | Replaced repeated role/protocol inventories with compatibility and restart reasoning; distinguished carrier recovery from operation outcomes. [Evidence][E]; [repetition decisions][R]. |
| 31 | done | done | done | pending | done | done | Checked current separate suite source; clarified independent raw/projection writes and bridge extension; added publication trace and corrected ecosystem labels. Source inspection complete; suite deployment unexecuted. [Evidence][E]; [repetition decisions][R]. |
| 32 | done | done | done | done | done | done | Qualified link visibility and runtime defaults; added installed-component failure exercise. [Evidence][E]; [repetition decisions][R]. |
| 33 | done | done | done | blocked | done | done | Added Linux service and OpenWrt walkthroughs; Linux bounded rehearsal passed; old feed source mismatch identified; SDK/device validation pending. Matching SDK, 2.0 recipe port and target unavailable. [Evidence][E]; [repetition decisions][R]. |
| 34 | done | done | done | done | done | done | Added checked-reconfiguration test guidance and executable bounded latency experiment; distinguished diagnostic formatter tests from actual wire exchanges and service assertions. [Evidence][E]; [repetition decisions][R]. |
| 35 | done | done | done | pending | done | done | Refined model/registry scope, literal MQTT topic expectation and session readiness; added observable failure/restart exercises. HTTP/CONNECT behavior checked; broker delivery/restart exercise pending. [Evidence][E]; [repetition decisions][R]. |
| 36 | done | done | done | done | done | done | Developed malformed/split input exercises and process-lifetime tradeoff; clarified Figure 12 scope. [Evidence][E]; [repetition decisions][R]. |
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
