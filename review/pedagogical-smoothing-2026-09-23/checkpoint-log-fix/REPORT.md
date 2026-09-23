# Fix ch13 checkpoint log observation — complete

Date: 2026-09-23. Author authorization: ../FOLLOWUP-10.md. The follow-up requires
usage and APIs to remain unchanged. Scope is the exercise verification driver,
not framework or example/lab implementation changes.

## Change and invariant

Only `companion/exercises/ch12/configuration.py` changes among ci/companion files.
Although stored under ch12, its checkpoint mode is registered as
`exercise-ch13-part-checkpoint` by `companion/exercises/ch13/CMakeLists.txt`.

The violated invariant was that assertions about a complete asynchronous log
must inspect it after the producer has finished and shutdown has drained records.
The old driver saved the file snapshot before normal shutdown and later asserted
against that stale snapshot. The prior diagnostic found the required payload
record missing in 14/40 early reads, yet present in all 40 completed logs.
Evidence remains in ../shutdown-recheck-07ca9a29/REPORT.md and its raw observations.

The corrected driver opens a read-only handle inside the existing process
context, retains it through normal shutdown and temporary-directory cleanup,
then parses the completed log. ExitStack closes the retained handle on both
success and exceptions. No alternative shutdown policy or new helper API was
introduced. No sleep, polling, timeout increase or ignored assertion is added.

The original exchanges and all assertions are unchanged, verified by comparing
Python ASTs (`preservation.json`). The five-second SIGINT grace and CTest's
40-second limit are unchanged. Configuration precedence/discovery modes are
unchanged. Searches of the other log-reading drivers and the existing CMake
registrations confirmed that this change can remain local to the checkpoint;
no shared harness interface needs modification.

This is test/verification code used by the public exercise. No C++ exercise or
lab program, example implementation, framework API, Python function signature,
CLI argument, CMake registration, reader command or manuscript was changed.
The existing ch13 README command continues to invoke the same CTest. The verbose
checkpoint output can now include the final drained records instead of a partial
snapshot; the expected logging policy and payload assertions are identical.

## Verification

Source remains clean at **07ca9a2936ee72582df7d159cb06666fe23e30f8**. Tests use
`build/shutdown-recheck-07ca9a29/install-gcc`, the fresh verified installation
from the preceding session. No rebuild is needed for the edited Python driver;
CTest invokes its source path directly.

- **40/40 consecutive checkpoint executions pass**, using CTest
  `--repeat until-fail:40` and the original timeout. Evidence:
  checkpoint-repeat.log; checkpoint-repeat.xml reports the final test result,
  while the verbose log records all forty executions.
- **62/62 public exercises pass**, zero skips. This includes the unchanged
  configuration modes and the corrected logging checkpoint. Evidence: labs.log,
  labs.xml. All three equipped exercises execute.
- Exact commands, prefix, exit codes and times: run.py and results.json.
- Assertions identical, only one ci/companion path edited, and all other recorded
  book inputs unchanged: preservation.json. These source/input checks were also
  repeated after the runtime suites completed.
- Existing framework, external echo, smoke/lifetime and 100-trial SIGINT results
  remain recorded in ../shutdown-recheck-07ca9a29/. They were **not rerun** for
  this Python-only fix; neither their code nor the framework installation changed.

Our changes: production/example/framework code **+0/−0**; exercise verification
Python **+12/−7** (net +5 lines). Shared harness and all other test drivers are
unchanged. Added review scripts/logs are evidence support, accounted separately.
No complete manuscript listings changed, so no listing-alignment rerun is claimed.

**Outcome:** the identified checkpoint timing defect is fixed and the complete
public exercise suite is green. Framework API and user-facing invocation remain
unchanged. Book refinement stays paused; source-baseline reconciliation and the
unfinished P1 work remain outside this fix. No framework or publication gate is
claimed newly executed. Historical failure evidence remains preserved.
