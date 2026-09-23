# R2 claim review — 07ca9a29

Scope: 9746d186 drains asynchronous logs during shutdown; 55c36e41 keeps
process-signal handling on the event-loop thread; 07ca9a29 simplifies logging
synchronization. Inspected the diffs and current EventLoop.cpp/.h, Logger.cpp/.h
and detail/SpdlogBackend.cpp/.h. Source inspection below is separate from the
fresh build/runtime evidence in R2-build/. No framework investigation or repair.

## Changed behavior and local correction

| Book claim (pre-split paths under manuscript/chapters) | Frozen source | Verdict |
|---|---|---|
| 05-core-runtime-and-event-processing.md:89, dispatch in RUNNING or STOPPING | src/core/EventLoop.cpp:224 | Corrected locally: RUNNING requires no pending stop signal; STOPPING still dispatches. |
| Same paragraph: public tick requires INITIALIZED; use start for examples | src/core/EventLoop.cpp:244, 298 | Still true; no change. |
| 05-core-runtime-and-event-processing.md:85–87, start controls progression and iteration timeout | src/core/EventLoop.cpp:275–320 | Still true. |
| 05-core-runtime-and-event-processing.md:102, reconfigure is a running-thread operation | src/core/EventLoop.cpp:343 | Still true. |
| 05-core-runtime-and-event-processing.md:234–246, coordinated bounded cleanup and non-vetoing signal callback | src/core/EventLoop.cpp:359–406; src/core/socket/stream/SocketConnection.hpp:345–357 | Still true; stoponsig now only records the signal at EventLoop.cpp:409; _tick logs it and calls stop at 228–234. No old handler-side execution claim exists to replace. |
| 09-writing-socketcontext-classes-well.md:114–116, 172, 226, 348, signal-close response and transport cleanup | src/core/socket/stream/SocketConnection.hpp:345–357, 394–413; companion/examples/LineProtocol-Server/LineCommandServerContext.cpp | Still true: context handles protocol closure; callback result does not veto cleanup. |
| 14-tls-across-the-framework.md:178–189, close-notify, bounded shutdown, idempotence and signal callback | src/core/socket/stream/SocketConnection.hpp:345–357; src/core/socket/stream/tls/TLSShutdown.cpp:450–475 | Still true; TLS source is byte-identical to prior pin. |
| 15-timeouts-retries-and-failure-modes.md:33–70, 217, 241–275, shutdown limits and queue behavior | src/core/socket/stream/SocketClient.h:221,269; src/core/socket/stream/FlowController.hpp:74; unchanged stream/TLS sources | Still true; stop does not redefine retry/reconnect or queue admission. |
| 27-testing-debugging-and-benchmarking.md:165, tests cover stopping from callbacks | tests/component/core/; src/core/EventLoop.cpp:353 | Still true; no total test count or handler-side shutdown promise. |
| 27-testing-debugging-and-benchmarking.md:239, 293, 353, timeout evidence, service shutdown and lifetime transitions | src/core/EventLoop.cpp:359–406; tests/component/core/ | Still true; these prescribe observable checks, not unverified deployment success. |
| 13-logging-diagnostics-and-runtime-introspection.md:233–235, startup deferral, worker and visibility | src/core/EventLoop.cpp:298–321, 355–357, 406; src/log/detail/SpdlogBackend.cpp:161–192 | Still true. free ends with Logger::shutdown, which joins the worker then flushes sinks; waiting for orderly process completion remains valid. |
| 13-logging-diagnostics-and-runtime-introspection.md:287–311, borrowed bytes copied before return, disabled early return, worker formatting and queue backpressure | src/log/SemanticLogger.cpp:728; src/log/detail/SpdlogBackend.cpp:270–299 | Still true. One worker and captured sink ownership remain; no arbitrary multithreaded logging-API guarantee is claimed. |
| companion/exercises/ch12/configuration.py:64–89, completed log after normal shutdown | src/core/EventLoop.cpp:406; src/log/Logger.cpp:72; src/log/detail/SpdlogBackend.cpp:182–192 | 2e71f2a fix carried forward unchanged; assertions and original grace preserved. |

## Shutdown-output sweep

Searched the entire manuscript for log/output paired with shutdown, exit,
termination, drain or flush, plus asynchronous/synchronous logging, worker and
signal-handler terms. Other hits are diagnostic guidance (07:325, 09:348,
13:30, 14:220, 27:293, Appendix A:275), a protocol signal log (28:954), or
HTTP framing (15:275), and make no false delivery claim. All retained unchanged.
The logging chapter's 235 and 296 are the substantive output-timing claims,
reviewed above. No claim says a returned log call has synchronously written its
record. No additional local correction is required.

## Carried-forward source contracts

Compared every registered anchor file with the previous manifest. Contracts
whose anchors all remain byte-identical are carried forward; all anchor needles
were also checked at their recorded lines. Changed-file contracts are reviewed
above. This does not relabel historical runtime results as new evidence.

- Chapter 1: all registered source files byte-identical; contract carried forward.
- Chapter 2: all registered source files byte-identical; contract carried forward.
- Chapter 3: all registered source files byte-identical; contract carried forward.
- Chapter 4: all registered source files byte-identical; contract carried forward.
- Chapter 5: reviewed above: src/core/EventLoop.cpp.
- Chapter 6: all registered source files byte-identical; contract carried forward.
- Chapter 7: all registered source files byte-identical; contract carried forward.
- Chapter 8: all registered source files byte-identical; contract carried forward.
- Chapter 9: all registered source files byte-identical; contract carried forward.
- Chapter 10: all registered source files byte-identical; contract carried forward.
- Chapter 11: all registered source files byte-identical; contract carried forward.
- Chapter 12: all registered source files byte-identical; contract carried forward.
- Chapter 13: all registered source files byte-identical; contract carried forward.
- Chapter 14: all registered source files byte-identical; contract carried forward.
- Chapter 15: all registered source files byte-identical; contract carried forward.
- Chapter 16: all registered source files byte-identical; contract carried forward.
- Chapter 17: all registered source files byte-identical; contract carried forward.
- Chapter 18: all registered source files byte-identical; contract carried forward.
- Chapter 19: all registered source files byte-identical; contract carried forward.
- Chapter 20: all registered source files byte-identical; contract carried forward.
- Chapter 21: all registered source files byte-identical; contract carried forward.
- Chapter 22: all registered source files byte-identical; contract carried forward.
- Chapter 23: all registered source files byte-identical; contract carried forward.
- Chapter 24: all registered source files byte-identical; contract carried forward.
- Chapter 25: all registered source files byte-identical; contract carried forward.
- Chapter 26: all registered source files byte-identical; contract carried forward.
- Chapter 27: all registered source files byte-identical; contract carried forward.
- Chapter 28: all registered source files byte-identical; contract carried forward.
- Chapter 29: all registered source files byte-identical; contract carried forward.
- Chapter 30: all registered source files byte-identical; contract carried forward.
- Chapter A: all registered source files byte-identical; contract carried forward.
