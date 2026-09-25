# Follow-up 15 — refinement and validation report

**Scoped edits committed; the publisher gate is not fully closed.** The local Clang run has 65/66 labs because the unchanged Ch16 live-log parser read an incomplete JSON record. Bibliography completion also leaves backmatter at 812 tokens against the older 800-token cap; no unapproved exception or teaching cut has been made. Hosted results are recorded below. No further broad refinement follows this pass.

Main was fast-forwarded with `--ff-only` from ccbe53b to 8328dfc and pushed before editing. Default-branch HEAD replaced old source pins. The author framework tree was read-only and unchanged. Every existing historical record remains; FOLLOWUP-15.md contains the verbatim instruction and clarifications.

## Commits

| Group | Commit | Scope |
|---|---|---|
| A | `6af9c81` | HEAD source identity and external anchors |
| B | `55507ca` | Technical corrections and QUIT regression |
| C | `14263b0` | Publication tools, formatting, identity channel, index and bibliography |
| D | `09803e1` | Linked copy-edit, retained examples and local cadence |
| C integration | `f6b47e0` | Actual PDF build/render findings, regression guards and refreshed proposal measurements |

An additional C integration commit was necessary after the first A–D push exposed the obsolete caption override and rendered layout defects. This departs from the requested four item commits; it preserves the already-pushed history and makes the corrective build change explicit. The final evidence commit contains this report and logs. The two outstanding author decisions are not treated as approvals. A concrete two-line Ch16 reader patch is saved as followup-15-evidence/ch16-proposed.patch but has not been applied; isolated tests show it defers incomplete records and still rejects complete malformed JSON.

## Observed default-branch HEADs

SHAs below are observations, never checkout/fetch targets. External heads did not move. Book main advanced through this work; its end observation is the tested production tip before the evidence-only commit.

| Repository / branch | Start | End |
|---|---|---|
| SNodeC/snode.c / master | `07ca9a2936ee72582df7d159cb06666fe23e30f8` | `07ca9a2936ee72582df7d159cb06666fe23e30f8` |
| SNodeC/mqttsuite / master | `5fef5c3036928dfa40ad4f124bb237cc9c3202bb` | `5fef5c3036928dfa40ad4f124bb237cc9c3202bb` |
| SNodeC/OpenWRT / main | `5bef8cca5982838a7191a148633c1058f154e5eb` | `5bef8cca5982838a7191a148633c1058f154e5eb` |
| SNodeC/SNode.C-Book / main | `8328dfcd796dcf9b1b65246d5ef020192d857458` | `f6b47e02b7cff1969b6b6f1e382108f8502f57f0` |

Author tree start/end: HEAD 07ca9a2936ee72582df7d159cb06666fe23e30f8, empty porcelain status in both records. The comparison ignores only the porting/ entry and never reads or changes that directory. See `author-tree-followup-15-start.json` and `author-tree-followup-15-end.json`.

## Findings and changes

All item findings reproduced unless qualified below. Pre-edit and source-HEAD file:line evidence is preserved in FOLLOWUP-15-VERIFICATION.md. This table gives current locations and commit attribution. Existence checks are not execution evidence.

| Item | Result | Current evidence | Commit group |
|---|---|---|
| A1 | Verified; default master target, digest/anchor drift failure, changed-file names and observed build SHA. | `source-baseline/book-source-baseline.env:5`; `ci/check-source-alignment.py:28`; `ci/build-companion-examples.sh:18` | A |
| A2 | Verified; clone master and check edition content; drift means update/check again, then pause affected examples if unresolved. Source/build/install separation retained. | `manuscript/chapters/02-preparing-your-environment.md:125`; `manuscript/frontmatter/preface.md:36` | A |
| A3 | Verified at feed main:2.0.0, OpenWRT source tag, hashed spdlog 1.17.0, disconnected FetchContent and valid net-un-phy. Live recipe checks replace false porting claims; logger/component rows met; deployment remains reader evidence. | `manuscript/chapters/28-deployment-on-linux-and-openwrt.md:256`; `manuscript/chapters/28-deployment-on-linux-and-openwrt.md:256` | A |
| A4 | Verified: bridge forwarding and independent raw/projection submissions; canonical SNodeC/mqttsuite master; fresh external existence guard. | `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:6`; `ci/check-external-anchors.py:16` | A |
| B1 | Verified and corrected: QUIT stops the receive batch, clears pending bytes and returns consumed count. Coalesced QUIT/PING expects EOF; existing assertions unchanged. | `companion/examples/LineProtocol-Server/LineCommandServerContext.cpp:44`; `companion/exercises/ch10/protocol.py:73`; `manuscript/chapters/10-writing-socketcontext-classes-well.md:189` | B |
| B2 | Verified composed SHARED target and public dependency tree; installed examples use http-server-express-legacy-in. Framework in-tree fragment unchanged. | `manuscript/chapters/25-reading-complete-snodec-applications.md:67`; `manuscript/chapters/27-cmake-components-and-linking-strategy.md:181` | B |
| B3 | Verified minimum checks and hosted GNU 13.3.0/Clang 18.1.3 evidence. Clang 21 remains the recorded framework compatibility failure; no fresh Clang 21 execution is claimed. | `manuscript/chapters/02-preparing-your-environment.md:71` | B |
| B4 | Verified missing optional Asio dependency; labelled Chapter 1 comparison package added, later guidance retained. | `manuscript/chapters/02-preparing-your-environment.md:106` | B |
| B5 | Verified facade/internal tick distinction and deferred atNextTick operation; compressed status sentence clarified. | `manuscript/chapters/06-core-runtime-and-event-processing.md:110`; `manuscript/chapters/06-core-runtime-and-event-processing.md:167` | B |
| B6 | Verified overstatement; memory tools can expose violations only on executed paths. | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:327` | B |
| B7 | Verified omitted log prefixes; named echoserver and conn=1 explicitly. | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:219` | B |
| B8 | Verified Router.h macro expansion; first explanation and capstone back-pointer added. | `manuscript/chapters/25-reading-complete-snodec-applications.md:167`; `manuscript/chapters/30-building-minigateway.md:765` | B |
| B9 | Verified broker identity and four Mqtt constructor parameters against client/Mqtt.h/.cpp. | `manuscript/chapters/21-mqtt-support-in-snodec.md:45`; `manuscript/chapters/21-mqtt-support-in-snodec.md:230` | B |
| B10 | Verified trust-source warning; full paragraph retained in warning box. | `manuscript/chapters/15-tls-across-the-framework.md:148` | B |
| B11 | Verified teaching socket default and existing override; Ch7 ownership pointer added. | `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:248` | B |
| C1 | Verified ABI mismatch; matching Pandoc 3.9.0.2/crossref assetv0.3.24a, parsed build-version guard shared by workflow and CMake. Obsolete caption overrides removed after actual build failure. | `ci/check-publication-tools.py:8`; `.github/workflows/book-package.yml:45`; `production/cmake/SNodeCBookTools.cmake:28` | C + C integration |
| C2 | Verified 53 fenced lines over 100 columns; measured PDF frame and chose 90. Sources/listings reformatted together; all 37 exact listings match. Guard installed; inline filename overflow fixed after rendering. | `ci/check-listing-width.py:7`; `manuscript/chapters/30-building-minigateway.md:249`; `manuscript/chapters/18-the-express-like-framework.md:251` | C + C integration |
| C3 | Verified shared stdout race; identity uses stderr captured in a dedicated file while async logging stays on stdout. Assertions/timeouts unchanged.50 IP and 50 Unix runs per compiler pass. | `companion/exercises/ch07/family-server.cpp:15`; `companion/exercises/ch07/families.py:27`; `companion/exercises/lab_support.py:30` | C |
| C4 | Verified both duplicate index directives and split headings; removed duplicates, normalized instances/Unix domain sockets. | `manuscript/chapters/13-configuring-applications-and-named-instances.md:211`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:165` | C |
| C5 | Verified checkpoint heading, figure attributes and README prefix convention. Full README retained; existing short running-head facility keeps new heading clear of page number. | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:327`; `manuscript/chapters/21-mqtt-support-in-snodec.md:21`; `companion/examples/MiniGateway/README.md:15` | C + C integration |
| C6 | Verified all four book editions/publishers/years using their publisher catalogues; complete entries retained. Older backmatter cap remains a separate open budget item. | `manuscript/backmatter/further-reading.md:12`; `manuscript/backmatter/further-reading.md:21` | C |
| D1 | Verified release-note wording; changed to present-tense API and invariant descriptions without removing the technical distinctions. | `manuscript/chapters/10-writing-socketcontext-classes-well.md:368`; `manuscript/chapters/25-reading-complete-snodec-applications.md:271`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:341` | D |
| D2 | Verified compressed logging sentences; expanded scope/type, bootstrap, filtering, delivery and confidentiality explanations. | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:132`; `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:231`; `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:293` | D |
| D3 | Verified repeated passages; explicit links retain content, and Echo receive/constructor excerpts match Ch3 exactly apart from excerpt indentation. | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:448`; `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:164`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:446`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:53` | D |
| D4 | Verified closing seam; flow paragraph remains in its original position with a local bridge; epilogue names singular design chapter. | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:237`; `manuscript/chapters/epilogue.md:57` | D |
| D5 | Verified cadence runs; merged selected paragraphs without dropping sentences, varied five Ch13 openers and six Ch30 bridges while retaining running values and ownership constraints. | `manuscript/chapters/08-servers-clients-and-connections.md:86`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:30`; `manuscript/chapters/30-building-minigateway.md:352`; `manuscript/chapters/epilogue.md:7` | D |

Skipped/refuted work: A1 chapter records already referenced the manifest; that relation was retained and its reviewed tree digest is checked. The SSE listener re-entrancy change was explicitly refuted and dropped by the author, so no SSE logic was changed. B3 reports the existing Clang 21 failure against unchanged source, not a newly executed Clang 21 build. No external repository was modified.

Publisher catalogues used for C6: [Stroustrup](https://www.informit.com/store/c-plus-plus-programming-language-9780321563842), [Meyers](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/), [Stevens/Fenner/Rudoff](https://www.informit.com/store/unix-network-programming-volume-1-the-sockets-networking-9780131411555), [Kerrisk](https://nostarch.com/tlpi).

## Gates

| Gate | Result |
|---|---|
| Editorial matrix | 37/37● in each dimension; 296●, 0◐, 0○. This does not override failing runtime/budget gates. |
| Book package, local | PASS: 330-page book, 9-page proposal, 61-page sample; two builds, 459 unique package entries; no unresolved references; no overfull boxes in the main book. |
| Publication pair | Pandoc 3.9.0.2 and pandoc-crossref release asset v0.3.24a (binary reports v0.3.24, built with Pandoc v3.9.0.2); TeX Live 2026. Shared parsed-version guard passes; mismatch/missing-version tests reject invalid pairs. |
| GCC 13.3.0 local labs | PASS 66/66; framework 185/185, external consumer 4/4; all teaching/behavior/lifetime suites pass. |
| Clang 18.1.3 local labs | FAIL 65/66: exercise-ch16-part-checkpoint raises JSONDecodeError in recovery.py:14 while the producer is still running. Framework 185/185, external consumer 4/4 and all subsequent smoke/lifetime checks pass. |
| Hosted gates | **PASS:** book-package [36117637249](https://github.com/SNodeC/SNode.C-Book/actions/runs/36117637249), companion [36117636257](https://github.com/SNodeC/SNode.C-Book/actions/runs/36117636257); GCC and Clang 66/66, every job successful. The local failure remains open. |
| C3 repetitions | PASS: 50 IP-family and 50 Unix-path executions per compiler; 200/200 total. No assertion or timeout changed. |
| SNode.C master alignment | PASS: 1,448 file content manifest, 33 chapter/appendix records, 37 exact listings, zero errors. Drift test verifies modified/missing/untracked file names. |
| External anchors | PASS: fresh mqttsuite master/OpenWRT main clones; explicit path and symbol checks. This proves source existence, not service deployment. |
| Author tree | PASS: observed HEAD and filtered porcelain status equal start; no author-tree writes. |
| Chapter/global budgets | PASS: 111,739 tokens, all floors preserved; eight documented cap waivers within 5%; global ceiling 115,000. |
| Backmatter budget | OPEN: 812 versus 800. The 12-token exception was requested because C6 requires the added bibliography details and NO CUTS preserves explanations. No answer is assumed; checker remains strict. |
| Editorial checks | Polish 9/9 and final regression guards pass; smoothing 15/16 groups passes except the backmatter cap. Smoothing tests 3/4 pass, with the current-manuscript acceptance test reporting that same open cap. |
| Other checks | Chapter references 321/321; hygiene, metrics, source alignment and external anchors pass. Final-guard tests 21/21, polish 17/17, metrics 5/5, references 6/6, drift 1/1, publication-version 3/3. |

## Hosted runs

| Run / tested book tip | Job | Version evidence | Conclusion |
|---|---|---|---|
| [36116892429](https://github.com/SNodeC/SNode.C-Book/actions/runs/36116892429) / `09803e1` | build-book-package | Matched pair; obsolete caption override still present | **failure**, preserved as the pre-correction result |
| [36116892333](https://github.com/SNodeC/SNode.C-Book/actions/runs/36116892333) / `09803e1` | Companion examples (gcc) | GNU 13.3.0; framework 185/185, consumer 4/4, labs 66/66; smoke/lifetime pass | **success** |
| Same run | Companion examples (clang) | Clang 18.1.3; framework 185/185, consumer 4/4, labs 66/66; smoke/lifetime pass | **success** |
| [36117637249](https://github.com/SNodeC/SNode.C-Book/actions/runs/36117637249) / `f6b47e0` | build-book-package | Pandoc 3.9.0.2; crossref reports built with Pandoc v3.9.0.2; book 330 pages, proposal 9, sample 61 | **success**, every job step passes |
| [36117636257](https://github.com/SNodeC/SNode.C-Book/actions/runs/36117636257) / `f6b47e0` | Companion examples (gcc) | GNU 13.3.0; framework 185/185, consumer 4/4, labs 66/66; all smoke/lifetime steps pass | **success**, every job step passes |
| Same run | Companion examples (clang) | Clang 18.1.3; framework 185/185, consumer 4/4, labs 66/66; all smoke/lifetime steps pass | **success**, every job step passes |

The hosted Clang successes do not cancel the local failure: the Ch16 reader is unchanged. Full job/step conclusions and selected version/test log lines are preserved in followup-15-evidence. The final evidence commit changes only review records and checker fixture support; later automatically triggered evidence-push runs are distinct from these recorded production-tip runs.

## Validation limits and remaining issue

Local workflow commands ran in separate Ubuntu 24.04.4 workspaces with GNU 13.3.0 and Clang 18.1.3, separate builds/install prefixes/homes and private temporary directories. Bubblewrap mounted the fresh public master clone read-only; the author tree was not mounted. The host kernel is shared. The compiled inputs are identical between the C archive used locally and final production tip; later changes are prose, publication and checker records.

The bare lab command was exactly `ctest --test-dir build/ci-book-examples --output-on-failure --no-tests=error`, with no caller LD_LIBRARY_PATH. GCC completed all workflow commands. Clang CTest returned 8 after running all 66 tests; the independent smoke/lifetime commands and C3 repetitions then ran separately and returned 0. No failure was hidden by a successful rerun. The Ch16 parser calls json.loads on every currently visible line beginning with `{`; its error is an unterminated string while the producer is live. This is evidence of a test-reader boundary problem, not a demonstrated framework defect. No unrelated parser fix, assertion change or timeout change was made.

Outside this repository: the OpenWRT main recipe selects the snode.c tag OpenWRT instead of master. The observed tag object is `8b8da56`, three commits behind observed master. Source history was read by deepening master, without checking out or fetching a tag/SHA target. Clang 21.1.8’s -Werror/-Wnrvo failure at src/tools/snodec-control/src/ConfigActions.cpp:296 remains a framework follow-up.

## PDF production and retained content

The pre-pass book has 328 pages; the matched-tool/refined book has 330 (+2). Proposal and sample remain 9 and 61. Final LaTeX logs contain no unresolved references; named PDF destinations are 4430→4525 in the book and 1540→1593 in the sample (anchors also include code/listing destinations). No fenced-code source line exceeds 90 source columns. The measured code content width is 453.543 pt (outer 465.498pt), or 435.022 pt in a note box. LMMono’s cell is about 4.707pt, so 90 columns occupy 423.66pt.

All 24 reformatted companion source files preserve their non-whitespace content and string literals against the post-B source (`formatting-preservation.json`). The 37 marked complete listings remain exact. B1 intentionally changes closure behavior; D3 intentionally restores exact Echo excerpt content, including its debug record and buffer declaration. The full MiniGateway README remains printed with CMAKE_PREFIX_PATH. No teaching passage, example, listing or explanation was deleted.

Rendered physical pages 135,165,271,276 and 293 confirm the repaired heading/inline filename and readable capstone/extension code. The main-book final log has no overfull boxes. Proposal and sample contents tables report 0.70139 pt overfull cells for “publisher”; these small table warnings are disclosed rather than counted as unresolved references or code wrapping. The pre-pass PDF has the same narrow contents-table column; it is not a regression from the tool change. Source is authoritative; PDF pagination is production evidence, not a replacement for source review.

## Editorial matrix

E=entry; D=depth; G=gradient; X=explicitness; T=theory–example; L=language; S=structure; C=continuity. Ratings retain the prior 37×8 completed editorial assessment. No rating changed from●, so there are no changed-status cells requiring a promotion rationale. Updated evidence below supports every affected row; all eight cells in a row share that row’s local evidence. Runtime and budget qualifications remain in the gate table.

| Row | Issue | E | D | G | X | T | L | S | C | Current evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Canonical terminology | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/05-layers-in-practice.md:35`; `terminology-allowlist.md:1` |
| 2 | Opening gradient | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/01-why-snodec-exists.md:19`; `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:21` |
| 3 | Runtime/layer split | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:13`; `manuscript/chapters/05-layers-in-practice.md:9` |
| 4 | Event-loop model before internals | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/06-core-runtime-and-event-processing.md:18` |
| 5 | Shortest route to the first program | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/02-preparing-your-environment.md:125`; `manuscript/frontmatter/preface.md:36` |
| 6 | Application/system split | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/25-reading-complete-snodec-applications.md:13`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:14` |
| 7 | Express example before inventory | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/18-the-express-like-framework.md:23`; `manuscript/chapters/18-the-express-like-framework.md:203` |
| 8 | MQTT conversation and fundamentals | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/21-mqtt-support-in-snodec.md:45`; `manuscript/chapters/21-mqtt-support-in-snodec.md:230` |
| 9 | CMake starts with a consumer | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/25-reading-complete-snodec-applications.md:67`; `manuscript/chapters/27-cmake-components-and-linking-strategy.md:181` |
| 10 | Configuration follows one port | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/08-servers-clients-and-connections.md:86`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:30`; `manuscript/chapters/30-building-minigateway.md:352`; `manuscript/chapters/epilogue.md:7` |
| 11 | Interpretation after capstone listings | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/30-building-minigateway.md:352`; `manuscript/chapters/30-building-minigateway.md:1167` |
| 12 | Three explained extension excerpts | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/31-extending-minigateway-with-a-new-network-role.md:248` |
| 13 | Expanded architectural synthesis | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:72`; `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:86`; `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:100` |
| 14 | Application-facing recovery settings | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/16-timeouts-retries-and-failure-modes.md:108` |
| 15 | Chapter and Part seams | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:237`; `manuscript/chapters/epilogue.md:57` |
| 16 | Taxonomy has one teaching home | ● | ● | ● | ● | ● | ● | ● | ● | `check-polish.py:74`; `manuscript/frontmatter/conventions.md:23`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:83` |
| 17 | Protocol chapters end with a transition | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/17-the-http-layer.md:310`; `manuscript/chapters/18-the-express-like-framework.md:289`; `check-smoothing.py` group 8 |
| 18 | Edition/verification voice contained | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/02-preparing-your-environment.md:125`; `manuscript/frontmatter/preface.md:36` |
| 19 | Concrete actors replace abstraction stacks | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:210`; `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:246`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:45`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:74` |
| 20 | Logging explanation and current wording | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:132`; `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:231`; `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:293` |
| 21 | Testing starts from a problem | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:16` |
| 22 | Performance stance and limits | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/29-testing-debugging-and-benchmarking.md:327` |
| 23 | Appendix entry supports different readers | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:24` |
| 24 | TLS configuration is on the page | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/15-tls-across-the-framework.md:148` |
| 25 | Experience precedes formal vocabulary | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/01-why-snodec-exists.md:19`; `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:21` |
| 26 | Address-comparison seam | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:254` |
| 27 | Core mechanism readable without the lab | ● | ● | ● | ● | ● | ● | ● | ● | `P5-core-mechanism-review.md:1`; `chapter-ledger.md:1`; `manuscript/chapters/18-the-express-like-framework.md:23`; `manuscript/chapters/21-mqtt-support-in-snodec.md:39` |
| 28 | Part II checkpoint interface printed | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/06-core-runtime-and-event-processing.md:254` |
| 29 | A distinct IoT worked decision | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/23-designing-iot-systems-with-multiple-protocols.md:74` |
| 30 | Native/composed MQTT trace | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/22-mqtt-over-websocket.md:20` |
| 31 | One-peer timeline before distinctions | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/08-servers-clients-and-connections.md:23` |
| 32 | Verification phrasing restored to baseline | ● | ● | ● | ● | ● | ● | ● | ● | `followup-15-evidence/polish.log:1` (46 constructions) |
| 33 | Purposeful, explicitly linked repetition | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:448`; `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:164`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:446`; `manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:53` |
| 34 | References and narrative order | ● | ● | ● | ● | ● | ● | ● | ● | `followup-15-evidence/references.log:1` (321 references) |
| 35 | Slips and register | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/10-writing-socketcontext-classes-well.md:368`; `manuscript/chapters/25-reading-complete-snodec-applications.md:271`; `manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:341` |
| 36 | Apparatus and placement | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:327`; `manuscript/chapters/21-mqtt-support-in-snodec.md:21`; `companion/examples/MiniGateway/README.md:15` |
| 37 | Cadence and style without shortening | ● | ● | ● | ● | ● | ● | ● | ● | `manuscript/chapters/08-servers-clients-and-connections.md:86`; `manuscript/chapters/13-configuring-applications-and-named-instances.md:30`; `manuscript/chapters/30-building-minigateway.md:352`; `manuscript/chapters/epilogue.md:7` |

Dimension totals: E 37/0/0; D 37/0/0; G 37/0/0; X 37/0/0; T 37/0/0; L 37/0/0; S 37/0/0; C 37/0/0 (●/◐/○).

## Extent

Fresh whitespace-token measurement includes markup and fences. Before is `8328dfc`; after is the final manuscript. Every touched chapter/section is included, even if its token count did not change.

| Chapter / section | Before | After | Change | Floor / cap |
|---|---:|---:|---:|---|
| Preface | 612 | 617 | +5 | group budget |
| Ch2 — Preparing Your Environment | 3,250 | 3,343 | +93 | 3,006 / 3,250; waiver 2.86% |
| Ch3 — Your First Working Program: The Echo Pair | 3,023 | 3,020 | -3 | 3,000 / 3,270 |
| Ch4 — The SNode.C Runtime Mental Model | 2,926 | 2,938 | +12 | 2,700 / 3,050 |
| Ch6 — Core Runtime and Event Processing | 3,502 | 3,523 | +21 | 3,500 / 3,850 |
| Ch7 — Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 4,241 | 4,288 | +47 | 4,175 / 4,250; waiver 0.89% |
| Ch8 — Servers, Clients, and Connections | 3,224 | 3,224 | +0 | 3,150 / 3,334 |
| Ch10 — Writing `SocketContext` Classes Well | 3,087 | 3,123 | +36 | 3,040 / 3,140 |
| Ch12 — Building the Same Protocol over Different Lower Layers | 2,598 | 2,628 | +30 | 2,505 / 2,605; waiver 0.88% |
| Ch13 — Configuring Applications and Named Instances | 4,535 | 4,595 | +60 | 4,300 / 4,673 |
| Ch14 — Logging, Diagnostics, and Runtime Introspection | 2,794 | 2,847 | +53 | 2,650 / 2,800; waiver 1.68% |
| Ch15 — TLS Across the Framework | 2,754 | 2,762 | +8 | 2,700 / 2,900 |
| Ch16 — Timeouts, Retries, and Failure Modes | 3,209 | 3,207 | -2 | 3,200 / 3,390 |
| Ch17 — The HTTP Layer | 2,480 | 2,482 | +2 | 2,450 / 2,600 |
| Ch18 — The Express-Like Framework | 2,242 | 2,244 | +2 | 2,050 / 2,315 |
| Ch19 — Server-Sent Events and Real-Time HTTP | 3,305 | 3,307 | +2 | 3,220 / 3,370 |
| Ch20 — WebSocket and Protocol Upgrade | 3,013 | 3,019 | +6 | 2,950 / 3,100 |
| Ch21 — MQTT Support in SNode.C | 3,313 | 3,342 | +29 | 3,000 / 3,405 |
| Ch24 — Database Support and Application State | 3,857 | 3,858 | +1 | 3,826 / 3,926 |
| Ch25 — Reading Complete SNode.C Applications | 2,587 | 2,657 | +70 | 2,450 / 2,600; waiver 2.19% |
| Ch26 — From Applications to Systems: MQTTSuite | 3,897 | 3,952 | +55 | 3,750 / 3,941; waiver 0.28% |
| Ch27 — CMake Components, Public Headers, and Linking Strategy | 3,784 | 3,780 | -4 | 3,700 / 4,000 |
| Ch28 — Deployment on Linux and OpenWrt | 3,602 | 3,636 | +34 | 3,546 / 3,646 |
| Ch29 — Testing, Debugging, and Benchmarking | 4,373 | 4,381 | +8 | 4,300 / 4,500 |
| Ch30 — Building MiniGateway | 4,597 | 4,631 | +34 | 4,400 / 4,618; waiver 0.28% |
| Ch31 — Extending MiniGateway with a New Network Role | 2,835 | 2,860 | +25 | 2,650 / 2,841; waiver 0.67% |
| Ch32 — Architectural Judgment: Choosing the Right Layer and Boundary | 3,165 | 3,180 | +15 | 3,100 / 3,350 |
| The Principles Behind the Programs | 1,383 | 1,383 | +0 | group budget |
| Appendix A — Reading and Extending the Framework | 3,970 | 3,972 | +2 | 3,900 / 3,994 |
| Further Reading | 764 | 792 | +28 | group budget |
| **Full book** | **111,070** | **111,739** | **+669** | **115,000 ceiling** |
| Prose/markup | 103,194 | 103,818 | +624 |  |
| Fenced tokens | 7,876 | 7,921 | +45 |  |

Net growth is 0.602%. Current extent is 4,401 above must 107,338, 599 below wish 112,338, and 3,261 below the ceiling. No floor was waived. Small negative chapter deltas come from formatting and the requested wording/component corrections; no teaching passage was removed.

## Implementation accounting

| Category | Added | Removed | Net |
|---|---:|---:|---:|
| Application C++ | 252 | 178 | +74 |
| Exercise code/drivers | 14 | 7 | +7 |
| CI validation/build support | 174 | 18 | +156 |
| CI regression tests | 49 | 0 | +49 |
| Production CMake/LaTeX | 9 | 3 | +6 |
| Workflow configuration | 10 | 5 | +5 |
| Editorial regression checks/tests | 115 | 2 | +113 |

No framework code changed. Functional companion growth is the explicitly requested B1 closure result (+5 net C++ lines). C2 adds physical lines only to reflow the same source tokens. C3 changes the test observation channel and adds no application state. CI additions are the explicitly requested external-anchor, listing-width and publication-version guards; the shared ABI parser replaces reliance on incompatible binaries rather than adding a second authority. Full per-file additions/deletions are in implementation-numstat.txt.

No OpenWrt device deployment, MQTTSuite service deployment or new Clang 21 build is claimed. The manuscript is frozen again against broad refinement; the unresolved Ch16 test-reader failure and bibliography-cap decision are disclosed for the author.

The local CMake cache also selects the downloaded matching Pandoc executable explicitly. A final invocation of ci/build-book-package.sh with the normal shell PATH passes; local use does not depend on retaining the temporary PATH override.
