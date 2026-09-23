# Publisher-style manuscript review

**Manuscript:** *Layered Network Programming with SNode.C: Building Multi-Protocol Applications in Modern C++*, Volker Christian.

**Review date:** 23 September 2026.

**Book revision reviewed:** `9b82ea4668f96e2b577b2c474a337e02fbb61ae0`.

**Recommendation:** Continue publication consideration, subject to focused developmental revision, correction of the submission package, and independent technical and reader review before production.

## 1. Assessment and method

This manuscript has a credible book-length subject: how to keep network software understandable as protocols, callbacks, application state and operational requirements accumulate. Its contribution is the sustained connection between those concerns. SNode.C gives the author a concrete implementation through which to explain them; MiniGateway makes the consequences observable. The manuscript deserves serious consideration for an advanced C++ and network-systems readership.

It is strongest when a requirement produces a choice, the choice has an ownership or lifetime consequence, and an experiment exposes that consequence. It is less effective when it inventories names or repeats a general architectural principle after the reader already has the information needed to apply it. These two modes coexist throughout the manuscript. The next editorial pass should increase the proportion of the first mode by reshaping existing material.

I would support acquisition discussions. I would hold production approval pending the concrete corrections and reader validation below. Completion of the previous editorial specification and its automated gates is useful evidence, but does not settle acquisition, learning effectiveness or production readiness.

This is a publisher-style developmental assessment, not an independent human peer review. The reviewing assistant participated in the preceding editorial work. The assessment therefore makes its evidence and limitations explicit rather than presenting itself as an external endorsement.

The review used the Markdown inputs in `manuscript/book-files.txt`, the proposal, selected companion implementations and public exercise solutions, and the previous verification report. It covered the structure, openings, section arguments and teaching apparatus across all 32 chapters, Appendix A and the epilogue, with closer reading of the foundation, representative protocol explanations, persistence, capstone and judgment passages. Code inspection was selective. This was systematic coverage and targeted close reading, not a word-by-word copy-edit or exhaustive new code audit.

Fresh manuscript metrics exactly match `metrics-after-final.json`. The prior test results were inspected as recorded evidence; the framework and companion suites were not rerun for this review. The framework working directory now contains untracked `porting/` files, although its HEAD remains `07ca9a29`. That material was not investigated. The earlier freeze and P7 results must be described as evidence from that completed run, not as certification of the present framework working directory.

The reading PDF was not visually proofed in this review. Pagination, typography, code wrapping, figure legibility and final index usability remain production-review questions.

## 2. Audience, contribution and acquisition case

### Intended reader

The stated reader is plausible and specific: an advanced student or C++ developer who understands templates, callbacks, lambda captures, ownership and basic networking, can build a CMake project, and has no SNode.C experience. The prerequisites in the [Preface](/home/voc/projects/snodec/publications/book/manuscript/frontmatter/preface.md) are appropriately candid.

The manuscript should continue to be positioned at that level. Its factories, composed type names, installed-component graph and asynchronous lifetime reasoning would be a substantial additional burden for someone still learning C++. The references to makers and scientists work when the same prerequisites remain explicit.

The reader's reason to buy the book needs to extend beyond learning one framework. The strongest promise is learning to place state and behavior correctly in event-driven C++ systems, with enough runnable material to test that understanding. That promise is supported by the manuscript. Broad claims to be a comprehensive modern C++ networking course would overstate its coverage: the book deliberately follows this framework's callback model and Linux-oriented environment.

### Distinctive strengths

1. **A consistent question about ownership.** Handles, configured instances, activation flows, peer connections, protocol contexts and shared application state have different lifetimes. The book follows the practical consequences instead of treating ownership as an introductory C++ aside.
2. **Observable distinctions between kinds of success.** Connection readiness, accepted state, queue admission, subscriber receipt and committed storage are not interchangeable. Chapters 15, 19, 24, 29 and 30 make this distinction useful to a working programmer.
3. **An integrated application with a defensible purpose.** MiniGateway has one acceptance owner and several adapters and observers. The Unix input extension demonstrates a real benefit of that organization.
4. **Operational continuity.** Headers, CMake components, installed libraries, dynamically loaded modules, configuration and supervision belong to the same application story. Chapters 27–29 give the book more practical reach than protocol examples alone would provide.
5. **Inspectable teaching material.** Complete companion programs, public conceptual answers, independent test peers and a recorded source baseline make the material reviewable and maintainable.

### Acquisition questions still open

The supplied proposal supports the author's subject expertise and teaching experience. It does not yet establish the size of a buying audience. Its dated repository activity figures are explicitly not readership or adoption figures, which is the correct qualification. A publisher should assess course demand, practitioner demand and the value of the transferable architecture argument separately from framework activity.

The proposal still requests author evidence and permissions, including teaching/adoption details, support for the field application account, permission to identify collaborators where needed, and revision availability. These are concrete submission tasks. They should remain visibly unconfirmed until supplied. This review did not independently verify the external biography, institutional or market claims, and makes no sales forecast.

The source pin is a reproducibility strength. It also creates an editorial maintenance obligation: the publisher and author should agree who maintains the downloadable code, which version the printed text supports, how errata are issued, and how later framework revisions are distinguished from the book edition.

## 3. Priority findings

### R1 — Resolve the early-lab dependency mismatch

**Priority: reader-blocking when optional components are absent. Evidence: static configuration inspection.**

[Chapter 2](/home/voc/projects/snodec/publications/book/manuscript/chapters/02-preparing-your-environment.md:98) presents Bluetooth and MariaDB development libraries as optional. Its lab-environment discussion says the first echo labs require the installed framework, CMake, a compiler, Python and loopback sockets. However, the [Chapter 3 solution](/home/voc/projects/snodec/publications/book/companion/exercises/ch03/README.md:21) directs the learner to the common repository-wide lab configuration.

That configuration enters both the examples and exercises. The [examples list](/home/voc/projects/snodec/publications/book/companion/examples/CMakeLists.txt:11) unconditionally includes every example, including [MariaDB-Minimal](/home/voc/projects/snodec/publications/book/companion/examples/MariaDB-Minimal/CMakeLists.txt:11), whose package request requires `db-mariadb`, and the [Asio comparison](/home/voc/projects/snodec/publications/book/companion/examples/Comparison-AsioEcho/CMakeLists.txt:3), whose header search is required. The [exercise list](/home/voc/projects/snodec/publications/book/companion/exercises/CMakeLists.txt:7) enters every chapter, including [Chapter 9](/home/voc/projects/snodec/publications/book/companion/exercises/ch09/CMakeLists.txt:1), which requires the Bluetooth components.

Consequently, requesting only `ch03-lab` at the build step does not remove the earlier configuration requirements. Similarly, a CTest label exclusion does not change which dependencies CMake must find. A learner with a valid minimal echo installation can encounter a database or Bluetooth dependency error before reaching the intended echo lab.

The standalone EchoPair can still be built through its own project; this finding concerns the common public-lab route. It also concerns development components, not a requirement to run a database server or possess Bluetooth hardware for echo. Those distinctions should be preserved when correcting it.

**Requested outcome:** Make the advertised prerequisites and the actual supported lab entry point agree. An editorial correction could explicitly declare the full common-build requirements and identify the minimal standalone route. A build-selection change could preserve staged dependencies, but would require a separately authorized implementation decision. Validate the chosen instructions on a clean installation with only the prerequisites that the early chapter promises. This review has not reproduced that clean-environment run.

### R2 — Correct the proposal before submission

**Priority: submission correction. Evidence: directly conflicting current records.**

The [proposal snapshot](/home/voc/projects/snodec/publications/book/review/proposal/book-proposal-package.md:14) gives the current count as 110,177, then states that the 105,000 stretch target is met. It is not. The current author-approved budget is different, and the proposal should report it consistently.

The [revision plan](/home/voc/projects/snodec/publications/book/review/proposal/book-proposal-package.md:114) still says the smoothing pass is underway, the split chapters will complete their apparatus at P3, and later gates remain in progress. That conflicts with the completed run and the proposal's own completed-material claims. The same table retains 252 chapter subheadings, 334.87 average section tokens, and 45 text fences; the fresh measurement records 259 chapter subheadings, 363.03, and 46 respectively, using the script's stated definitions.

These inconsistencies make it harder for an acquiring editor to know which file describes the actual submission. The corrections are small, but should precede circulation. Remove obsolete internal gate language from the publisher-facing status, give the current revision accurately, and keep remaining publisher review and author evidence tasks explicit.

Also keep counting terminology consistent: the measurement counts raw Markdown whitespace tokens, including markup. It is not a rendered-prose word count. The internal budgets are meaningful under that method; a publisher may use a different method for contractual extent and production costing.

### R3 — Make the first successful run easier to reach

**Priority: developmental revision. Evidence: reading sequence.**

Chapter 2 correctly distinguishes source, build and installation directories and gives valuable advice about selecting the intended installed package. Its “Shortest path to Chapter 3” is nevertheless a prose itinerary followed by several environment and build branches. The learner must assemble the practical route from material distributed through the chapter.

For independent study, provide one clearly identified, contiguous supported route with a consistent local prefix, explicit working directories and one expected success observation at each transition. Keep the existing alternative toolchains, system installation and maintenance detail available nearby as reference. This is an organization problem more than a need for additional explanation.

Test the route with a reader who meets the stated C++ prerequisites but has never installed SNode.C. Record where that reader loses track of the source tree, installation or executable. A previously configured author workstation cannot answer that question.

### R4 — Reduce repetition that adds no new decision

**Priority: developmental revision. Evidence: local examples and recurring pattern.**

Reinforcement is necessary in a book spanning this many layers. The most successful returns to a principle introduce a new failure, lifetime, consumer or operating condition. Some passages instead restate a conclusion immediately or reproduce an already completed trace.

Two clear examples are:

- [Chapter 21, lines 75 and 77](/home/voc/projects/snodec/publications/book/manuscript/chapters/21-mqtt-support-in-snodec.md:75): adjacent paragraphs enumerate substantially the same MQTT responsibilities.
- [Chapter 18, opening trace](/home/voc/projects/snodec/publications/book/manuscript/chapters/18-the-express-like-framework.md:64) and [later test discussion](/home/voc/projects/snodec/publications/book/manuscript/chapters/18-the-express-like-framework.md:247): the same middleware/handler path and short-circuit explanation are substantially repeated. The later section has useful additional cases and a modification experiment; concentrate it on those additions.

There are broader opportunities in the runtime taxonomy across Chapters 4–8, header/component inventories across Chapters 5, 7 and 27, and repeated reminders that one observed success does not establish a different success. Preserve each actual distinction. After it has been taught, a shorter reference often leaves more room for the next consequence.

The prose sometimes defaults to broad nouns—role, boundary, meaning, visibility—when naming the actual actor would make the sentence easier to understand. These are valid technical terms, but they work best after a concrete action: a subscriber disconnects, a model accepts a measurement, a database callback reports failure. Edit for that movement from action to principle.

**Requested outcome:** In each repeated passage, identify the new question it answers. Keep it if the answer is substantive; combine or shorten it if it simply repeats a prior conclusion. Do not remove complete code listings or impose a blanket chapter percentage cut.

### R5 — Put a concrete result before the densest machinery

**Priority: developmental revision. Evidence: selected chapter organization.**

The short event-loop narrative in Chapter 6 and the worked route in Chapter 18 show the effective pattern: give the reader an event sequence, then explain its machinery. Some later sequences spend substantial time on API or implementation inventory before the learner gets another observable result.

Chapter 17 moves from HTTP composition into parser facilities and upgrade-factory deployment. Its first substantial route example is an upgrade route. This is useful material, but ordinary request admission and response behavior deserve a more immediate anchor before the reader takes on module resolution. Chapter 20 similarly asks the reader to follow factory registration and loading before the full message-behavior example. The internal explanation can remain; its reading order should serve the application question.

In Chapters 21–22, the packet conversation is valuable, but a compact publisher/broker/subscriber sequence diagram would be easier to consult than the long inline progression. It should keep the publisher's session, subscriber's subscription and observed delivery visibly distinct. The diagram can replace part of the repeated verbal explanation.

**Requested outcome:** For the densest chapters, make it possible to identify a concrete input, responsible callback and observable output before requiring the whole class or loader map. Mark deeper source-reading sections clearly for readers returning to them later.

### R6 — Strengthen evidence of learning beyond executing supplied solutions

**Priority: developmental revision and reader validation. Evidence: apparatus and representative solutions.**

The apparatus is substantial: three objectives, two review questions, two labs and one design problem in every numbered chapter and Appendix A. Public solutions usually explain what an observation establishes and what it leaves open. This is a strong foundation for self-study.

Several labs, however, primarily ask the learner to build supplied code, run a supplied test and explain its expected result. The [Chapter 10 framing lab](/home/voc/projects/snodec/publications/book/companion/exercises/ch10/README.md:26) is technically useful: it exercises segmentation and delimiters through independent peers. Passing it establishes behavior of the supplied implementation. The learner's ability to write or repair a parser needs an additional act by the learner. The same distinction applies to running the completed capstone.

The book already includes useful prediction, private-copy modification and design questions. Develop those selectively rather than adding more test registrations. A few well-placed tasks should require a prediction before execution, diagnosis of a small wrong implementation, or a bounded change whose outcome is checked without revealing the finished solution first. The answer should explain why plausible alternatives fail, not only state the intended design.

**Requested outcome:** Pilot the first program, one lifetime exercise and a capstone modification with representative readers. Observe whether they can explain and make the change without following the solution line by line. Reader performance is stronger evidence for the “without a lecturer” promise than objective mapping alone.

### R7 — Align the strength of “worked system” promises with the experiments

**Priority: scope and presentation. Evidence: explicit limitations in the manuscript and solutions.**

Chapter 26 gives useful source-guided architectural analysis of MQTTSuite. Its public labs exercise a local broker/client fixture and compare separate database and gateway experiments. They explicitly do not run MQTTBridge, MQTTStore or a multi-broker deployment; see the [public solution](/home/voc/projects/snodec/publications/book/companion/exercises/ch26/README.md:28).

This is honest and technically responsible. It leaves a teaching gap if a reader interprets “MQTTSuite as a worked system” as a reproducible end-to-end suite walkthrough. Choose the promise explicitly: either frame the chapter as a source-guided system case study with separate supporting experiments, or supply a bounded, fully specified suite exercise when that work is justified and authorized. Do not imply that the existing CTests establish the full deployment.

The OpenWrt discussion has the same distinction. [Chapter 28](/home/voc/projects/snodec/publications/book/manuscript/chapters/28-deployment-on-linux-and-openwrt.md:253) responsibly identifies a feed that does not yet select the book's source and requires a ported recipe and matching SDK before the rehearsal. That makes the section a conditional deployment procedure, not an immediately reproducible current package recipe. Keep that condition prominent in chapter and marketing descriptions.

### R8 — Preserve the capstone, but make its stages and transfer limits easier to see

**Priority: refinement. Evidence: capstone and reading guide.**

MiniGateway is the right culmination. The HTTP/SSE observations provide immediate feedback, the shared model owns acceptance order, and Chapter 31 adds input without changing the meaning of that order. Chapter 32 then tests the design against changed requirements. This is the book's strongest sustained argument.

The reading guide calls MiniGateway the “running project,” while the full assembly arrives in Chapter 30. Earlier checkpoints supply related skills and measurement experiments rather than one continuously extended codebase. Both approaches are legitimate, but a compact milestone map should say what carries forward: byte transport, framing, validation, shared acceptance, observation, broker delivery and persistence distinctions, then full assembly. That would make the cumulative promise easier to follow without moving the capstone.

Chapter 30 has complete files with explanatory bridges, which should be preserved. Add navigational emphasis to the existing assembly stages and observations so a learner can stop and account for the model before absorbing configuration, web and MQTT plumbing. Chapter 31's three explained excerpts are an effective approach to the larger parser file. The author's approved CMake-listing exception is not treated as an outstanding defect in this review.

The book also correctly identifies transfer limits: the process-wide MQTT client list assumes one model; the sequence is in-memory; SSE reconnect is not durable replay; queueing is not delivery. Keep these near the corresponding code. For the [transaction sketch in Chapter 24](/home/voc/projects/snodec/publications/book/manuscript/chapters/24-database-support-and-application-state.md:324), the warning about a prequeued commit is essential. A compact failure-path trace contrasting that sketch with outcome-dependent commit/rollback would further help a reader apply the warning. A new persistence subsystem is not required to teach that distinction.

## 4. Chapter-by-chapter assessment

Counts below are current raw Markdown whitespace tokens, using the existing measurement method. They describe extent, not chapter quality. “Priority” means relative editorial attention within this review, not a new authorization to edit or a replacement for the author's agreed scope.

| Chapter | Tokens | Assessment and strongest contribution | Recommended editorial attention |
|---|---:|---|---|
| 1 — Why SNode.C Exists | 2,402 | A persuasive sensor-to-system motivation. The Asio comparison makes ownership costs concrete and acknowledges tradeoffs. | Moderate: reduce repeated versions of the opening measurement scenario after its purpose is established. Keep the framework costs visible. |
| 2 — Preparing Your Environment | 3,194 | Sound distinction between source, build, install and consumer; useful package-identity checks. | High: resolve the common-lab prerequisites and make the first successful route contiguous. |
| 3 — The Echo Pair | 3,001 | A complete first program with a useful chronological explanation and meaningful independent binary-echo checks. | Moderate: separate the minimum actions for first success from the fuller context/factory explanation; validate with a first-time learner. |
| 4 — Runtime Mental Model | 2,908 | Important distinctions between handle, instance, flow, connection and context; good explanation of what diagrams do and do not mean. | Moderate: trim repeated lifetime/taxonomy statements. Correct Exercise 2's “excerpt below,” which refers to an excerpt above it. |
| 5 — Layers in Practice | 2,882 | Connects type, header, component and configuration views; explains why a build choice and a runtime choice differ. | Moderate: consolidate recurring inventories and TLS-selection explanations while retaining the worked consequences. |
| 6 — Core Runtime and Event Processing | 3,502 | The readiness/deferred-work/shutdown story gives substance to event-driven execution. | Moderate: distinguish the application-facing reading path from the deeper source and tick-status reference material. |
| 7 — Network Families and Addresses | 4,206 | Concrete address semantics, wildcard distinctions and Unix-path considerations make the family choices usable. | Moderate: reduce the cost of many similar declaration/constructor blocks through comparative presentation. |
| 8 — Servers, Clients and Connections | 3,184 | Activation-flow independence and callback-stage lifetimes are important and carefully distinguished. | Moderate: rely more directly on Chapter 4 for the established taxonomy; emphasize the new flow and callback consequences. |
| 9 — Bluetooth | 2,173 | Appropriate separation of Classic Bluetooth stream support, selectors, preparation and physical exchange. | Lower: keep hardware-free selector observations visibly separate from radio evidence; do not broaden the promise to BLE. |
| 10 — Writing SocketContext Classes | 3,087 | A strong practical chapter: fragmented input, delimiters, state locality, limits and queue admission become observable contracts. | Moderate: add or sharpen one learner-performed prediction or repair task around the existing parser. |
| 11 — Writing SocketContextFactory Classes | 2,258 | Clear construction and dependency ownership; refusal and immutable/shared dependency distinctions have practical value. | Lower: use existing concrete examples to shorten repeated definitions of what a factory does not own. |
| 12 — Protocol Reuse Across Lower Layers | 2,581 | The framed-protocol transfer makes reuse testable; the discussion of where identity and authorization stop reuse is especially useful. | Moderate: shorten repeated echo setup and concentrate on changed family, unchanged parser, and changed operating assumptions. |
| 13 — Configuration and Named Instances | 4,475 | The successive port settings supply a useful through-line; reparsing versus active policy is a valuable distinction. | Moderate: bring a configuration experiment closer to the initial explanation and reduce intervening classification. |
| 14 — Logging and Diagnostics | 2,793 | Teaches diagnosis by phase and responsible object; distinguishes configuration metadata from events and completed output. | Lower: keep the public logging path foremost and contain the more specialized API/reference detail. |
| 15 — TLS | 2,754 | One of the strongest responsibility distinctions: encryption, trust, expected identity and SNI are separate. The three-outcome fixture is well chosen. | Moderate: ensure readers encounter the policy sketch and its assumptions as one unit; preserve the explicit limits of verification evidence. |
| 16 — Timeouts, Retries and Failure | 3,200 | Good distinction between connection recovery, protocol progress and application replay. The slow-drip/deadline question teaches a real failure mode. | Lower: keep the phase/time relationship easy to consult; retain the bounded-policy discussion without turning it into a general retry cookbook. |
| 17 — HTTP | 2,478 | Explains admission, message semantics, parser limits and upgrade responsibilities. | High: anchor the chapter earlier in one ordinary request/response observation before the detailed upgrade/deployment machinery. |
| 18 — Express-like Framework | 2,218 | The complete dispatch fixture makes middleware continuation and short-circuiting concrete. | Moderate: merge repeated trace explanation; let the later test section concentrate on the outside-route and modification cases. |
| 19 — Server-Sent Events | 3,305 | Strong teaching of long-lived responses, observer removal and reconnect/replay limits. A good publisher sample. | Lower: improve navigation between the core working stream, client behavior and advanced observer/overload consequences. |
| 20 — WebSocket and Upgrade | 3,001 | Makes message semantics, subprotocol selection and runtime module requirements explicit. | Moderate: lead the reader from a successful message exchange into the factory/loading detail; keep size/close behavior nearby. |
| 21 — MQTT | 3,015 | The progression from session establishment to actual subscriber receipt is valuable; scope and private-extension limits are candid. | High: remove the adjacent responsibility duplication and show the publisher/broker/subscriber sequence more compactly. |
| 22 — MQTT over WebSocket | 2,119 | Separates HTTP upgrade, WebSocket negotiation and MQTT progress; makes composition meaningful. | Moderate: use a concise end-to-end trace to orient the reader before adapter internals. |
| 23 — Multi-Protocol IoT Design | 3,141 | The worked HTTP/MQTT input change and unavailable-output experiment apply the shared-authority principle well. | Moderate: trim repeated protocol-selection prose after the useful mapping table; preserve consequences of process separation. |
| 24 — Database and Application State | 3,857 | Clear distinction between acceptance and committed state; command ordering and the rollback-queue pitfall have real instructional value. | Moderate: strengthen the failure-path teaching around the success-only transaction sketch and keep component/service prerequisites distinct. |
| 25 — Reading Complete Applications | 2,560 | The target-to-entry-point-to-observation method is transferable and supports source literacy. | Lower: keep one complete trace in focus so the family catalogue supports rather than interrupts the method. |
| 26 — MQTTSuite | 3,843 | Useful architectural case study separating brokerage, transformation, forwarding and storage. | High: make the source-guided scope and actual lab coverage prominent; full suite operation remains a separate exercise. |
| 27 — CMake and Linking | 3,748 | Strong treatment of declared dependencies, public headers, supported component requests and installed consumers. | Moderate: make this the obvious reference home for repeated header/component inventories elsewhere. |
| 28 — Linux and OpenWrt Deployment | 3,586 | The Linux service rehearsal has concrete lifecycle observations; the OpenWrt section identifies real prerequisites and limits. | Moderate: distinguish the reproducible Linux exercise from the conditional SDK/recipe procedure at the point of entry. |
| 29 — Testing, Debugging and Benchmarking | 4,360 | Strong account of independent peers, installed-consumer checks, skipped evidence and bounded measurement. Avoids unsupported capacity claims. | Moderate: the repository test catalogue can be more compact; give application diagnosis and the actual measurement experiment the strongest emphasis. |
| 30 — Building MiniGateway | 4,587 | The central demonstration succeeds: one acceptance model, shared representation, observable HTTP/SSE behavior and a distinct broker relationship. | Moderate: strengthen navigational staging through the complete files and relate each stage explicitly to its earlier milestone. |
| 31 — Extending MiniGateway | 2,834 | A convincing extension that preserves the model; framing, validation and acceptance are explained separately with useful boundary tests. | Lower: retain the three-excerpt treatment and make the lack of input acknowledgement conspicuous near injection commands. |
| 32 — Architectural Judgment | 3,108 | A strong conclusion. Changed durability, privilege and protocol requirements produce conditional decisions with explicit costs. | Lower: shorten general restatements after the worked decisions; preserve the competing alternatives and their consequences. |
| Appendix A — Reading and Extending | 3,968 | Useful optional source-navigation and extension method, with appropriate public/private API distinctions. | Moderate: emphasize its source-reading purpose and cross-reference Chapters 27/29 instead of repeating their general policies. |
| Epilogue | 1,383 | Consistent with the author's architectural position and provides a recognizable closing voice. | Optional: shorten the philosophical recapitulation if a more decisive ending is desired; Chapter 32 already carries much of the conclusion. |

The chapter structure itself is defensible. I do not recommend another wholesale split/merge exercise on this evidence. Improving transitions and the balance between example and reference would address the larger reading problems with less disruption.

## 5. Technical credibility and limits of the evidence

The previous run records a clean archive build of the pinned framework, 185 framework tests, four external Echo tests, 66 public labs, passing smoke and lifetime suites, and zero source-alignment errors across 33 ordered records and 37 complete marked listings. See the [completed run report](/home/voc/projects/snodec/publications/book/review/pedagogical-smoothing-2026-09-23/REPORT.md:79). These are substantial assets for technical publishing.

Their scope still matters. Exact listing equality protects against book/source drift. It does not prove that every adjacent explanation is complete, that a fresh learner can follow the instructions, or that a supplied teaching architecture meets a different production requirement. A test on a fully equipped workstation does not establish a minimal-installation learning path. The R1 finding illustrates this distinction without invalidating the recorded passing tests.

The manuscript is generally careful about its evidence boundaries. It distinguishes hardware-free Bluetooth checks from radio exchange, Linux process checks from an OpenWrt deployment, current-state SSE from replay, and working HTTP from broker readiness. The benchmark explicitly declines to turn a sequential loopback observation into a capacity figure. Preserve that discipline.

No new framework defect is established by this review. Equally, this report is not a new certification of every framework claim. Independent review should concentrate on the lifetime/callback chapters, TLS policy, HTTP/WebSocket transitions, MQTT interoperability assumptions and database error sequencing, using the edition's archived source and examples. It should also examine the teaching assumptions around callback behavior and single-threaded model use rather than assuming general-purpose guarantees from the concise examples.

## 6. Extent, apparatus and production

| Measure | Current position | Editorial interpretation |
|---|---:|---|
| Baseline extent | 100,338 | Author's comparison baseline, `c7b76c1` |
| Current extent | 110,177 | Freshly measured; identical to saved final metrics |
| Growth | +9,839 / +9.81% | A defensible increase if it pays for explanation and usable examples |
| Author's must threshold | 107,338 | Current extent is 2,839 above it |
| Author's wish threshold | 112,338 | Current extent is 2,161 below it; no editorial reason to fill the difference mechanically |
| Author's ceiling | 115,000 | Current extent has 4,823 headroom |
| Outside fenced blocks | 102,339 | Raw tokens including Markdown, headings, index commands and other markup; not pure rendered prose |
| Inside fenced blocks | 7,838 | Includes fence markers; actual fenced content is 7,118 tokens |
| Teaching units | 32 chapters + Appendix A | 99 objectives and 165 mapped exercises in the recorded apparatus |
| Applied rules | 20 | Enough; more rule boxes are not a priority |

The overall extent is reasonable for the stated ambition. The remaining editorial problem is distribution of attention, not the headline total. A shorter paragraph is useful if it removes a repeated conclusion; an additional paragraph is useful if it resolves an actual missing step. Neither the must nor wish threshold can establish that a chapter teaches well.

The apparatus gives the book a usable instructional rhythm. Three objectives and five exercises everywhere are a good organizing discipline, but identical counts should not force identical kinds of learning. Some subjects need prediction and tracing; others need construction, diagnosis or tradeoff evaluation. Evaluate the quality of the tasks at those boundaries.

The Markdown captions often helpfully distinguish interaction diagrams from ownership or execution order. That is an editorial strength. This review does not establish that the rendered figures and code are readable at the publisher's trim size. A later proof should check figure labels, arrow meaning, code wrapping, continued listings, table breaks, exercise placement, navigation and index entry usefulness. The 326-page reading build is a reported build artifact, not a binding estimate of the finished book's extent.

The existing sample selection—Chapters 1, 3, 19, 30 and 32—is well chosen to show motivation, a first program, lifetime complexity, integration and judgment. For a novice-reader trial, supply Chapters 2 and 3 together so the actual installation path is tested. Samples drawn from distant chapters should retain the present prerequisite note.

## 7. Recommended acceptance evidence

These are recommendations for a subsequent authorized revision, not changes made by this review.

1. **Submission consistency:** Correct the stale length claim, completion status and metrics in the proposal. Confirm that all publisher-facing files describe the same manuscript and clearly separate outstanding author evidence.
2. **First-run usability:** Demonstrate the advertised initial lab route on a clean environment using exactly the listed prerequisites. Account separately for optional development components, services and hardware.
3. **Focused developmental revision:** Resolve the clear local repetitions, improve the densest chapters' example-first entry, and state the scope of the MQTTSuite and OpenWrt exercises accurately. Preserve technical depth and complete listings.
4. **Reader transfer:** Have representative readers complete the first program, explain an ownership/failure observation, and make a small capstone change before seeing its solution. Record where they require assistance.
5. **Independent technical review:** Review the high-risk claims against the archived edition source and rerun relevant examples in the review environment. Report its exact limits.
6. **Production readiness:** Complete copy-editing, permissions and author-delivery arrangements, then proof the final layout and index. Do not infer visual readiness from a successful PDF build.

The manuscript already has a coherent subject, a credible voice and a useful complete application. My recommendation is to invest in the focused revision and validation above. The work should make the reader's path clearer and the submission more trustworthy while retaining the architecture and technical substance that give the book its value.

---

**Review-only record:** No manuscript, companion implementation, test assertion, timeout, source pin or historical report was changed. The only intended repository addition is this review. Fresh metrics and reading helpers were written under the ignored `build/publisher-review/` directory. No new framework or companion runtime result is claimed.
