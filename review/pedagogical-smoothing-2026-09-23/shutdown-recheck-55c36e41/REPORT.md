# Framework signal fix — all requested runtime checks pass

Date: 2026-09-23. Author instruction: ../FOLLOWUP-08.md.
Source: clean **55c36e418a831573ac9b5284830f4bd0d5074bac**, “Keep process signals
on event-loop thread”. Verification only; no manuscript refinement or repairs.

## Results

| Check | Result | Evidence |
|---|---|---|
| Fresh framework configure/build/install | PASS; 970 build steps | framework-configure.log, framework-build.log, framework-install.log |
| Complete configured framework CTests | **185/185 PASS**, zero skips | framework-tests.log, framework-tests.xml |
| External installed-package echo | **4/4 PASS**, zero skips | external-echo-tests.log, external-echo-tests.xml |
| Fresh companion configure/build | PASS; 114 build steps | companion-build.log |
| All public exercises | **62/62 PASS**, zero skips | labs.log, labs.xml |
| Teaching smoke | PASS | teaching-smoke.log |
| Behavior smoke | PASS | behavior-smoke.log |
| Example lifetime/echo checks | PASS | lifetime-tests.log |
| Repeated idle-listener SIGINT diagnostic | **100/100 PASS**; maximum observed shutdown **7.74 ms**, median **3.35 ms** | sigint-stress.json, sigint-stress-summary.json |
| Source and book-input preservation | PASS | framework-freeze-before.json, framework-freeze-after.json, final-preservation.json |

[All 251 CTest results](all-tests.md) list every test and duration. No internal
SKIP messages were found, and all three equipped exercises executed and passed.
`results.json` records actual exit codes and start/end times for every suite.
These are local results; no hosted CI run is claimed.

All twelve exercises that failed against 9746d186 now pass without changes.
The ch13 checkpoint reaches its positive scoped-record assertions and passes
(`labs.log:347–356`); the earlier first-shutdown failure no longer prevents them.
This passing observation does not establish that an arbitrary asynchronous log
snapshot before shutdown is guaranteed complete.

## What changed, and why it addresses the traced hang

Inspected against the author's read-only tree at `/home/voc/projects/snodec/snode.c`:

- `src/log/detail/SpdlogBackend.cpp:41–64,170–174` blocks signals around worker
  creation and then restores the creator's mask. The worker inherits blocked
  signals, preventing the process-directed SIGINT from running its handler there.
- `src/core/EventLoop.h:106` makes stopsig a volatile sig_atomic_t.
  `src/core/EventLoop.cpp:409–410` restricts the handler to recording the signal;
  it no longer logs or changes event-loop state inside the signal handler.
- `src/core/EventLoop.cpp:222–239` uses pthread_sigmask, checks a recorded signal
  before entering a normal wait, and performs logging and STOPPING transition
  on the event-loop thread. Intentional STOPPING cleanup ticks remain permitted.
- The earlier log-drain fix remains at `src/core/EventLoop.cpp:406`.
  SNodeCAsyncLogDrainTest still passes its 4,096-record verification after free().

The new `ShutdownReceiverNotification_signal-wait` test passes in approximately
0.11 seconds (`framework-tests.log:645–650`). It sends SIGINT from a child
process while the event loop has a five-second wait and requires completion in
under two seconds, plus exactly one shutdown notification and correct signal
metadata/result (`tests/component/core/ShutdownReceiverNotificationTest.cpp:91–131`).
The source change inspected is preserved in `source-change.diff`.

## Rechecking the previous reproduction

`sigint-stress.py` executes 100 fresh canonical EchoPair processes from the new
installation. Each trial verifies an exact binary echo, closes the peer, then
sends process-directed SIGINT. Fifty trials disable logging and fifty retain the
default logging policy. Delays after peer closure alternate between 0, 2 and
10 ms. Every observed worker mask blocks SIGINT; masks are recorded per trial.

The event loop uses its normal default wait. Every trial retains the original
five-second process-exit deadline, receives no later wake-up connection or second
signal, and exits normally with status 254. All 100 pass; no diagnostic forced
kill or debugger capture was required. The duration includes Python's process
wait/polling overhead and is an observed bound for these trials, not a latency
benchmark or proof about every possible application/thread configuration.

The previous lost-wake-up failure no longer reproduces in these checks. Unlike
the preceding 9746d186 investigation, no listener probe was needed to release a
stalled process. The behavior/lifetime helpers still permit forced cleanup, so
their PASS alone is not used to establish graceful shutdown; the unchanged public
lab harness and dedicated 100-run diagnostic enforce it directly.

## Provenance and scope

A fresh git archive was exported into `build/shutdown-recheck-55c36e41/source`.
All 1,448 tracked files match the author tree byte-for-byte. Tree digest:
`94947beddc313d745c6e28445d6a9875068eb7be776a3c8edc1397fc5c6d5843`.
See export-verification.json. GCC Debug, framework tests and applications enabled;
installation: `build/shutdown-recheck-55c36e41/install-gcc`. Framework and companion
build directories are fresh. Every runtime suite uses that installation.
`run.py` and the logged commands record the collection method.

The author tree remains clean at the same HEAD, with identical before/after
freezes, including after the stress diagnostic. Tracked and non-ignored
manuscript/ci/companion files have identical before/after hashes. Ignored local
build outputs are excluded from this preservation measure. `ci/` and `companion/`
remain identical to fa62fa1, the restored pre-adaptation state. No existing test,
assertion, timeout, framework or manuscript file was changed: production and
existing test code changes **+0/−0**. New Python files are review diagnostics only.

**Outcome:** verification complete; no failed or skipped runtime check in this
run. No outstanding runtime failure was reproduced. The book's recorded source
baseline is still 8b8da56; this check does not silently update its pin, manifest
or source-claim anchors. Reconciliation and the incomplete P1 editorial work
remain pending an explicit refinement resumption. No PDF/package rebuild or
full editorial gate check was requested or claimed. Stop after reporting.
