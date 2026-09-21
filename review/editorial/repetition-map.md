# Whole-book editorial map

Pass begun 21 September 2026. Starting manuscript: 144,662 whitespace-delimited
words across the 62 inputs in `manuscript/book-files.txt`. This is an accounting
baseline, not a length target. Hashes are in `pass-baseline-2026-09-21.json`.

## Method and scope

The initial inventory examined every chapter's structure, opening, and closing,
all framing material, and exact repeated prose paragraphs. It is a map for the
subsequent full, contextual chapter reading, not evidence that every paragraph
has already been edited. The six editorial dimensions are assessed together in
coherent groups; each dimension retains its own completion status.

An explanation has a primary teaching home. Later appearances are retained when
they add a changed consequence, application, failure case, or a reminder needed
to read a local example. Cross-references must not make a chapter unintelligible
on its own. Neither chapter length nor a numerical reduction decides an edit.

## Significant recurring explanations

| Cluster | Primary teaching home | Work in later appearances |
|---|---|---|
| Audience, prerequisites, and the book's promise | Preface and Chapter 1 | Keep reading routes in the guide; consolidate Chapter 1's two scope inventories. Replace broad endorsements with the cost of an actual choice. |
| Source, build, install, and consumer locations | Chapter 2 | Chapter 4 uses them for navigation; Chapter 32 resolves component selection. A later reminder should diagnose a concrete mismatch instead of repeating the four-area introduction. |
| Public header, namespace, component, and source path | Chapter 2's first pairing; Chapter 4's navigation table | Chapter 7 assigns responsibilities; Chapter 32 teaches dependency selection. Preserve exact local headers beside examples. |
| Handle, configured instance, flow, connection, context, factory | Chapter 5 | Chapter 6 adds scheduling; Chapter 9 adds lifetime and callbacks. Later chapters should explain which lifetime or policy changed. Avoid another complete model inventory in each opening. |
| Family-independent context versus family-specific endpoint | Chapters 8 and 10 | Unix sockets add namespace and permissions; Bluetooth adds adapter/service policy. Chapters 11 and 12 currently repeat two model lists verbatim. Chapter 15 must demonstrate transfer and its limits. |
| Context behavior and factory construction | Chapters 13 and 14 | Preserve both boundaries but give the transition into Chapter 15 a concrete experiment rather than repeating the same maxim three times. |
| Configuration names, hierarchy, and discovery | Chapter 16 introduces policy; Chapter 17 performs traversal | The two chapters repeat lists of name uses and configuration sections. Retain one inventory and develop the other into an observation or failure diagnosis. |
| TLS below application behavior | Chapter 19 | Retain identity-policy detail and lifecycle qualifications. Repeated assurances that TLS leaves the protocol intact should become decisions about trust, readiness, and failure. |
| Retry and reconnect | Chapter 20 | Chapters 9, 27, 30, and 35 use the distinction to decide application recovery; they need not re-teach the entire flow model. |
| HTTP, routing, SSE, and WebSocket | Chapters 21–24, each at its own boundary | Reduce successive full-stack recaps. Keep comparisons where they explain request completion, retained response lifetime, or protocol upgrade. |
| MQTT session versus its carrier | Chapter 25 for session behavior; Chapter 26 for WebSocket carriage | Chapter 26 needs an observable negotiation/exchange exercise alongside its repeated composition diagrams. |
| Multi-role systems | Chapter 27 selects conversations; Chapter 30 selects process/state boundaries | Chapter 31 traces an ecosystem; Chapters 37–38 judge and extend designs. Their conclusions should answer different questions instead of repeating role constellations. |
| Persistence boundary | Chapter 28 | Preserve asynchronous sequencing and transaction limits. Later state summaries must say which accepted fact survives restart and which does not. |
| Deployment as architecture | Chapter 33 | Replace repeated inventories with a concrete service-operation walkthrough and an OpenWrt packaging path, with execution limits recorded honestly. |
| Testing as evidence | Chapter 34 | Add an observable regression/debugging exercise using existing tests. Distinguish compilation, controlled peers, real services, and load evidence throughout. |
| Capstone and framework extension | Chapters 35–38 | Keep MiniGateway's actual limitations visible. Develop credible alternatives and an extension-validation exercise without expanding production code implicitly. |
| Chapter summaries and part transitions | All parts and chapters | Retain useful “What to remember” summaries. Refine a second closing summary when it does the same job; part introductions should identify the next learning task rather than re-list every previous layer. |

## Exact repetition found in the initial scan

- Chapters 11 and 12 repeat both the shared-framework-model list and the context
  behavior list. Family-specific consequences are the useful material here.
- Chapters 16 and 17 repeat the uses of instance names and the configuration
  section inventory. One should introduce; the other should guide inspection.
- Chapter 6 repeats its “One tick is the multiplexer coordinating…” sentence.
  One occurrence can state the model; the other should explain ordering or limits.

Exact matching finds little of the main issue: much of the repetition is the same
proposition expressed in different words. Each proposed removal therefore needs
the full local reading and neighboring transition check.

## Chapter groups

A: front matter and Chapters 1–4. B: Chapters 5–9. C: Chapters 10–15.
D: Chapters 16–20. E: Chapters 21–26. F: Chapters 27–31.
G: Chapters 32–34. H: Chapters 35–38, epilogue, and back matter.
Part introductions and figure sources are reviewed with their related chapters.

## Evidence boundary

The current source check at the start of this pass passed: 38 chapter records,
35 exact complete listings, and framework tree digest
`03d44f881f28d5d44554dbbe37e0e7284eb3dc8d7e64841b662e57868b0423d0`.
The authority remains the author's current working tree, not the saved manifest
if that tree changes. Earlier runtime results retain their original date and
inputs. PDF reading and visual production QA are outside this pass.

During group A, the author committed the captured framework changes as
`15ddc04c713d172edb32cfa4dbc6778c2d5fe8ae`. The full file comparison reported no
content differences. The reconstruction base and patch remain valid; the checker
now verifies working-tree contents without also requiring the current checkout's
HEAD to equal the older reconstruction base. That redundant identity requirement
was removed, while every file hash, source anchor, and listing check was retained.

## Outcomes of the combined pass

All 62 manuscript inputs were read in book order. All 38 chapters received the
combined editorial assessment and local refinement, followed by an integrated
reread. In that final reread, complete marked listings already read in the first
pass were represented by their companion paths and checked byte-for-byte again;
prose, unmarked sketches, exercises, tables and transitions were read in context.
Index directives were omitted from that reading view, but remain in the manuscript.

| Cluster | Final treatment and reason |
|---|---|
| Audience and orientation | The preface and reading guide establish prerequisites and routes; Chapter 1 closes with an actual application decision. Chapter 2 owns setup; Chapter 4 turns repeated directory descriptions into source tracing. |
| Endpoint and lifetime model | Chapter 5 remains the primary explanation. Chapters 6 and 9 develop scheduling and callback lifetime. Later references distinguish shared configuration from per-activation controllers, including independent cancellation. These repeats protect different operational decisions. |
| Lower-family transfer | Removed duplicate model/context inventories in the family chapters. Retained address, permission, credential, service-selection and platform differences. Chapter 15 now tests one unchanged parser over IPv4 and Unix-domain carriers. |
| Context and factory | Retained the detailed construction and parsing treatment. Repeated closing maxims were reduced where the dependency-lifetime comparison and transfer exercise already demonstrate the boundary. |
| Configuration | Chapter 16 introduces scope and policy; Chapter 17 traverses and tests precedence. The new current-source runtime reparse is explained with its lifecycle, unchanged command-line precedence and absence of rollback or automatic socket restart. |
| TLS and recovery | Retained the trust/identity example and detailed shutdown treatment. Developed carrier-specific consequences and proxy tradeoffs. Retry timing now consistently distinguishes endpoint policy from each flow's timer and state. |
| Web protocols | Repeated stack inventories now give way to request-admission, continuation and negotiation observations. The HTTP/SSE/WebSocket comparisons remain because their message ownership and temporal behavior differ. |
| MQTT and carrier composition | Preserved packet/session teaching and binary adapter details. Added separate connection, CONNACK, SUBACK and delivery observations. Removed a late duplicate handshake checklist after the concrete Chapter 26 exercise. |
| Persistence | Retained command and transaction depth; corrected the usable-connection SQL-error queue behavior. Source submission, operation success and durable commit remain separate. The memory-versus-durability distinction recurs where acceptance policy changes. |
| Systems and ecosystem | Chapters 27, 30 and 31 now add fan-out failure, process recovery, independently deployed contracts, and raw/projection-write outcomes. Repeated role catalogues were consolidated or turned into source questions. |
| Build and deployment | Exact local headers and component names remain beside examples; Chapter 32 is the consolidated graph/matrix home. Added an installed-component failure exercise and Linux service rehearsal. OpenWrt has a concrete source/recipe/SDK gate, not a substituted old framework. |
| Testing | Retained the existing test taxonomy. Added bounded executable observations and distinguished protocol, service and measurement evidence. Latest binary logging has presentation tests separate from wire tests. |
| Capstone | Kept all complete listings and the before/after comparison. That deliberate repetition proves unchanged model/web/MQTT boundaries. Clarified process-global registry scope, sequence authority, literal MQTT input topic and publication-driven SSE cleanup. |
| Judgment and extension | Replaced weak alternatives with plausible HTTP, MQTT, Unix and separate-service choices. Retained worked decisions because they ask the reader to choose ownership, not repeat an API tour. |
| Summaries and framing | Retained “What to remember” summaries and cumulative part bridges. Moved new applied conclusions before summaries where needed; removed local second conclusions that supplied no new consequence. |

The epilogue intentionally returns to layers, boundaries and roles. Its job is
synthesis after the construction and judgment chapters. It was refined locally,
not removed because it repeats the book's central vocabulary.

## Figure content review

All 18 editable figure sources and their surrounding text were reviewed. Figure
identifiers remain unchanged. This is content review, not rendered visual QA.

| Figure | Content outcome |
|---|---|
| 01 | Retained layer stack; caption distinguishes increasing specificity from ownership or callback order. |
| 02 | Explicit activation flow between endpoint configuration and connection/context creation. |
| 03 | Corrected runtime/event-publication relationships and scope of one tick. |
| 04 | Carrier branches express possible reuse, subject to protocol and platform assumptions. |
| 05 | Server/client activation paths distinguish shared policy, per-call flow and later readiness. |
| 06 | Retained HTTP foundation and dependent SSE/WebSocket shapes; Express is application organization. |
| 07 | MQTT bytes travel in binary WebSocket messages; carrier composition does not duplicate MQTT semantics. |
| 08 | Boundary arrows permit exchanges in both directions; caption rejects a serial-pipeline interpretation. |
| 09 | Operational visibility flows from the process; configuration/deployment arrows denote influence. |
| 10 | Suite roles and raw storage/projection are distinguished; no deployment or atomicity guarantee implied. |
| 11 | Retained build/install/package/runtime surfaces; surrounding prose supplies supervision and filesystem requirements. |
| 12 | Caption distinguishes in-memory acceptance and output adaptation; JSON is not a CSV-input dependency. |
| 13 | Retained representative hierarchy; caption allows root/instance options and deeper discovery nodes. |
| 14 | Retained semantic logging scope, filtering and output model; scoped binary diagnostics use that same model. |
| 15 | Secure connection setup and readiness are distinct; protocol continuity is conditional. |
| 16 | Retry/reconnect stay inside one activation controller; another explicit connect starts another flow. |
| 17 | Queued database work remains transient; submission is not durable commit. |
| 18 | Retained separate confidence surfaces; CI orchestrates checks rather than adding a protocol guarantee. |

Source/reference checks cover figure labels and references, existence of all 18
editable sources, and basic source delimiter balance. They do not certify layout,
font size, line routing or page placement. The PDF was neither read nor generated.

## Final source reconciliation

The author first committed the captured per-call flow changes, then added checked
runtime reconfiguration, and later changed scoped binary logging and presentation.
Each content change was inspected against the current local tree. Historical
verification retains its own manifest and patch; final evidence is recorded in
`refinement-2026-09-21.md` and `evidence-2026-09-21.json`.
