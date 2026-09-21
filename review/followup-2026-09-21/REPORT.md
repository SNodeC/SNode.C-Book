# Four-item refinement pass — 21 September 2026

The four requested items are complete: simple SSE and WebSocket code examples,
Bluetooth preparation in principle, and closure of this pass. The preceding book
refinement was committed first as `884dbfe1ce38e97413d336262e83f72f1e98dcc5`.
The changes preserve the 38-chapter structure, established explanatory style and
depth. There was no shortening target.

The new teaching text is in its corresponding chapter: Bluetooth in Chapter 12,
SSE in Chapter 23, and WebSocket in Chapter 24. Chapter 35's dependent listings
and explanation were synchronized. Both capstone source trees retain the same
model contract, so Chapter 36's comparison remains valid.

## SSE: connection lifetime owns subscription removal

The old publisher discovered disconnected observers only when another measurement
was published. During idle client churn, the listener list retained callbacks and
their captured response objects. The invariant is that the observer's subscription
ends when the HTTP context reports disconnection.

The small publisher now returns a list iterator as the subscription handle.
The route installs the existing `setOnDisconnected(...)` callback and calls
`unsubscribe(...)` with that handle. The callback's owning response reference is
released even if no later measurement arrives. The same correction is applied to
MiniGateway and MiniGateway Extended, including their persistent MQTT listeners.

Explicit removal replaces the boolean callback result and publication-time
pruning; there are no competing cleanup paths. An unused forwarding overload in
the small publisher was removed. No timer, polling mechanism, new framework API,
subscription registry or helper layer was introduced. The full compact program is
now printed in Chapter 23 instead of leaving its publisher implicit.

The source trace covers the Express response facade, HTTP response/context,
registered disconnect callback, and deferred descriptor teardown. The HTTP context
disconnects its underlying response before invoking its disconnect listeners.
The application publisher/model lives across the event loop. These examples use
one event-loop thread and listeners that do not modify the list during publication.
A silent network failure still requires transport detection or the configured
timeout; callback cleanup does not claim instantaneous knowledge of a vanished peer.

## WebSocket: echo bytes and message type

The original echo accumulated bytes but sent them through the text-only string
overload. It therefore changed a binary message into text. The invariant is that
an echo returns the original payload and its text/binary type.

The server now records the incoming type at message start and uses the existing
`SubProtocolContext::sendMessage(type, data, length)` operation after collecting
the message. This preserves embedded zero bytes and arbitrary binary data.
Redundant clears after completion, error and disconnection were removed; the
buffer is cleared at the next message start and destroyed with the object.
Logging reports a byte count instead of rendering binary payload as text.

The existing whole-message example remains easy to read. A streaming echo would
remove its payload buffer but introduce outgoing-fragment handling into this
lesson. The chosen refinement retains the teaching structure without increasing
production lines. Carrier validation, ping/pong and close handling remain in the
framework. The reply preserves message type and payload, not the original frame
boundaries. The chapter explains the need for a finite receiver message limit
when handling untrusted peers.

## Bluetooth: prerequisites and preparation

Chapter 12 now explains compatible controllers/adapters and peers, required driver
and firmware support, radio state, BlueZ build dependencies, and a running peer
service. It gives a short interactive preparation sequence and explains when
pairing is required. Paired state, authorization/trust, and application-service
readiness are distinguished. Existing valid pairing need not be recreated.

The existing addressing treatment was retained without adding another address,
channel or PSM tour. The new text concerns preparation and diagnosis in principle.
It does not claim a hardware exchange. The platform commands were checked against
[BlueZ's bluetoothctl manual](https://github.com/bluez/bluez/blob/master/doc/bluetoothctl.rst),
the [Adapter API](https://bluez.readthedocs.io/en/latest/adapter-api/) and
[Device API](https://bluez.readthedocs.io/en/latest/device-api/), alongside the current
SNode.C family/build sources and locally installed BlueZ documentation.

## Verification

The source authority remains the author's local `/home/voc/projects/snodec/snode.c`
tree. It is clean at `bb63e8a87aeda88123e8c0d72cb6d298908a9fe6`. All 1,447 captured
file contents still match tree digest
`df2fbdbe844f3368f5ed142973d82c0008a057c13d87dda6b7670e45cc3eacb8`.
The author's intervening commit changed provenance without changing those contents.
No framework files were edited. The existing installation therefore supplies the
same verified implementation used by the earlier framework test run; the 183-test
run is historical evidence and was not represented as newly executed in this pass.

Fresh checks in this pass:

- All companion targets rebuilt successfully against that installation.
- Each SSE program passed three waves of eight idle disconnects, mixing ordinary
  close and reset, while one observer stayed connected. Disconnected response
  owners disappeared without publishing. The remaining observer then received the
  next accepted measurement, and final disconnect released its response as well.
- The identical lifetime probe against checkpoint `884dbfe` detected eight retained
  disconnected responses in each of the three old programs. This establishes that
  the check detects the original defect.
- The unchanged teaching WebSocket client received `hello` and closed normally.
  An independent peer checked text/binary type and exact payload bytes, embedded
  zero/non-UTF-8 binary bytes, empty and successive messages, an 8 KiB payload,
  fragmented text/binary with an interleaved ping, and a normal close handshake.
- Existing bounded companion checks passed for SSE, Extended Unix input, line
  limits and both gateways' MQTT CONNECT bytes. No external broker was used.
- Both printed inline WebSocket classes compiled independently, and their callback
  bodies match their companion counterparts. All 36 marked complete listings,
  source anchors, figure references and source hygiene checks passed.
- The new focused runner was exercised with the relative work-directory form used
  by CI. Workflow YAML parses; the GCC/Clang workflow includes the check and lets
  independent test steps run after another test failure. Remote CI was not run here.

The lifetime probe builds temporary copies with a weak-response observer and a
probe endpoint. That instrumentation never owns a response and does not change
the production subscription path. It makes idle retention observable without
adding a counter or diagnostic route to the teaching applications. The test is
bounded and is not a sustained-load or general leak-freedom claim. All test
processes were stopped.

Logs, exact input identities and test commands are indexed in [evidence.json](evidence.json).
The previous checkpoint's build logs that were inadvertently covered by the broad
`build-*` ignore rule are also retained as tracked evidence; their contents match
the hashes already recorded by that checkpoint's evidence file.

## Accounting and closure

Against checkpoint `884dbfe`:

| Category | Added lines | Removed lines |
|---|---:|---:|
| Companion production C++ | 64 | 67 |
| New focused test support | 304 | 0 |
| CI configuration | 17 | 0 |
| Markdown manuscript | 184 | 80 |

Production C++ decreases by three lines. The lifetime correction decreases by
three; the WebSocket correction is neutral. These are responsibility changes,
not line compression. The manuscript grows from 151,071 to 151,914 whitespace-
delimited source words, including code, tables and index directives. The detailed
[file accounting](change-accounting.json) separates this pass from earlier work.

The [persistent work plan](../EDITORIAL-WORK-PLAN.md) records the author's revised
scope and completion. OpenWrt remains deferred because its integration is not yet
updated and is expected to fail build/install. Broader hardware, database, broker,
MQTTSuite deployment and sustained-load validation is intentionally omitted by
request, not counted as passed. PDF regeneration and visual production review
remain deferred. This closes the four-item pass; it does not declare the book finished.
