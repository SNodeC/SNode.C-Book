# Final polish report — Follow-up 13

**Stopped; publisher freeze gate not passed.** The frozen framework fails the local Clang 21.1.8 workflow build in `src/tools/snodec-control/src/ConfigActions.cpp:296`: `-Werror,-Wnrvo` reports “not eliding copy on return”. The GCC build was stopped when that failure was identified. No framework fix, alternate compiler experiment, warning suppression or test adaptation followed. The author-tree freeze still matches R2.

Work began at `b98eb4a`. A–I now have individual commits; I has focused loader verification, but the required fresh GCC/Clang 66-lab runs remain incomplete. This is a local compiler/build compatibility failure; it does not establish the outcome on the hosted Ubuntu 24.04 toolchains. Historical results from 23 September remain historical.

## Author decision: retain the manuscript

The author first retained the chapter floors, then explicitly said: “Did i select cut down? I do not want to cut the manuscript down!” No compression had been applied. The shortening portions of D were withdrawn; no prose was removed under E/H. D retains every targeted listing and explanation, aligns the file value at 18091, connects the two preserved trees, and adds final architectural interpretation to the existing Ch32 labs. H joins short paragraphs, presents all 19 compile definitions in a table, and varies five transitions without removing their content.

Raw extent rises from **110,767 to 110,955 tokens (+188; +0.17%)**. The three-token combined reductions in Ch3/4 are grammatical and terminology corrections, not content cuts. All 33 chapter/appendix floors and caps pass without waivers. No broad refinement follows this report.

## Item commits

| Item | Commit | Result |
|---|---|---|
| A | `49c8ba7` | Three local errors corrected |
| B | `f390b8c` | Instances, variants and callback terminology; retained design roles inventoried |
| C | `7a92b21` | Explicit protocol/network-family claim |
| D | `e458f2d` | Teaching material retained; file values and synthesis aligned |
| E | `ab0a145` | Contrast, chapter destination and MQTT/introductory ordering repaired |
| F | `ae145cb` | Grammar, version spelling and illustrative label corrected |
| G | `443e24d` | Recaps, build note, answer pointers and descriptor placement aligned |
| H | `99ca720` | Cadence and table presentation; content retained |
| I | `f19a658` | Shared Linux inherited-RPATH policy; two focused tests pass; full verification stopped |

Application implementation: **0 lines changed**. Existing test assertions, timeouts and driver logic: **0 lines changed**. Shared companion build support: **+6 / −0 lines** (two comments, one platform condition, one linker option, its closing line and spacing). New editorial checker/test support is accounted separately in the evidence commit; it is not application code.

## Freeze gate

| Requirement | Result |
|---|---|
| Matrix all ● | **Qualified:** row 33 retains ◐ in all dimensions for the withdrawn compression criterion. This is not a request for further cuts. |
| Book package | **PASS:** twice-built final package; book **328 pages**, proposal 9, sample 60; 454 unique archive entries; no unresolved final references. |
| Local GCC labs 66/66 | **Not established:** fresh GCC 16.2.0 build stopped after the Clang failure; no fresh full lab/smoke/lifetime result. |
| Local Clang labs 66/66 | **Blocked:** Clang 21.1.8 failed while building the frozen framework, before companion tests. |
| Hosted CI | **Hosted CI pending:** run [36002150169](https://github.com/SNodeC/SNode.C-Book/actions/runs/36002150169), pushed code commit `f19a658`, observed in progress. The final evidence-only push starts another run. |
| Frozen-source alignment | **PASS:** fresh public clone at 07ca9a29; 1,448 files, 33 evidence records, 37 exact complete listings, zero errors. |
| Author freeze | **PASS:** start and end equal `framework-freeze-R2.json` in all four required fields. |

## Status matrix

Rows are issue-register rows, not chapter grades. E = entry, D = depth, G = gradient, X = explicitness, T = theory–example, L = language, S = structure, C = continuity. ● means met for the scoped row; ◐ means qualified/partly met; ○ means open. Rows 1–32 carry forward the prior scoped evidence, with row 16/C now closed by the precisely limited table exemptions. New rows 34–37 assess the specified local corrections. Row 33 is not marked complete by relabelling unperformed compression as a verified elimination of redundancy. Its qualifications record the author’s withdrawal; no shortening remains authorized.

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
| 16 | Taxonomy has one teaching home | ● | ● | ● | ● | ● | ● | ● | ● |
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
| 33 | Repetition retained by author | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ |
| 34 | References and narrative order | ● | ● | ● | ● | ● | ● | ● | ● |
| 35 | Slips and register | ● | ● | ● | ● | ● | ● | ● | ● |
| 36 | Apparatus and placement | ● | ● | ● | ● | ● | ● | ● | ● |
| 37 | Cadence and style without shortening | ● | ● | ● | ● | ● | ● | ● | ● |

| Dimension | ● | ◐ | ○ |
|---|---:|---:|---:|
| E | 36 | 1 | 0 |
| D | 36 | 1 | 0 |
| G | 36 | 1 | 0 |
| X | 36 | 1 | 0 |
| T | 36 | 1 | 0 |
| L | 36 | 1 | 0 |
| S | 36 | 1 | 0 |
| C | 36 | 1 | 0 |

Total: **288 ●, 8 ◐, 0 ○**. The matrix is an issue-closure record; the separate executable freeze gate remains blocked.

## Evidence for changed or newly assessed cells

| Cells | Current file:line evidence |
|---|---|
| 16 / C: ◐ → ● | `check-polish.py:74`; `manuscript/frontmatter/conventions.md:23`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:83`; `test-polish.py:45` rejects extra taxonomy tables even in the two exempted files. |
| 33 / E, D, G, X, T, L, S, C | `review/EDITORIAL-WORK-PLAN.md:2412`; `manuscript/chapters/01-why-snodec-exists.md:44`; `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:250` |
| 34 / E, D, G, X, T, L, S, C | `manuscript/chapters/01-why-snodec-exists.md:39`; `manuscript/chapters/02-preparing-your-environment.md:449`; `manuscript/chapters/21-mqtt-support-in-snodec.md:27`; `manuscript/chapters/29-testing-debugging-and-benchmarking.md:16` |
| 35 / E, D, G, X, T, L, S, C | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:232`; `manuscript/chapters/16-timeouts-retries-and-failure-modes.md:194`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:110` |
| 36 / E, D, G, X, T, L, S, C | `manuscript/chapters/05-layers-in-practice.md:241`; `manuscript/chapters/25-reading-complete-snodec-applications.md:289`; `manuscript/chapters/20-websocket-and-protocol-upgrade.md:391`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:626`; `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:343`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:96` |
| 37 / E, D, G, X, T, L, S, C | `manuscript/chapters/08-servers-clients-and-connections.md:157`; `manuscript/chapters/10-writing-socketcontext-classes-well.md:257`; `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:353`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:222`; `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:54`; `manuscript/chapters/27-cmake-components-and-linking-strategy.md:276`; `manuscript/chapters/30-building-minigateway.md:283` |

Additional corrections keep previously met cells current: row 1 uses the full `terminology-allowlist.md` (328 role occurrences, 29 carrier occurrences); row 26 names its claim at `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:248`. Source verification for A–I is in `FINAL-CLAIMS.md`. `check-final.py` protects the listed factual and apparatus corrections, including soft-wrapped answer pointers, without treating Markdown line wrapping as a prose defect.

## Extent

Counts are raw whitespace tokens from `ci/manuscript-metrics.py`, including Markdown and fenced content. Every chapter is shown, including unchanged chapters; this prevents a touched-only table from hiding overall changes.

| Chapter | Before | After | Δ | Floor | Cap |
|---|---:|---:|---:|---:|---:|
| 1 — Why SNode.C Exists | 2,403 | 2,411 | +8 | 2,400 | 2,670 |
| 2 — Preparing Your Environment | 3,248 | 3,250 | +2 | 3,006 | 3,250 |
| 3 — Your First Working Program: The Echo Pair | 3,006 | 3,004 | -2 | 3,000 | 3,270 |
| 4 — The SNode.C Runtime Mental Model | 2,908 | 2,907 | -1 | 2,700 | 3,050 |
| 5 — Layers in Practice | 2,892 | 2,903 | +11 | 2,875 | 3,325 |
| 6 — Core Runtime and Event Processing | 3,502 | 3,502 | +0 | 3,500 | 3,850 |
| 7 — Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 4,208 | 4,218 | +10 | 4,175 | 4,250 |
| 8 — Servers, Clients, and Connections | 3,219 | 3,224 | +5 | 3,150 | 3,334 |
| 9 — Bluetooth in SNode.C: RFCOMM and L2CAP | 2,173 | 2,173 | +0 | 2,120 | 2,220 |
| 10 — Writing `SocketContext` Classes Well | 3,087 | 3,087 | +0 | 3,040 | 3,140 |
| 11 — Writing `SocketContextFactory` Classes Well | 2,260 | 2,260 | +0 | 2,215 | 2,315 |
| 12 — Building the Same Protocol over Different Lower Layers | 2,583 | 2,583 | +0 | 2,505 | 2,605 |
| 13 — Configuring Applications and Named Instances | 4,535 | 4,535 | +0 | 4,300 | 4,673 |
| 14 — Logging, Diagnostics, and Runtime Introspection | 2,794 | 2,794 | +0 | 2,650 | 2,800 |
| 15 — TLS Across the Framework | 2,754 | 2,754 | +0 | 2,700 | 2,900 |
| 16 — Timeouts, Retries, and Failure Modes | 3,204 | 3,209 | +5 | 3,200 | 3,390 |
| 17 — The HTTP Layer | 2,480 | 2,480 | +0 | 2,450 | 2,600 |
| 18 — The Express-Like Framework | 2,225 | 2,225 | +0 | 2,050 | 2,315 |
| 19 — Server-Sent Events and Real-Time HTTP | 3,305 | 3,305 | +0 | 3,220 | 3,370 |
| 20 — WebSocket and Protocol Upgrade | 3,008 | 3,013 | +5 | 2,950 | 3,100 |
| 21 — MQTT Support in SNode.C | 3,313 | 3,313 | +0 | 3,000 | 3,405 |
| 22 — MQTT over WebSocket | 2,125 | 2,125 | +0 | 2,100 | 2,282 |
| 23 — Designing IoT Systems with Multiple Protocols | 3,181 | 3,181 | +0 | 3,100 | 3,222 |
| 24 — Database Support and Application State | 3,857 | 3,857 | +0 | 3,826 | 3,926 |
| 25 — Reading Complete SNode.C Applications | 2,562 | 2,587 | +25 | 2,450 | 2,600 |
| 26 — From Applications to Systems: MQTTSuite | 3,889 | 3,897 | +8 | 3,750 | 3,941 |
| 27 — CMake Components, Public Headers, and Linking Strategy | 3,750 | 3,784 | +34 | 3,700 | 4,000 |
| 28 — Deployment on Linux and OpenWrt | 3,587 | 3,602 | +15 | 3,546 | 3,646 |
| 29 — Testing, Debugging, and Benchmarking | 4,360 | 4,361 | +1 | 4,300 | 4,500 |
| 30 — Building MiniGateway | 4,588 | 4,591 | +3 | 4,400 | 4,618 |
| 31 — Extending MiniGateway with a New Network Role | 2,835 | 2,835 | +0 | 2,650 | 2,841 |
| 32 — Architectural Judgment: Choosing the Right Layer and Boundary | 3,108 | 3,165 | +57 | 3,100 | 3,350 |
| A — Reading and Extending the Framework | 3,970 | 3,970 | +0 | 3,900 | 3,994 |
| **Full book** | **110,767** | **110,955** | **+188** | — | **115,000** |

Current prose: **103,079**; fenced tokens: **7,876**. Against the historical absolute targets: 3,617 above 107,338; 1,383 below 112,338; 4,045 below 115,000. Front/back matter and Part openers are included in the full-book total. The reading PDF moves from 330 to 328 pages because paragraph and list layout changes; the manuscript has more tokens, not less content. Publisher pagination remains separate.

## Checks and limits

| Check | Outcome |
|---|---|
| check-smoothing.py | PASS, 16 assertion groups; all floors/caps and total budget. |
| check-polish.py | PASS, 9/9 groups; exactly 46 verification constructions; proposal figures match current metrics and PDF. |
| check-final.py | PASS; all specified regression guards. |
| Editorial checker tests | PASS: 17 polish tests and 13 final tests. |
| Chapter references / hygiene | PASS: 312 current references; 374 preserved migration dispositions; 6 reference-checker tests; hygiene clean. |
| Source alignment | PASS against the fresh public clone; complete listings unchanged. |
| PDF package | PASS; final book, proposal and sample rebuilt; artifact structure checked. |
| Targeted PDF visual review | Book physical pages 55, 184, 224, 227, 242 and 311: recaps, build note, illustrative label, compact definitions and descriptor placement legible without clipping/overlap. This is targeted review, not a new page-by-page production audit. |
| Focused loader tests | PASS 2/2 under existing verified installation, with /usr/local/lib hidden and LD_LIBRARY_PATH unset; readelf confirms inherited DT_RPATH. |
| Fresh framework / companion / smoke / lifetime runs | Incomplete: local Clang framework build failure; GCC stopped under the author’s stop rule. No 66/66 claim for either current workflow run. |

The bare-loader diagnostic used a historical 62-test build. It exposed the two specified missing indirect libraries after the unrelated host installation was hidden. Other failures in that mixed historical-build/current-driver run are not adjudicated and are not presented as a current verification result. The focused fix verification uses freshly built current companion targets. Full clean workflow verification was attempted from the fresh clone with both compiler selections, with the same script flags and default parallelism as the workflow; local Debian compiler versions differ from the hosted Ubuntu toolchains.

The runtime invariant is one coherent lookup policy for each private-prefix dependency closure. Applying the existing lifecycle-lab linker policy before both companion subdirectories solves the direct-test boundary without changing Python drivers or adding separate per-test environment policies. The framework’s compiler diagnostic is a separate blocker. No framework investigation was pursued after it appeared.

## Freeze and evidence

Fresh public clone: `build/final-polish-public-07ca9a29`, checked out at `07ca9a2936ee72582df7d159cb06666fe23e30f8`. Author tree: `/home/voc/projects/snodec/snode.c`. Its filtered porcelain is empty; HEAD matches; binary diff digest is SHA-256 of empty bytes; there are no untracked nonignored files outside the excluded `porting/` entry. The author tree and its configuration were never modified; porting contents were not read. Start/end records are `framework-freeze-final-start.json` and `framework-freeze-final-end.json`.

Source content digest: `2face99fc58fb1ec5374c35d88e6fcd9c7a7d56b52ea44cb00e49eb4825b9a2b`. The R2 record is unchanged. Permanent compact logs are under `final-evidence/`; full local logs are under `build/final-polish/`.

| Full local log | SHA-256 |
|---|---|
| `book-build-final.log` | `32a5eaba21587f646ea4a5c8753a1029e50473d6edc90d00c4f68eabe53adef2` |
| `gcc-build.log` | `5b761cdd443b6d55f4046d8abd284ed8d8b542180d0565f5b64b213812468032` |
| `clang-build.log` | `ba3e2cea1358fe8883472854ccacb3e5b7e2d6b158c84d85b0dde75ff401bf55` |
| `bare-ctest-before.log` | `1cecfbccf372de83442e9c299e02cdbe475ed6721156f455e5aa853379843033` |

A–I were pushed at `f19a658`; this report and its evidence are committed and pushed afterward without merging. Hosted status is pending, not inferred from the old failed run. The initial log download requests returned HTTP 403. The run ends here: the manuscript receives no further broad refinement, and publisher submission is not certified while the executable freeze gate is incomplete.
