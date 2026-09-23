# Accepted framework update — verification complete; refinement remains stopped

Date: 23 September 2026. Authorization: ../FOLLOWUP-06.md.
Source: clean **9746d1862b30a5104d3590aaa4ed79752ba9aa6a**, “Drain asynchronous
logs during shutdown”. The author explicitly accepts this HEAD change.

## Results

| Check | Result | Evidence |
|---|---|---|
| Fresh framework configure/build/install | PASS | framework-configure.log, framework-build.log, framework-install.log |
| Complete configured SNode.C CTest suite | **184/184 PASS**, zero skips | framework-tests.log, framework-tests.xml |
| External installed-package echo | **4/4 PASS**, zero skips | external-echo-tests.log, external-echo-tests.xml |
| Fresh companion configure/build | PASS | companion-build.log |
| All public labs | **50/62 PASS; 12 FAIL**, zero skips | labs.log, labs.xml |
| Teaching smoke | PASS | teaching-smoke.log |
| Behavior smoke | PASS | behavior-smoke.log |
| Example lifetime/echo checks | PASS | lifetime-tests.log |
| Source freeze and book/test preservation | PASS | framework-freeze-before.json, framework-freeze-after.json, preservation.json |

[All 250 individual CTest results](all-tests.md) list every name, status and duration.
The JSON inventories and JUnit files preserve the complete configured test sets.
No internal “SKIP:” messages were found. All three equipped public labs ran.
The test runner did not stop after failures; each independent suite completed.
`results.json` records actual exit codes and start/end times; the labs exit code
is 8. Completion of orchestration does not mean all checks passed.

## What the update fixes

**Inspected:** framework `src/core/EventLoop.cpp:386` calls Logger::shutdown
at the end of free(), after the final shutdown records. In
`src/log/detail/SpdlogBackend.cpp:155–166`, shutdown resets the async worker
logger and thread pool, then flushes the stdout/file sinks.

**Run:** SNodeCAsyncLogDrainTest passes. It queues 4,096 records and checks that
all are present immediately after SNodeC::free() returns, including the final
record (`tests/unit/core/SNodeCAsyncLogDrainTest.cpp:79–93`). The previously
failing EndpointLifetimeCountersTest and InetLegacyClientConnectFailureTest
also pass. The new regression exercises explicit free; it does not establish
that every signal-driven event loop reaches free().

## Remaining failures

Every failing lab raises `RuntimeError: Process did not stop after SIGINT`
after the original five-second grace period:

- `exercise-ch01`
- `exercise-ch01-independent-peers`
- `exercise-ch07-independent-peers`
- `exercise-ch11-part-checkpoint`
- `exercise-ch11-endpoint-failure`
- `exercise-ch13-part-checkpoint`
- `exercise-ch14-secure-echo`
- `exercise-ch16-framing`
- `exercise-ch17-order`
- `exercise-ch24-composition`
- `exercise-ch26-lifecycle`
- `exercise-ch27-diagnosis`

No timeout was increased and no test was modified. The teaching-smoke grace
remains 12 seconds; CTest and nested-process bounds remain at their restored
values. `ci/` and `companion/` exactly match fa62fa1, the pre-adaptation state,
including the separately approved P−1 C++20 requirements.

A separate controlled echo reproduction also hangs after SIGINT; see
sigint-diagnosis.json and sigint-backtrace.log. The echo exchange succeeds.
The debugger records eventLoopState = 3 (STOPPING) and stopsig = 2 (SIGINT)
at sigint-backtrace.log:7–8. Its main-thread backtrace remains inside
EventLoop::_tick → EventMultiplexer::tick → epoll_pwait, with wait timeout
2147483647; the logger worker is waiting on its queue. This capture shows the
remaining hang occurs **before** the new free()/Logger::shutdown drain call.
The signal has been received, but the waiting event loop has not reached cleanup.
It does not establish which thread received the signal in this particular trial.
The diagnostic process was killed after the capture; forced kill was not treated
as successful shutdown. No framework workaround or thread-directed signal was used.

## Provenance and scope

A git archive was exported from the read-only author tree into
`build/shutdown-recheck-9746d186/source`. All 1,448 tracked files match the author
tree byte-for-byte (export-verification.json). Fresh GCC Debug build, tests and
applications enabled; 970 build steps. Installation:
`build/shutdown-recheck-9746d186/install-gcc`. The companion CMake cache selects
that installation. Framework and lab test commands are recorded in their logs;
run.py records orchestration and diagnose-sigint.py records the separate reproduction.
No prior installation supplies these results.

Before/after source freezes are identical. Manuscript, ci and companion contents
are unchanged by this verification, as checked against book-input-hashes-before.json.
No production or test code changes: +0/−0. New files are review/evidence support only.
The incomplete P1 vocabulary work remains uncommitted and is not certified here.

The recorded book source baseline remains 8b8da56; no pin, manifest, claim anchor,
manuscript or publication artifact was silently re-baselined. That reconciliation
belongs to an explicitly resumed refinement run. No publication rebuild or hosted
CI run was requested or claimed.

**Outcome:** verification complete; book refinement remains stopped as instructed.
Framework tests pass, but the remaining signal-shutdown lab failures prevent an
all-green entry check. No additional repair or refinement was attempted.
