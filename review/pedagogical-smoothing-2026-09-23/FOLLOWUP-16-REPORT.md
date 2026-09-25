# Follow-up 16 — author style, wording and CI evidence

**All book gates passed. The manuscript is frozen again.** Work started on main at `06677fb`; A is `c39e6b0`, B is `446d3e3`. Both were pushed together. The final evidence commit retains these commits. No merge or pin change was made.

## Authority and identity

The four supplied paths are the author’s framework files named in the request. Both root styles and both supplied CMake modules were byte-identical to a fresh public `Book-1.0` clone before use. `cmake/format.cmake` was present. The installed root `.clang-format` and `.cmake-format.py` remain byte-identical, including their original trailing blank lines. The companion file contains only the FU16 comment, `BasedOnStyle: InheritParentConfig`, and `ColumnLimit: 90`; cmake-format retains its 80-column style. Evidence: `followup-16-evidence/style-identity.json`.

Observed commits below are evidence only; every dependency checkout target remains `Book-1.0`.

| Repository | Tag | Observed commit |
|---|---|---|
| SNodeC/snode.c | Book-1.0 | `07ca9a2936ee72582df7d159cb06666fe23e30f8` |
| SNodeC/mqttsuite | Book-1.0 | `5fef5c3036928dfa40ad4f124bb237cc9c3202bb` |
| SNodeC/OpenWRT | Book-1.0 | `5bef8cca5982838a7191a148633c1058f154e5eb` |

The author tree’s recorded HEAD is `07ca9a2936ee72582df7d159cb06666fe23e30f8`. Porcelain status ignores only the authorized `?? porting/` entry. Nothing in the author tree was modified or inspected under porting/. The final comparison is recorded in `followup-16-evidence/author-tree-end.json`, which equals the entry record exactly. Pin declarations, the framework manifest, and its patch are unchanged from entry.

## Formatter calibration

| Tool | Version | Tagged-framework check |
|---|---|---|
| clang-format | 21.1.8 | Style parsed; dry-run exit 1 on a set of 733 C++ files under core/net/express/web/iot; 37 files with formatting diagnostics. |
| clang-format | 18.1.3 | Style parsed; dry-run exit 1 on a set of 733 C++ files under core/net/express/web/iot; 44 files with formatting diagnostics. |
| cmakelang | 0.6.13 | Latest published version checked against PyPI; 8 root/module CMake files checked; only cmake/Packing.cmake differs. |

Neither available clang-format version is clean on the representative framework set. The author’s explicit fallback therefore selects the hosted Ubuntu 24.04 tool, **clang-format 18.1.3**, with **cmakelang 0.6.13**. Framework formatting differences were recorded without changing the clone or author tree. The archived dry-run diagnostics and `tool-calibration.json` are the calibration evidence. The shared checked sets contain 84 C++ files and 67 CMake files (`format-file-sets.json`). This is a formatting delta, not a claimed framework behavior defect.

## Item findings and changes

| Item | Verified finding and result | Current evidence | Commit |
|---|---|---|
| A1 | Style identity verified; unchanged root styles plus the sole 90-column companion override. | `companion/.clang-format:2` | c39e6b0 |
| A2 | Root lacked author format targets. Retained format-cmds, find_program detection and warning text; shared file sets feed format and format-check. Filters exclude builds, detected CMake output trees, installed/dependency/external source trees. Missing formatters fail format-check. Package includes styles/modules so an extracted source package configures. | `cmake/format.cmake:77`; `packaging/cmake/MakeProposalPackage.cmake:36` | c39e6b0 |
| A3 | Ran format, rebuilt every companion target and synchronized 37 marked listings. Includes, comments and C++ tokens audited; two long diagnostic messages are equivalent adjacent string literals. The last-line startup cue still describes the final executable statement; no layout-dependent prose correction was needed. | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:180`; `manuscript/chapters/30-building-minigateway.md:586` | c39e6b0 |
| A4 | Reviewed all unmarked snippets. Companion excerpts were synchronized; framework-derived excerpts preserved. Other complete units were formatted; partial fragments received only visible alignment/indentation corrections. Ch1 already explicitly labels its paired excerpts reflowed; their token sequence and existing paired presentation are retained. All 204 C++ blocks preserve code tokens and comment words. Ch25’s simplified pipe illustration restores the same left-aligned references visible at Book-1.0 in src/apps/testpipe.cpp:64. | `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:144`; `manuscript/chapters/06-core-runtime-and-event-processing.md:50`; `manuscript/chapters/01-why-snodec-exists.md:85` | c39e6b0 |
| A5 | CI installs clang-format-18 and cmakelang 0.6.13; the companion build script runs the shared format-check, which logs both versions. Declaration guard rejects right-aligned pointers/references and excludes rvalue references, unary operations, multiplication, comments and strings. Final verification extends fence recognition to attributed C++ blocks as well. | `.github/workflows/companion-examples.yml:61`; `ci/build-companion-examples.sh:52`; `review/pedagogical-smoothing-2026-09-23/check-final.py:40` | c39e6b0; evidence guard completion |
| A — approved Ch12 exception | Formatting moved the port token; a whitespace-dependent CMake substitution missed it. The author explicitly approved removing leading whitespace from the match and replacement strings. Baseline-generated and corrected-generated C++ are identical after formatting; no assertions, timeouts or runtime logic changed. | `companion/exercises/ch12/CMakeLists.txt:19` | c39e6b0 |
| B — configuration | 18092 is described as the effective value, not file syntax; network-family wording is canonical. | `manuscript/chapters/13-configuring-applications-and-named-instances.md:207`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:595` | 446d3e3 |
| B — edition and compiler | Edition-tag wording corrected; bypass prohibition retained without asking readers to move a tag. Baseline paragraph split into the three requested topics. Clang 21 failure retained; source location moved to this report. | `manuscript/chapters/02-preparing-your-environment.md:167`; `manuscript/chapters/02-preparing-your-environment.md:71` | 446d3e3 |
| B — prefixes and links | One prefix explanation remains beside the log excerpt with the interpretation sentence. Unix endpoint links retain the earlier address-field distinction and the Chapter 8 lifetime purpose. | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:219`; `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:524` | 446d3e3 |
| B — cadence | The specified Ch8 paragraphs are joined while retaining every sentence. Proposal quantities are refreshed from the current metrics and rebuilt PDF. | `manuscript/chapters/08-servers-clients-and-connections.md:95`; `manuscript/chapters/08-servers-clients-and-connections.md:258` | 446d3e3 |
| C | Local GCC and Clang builds and all 66 labs pass; final A+B hosted workflows and their tool versions are recorded below. | `followup-16-evidence/local-gcc.log`; `local-clang.log`; hosted evidence below | evidence |

Pre-edit file:line findings are in `verified-passages-before.json`, `snippets-before.json`, `layout-cues-before.json` and `wording-changes.json`. No requested wording finding was skipped as unreproduced. Framework-derived snippets and already-consistent partial fragments were deliberately left unchanged, with per-snippet decisions in `snippet-decisions.json`. No teaching passage, example or distinction was removed.

## Formatting and production evidence

`A-files.txt` and `A-commit-numstat.txt` enumerate the changed files. `format-token-audit.json` has no companion C++ token/comment mismatches after normalizing include order and adjacent string literal concatenation. `listing-token-audit.json` has zero mismatches across 204 C++ blocks, including the two attributed Ch1 fences. `ch12-generator-verification.json` confirms generated C++ equivalence. The 37 full listings are checked separately byte-for-byte. The 57 existing CMake files changed solely by formatting also retain identical command/argument tokens (`cmake-token-audit.json`). A disposable extracted-package fixture confirms reject → format → accept, while generated/external sentinel files remain untouched (`format-target-regression.json`). Assertion and timeout values remain unchanged.

Local behavior agrees with the pre-pass 66/66 baseline for both compiler configurations. This means identical suite outcomes, not byte-identical diagnostic logs or timing. No fresh framework build is claimed for the local reused Book-1.0 installations; hosted jobs build the pinned framework independently.

PDF: 330 → **332 pages**, with the same publication pair: **Pandoc 3.9.0.2** and **pandoc-crossref v0.3.24a** (the binary reports v0.3.24, built with Pandoc 3.9.0.2). Hosted logs directly record Pandoc and crossref’s Pandoc ABI version; the crossref release asset is selected by the tested CMake configuration, while v0.3.24 is the local binary’s self-report. The package script completed both builds, no unresolved final references or overfull boxes were found, and the archive contains 468 unique entries. Rendered EchoPair, constructor/initializer and extension CMake pages were inspected for legibility and frame fit.

Line accounting separates formatting growth from behavior changes:

| Area | Added | Removed | Net | Files |
|---|---:|---:|---:|---:|
| author style configuration | 381 | 0 | +381 | 3 |
| build, packaging and CI configuration | 1263 | 517 | +746 | 65 |
| companion production C++ (formatting only) | 516 | 385 | +131 | 53 |
| exercise C++ (formatting only) | 123 | 71 | +52 | 13 |
| manuscript listings | 365 | 383 | -18 | 18 |
| scope and supporting records | 434 | 165 | +269 | 4 |
| regression guard | 20 | 1 | +19 | 1 |

The production C++ increase is line wrapping, expanded bodies and author layout, with no new runtime mechanism. Build/configuration growth implements the explicitly requested author formatting targets, shared checks and packaged inputs. The approved Ch12 substitution changes the generator’s whitespace dependency while preserving its generated program.

## Status matrix

**75 applicable cells: all ●; 221 cells are not applicable (—).** This makes applicability explicit rather than repeating the earlier reports’ blanket 296 successful cells. The primary PROMPT issue dimensions and subsequent scope amendments determine the issue being assessed; adjacent dimensions below describe that issue’s concrete learning effect. This matrix does not claim a new broad publisher review. Unchanged accepted issue closures carry forward. No applicable cell was downgraded or newly promoted in this pass.

| Row | Issue | E | D | G | X | T | L | S | C | Current evidence |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 | Canonical terminology | — | — | — | — | — | ● | — | ● | `manuscript/frontmatter/conventions.md:36` |
| 2 | Opening gradient | ● | — | ● | — | — | — | — | — | `manuscript/chapters/01-why-snodec-exists.md:35` |
| 3 | Runtime/layer split | — | — | — | — | — | — | ● | — | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:13` |
| 4 | Event-loop model before internals | — | ● | ● | — | — | — | — | — | `manuscript/chapters/06-core-runtime-and-event-processing.md:18` |
| 5 | Shortest route to the first program | — | — | ● | — | — | — | ● | — | `manuscript/chapters/02-preparing-your-environment.md:18` |
| 6 | Application/system split | — | — | — | — | — | — | ● | ● | `manuscript/chapters/25-reading-complete-snodec-applications.md:11` |
| 7 | Express example before inventory | — | ● | — | — | ● | — | — | — | `manuscript/chapters/18-the-express-like-framework.md:23` |
| 8 | MQTT conversation and fundamentals | — | ● | ● | — | — | — | — | — | `manuscript/chapters/21-mqtt-support-in-snodec.md:23` |
| 9 | CMake starts with a consumer | ● | — | — | — | ● | — | — | — | `manuscript/chapters/27-cmake-components-and-linking-strategy.md:19` |
| 10 | Configuration follows one port | — | — | ● | — | ● | — | — | — | `manuscript/chapters/13-configuring-applications-and-named-instances.md:207` |
| 11 | Interpretation after capstone listings | — | — | — | ● | ● | — | — | — | `manuscript/chapters/30-building-minigateway.md:249` |
| 12 | Three explained extension excerpts | — | — | — | — | ● | — | ● | — | `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:368` |
| 13 | Expanded architectural synthesis | — | ● | — | — | ● | — | — | — | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:38` |
| 14 | Application-facing recovery settings | — | ● | — | — | ● | — | — | — | `manuscript/chapters/16-timeouts-retries-and-failure-modes.md:108` |
| 15 | Chapter and Part seams | ● | — | — | — | — | — | — | ● | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:237` |
| 16 | Taxonomy has one teaching home | — | — | — | — | — | ● | — | ● | `manuscript/chapters/08-servers-clients-and-connections.md:250` |
| 17 | Protocol chapters end with a transition | — | — | — | — | — | — | ● | ● | `manuscript/chapters/17-the-http-layer.md:309` |
| 18 | Edition/verification voice contained | — | — | — | ● | — | ● | — | — | `manuscript/chapters/02-preparing-your-environment.md:167` |
| 19 | Concrete actors replace abstraction stacks | — | — | — | ● | ● | ● | — | — | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:15` |
| 20 | Logging explanation and current wording | — | — | — | ● | — | ● | — | — | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:132` |
| 21 | Testing starts from a problem | ● | — | ● | — | — | — | — | — | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:14` |
| 22 | Performance stance and limits | — | ● | — | ● | — | — | — | — | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:391` |
| 23 | Appendix entry supports different readers | ● | — | — | — | — | — | — | ● | `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:13` |
| 24 | TLS configuration is on the page | — | ● | — | — | ● | — | — | — | `manuscript/chapters/15-tls-across-the-framework.md:157` |
| 25 | Experience precedes formal vocabulary | ● | — | ● | — | — | — | — | — | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:21` |
| 26 | Address-comparison seam | — | — | — | — | — | — | ● | ● | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:248` |
| 27 | Core mechanism readable without the lab | — | ● | — | — | ● | — | — | — | `manuscript/chapters/21-mqtt-support-in-snodec.md:25` |
| 28 | Part II checkpoint interface printed | — | — | — | — | ● | — | — | ● | `manuscript/chapters/06-core-runtime-and-event-processing.md:257` |
| 29 | A distinct IoT worked decision | — | — | — | ● | ● | ● | — | — | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:64` |
| 30 | Native/composed MQTT trace | — | ● | — | — | ● | — | — | — | `manuscript/chapters/22-mqtt-over-websocket.md:28` |
| 31 | One-peer timeline before distinctions | — | — | ● | — | ● | — | — | — | `manuscript/chapters/08-servers-clients-and-connections.md:30` |
| 32 | Verification phrasing restored to baseline | — | — | — | ● | — | ● | — | — | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:327` |
| 33 | Purposeful, explicitly linked repetition | — | — | — | — | ● | — | — | ● | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:524` |
| 34 | References and narrative order | — | — | — | — | — | — | ● | ● | `manuscript/chapters/02-preparing-your-environment.md:445` |
| 35 | Slips and register | — | — | — | ● | — | ● | — | — | `manuscript/chapters/13-configuring-applications-and-named-instances.md:595` |
| 36 | Apparatus and placement | — | — | — | — | — | — | ● | ● | `manuscript/chapters/25-reading-complete-snodec-applications.md:284` |
| 37 | Cadence and style without shortening | — | — | — | ● | — | ● | — | — | `manuscript/chapters/08-servers-clients-and-connections.md:95` |

| Dimension | ● | ◐ | ○ |
|---|---:|---:|---:|
| E | 6 | 0 | 0 |
| D | 9 | 0 | 0 |
| G | 8 | 0 | 0 |
| X | 9 | 0 | 0 |
| T | 15 | 0 | 0 |
| L | 9 | 0 | 0 |
| S | 8 | 0 | 0 |
| C | 11 | 0 | 0 |

Updated supporting evidence is concentrated in row 1/L (canonical declarations and network-family wording), row 10/G,T (effective running value), row 18/L,X (edition wording), row 33/T,C (retained repetition links), and row 37/L,X (author code style and local cadence). Their current file:line evidence appears in the item table; the score remains ●.

## Gates and hosted workflows

| Gate | Result and evidence |
|---|---|
| Matrix | 75/75 applicable cells ●; 0 ◐; 0 ○. |
| Book package | Local and hosted PASS; 332-page book, 9-page proposal, 60-page sample; Pandoc 3.9.0.2 / crossref release v0.3.24a, Pandoc ABI 3.9.0.2. |
| GCC 13.3.0 | All companion targets rebuilt; local 66/66 and hosted 66/66 labs PASS. |
| Clang 18.1.3 | All companion targets rebuilt; local 66/66 and hosted 66/66 labs PASS. |
| Hosted framework evidence | Both jobs: 185/185 framework CTests and 4/4 external Echo CTests PASS. |
| Hosted smoke/lifetime suites | Teaching smoke, behavioral smoke, SSE lifetime and WebSocket echo steps all PASS for both compilers. |
| Source alignment | PASS against fresh Book-1.0 clone: 1,448 manifest files, 33 chapter/appendix records, 37 exact listings. |
| External anchors | PASS against fresh Book-1.0 clones of SNodeC/mqttsuite and SNodeC/OpenWRT; source existence, not deployment execution. |
| format-check | PASS locally, in both hosted compiler jobs, and in an extracted source package. Tools: clang-format 18.1.3; cmakelang 0.6.13. |
| Editorial checks | check-smoothing.py: 16 groups PASS; check-polish.py: 9/9 groups PASS; check-final.py PASS, covering all 204 C++ fences. |
| References, metrics, hygiene and width | All requested scripts PASS; 90-column listing limit; 321 chapter references with 374 historical dispositions. |
| Checker tests | test-final.py 23/23; test-polish.py 17/17; publication-configure tests 4/4. |
| Author tree | HEAD and filtered porcelain status identical at entry and exit; author files and porting/ untouched. |

Hosted runs test **A+B tip 446d3e3**, not an earlier historical source. The final evidence commit adds this report, measured records, and editorial-checker maintenance (attributed fences and the updated Ch7 fixture); it changes no manuscript, companion, CI workflow, build configuration or pinned-source input.

| Workflow / job | Run | Job | Conclusion | Observed tools |
|---|---|---|---|---|
| Book package / build-book-package | [36138689872](https://github.com/SNodeC/SNode.C-Book/actions/runs/36138689872) | 108082897020 | success | Pandoc 3.9.0.2; crossref Pandoc ABI 3.9.0.2; release asset v0.3.24a from tested CMake configuration; TeX Live 2026. |
| Companion examples / GCC | [36138689770](https://github.com/SNodeC/SNode.C-Book/actions/runs/36138689770) | 108082897026 | success | GCC/G++ 13.3.0; clang-format 18.1.3; cmakelang 0.6.13. |
| Companion examples / Clang | [36138689770](https://github.com/SNodeC/SNode.C-Book/actions/runs/36138689770) | 108082897210 | success | Clang/Clang++ 18.1.3; clang-format 18.1.3; cmakelang 0.6.13. |

Every step in each hosted job concluded success. Job records and selected timestamped logs are archived under `followup-16-evidence/hosted-*`. Local scripts ran against the same companion sources with the workflow’s compiler versions. The Ch12 build interruption and approved generator correction are recorded separately. One editorial mutation fixture initially failed because it still quoted B’s superseded Ch7 sentence; only the fixture’s source text was updated, retaining the same negative substitution, assertions and expected rejection. The original failure log remains historical. No companion lab assertion, timeout or behavior changed.


## Token accounting

Whitespace tokens use the existing manuscript-metrics authority. No code or teaching content was cut to reduce counts. B’s explicitly requested duplicate-claim joins and wording changes account for the small prose reduction. Existing documented chapter waivers remain below 5%; the prior narrow backmatter waiver remains explicit at **810/800, within 812**. The global ceiling remains **115,000**.

| Touched chapter | Before | After | Change | Base cap |
|---|---:|---:|---:|---:|
| 2 — Preparing Your Environment | 3,341 | 3,335 | -6 | 3,250 |
| 3 — Your First Working Program: The Echo Pair | 3,020 | 3,016 | -4 | 3,270 |
| 4 — The SNode.C Runtime Mental Model | 2,938 | 2,927 | -11 | 3,050 |
| 6 — Core Runtime and Event Processing | 3,523 | 3,523 | +0 | 3,850 |
| 7 — Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 4,288 | 4,276 | -12 | 4,250 |
| 8 — Servers, Clients, and Connections | 3,224 | 3,224 | +0 | 3,334 |
| 10 — Writing `SocketContext` Classes Well | 3,123 | 3,122 | -1 | 3,140 |
| 12 — Building the Same Protocol over Different Lower Layers | 2,628 | 2,630 | +2 | 2,605 |
| 13 — Configuring Applications and Named Instances | 4,595 | 4,595 | +0 | 4,673 |
| 14 — Logging, Diagnostics, and Runtime Introspection | 2,847 | 2,847 | +0 | 2,800 |
| 17 — The HTTP Layer | 2,482 | 2,481 | -1 | 2,600 |
| 18 — The Express-Like Framework | 2,244 | 2,245 | +1 | 2,315 |
| 19 — Server-Sent Events and Real-Time HTTP | 3,307 | 3,307 | +0 | 3,370 |
| 20 — WebSocket and Protocol Upgrade | 3,019 | 3,022 | +3 | 3,100 |
| 21 — MQTT Support in SNode.C | 3,342 | 3,342 | +0 | 3,405 |
| 22 — MQTT over WebSocket | 2,125 | 2,129 | +4 | 2,282 |
| 24 — Database Support and Application State | 3,858 | 3,858 | +0 | 3,926 |
| 25 — Reading Complete SNode.C Applications | 2,657 | 2,656 | -1 | 2,600 |
| 27 — CMake Components, Public Headers, and Linking Strategy | 3,780 | 3,778 | -2 | 4,000 |
| 30 — Building MiniGateway | 4,631 | 4,633 | +2 | 4,618 |
| 31 — Extending MiniGateway with a New Network Role | 2,860 | 2,861 | +1 | 2,841 |
| 32 — Architectural Judgment: Choosing the Right Layer and Boundary | 3,180 | 3,180 | +0 | 3,350 |
| A — Reading and Extending the Framework | 3,972 | 3,972 | +0 | 3,994 |
| **Full book** | **111,729** | **111,704** | **-25** | **115,000** |

## Outside this repository and limits

The Clang 21 `-Wnrvo` / `-Werror` framework follow-up remains at `src/tools/snodec-control/src/ConfigActions.cpp:296`. The pinned source still returns the local `path` there; this pass preserves the previously verified failure statement and does not claim a fresh Clang 21 framework build. Framework formatting diagnostics under both tried clang-format versions and cmakelang are also retained as calibration evidence, without changing the framework.

Final freeze: no further broad refinement is authorized. Later work is limited to an actual technical error, broken build/reference or production defect.
