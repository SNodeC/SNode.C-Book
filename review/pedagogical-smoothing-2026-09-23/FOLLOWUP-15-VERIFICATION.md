# Follow-up 15 — verify-first ledger

Evidence below was inspected before the corresponding edit. Repository HEADs are in heads-followup-15-start.json; paths under build/followup-15 are fresh default-branch clones. Existence is not execution.

| Item | Finding at entry / HEAD evidence | Decision |
|---|---|---|
| A1 | source-baseline/book-source-baseline.env:5–6; ci/check-source-alignment.py:35–60 require a SHA and reader declarations repeat it; .github/workflows/companion-examples.yml:43 uses that value. Fresh snode.c master is content-identical to the edition manifest. | Reproduced; change checkout authority to master and retain digest/anchor checks. Chapter evidence already references framework_manifest (source-claims.json:3); no chapter SHA requirement exists separately, so retain that correct relation. |
| A2 | preface.md:36 and ch02:19,155,163,173–186 contain the pinned-checkout instructions. | Reproduced; replace with master clone/update and actionable content-drift guidance, retaining separate source/build/install areas. |
| A3 | OpenWRT/net/snode.c/Makefile:4 version 2.0.0; :10 selects OpenWRT; :70–80 hashed spdlog 1.17.0 download; :109–111 disconnected FetchContent; :347 net-un-phy. snode.c/src/net/un/phy/CMakeLists.txt:46–49 defines the valid SHARED target. ch28:255–257 instead describes 1.0.1 and an obsolete component. | Reproduced; correct the live feed description and re-rate every table row. Device/SDK rehearsal remains unexecuted deployment guidance. The feed's tag selection is reported outside this repository, not used as a checkout target. |
| A4 | mqttsuite/mqttbridge/lib/Mqtt.cpp:119–120 forwards to broker.getBridge().publish; mqttstore/lib/Mqtt.cpp:138–149 calls storage.store; MariaDbStorage.cpp:94–108 submits raw exec then calls storeProjections outside either callback; :300 defines the projection operation. | Verified; make the independent submission order explicit and guard external paths/symbols at master/main HEAD. |

## B — confirmed before editing

| Item | Entry evidence and HEAD verification | Decision |
|---|---|---|
| B1 | LineCommandServerContext.cpp:44–46 continues after processLine; :68–69 closes QUIT without terminating that loop. Ch10:184–214 repeats it. SocketContext close delegates to connection shutdown; the command handler must tell the parser to stop. | Reproduced by source control flow. Return a continuation result, clear pending bytes and return chunkLen on closure. Add the coalesced peer-boundary case; preserve every existing assertion. |
| B2 | Ch25:67–119 and Ch27:181–191,338–364 teach generic Express plus transport for an installed WebApp consumer. Framework src/express/legacy/in/CMakeLists.txt:46–62 declares the composed SHARED target and both public dependencies; src/apps/CMakeLists.txt:49 uses the separate in-tree pair. | Reproduced; use the composed installed target, preserve the in-tree example and all dependency detail. |
| B3 | Ch2:73–88 says compiler minimum implies suitability. src/CMakeLists.txt:44–64 accepts GCC12.2/Clang13.0; hosted 36039311975 logs verify GNU13.3.0/Clang18.1.3. The unchanged ConfigActions.cpp:296 and recorded Clang21 diagnostic remain the external compatibility issue. | Reproduced; distinguish the configuration minimum from tested compiler versions and the known failure. |
| B4 | Ch2 optional install command lacks libasio-dev; ch01 comparison CMakeLists requires standalone Asio headers. | Reproduced; add the labelled optional package, retain later guidance. |
| B5 | Ch6:109 calls EventLoop::tick public; EventLoop.h:93 is internal and SNodeC.cpp:72–73 is the facade. EventReceiver.cpp:50–68 queues a receiver and invokes the callback from onEvent. | Reproduced; name the public entry and deferred operation, clarify the status sentence. |
| B6 | Ch29:327 promises verification of architectural assumptions by memory tools. | Reproduced; bound evidence to violations exposed on executed paths. |
| B7 | Ch4:219 omits prefixes; :228 attributes identities to those unseen prefixes. Echo context/transport semantic diagnostics contain inst and conn fields. | Reproduced; state explicitly which identity fields the omitted prefixes carry. |
| B8 | src/express/Router.h:68–69 defines APPLICATION as two maybe_unused const shared_ptr references; Ch25:168 first uses it without explanation and Ch30:789 repeats it. | Reproduced; explain the parameter-list shorthand and link back. |
| B9 | Ch21:45 says “This broker”; Mqtt.h:88–91 names connectionName, clientId, keepAlive and sessionStoreFileName; Mqtt.cpp:103–108 stores/loads those values. | Reproduced; name the SNode.C implementation and explain all four arguments. |
| B10 | Ch15:148 contains the unboxed trust warning. src/core/socket/stream/tls/ssl_utils.cpp selects verification from trust configuration; no trust source leaves mode zero. | Verified; retain the entire paragraph inside a warning box. |
| B11 | Ch31:231–242 gives a /tmp path and override, but not ownership guidance. Ch7's final pathname section teaches directory permissions, owned cleanup and collisions. | Reproduced; label the teaching default and link back. |

B1 adds a short-lived return result, not persistent state: command dispatch owns the closure decision and the receive loop owns buffer consumption. The explicit author fix authorizes the small production-code growth; final accounting distinguishes it from formatting and tests. No SSE re-entrancy change is made: that finding was refuted and dropped.

B verification: the rebuilt companion passes all six selected Ch10, Ch12 and Appendix A CTests with GCC13.3.0 and Clang18.1.3, including the added coalesced QUIT case. The installed framework contents equal fresh master HEAD under the manifest; the full workflow rebuild/runs follow C. The precise TLS source is ssl_utils.cpp:204–209.

## C — confirmed before editing

| Item | Entry/HEAD evidence | Decision |
|---|---|---|
| C1 | book-package.yml:30–42 installs Pandoc3.10.1/crossref0.3.24a. Local binaries report the same mismatch: crossref built with Pandoc3.9.0.2. | Reproduced; keep crossref and select Pandoc3.9.0.2; one parsed-version guard serves CMake/local and CI paths. |
| C2 | Wide-line scan still finds 53 code lines over100 columns; metadata.yaml:214–217 permits mid-identifier wrapping. PDF page271 has 453.543pt code content and 465.498pt outside frame; narrower boxed content is435.022pt. Embedded LMMono fonts have525-unit cells at8.9664pt, about4.707pt/cell. | Reproduced; choose90 columns (423.66pt), leaving room in both full-width and boxed listings. Reformat affected sources/listings without changing behavior. Narrow217.699pt rectangles belong to figure/side-by-side content, not these full listings. |
| C3 | family-server.cpp:15 writes IDENTITY through std::cout; lab_support.running merges stdout/stderr into the logger file. families.py:49–54 parses that shared stream. Hosted36002150169 records an actual corrupted record. | Reproduced; use a dedicated identity file supplied by the Ch7 harness, leaving logging and every assertion intact. |
| C4 | ch13:211/213 and appendix-a:165/167 duplicate adjacent directives; singular/plural instance keys and Unix-domain spelling split headings. | Reproduced; remove only the duplicate index commands, consolidate headings, preserve teaching prose. |
| C5 | ch14:326 checkpoint is bold inline text; ch21:21 figure lacks neighbours'90%/tbp attributes; MiniGateway README and Ch30 copy use snodec_DIR. | Reproduced; heading, matching attributes and CMAKE_PREFIX_PATH convention; README retained. |
| C6 | Four book entries at further-reading:12,13,20,21 lack edition/publisher/year. | Reproduced; publisher catalogues verify Stroustrup4th/Addison-Wesley2013, Meyers1st/O’Reilly2014, Stevens/Fenner/Rudoff3rd/Addison-Wesley2003, Kerrisk1st/NoStarch2010. Primary links accompany the entries. Standards and protocol specifications are not book entries. |
