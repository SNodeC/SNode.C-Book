# Publisher's review: *Layered Network Programming with SNode.C*

**Author:** Volker Christian  
**Subtitle:** *Building Multi-Protocol Applications in Modern C++*  
**Review date:** 21 September 2026  
**Manuscript reviewed:** book commit `a90fe28`, with the declared SNode.C 2.0.0 source snapshot `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`  
**Recommendation:** Revise and resubmit after substantial developmental and technical revision. A conditional specialist acquisition is defensible; release to production is premature.

**Review authority:** The Markdown files under `manuscript/`, ordered by `manuscript/book-files.txt`, are the current book. This revised report excludes observations drawn from the previously inspected PDF and generated archive. The author has since confirmed that the PDF in `dist` is up to date; it has not been reread for this revision.

This is the review before refinement. The subsequent changes and current-source verification are recorded in `verification/manuscript-refinement-2026-09-21.md`. Earlier recommendations to reduce length are not the governing instruction for that work: the author explicitly requested preservation of depth with no shortening target.

## 1. Editorial judgment

This manuscript has a publishable central idea, an author with direct command of the subject, and a useful integration project. Its strongest contribution is the explanation of how a network application can preserve clear ownership and responsibility while combining communication families, protocol layers, configuration, diagnostics, and deployment. It gives the reader a vocabulary for discussing a real system, and it repeatedly connects that vocabulary to public types, source files, build components, and runtime roles.

The book is considerably stronger as an explanation of SNode.C's architecture than as a progressive practical course in building applications with it. It often explains why a boundary matters several times before demonstrating what a reader should do at that boundary. Some chapters with practical titles are predominantly conceptual inventories. Conversely, the more concrete passages sometimes leave essential setup, failure handling, or interoperability assumptions unstated. The book needs redistribution of attention as much as it needs correction.

I would encourage an acquiring editor to continue the conversation. I would not describe this as a manuscript ready for copyediting and typesetting alone. The required changes include teaching structure, executable demonstrations, protocol accuracy, and reader access to the companion sources.

| Assessment area | Judgment |
|---|---|
| Core concept | Strong and coherent |
| Authorial subject knowledge | Strong, especially framework ownership, configuration, logging, and component boundaries |
| Distinctiveness | Credible as a first-party framework guide and applied architecture case study |
| Practical teaching progression | Uneven; substantial revision needed |
| Technical reliability | Good foundation, with specific corrections and validation gaps to resolve |
| Prose economy | Repetition materially reduces pace |
| Reference usefulness | Promising, but needs more precise links, consolidated lookup material, and versioned supporting sources |
| Editorial readiness for production | Substantive manuscript revision needed before final copyediting; rendered output is outside this review |
| Broad trade acquisition case | Not established by the supplied evidence |
| Specialist or advanced-course potential | Credible, subject to revision and independent reader testing |

The most useful governing editorial principle is: **introduce each important concept once, demonstrate it promptly, and revisit it through a new problem rather than another definition.** That preserves the author's architectural purpose while improving the reader's experience.

## 2. Scope and basis of review

I read the complete current manuscript in the order specified by `manuscript/book-files.txt`: all front matter, part introductions, Chapters 1–38, the epilogue, further reading, and index source. I also examined the proposal and evidence sheet, current verification notes, publication configuration, selected companion implementations, and relevant implementation paths in the locally available framework checkout. That checkout's HEAD matches the manuscript's declared base commit; its current file contents also include uncommitted changes. The subsequent refinement records those contents explicitly rather than treating the base commit as the whole source identity.

The source contains **140,268 whitespace-delimited words**, including code, Markdown, and indexing commands. This is a reproducible size indicator, not a publisher's edited prose count. Chapters 1–12 alone account for approximately 40,000 such words before the line-protocol chapter begins. The working tree was clean at the start of this review.

The review's chapter assessments and technical findings are based on the current Markdown manuscript, supporting sources, and selected implementation checks. PDF pagination, running heads, rendered index quality, visual layout, accessibility tagging, and generated-artifact currency are outside this revised report. The diagram discussion concerns explanatory content and source semantics.

The following checks were actually performed:

| Check | Observed result | What it does not establish |
|---|---|---|
| Current source-alignment checker, including local framework checkout | Passed: 38 chapters and 35 exact marked complete listings; framework pin matched | Compilation of every excerpt, protocol correctness, or runtime correctness |
| Source-hygiene checker | Passed | Editorial completeness or standards conformance |
| Focused C++ checks using the receive-loop bodies extracted from the companion implementations | Reproduced segmentation-dependent line rejection and oversized-record recovery problems | A full socket-level integration test |
| Focused C++ check linked with the actual `MeasurementModel.cpp` | Confirmed that captured subscriber objects remain retained until another publication invokes and removes their callbacks | A measured process-memory leak or full HTTP connection-lifetime audit |
| Selected framework source inspection | Confirmed MQTT loop-prevention encoding, successful-CONNACK callback gating, and relevant TLS configuration behavior | Full framework conformance or security certification |
| Primary-source standards checks | Consulted HTTP/SSE, MQTT, Mosquitto, OpenSSL, BlueZ, and MariaDB documentation where needed | Exhaustive protocol review |

I did **not** rebuild the complete framework, run its full CTest matrix, independently reproduce the GCC/Clang companion matrix, launch a live MQTT broker or MariaDB service, test Bluetooth hardware, deploy to OpenWrt, or conduct load and endurance testing. The report distinguishes these outstanding checks from the results above. No manuscript, companion, framework, or publication source was changed during the review.

## 3. What the publisher should preserve

### A. A coherent architectural argument

The manuscript consistently distinguishes an application-side handle, a registered runtime instance, a connection, a context, and a context factory. That is valuable teaching. Readers of asynchronous frameworks often suffer precisely because these lifetimes and responsibilities are blurred. The discussion gives names to the distinctions and explains why they affect configuration, callbacks, diagnostics, and extension.

The emphasis on one application-owned model is also useful. MiniGateway's measurement acceptance boundary assigns the gateway's sequence once, and the protocol-facing roles observe the accepted state. Chapter 36 then makes the benefit visible by adding a Unix-domain input role without changing the existing web or MQTT role. This is the book's most convincing demonstration of its thesis.

### B. The connection between source architecture and operational reality

The author treats public headers, installed components, runtime configuration, logging, packaging, and deployment as things an application developer must understand. That is a strength. The distinction between an in-tree example and an external consumer is particularly important for a framework guide, and the manuscript returns to it with useful specificity.

The explanation that a successful queue admission is not proof of peer delivery is another strong point. Likewise, retry after a failed connection attempt and reconnect after an established connection ends are separated clearly. These are the kinds of distinctions that prevent misleading operational behavior.

### C. The revised logging and testing material

Chapter 18 is among the strongest chapters. It describes semantic scope, ownership of diagnostic identity, threshold selection, typed errors, output format, and diagnostic cost. It is substantially more useful than a catalogue of logging calls.

Chapter 34 also benefits from precision. It separates unit, component, source-policy, installed-consumer, external-application, and publication evidence. It correctly warns that a skipped test is not a passed behavioral check and that a workflow definition is not evidence of a successful run. These qualifications should survive editing.

### D. Honest first-party positioning

The author/framework relationship is disclosed. The proposal separates author-supplied background, project evidence, and unproven adoption claims. It does not manufacture market statistics or use the author's related projects as evidence of independent uptake. This restraint improves the submission's credibility.

### E. A substantial companion and production foundation

Complete companion source trees, immutable framework pinning, checks for marked listing equality, a figure system, an index, and publication workflows are real assets. Many technical manuscripts reach acquisition without this support. The remaining task is to make the published reader experience as reliable as these mechanisms intend it to be.

## 4. Developmental revision required

### 4.1 Choose a primary reader more firmly

The primary reader should be an experienced C++ developer or an advanced student working with Linux/POSIX systems. The manuscript assumes comfort with templates, callbacks, ownership, CMake, protocols, and system operation. Makers and scientists may be good secondary users, but their inclusion should not imply that the book provides the prerequisite instruction they may need.

The front matter names several audiences, but the actual reading routes remain broad ranges of chapters. The makers' route even omits the environment chapter. Replace these with two or three concrete paths, each with prerequisites and an observable outcome: for example, an external application path, a multi-protocol gateway path, and a framework-internals path. Every practical route should include the necessary setup and companion retrieval instructions.

The phrase “modern C++” is defensible because of the language baseline and source style. It should not lead readers to expect a comparative treatment of coroutines, executors, or contemporary asynchronous library designs. A short explanation of why this framework uses its particular callback, inheritance, and factory model would prevent that mismatch.

### 4.2 Reduce repeated conceptual explanation

The repetition is structural, not merely a matter of repeated words. Chapters 4–9 repeatedly explain how names encode layers and how handles, instances, connections, contexts, and factories differ. Chapters 8–12 revisit the stable upper model as each family changes. Chapters 13–15 repeat construction versus behavior. Chapters 16–17 overlap in configuration philosophy. Chapters 27, 30, 37, 38, and the epilogue repeatedly restate responsibility, role, lifetime, and boundary selection.

Repetition can support teaching, but it needs to produce a new result. Here it too often takes the form of a second table, a short arrow diagram, a rule box, a takeaway list, and a closing paragraph explaining essentially the same proposition. All 38 chapters have a “What to remember” section. Those summaries are useful; the repeated lead-ins and conclusions around them are less consistently justified.

I recommend an initial compression target of **15–25%**, applied selectively to repeated exposition, component inventories, and repeated transitions. This is an editorial planning estimate, not a measured quantity of removable text. Some recovered space should be reinvested in the missing exercises. Do not shorten the difficult ownership and operational explanations simply to meet a numerical target.

A practical editing method is to assign one authoritative home to each core concept. Later chapters should point back briefly and then show a changed consequence. For example, the Unix-domain chapter can assume the context/factory model and devote its space to permissions, path lifecycle, peer identity, and a runnable local exchange.

### 4.3 Bring application work forward

The early echo pair is a good opening practical achievement. The long interval before the next substantial application behavior weakens that momentum. A reader can spend tens of thousands of source words recognizing architecture before being asked to make an interesting application decision.

Introduce a small measurement application earlier, without moving the entire capstone into the opening. Let readers add one behavior at a time: parse an input, expose a snapshot, stream an update, send it through MQTT, and observe a failure. Chapters 35–36 can then assemble and extend something the reader already understands.

For each major practical chapter, require a compact teaching contract:

1. The problem and prerequisite state.
2. The files or changes involved.
3. The exact build and run commands.
4. The expected observable result.
5. One deliberately introduced failure and its diagnosis.
6. One exercise that transfers the idea.

This need not make the book a recipe collection. It gives its architectural argument evidence.

### 4.4 Match chapter titles to delivered depth

Several titles promise more practical instruction than the text currently supplies:

- **Chapter 15, “Building the Same Protocol over Different Lower Layers”:** much of the chapter classifies what should remain stable. It needs one protocol actually built and exercised over at least two carriers.
- **Chapter 19, “TLS Across the Framework”:** the placement of TLS is explained well, but a reader is not taken through a complete authenticated connection and controlled verification failures.
- **Chapter 22, “The Express-Like Framework”:** classes and responsibilities receive more attention than a complete route/middleware flow with continuation, short-circuiting, response ownership, and error handling.
- **Chapter 26, “MQTT over WebSocket”:** the composition is explained, but a reproducible negotiation and message exchange are missing.
- **Chapter 33, “Deployment on Linux and OpenWrt”:** this is largely a deployment architecture discussion. It does not supply a complete service/package walkthrough on either target.
- **Chapter 34, “Testing, Debugging, and Benchmarking”:** the taxonomy is strong, but a worked regression and a small recorded benchmark would make the final two promises concrete.
- **Chapter 38, “Extending the Framework Safely”:** the principal worked extension is explicitly application-local. Either narrow the title or demonstrate a small reusable framework/public-component extension through installation and a consumer test.

The publisher should choose between adding the missing demonstrations and narrowing the promises. The present halfway position risks reader dissatisfaction.

### 4.5 Make architectural judgment genuinely contestable

The manuscript often contrasts an obviously poor placement with an obviously appropriate one. That teaches vocabulary but does less to teach judgment under uncertainty. Chapter 37's worked decisions are a useful advance, especially the distinction between producer numbering and gateway acceptance order.

Develop two or three decisions in which both alternatives are reasonable: synchronous model notification versus queued delivery; one process versus separately supervised roles; a connection-local object versus a shared application service; a minimal callback implementation versus a more explicit lifetime mechanism. Explain what is gained and what becomes harder.

The capstone itself provides material. Its static MQTT client registry is convenient, but it is process-wide hidden state in a book that repeatedly recommends explicit dependencies. This is not automatically a fatal design error. It is a tradeoff that deserves a sharper account: lifetime assumptions, one-model expectations, test isolation, and how another gateway instance in the same process would change the decision.

### 4.6 Complete the operational teaching

The book says callbacks should not block, but does not give the reader a sufficiently explicit contract for thread confinement, calling framework APIs from another thread, or handing off expensive work and returning a result safely. Even if the intended rule is simply to keep application access on the event-loop thread, state it clearly and explain the supported integration boundary.

The capstone also needs a compact operational contract: what happens to measurements while MQTT is disconnected; whether anything is replayed; what sequence numbers mean after process restart; how slow SSE observers are bounded; when disconnected observers are removed; and whether startup succeeds in degraded mode. A teaching application may intentionally omit durability and authentication. It should still state its behavior precisely.

## 5. Technical findings requiring correction or explicit qualification

The items below are separated by evidence and consequence. They are not claims that the entire framework is defective.

### T1. Line-length handling depends on read segmentation

**Priority: technical correction before publication. Reproduced in focused C++ checks.**

The receive loops process complete lines before checking the residual buffer length. The `maxLineLength` name and safety discussion can therefore be read as a line-size guarantee that the code does not provide. The actual check limits an unfinished remainder after complete records have already been dispatched. See [Chapter 13's receive loop](/home/voc/projects/snodec/publications/book/manuscript/chapters/13-writing-socketcontext-classes-well.md:278) and the [runnable server implementation](/home/voc/projects/snodec/publications/book/companion/examples/LineProtocol-Server/LineCommandServerContext.cpp:30).

With 4,096 bytes already buffered, another 100 bytes followed by a newline produces a 4,196-byte line that is passed to `processLine`. Deliver the same final 100 bytes separately from the newline and the server closes before processing the line. The accepted/rejected outcome thus changes with chunk boundaries for the same wire record.

MiniGateway Extended repeats the ordering. It also clears an oversized unfinished buffer without closing or remembering that the rest of that record must be discarded. After 8,192 non-newline bytes have been cleared, a following `21.5,43.0,3.72\n` is treated as a fresh valid measurement, even when it is the suffix of the same oversized record. See [the extension's receive loop](/home/voc/projects/snodec/publications/book/companion/examples/MiniGateway-Extended/MeasurementUnixSocketContext.cpp:110).

The governing invariant is that record validation and recovery must follow protocol boundaries rather than arbitrary read boundaries. The exact maximum should specify whether delimiters and an optional carriage return count.

**Required result:** choose and document a coherent size/recovery policy, enforce it before dispatch, and test the same records with different fragmentations, including an oversized prefix followed by a plausible valid suffix. Reuse of the teaching pattern should not propagate the defect into another example.

### T2. MiniGateway's MQTT loop prevention is a broker-specific interoperability choice

**Priority: substantial technical qualification and integration test. Confirmed in the pinned source; no live broker matrix run.**

[MiniGateway passes `true` as the final `sendConnect` argument](/home/voc/projects/snodec/publications/book/companion/examples/MiniGateway/MiniGatewayMqtt.cpp:38). Chapter 35 describes this simply as enabling loop prevention. In the pinned framework's `Connect.cpp`, that flag ORs `0x80` into the MQTT 3.1.1 protocol-level byte, producing `0x84` rather than the standard `0x04`; the source comment identifies the Mosquitto `try_private` convention.

MQTT 3.1.1 specifies protocol level `0x04`. Mosquitto documents that its private bridge indication is not supported by all brokers and may need to be disabled for connectivity. This is therefore not a portable ordinary-client option or a general guarantee that loops cannot occur. [MQTT 3.1.1, §3.1.2.2](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html), [Mosquitto bridge configuration](https://mosquitto.org/man/mosquitto-conf-5.html).

The default input and output topics are already different, so explain why the extension is needed for this example. If retained, name the supported broker behavior and test it. If broad broker compatibility is intended, make the ordinary protocol path the teaching baseline and explain loop control at the appropriate topology/application boundary.

**Required result:** an explicit MQTT version statement, a documented extension policy, and a recorded broker exchange for the current edition. Also distinguish session establishment from successful subscription and acknowledged delivery.

### T3. SSE `Accept` handling is presented too broadly

**Priority: correct the protocol explanation and example policy. Confirmed from the code and standards.**

[Chapter 23](/home/voc/projects/snodec/publications/book/manuscript/chapters/23-server-sent-events-and-real-time-http.md:169) says the route must first verify that the request asks for an event stream and implements this using a case-insensitive substring check. [MiniGateway uses the same policy](/home/voc/projects/snodec/publications/book/companion/examples/MiniGateway/MiniGatewayWeb.cpp:30).

That helper rejects absent or wildcard `Accept` values, while accepting `text/event-stream;q=0`. It is not a correct general implementation of HTTP media-type negotiation. The SSE specification permits the user agent to send the explicit header; it does not make that header a universal prerequisite for serving an event stream. HTTP permits media ranges and uses quality zero to express unacceptability. [WHATWG EventSource processing](https://html.spec.whatwg.org/multipage/server-sent-events.html), [RFC 9110, §12](https://www.rfc-editor.org/rfc/rfc9110.html#section-12).

An application can deliberately adopt a restrictive request contract. If that is the intent, label it as application policy and explain its interoperability cost. Do not teach a substring match as standards-level validation.

There is also a framework dependency: the pinned HTTP server's `responseStarted` implementation uses the same Accept substring to classify an SSE connection and disable its read timeout. Changing only the example helper could therefore leave streaming lifecycle behavior inconsistent. The revision must either document this snapshot-specific restriction accurately or coordinate the change at the framework policy boundary.

**Required result:** align the prose, helper, framework assumptions, and tests around an explicit policy. Test absent, wildcard, explicit allowed, explicit excluded, and unrelated media types. Preserve the useful framework-specific explanation of `sendFragment` and the separate blank event boundary.

### T4. Disconnected SSE subscriptions can accumulate while the model is idle

**Priority: resolve or bound the lifetime behavior in the capstone. Confirmed retention mechanism; no whole-process memory measurement.**

The web role [captures the response in a model subscription](/home/voc/projects/snodec/publications/book/companion/examples/MiniGateway/MiniGatewayWeb.cpp:63). The model [removes a listener only when a later publication invokes it and receives `false`](/home/voc/projects/snodec/publications/book/companion/examples/MiniGateway/MeasurementModel.cpp:20). No publication means no removal.

A focused test linked against the actual model retained all 1,000 callback-captured objects until a subsequent `accept()` invoked the callbacks; they were released afterward. That establishes the retention rule. Combined with the response capture, it means repeated event-stream subscriptions followed by disconnects can leave subscription entries and response references retained while measurements are idle. It does not establish that the entire underlying connection remains alive, nor does it quantify process memory.

This is a particularly relevant example in a book that emphasizes ownership and lifetime. The existing cleanup strategy may be adequate for a narrowly bounded demonstration, but its dependence on future domain activity should be explicit.

**Required result:** make observer lifetime cleanup or a clear bound part of the design, and verify repeated connect/disconnect behavior with no intervening measurement. Also show how the existing framework output policy bounds slow observers; the capstone should apply the backpressure lessons taught earlier.

### T5. TLS teaching needs an authenticated connection recipe

**Priority: substantial pedagogical and technical revision. Source-inspected concern, not an executed attack test.**

Chapter 19 discusses trust material and SNI but does not take the reader through a complete client/server setup that demonstrates identity verification. Its general caveat that TLS-capable linking does not finish a secure deployment is correct, but insufficiently operational.

The pinned TLS implementation makes verification dependent on configuration. In `ssl_utils.cpp`, no configured trust source and no default-CA-directory selection leads to verification mode zero. The configuration's default-CA-directory flag is false. The inspected SNI helper sets the offered server name; that operation alone does not establish a hostname verification policy. User hooks may add such policy, so this is not a claim that every possible application fails to verify peers.

OpenSSL documents expected-peer-name verification separately from SNI. The book needs to teach that distinction explicitly rather than leave it to inference. [OpenSSL hostname verification documentation](https://docs.openssl.org/3.6/man3/SSL_set1_host/).

**Required result:** one complete authenticated local TLS exercise with deliberate trust configuration, expected peer identity, and tests for a wrong name and an untrusted certificate. Identify what the framework configures automatically and what application code must configure. Include the exact snapshot behavior rather than an abstract list of security concerns.

### T6. Two setup examples leave misleading state assumptions

**Priority: straightforward corrections before reader testing. Confirmed by command/source inspection.**

In [Chapter 2](/home/voc/projects/snodec/publications/book/manuscript/chapters/02-preparing-your-environment.md:208), a local installation configures `CMAKE_INSTALL_PREFIX` to the user's local directory. The subsequent “system-wide installation” command uses `sudo cmake --install` on the same build directory without changing that prefix. Privilege does not change the cached destination. Present two independent paths or explicitly reconfigure the installation destination. Likewise, the optional Ninja sequence should use a fresh build directory if the earlier sequence selected another generator.

In [Chapter 28's SQL setup](/home/voc/projects/snodec/publications/book/manuscript/chapters/28-database-support-and-application-state.md:240), `CREATE DATABASE snodec;` is followed by an unqualified `CREATE TABLE measurements`. Creating a database does not select it for subsequent statements. A clean session needs `USE snodec;` or a qualified table name. [MariaDB `USE` documentation](https://mariadb.com/docs/server/reference/sql-statements/administrative-sql-statements/use-database).

**Required result:** run the printed setup sequences from the stated initial conditions. Do not rely on the author's pre-existing shell, build cache, or database session.

### T7. GET is used for an intentional state-changing operation

**Priority: correct or prominently constrain the teaching example.**

MiniGateway's `/simulate` route accepts a new measurement and advances the sequence through an HTTP GET. This is an explicit requested state change, not an incidental logging side effect. It is a poor method-selection example for readers building web interfaces. HTTP defines safe methods around essentially read-only requested semantics. [RFC 9110, §9.2.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1).

The lesson is easy to preserve with a command-oriented method and corresponding invocation. If the GET route is retained solely for a local demonstration, its limitation should be explicit at the point of use. Describing it as “controlled input” does not by itself explain the HTTP semantics.

### T8. Bluetooth pairing is stated as an unconditional prerequisite

**Priority: qualify the claim and establish a tested platform recipe.**

Chapter 12 twice says devices must already be paired before SNode.C can communicate over RFCOMM or L2CAP. The intended practical advice is sensible for many setups, but it is too absolute as a transport statement. Bluetooth behavior depends on security level, service policy, platform, and potentially pairing initiated during connection setup. BlueZ documents distinct RFCOMM security levels, rather than one universal prior-pairing contract. [BlueZ RFCOMM documentation](https://github.com/bluez/bluez/wiki/RFCOMM%287%29).

**Required result:** state the tested adapter/OS/security configuration and the setup needed for that recipe. Distinguish pairing, bonding/trust, discoverability, authorization, and service availability. I did not test hardware, so this remains a correction to the breadth of the claim rather than a reproduced device failure.

### T9. Supporting references and diagrams need precision

**Priority: editorial/technical cleanup.**

The Chapter 32 component tree is introduced as a view from lower components toward their dependents. Some branches then place a dependency beneath its consumer, such as an HTTP dependency under a WebSocket server and a selected carrier under an Express composition. The explanation that the true structure is a graph does not remove the directional ambiguity. Use one edge meaning, separate containment from dependency, and move the exhaustive matrix to reference material if necessary.

Chapter 35 says the exact timestamp in the shown output depends on the run, but its JSON codec does not emit a timestamp and the displayed output contains none. Decide whether time is part of the public measurement representation, then align the prose and example. This is a small error, but a useful indicator that the final text still needs a consistency pass.

Chapter 31 describes implementation details of MQTTSuite without a comparably explicit immutable MQTTSuite baseline in the reader-facing chapter. The framework pin does not by itself pin that separate ecosystem. Add a versioned reference for source-derived claims.

The proposal's SSE contract paragraph contains broken inline-code formatting around newline escapes. This should be corrected before submission; it is visible in the source and is not a subtle protocol issue.

### T10. The WebSocket echo example does not preserve message type

**Priority: clarify the example contract or correct its behavior. Confirmed by source inspection.**

The companion server's `onMessageStart(int)` ignores the incoming opcode, and `onMessageEnd()` passes the accumulated `std::string` to `sendMessage`. In the pinned framework that overload sends a text message; the pointer/length overload sends binary. Consequently, an incoming binary message is not echoed with its original type. See [the echo implementation](/home/voc/projects/snodec/publications/book/companion/examples/WebSocket-Echo-ServerSubprotocol/EchoServer.cpp:13).

If this is a text-only teaching subprotocol, say so and handle unsupported input deliberately. If it is a general echo, preserve the message type. Include a binary case in the reader-visible verification. This is a useful opportunity to demonstrate the difference between message meaning and byte accumulation.

### A suspected defect that was not sustained

The small MQTT role in Chapter 25 does not inspect the CONNACK return code before subscribing and publishing. On inspecting the pinned framework, I found that `_onConnack` invokes the application callback only on acceptance. I therefore do **not** report that example as subscribing after rejection. Explaining the callback guarantee would improve the chapter and avoid forcing readers to infer it from implementation details.

## 6. Chapter-by-chapter editorial assessment

The table identifies the principal value and most useful revision for every chapter. It is deliberately selective: the cross-book findings above should be applied consistently rather than repeated in every row.

| Chapter | Assessment and recommended action |
|---|---|
| **1. Why SNode.C Exists** | A credible opening statement of the architectural purpose and an appropriately bounded claim about the framework. Shorten repeated declarations that layers matter. Give the prospective reader one concrete before/after design problem and a concise account of when another tool would be a better choice. |
| **2. Preparing Your Environment** | Good separation of source, build, installation, and external application. The exact framework pin is a strength. Correct the cached-prefix and generator instructions; provide companion acquisition, a tested host environment, and a clean-start command sequence. |
| **3. The Echo Pair** | A useful first success and a sensible introduction to context ownership. Preserve the complete source alignment. Add an expected transcript, a bounded exercise, and one controlled failure. Make clear what the example proves beyond a successful build. |
| **4. Reading the Codebase with Confidence** | Valuable navigation through source, applications, tests, and public surfaces. Reduce directory commentary that is revisited in Chapters 29 and 32. Give readers a guided trace from one include through one runtime behavior. |
| **5. The Mental Model** | Essential terminology and lifetime distinctions. Make this the authoritative home of that vocabulary. A compact glossary and one lifecycle trace would reduce the need to redefine the same objects later. |
| **6. Core Runtime and Event Processing** | Stronger than a superficial event-loop introduction, with useful lifecycle and tick vocabulary. Trim repeated architectural interpretation of names. State thread confinement, reentrancy, blocking-work limits, and supported external-loop integration explicitly. |
| **7. Layers in Practice** | The name-reading method is useful, especially the relationship between types, includes, and components. Consolidate overlap with Chapters 4–5. Clarify that the layer vocabulary is the framework's practical decomposition, not a replacement for standard network-layer terminology. |
| **8. Socket Addresses and Address Semantics** | Good attention to defaults and family-specific meaning. Replace some abstract comparisons with a small bind/connect experiment showing actual wildcard, empty, and zero-value consequences. |
| **9. Servers, Clients, and Connections** | Important distinction between status callbacks, attempts, established connections, and context readiness. This chapter substantially overlaps earlier definitions. Organize it around a successful connection, a failed attempt, and a disconnect trace. |
| **10. IPv4 and IPv6** | Correctly preserves common protocol structure while distinguishing endpoint identity. Needs a complete dual-family exercise, exact address/port setup, and one practical explanation of host-dependent dual-stack behavior. |
| **11. Unix Domain Sockets** | Peer credentials and the distinction between identity facts and authorization are valuable. Add a runnable example covering path ownership, permissions, stale-path handling, and cleanup. Avoid leaving the reader with questions that the chapter itself should answer. |
| **12. Bluetooth RFCOMM and L2CAP** | Broadens the framework's story beyond familiar IP examples. Qualify prior-pairing claims, identify supported socket semantics, and supply one hardware-tested recipe with explicit prerequisites. Keep unsupported platform generalizations modest. |
| **13. Writing SocketContext Classes Well** | The book becomes more practically useful here. The line protocol is an appropriate teaching choice. Correct the framing/length behavior, clarify what “processed” byte accounting means when bytes are buffered, and add fragmented-input tests. |
| **14. Writing SocketContextFactory Classes Well** | Explains construction and ownership responsibly. It is long relative to the new behavior introduced. Demonstrate dependency injection into a complete application sooner, then use the remaining space for lifetime mistakes and their consequences. |
| **15. Same Protocol over Different Lower Layers** | A good architectural consolidation point, but insufficiently procedural for its title. Build the same parser over IPv4 and Unix-domain sockets and show the identical application exchange plus genuinely different endpoint/setup behavior. |
| **16. Configuration Philosophy** | The single configuration authority and deployment-policy distinction are important. Merge substantial overlap with Chapter 17 or shorten this to a conceptual preface followed immediately by a worked configuration. |
| **17. Configuration in Detail** | Useful hierarchy, precedence, metadata, and tooling discussion. Use one consistent role name throughout a runnable example. Show code defaults, a saved file, a command-line override, and the resulting effective configuration. |
| **18. Logging and Diagnostics** | One of the strongest chapters. Preserve semantic scope, threshold precedence, typed errors, and cost distinctions. Add short actual text/JSON records and a diagnosis exercise; reduce source-inventory material where it interrupts use. |
| **19. TLS Across the Framework** | The architectural placement and lifecycle discussion are sound foundations. Add an authenticated connection walkthrough and explicit peer-name verification. A list of certificate/trust/SNI options is not yet a practical secure-client lesson. |
| **20. Timeouts, Retries, and Failure Modes** | Useful distinction between attempt retry, reconnect, timeout ownership, and queue admission. Remove duplicated timeout exposition. Show a controlled refused connection, a recovered connection, and a slow-peer policy with observable outcomes. |
| **21. The HTTP Layer** | Good explanation of HTTP objects, upgrade ownership, limits, and descriptor handoff. Establish a complete ordinary request/response example before the upgrade material. Replace the provisional companion-publication wording with a real access path. |
| **22. The Express-Like Framework** | Conceptual mapping is helpful, but the chapter lacks the complete route/middleware demonstration its audience needs. Show route matching, middleware order, continuation, early response, error handling, and asynchronous response lifetime in one small program. |
| **23. SSE and Real-Time HTTP** | One of the more concrete protocol chapters; the framework-specific fragment framing is valuable. Correct the Accept explanation, make subscriber lifetime explicit, and demonstrate disconnect/reconnect and the stated limits of replay support. |
| **24. WebSocket and Protocol Upgrade** | The two-stage upgrade/subprotocol model and loadable-module discussion are worthwhile. Complete the run/install path and test text versus binary behavior, fragmentation, invalid input, and close. Clarify exactly which echo behavior the sample promises. |
| **25. MQTT Support** | Useful separation of carrier, MQTT protocol object, and application behavior. State the supported MQTT version and callback guarantees. The companion role library needs a clearly linked executable exercise so readers can observe a real broker exchange. |
| **26. MQTT over WebSocket** | The reuse argument is clear. Reduce repeated composition explanation and supply a complete negotiated connection, selected subprotocol, message exchange, and one failure caused by missing upgrade/module support. |
| **27. Multi-Protocol IoT Systems** | Sensible attention to shared application state and role-specific failures. Overlaps Chapter 30. Ground it in one scenario with actual ordering, loss, duplication, and recovery decisions rather than another general role constellation. |
| **28. Database Support and Application State** | The separation between asynchronous work, command ordering, and transactional intent is valuable. Fix the SQL setup. Add an actual service-backed run and show what happens after a failed statement, including the transaction/rollback policy and safe input handling. |
| **29. Learning from src/apps** | Useful as a reader's source-navigation guide. Compress the catalogue and develop one or two applications more deeply. Remove editorial instructions such as a project's role “in the manuscript” being secondary. |
| **30. From Applications to Systems** | Strong subject, but much of the content repeats Chapter 27 and anticipates Chapter 37. Give this chapter the specific job of process boundaries, supervision, partial failure, and operational ownership, demonstrated through a deployment scenario. |
| **31. MQTTSuite** | A relevant applied ecosystem and a welcome step beyond tiny examples. Pin the separate source baseline, follow one message through concrete roles, and make clear which evidence is first-party. Add a reproducible small topology or narrow implementation claims. |
| **32. CMake Components and Linking** | Technically useful public-header/component distinctions and installed-consumer guidance. The long component tree and matrix impede narrative flow. Correct edge-direction ambiguity and move exhaustive lookup material to an appendix or maintained companion reference. |
| **33. Deployment on Linux and OpenWrt** | Correctly identifies packaging, filesystem, supervision, and target constraints. It is presently an operational-design overview. Supply a complete Linux service example and a tested OpenWrt recipe, or retitle/narrow the chapter accordingly. |
| **34. Testing, Debugging, and Benchmarking** | The evidence taxonomy is a major strength. Add one actual failing application regression, the diagnosis, and its passing boundary test. Include a small reproducible measurement rather than implying that naming tools constitutes a benchmark lesson. |
| **35. Building MiniGateway** | The most important practical chapter: source ownership and model-centered composition become concrete. Preserve the staged assembly. Resolve the MQTT extension, observer lifetime, GET mutation, and output-policy issues; clarify idle, disconnected, restart, and timestamp behavior. |
| **36. Extending MiniGateway** | A convincing demonstration that a new role can leave existing roles unchanged. Correct oversized-record recovery. Test valid, malformed, fragmented, and oversized input through the public Unix socket and verify resulting HTTP/SSE/MQTT observations. |
| **37. Architectural Judgment** | The worked sequence-ownership decision improves the synthesis. Retain that concrete reasoning and cut broad restatement. Include at least one decision where competing solutions are both credible and the tradeoff cannot be resolved by naming a layer alone. |
| **38. Extending the Framework Safely** | Sound extension discipline, but predominantly application-level evidence. Reduce repeated boundary advice and either add a small exported framework extension with installed-consumer verification or narrow the title. |

**Front matter:** the disclosure, prerequisites, and source baseline are useful. Tighten the audience promise, provide the real companion location and edition identifier, and make reading paths outcome-oriented.

**Part introductions:** these help orientation but often preview an argument already repeated at chapter level. Keep them short and explain what new capability the part delivers.

**Epilogue:** the central message is clear, but the philosophical review repeats much of the preceding synthesis. End with a short, specific account of what the reader can now build and how to continue. One strong conclusion is more effective than several successive conclusions.

**Further reading and index:** the selection of standards and foundational books is sensible. Add useful bibliographic details and direct, version-aware links, especially for framework/companion access and moving documentation. Review the manuscript's index terms for preferred terminology, synonyms, and useful subentries. Locator accuracy belongs to a later production proof. Add a concise glossary for the framework's overloaded vocabulary.

## 7. Language, presentation, and production

### Prose

The prose is usually understandable, and the author generally explains terms before using them. Its weakness is insistence: readers are frequently told that a distinction matters, that something is not decoration, or that the architecture remains honest. These expressions become less persuasive through repetition. Concrete consequences should carry more of the argument.

There is also residual planning language. Chapter 21 says the published edition should make companion sources available; Chapter 29 comments on what an application's role in the manuscript should be. Such sentences belong in an editorial plan, not the final reader-facing text. Replace them with direct instructions or remove them.

Use a style sheet for “Unix-domain,” “WebSocket,” “MQTT over WebSocket,” “Express-like,” “runtime instance,” “application role,” and related terms. Preserve meaningful distinctions but avoid making the reader learn several near-synonyms for one idea. Decide where contractions and direct second-person instructions are appropriate; the opening tutorial voice and later expository voice can coexist if transitions are deliberate.

A professional technical copyedit remains necessary after developmental revision. It should check grammatical slips, list parallelism, heading promises, defined abbreviations, callback/type spelling, example names, source references, and statements whose tense still reflects the migration process.

### Diagram content

The diagrams are most useful when they explain lifetime, ownership, or a flow that prose alone makes difficult. Some later system-constellation diagrams contribute less new information than their surrounding tables and could be consolidated. The current logging and testing diagram sources support the more specific explanations in their revised chapters.

Check arrow semantics rigorously: dependency, control flow, data flow, construction, containment, and conceptual association need explicit meanings. This is a recommendation about explanatory content; visual legibility and page design require a separate production review.

### Companion access and maintenance

The printed manuscript repeatedly refers to companion directories but lacks a finished reader-facing acquisition route. A directory name is useful only after the reader has obtained the right package. Publish a stable landing page or repository URL, an edition-specific download, the framework pin, instructions for the aggregate build, known optional dependencies, and a clear errata route.

Keep the immutable edition separate from examples maintained for later framework versions. The book already understands that distinction; the published material must make it easy for readers to follow it. Identify the licensing terms for reusable example code and confirm permissions for source-derived material during the publisher's normal rights process. This review did not perform a rights audit.

## 8. Acquisition, audience, and positioning

The strongest position is a **first-party SNode.C guide for experienced C++ developers, with a substantial architectural case study and advanced-course application**. The author has a credible reason to write it, and the integration of lower communication families with web, messaging, persistence, and operations gives the project a recognizable identity.

The principal market limitation is that the named framework defines a relatively specialized entry point. The supplied proposal does not establish independent demand at the scale a broad professional-trade acquisition might require. This is an evidence limitation, not a prediction of poor sales and not an independently measured statement about current adoption.

For specialist or project-authoritative publication, the acquisition question is whether the book saves a motivated user substantial time and helps them build more reliable systems. It can do so after the practical gaps are closed. For a broader architecture readership, it needs a stronger explanation of which lessons transfer, which costs arise from this framework's model, and when another model is preferable.

The course case is plausible but not yet fully supported pedagogically. A course spine needs learning objectives, exercises, expected outcomes, prerequisite mapping, and some instructor support. The present reflective questions and takeaways are helpful but are not a substitute for assessed practice. An independent instructor and several target readers should attempt selected chapters without author assistance.

The title is accurate for a specialist framework book. The subtitle makes a strong practical promise, so the revised manuscript must support “Building” with reproducible application work throughout. If the author chooses to preserve the predominantly conceptual treatment, a subtitle emphasizing architecture and design would better match the delivered experience.

The proposal's comparable-books section currently identifies shelves and categories rather than a researched set of actual competing titles. Before a commercial acquisition decision, develop a short, current comparison with specific editions, readership, practical coverage, and the reason this book earns a place beside them. No sales forecast or independently researched competing-title market analysis is asserted here.

For a revised sample package, I would retain the opening and echo material, include the revised logging chapter, and pair MiniGateway with its extension. The extension is important: it is the clearest evidence that the advertised architectural discipline produces a useful result. Samples should represent both the conceptual voice and the practical reliability of the final book.

## 9. Revision plan and acceptance criteria

### Stage 1: complete the reader's reproducibility instructions

Retain the identified book commit and framework pin. Complete the public companion acquisition instructions and connect them to the edition-specific examples. Attach the exact current verification run and distinguish passed, failed, skipped, and unexecuted paths.

**Acceptance criterion:** a reader can obtain the correct source package and identify its prerequisites and verification scope without reconstructing the repository's history.

### Stage 2: correct the technical teaching examples

Resolve the line-framing and recovery behavior, MQTT extension assumptions, SSE negotiation policy, observer cleanup/bounds, TLS verification recipe, GET mutation, and setup errors. Qualify Bluetooth claims. Apply corrections consistently to source, printed excerpts, diagrams, commands, and expected results.

**Acceptance criterion:** each substantive finding has either a corrected behavior with an appropriate test or a clearly justified and accurately documented limitation. A prose disclaimer alone should not substitute for fixing an example that demonstrates the wrong invariant.

### Stage 3: restructure for reader progress

Give the core vocabulary one authoritative home. Merge or shorten the largest areas of overlap. Move exhaustive component inventories to reference material. Introduce application work sooner and add the missing Express, TLS, MQTT-over-WebSocket, persistence, deployment, and diagnostic exercises.

**Acceptance criterion:** every practical chapter ends with a capability the reader has actually exercised, and every conceptual chapter has a distinct purpose that neighboring chapters do not already fulfill.

### Stage 4: independent technical and reader validation

Use a clean supported environment and an external reader. Run the exact printed setup and commands. Record full MQTT input/output with the chosen broker, database setup and failure handling, and the deployment targets actually claimed. Test invalid, fragmented, oversized, disconnected, and slow-peer cases at public boundaries. Hardware- and target-specific claims should have their own evidence or be narrowed.

**Acceptance criterion:** the reader can reproduce the promised outcomes without unpublished knowledge, and the report records the real limits of the validation. Framework tests and selected HTTP/SSE smoke tests remain valuable but do not stand in for these missing application workflows.

### Stage 5: copyedit and production proof

Complete a technical copyedit, reference/glossary/index pass, actual-trim figure review, running-head and contents review, accessibility planning, and a final cross-artifact consistency check. Remove planning language and identify code reuse terms.

**Acceptance criterion:** the edited manuscript, companion package, and eventual production proof agree with the edition's evidence. Page-level assessment is a separate task following manuscript revision.

## 10. Recommendation to the acquiring editor

**Invite substantial revision. Consider a conditional specialist acquisition if the author is willing to compress repeated exposition, strengthen the practical progression, and close the identified technical and reader-access gaps. This recommendation is based on the current Markdown manuscript; it makes no judgment about the currency or layout of the updated PDF.**

The manuscript's value lies in its informed account of a coherent framework and its insistence that application meaning, lifetime, and operational responsibility remain visible. That value is worth preserving. The necessary revision should make the book demonstrate its principles more consistently, let readers achieve useful results sooner, and ensure that the exact edition they receive supports the claims printed on its pages.

The author does not need a different subject. The author needs a tighter book, more decisive practical evidence, and a reliable publication handoff.
