# Pedagogical smoothing — Follow-up 11 run

## Run history

- **P0b stop:** source alignment found framework drift; the run stopped in
  `965bcbc`. [Original report](REPORT-P0b-stopped.md) and P0b evidence remain historical.
- **Phase R at 8b8da56:** the public pin and anchors were reconciled; framework
  and exercise failures left the gate qualified. The subsequent adaptations were
  reverted. [Historical report](REPORT-R4-before-continuation.md).
- **9746d186–07ca9a29:** the author added shutdown log draining, moved signal
  processing to the event-loop thread, then simplified logging synchronization.
  [Initial verification](shutdown-recheck-9746d186/REPORT.md),
  [signal investigation](shutdown-investigation-9746d186/REPORT.md),
  [signal-fix verification](shutdown-recheck-55c36e41/REPORT.md), and
  [simplification verification](shutdown-recheck-07ca9a29/REPORT.md) are completed
  historical work. The only carried-forward driver change is
  [2e71f2a's completed-log observation](checkpoint-log-fix/REPORT.md).
- **Phase R2 at 07ca9a29:** Follow-up 11 resumes from `a2ecd9c`, preserving all
  commits and the unfinished P1 snapshot. A fresh public clone confirms the pin.
  The 1,448-file manifest and three prescribed anchors are updated; one local
  dispatch-condition claim is corrected. Fresh build/runtime verification passes: framework 185/185, external Echo
  4/4, labs 62/62, and all smoke/lifetime suites. The resumed P0b and P1–P7 gates complete below.

## Governing scope and source

[PROMPT.md](PROMPT.md), [FOLLOWUP-01 §5](FOLLOWUP-01.md), and
[FOLLOWUP-11](FOLLOWUP-11.md) govern this run. PROMPT.md remains unchanged.
Follow-ups 02–10 authorize no new work. No timeout or assertion changes.
The previous report is preserved as [REPORT-before-FOLLOWUP-11.md](REPORT-before-FOLLOWUP-11.md).

Author source: `/home/voc/projects/snodec/snode.c`, clean at
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. The freeze authority is
[framework-freeze-R2.json](framework-freeze-R2.json). The new source digest is
`2face99fc58fb1ec5374c35d88e6fcd9c7a7d56b52ea44cb00e49eb4825b9a2b`.
The retained patch is empty. The reviewed claim digest now matches the new source manifest.

A pre-existing ignored `build/rebaseline-R2-07ca9a29` directory was preserved.
This run uses a new archive/build/prefix beneath
`build/rebaseline-R2-07ca9a29-followup11`, verified against all 1,448 frozen files.
No fetch, build or edit occurs in the author's framework tree.

## Outcome and decisions

Completed: **100,338 → 110,177 raw whitespace tokens** (+9,839); **2,839 above the must**, **2,161 below the wish**, and **4,823 below the ceiling** of 107,338 / 112,338 / 115,000. Prose: 102,339; fenced tokens: 7,838. All 33 units and front/Part/epilogue/back groups meet their floors and caps. **No floor or cap waivers.** Original metrics-before.json and metrics-after.json remain historical; the fresh exit measurement is [metrics-after-final.json](metrics-after-final.json).

- **D1:** 32 numbered chapters, 11 Parts, Appendix A; old Ch4 and Ch24 split at the approved topics. See smoothing-structure.json and the chapter ledger below. All 56 pre-existing topic anchors remain resolvable.
- **D2:** canonical glossary at `manuscript/frontmatter/conventions.md:19`; snapshot substitutions reread in context in P1-context-review-notes.md. Final sweep also corrects the hyphenated server-instance description in `manuscript/chapters/17-the-http-layer.md:47`, lower-family-specific setup in Ch12 and configured endpoint wording in Ch32. These are local precision corrections, not a wholesale reversal.
- **D3:** version/pin/checkout/alignment in Ch2’s Edition and source baseline sidebar; Preface retains one version statement. No patch application is required. Final deployment wording says prepared source revision instead of the prohibited provenance phrase (`manuscript/chapters/28-deployment-on-linux-and-openwrt.md:295`). All seven prohibited provenance phrases are absent outside Ch2.
- **D4:** three additional worked decisions in Ch32 cover persistence, independent processes and limits of cross-family reuse. Each follows requirements/options/five questions/verdict/consequence; see the ledger’s exact source evidence.
- **D5:** logging sentence ends “not CMake component names” (`manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md`, ledger below); unneeded migration wording removed.
- **D6:** the book reports no performance figures; Ch29 teaches measurement and interpretation, not expected capacity. The exact statement is identified in the ledger.

The P−1 prerequisite remains `c70d9d1`: only the specified exercise targets request `cxx_std_20`. Historical P-minus-1-build.log records Clang 19 with default `__cplusplus=201703` and all 21 targeted compilation units. The fresh R2/P7 build uses GNU 16.2 and compiles every target against the new installation; those are separate observations. Existing commits are retained, including the author-authorized `2e71f2a` completed-log read after shutdown. No existing assertion or timeout changes were carried forward or made in this run.

The prompt’s Ch31 `MeasurementInputSocketContext.cpp` names the corresponding actual `MeasurementUnixSocketContext.cpp` in this repository. That 147-line file remains complete in the companion; three unmarked excerpts teach framing/buffering, parse/validation and acceptance. Its registered source anchor is retained. The author additionally approved the existing 67-line complete CMake listing adjustment: seven blank separators were removed from both canonical source and printed copy, producing 60 lines with identical tokens and behavior (P3-gate-notes.md).

## Gates and verification

| Gate | Commit | Evidence |
|---|---|---|
| P0a, historical scope | `371a1b0` | Original scope/freeze retained |
| P−1 | `c70d9d1` | Target C++20 prerequisite; fresh compilation repeated at R2/P7 |
| Original P0b stop | `965bcbc` | REPORT-P0b-stopped.md and P0b logs |
| R2 scope/R0 | `8fd9a23` | R2-preconditions.json; fresh public clone; framework-freeze-R2.json |
| R2 R1 pin | `4762369` | 1,448-file manifest; empty patch; public 07ca9a29 |
| R2 R2 anchors | `69ac502` | R2-anchor-review.md; all source anchors verified |
| R2 R3 claims | `cfd65ab` | R2-claim-review.md; local event dispatch correction |
| R2 evidence | `2be416b` | R2-build/results.json, R2-entry-results.json |
| P0b R2 resume | `77226ab` | P0b-R2-resume-results.json; all 13 groups pass |
| P1 | `c603b8f` | P1-context-review-notes.md, terminology-counts.md, metrics-after-P1.json |
| P2 | `9df7d00` | P2-registry-review.md, P2-source-preservation.json, P2 logs |
| P3 | `0deb8b3` | P3-api-review.md, P3-gate-notes.md, P3-apparatus.json, P3 labs |
| P4 + P5 | `6683818` | P4-P5-api-review.md, P5-core-mechanism-review.md, separate phase metrics |
| P6 | `6b7d7c0` | seam-log.md and P6-seam-snapshots.json: all 55 manifest pairs |
| P7 | `c1db599` | P7-final-results.json; final logs and diagnostics linked below |

R2, pre-API P3 and P7 freeze records are identical: framework-freeze-R2.json, framework-freeze-P3-R2.json and framework-freeze-P7-R2.json. The author tree was never modified. The final digest comparison is recorded in P7-freeze-check.log.

**Inspected:** all registered source anchors, the three framework commits’ affected claims, snapshot vocabulary in context, APIs in new/changed code, every core teaching mechanism and every seam. Specific header:line API evidence is in [P3-api-review.md](P3-api-review.md) and [P4-P5-api-review.md](P4-P5-api-review.md). The retry setters are at `src/net/config/ConfigPhysicalSocket.h:83–101`, reconnect at `src/net/config/ConfigPhysicalSocketClient.h:70–73`, and getConfig at `src/core/socket/Socket.h:73`; zero retries means unlimited. This is source inspection, separately supported by compilation and runtime observations below.

**Compiled:** a clean `git archive` export of 07ca9a29 in a new build/prefix; all companion targets; the exact added retry setter sequence in an isolated EchoPair consumer; all book/proposal/sample PDFs. P7 rebuilds companions in a fresh examples-P7 directory against the R2 installation. The rebuilt reading PDF is 326 pages; visual/page-layout review and publisher pagination are separate work.

**Run:** R2 framework tests **185/185**, external Echo **4/4**, then initial **62/62** public labs. After the four distinct-objective registrations, P7 passes **66/66**, no skips, including the three equipped cases available locally. Teaching, behavior and lifetime suites all pass. Logs are P7-R2-labs.log, P7-R2-teaching.log, P7-R2-behavior.log and P7-R2-lifetime.log. These tests do not imply Bluetooth hardware, OpenWrt deployment or MQTTSuite production validation.

**Static/final:** chapter-reference checks; source alignment with **zero errors**, **33 ordered records and 37 exact complete listings**; hygiene; all existing ci/test-*.py regressions; package build and extracted-package hygiene. The new check-smoothing.py passes **all 16 assertion groups**. Its four tests include independent mutations for every group, nested-fence handling and objective-exclusion diagnostics. See P7-smoothing.log, P7-test-smoothing.log, P7-source-alignment-final.log, P7-references-final.log, P7-hygiene-final.log, P7-package-final.log and P7-extracted-hygiene-final.log.

The first P7 package built but extracted hygiene found that packaging still copied the historical chapter registries. The invariant is that the packaged checker must carry its own active data. `packaging/cmake/MakeProposalPackage.cmake:41` now replaces those two obsolete registry paths with the active smoothing files; PACKAGE-CONTENTS.txt lists them. No check was weakened. P7-R2-results.json and its failure log preserve that attempt; P7-final-results.json points to the passing final build/extraction. This was a book packaging omission, not framework behavior.

## Chapter outcomes


Before counts are the author’s §6 allocation of c7b76c1 (including the planned split halves). After counts are freshly measured raw tokens. No waiver is used.

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

Group totals and exact per-file metrics are in metrics-after-final.json. P4’s projection stayed below 113,500, so optional rows 30 and 31 were completed. There is no padding recovery or waiver.

## Terminology and diagnostics

[terminology-counts.md](terminology-counts.md) preserves the required c7b76c1→P1 comparison and adds the final c7b76c1→P7 comparison. The final deprecated-term counts are zero outside the explicit immutable-reference exceptions. Server-instance and client-instance forms are zero. Remaining communication/server/client-role prose denotes design responsibilities; exact lines are listed in [terminology-allowlist.md](terminology-allowlist.md). Carrier is confined to Ch21–22, the glossary and the two preserved IDs; every occurrence is listed. The P1 inventory itself is retained separately.

[smoothing-diagnostics.json](smoothing-diagnostics.json) records every requested diagnostic before and after for all 33 units, including first-400-word identifiers and the last three body blocks. [diagnostic-review.md](diagnostic-review.md) records the manual interpretation. Identifier density rises notably in Ch18 because the requested complete dispatch and its trace name the concrete APIs; Ch16 adds the requested compilable setters. Logging and appendix reference density remains intentional. Abstract-cluster hits include tables, captions and index entries; the actual prose was read with its concrete actors. These proxies are not optimized as word-count targets.

## Apparatus for the four split chapters

Every unit has three objectives, one recap, two reviews, two labs, one design exercise and all five public answer sections. There are 99 objectives and 165 exercises; all eleven Part checkpoints sit in their last chapter’s apparatus. No TODO(P3-apparatus) remains. P3-apparatus.json and the P7 checker verify the inventory.

| Chapter | O1 | O2 | O3 | Public answer file |
|---|---|---|---|---|
| 4 | Runtime lifetimes | Attribute observations to runtime objects | Per-peer versus shared state | companion/exercises/ch04/README.md |
| 5 | Decode type/header/component | Predict affected layers | Confirm component choices | companion/exercises/ch05/README.md |
| 25 | Target to observable contract | Entry point as assembly | Relate app, consumer and tests | companion/exercises/ch25/README.md |
| 26 | Recovery versus accepted/durable state | Assign process responsibilities | Trace publication evidence | companion/exercises/ch26/README.md |

| Chapter / exercise | Objective mapping and task | CTest (labs only) |
|---|---|---|
| 4 / 1 Review | O1: independent lifetimes | — |
| 4 / 2 Review | O2: attribute completed EchoPair log | — |
| 4 / 3 Lab | O3: shared versus separate accepted state | exercise-ch04-model-instances |
| 4 / 4 Lab | O1/O2: independent peers | exercise-ch04-independent-peers |
| 4 / 5 Design | O1/O3: second flow and state ownership | — |
| 5 / 1 Review | O1: RFCOMM/TLS type decoding | — |
| 5 / 2 Review | O1/O2: three layer changes | — |
| 5 / 3 Lab | O2/O3: identical echo over IPv4 and Unix | exercise-ch05-layer-families |
| 5 / 4 Lab | O1/O3: component choice and link outcome | exercise-ch05-layer-component |
| 5 / 5 Design | O2: Unix input layer choices | — |
| 25 / 1 Review | O1: in-tree versus installed links | — |
| 25 / 2 Review | O2: composition-root inventory and prediction | — |
| 25 / 3 Lab | O1/O3: target/entry point/HTTP contract | exercise-ch25-composition |
| 25 / 4 Lab | O1/O3: installed-consumer trace | exercise-ch25-consumer-trace |
| 25 / 5 Design | O2/O3: reading order and observations | — |
| 26 / 1 Review | O1/O2: ownership/restart/raw versus projection | — |
| 26 / 2 Review | O3: publication evidence by process | — |
| 26 / 3 Lab | O1/O2: equipped Part IX persistence checkpoint | exercise-ch26-part-checkpoint |
| 26 / 4 Lab | O2/O3: local broker-mediated publication | exercise-ch26-publication-trace |
| 26 / 5 Design | O1/O2/O3: destination failure and evidence | — |

New labs reuse canonical drivers, with no new application implementation. The Ch5 family lab asks about byte behavior and layer selection, not later address semantics. Ch25 reads the consumer as an assembled application; Ch26 attributes submission/subscription/receipt to participants and requires no external broker or database. Ch4 retains both existing experiments. The old Ch24 apparatus is divided between Ch25/26, so each now has an unequipped runnable lab.

## Preservation and registry accounting

| Protected item | Baseline | Final | Explanation |
|---|---:|---:|---|
| Exact source markers | 37 | 37 | Ch18 +1; Ch31 −1; equality checked |
| Index entries | 1,033 | 1,037 | Entries for new teaching sections |
| Figure IDs | 18 | 18 | All references and asset paths resolve |
| Executable/config fences | 293 | 302 | Required dispatch, setters, TLS and excerpts; full companion sources retained |
| Fenced tokens | 8,151 | 7,838 | −313 (−3.84%), inside ±5%; named Ch27 tree/Ch31 presentation changes |
| Public labs | 62 | 66 | Four distinct-objective registrations; all pass |
| Rule boxes | 20 | 20 | No new rule box |

P7-preservation.json records the inventory. Existing heading/topic identities remain; the reference checker validates all 56 registered topics and each manual chapter reference by its recorded target. Existing C++ companion source additions/deletions are **+0/−0** across this run after rename detection. Production CMake formatting is **+0/−7 blank lines**, no statement change. P3 lab-registration support is **+18/−3 lines**, net +15 across ch05/ch25/ch26 CMake files; these four registrations are expressly required by §5a. Driver edits are mechanical chapter-path changes only. Existing assertions and timeout values remain unchanged. New smoothing checker/regression files are review/test tooling explicitly requested by §12, not application code. Packaging substitutes two registry paths at neutral code-line count.

Live structure-sensitive registries changed in P2: manuscript/book-files.txt; smoothing-structure.json (chapters, Parts, map, topic IDs, budgets); smoothing-reference-register.json; ci/check-chapter-references.py and ci/test-chapter-references.py; review/verification/source-claims.json; companion/exercises directory/CMake/CTest/relative-driver/public-answer paths and top-level foreach; chapter source markers and exercise pointers; ci/run-example-lifetime-tests.py and ci/run-teaching-smoke-tests.py; README.md; STRUCTURE.md; How to Read This Book; affected Part openers; review/proposal/CMakeLists.txt and all three proposal texts; current work-plan ledger and this pass’s chapter-ledger.md. See P2-path-map.json and P2-registry-review.md for the detailed migration. P7 additionally corrects packaging/cmake/MakeProposalPackage.cmake and PACKAGE-CONTENTS.txt and refreshes final Part totals/proposal metrics. .github/workflows, source-baseline and production were searched; no additional live chapter references needed migration. Historical phase JSON/checkers/reports remain unchanged.

## Dimension matrix — editorial self-assessment

Scores 1–5 use PROMPT §9 after the pass; this is not an independent review or a re-score of the original diagnosis. Evidence is the chapter ledger, diagnostic-review.md, P5-core-mechanism-review.md and the 55-pair seam-log.md. A 4 records retained technical density or a concise reference treatment; a 5 records the requested learning cycle with concrete evidence.

| Unit | E | D | G | X | T | L | S | C |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 4 | 5 | 4 | 4 | 5 | 4 | 4 |
| 2 | 5 | 4 | 4 | 4 | 5 | 5 | 4 | 5 |
| 3 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 |
| 4 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| 5 | 5 | 4 | 5 | 4 | 5 | 5 | 5 | 5 |
| 6 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 7 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 8 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 9 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 4 |
| 10 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| 11 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| 12 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 |
| 13 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 14 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 15 | 4 | 5 | 4 | 5 | 5 | 5 | 4 | 5 |
| 16 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 17 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 |
| 18 | 5 | 5 | 4 | 4 | 5 | 5 | 5 | 5 |
| 19 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| 20 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| 21 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| 22 | 5 | 5 | 4 | 4 | 5 | 5 | 5 | 5 |
| 23 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 24 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| 25 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| 26 | 5 | 5 | 4 | 4 | 5 | 5 | 5 | 5 |
| 27 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | 5 |
| 28 | 4 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 29 | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| 30 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 |
| 31 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |
| 32 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| A | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 |
| Population variance | 0.129 | 0.107 | 0.244 | 0.211 | 0.057 | 0.000 | 0.250 | 0.057 |

## Open, qualified and blocked items

- **Open in this run:** none. Every required gate, floor/cap and check is met. No stop condition occurred after R2 began.
- **Qualified evidence:** runtime results are bounded local observations against the new installation. No Bluetooth equipment coverage, OpenWrt deployment certification, full MQTTSuite deployment, long-duration reliability claim or capacity result is implied. The equipped local cases did run; equipped does not mean every platform was validated. PDFs were rebuilt, not visually certified.
- **Editorial qualification:** dimension scores are the editor’s self-assessment, with the retained density and limitations recorded per chapter. The wish is aspirational; the absolute must and ceiling are satisfied without waivers.
- **Blocked:** none. All historical stop/investigation files and commits remain available. Work branch only; no merge into SNode.C-2.0-refinement.
