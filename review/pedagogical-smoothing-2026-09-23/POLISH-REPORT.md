# Follow-up 12 — final polish report

**Run ended for the author’s reading, with one explicit qualification.** P1–P9 have individual commits; the evidence commit closes two in-scope omissions found during checking. Eight of nine new polish assertion groups pass. Group 2 remains failed for two pre-existing tables outside the authorized Ch8 edit. Consequently **row 16 / C remains ◐**; this is not an all-green completion claim.

## Scope and history

The previous entry stop at the framework’s untracked `porting/` directory is preserved byte-for-byte as [POLISH-REPORT-entry-stop.md](POLISH-REPORT-entry-stop.md). This resumption starts at `9172e99`, whose manuscript matches `9b82ea4`. FOLLOWUP-12 was already installed and was not stored again. PROMPT, FOLLOWUP-01, FOLLOWUP-11, FOLLOWUP-12, R2 freeze, manifest and approved chapter structure are unchanged. All prior commits are retained.

The latest author instruction excludes `porting/` from source authority. No file in that directory was read, moved or changed, and no author-tree exclude file or Git configuration was edited. Only the author-approved filtered freeze comparison and the fresh public clone were used. No companion file, existing assertion, timeout or framework source changed. The separate publisher review remains historical; its additional recommendations were not implemented.

## Item commits

| Item | Commit | Result |
|---|---|---|
| P1 | `f8df09d` | Canonical vocabulary reviewed; 335 retained whole-word role uses and 29 carrier uses individually inventoried. |
| P2 | `40aed6c` | Ch8 reduced to three operational concerns with a Ch4 pointer; broader taxonomy condition qualified. |
| P3 | `be2179d` | Seven numbered command steps matching the later instructions. |
| P4 | `5cefd5c` | echoserver’s default/file/CLI port returns before generalization in all nine later sections. |
| P5 | `505d6d6` | MQTT 3.1.1 fundamentals and a built, inspected TikZ sequence before class vocabulary. |
| P6 | `7368aa0` | Type, lifecycle and method inventories collected; only the HTTP/Express comparison table remains outside the box. |
| P7 | `82a908d` | Broker-placement case with requirement/options/decision/consequence/test; concrete-actor rewrites in Ch23/26. |
| P8 | `ff995b8` | Exact verification regex returns to 46; fourteen later-added passages replaced in P8. |
| P9 | `f5ba856` | Completed revision described for publishers; all manuscript quantities and PDF extent refreshed. |

The final evidence commit additionally changes Ch24’s last “protocol roles” phrase to “application services”, turns Ch18’s two-row observation table into equivalent bullets, and removes editorial “frozen” wording from the MQTT version sentence. These are closure of P1/P6/P5, not additional review items. It registers the P2 Chapter 4 pointer against the existing topic identity and refreshes the terminology line addresses. No history is rewritten.

## Register status matrix

Rows are **issue-register rows**, not chapters. E = entry, D = depth, G = gradient, X = explicitness, T = theory–example, L = language, S = structure, C = continuity. ● = met for the row’s scoped requirement; ◐ = partly met; ○ = open. These are issue-closure judgments, not independent publisher ratings or replacements for the historical 1–5 chapter scores.

No earlier 32×8 symbol matrix was stored. The carry-forward basis is the completed chapter ledger, core-mechanism sweep, seam log, unchanged accepted passages, and fresh structural checks. A ● in an unaffected dimension means no remaining condition of **that register row** in that dimension, supported by the row evidence below; it does not certify every aspect of every chapter. Newly closed cells are listed separately with current file:line evidence. The prior report’s blanket taxonomy-completion implication is corrected by the explicit ◐.

| Row | Issue | E | D | G | X | T | L | S | C |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Canonical terminology | ● | ● | ● | ● | ● | ● | ● | ● |
| 2 | Opening gradient | ● | ● | ● | ● | ● | ● | ● | ● |
| 3 | Runtime/layer split | ● | ● | ● | ● | ● | ● | ● | ● |
| 4 | Event-loop model before internals | ● | ● | ● | ● | ● | ● | ● | ● |
| 5 | Shortest route to the first program | ● | ● | ● | ● | ● | ● | ● | ● |
| 6 | Application/system split | ● | ● | ● | ● | ● | ● | ● | ● |
| 7 | Express example before inventory | ● | ● | ● | ● | ● | ● | ● | ● |
| 8 | MQTT conversation and fundamentals | ● | ● | ● | ● | ● | ● | ● | ● |
| 9 | CMake starts with a consumer | ● | ● | ● | ● | ● | ● | ● | ● |
| 10 | Configuration follows one port | ● | ● | ● | ● | ● | ● | ● | ● |
| 11 | Interpretation after capstone listings | ● | ● | ● | ● | ● | ● | ● | ● |
| 12 | Three explained extension excerpts | ● | ● | ● | ● | ● | ● | ● | ● |
| 13 | Expanded architectural synthesis | ● | ● | ● | ● | ● | ● | ● | ● |
| 14 | Application-facing recovery settings | ● | ● | ● | ● | ● | ● | ● | ● |
| 15 | Chapter and Part seams | ● | ● | ● | ● | ● | ● | ● | ● |
| 16 | Taxonomy has one teaching home | ● | ● | ● | ● | ● | ● | ● | ◐ |
| 17 | Protocol chapters end with a transition | ● | ● | ● | ● | ● | ● | ● | ● |
| 18 | Edition/verification voice contained | ● | ● | ● | ● | ● | ● | ● | ● |
| 19 | Concrete actors replace abstraction stacks | ● | ● | ● | ● | ● | ● | ● | ● |
| 20 | Logging explanation and current wording | ● | ● | ● | ● | ● | ● | ● | ● |
| 21 | Testing starts from a problem | ● | ● | ● | ● | ● | ● | ● | ● |
| 22 | Performance stance and limits | ● | ● | ● | ● | ● | ● | ● | ● |
| 23 | Appendix entry supports different readers | ● | ● | ● | ● | ● | ● | ● | ● |
| 24 | TLS configuration is on the page | ● | ● | ● | ● | ● | ● | ● | ● |
| 25 | Experience precedes formal vocabulary | ● | ● | ● | ● | ● | ● | ● | ● |
| 26 | Address-comparison seam | ● | ● | ● | ● | ● | ● | ● | ● |
| 27 | Core mechanism readable without the lab | ● | ● | ● | ● | ● | ● | ● | ● |
| 28 | Part II checkpoint interface printed | ● | ● | ● | ● | ● | ● | ● | ● |
| 29 | A distinct IoT worked decision | ● | ● | ● | ● | ● | ● | ● | ● |
| 30 | Native/composed MQTT trace | ● | ● | ● | ● | ● | ● | ● | ● |
| 31 | One-peer timeline before distinctions | ● | ● | ● | ● | ● | ● | ● | ● |
| 32 | Verification phrasing restored to baseline | ● | ● | ● | ● | ● | ● | ● | ● |

| Dimension | ● | ◐ | ○ |
|---|---:|---:|---:|
| E | 32 | 0 | 0 |
| D | 32 | 0 | 0 |
| G | 32 | 0 | 0 |
| X | 32 | 0 | 0 |
| T | 32 | 0 | 0 |
| L | 32 | 0 | 0 |
| S | 32 | 0 | 0 |
| C | 31 | 1 | 0 |

Total: **255 ●, 1 ◐, 0 ○**. These totals cover issue closure only.

### Evidence for moved cells

| Register row / dimensions newly closed | Current evidence |
|---|---|
| 1 / L, C; 16 / L | `manuscript/chapters/05-layers-in-practice.md:35`, `manuscript/chapters/05-layers-in-practice.md:62`, `manuscript/chapters/08-servers-clients-and-connections.md:339`, `manuscript/chapters/24-database-support-and-application-state.md:133`; every kept use at `terminology-allowlist.md:1`; polish group 1 passes. |
| 5 / G, S | `manuscript/chapters/02-preparing-your-environment.md:18`: seven actual command steps and the stop-on-failure sentence, followed by the full explanation. |
| 7 / T | `manuscript/chapters/18-the-express-like-framework.md:201`: one reference box; `manuscript/chapters/18-the-express-like-framework.md:249`: observation bullets; the sole external table is the HTTP/Express comparison at line 72. |
| 8 / D | `manuscript/chapters/21-mqtt-support-in-snodec.md:21`: packet sequence; `manuscript/chapters/21-mqtt-support-in-snodec.md:39`–45: version, filters, wildcards, QoS, retained state, keep-alive and sessions; source verification in `POLISH-CLAIMS.md`. |
| 10 / G, T | `manuscript/chapters/13-configuring-applications-and-named-instances.md:30`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:113`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:207`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:278`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:375`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:470`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:509`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:542`, `manuscript/chapters/13-configuring-applications-and-named-instances.md:600`: each later section starts from the same port. |
| 19 / X, T, L | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:30`, `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:206`, `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:210`, `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:246`, `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:45`, `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:74`, `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:361`: named operators/processes replace abstract stacks; polish group 7 passes without a noun-stack exception. |
| 29 / X, T, L | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:74`–86: a distinct multi-protocol decision about local/remote broker placement, outages, QoS and acknowledgement limits. |
| 32 / X, L | `polish-verification-rewrites.json:1` gives all fourteen before/after replacements and their baseline provenance; `polish-checks.json:1` records 46 matches. |

### Remaining qualified cell

**16 / C: ◐.** The requested Ch8 table is corrected. The stronger global check also counts the canonical glossary at `manuscript/frontmatter/conventions.md:23` and the activation-reading table at `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:83`. Each names all six runtime terms. P2 specifies a Ch8 edit, and Follow-up 12 forbids other manuscript changes. The glossary is also required by the governing terminology specification. Broadening the edit or inventing a checker exemption would conceal this scope conflict. Both tables remain, the checker exits 1, and this cell is not marked met.

### Carry-forward evidence by register row

| Row | Evidence reviewed or retained |
|---:|---|
| 1 | `manuscript/chapters/05-layers-in-practice.md:35`; `terminology-allowlist.md:1` |
| 2 | `manuscript/chapters/01-why-snodec-exists.md:19`; `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:21` |
| 3 | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:13`; `manuscript/chapters/05-layers-in-practice.md:9` |
| 4 | `manuscript/chapters/06-core-runtime-and-event-processing.md:18` |
| 5 | `manuscript/chapters/02-preparing-your-environment.md:18` |
| 6 | `manuscript/chapters/25-reading-complete-snodec-applications.md:13`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:14` |
| 7 | `manuscript/chapters/18-the-express-like-framework.md:23`; `manuscript/chapters/18-the-express-like-framework.md:201` |
| 8 | `manuscript/chapters/21-mqtt-support-in-snodec.md:21`; `manuscript/chapters/21-mqtt-support-in-snodec.md:39` |
| 9 | `manuscript/chapters/27-cmake-components-and-linking-strategy.md:14`; `manuscript/chapters/27-cmake-components-and-linking-strategy.md:90` |
| 10 | `manuscript/chapters/13-configuring-applications-and-named-instances.md:22`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:276`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:507`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:598` |
| 11 | `manuscript/chapters/30-building-minigateway.md:473`; `check-smoothing.py` group 13 |
| 12 | `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:357`; `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:393`; `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:437` |
| 13 | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:72`; `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:86`; `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:100` |
| 14 | `manuscript/chapters/16-timeouts-retries-and-failure-modes.md:108` |
| 15 | `seam-log.md:1`; `polish-chapter-references.log:1`; `smoothing-reference-register.json` |
| 16 | `manuscript/chapters/08-servers-clients-and-connections.md:333`; `manuscript/frontmatter/conventions.md:23`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:83` |
| 17 | `manuscript/chapters/17-the-http-layer.md:307`; `manuscript/chapters/18-the-express-like-framework.md:285`; `check-smoothing.py` group 8 |
| 18 | `manuscript/chapters/02-preparing-your-environment.md:132`; `polish-smoothing.log:1`; `polish-verification-rewrites.json:1` |
| 19 | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:210`; `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:246`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:45`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:74` |
| 20 | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:59`; `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:182` |
| 21 | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:16` |
| 22 | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:20`; `chapter-ledger.md:35` |
| 23 | `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:24` |
| 24 | `manuscript/chapters/15-tls-across-the-framework.md:50` |
| 25 | `manuscript/chapters/01-why-snodec-exists.md:19`; `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:21` |
| 26 | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:254` |
| 27 | `P5-core-mechanism-review.md:1`; `chapter-ledger.md:1`; `manuscript/chapters/18-the-express-like-framework.md:23`; `manuscript/chapters/21-mqtt-support-in-snodec.md:39` |
| 28 | `manuscript/chapters/06-core-runtime-and-event-processing.md:253` |
| 29 | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:74` |
| 30 | `manuscript/chapters/22-mqtt-over-websocket.md:20` |
| 31 | `manuscript/chapters/08-servers-clients-and-connections.md:23` |
| 32 | `polish-verification-rewrites.json:1`; `polish-polish.log:3` |

The historical ledgers’ token counts and old line offsets are not reused as current metrics. The direct references above and the fresh metrics are authoritative for this polish. Historical runtime results retain their original scope; no new lab, hardware, deployment or full MQTTSuite execution is claimed.

## Extent and budgets

Counts are `ci/manuscript-metrics.py` raw UTF-8 whitespace tokens, including Markdown and code. They are not a publisher’s typeset-word estimate. “Before” is the fresh `9172e99` entry measurement; “now” is `metrics-after-polish.json`.

| Measure | Before | Now | Change |
|---|---:|---:|---:|
| Full book | 110,177 | 110,767 | +590 |
| Outside fences | 102,339 | 102,891 | +552 |
| In fences, including markers | 7,838 | 7,876 | +38 |
| Code content, without fence markers | 7,118 | 7,152 | +34 |

| Threshold | Absolute tokens | Current position |
|---|---:|---|
| Global must | 107,338 | 3,429 above |
| Requested comparison / wish | 112,338 | 1,571 below |
| Follow-up 12 aim | 112,500 | 1,733 below |
| Hard ceiling | 115,000 | 4,233 below |

Growth in this polish: **590 tokens (0.54%)**. All chapter floors and caps, and all front/Part/epilogue/backmatter group bounds, pass without a waiver.

### Chapter accounting

Every chapter is shown so that touched chapters can be compared with unchanged ones. “Edited” records manuscript changes since `9172e99`; a zero token delta does not mean unchanged prose.

| Chapter | Before | Now | Δ | Floor | Cap | Edited |
|---|---:|---:|---:|---:|---:|:---:|
| 1 — Why SNode.C Exists | 2,402 | 2,403 | +1 | 2,400 | 2,670 | yes |
| 2 — Preparing Your Environment | 3,194 | 3,248 | +54 | 3,006 | 3,250 | yes |
| 3 — Your First Working Program: The Echo Pair | 3,001 | 3,006 | +5 | 3,000 | 3,270 | yes |
| 4 — The SNode.C Runtime Mental Model | 2,908 | 2,908 | +0 | 2,700 | 3,050 | yes |
| 5 — Layers in Practice | 2,882 | 2,892 | +10 | 2,875 | 3,325 | yes |
| 6 — Core Runtime and Event Processing | 3,502 | 3,502 | +0 | 3,500 | 3,850 | no |
| 7 — Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 4,206 | 4,208 | +2 | 4,175 | 4,250 | yes |
| 8 — Servers, Clients, and Connections | 3,184 | 3,219 | +35 | 3,150 | 3,334 | yes |
| 9 — Bluetooth in SNode.C: RFCOMM and L2CAP | 2,173 | 2,173 | +0 | 2,120 | 2,220 | yes |
| 10 — Writing `SocketContext` Classes Well | 3,087 | 3,087 | +0 | 3,040 | 3,140 | yes |
| 11 — Writing `SocketContextFactory` Classes Well | 2,258 | 2,260 | +2 | 2,215 | 2,315 | yes |
| 12 — Building the Same Protocol over Different Lower Layers | 2,581 | 2,583 | +2 | 2,505 | 2,605 | yes |
| 13 — Configuring Applications and Named Instances | 4,475 | 4,535 | +60 | 4,300 | 4,673 | yes |
| 14 — Logging, Diagnostics, and Runtime Introspection | 2,793 | 2,794 | +1 | 2,650 | 2,800 | yes |
| 15 — TLS Across the Framework | 2,754 | 2,754 | +0 | 2,700 | 2,900 | no |
| 16 — Timeouts, Retries, and Failure Modes | 3,200 | 3,204 | +4 | 3,200 | 3,390 | yes |
| 17 — The HTTP Layer | 2,478 | 2,480 | +2 | 2,450 | 2,600 | yes |
| 18 — The Express-Like Framework | 2,218 | 2,225 | +7 | 2,050 | 2,315 | yes |
| 19 — Server-Sent Events and Real-Time HTTP | 3,305 | 3,305 | +0 | 3,220 | 3,370 | no |
| 20 — WebSocket and Protocol Upgrade | 3,001 | 3,008 | +7 | 2,950 | 3,100 | yes |
| 21 — MQTT Support in SNode.C | 3,015 | 3,313 | +298 | 3,000 | 3,405 | yes |
| 22 — MQTT over WebSocket | 2,119 | 2,125 | +6 | 2,100 | 2,282 | yes |
| 23 — Designing IoT Systems with Multiple Protocols | 3,141 | 3,181 | +40 | 3,100 | 3,222 | yes |
| 24 — Database Support and Application State | 3,857 | 3,857 | +0 | 3,826 | 3,926 | yes |
| 25 — Reading Complete SNode.C Applications | 2,560 | 2,562 | +2 | 2,450 | 2,600 | yes |
| 26 — From Applications to Systems: MQTTSuite | 3,843 | 3,889 | +46 | 3,750 | 3,941 | yes |
| 27 — CMake Components, Public Headers, and Linking Strategy | 3,748 | 3,750 | +2 | 3,700 | 4,000 | yes |
| 28 — Deployment on Linux and OpenWrt | 3,586 | 3,587 | +1 | 3,546 | 3,646 | yes |
| 29 — Testing, Debugging, and Benchmarking | 4,360 | 4,360 | +0 | 4,300 | 4,500 | no |
| 30 — Building MiniGateway | 4,587 | 4,588 | +1 | 4,400 | 4,618 | yes |
| 31 — Extending MiniGateway with a New Network Role | 2,834 | 2,835 | +1 | 2,650 | 2,841 | yes |
| 32 — Architectural Judgment: Choosing the Right Layer and Boundary | 3,108 | 3,108 | +0 | 3,100 | 3,350 | no |
| A — Reading and Extending the Framework | 3,968 | 3,970 | +2 | 3,900 | 3,994 | yes |

| Other material | Before | Now | Δ |
|---|---:|---:|---:|
| frontmatter | 2,291 | 2,290 | -1 |
| parts | 1,392 | 1,392 | +0 |
| backmatter | 783 | 783 | +0 |
| Epilogue | 1,383 | 1,383 | +0 |

## Checks and source freeze

| Check | Result and scope |
|---|---|
| New polish checker | **8/9 groups pass**; group 2 fails only for the two tables above. `polish-checks.json` and `polish-polish.log`. |
| New checker mutation tests | **16/16 pass**; malformed phrases, missing commands/port/diagram/fundamentals, extra tables, abstract captions, excess regex matches, stale metrics/pages and internal proposal terms are rejected. `polish-polish-tests.log`. |
| Existing smoothing checker | **16/16 assertion groups pass**, including all budgets; `polish-smoothing.log`. |
| Fresh metrics | **PASS**; `metrics-before-polish.json`, `metrics-after-polish.json`. |
| Chapter references | **PASS**: 32 chapters + Appendix A, 56 stable topics, 310 current references, 374 preserved migration dispositions. |
| Source alignment, explicit public clone | **PASS**: 1,448 manifest files, 33 evidence records, 37 exact complete listings; zero errors. |
| Source hygiene | **PASS**, including six reference-checker tests and the ordinary recorded-baseline alignment check. |
| Figure target | **PASS**; new TikZ sequence and contact sheet built through the existing pipeline. |
| Book package | **PASS**: twice-built book/proposal/sample PDFs, no unresolved final references, archive 454 unique paths. `polish-build.log`. |
| Companion/labs | No companion changes, so labs are not rerun, exactly as Follow-up 12 directs. The earlier 66 labs/185 framework tests remain historical evidence. |
| Preservation | **PASS**; `polish-preservation.json` records protected-file hashes, unchanged companion/source baseline/tests, retained history and the byte-identical historical stop report. |

Framework HEAD at entry and exit is `07ca9a2936ee72582df7d159cb06666fe23e30f8`. Filtered porcelain status is empty; the binary HEAD diff has SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; no untracked nonignored files exist outside `porting/`. Both resumption freeze JSONs equal `framework-freeze-R2.json`. The authority record itself is unchanged.

The fresh public clone is `build/polish-07ca9a29-public`, from `https://github.com/SNodeC/snode.c.git`, clean at the same detached HEAD. Explicit alignment against it verifies the content digest `2face99fc58fb1ec5374c35d88e6fcd9c7a7d56b52ea44cb00e49eb4825b9a2b`. The author’s tracked content matches this clone under the approved freeze comparison. No framework behavioral investigation or fix was performed. Changed technical explanations are supported by precise source/header anchors in [POLISH-CLAIMS.md](POLISH-CLAIMS.md), which is part of this report’s evidence.

## PDF and visual inspection

Book: **330 pages**, `/home/voc/projects/snodec/publications/book/dist/pdf/snodec-book.pdf`. Proposal: 9 pages. Combined proposal/samples: 60 pages. Artifact paths, page counts and SHA-256 hashes are in `polish-artifacts.json`. Page numbers here are physical PDF pages, not the printed frontmatter/body folios.

Raster review covered the new MQTT figure and book pages 23, 115, 120, 124, 163–166, 188–189 and 203; proposal pages 1, 5 and 8; sample pages 10–11. The command box is readable, the routing reference continues cleanly across pages, the sequence labels/arrows are distinct, the five-part worked case is legible, and the updated proposal numbers fit their tables. This is targeted visual review of the changed layouts, not a fresh page-by-page certification of all 330 pages.

## Accounting and handoff

Production/framework/companion code: **0 lines changed**. Existing tests/checkers: **0 lines changed**. New editorial assertion support: **245 lines**; its new mutation-test support: **133 lines**. Remaining changes are manuscript, figure source, proposal, reference metadata and review evidence. The 67-line extension CMake listing remains under the author’s existing approval.

The work branch is `book/pedagogical-smoothing-2026-09-23`. Push the nine item commits and the final evidence commit; do not merge. The run ends with the qualified cell recorded, for the author’s reading. No further editorial expansion is authorized or implied.
