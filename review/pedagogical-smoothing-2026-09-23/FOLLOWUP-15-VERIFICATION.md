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

## D — passages verified before each local edit

All requested passages reproduced. The lines below are pre-edit locations in the evolving pass. D2 retains the contracts checked in src/log/Logger.h/.cpp and detail/SpdlogBackend.cpp (scope ownership, bootstrap, filtering and async copying). D3 follows the existing address classes, Config hierarchy and identical EchoPair source; no new runtime behavior is asserted. D4 retains the paragraph position and the per-activation ownership contract. D5 preserves each sentence when merging paragraphs.

| Item | Pre-edit file:line | Passage |
|---|---|---|
| D1 | manuscript/chapters/10-writing-socketcontext-classes-well.md:370 | The stream context now exposes `trySendToPeer(...)` in addition to the existing void send surface. |
| D1 | manuscript/chapters/13-configuring-applications-and-named-instances.md:558 | The root configuration now exposes |
| D1 | manuscript/chapters/16-timeouts-retries-and-failure-modes.md:263 | SNode.C now exposes that policy in the instance's existing `connection` section: |
| D1 | manuscript/chapters/17-the-http-layer.md:269 | HTTP parsing now receives |
| D1 | manuscript/chapters/27-cmake-components-and-linking-strategy.md:301 | The top-level build now distinguishes |
| D1 | manuscript/chapters/29-testing-debugging-and-benchmarking.md:125 | The core unit tests now include |
| D1 | manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:308 | The semantic logger now carries |
| D1 | manuscript/chapters/appendix-a-reading-and-extending-the-framework.md:342 | The current `InetPerCallFlowTest` is the relevant composed regression boundary; an old singleton-controller sketch would be the wrong foundation for this extension. |
| D1 | manuscript/chapters/25-reading-complete-snodec-applications.md:271 | The current public logging entry point is `<Log.h>`; the source excerpts in this chapter use that surface rather than a removed macro interface. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:132 | Their return type is lower-level, not `snode::log::Logger`: do not mix level enums or error-method names. Use the facade for its `event(...)`, `systemError(...)` or `Level`; use the inherited helper for ordinary context-scoped severity calls. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:225 | Their values use `name=level` pairs; lists can contain comma-separated pairs. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:227 | Use the narrowest scope; global trace can obscure relevant records and change timing. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:229 | Do not overlay an unrelated `configure(Settings)` and expect merging: it initializes and freezes its own policy, not a live per-record adjustment. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:231 | Successful startup emits those pending records and starts one logging worker; a failed bootstrap discards them. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:231 | Wait for the record or for orderly process completion when checking a log; do not infer delivery from an unrelated callback finishing. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:233 | Parsed `log-level` or `log-format` changes need not affect emitted records; use a controlled restart to change deployment logging. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:233 | Framework-owned scopes manage their own lifecycle and generation-aware caches; application code should not manage those generations. |
| D2 | manuscript/chapters/14-logging-diagnostics-and-runtime-introspection.md:293 | The renderer belongs to the logging library; the utility library retains its dependency on that library. Applications need not assemble a second colored dump. Enabled large dumps copy the bytes before returning and need a confidentiality decision. After asynchronous logging starts, the logging worker formats and writes them; copying and queue submission still cost time on the caller. |
| D3 | manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:54 | The concrete address families are: |
| D3 | manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:448 | The Unix-domain address class is: |
| D3 | manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:464 | Default construction is meaningful in the Unix-domain address model. |
| D3 | manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:524 | This keeps the local/remote distinction visible. The remote path is the service endpoint the client wants to reach. |
| D3 | manuscript/chapters/13-configuring-applications-and-named-instances.md:393 | This traverses the `echoserver` instance’s `local` section to set its `port`. Help follows the same path: |
| D3 | manuscript/chapters/13-configuring-applications-and-named-instances.md:446 | In a configuration file, the same hierarchy becomes a dotted key: |
| D3 | manuscript/chapters/13-configuring-applications-and-named-instances.md:481 | The required-value walk above explains why these calls can omit addresses: |
| D3 | manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:111 | The endpoint identity changes with the network family. |
| D3 | manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:144 | EchoSocketContext::EchoSocketContext(SocketConnection* socketConnection, Role role) |
| D3 | manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:162 | const std::size_t chunklen = readFromPeer(chunk, 4096); |
| D3 | manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:53 | Packaging is an operational decision. Neither one binary nor many services is automatically better; compare the required lifetimes, permissions and failure domains. |
| D3 | manuscript/chapters/26-from-applications-to-systems-mqttsuite.md:106 | Configuration, diagnostics and failure behavior expose how the roles operate together. |
| D4 | manuscript/chapters/32-architectural-judgment-choosing-the-right-layer-and-boundary.md:237 | The current flow API provides another concrete boundary test. |
| D4 | manuscript/chapters/epilogue.md:67 | The final design chapters then named |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:86 | Calling `listen(...)` should be understood as registering listening intent. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:88 | Retry logic, status reporting, accept-event observation, and context creation all belong to the managed runtime story. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:88 | When the server-side instance succeeds in listening, peers can be accepted. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:88 | Each accepted peer becomes a concrete `SocketConnection`. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:95 | Calling `connect(...)` registers connection intent. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:243 | The address identifies the relevant endpoint. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:250 | `core::socket::State` is richer than a Boolean. |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:250 | Its principal values include: |
| D5 | manuscript/chapters/08-servers-clients-and-connections.md:250 | `OK`, `DISABLED`, `ERROR`, `FATAL`, `NO_RETRY`. |
| D5 | manuscript/chapters/10-writing-socketcontext-classes-well.md:114 | The base context interface also requires explicit handling for signals and read/write errors. |
| D5 | manuscript/chapters/24-database-support-and-application-state.md:412 | The MariaDB API exposes state and errors. The application must decide the policy. |
| D5 | manuscript/chapters/24-database-support-and-application-state.md:414 | When incoming protocol activity is faster than database completion, pending command sequences accumulate. Event integration keeps other callbacks runnable; it does not bound that queue for the application. |
| D5 | manuscript/chapters/02-preparing-your-environment.md:69 | SNode.C is a modern C++ framework. |
| D5 | manuscript/chapters/02-preparing-your-environment.md:109 | `libbluetooth-dev` is relevant for Bluetooth RFCOMM and Bluetooth L2CAP. `libmagic-dev` is relevant where file-type or content-type detection is used. |
| D5 | manuscript/chapters/epilogue.md:7 | The word layered can be used lazily. In SNode.C, it is meant operationally. |
| D5 | manuscript/chapters/epilogue.md:34 | When the vocabulary is clear, a system can be discussed by developers, operators, teachers, and students using the same names. |
| D5 | manuscript/chapters/epilogue.md:43 | The recurring lesson is that bytes become useful only when a layer gives them meaning. |
| D5 | manuscript/chapters/epilogue.md:50 | A network framework does not end at the source tree. |
| D5 | manuscript/chapters/epilogue.md:52 | For that reason, this book treated CMake, packaging, deployment, testing, and debugging as architectural surfaces rather than as afterthoughts. |
| D5 | manuscript/chapters/epilogue.md:81 | A reader who finishes this book should know how SNode.C public headers, servers, clients, contexts, HTTP, WebSocket, MQTT, configuration, and CMake components fit together. |
| D5 | manuscript/chapters/13-configuring-applications-and-named-instances.md:30 | `echoserver.local.port` starts at the C++ default 8080, takes 18091 from the selected file, and becomes 18092 when the command line overrides that file. |
| D5 | manuscript/chapters/13-configuring-applications-and-named-instances.md:113 | The key `echoserver.local.port` addresses the named instance created by the entry point; its 18091 file value belongs to that listener. |
| D5 | manuscript/chapters/13-configuring-applications-and-named-instances.md:207 | For our running value, `echoserver.local.port = 18092` belongs to the named listener’s local endpoint. |
| D5 | manuscript/chapters/13-configuring-applications-and-named-instances.md:272 | For `echoserver`, 18092 belongs in `local.port`: it selects where this server listens. |
| D5 | manuscript/chapters/13-configuring-applications-and-named-instances.md:530 | Help located `echoserver.local.port`; structured discovery lets a tool locate that same option and inspect its metadata. |
| D5 | manuscript/chapters/30-building-minigateway.md:352 | The declarations give every JSON-facing participant one representation contract. They do not accept state or assign its order; the implementation below must first turn valid fields into a value before an input can ask the model to accept it. |
| D5 | manuscript/chapters/30-building-minigateway.md:576 | These declarations expose the MQTT settings that deployment may vary while leaving the model contract fixed. The implementation below registers defaults and getters that the protocol and startup code can consume when they configure and initiate the broker connection. |
| D5 | manuscript/chapters/30-building-minigateway.md:722 | Successful activation and failures receive comparable diagnostics through these state cases. Reporting leaves failed-endpoint repair and measurement validation to their owners. We can now read the web implementation, whose routes retain the application-level decisions behind those reports. |
| D5 | manuscript/chapters/30-building-minigateway.md:1074 | Incoming MQTT data passes through the codec before acceptance, while outgoing data represents the model’s accepted measurement. Session handling remains here rather than in the model; the factory below supplies a fresh protocol object when a connection needs one. |
| D5 | manuscript/chapters/30-building-minigateway.md:1167 | The factory now joins one connection, its MQTT context and the application protocol object with the existing model reference. That reference still needs a valid lifetime; the next startup wrapper selects and activates the client without becoming another model owner. |
| D5 | manuscript/chapters/30-building-minigateway.md:1263 | Startup now supplies endpoint defaults, MQTT options and state reporting before registering connection work. Registration is not broker acceptance; `main()` follows by constructing the model once and keeping it available while the runtime advances both communication paths. |
