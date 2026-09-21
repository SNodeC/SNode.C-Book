# Combined manuscript refinement — 21 September 2026

The combined editorial pass has been carried through all 38 chapters and all 62
manuscript inputs. Each chapter was read in full, refined locally across the six
agreed dimensions, and reviewed in the integrated reading sequence. The established
voice, explanatory depth, chapter order and cumulative teaching method remain.
Whole parts were not replaced, and no shortening target was used.

Five editorial dimensions meet their completion criteria. Practical depth has
been substantially developed and its local exercises verified, but its full
acceptance remains qualified by the OpenWrt prerequisite gap and the explicitly
pending hardware/service exercises. This is not a claim that the entire persistent
work plan or publication production is finished.

## What was completed

| Agreed dimension | Outcome |
|---|---|
| 1. Repetition and progression | Whole-book map completed; redundant inventories and second conclusions refined; purposeful reinforcement retained with reasons. |
| 2. Prose and voice | Local sentence/paragraph work across every chapter, followed by contextual rereading; abstract endorsements developed into concrete observations or costs. |
| 3. Reader positioning | Prerequisites, reading routes, chapter promises and movement from guided examples to independent diagnosis made more consistent. |
| 4. Practical depth | Runnable transfer, precedence, component-selection, Linux supervision and bounded measurement exercises added or strengthened; platform/service evidence remains individually pending. |
| 5. Architectural tradeoffs | Credible alternatives developed for ownership, TLS placement, recovery, process boundaries, persistence and the capstone's local input. |
| 6. References and figures | All 18 editable figures and surrounding explanations reviewed; labels and references checked; standards and implementation evidence distinguished. Visual production QA remains separate. |

The [repetition map](repetition-map.md) identifies the primary teaching home of
recurring concepts and records why later explanations remain. The
[work plan](../EDITORIAL-WORK-PLAN.md) gives the chapter-by-chapter ledger.

## Chapter-group outcomes

| Chapters | Substantive editorial result |
|---|---|
| 1–4 | Sharper primary reader and prerequisites; fewer repeated scope/directory inventories; installed-package diagnosis and a concrete source-tracing task replace general recaps. The first echo exercise has controlled observations and a failure boundary. |
| 5–9 | Shared endpoint configuration, per-call activation, connection and context lifetime are distinguished consistently. Runtime ordering and public tick limitations are explicit. Default addresses are separated from wildcard binds; callback timing and borrowed disconnect pointers are qualified. |
| 10–15 | Family chapters retain their address, permission, credential and platform depth while duplicate model lists are reduced. A complete IPv4-to-Unix exercise tests one unchanged line parser, fragmented input, peer isolation, failure before readiness and pathname cleanup. Factory dependency choices explain lifetime costs. |
| 16–20 | Configuration chapters now have different teaching jobs: policy and hierarchy, then traversal and observation. The precedence exercise distinguishes commented defaults from active assignments. Current runtime reconfiguration, frozen logging policy, TLS trust versus expected identity, retry counts, per-flow timers and protocol deadlines are precise. |
| 21–26 | Web chapters progress through admission, dispatch, retained response lifetime and negotiated upgrade. Middleware exercises observe both responses and handler counts. MQTT acceptance, subscription and delivery are separated. The WebSocket adapter exercise includes concrete binary CONNECT bytes and endpoint prerequisites. |
| 27–31 | Multi-protocol diagrams describe fan-out rather than an accidental serial pipeline. System choices now include partial failure, independent restart and compatibility costs. MariaDB command errors and prequeued commit behavior are corrected. MQTTSuite raw storage and projection are identified as separately queued writes. |
| 32–34 | Dependency visibility is qualified for static linking. Component failure is an executable exercise. Linux deployment now includes an installed consumer, configuration, supervision, restart, failure and recovery. OpenWrt identifies its actual recipe mismatch. Testing distinguishes diagnostic formatting from wire exchanges and adds a bounded measurement example. |
| 35–38 | Capstone limitations are explicit: in-memory ordering, process-wide MQTT registry, concrete input-topic matching, CONNACK versus SUBACK, and publication-driven SSE cleanup. Malformed/split input exercises and credible protocol/process alternatives develop judgment. Extension questions distinguish a shared domain change from adding another carrier. |

All front matter, part introductions, the epilogue and back matter were included.
Some framing material was retained after assessment because it already served its
transition or orientation purpose. A review does not require changing every file.

## Repetition that changed, and repetition that stays

The clearest removals concern repeated framework/context inventories in the Unix
and Bluetooth chapters, overlapping configuration-name inventories, a repeated
one-tick definition, repeated full-stack openings, and closing paragraphs that
restate an exercise immediately above them. Several repetitions became a new
question instead: which value won, which callback ran, which object survived,
which output completed, or which component failed to load?

The model is still taught cumulatively. A local header remains beside an example
even though Chapter 32 collects headers and components. TLS retains detailed
readiness and shutdown explanation because those phases change its operational
meaning. MiniGateway Extended keeps its before/after comparison because unchanged
model and output roles are the comparison's evidence. Chapter summaries and the
epilogue still synthesize earlier material.

The result is more precise and less repetitive without turning the book into a
short reference manual. The added exercises supply practice at the existing
explanatory depth.

## Alignment with the author's current source

The authority was `/home/voc/projects/snodec/snode.c`, including the author's
uncommitted changes. Neither remote `master` nor the reconstruction base alone
was used as a substitute.

- Framework project version: **2.0.0**.
- Author HEAD at capture: `2e52b6b7337f21812932eb1e097fb3c27c8228a9`.
- Working tree: **25 changed paths**, included in the captured contents.
- Exact content digest: `df2fbdbe844f3368f5ed142973d82c0008a057c13d87dda6b7670e45cc3eacb8`.
- Captured files: **1,447**.
- Reconstruction base: `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`, plus the supplied patch.

The author changed the framework during this pass. Per-call flow control, checked
runtime reconfiguration, and scoped binary logging were reconciled as they appeared.
The logging chapter now covers the public `hexDump(...)` operation, its borrowed
input, disabled-level behavior, output policy and synchronous cost. The final MQTT
change guards diagnostic payload preparation; it does not change the protocol
contract described in the book.

Two source findings deserve particular attention:

1. On a usable MariaDB connection, a command-level SQL error does not automatically
   cancel the remaining sequence. A prequeued commit is still queued; a new rollback
   sequence from an error callback does not jump ahead of it. Chapter 28 now teaches
   that exact limitation and the necessary conditional enqueue/interleaving policy.
2. The tests named `HttpRequestFormatterRawWireTest` and
   `HttpResponseFormatterRawWireTest` inspect diagnostic `toString(...)` output.
   Their names do not make them observations of transmitted HTTP bytes. Chapter 34
   now distinguishes them from the actual component exchanges.

The [source-claim map](../verification/source-claims.json) provides chapter-specific
implementation anchors. Mechanical checks establish file identity, anchor location
and listing equality; they do not prove every sentence's meaning. The manual source
reading and the bounded runtime checks provide the corresponding semantic evidence.
This is traceable verification of the stated contracts, not universal protocol or
deployment certification.

MQTTSuite was inspected separately at clean revision
`f96daffdbae8f95531a73fb52c9d22d410044211`. Its selected source hashes are in the evidence
record. No MQTTSuite build or deployment is claimed. The OpenWrt feed was inspected
at `c9378fe95f7c015752c748fc4ab012b585d294d1`; it still selects framework 1.0.1 and an
`OpenWRT` branch, so Chapter 33 requires a real 2.0 recipe port.

## Verification and its limits

The current framework was rebuilt and installed with GNU C++ 16.2.0, CMake 4.3.4,
OpenSSL 3.6.3, Debug framework libraries, tests/applications enabled, documentation
and the optional Curses interface disabled. Companion and external consumers were
rebuilt against that installation. The service consumer used Release compilation
with those Debug framework libraries; its timing output is not a capacity claim.

| Check | Result and scope |
|---|---|
| Framework CTest | **183/183 passed**, no skips in this run. |
| Installed external echo | **4/4 passed**: discovery, independent server/client peers and bounded pair. |
| Contract probes | **3/3 passed**: public tick limitation, TLS trust/identity, numeric global and named scoped logging. |
| Teaching smoke checks | **3 groups passed**: logging output, controlled echo server, controlled echo client. |
| Companion behavior | **4 scenarios passed**: SSE, Extended Unix input, whole/split line-length boundaries, MQTT CONNECT protocol level for both gateways. |
| Chapter 15 transfer | Both carriers passed framing, independent-peer, isolation and cleanup observations. |
| Chapter 17 precedence | Effective values 8080 / 18091 / 18092 observed; display exit 2 and unchanged input file checked. |
| Chapter 24 negotiation | Installed echo modules selected `echo`; the client received `hello` and closed. Unsupported selection attached no echo; an independent request observed HTTP 404. |
| Chapter 32 component request | Nonexistent required component rejected at configuration; restored component configured and built. |
| Chapter 33 Linux service | Unit syntax checked; installed foreground and transient supervised exchanges, changed PID after restart, invalid-port failure, recovery and final stop checked. |
| Chapter 34 measurement | Printed bounded 200-sample exchange executed with complete payload verification. It is a small loopback experiment, not a load benchmark. |
| Source reconstruction | Base plus patch reproduces all 1,447 recorded file contents. |
| Manuscript consistency | 38 chapter evidence records, 35 exact complete listings, source hygiene and figure/reference checks passed. |

The service rehearsal substituted temporary executable/configuration paths and an
isolated framework configuration base. It used a transient user unit; it did not
install or enable the printed persistent home-directory unit. These substitutions
are recorded in its harness and log. The test resources were stopped afterward.

Earlier cohorts and failures remain recorded. The first binary-logging run found
one obsolete whitespace expectation in the HTTP diagnostic formatter test. The
author's subsequent source updated that expectation and the renderer; the fresh
run passed. No framework files or tests were modified by this editorial pass.
Corrected harness mistakes are explained in [the evidence index](README.md).

The runtime logs are linked by [the machine-readable evidence record](evidence-2026-09-21.json).
Primary protocol and tool references were added to the back matter. The OpenWrt
SDK documentation returned an anti-bot page during automated access, so its full
page content was not independently checked here. Local reference checks do not
claim to validate every external website.

## Change accounting

Against the hashed editorial starting snapshot, which already includes the earlier
technical refinement:

- Manuscript: **144,662 → 151,071 words**, an incidental increase of **6,409**.
  These are whitespace-delimited Markdown source words, including listings, tables
  and index directives; they are not a prose-only publication count.
- Manuscript lines: **828 added / 1,026 removed** across 44 changed inputs.
  Paragraph reshaping makes line counts different from word counts.
- Figure sources: **39 added / 33 removed**; 11 figure sources changed, all 18 reviewed.
- Companion production C++: **0 added / 0 removed** in this pass; 70 recorded production
  files still match the preceding technical-refinement evidence byte-for-byte.
- New editorial probe support: **382 added / 0 removed** across four scripts.
- Existing source-check support: **0 added / 3 removed**. The redundant requirement
  that current HEAD equal the reconstruction base was removed; complete content
  comparison remains. A commit with unchanged file contents is not source drift.

The MiniGateway companion README and its printed excerpt were also synchronized.
Audit records, manifests, source patches and logs are evidence/documentation, not
new application implementation. The [detailed accounting](change-accounting-2026-09-21.json)
retains per-input hashes and changes. Existing earlier production changes in the
working tree were preserved and are not relabeled as new editorial work.

## What remains open

The practical-depth criterion stays qualified until a matching OpenWrt SDK, a
ported framework/application recipe and a disposable target can establish the
cross-build, installation and service/reboot behavior. The old feed is not a valid
substitute. Bluetooth hardware, controlled MariaDB service integration, full MQTT
broker/subscription/delivery exercises, MQTTSuite deployment and sustained-load or
long-duration behavior also remain explicitly unexecuted.

The separately tracked implementation items remain open: disconnection-driven
SSE subscription removal during idle churn, and deliberate handling of unsupported
binary input in the text WebSocket echo example. Describing those limitations did
not fix them. They require the ownership review and implementation/approval rules
already recorded in the persistent plan.

No PDF was read or regenerated. Figure layout, page placement, typesetting and
final production QA remain separate work. The Markdown manuscript and editable
figure sources are the refined result of this pass.
