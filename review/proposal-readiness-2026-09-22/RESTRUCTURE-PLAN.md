# Restructure plan — teaching book

**Status: awaiting author approval.** Proposed on 22 September 2026. This is a
planning document; no manuscript, companion, TOC, or proposal edit is applied.
Approval must be recorded in `review/EDITORIAL-WORK-PLAN.md` before Phase 5a.

## Decision requested

Approve a main learning path of **30 numbered chapters in 11 Parts**, followed
by the existing epilogue and **Appendix A, Reading and Extending the Framework**.
Keep the five sample chapters as identifiable chapters and keep the two MiniGateway
construction chapters adjacent near the end. The proposed total is **112,250
whitespace tokens**, including code, appendix, front/back matter, Part checkpoints,
and new pedagogical material. This leaves 2,750 words below the 115,000 ceiling.
The 105,000 stretch remains optional; this plan does not pretend to achieve it.

The proposed merges below refine the existing explanations. They do not replace
them with a new generic treatment. Remove repeated framing, parallel explanations
with the same consequence, and duplicate recaps; keep the explanation that first
teaches a distinction and later uses that apply it to a new problem. Preserve
complete listings, the author's teaching voice, technical depth, and the deliberate
epilogue closing. The new appendix is included in every word and teaching budget;
relocation is not counted as shortening.

The governing teaching invariant is that a reader with the stated prerequisites
can follow the main path without consulting the contributor appendix or needing
a lecturer. A concept must be explained before a milestone depends on it. All
runtime milestones below are **proposed work**, except the expressly identified
existing sample labs; they are not newly implemented or newly verified here.

## Why these consolidations

| Candidate | Recommendation | Teaching reason and preservation boundary |
| --- | --- | --- |
| Old 5–7 → two chapters | Accept: combine 5 and 7 as new 4; keep 6 as new 5 | One chapter establishes endpoint/flow/connection/context lifetime and the selectable layers. The next explains event delivery, timers, cleanup, and shutdown. Do not interleave source-level multiplexer details with a learner's first vocabulary pass. |
| Old 8, 10, 11 → one family chapter | Accept as new 6, before old 9 → new 7 | Teach endpoint identity once, then contrast IP resolution and Unix path/permission/credential semantics. Keep the detailed connection lifecycle in new 7. Bluetooth remains new 8 because preparation and service discovery are additional teaching problems. |
| Old 16–17 → one configuration chapter | Accept as new 12 | Teach the hierarchy, precedence, inspection, and one controlled echo experiment as one argument. Preserve runtime reconfiguration limits and the distinction between displayed values and effective policy. |
| Old 29–31 → one larger-systems chapter | Accept as new 24, with a protected worked-system spine | Follow an executable from its build target to its roles, then to MQTTSuite's concrete topology and persistence. Replace repeated catalogues and operational framing; retain tool-specific distinctions, focused examples, and both system diagrams. |
| Old 4 and 38 → contributor appendix | Accept conditionally: move the extended treatment to A and retain an introduction of at most 300 words in new 4 | A learner still needs to decode a public type and distinguish source path, include path, and component. Keep that minimum on the main path; the appendix develops source navigation and reusable extension after the capstone. |

### New 4 and 5: one model, then its execution

Read together: old 5's runtime/lifetime treatment at
`manuscript/chapters/05-the-mental-model-of-snodec.md:60`, its layer treatment at
line 302, old 7's layer choices and transfer discussion at lines 345–530, and
old 6's event-processing treatment at lines 99–591. New 4 should progress from
the echo pair to the handle/endpoint/flow distinction, connection/context/factory
ownership, then the lower-layer choices, with one worked type/header/component
comparison. Reuse the existing lifetime figure. Combine old 5's and old 7's
stack summaries; refer to Figure 1 instead of repeating it in arrow blocks.

New 5 retains the public runtime surface, coarse state versus a tick result,
event versus readiness, multiplexer sequence, descriptor/timer behavior, and
coordinated shutdown. Keep the source excerpts and the consequences of slow
callbacks. Compress parallel lists of publisher/receiver responsibilities into
one explanation tied to observable work. Preserve all technical qualifications.

The main-path source-reading introduction comes from old 4:151–240 and 360–378.
It is included in new 4's budget and removed from Appendix A's allocation. Old
5's two references to having already read Chapter 4 must become references to
this introduction; pointing them to an optional appendix would break the path.

### New 6: address meaning before connection machinery

Old 8:61–103 supplies local versus remote identity and the family comparison.
Combine it with old 10's parallel IPv4/IPv6 wrappers and resolution discussion,
then old 11:52–255 and 312–399 on paths, ownership of the filesystem entry,
permissions, cleanup, and peer credentials. A single comparison table can carry
shared call shapes; sentences must still explain what wildcard bind, a concrete
peer, and a local pathname mean. Keep credentials distinct from authorization.

New 6 uses the already familiar echo program for endpoint observations. It must
not require detailed accept/connect machinery before new 7 teaches it. New 7
retains attempt/flow/connection/context lifetimes and callback ordering. New 8
retains RFCOMM versus L2CAP, service discovery/preparation, and hardware limits.
This prevents a broad family merge from flattening platform-specific knowledge.

### New 12: configuration explained through one experiment

Use old 16:94–253 for the three input paths and precedence; old 17:22–377 for
the hierarchy and scoped options; old 17:512–531 for the echo-server precedence
experiment; old 17:644–687 for discovery, control, and policy snapshots. Explain
naming and parameterless activation once beside the actual command/configuration
views. Fold the two section catalogues together. Preserve persistence versus
one-run actions, anonymous/deeper nodes, runtime reparse limits, and the fact
that reconfiguration is not endpoint reactivation. Do not reduce these to an
option list or duplicate a CLI11 manual.

### New 24: one journey from application to system

Retain three substantial sections: (1) build target, public includes, and
composition root, from old 29:45–410; (2) role/process/state boundaries and
restart consequences, from old 30:46–461; (3) MQTTSuite as the worked system,
from old 31:26–405. Keep the web application shell, echo matrix, JSON pair,
`testpost`, and database examples as a compact application-purpose table with
their distinct lessons. Keep complete code unchanged, including any examples
within those source ranges. Detailed component rules remain in new 25.

MQTTBroker's web administration, MQTTIntegrator's transformation, MQTTBridge's
topology, MQTTCli's operational role, and MQTTStore's raw/projection persistence
must remain distinguishable. The publication trace at old 31:395 is the payoff.
Use it to apply old 30's boundary questions rather than repeating that chapter's
checklist. Keep the private MQTT option and delivery/persistence qualifications.
This is the most demanding merge: its 6,200-word budget is a planning ceiling,
not evidence that a safe 42% net reduction has already been achieved. If the
worked trace and its prerequisites do not fit after removing repetition, stop
that Part as qualified and revise the plan with the author.

### Appendix A and the final Part

Appendix A develops application-first source navigation, header/alias/build
reading, and locating the correct change boundary. Then it develops safe
extension through the existing context/factory, routing, WebSocket, MQTT,
configuration, diagnostics, and testing examples. Preserve old 38's concrete
MiniGateway extension excerpts while referring to the full construction in new
29. One table can replace repeated “appropriate extension point” introductions;
it must retain the selection criterion and a consequence for each choice.

Old Part XII would contain only old 37 after moving 38. Put architectural
judgment (new 30) at the end of Part XI, after new 28–29's integrated application.
This keeps the decision chapter beside the system it evaluates and avoids a
one-chapter Part. Preserve the epilogue's argument and final author-selected
closing words. Add its objective/recap/exercise apparatus around that text in
the final session without replacing the closing argument. Appendix A follows
the epilogue, before further reading and the index, as an optional contributor
path; it also receives objectives, a recap, and public tiered exercises.

## Proposed TOC and chapter word budgets

Every budget below is a **total raw whitespace-token ceiling** under
`ci/manuscript-metrics.py`, including headings, objectives, recaps, exercise
prompts, captions, index markup, and fences. The conservative prose allowance
subtracts *all current fenced words*, even the text diagrams slated for removal.
Thus the arithmetic needs no code cuts. Removing a redundant text fence may
change the prose/fence partition; measure the resulting total again.

Allow approximately 450–600 words within each unsampled chapter's budget for
objectives, recap, and five exercises. Public solutions stay under
`companion/exercises/<chapter>/`; the printed public-solution pointer is counted.
Chapter 2 has a tighter allowance of at most 400 new apparatus words; retain its
existing preparation instructions. The five samples retain their three objectives, five exercises, public solutions,
and original Phase 2 prose-reduction thresholds. Reuse their labs as checkpoints
where applicable. No additional checkpoint prose may silently erase the 20%
reduction, particularly in the SSE and MiniGateway samples.

“H” is a ceiling on level 3–6 headings, not a quota. It includes subordinate
headings and empty parent sections. Each chapter and Appendix A must also have
an actual average section length of at least 250 prose words; do not pad prose or
simply disguise a heading to obtain the metric. Fold short repeated sections into
connected explanations. The epilogue follows the same standard.

| Part | Proposed title | New chapters | Chapter words |
| --- | --- | --- | ---: |
| I | Getting Oriented | 1–3 | 7,850 |
| II | The SNode.C Architecture | 4–5 | 9,000 |
| III | Networking Foundations in SNode.C | 6–8 | 11,050 |
| IV | From Raw Connections to Application Protocols | 9–11 | 8,800 |
| V | Configuration and Operational Behavior | 12–13 | 8,150 |
| VI | Secure and Robust Communication | 14–15 | 6,350 |
| VII | Web Protocols and Web Applications | 16–19 | 11,300 |
| VIII | IoT and Message-Oriented Systems | 20–22 | 7,400 |
| IX | Persistence and Full Systems | 23–24 | 10,100 |
| X | Building, Porting, and Maintaining | 25–27 | 11,600 |
| XI | Building and Evaluating MiniGateway | 28–30 | 8,900 |

The epilogue and Appendix A follow Part XI. Part-opening/checkpoint prose is
allocated separately below and is not counted twice in these chapter totals.

| New | Part | Title | Old sources | Current total | Budget | Prose allowance* | H |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1 | I | Why SNode.C Exists | 1 | 1,820 | 1,850 | 1,753 | 5 |
| 2 | I | Preparing Your Environment | 2 | 2,944 | 3,350 | 3,044 | 9 |
| 3 | I | Your First Working Program: The Echo Pair | 3 | 2,565 | 2,650 | 2,072 | 6 |
| 4 | II | The Mental Model and Layers in Practice | 5, 7 | 7,807 | 5,300 | 4,787 | 15 |
| 5 | II | Core Runtime and Event Processing | 6 | 5,189 | 3,700 | 3,601 | 11 |
| 6 | III | Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 8, 10, 11 | 8,266 | 5,200 | 4,735 | 15 |
| 7 | III | Servers, Clients, and Connections | 9 | 4,858 | 3,650 | 3,420 | 10 |
| 8 | III | Bluetooth in SNode.C: RFCOMM and L2CAP | 12 | 2,612 | 2,200 | 2,050 | 5 |
| 9 | IV | Writing `SocketContext` Classes Well | 13 | 4,297 | 3,200 | 2,896 | 8 |
| 10 | IV | Writing `SocketContextFactory` Classes Well | 14 | 3,866 | 2,800 | 2,509 | 7 |
| 11 | IV | Building the Same Protocol over Different Lower Layers | 15 | 3,627 | 2,800 | 2,479 | 7 |
| 12 | V | Configuring Applications and Named Instances | 16, 17 | 8,698 | 5,400 | 4,889 | 16 |
| 13 | V | Logging, Diagnostics, and Runtime Introspection | 18 | 3,778 | 2,750 | 2,450 | 7 |
| 14 | VI | TLS Across the Framework | 19 | 3,790 | 2,950 | 2,753 | 8 |
| 15 | VI | Timeouts, Retries, and Failure Modes | 20 | 4,533 | 3,400 | 3,086 | 9 |
| 16 | VII | The HTTP Layer | 21 | 3,515 | 2,600 | 2,210 | 6 |
| 17 | VII | The Express-Like Framework | 22 | 3,058 | 2,350 | 2,097 | 5 |
| 18 | VII | Server-Sent Events and Real-Time HTTP | 23 | 3,268 | 3,300 | 2,929 | 7 |
| 19 | VII | WebSocket and Protocol Upgrade | 24 | 3,982 | 3,050 | 2,499 | 7 |
| 20 | VIII | MQTT Support in SNode.C | 25 | 2,996 | 2,350 | 2,062 | 5 |
| 21 | VIII | MQTT over WebSocket | 26 | 2,730 | 2,100 | 1,722 | 4 |
| 22 | VIII | Designing IoT Systems with Multiple Protocols | 27 | 3,971 | 2,950 | 2,766 | 8 |
| 23 | IX | Database Support and Application State | 28 | 5,196 | 3,900 | 3,400 | 10 |
| 24 | IX | SNode.C in Larger Systems | 29, 30, 31 | 10,711 | 6,200 | 5,174 | 17 |
| 25 | X | CMake Components, Public Headers, and Linking Strategy | 32 | 6,310 | 4,100 | 3,412 | 10 |
| 26 | X | Deployment on Linux and OpenWrt | 33 | 5,557 | 3,700 | 3,382 | 10 |
| 27 | X | Testing, Debugging, and Benchmarking | 34 | 5,722 | 3,800 | 3,335 | 10 |
| 28 | XI | Building MiniGateway | 35 | 3,834 | 3,850 | 1,879 | 6 |
| 29 | XI | Extending MiniGateway with a New Network Role | 36 | 2,966 | 3,150 | 2,249 | 6 |
| 30 | XI | Architectural Judgment: Choosing the Right Layer and Boundary | 37 | 1,877 | 1,900 | 1,882 | 6 |
| A | Appendix | Reading and Extending the Framework | 4, 38 | 6,976 | 4,700 | 3,442 | 10 |

*Prose allowance assumes every existing fenced token in the source chapters is
retained. New 4's 300-word introductory transfer is already inside its ceiling;
Appendix A must release those words. For merged chapters, current totals are
sums of their old inputs before any condensation.

| Other counted material | Current total | Budget | Treatment |
| --- | ---: | ---: | --- |
| Epilogue: The Principles Behind the Programs | 1,529 | 1,900 | Keep author closing; add the teaching apparatus, H ≤ 4 |
| Front matter | 2,291 | 2,500 | One main learning path and at most two shortcuts; prerequisites remain explicit |
| Eleven Part openings/checkpoints and epilogue opener | 1,075 | 1,650 | Eleven Part introductions/checkpoint pointers plus the existing epilogue opener |
| Reference material and public-solution pointers | 736 | 1,000 | Further reading, index source, and public solution pointers; full solutions remain public companion material |

| Allocation | Words |
| --- | ---: |
| 30 numbered chapters | 100,500 |
| Appendix A | 4,700 |
| Epilogue chapter | 1,900 |
| Front matter | 2,500 |
| Part/epilogue openers and checkpoint pointers | 1,650 |
| Back matter | 1,000 |
| **Planned total** | **112,250** |
| Unallocated room below the hard ceiling | 2,750 |
| Current measured total | 146,950 |
| **Required net reduction to this plan** | **34,700** |

Current fenced content is 14,450 tokens, leaving 97,800 planned tokens if all
of it is retained. New pedagogical prose consumes part of that allowance: for
25 unsampled numbered chapters, approximately 11,250–15,000 words must be found
*inside* the budgets by further prose refinement, not added above them. Appendix
and epilogue teaching elements have their own included allocations. The chapter
heading ceilings sum to **269** including A and the epilogue, below the global
550 ceiling. At 250 words per section, 269 sections need 67,250 section-body
words; the budget leaves room for that plus listings, preambles, and other matter.
Actual measured averages remain exit checks, not an arithmetic guarantee.

No future page count is asserted for an unbuilt structure. The current PDF is
470 pages; the final sub-phase will regenerate the proposal TOC, Part extents,
and page counts from the actual build. The 2,750-word reserve is not permission
to exceed a chapter ceiling silently; record and obtain approval for any budget
redistribution that changes this plan. The stretch target would need a further
7,250-word cut below this plan and must not sacrifice the stated teaching depth.

## Old-to-new map and reference migration

The following is the chapter-identity map. New numeric filenames should use the
new chapter number and title slug; the appendix belongs under
`manuscript/chapters/appendix-a-reading-and-extending-the-framework.md` so the
existing chapter metrics also count it. The one manifest remains the order
authority. Keep short explicit semantic anchors for moved topics where an old
chapter now resolves to a section inside a merged chapter.

| Old chapter | New chapter | Main destination |
| --- | --- | --- |
| 1 | 1 | Why SNode.C Exists |
| 2 | 2 | Preparing Your Environment |
| 3 | 3 | Your First Working Program: The Echo Pair |
| 4 | A | Reading and Extending the Framework (minimum orientation stays in new 4) |
| 5 | 4 | The Mental Model and Layers in Practice |
| 6 | 5 | Core Runtime and Event Processing |
| 7 | 4 | The Mental Model and Layers in Practice |
| 8 | 6 | Network Families: Addresses, IPv4/IPv6, and Unix Sockets |
| 9 | 7 | Servers, Clients, and Connections |
| 10 | 6 | Network Families: Addresses, IPv4/IPv6, and Unix Sockets |
| 11 | 6 | Network Families: Addresses, IPv4/IPv6, and Unix Sockets |
| 12 | 8 | Bluetooth in SNode.C: RFCOMM and L2CAP |
| 13 | 9 | Writing `SocketContext` Classes Well |
| 14 | 10 | Writing `SocketContextFactory` Classes Well |
| 15 | 11 | Building the Same Protocol over Different Lower Layers |
| 16 | 12 | Configuring Applications and Named Instances |
| 17 | 12 | Configuring Applications and Named Instances |
| 18 | 13 | Logging, Diagnostics, and Runtime Introspection |
| 19 | 14 | TLS Across the Framework |
| 20 | 15 | Timeouts, Retries, and Failure Modes |
| 21 | 16 | The HTTP Layer |
| 22 | 17 | The Express-Like Framework |
| 23 | 18 | Server-Sent Events and Real-Time HTTP |
| 24 | 19 | WebSocket and Protocol Upgrade |
| 25 | 20 | MQTT Support in SNode.C |
| 26 | 21 | MQTT over WebSocket |
| 27 | 22 | Designing IoT Systems with Multiple Protocols |
| 28 | 23 | Database Support and Application State |
| 29 | 24 | SNode.C in Larger Systems |
| 30 | 24 | SNode.C in Larger Systems |
| 31 | 24 | SNode.C in Larger Systems |
| 32 | 25 | CMake Components, Public Headers, and Linking Strategy |
| 33 | 26 | Deployment on Linux and OpenWrt |
| 34 | 27 | Testing, Debugging, and Benchmarking |
| 35 | 28 | Building MiniGateway |
| 36 | 29 | Extending MiniGateway with a New Network Role |
| 37 | 30 | Architectural Judgment: Choosing the Right Layer and Boundary |
| 38 | A | Reading and Extending the Framework |

The complete [reference migration register](phase-4-reference-map.md) is part
of this plan. It enumerates **374 occurrences**, including **326 requiring a
migration treatment**, with current path, line, phrase, intended target, and
required treatment. It covers all **276** singular manuscript references counted
by the metrics tool, and additionally plural/multiline/range references, running
heads, public companion documentation, proposal text, and relevant tool messages.
A policy guard is explicitly distinguished from reader text. The register is
not a blind search-and-replace specification.

The particularly important semantic cases are:

- Old 5:10 and 393 point to the retained orientation inside new 4, not the optional
  appendix. Old 7's claim that old 6 has already been read must become a forward
  runtime pointer when 5 and 7 are joined ahead of new 5.
- References among old 8/10/11, 16/17, or 29/30/31 become named section references
  inside new 6, 12, or 24. The old 29→30→31 text block is redundant framing;
  remove it during that Part's condensation, after mapping its intended meaning.
- “Chapters 1–7” becomes the foundation in new 1–5, excluding Appendix A. Ranges
  expand through the identity map before recompression; shared targets are
  deduplicated. The proposed web/MQTT shortcut is 1–5, 12–13, 15–18, 20, 25, 28,
  with the remaining security/family/deployment chapters still part of full study.
- Samples become **1, 3, 18, 28, 30**. Update the proposal sample CMake paths,
  displayed sample numbers, ledger mappings, and public solution links together.
- Rename sample exercise directories ch23→ch18, ch35→ch28, ch37→ch30 and their
  chapter-oriented build/test labels in one change; update commands in public
  answers and any CI selection patterns. Keep example project names stable.
- The printed MiniGateway README is a complete companion copy. Renumber its
  chapter mentions in the canonical README and its marked listing together;
  rerun alignment. No other code listing is cut to reduce words.
- Chapter 2 remains at 2. Its ordinary pointers to diagnostics/testing must resolve
  to new 13/27. Changes to its preparation instructions are outside this plan.

In Phase 5a, implement the requested reference check from this map and register.
For every migrated occurrence, record a stable intended chapter/topic anchor,
its new source location, and either the updated reference or an explained removal
of duplicate framing. Check that the anchor exists once in the ordered manifest
and that its displayed chapter number matches. A check that merely accepts any
number from 1 to 30 is insufficient: old Chapter 23 now means a different subject.
Scan singular/plural forms, ranges, line-wrapped lists, running heads, and public
solution/documentation references. Require explicit disposition for every register
row, and include a negative fixture in which a valid number names the wrong topic.
Do not mutate historical reports to make old numbers disappear.

The new chapter/anchor map must also drive the existing alignment check's chapter
coverage and current `review/verification/source-claims.json` associations. Merge
source/companion evidence by semantic chapter destination without losing anchors;
include Appendix A. Replace the existing 38-chapter cardinality assumption with
coverage of the approved manifest. Likewise migrate the hygiene script's exact
old Chapter 10 filename expectation to the new family chapter; preserve its
original purpose and all forbidden-phrase guards. Earlier Phase 2/3 review scripts
remain evidence for their original stage; new exits carry sample identity through
the approved map instead of modifying those historical records.

## Figures, index, and other publication surfaces

Preserve all **18 figure assets, captions, and label IDs**. No illustration needs
to be redrawn for this plan. Their reading order remains unchanged; global figure
numbers should therefore remain unchanged if the production counter remains the
same. Chapter-qualified numbers and page numbers must be regenerated and checked.
Figure 1 remains the authority for the layer stack. New 24 retains both the
application-as-system diagram and the MQTTSuite ecosystem diagram because they
answer different questions.

| Figure label | Current chapter | New chapter |
| --- | ---: | --- |
| `fig:snodec-layer-stack` | 1 | 1 |
| `fig:snodec-runtime-model` | 5 | 4 |
| `fig:snodec-event-runtime` | 6 | 5 |
| `fig:server-client-path` | 9 | 7 |
| `fig:snodec-lower-family-transfer` | 15 | 11 |
| `fig:configuration-hierarchy` | 17 | 12 |
| `fig:logging-diagnostic-visibility-map` | 18 | 13 |
| `fig:tls-connection-layer-specialization` | 19 | 14 |
| `fig:retry-reconnect-flow` | 20 | 15 |
| `fig:web-protocol-layer-structure` | 24 | 19 |
| `fig:native-mqtt-vs-mqtt-over-websocket` | 26 | 21 |
| `fig:iot-boundary-constellation` | 27 | 22 |
| `fig:persistence-boundary` | 28 | 23 |
| `fig:application-system-role-constellation` | 30 | 24 |
| `fig:mqttsuite-ecosystem-map` | 31 | 24 |
| `fig:build-install-package-deployment-surface` | 33 | 26 |
| `fig:testing-confidence-surfaces` | 34 | 27 |
| `fig:minigateway-extended-network-role-architecture` | 36 | 29 |

The inventory records **1,033 index insertions with 821 distinct keys**. Preserve
the key vocabulary and attach entries to their retained explanations as text
moves. Two insertions can collapse only when the same concept's duplicate passage
is actually removed; do not delete an index topic merely to reduce counts.
Union the merged chapters' keys and preserve the contributor keys in Appendix A.
Regenerate index pages and inspect the entries for contexts/factories, configuration,
Unix sockets, MQTTStore, and MiniGateway. No page-number edit by hand is valid.

The reference inventory also records **five hardcoded chapter/section running-head
commands**, explicit semantic anchors, and **30 Part-reference occurrences**.
Recompute section-number overrides after condensation; preserve or update each
explicit anchor's incoming references. Check implicit heading anchors and PDF
bookmarks after merged chapter-title changes. Update `book-files.txt`, Part files,
`STRUCTURE.md`, README positioning, and proposal/sample links in Phase 5a.
The main book remains the learning-path authority; the proposal follows it.

## MiniGateway milestones and runnable Part checkpoints

MiniGateway should be a running project in the learning narrative and companion
exercises, while the complete integration remains old 35–36, now **28–29**.
Introduce the measurement problem at the first echo exercise. Progressively
isolate its model, inputs, configuration, and protocol observations. Use the
existing canonical `Measurement`, model, codec, and role sources where they are
needed; do not maintain eleven copied versions of the application. Earlier
experiments may use focused test targets and source excerpts, with the full
assembly/listings retained in new 28–29.

Each row is the Part's mandatory final checkpoint, with a public command sequence
and an explicit expected observation to be supplied in that Part's Phase 5 session.
It is included in the final chapter's mapped exercises, not an extra unmapped
exercise set. Part openers provide short pointers within their 1,650-word shared
budget. Additional optional hardware/service experiments must identify their
prerequisites and cannot be counted as executed by a build-only check.

| Part / new chapters | MiniGateway milestone | Run and observe | Existing basis and remaining work |
| --- | --- | --- | --- |
| I / 1–3 | Establish the byte-transport baseline for a measurement peer | Build EchoPair; use a bounded peer to send a measurement-shaped byte sequence, then verify identical returned bytes and independent peers. Name the absence of domain acceptance. | Existing ch01/ch03 labs pass; reuse their procedures and give the payload its running-project purpose. No gateway parser is claimed yet. |
| II / 4–5 | Give accepted measurements one owner | Build a focused experiment against the canonical measurement model; accept two inputs and observe local sequence 1,2, then remove one observer and verify only the remaining observer fires. Explain how this will be called from event-loop callbacks. | Existing ch37 model labs provide the model/lifetime basis; add earlier explanations and objective mapping without requiring the later architectural chapter. This is model execution, not a proof of runtime scheduling. |
| III / 6–8 | Select an endpoint for a local measurement producer | Run the same bounded echo exchange over a loopback IP endpoint and a temporary Unix path; inspect actual peer/local identities and endpoint cleanup. | Reuse EchoPair context/factory in thin family test drivers. Add public fixtures and expected observations. Bluetooth chapter also needs a hardware-independent address/service-selector lab; a physical RFCOMM/L2CAP exchange is an additional explicitly equipped lab. |
| IV / 9–11 | Define and transfer input framing | Build the existing line protocol; send fragmented and coalesced lines over IPv4 and Unix-domain carriers and compare reconstructed replies. Reject the assumption that one write is one message. | Reuse LineProtocol source and the existing worked transfer in old 15:295; add bounded public solution scripts and assert identical protocol outcomes. MiniGateway's CSV domain parser stays in the later extension. |
| V / 12–13 | Make the role reproducible and diagnosable | Run the echo precedence experiment with source, file, and CLI values; compare effective configuration and scoped diagnostics. Expected CLI override wins, and a rejected endpoint is identified at the relevant scope. | Existing old 17:512 and SemanticLogging; add a mapped public lab with isolated configuration, rather than three separate precedence explanations. |
| VI / 14–15 | Distinguish secure connection and recovery outcomes | Use a local certificate fixture and controlled peer: trusted name succeeds, wrong name fails; stop/restart the peer and distinguish retry before establishment from reconnect afterwards. Bound the run time and capture each observed status. | Existing TLS/recovery teaching and test techniques; public fixture/harness work remains. Never treat a connected TCP socket as authenticated TLS or delivered application data. |
| VII / 16–19 | Observe one accepted state through web interfaces | Run the SSE measurement example: POST twice, compare status with ordered SSE events, disconnect one observer, and verify the other continues. Run the WebSocket echo negotiation check separately. | Existing ch23 labs pass; reuse them for the running state/observer milestone. New 19's lab completes the Part by checking upgrade/subprotocol behavior, without inventing WebSocket state ownership. |
| VIII / 20–22 | Add message-broker integration deliberately | Use a local test broker and a controlled subscriber with MQTT-ClientRole; observe the publication at the subscriber and distinguish connection, session, subscription, and delivery. Record the selected boundary map. | Existing client source and old 25/27 teaching; provide an isolated broker fixture and explicit readiness/timeout checks. The passing sample labs do not supply broker-delivery evidence. |
| IX / 23–24 | Distinguish accepted state from durable state | Run MariaDB-Minimal against a private disposable schema; record a successful committed write, restart the client, and read it back. Contrast the in-memory model restart. Apply the observation to MQTTStore's storage/projection role. | Existing MariaDB-Minimal and MQTTSuite trace; public database setup/cleanup and a deterministic lab remain to be supplied. No credentials or external production database required. |
| X / 25–27 | Reproduce the external application build and test | Build the selected companion consumer against the installed package in a fresh build directory, install the application into a temporary prefix, run its bounded public-interface lab, and identify a deliberately wrong endpoint separately from a build failure. | Existing external CMake examples and lab harnesses; supply reader-facing install/run steps and diagnostic exercise. OpenWrt target deployment remains a separately equipped exercise with its own evidence. |
| XI / 28–30 | Integrate, extend, and justify MiniGateway | Run HTTP/SSE while MQTT is unavailable; add the Unix-domain input and accept mixed inputs into one sequence. Remove/reconnect an observer; verify valid CSV changes state and malformed CSV does not. Explain a chosen process split using new 30's decision tables. | Existing ch35/ch37 labs cover local web/model checks. Add the public extended-input integration lab from the existing MiniGateway-Extended source; a broker-enabled extension has separate subscriber observations. |

All chapters receive 3–5 observable objectives, one recap with at most five
non-tautological bullets, and five exercises: two review, two labs, one design.
Each objective has at least one exercise and every exercise identifies an
objective. Preserve the five samples' already public answers. New review/design
answers and lab commands/expected results go in each chapter's public README;
lab source/fixtures build in CI. Appendix A receives a bounded public-consumer
extension experiment using existing companion abstractions, plus a source-reading
exercise, without requiring changes to the framework. The epilogue's hands-on
exercise reruns and explains an integrated checkpoint; it need not add another
production program. Record all mappings in the evolving chapter ledger.

## Risks to the cumulative path and safeguards

| Risk | Consequence | Required safeguard |
| --- | --- | --- |
| Moving source-reading away from the opening | Learner cannot decode the next public type without the appendix | Retain ≤300 words of the type/header/component path in new 4 and repair old 5's assumed prerequisite. |
| Combining family chapters before connection detail | Callbacks or lifecycle terms arrive before explanation | Use the known echo pair in new 6; put detailed flow/callback reasoning in new 7; keep operational family differences explicit. |
| Runtime chapter becomes a catalogue | Beginners memorize private types without understanding progress | Anchor new 5 in one event-processing sequence and an observable model/lifetime experiment; retain technical constraints. |
| Early milestones become copies of MiniGateway | Competing model, codec, or acceptance implementations drift | Reuse canonical source and thin test drivers; retain one acceptance authority; final construction listings remain intact. |
| MQTT/database/hardware checkpoints need extra setup | Independent learner cannot reproduce an observation | Public local fixture commands, readiness and timeout checks, clear dependencies; hardware-independent mandatory Bluetooth exercise plus explicit optional hardware path. |
| Condensation consumes teaching space | Objectives and labs are appended above budget or prerequisites disappear | Include 450–600 words of apparatus within each unsampled budget; measure after it is present and reread predecessor/successor context. |
| Merge 29–31 loses concrete system distinctions | Final gateway is motivated only by generic advice | Protect build→composition→MQTTSuite trace and unique tool semantics; qualify the Part if that content cannot fit. |
| Final integration is weakened by moving explanations early | Capstone is no longer independently buildable | Keep all original complete listings and build order in new 28; new 29 keeps extension source and explicit unchanged roles. |
| Renumbering passes a range-only check | References resolve to the wrong subject without an error | Track topic anchors and individual migration dispositions; test a valid-but-wrong chapter number. |
| Appendix or epilogue falls outside accounting | Apparent target met by moving text out of measurement | Keep both in ordered manuscript inputs and chapter metrics; include their teaching apparatus and budgets. |

## Execution after approval

Phase 5a moves and joins only the approved material, updates all current references
and publication/build consumers, and introduces the intent-aware reference check.
It may repair transitional sentences and duplicate chapter-opening/closing shells
needed to make a coherent join; prose condensation to budgets and new exercises
belong to the subsequent Part sessions. Preserve all listings and topic/index
anchors during movement. Rebuild all PDFs and the package, run hygiene/alignment,
companion builds and labs, and review changed pagination. Mark 5a qualified if an
identity or cross-reference is unresolved; never treat a successful PDF build as
proof that a reference names the intended topic.

| Session | One Part to condense | Numbered chapter budget | Associated work |
| --- | --- | ---: | --- |
| 5b | I: new 1–3 | 7,850 | That Part opener/checkpoint and public chapter solutions; front matter within 2,500 words |
| 5c | II: new 4–5 | 9,000 | That Part opener/checkpoint and public chapter solutions |
| 5d | III: new 6–8 | 11,050 | That Part opener/checkpoint and public chapter solutions |
| 5e | IV: new 9–11 | 8,800 | That Part opener/checkpoint and public chapter solutions |
| 5f | V: new 12–13 | 8,150 | That Part opener/checkpoint and public chapter solutions |
| 5g | VI: new 14–15 | 6,350 | That Part opener/checkpoint and public chapter solutions |
| 5h | VII: new 16–19 | 11,300 | That Part opener/checkpoint and public chapter solutions |
| 5i | VIII: new 20–22 | 7,400 | That Part opener/checkpoint and public chapter solutions |
| 5j | IX: new 23–24 | 10,100 | That Part opener/checkpoint and public chapter solutions |
| 5k | X: new 25–27 | 11,600 | That Part opener/checkpoint and public chapter solutions |
| 5l | XI: new 28–30 | 8,900 | That Part opener/checkpoint and public chapter solutions; Appendix A (4,700), epilogue (1,900), back matter (1,000), final global audit and proposal pagination |

Part XI owns the associated closing material in the final session; it does not
start a second numbered Part. The shared Part-opening/checkpoint allowance is
1,650 words in total, measured after every Part. Each session rechecks its previous
exit, adds/rereads that Part's mapped pedagogy, and runs the required checks.

The final 5l session also checks total ≤115,000 (planned 112,250), headings ≤550
(planned ≤269), actual average section prose ≥250, text fences ≤250, rules ≤20,
no closing-perspective sections, no forbidden phrases, one recap per chapter,
all objective/exercise mappings and public solutions, and zero PDF warnings/bad
boxes. Refresh the proposal TOC, page counts, evidence sheet, and sample guide
against the final build. No word-budget claim authorizes code-listing cuts.

**Approval has not been given.** Record the author's acceptance or requested
changes to this concrete TOC, budgets, merge boundaries, and milestone sequence
in the work plan before beginning Phase 5a. This Phase 4 session ends here.
