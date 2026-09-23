# Author scope revision — pedagogical smoothing, 2026-09-23 (one-pass refinement)

Store this prompt verbatim as `review/pedagogical-smoothing-2026-09-23/PROMPT.md`.

---

## 0. What "one pass" means: branch, run, commits

**One pass** means one autonomous refinement run, on one branch, that proceeds through every phase in §10 without asking the author for approval. The phases are internal gates, and each gate ends with a commit. The run is not a single monolithic edit.

**Branch**
- Create `book/pedagogical-smoothing-2026-09-23` from the current tip of `SNode.C-2.0-refinement`.
- The tip must contain `c7b76c108db43de7326a1a63756cf02eed3dbb31`. That is the review baseline, and all `old chNN:line` evidence refers to it.
- If the tip differs from that commit, record the drift and find each piece of evidence by its content, not by line number.
- The book tree must be clean at entry. Untracked build directories are the only exception.

**Commits**
- Make one commit at each gate, in this order: P0a (scope installed), P−1 (prerequisite fix), P0b (entry logs), P1, P2, P3, P4+P5, P6 and P7.
- Checks must pass at every gate.
- Do not squash commits.

## 1. Authority and governing constraints

**Before you start**
1. Read `AGENTS.md` and `review/EDITORIAL-WORK-PLAN.md`.
2. Add a section to the plan named **"Author scope revision — pedagogical smoothing, 2026-09-23"** that points to this prompt.
3. Update `AGENTS.md` so it names this pass as the active scope.
4. Where this prompt conflicts with an earlier constraint, this prompt wins. Every earlier constraint that does not conflict still applies.

**This pass explicitly supersedes**
- the 105,000-token stretch target, which is replaced by the budget in §4;
- the chapter-structure freeze: two splits are approved (§5);
- the proposal-readiness checkers (`review/proposal-readiness-2026-09-22/check-phase-*.py`) as active gates. They stay historical and must not be edited.

**Constraints that still apply**
- The hard ceiling of **115,000** tokens.
- Preserve the author's voice, technical depth, cumulative progression and the MiniGateway capstone.
- At most **20 rule boxes**. There are 20 now, so add none; move one if a split requires it.
- No code listing may be cut to meet a budget.
- Distinguish deliberate pedagogical reinforcement from repetition that adds nothing.
- The Markdown inputs in `manuscript/book-files.txt` are the manuscript authority. Regenerating the PDF is separate work.

**What "refine, don't replace" means here.** Preserve substantive content, technical claims, examples and the author's voice. You may reorder, split and merge material, and rewrite sentences or paragraphs, wherever this prompt requires it. New passages are allowed where §6 says **add**. Do not replace a technically sound treatment with a different conceptual treatment merely for style.

**Source authority**
- The source authority is the author's working tree at `/home/voc/projects/snodec/snode.c`, including uncommitted changes.
- Do not substitute `master`, a remote branch or a recorded base commit. Do not modify the framework.
- **Freeze record.** At P0a, record the framework's `git rev-parse HEAD`, its `git status --porcelain=v1`, a digest of `git diff HEAD --binary`, and a sorted `sha256sum` list of the contents of every untracked, non-ignored file (`git ls-files --others --exclude-standard`).
- Repeat that record before the first API verification in P3 and again at P7.
- If the tree has changed, stop and report (§14). Never certify against a moving source.

## 2. Diagnosis: why this pass exists

Two independent reviews converged on one diagnosis. The book has enough technical depth and explicit reasoning. Its weakness is **uneven pedagogical spacing**: concepts, identifiers and listings arrive faster than the explanation that connects them. The problem shows up in two clusters:

- **Early chapters (new Ch1–6).** Mental models are named before the reader has formed them.
- **Later chapters (new Ch18, 21, 25–27, 30–32).** API and build inventories, and listings without interpretation, take the place of narrative.

**Goal.** Make depth arrive at an even rate across all eight dimensions (§9). Growth is a means, not a target.
- Every added word must serve a register row (§8).
- Every change must improve its chapter's weakest dimension without worsening another.
- Added text should not materially worsen identifier density or abstract-noun density unless there is a pedagogical reason, such as a required concrete example. These metrics are diagnostics, not optimization targets.
- Chapters grow by different amounts, and some shrink.

Do not re-score or re-argue the diagnosis; implement it. If the source contradicts an instruction, follow the source and report the conflict.

## 3. Author decisions (settled)

| ID | Decision |
|---|---|
| D1 | **Split old Ch4 and old Ch24** (§5). The book then has 32 numbered chapters in 11 Parts, plus Appendix A. |
| D2 | **Canonical vocabulary** as in §7. |
| D3 | **No SNode.C 2.0 tag yet.** The reconstruction mechanics live only in one **"Edition and source baseline"** sidebar in Ch2 and in `source-baseline/SOURCE-VERSION.md`. The Preface keeps its one-sentence statement of which version the book covers. All other prose states behavior only. |
| D4 | **Worked decisions for new Ch32:** (a) where persistence belongs, drawing on Ch24; (b) when a role deserves its own process, drawing on Ch31; (c) when reusing a protocol across network families should stop, drawing on Ch12. |
| D5 | **Old ch13:68.** Delete "or handshake claims", so the sentence ends "…not CMake component names." Rephrase the migration sentence only if the reader needs it operationally: "Older code may still include `SemanticLog.h`; new application code includes `Log.h`." Otherwise delete it. |
| D6 | **Benchmarking stance** in new Ch29: "This book reports no performance figures. It uses SNode.C to teach layered network programming; this section teaches how to measure and interpret a workload, not what capacity to expect." The statement is about the book's purpose, not a characterization of the framework. |

## 4. Word budget

**Method.** Count with `ci/manuscript-metrics.py`: `str.split` tokens over the raw inputs in manifest order, markup included. The baseline is **100,338**.

| Global target | Tokens |
|---|---|
| Must (+7,000) — cannot be waived | at least **107,338** |
| Wish (+12,000) | about **112,338** |
| Hard ceiling | at most **115,000** |

**Per-chapter floors and caps** are listed in §6. The floors sum to **107,783**; the caps sum to **114,876**.
- **Floors** are planned minimums. A chapter may end below its floor only with a documented waiver in `floor-waivers.md`. The waiver must state which rows' work is complete (with evidence), why more text would be padding, and which higher-priority chapter(s) with open cap headroom recover the shortfall.
- **Caps** may be exceeded by at most 5%, again with a documented waiver. The global ceiling is absolute.

**How to grow**
- Growth is prose. Fenced tokens (8,151 at baseline) stay within ±5%, apart from the listing changes named in §6.
- When budgets conflict, the **smaller rank number** (the higher-priority issue in §8) wins.
- Measure after every phase.
- If the projected total exceeds **113,500** before P5, skip the optional rows 30 and 31 and report it.

## 5. Structure changes

**Chapter map (old → new)**

| Old | New | Title (file) |
|---|---|---|
| 1–3 | 1–3 | Unchanged |
| 4, first half: § "The mental model" through § "Configuration, callbacks, and observable behavior" | **4** | **The SNode.C Runtime Mental Model** (`04-the-snodec-runtime-mental-model.md`) |
| 4, second half: § "Reading public types and components" to the end | **5** | **Layers in Practice** (`05-layers-in-practice.md`) |
| 5–23 | 6–24 | Titles unchanged; files renumbered |
| 24, first part: § "Reading complete applications" through § "Read applications beside consumer examples and tests" | **25** | **Reading Complete SNode.C Applications** (`25-reading-complete-snodec-applications.md`) |
| 24, second part: § "From applications to systems" to the end | **26** | **From Applications to Systems: MQTTSuite** (`26-from-applications-to-systems-mqttsuite.md`) |
| 25–30 | 27–32 | Titles unchanged; files renumbered |

These split points follow the chapter boundaries that existed before the Phase 4 consolidation (old 5+7 and old 29/30/31).

**Parts**

| Part | I | II | III | IV | V | VI | VII | VIII | IX | X | XI |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Chapters | 1–3 | 4–6 | 7–9 | 10–12 | 13–14 | 15–16 | 17–20 | 21–23 | 24–26 | 27–29 | 30–32 |

Part checkpoints stay at the end of each Part's last chapter. The Part II checkpoint is now in Ch6, and the Part IX checkpoint moves to the end of Ch26.

**Anchors and chapter references**
- Keep every existing heading anchor resolvable, and delete none. A former chapter-level anchor stays on the section that now carries its topic. New chapter headings get new IDs.
- Renumber every "Chapter N" reference using the map above, and verify each one against its topic, not by arithmetic.
- In `review/pedagogical-smoothing-2026-09-23/`, create:
  - `smoothing-structure.json`, holding the chapters, the old→new map, Parts, topic anchors, and floors and caps;
  - `smoothing-reference-register.json`.
- Point `ci/check-chapter-references.py` and `ci/test-chapter-references.py` at these files and at 32 chapters. Leave the historical JSON files unchanged.

**Companion exercises**
- Rename the `companion/exercises/chNN` directories, starting from the highest number so names never collide.
- Split `ch04` into `ch04` and `ch05`, and old `ch24` into `ch25` and `ch26`.
- Update:
  - the `foreach` list in `companion/exercises/CMakeLists.txt`;
  - every lab and CTest target name (`exercise-chNN-…`, `chNN-lab`);
  - relative paths between exercise directories (for example `../ch17/dispatch.py` → `../ch18/dispatch.py`);
  - chapter-text references to those names;
  - CI scripts that name directories, such as `ci/run-example-lifetime-tests.py` (ch19→ch20) and `ci/run-teaching-smoke-tests.py` (ch13→ch14) — find the rest with grep;
  - `.github/workflows`, if it references any of these.

**Source-alignment registry and other structure-sensitive data** (part of P2)
- `ci/check-source-alignment.py` requires `review/verification/source-claims.json` to hold exactly one record per ordered chapter and for Appendix A, in manifest order. Each record's `chapter` number must match its file prefix.
- Update this file for the 32-chapter structure:
  - Renumber the records and their `manuscript` paths.
  - Split the old Ch4 record into Ch4 and Ch5, and the old Ch24 record into Ch25 and Ch26.
  - Assign each `framework_sources` and `companion_sources` anchor to the chapter whose prose now carries the claim, and divide `reviewed_contract` by its clauses.
  - Drop no anchor. Change no `path`, `line` or `needle`.
  - Leave `framework_manifest` and `reviewed_tree_sha256` unchanged.
  - Record the dispatch listing added to Ch18 and the marked listing removed from Ch31.
- Do not weaken any check and do not change any technical claim to make a check pass.
- Grep `ci/`, `review/` (outside historical pass folders), `source-baseline/`, `production/`, `packaging/` and `companion/` for chapter file names, `chNN` names and chapter counts. Update every live registry you find.
- Historical pass folders stay unchanged: `review/proposal-readiness-2026-09-22/`, `review/editorial/`, `review/followup-2026-09-21/`, `review/pdf-*`, `review/index/` and `review/verification/refinement-2026-09-21/`.
- List every registry you changed in the report.

**Other references**
- Update `manuscript/book-files.txt`, the openers of Parts II, IX, X and XI, the chapter lists and shortcut routes in "How to Read This Book", `STRUCTURE.md`, and `README.md`.
- Update the proposal sample list in `review/proposal/CMakeLists.txt` and the proposal texts: samples 1, 3, 18, 28, 30 become **1, 3, 19, 30, 32**.
- Take proposal word counts from the metrics. Mark page counts "pending PDF rebuild" unless the PDF was rebuilt.
- Record the new structure in the work plan (including its "Chapter ledger" section) and in a new `review/pedagogical-smoothing-2026-09-23/chapter-ledger.md`, created for this pass. Do not edit `review/proposal-readiness-2026-09-22/chapter-ledger.md`; it is historical.

### 5a. Apparatus for the split chapters

**Two stages**
- **P2 (mechanical).** Move the existing objectives, exercises, CTests and public answers into the chapter where each belongs, using the mapping below. Mark each missing item with the literal placeholder `TODO(P3-apparatus)`.
- **P3 (pedagogical).** After the chapter's content work is done, write the final objectives and the remaining items so they match what the revised chapter actually teaches. The apparatus gate runs at the end of P3.

**Rules for every lab**
- Each lab tests a **distinct objective**.
- Labs reuse canonical implementations. Add no new application code beyond thin driver arguments.
- An existing experiment may be reused only if the chapter asks it a **different question** and the exercise text states the new observation. The book already works this way: old ch25 and Appendix A rerun `ch02/solution.py`.
- No conceptual forward dependency. A later chapter's program may be run only if everything needed to interpret the result is taught in or before the current chapter.
- Prefer at least one lab per chapter that runs without optional equipment; if that is not feasible, report it.
- Public answers go in `companion/exercises/chNN/README.md`.

**New Ch4 — Runtime Mental Model**

Objectives cover: the lifetimes of handle, instance, flow, connection and context (old O1); identifying these runtime objects in a running program (new); per-peer versus shared state ownership (old O3).

| # | Exercise |
|---|---|
| 1 | **Review** — old Ex1 (lifetime independence). |
| 2 | **Review, new** — Attribute each line of a short EchoPair log excerpt to a handle, instance, flow, connection or context. Use existing EchoPair output; no new code. |
| 3 | **Lab** — old Ex3, test `exercise-ch04-model-instances`, kept as is. |
| 4 | **Lab** — old Ex4, test `exercise-ch04-independent-peers`, kept as is. |
| 5 | **Design, new, runtime only** — Add a second client flow against the same server and assign per-connection, per-flow and shared state. No layer changes. |

**New Ch5 — Layers in Practice**

Objectives cover: decoding a type, header and component (old O2); predicting which layer a change touches and what stays unchanged (new); confirming a layer decision through the component request (new).

| # | Exercise |
|---|---|
| 1 | **Review** — old Ex2 (decode `net::rc::stream::tls::SocketServer<MyFactory>`). |
| 2 | **Review, new** — For three changes (IPv4→Unix, legacy→TLS, echo→line protocol), name the affected layer, type, header and component, and what stays unchanged. |
| 3 | **Lab, new observation** — The same echo context built against two network-family headers, IPv4 and Unix only. Candidate implementation: the family-server targets, now in `exercises/ch07`. Identical replies are observed while only type, header and component differ. The lab must not rely on Ch7's address-semantics teaching. |
| 4 | **Lab, new observation** — The component mode of `ch02/solution.py`. The matching component configures and links; a missing component fails. Name the layer the missing component represents. |
| 5 | **Design** — old Ex5, reduced to layer decisions: type, header and component changes, and what stays shared. Its ownership part moves to Ch4's design exercise. |

**New Ch25 — Reading Complete Applications**

Objectives cover: tracing a build target through the composition root to an observable contract (old O1); reading an entry point as an assembly point (new); relating an application to its consumer example and tests (new).

| # | Exercise |
|---|---|
| 1 | **Review** — old Ex1. |
| 2 | **Review, new** — For one `src/apps` entry point, list the handles, instances and components it assembles, and predict one observable behavior. |
| 3 | **Lab** — old Ex3, renamed `exercise-ch25-composition`. |
| 4 | **Lab, new observation** — The consumer mode of `ch02/solution.py`, read as a trace: target → `main()` → linked components → the echo contract. The question is reading the application, not verifying the environment. |
| 5 | **Design, new** — The reading order you would follow, and the three observations you would make, before modifying an unfamiliar application. |

**New Ch26 — From Applications to Systems: MQTTSuite**

Objectives cover: separating process recovery, accepted state and durable storage (old O2); assigning broker, mapping, bridge and storage responsibilities (old O3); tracing one publication across processes (new).

| # | Exercise |
|---|---|
| 1 | **Review** — old Ex2. |
| 2 | **Review, new** — For each step of the worked publication trace, name the owning process and what each tool's observation proves. |
| 3 | **Lab** — old Ex4, renamed `exercise-ch26-part-checkpoint`. This is the equipped Part IX checkpoint. |
| 4 | **Lab, new observation** — A broker-mediated publication observed at publisher and subscriber. Candidates: the MQTT broker and role labs, now in `exercises/ch21`. Ask it as a system question: which responsibility produced each outcome? Prefer an unequipped run. |
| 5 | **Design** — old Ex5. |

## 6. Chapter table

"Now" is the current raw token count. Rows refer to §8; dimension letters refer to §9. **Add** marks where new passages are authorized.

| New | Old | Title | Now | Floor | Cap | Rows | Required work | Dim |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | 1 | Why SNode.C Exists | 1,821 | 2,400 | 2,670 | 2, 25, 18 | **Add** a problem runway before the ownership vocabulary: one endpoint → several → another protocol → shared state → operational configuration. Then motivate the layered idea briefly; defer the detailed layer model and its vocabulary to Ch5. Keep the Asio/EchoPair comparison (old ch01:52), with one sentence saying the SNode.C side is explained in Ch3. Move the edition paragraph (old ch01:139) to the Ch2 sidebar. | E, G |
| 2 | 2 | Preparing Your Environment | 3,006 | 3,006 | 3,250 | 5, 18 | After one short orienting paragraph, put a **"Shortest path to Chapter 3"** box: source → configure → build → install → verify the package → build EchoPair → continue. The environment architecture follows. Create the **Edition and source baseline** sidebar, holding the patch and alignment mechanics (including old ch02:146) and the provenance text moved from Ch1, 6, 14, 26 and 29 and from Conventions. | G, L |
| 3 | 3 | Your First Working Program: The Echo Pair | 2,568 | 3,000 | 3,270 | 2, 25, 16 | Move the side references (`--log-level=5`, `src/apps/echo`, `examples/echo`, the Ch27 pointer) out of the first paragraph. **Add** a chronological trace before the file walkthrough: `main()` → configure server → `listen()` → configure client → `connect()` → `start()` → connection → factory → context attached → `onConnected()` → bytes arrive → `onReceivedFromPeer()` → `sendToPeer()`. Map each step to one of the four files, and name the abstractions only after the trace. | E, G, T |
| 4 | 4a | The SNode.C Runtime Mental Model | 1,992 | 2,700 | 3,050 | 3, 2, 16 | Bridge from Ch3's trace. This is the **only** place the taxonomy is tabulated: figure `fig:snodec-runtime-model` plus one terminology box covering handle → instance → flow → connection → factory → context and their lifetimes. **Add** a small example for each distinction and an observation checkpoint. Apparatus per §5a. | S, G, C |
| 5 | 4b | Layers in Practice | 2,083 | 2,875 | 3,325 | 3, 2 | Opening bridge: with the runtime objects fixed, what can change beneath a context? Walk network family → transport form → connection variant → application protocol, mapped to types, headers and components. **Add** spacing between the layers. Apparatus per §5a. | S, G |
| 6 | 5 | Core Runtime and Event Processing | 2,983 | 3,500 | 3,850 | 4, 28, 18 | **Add** a bridge and an event-loop thought experiment (peer A readable, retry timer due, queued callback, peer B read timeout) that walks wait → dispatch → queued work → timeouts → cleanup, placed before any source excerpt. Move the descriptor publisher/receiver population section to Appendix A. Turn old ch05:89 into reader guidance; its provenance goes to Ch2. At the Part II checkpoint (old ch05:252), print the ~5-line `MeasurementModel` interface excerpt. | G, E, C |
| 7 | 6 | Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 4,175 | 4,175 | 4,250 | 26 | Keep as one chapter. Fix the section opening at old ch06:248 so the comparison exists before it is used. Merging micro code blocks is optional. | S |
| 8 | 7 | Servers, Clients, and Connections | 3,084 | 3,150 | 3,334 | 31, 16 | Replace the opening re-tabulation with a reference to Ch4. **Add** a single-peer timeline (listen → accept → context → data → close) before the recovery and callback-layer distinctions. | T, C |
| 9 | 8 | Bluetooth in SNode.C: RFCOMM and L2CAP | 2,170 | 2,120 | 2,220 | 1, 15 | Terminology and seams only. | — |
| 10 | 9 | Writing `SocketContext` Classes Well | 3,089 | 3,040 | 3,140 | 1, 15 | Terminology and seams only. Reference model. | — |
| 11 | 10 | Writing `SocketContextFactory` Classes Well | 2,265 | 2,215 | 2,315 | 1, 15 | Terminology and seams only. Reference model. | — |
| 12 | 11 | Building the Same Protocol over Different Lower Layers | 2,555 | 2,505 | 2,605 | 1, 15 | Terminology and seams only. This chapter has the heaviest *carrier* normalization (26 uses). | L |
| 13 | 12 | Configuring Applications and Named Instances | 4,273 | 4,300 | 4,673 | 10, 16 | Introduce one running value, the **`echoserver` local port**, in the first section. Follow it through C++ default → file → CLI → effective value → help/discovery → validation → runtime use. Each later section returns to it before generalizing. Refer to Ch4 instead of re-tabulating the taxonomy. | G, T |
| 14 | 13 | Logging, Diagnostics, and Runtime Introspection | 2,698 | 2,650 | 2,800 | 20, 18 | Keep the opening. Apply D5 at old ch13:68. Rewrite old ch13:30 as explained steps. Explain the four construction functions through one example before their table. | X, L |
| 15 | 14 | TLS Across the Framework | 2,579 | 2,700 | 2,900 | 24, 15 | Open with a bridge from diagnostics. **Add** one configured-TLS box (server certificate and key, client trust and expected identity), excerpted from the renamed `companion/exercises/ch15` sources where possible. No new internals. | T, C |
| 16 | 15 | Timeouts, Retries, and Failure Modes | 2,990 | 3,200 | 3,390 | 14 | Before the internal excerpts (old ch15:108, :129), **add** the application-facing configuration: C++ setters and the CLI equivalent, as in the renamed `ch16/recovery.py`. Keep the internals only to explain why retry and reconnect differ. A text timeline is optional. | T |
| 17 | 16 | The HTTP Layer | 2,471 | 2,450 | 2,600 | 17 | Add a Build note and end on a transition to routing. Otherwise a reference model. | S |
| 18 | 17 | The Express-Like Framework | 2,065 | 2,050 | 2,315 | 7, 16, 17 | Early in the chapter, print the renamed `companion/exercises/ch18/dispatch.cpp` as a **marked complete listing**. Trace one request (app middleware → mounted router → router middleware → handler) and show the `/blocked` short-circuit. Only then `WebAppT` and `Controller`. Collapse the method, facade, dispatcher and middleware tables into **one** reference box placed after the mechanism. Remove the handle recital. Add a Build note and end on a transition to SSE. | T, D, G |
| 19 | 18 | Server-Sent Events and Real-Time HTTP | 3,269 | 3,220 | 3,370 | 17 | Build note only. Reference model. | S |
| 20 | 19 | WebSocket and Protocol Upgrade | 3,000 | 2,950 | 3,100 | 1, 15 | Terminology and seams only. Reference model. | — |
| 21 | 20 | MQTT Support in SNode.C | 2,005 | 3,000 | 3,405 | 8, 17, 19 | **Add** an opening text-diagram conversation — CONNECT → CONNACK → SUBSCRIBE → SUBACK → PUBLISH → subscriber receipt — stating what each step proves. Distinguish the TCP connection, the MQTT session, subscription acceptance, publication submission and application delivery. Only then introduce `Mqtt`, `MqttContext`, `Session` and `Topic`, with at most two class tables. Define *carrier* briefly at its first use here (§7). Add a Build note and end on a transition to MQTT over WebSocket. | D, E, G |
| 22 | 21 | MQTT over WebSocket | 1,782 | 2,100 | 2,282 | 30, 17, 19 | **Add** a side-by-side trace: native (TCP → MQTT) versus composed (TCP → HTTP Upgrade → WebSocket binary message → MQTT), with the failure evidence available at each step. Use *carrier* as defined in Ch21 (§7). Rewrite old ch21:63. Build note. | T, X |
| 23 | 22 | Designing IoT Systems with Multiple Protocols | 2,922 | 3,100 | 3,222 | 29, 19 | **Add** one worked before/after design decision. Ground the abstract-noun clusters in concrete actors; "boundary" alone appears 48×. | T, X |
| 24 | 23 | Database Support and Application State | 3,826 | 3,826 | 3,926 | 15 | Exit bridge to Ch25. | C |
| 25 | 24a | Reading Complete SNode.C Applications | 2,018 | 2,450 | 2,600 | 6, 15 | Bridge from Ch24. Remove the incidental app-name inventory (old ch24:21). Keep the sequence build target → composition root → linked components → entry point → observable contract. Apparatus per §5a. Exit bridge to systems. | S, E |
| 26 | 24b | From Applications to Systems: MQTTSuite | 3,573 | 3,750 | 3,941 | 6, 15, 18, 19 | Opening bridge. Move old ch24:454 to Ch2. Ground the abstract-noun clusters. The Part IX checkpoint goes at the end. Apparatus per §5a. | S, C |
| 27 | 25 | CMake Components, Public Headers, and Linking Strategy | 3,903 | 3,700 | 4,000 | 9, 19 | Open with a minimal consumer: `find_package(snodec REQUIRED COMPONENTS net-in-stream-legacy)` plus `target_link_libraries(app PRIVATE snodec::net-in-stream-legacy)`. Ask why one component is enough and where the lower dependencies come from, then unfold the rest from there. The framework's top-level CMake and compiler flags come after. Replace the 99-line tree with a reference box of at most 40 lines showing the consumer's subgraph; add a full-graph figure only if the figure build passes. Rewrite old ch25:320. | T, E, G |
| 28 | 26 | Deployment on Linux and OpenWrt | 3,596 | 3,546 | 3,646 | 15 | Seams only. Reference model. | C |
| 29 | 27 | Testing, Debugging, and Benchmarking | 4,169 | 4,300 | 4,500 | 21, 22, 18 | **Add** a problem-first opening before the taxonomy and commands (old ch27:14): a unit test passes but the installed consumer fails; a correct build talks to the wrong endpoint; a local latency figure is not capacity. Add the D6 stance. Move old ch27:54 to Ch2. | E, D |
| 30 | 28 | Building MiniGateway | 3,818 | 4,400 | 4,618 | 11, 15 | After every listing (old ch28:296–1195), **add** 1–3 sentences: which responsibility was implemented, what it deliberately does not know, which invariant now holds, and why the next file follows. **No new code.** Bridge from Part X. | T |
| 31 | 29 | Extending MiniGateway with a New Network Role | 2,541 | 2,650 | 2,841 | 12 | Replace the 147-line marked listing (old ch29:362) with three unmarked excerpts — framing/buffering, parse/validation, acceptance — with explanation between them, and point to the complete companion file. The architecture is otherwise unchanged. | T |
| 32 | 30 | Architectural Judgment: Choosing the Right Layer and Boundary | 1,850 | 3,100 | 3,350 | 13 | **Add** the three D4 worked decisions. Each gives the requirement, the options, the criteria from the five questions, and a verdict with its consequence. The role disclaimer at old ch30:20 becomes unnecessary. | D |
| A | A | Reading and Extending the Framework | 3,694 | 3,900 | 3,994 | 23, 4 | Rewrite the opening (appA:24) so it works both after Ch3 and after the Epilogue. Receive Ch6's descriptor-population material as a source-reading section. | E, C |
| Front | — | Conventions and other front matter | 1,980 | 2,280 | 2,430 | 1, 18 | Add the glossary (§7). Remove the verification-coverage note from Conventions and reword its source-package pointer to point to the Ch2 sidebar. Renumber "How to Read This Book". | L |
| Parts | — | Part openers | 1,356 | 1,356 | 1,456 | 3, 6, 15 | Update the openers of Parts II, IX, X and XI. | C |
| Epi | — | Epilogue | 1,388 | 1,338 | 1,438 | 15 | Seam only. | C |
| Back | — | Back matter | 781 | 781 | 800 | — | Update the solution paths in Further Reading. | — |

**Build note format.** `::: {.snodec-note title="Build note"}` holds the chapter's `#include` and component material. It sits before the transition paragraph, which comes before "What to remember".

**Reference models** keep their structure: Ch10, 11, 12, 17, 19, 20, 28, and the architecture of Ch31. For style, follow Ch10, Ch14's opening, Ch19, Ch20 and Ch31.

## 7. Canonical vocabulary (D2)

Add a glossary to Conventions. Normalize the whole manuscript, including front matter, Part openers and exercises, judging each occurrence in context. Record counts before and after in `terminology-counts.md`. Any justified survivor of a deprecated form goes in `terminology-allowlist.md` with its reason; typical cases are exact type or API names, quotations, and historical file names.

| Concept | Canonical term | Replace | Notes |
|---|---|---|---|
| Object in application code that configures a server or client (`SocketServer`, `SocketClient`, `WebApp`, …) | **endpoint handle** ("handle" after the first use in a chapter) | — | The definition already exists in Conventions |
| The configuration-and-runtime identity a handle creates | **instance** | configured role, registered instance, configuration instance, runtime-visible role, endpoint role, configured endpoint | Do not use "instance" for a plain C++ object; say "object" |
| An instance that is addressable through configuration, CLI and logs | **named instance** | named endpoint; "server instance" / "client instance" when they mean this | |
| An unnamed instance | **anonymous instance** | — | |
| One `listen()`/`connect()` activation and its controller | **flow**, **flow handle** | — | "activation flow" is allowed as the full form |
| One peer relationship (`SocketConnection`) | **connection** | peer episode, connection episode | |
| The per-connection protocol object (`SocketContext`) | **context** | — | |
| The creator of contexts (`SocketContextFactory`) | **factory** | — | |
| IPv4, IPv6, Unix domain, RFCOMM, L2CAP | **network family** | lower family, communication family, lower communication family | Matches the Ch7 title and the Ch5 "network layer" |
| Stream versus other forms | **transport form** | — | |
| Legacy versus TLS | **connection variant** | — | |
| Native stream versus WebSocket beneath MQTT | **carrier** | every other use → the precise term above | Book coinage, absent from framework source. Define it at its first use in Ch21; use it only in Ch21–22. Test and target names containing "carrier" may be renamed. |
| A design responsibility in a system (web role, MQTT uplink role) | **role** | "server role" / "client role" → "server side" / "client side" | Narrow Conventions' broad definition to match |
| The model's authoritative state transition | **acceptance**, **accepted state** | — | |

## 8. Ranked issue register

When budgets or rows conflict, the **smaller rank number wins**. Chapter numbers are new.

| Rank | Issue | Chapters | Dim |
|---:|---|---|---|
| 1 | Terminology is not canonical; *carrier* has three meanings | book-wide | L |
| 2 | Steep initial gradient: mental models are named before they are formed | 1–6 | G |
| 3 | Old Ch4 merged two chapters | 4, 5 | S |
| 4 | Source internals come before a simple event-loop model | 6 | G |
| 5 | No shortest path to the first program; meta-architecture comes first | 2 | G |
| 6 | Old Ch24 held three units | 25, 26 | S |
| 7 | Express is taught through inventories; the example exists only in the lab | 18 | T |
| 8 | MQTT is introduced through class vocabulary, not a conversation | 21 | D |
| 9 | The CMake chapter is an inventory, not a problem | 27 | T |
| 10 | Configuration is many concepts, not one story | 13 | G |
| 11 | Capstone listings have no interpretation | 30 | T |
| 12 | A 147-line listing | 31 | T |
| 13 | The synthesis rests on one worked decision | 32 | D |
| 14 | Application-side retry/reconnect configuration is not on the page | 16 | T |
| 15 | Weak seams: 14→15, 24→25, 28→29→30, Epilogue→App A, plus the new seams 3→4, 4→5, 5→6, 25→26, 26→27 | book-wide | C |
| 16 | The taxonomy is re-taught with fresh tables | 3, 4/5, 8, 13, 18 | C |
| 17 | Chapters end on `#include`/component housekeeping | 17, 18, 19, 21, 22 | S |
| 18 | Edition and verification voice in learner prose | 1, 2, 6, 14, 26, 29, Conventions | L |
| 19 | Abstract-noun chains (old ch21:63, old ch25:320) | 21–27, 29–32 | X |
| 20 | Compressed and migration-history wording | 14 | X |
| 21 | The testing chapter opens with commands | 29 | E |
| 22 | The stance on performance figures is unstated | 29 | D |
| 23 | Appendix A's opening assumes a reading position | A | E |
| 24 | The TLS page is weaker than the TLS lab | 15 | T |
| 25 | First contact should be experiential before formal terms | 1, 3 | E |
| 26 | Internal seam at old ch06:248 | 7 | S |
| 27 | Global rule: the core mechanism must be understandable without the lab | all | T |
| 28 | The Part II checkpoint depends on code printed 24 chapters later | 6 | C |
| 29 | The IoT design chapter has no worked case | 23 | T |
| 30 | No native-versus-WebSocket composition trace | 22 | T |
| 31 | Distinctions arrive before a single-peer timeline | 8 | T |

## 9. Dimension rules (acceptance for every chapter)

These rules are judged pedagogically. The automated checks in §12 either **assert** a row-specific structural fact or **report** a heuristic. A reported number never justifies an edit made only to move it.

| Dim | Rule | Evidence | Model |
|---|---|---|---|
| **E: Entry** | The first 1–3 paragraphs state the problem, why it matters, and how it connects to the previous chapter, before any command, listing or inventory table carries the explanation. | Manual, recorded in `seam-log.md`; reported: prose words before the first non-prose block | 10, 17, 24 |
| **D: Depth** | Major topics go what → how → why → consequence → limitation at the level of the reader's API. Internals appear only where they explain behavior the reader can observe. | Manual | 10, 11, 19, 24 |
| **G: Gradient** | problem → simple model → example → name → mechanism → observation → generalization. | Manual; reported: new identifiers per 1k tokens and in the first 400 words (book medians about 11 and 6) | 10–12 |
| **X: Explicitness** | No sentence depends on stacking three or more of {boundary, role, surface, policy, carrier, owner, ownership, observation} without a concrete actor. Every coined phrase is defined or replaced. | Reported cluster list plus manual rewrite | 19 |
| **T: Theory–example** | concept → small example → explanation of the example → consequence. Prose follows every listing. The core mechanism is understandable without opening the lab. | Manual; assertions for rows 7, 11 and 12 | 3, 19 |
| **L: Language** | Canonical terms (§7). Provenance mechanics appear only in the Ch2 sidebar. | Assertions (§12) | Conventions |
| **S: Structure** | One learning cycle per chapter. Tail order: … → Build note (where one applies) → transition paragraph → What to remember → Exercises. | Assertion for row 17; reported for all chapters | 31 |
| **C: Continuity** | The end of chapter N states the reader's model and N+1 opens from it. The taxonomy is tabulated only in Ch4. Nothing depends on code first printed later. | Manual, in `seam-log.md` | 10→11→12, 17→20 |

## 10. Phases and gates

**P0a — Preflight (no manuscript or companion edits).**
- Create the branch from the tip described in §0, and check that the tree is clean.
- Read `AGENTS.md` and `review/EDITORIAL-WORK-PLAN.md`.
- Install this prompt as `PROMPT.md`, add the work-plan section, and update `AGENTS.md` (§1).
- Make the framework freeze record (§1). If the working tree is unavailable, stop (§14).
- Commit: "review: install pedagogical-smoothing scope".

**P−1 — Known baseline prerequisite (its own commit, narrowly scoped).**
- Static inspection shows that no C++20 requirement reaches several exercise targets. The framework sets `CMAKE_CXX_STANDARD 20` only for its own build. Neither the companion's `CMakeLists.txt` nor `ci/build-companion-examples.sh` sets a standard.
- Add `target_compile_features(<target> PRIVATE cxx_std_20)` to exactly these targets (old directory names):

  | Directory | Targets |
  |---|---|
  | ch06 | `endpoint-${family}` |
  | ch08 | `endpoint-${family}` |
  | ch10 | `line-refusal` |
  | ch11 | `line-unix` |
  | ch14 | `tls-policy-lab`, `tls-echo` |
  | ch19 | `ws-lab-${side}` |
  | ch20 | `mqtt-role-lab`, `mqtt-broker-lab` |
  | ch21 | `mqtt-ws-lab` |

- Verify with a compiler whose default standard is below C++20, if one is available.
- Change nothing else. Commit: "companion: request C++20 for every exercise target".

**P0b — Entry checks.**
- Save `metrics-before.json`.
- Run all existing checks and labs, and keep the entry logs.
- Gate: everything passes. Any failure stops the run (§14); the P−1 defect has already been fixed at this point.
- Commit the entry logs.

**P1 — Vocabulary** (row 1).
- Add the glossary and normalize terms.
- Record the counts and the allowlist.
- Commit.

**P2 — Structure, mechanical** (rows 3 and 6).
- Splits and file renames; manifest, Part openers and anchors.
- Renumber references by topic; write the new JSON files; update the reference checker and its test.
- Rename companion directories and update CMake, CI and workflows.
- Move the existing apparatus (§5a) and add placeholders.
- Update `review/verification/source-claims.json` and every other live structure-sensitive registry (§5).
- Update the proposal, `STRUCTURE.md` and `README.md` references.
- Gate: the reference checker, source alignment, companion build and all labs pass. The apparatus check is deferred for Ch4, 5, 25 and 26. Commit.

**P3 — Tier 1 content** (rows 2–13, plus row 25 for Ch1 and Ch3).
- Work in rank order: Ch1–6, 13, 18, 21, 25–27, 30–32.
- Then write the §5a apparatus for Ch4, 5, 25 and 26.
- Re-check the framework freeze before the first API verification.
- Gate: every chapter passes the apparatus check, no `TODO(P3-apparatus)` remains, and all labs pass. Commit.

**P4 — Tier 2** (rows 14–23). **P5 — Tier 3** (rows 24 and 26–31; row 27 is a sweep over every chapter). Commit once after both.

**P6 — Seam pass.**
- For every consecutive pair, including Part openers, the Epilogue and Appendix A, read the last 1–2 paragraphs of N against the first 2–4 of N+1.
- Log each pair in `seam-log.md`, including entry and continuity notes.
- Commit.

**P7 — Exit.**
- Save `metrics-after.json`.
- Run all checks and labs, plus `check-smoothing.py`.
- Repeat the framework freeze record.
- Write the report, and update the work plan and this pass's `review/pedagogical-smoothing-2026-09-23/chapter-ledger.md`.
- Commit.

## 11. Preservation and verification

**Protected counts**

| Item | Phase 5m baseline | Required after the pass |
|---|---|---|
| Exact source markers | 37 | 37: Ch31 −1, Ch18 +1. Explain any other change. |
| Index entries | 1,033 | At least 1,033; new sections get entries. |
| Figure IDs | 18 | At least 18, all resolvable. |
| Executable/config fences | 293 | Report the change; only the Ch31 presentation change may reduce code. |
| Public labs | 62 | At least 62, all passing. |
| Rule boxes | 20 | At most 20. |

**Size limits.** Front matter at most 2,500 tokens; Part openers at most 1,650.

**API verification**
- Verify every C++ identifier in new or changed code against the frozen working tree, and report it as `header:line`.
- These hints were verified on base `1f0f728` plus the edition patch; re-verify them:
  - `setRetry`, `setRetryOnFatal`, `setRetryTimeout`, `setRetryTries` (where 0 means unlimited), `setRetryBase`, `setRetryLimit` and `setRetryJitter` are declared in `src/net/config/ConfigPhysicalSocket.h:83–101`.
  - `setReconnect` and `setReconnectTime` are declared in `src/net/config/ConfigPhysicalSocketClient.h:70–73`.
  - `getConfig()` returns `Config*` (`src/core/socket/Socket.h:73`).

**Listings.** Printed complete listings must equal their companion files exactly. Label excerpts as excerpts and leave them unmarked.

**Checks to run**, each as the Phase 5m exit logs record it:
- `ci/manuscript-metrics.py`
- `ci/check-chapter-references.py` (updated)
- `ci/check-source-alignment.py --framework <working tree>`
- `ci/check-source-hygiene.sh`
- `ci/build-companion-examples.sh`
- `ci/run-teaching-smoke-tests.py`
- `ci/run-behavior-smoke-tests.sh`
- `ci/run-example-lifetime-tests.py`
- `ci/test-*.py`
- `ci/build-book-package.sh` if the toolchain is available; otherwise record it as not run.

## 12. New checker: `review/pedagogical-smoothing-2026-09-23/check-smoothing.py`

**Assertions**
1. The global total is between 107,338 and 115,000. Print the distance to 112,338.
2. Each chapter lies between its floor and cap, unless `floor-waivers.md` or `cap-waivers.md` records a complete waiver. A cap waiver may exceed the cap by at most 5%.
3. The manifest lists 32 numbered chapters and Appendix A, in order, with no orphan files.
4. Every chapter has 3 objectives, 1 recap and 5 tiered exercises with a public answer file. Part checkpoints sit at the end of each Part's last chapter. No `TODO(P3-apparatus)` remains.
5. At most 20 rule boxes.
6. The unambiguous deprecated terms appear zero times outside the allowlist: configured role, registered instance, configuration instance, runtime-visible role, endpoint role, configured endpoint, named endpoint, lower family, communication family, lower communication family, peer episode, connection episode, and *carrier* outside Ch21–22.
7. The provenance phrases — "recorded working-tree", "source identity", "must not be presented", "handshake claims", "Existing consumers", "source tree recorded for this edition", "For this edition" — occur only in Ch2. Matching is case-insensitive. The Preface keeps only its version statement (D3), which contains none of these phrases. In Conventions, remove the verification-coverage note (old conventions.md:13) and reword the source-package pointer (old conventions.md:11) so that it points to the Ch2 sidebar without edition-provenance wording.
8. Ch17, 18, 19, 21 and 22 each contain a Build note box. No fenced block follows it before "What to remember", and at least one prose paragraph comes between the Build note and "What to remember".
9. Ch18 contains the `dispatch.cpp` marked listing before its first table.
10. Ch21's first section contains CONNECT, CONNACK, SUBSCRIBE, SUBACK and PUBLISH before the first class table.
11. Ch27's first section contains `find_package` and `target_link_libraries`.
12. Ch29's first section contains no `sh` fence.
13. Ch31 has no fenced block over 60 lines. In Ch30, prose separates every pair of listings.
14. Ch32 has at least 3 worked-decision sections.
15. The event-loop thought experiment comes before Ch6's first source excerpt. The descriptor-population section is in Appendix A and absent from Ch6.
16. The Conventions glossary contains every canonical term in §7.

**Reported per chapter, before and after (not asserted)**
- New-identifier density.
- Prose words before the first non-prose block.
- Abstract-noun clusters.
- The context-dependent terms: communication role, server instance, client instance, role.
- The change in fenced tokens.
- The last three blocks before "What to remember".

## 13. Report: `review/pedagogical-smoothing-2026-09-23/REPORT.md`

1. **Outcome.** Tokens before and after, against the must, the wish and the ceiling.
2. **Decisions.** D1–D6 as applied, with any deviation and its reason. Include the P−1 change and its evidence.
3. **Gates.** For each phase: commit SHA, log paths and the framework freeze records.
4. **Chapter table.** New and old number; tokens before, after, floor and cap; any waiver; rows addressed; what changed (1–2 lines); dimension evidence as `file:line`; any remaining concern.
5. **Terminology.** Counts before and after, and the allowlist.
6. **Apparatus.** For Ch4, 5, 25 and 26: objectives, exercises and labs, each with its objective and its CTest name.
7. **Preservation deltas**, and every structure-sensitive registry changed in P2.
8. **Dimension matrix after the pass.** Scores 1–5 for 8 dimensions × 33 units, with the variance per dimension. Label it a self-assessment.
9. **Open, qualified and blocked items.**

**Rules for the report**
- Every claimed fix cites the changed `file:line`.
- Distinguish inspected, compiled and run.
- Historical evidence stays historical.
- Do not declare completion while any gate, check or unwaived floor is unmet.

## 14. Stop conditions

- **The author's working tree is unavailable, or the freeze record changes.** Stop and report. Do not substitute another source.
- **An entry check or lab fails for a reason other than the P−1 defect.** Stop at P0 and report. Do not repair unrelated defects in this pass.
- **An API named in this prompt is absent from the frozen tree.** Do not print it; report it.
- **The projected total exceeds 113,500 before P5.** Skip the optional rows 30 and 31, keep the floors (or waive them), and report.
- **A chapter's work is complete below its floor.** File a waiver (§4) and recover the tokens elsewhere in rank order. The global must of 107,338 cannot be waived; if it cannot be met without padding, stop at P7 and report the shortfall instead of padding.
