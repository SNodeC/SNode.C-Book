# Exercise shutdown investigation — 9746d186

Date: 2026-09-23. Scope: investigate the failing exercises against the accepted
framework; no repairs, timeout changes or manuscript refinement. The author's
source tree is read-only. Source HEAD is
9746d1862b30a5104d3590aaa4ed79752ba9aa6a. All reproductions use the fresh
`build/shutdown-recheck-9746d186/install-gcc` installation.

## Conclusion and invariant

A framework signal-delivery/wake-up defect is reproduced with an unchanged public
EchoPair binary. A process-directed SIGINT can run its handler on the asynchronous
logging worker. The event-loop thread can then remain in its normal descriptor
wait instead of reaching shutdown. The required invariant is: accepting a stop
signal must make the event-loop owner leave its normal wait and enter shutdown,
without requiring a later client connection or unrelated timer.

The 12 failures in the complete preceding lab run all report the original
five-second SIGINT cleanup timeout. None reports an earlier exercise-body
assertion or JSON-decoding exception. This is evidence of one common failure
surface, not proof that every one of those historical processes had precisely the
same thread interleaving. The new trace below directly establishes that
interleaving for EchoPair; the focused lab rerun supplies further evidence.

## Direct reproduction and causal probe

Run `python3 review/pedagogical-smoothing-2026-09-23/shutdown-investigation-9746d186/trace-signal.py`
from the book workspace. The script does not import or change any lab driver. It
starts the built canonical echo server, verifies an exact 14-byte echo, closes
the peer, and sends `kill(pid, SIGINT)`, just like the public harness. Log level 0
also removes a large pending-log backlog as an explanation for this reproduction.

Four trials were run: three exited normally; the fourth stalled beyond five
seconds. `signal-trials.json` records the command, PIDs, times and results.

- Main thread 1083472 entered a 2147483647 ms `epoll_pwait` at
  1790170365.663081 (`trial-3.1083472:39`). The call did not finish until the later
  listener probe. With `strace -ttt`, the printed syscall timestamp is its entry
  time; the following mask restoration is at 1790170370.667167, line 40.
- Worker thread 1083473 received the process-directed SIGINT at
  1790170365.662658 (`trial-3.1083473:2`). The sender is the Python diagnostic
  process, not a thread-directed signal or a debugger injection.
- At the five-second deadline, `/proc` showed main in `do_epoll_wait`, worker in
  `futex_do_wait`, and no pending SIGINT. Both thread snapshots are retained in
  `signal-trials.json`.
- A diagnostic TCP connection at 1790170370.663382 woke the listener. The process
  exited at 1790170370.674212 with status 254, without another signal. This probe
  is evidence that descriptor activity releases the stall; it is not a lab fix
  and is not counted as a successful five-second shutdown.
- The earlier untraced reproduction independently captured `eventLoopState = 3`
  (STOPPING) and `stopsig = 2` (SIGINT), main in epoll, and the worker waiting on
  its spdlog queue: `../shutdown-recheck-9746d186/sigint-backtrace.log:7` onward.
  That earlier capture alone did not identify the signal recipient; this trace
  fills that evidence gap.

The wait argument is roughly 24.9 days, although descriptor activity can end it
sooner. Increasing a five-second grace to a minute would not restore the missing
wake-up guarantee. The latest log-drain fix is downstream of the observed stall.

## Source path and responsibility

Line references in this section are relative to the read-only framework tree:
`/home/voc/projects/snodec/snode.c`.

1. `src/core/EventLoop.cpp:279` starts the async logger before entering `_tick`.
   `src/log/detail/SpdlogBackend.cpp:143` constructs one spdlog worker. There is no
   framework signal-mask policy around that construction. The actual worker's
   unblocked mask is also observed in `trial-3.1083473:1`.
2. `src/core/EventLoop.cpp:213` blocks shutdown signals in the calling event-loop
   thread while dispatching; it does not block them in an already-created worker.
   The epoll call temporarily restores the caller's old mask. Thus the worker is
   an eligible recipient while the event-loop thread is masked.
3. `src/core/EventLoop.cpp:389` handles the signal, records `stopsig`, and calls
   `stop()`. `stop()` at line 331 only assigns STOPPING; it provides no descriptor
   wake-up or handoff to the event-loop owner.
4. `_tick` at line 215 permits both RUNNING and STOPPING. The outer loop tests
   RUNNING only after `_tick` returns (line 286). A stop handled on another thread
   therefore need not interrupt the owner's current/next descriptor wait.
5. `src/core/EventMultiplexer.cpp:132` chooses the wait from resources and the
   requested tick timeout, with no independent stop wake-up. The epoll backend
   calls `epoll_pwait` at `src/core/multiplexer/epoll/EventMultiplexer.cpp:127`.
6. `EventLoop::free()` starts at line 335 and `Logger::shutdown()` runs at line
   386. `SpdlogBackend.cpp:155` joins/drains the worker and flushes sinks. The
   observed hang precedes these operations; no failed drain is established here.

The correction belongs to framework signal ownership and event-loop wake-up,
not an exercise-specific sleep or a different cleanup signal. Simply rejecting
STOPPING in `_tick` would also affect the intentional shutdown-drain ticks in
`free()` (EventLoop.cpp:363–372); any framework repair must preserve that path.
No repair has been implemented or selected in this investigation.

## Each failure in the complete 62-lab run

Evidence: `../shutdown-recheck-9746d186/labs.xml`, its verbose `labs.log`, and the
unchanged drivers below. The traceback calls `contextlib.__exit__` at line 148,
its normal-body-return path, rather than showing an earlier body exception.
The shared failure is `companion/exercises/lab_support.py:45–51`: send SIGINT,
wait five seconds, kill for cleanup and report failure. A forced kill is not
accepted as a pass.

| Failed test | Observation reached before cleanup | Not established by that run / driver |
|---|---|---|
| exercise-ch01 | SNode.C echoed all 20,480 binary bytes and accepted a later connection. | Its shutdown failed; the following Asio comparison was not reached. `ch01/solution.py:11–23`. |
| exercise-ch01-independent-peers | Active peer echoed while a second peer was idle and after that peer closed. | SNode.C shutdown failed; Asio iteration was not reached. `ch01/independent-peers.py:11–18`. |
| exercise-ch07-independent-peers | Same peer-isolation assertions, through the shared ch01 driver. | Graceful shutdown not established. `ch07/CMakeLists.txt`, `ch01/independent-peers.py:11`. |
| exercise-ch11-part-checkpoint | IPv4 protocol passed 26 segmentations, CRLF/empty/unknown commands, QUIT and partial-prefix silence. | IPv4 cleanup failed before the Unix iteration and cross-family equality assertion. `ch09/protocol.py:107–113`. |
| exercise-ch11-endpoint-failure | Missing Unix path failed before protocol; valid peer returned command error then PONG. | Owned socket-path removal after shutdown was not checked. `ch09/protocol.py:38–39,125–136`. |
| exercise-ch13-part-checkpoint | Configuration precedence/help/invalid-port checks passed; global-Error run echoed and its log snapshot parsed. | First server shutdown failed before scoped overrides and final logging assertions. `ch12/configuration.py:53–81`. |
| exercise-ch14-secure-echo | Trusted sensor.example, exact binary TLS echo and reciprocal close_notify passed. | Whole server SIGINT shutdown failed. TLS session closure and server termination are distinct. `ch14/tls.py:28–38`. |
| exercise-ch16-framing | Incomplete headers caused no handler/response; completion yielded one correct HTTP 200. | Server SIGINT shutdown failed. `ch17/dispatch.py:33–47`. |
| exercise-ch17-order | Mounted route visited app/router/handler; outside route visited app only and returned 404. | Server SIGINT shutdown failed. `ch17/dispatch.py:59–66`. |
| exercise-ch24-composition | Reuses framing mode; same incomplete/complete-header assertions passed. | Server SIGINT shutdown failed. `ch24/CMakeLists.txt`, `ch17/dispatch.py:33–47`. |
| exercise-ch26-lifecycle | Fresh Release consumer build/install and first echo/shutdown/refused-connection check passed; second process echoed. | Second shutdown failed, so its refused-connection check and final PID comparison were not reached. `ch26/installed.py:54–74`. |
| exercise-ch27-diagnosis | Missing-component diagnosis, canonical consumer build/echo, fresh installed consumer, correct-endpoint echo and wrong-endpoint refusal passed. | Final installed server shutdown failed. `ch26/installed.py:89–100,118–126`. |

Paths in the table are under `companion/exercises/`. The public Express fixture's
APP/ROUTER/HANDLER observations use flushed `std::cout`, not asynchronously queued
spdlog records (`ch17/dispatch.cpp`). They are not failures to await spdlog output.

A separate, still-open driver concern remains in the logging checkpoint:
`ch12/configuration.py:71` snapshots asynchronous output before shutdown. The
source drain guarantee applies when `free()` returns, not at the instant an echo
is received. That race was already recorded historically and its adaptation was
reverted at the author's request. The preceding 62-lab run did not reach the
positive scoped-log iteration, so it cannot certify or disprove that issue.
No timing adaptation has been reinstated.

## Why the other suites passed

The preceding full verification remains: framework **184/184**, external echo
**4/4**, public exercises **50/62**; teaching, behavior and lifetime suites PASS.
Those suites were not all rerun here. All individual results are preserved in
`../shutdown-recheck-9746d186/all-tests.md`.

- `tests/unit/core/SNodeCAsyncLogDrainTest.cpp:81–93` emits 4,096 records, calls
  `SNodeC::free()` directly and checks their presence. It verifies the new drain
  guarantee, not entry into shutdown from an externally signalled idle listener.
- Signal cases in `StreamFrameworkShutdownTest.cpp:599–614` and
  `TLSFrameworkShutdownTest.cpp:567–573` trigger SIGTERM from a framework timer
  and use `start(Timeval({1,0}))`. A one-second wait ceiling allows progress even
  when a signal does not interrupt the waiting owner. These passing cases do not
  prove the default long-wait path is safe.
- Framework external echo uses SIGTERM, different timing and its own harness
  (`examples/echo/tests/echo_tests.py:47`). Server/client return-code assertions
  reject SIGKILL. Its four passes are real, but a single successful interleaving
  does not disprove this race; three of four new minimal trials also passed.
- Teaching smoke sends SIGINT and fails a timeout, with its original 12-second
  grace (`ci/run-teaching-smoke-tests.py:44–61`). Its successful run establishes
  that invocation only, not that a longer grace fixes the observed lost wake-up.
- Behavior smoke's `ManagedProcess.stop()` sends SIGTERM, then permits SIGKILL
  after three seconds without marking that cleanup as a failure
  (`ci/run-behavior-smoke-tests.py:54–68`). Lifetime tests use that same helper
  (`ci/run-example-lifetime-tests.py:142,178,184,199`). Their PASS results certify
  their functional assertions, not universal graceful termination. No claim is
  made that those particular passing processes required forced kill: the earlier
  logs do not distinguish the cleanup path.

## Repair verification that is missing

A framework regression should exercise a real listener with the normal default
wait, an active async worker, an external process-directed SIGINT after peers
close, and no subsequent traffic. It must verify bounded normal exit, correct
signal result and drained accepted log records, including repeated delivery
windows. Reducing an event-loop timeout in that test would conceal this specific
missing wake-up. This is a proposed coverage requirement, not a test change.

## Focused rerun of all 12 previously failing exercises

Executed the existing CTests under syscall tracing, with all original drivers,
assertions, timeout properties and five-second SIGINT grace unchanged. Exact
command and installation environment: `failing-labs-command.json`. CTest exit 8;
verbose output and JUnit: `failing-labs.log`, `failing-labs.xml`.

| Exercise | Traced rerun | Seconds |
|---|---|---|
| exercise-ch01 | PASS | 0.335038 |
| exercise-ch01-independent-peers | FAIL | 5.20097 |
| exercise-ch07-independent-peers | FAIL | 5.15474 |
| exercise-ch11-part-checkpoint | PASS | 0.568171 |
| exercise-ch11-endpoint-failure | PASS | 0.167281 |
| exercise-ch13-part-checkpoint | FAIL | 5.54578 |
| exercise-ch14-secure-echo | PASS | 0.30771 |
| exercise-ch16-framing | PASS | 0.343838 |
| exercise-ch17-order | PASS | 0.163444 |
| exercise-ch24-composition | PASS | 0.329513 |
| exercise-ch26-lifecycle | PASS | 8.07098 |
| exercise-ch27-diagnosis | FAIL | 19.0075 |

**8/12 pass; 4/12 fail**, all four on the same SIGINT timeout. Tracing changes
scheduling; these results do not replace the preceding full suite's 50/62 result
or establish a failure rate. The eight passes confirm those exercises can
complete unchanged on this source. They do not certify an intermittent race fixed.

Each new failure has direct recipient/wait evidence in `failing-labs.strace`:

| Exercise | Main TID | Worker TID | Evidence lines: worker creation; SIGINT; worker handler return; main wait; forced kill |
|---|---:|---:|---|
| ch01-independent-peers | 1084168 | 1084169 | 56; 66; 68; 67–70; 69 |
| ch07-independent-peers | 1084214 | 1084215 | 90; 100; 101; 102–104; 103 |
| ch13-part-checkpoint | 1084258 | 1084259 | 538; 545; 547; 546–549; 548 |
| ch27-diagnosis | 1084771 | 1084772 | 2940; 2950; 2953; 2952–2955; 2954 |

In ch07 the worker has even returned from the signal handler before main enters
the blocking epoll call. SIGINT was neither missing nor still waiting for its
handler. All four handler returns precede the eventual forced kill; this rules
out a handler that itself remains deadlocked in these captured failures.

## Status and preservation

- Investigation complete; framework signal/wake-up defect remains open.
- The prior complete suite had failures only in public exercises. That does not
  establish that the framework is defect-free; the exercises expose a gap not
  excluded by the passing tests.
- Qualified: a common shutdown cause is strongly supported for all 12 prior
  failures; exact interleavings were captured for four failing CTests and the
  separate echo reproduction, not every prior process.
- Open: scoped-log observation timing in the restored ch13 checkpoint remains
  unverified behind its first shutdown failure.
- Book refinement stays paused. No framework repair, new timeout, alternate
  signal, revised assertion or manuscript edit is part of this investigation.
- Production and existing test code changes: **+0/−0**. Added Python is diagnostic
  evidence support only. No API or publication change; no broad test-suite rerun
  beyond the focused twelve is claimed.
- `preservation.json` verifies source freeze equality with the preceding run,
  tracked manuscript/ci/companion hashes unchanged, and restored tests equal fa62fa1.
  Existing uncommitted P1 work is preserved.

The previous broad snapshot also included ignored `companion/build/Desktop_GCC-Debug`
artifacts. Twenty-five of those build outputs differ now; all differences are
listed in `preservation.json`. This investigation neither used nor rebuilt that
directory. Their provenance was not investigated. The tracked source files and
all manuscript inputs match; no broad all-files-preserved claim is made.
