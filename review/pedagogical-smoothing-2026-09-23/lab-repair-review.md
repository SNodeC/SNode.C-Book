# Lab-driver repair under Follow-ups 03 and 04

Invariant: a live asynchronous log is not a completed observation until the
expected complete record arrives. A successful network exchange does not imply
that its diagnostic output is already visible. Normal SIGINT must still produce
a graceful exit; a forced kill remains a test failure.

## Repairs and scope

- `companion/exercises/lab_support.py`: SIGINT grace 5 → 60 seconds. The teaching
  smoke harness changes 12 → 60. CTest process-lab limits below 180 become 180;
  existing 300-second consumer build limits and short model tests are retained.
- Nested checkpoint subprocess bounds in ch19/solution.py, ch20/mqtt.py and
  ch23/database.py change 35/40 → 150 seconds, allowing the inner grace period.
- Move the existing MQTT `wait_log` to shared lab support and require a complete
  newline-terminated matching record. Configuration and WebSocket observations
  reuse it. This replaces the separate configuration polling loop. All existing
  content, count, identity, negative and exit assertions remain.
- `ch15/recovery.py:14`: parse complete JSON records while the producer is alive;
  an unfinished tail is retried by the existing poll. Invalid complete JSON
  still fails. No new application code, signal workaround or framework changes.

## Executed evidence

`P0b-labs-resume.log`: 51/62 pass after the grace change, 11 fail on SIGINT
shutdown at about 60 seconds. The failure set differs from the earlier run,
consistent with scheduling sensitivity. No log-content assertion fails in this
run. All 62 execute. `P0b-resume-results.json`: all 12 other check groups pass.

`lab-observation-regression.log`: 3/3 pass: delayed complete record, missing
record failure, and partial JSON versus malformed complete JSON. Test support
is in `ci/test-lab-observations.py`.

`lab-driver-repair-ctest.log`: 11/12 focused integration tests pass against the
new 8b8da56 installation, including recovery, WebSocket, MQTT, database and
nested checkpoints. The configuration/logging checkpoint still fails during
the quiet process's SIGINT shutdown before it reaches the scoped-log assertion.
That assertion's integration validation remains qualified, not claimed passing.
`lab-repair-source-alignment.log` and `lab-repair-hygiene.log` pass.

## Shutdown cause, inspected separately

`lab-quiet-shutdown-backtrace.log:7–8` records eventLoopState = 3 (STOPPING) and
stopsig = 2 (SIGINT) while the main thread remains in epoll_pwait with timeout
2147483647 and the logger worker waits on its queue. The enum is in framework
`src/core/State.h:51`. The state transition is `src/core/EventLoop.cpp:331–333`;
the handler records the signal and calls stop at lines 387–392. `_tick` blocks
signals on the event-loop thread at lines 205–213 and may then enter the wait
for either RUNNING or STOPPING at lines 215–216. The async worker is created
without a signal-mask policy at `src/log/detail/SpdlogBackend.cpp:142–143`.

The signal was received; this is not merely a five-second grace period. The
blocked event loop has no wake-up from the state assignment. The separate
strace trials show SIGINT can be delivered to the logger worker; those trials
exit when concurrent descriptor activity wakes the main thread. The backtrace
plus source establish the missing wake-up; they do not identify the exact
receiving thread in the untraced hung trial. No thread-directed signal or extra
network wake-up was added to the drivers to conceal it.

The frozen tree remains unchanged (`framework-freeze-lab-repair.json`). Per the
author's continuation instruction, this framework issue stays qualified and
does not stop the editorial run. The two framework CTest log-visibility failures
also remain unchanged and qualified.

Accounting against R evidence: production C++ +0/−0; existing test/build support
+54/−59 (net −5); new regression test +49/−0. No application behavior or listed
source file changed. The refreshed package build passes in lab-repair-package.log.
