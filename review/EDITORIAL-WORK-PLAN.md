# Agreed manuscript refinement work plan

Established: 21 September 2026.
Status: active; editorial refinement remains unfinished.
Next action: read the manuscript in order and inventory repetition across chapters
before making the first coherent editorial changes.

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

### 1. Repetition and manuscript-wide progression — pending

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

### 2. Prose and voice — pending

- Review sentence-level redundancy, abstract wording, unnecessary emphasis, vague
  claims, and repeated conclusions within paragraphs and sections.
- Preserve the author's pace, vocabulary, explanatory layering, and depth.
- Make changes locally; avoid generic replacement prose or blanket style rules
  that flatten the book's distinctive teaching voice.
- Review edited passages in context, not only as isolated diffs.

Done when all manuscript inputs have received a prose pass and a contextual reread.
Track issues actually improved; do not count new paragraphs as proof of cleanup.

### 3. Reader positioning and learning progression — pending

- Sharpen the primary reader and prerequisites using the existing audience and
  teaching approach; do not reposition the book for a different market by assumption.
- Check front matter, chapter promises, introduced terminology, and assumed skills
  for consistency with that reader.
- Make the movement from guided examples to independent application clearer.
- Preserve useful alternative reading routes without making competing audiences
  equally primary throughout every chapter.

Done when reading guidance, prerequisites, chapter introductions, and exercises
form one consistent learning progression without unsupported assumptions.

### 4. Practical depth and exercises — pending

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

### 5. Architectural alternatives and tradeoffs — pending

- Develop concrete decisions already present in the book by comparing plausible
  alternatives, their costs, and the conditions favoring each.
- Prioritize ownership/lifetime, endpoint versus flow policy, process boundaries,
  protocol selection, persistence, and recovery.
- Avoid inventing weak alternatives solely to make the preferred design look good.
- Replace repeated endorsements with reasoning where that improves the passage.

Done when the relevant decisions teach judgment through credible alternatives
and consequences, rather than merely reiterating the preferred boundary.

### 6. References, diagrams, and captions — pending

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

### 9. Integration and final review — pending

- Reread the refined manuscript end to end for progression, repetition, voice,
  depth, terminology, and consistency between claims and examples.
- Reconcile the source baseline and evidence with the current framework tree;
  preserve prior results with their original source identity.
- Run appropriate source/listing/reference checks and affected builds/tests.
- Report production-code, test-support, and manuscript changes separately.
- Report which publisher-review recommendations are completed and which remain
  pending or blocked. Full completion requires every required item to be resolved
  or an explicit user decision changing its scope.

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

| Chapter | Repetition/progression | Prose/context reread | Outcome/evidence |
|---|---|---|---|
| 01 | pending | pending | — |
| 02 | pending | pending | — |
| 03 | pending | pending | — |
| 04 | pending | pending | — |
| 05 | pending | pending | — |
| 06 | pending | pending | — |
| 07 | pending | pending | — |
| 08 | pending | pending | — |
| 09 | pending | pending | — |
| 10 | pending | pending | — |
| 11 | pending | pending | — |
| 12 | pending | pending | — |
| 13 | pending | pending | — |
| 14 | pending | pending | — |
| 15 | pending | pending | — |
| 16 | pending | pending | — |
| 17 | pending | pending | — |
| 18 | pending | pending | — |
| 19 | pending | pending | — |
| 20 | pending | pending | — |
| 21 | pending | pending | — |
| 22 | pending | pending | — |
| 23 | pending | pending | — |
| 24 | pending | pending | — |
| 25 | pending | pending | — |
| 26 | pending | pending | — |
| 27 | pending | pending | — |
| 28 | pending | pending | — |
| 29 | pending | pending | — |
| 30 | pending | pending | — |
| 31 | pending | pending | — |
| 32 | pending | pending | — |
| 33 | pending | pending | — |
| 34 | pending | pending | — |
| 35 | pending | pending | — |
| 36 | pending | pending | — |
| 37 | pending | pending | — |
| 38 | pending | pending | — |

| Other manuscript input | Editorial status | Outcome/evidence |
|---|---|---|
| Front matter | pending | — |
| Part introductions | pending | — |
| Epilogue | pending | — |
| Back matter and further reading | pending | — |

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
