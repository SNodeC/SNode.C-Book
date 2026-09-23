# Logging synchronization simplification — shutdown passes; one lab timing failure

Date: 2026-09-23. Author instruction: ../FOLLOWUP-09.md.
Source: clean **07ca9a2936ee72582df7d159cb06666fe23e30f8**, “Simplify asynchronous
logging synchronization”. Verification and diagnosis only; no repairs or book
refinement. The framework working tree was read-only throughout.

## Results

| Check | Result | Evidence |
|---|---|---|
| Fresh framework configure/build/install | PASS; 970 build steps | framework-configure.log, framework-build.log, framework-install.log |
| Complete configured framework CTests | **185/185 PASS**, zero skips | framework-tests.log, framework-tests.xml |
| External installed-package echo | **4/4 PASS**, zero skips | external-echo-tests.log, external-echo-tests.xml |
| Fresh companion build | PASS | companion-build.log |
| All public exercises | **61/62 PASS; 1 FAIL**, zero skips | labs.log, labs.xml |
| Teaching smoke | PASS | teaching-smoke.log |
| Behavior smoke | PASS | behavior-smoke.log |
| Example lifetime/echo checks | PASS | lifetime-tests.log |
| Repeated idle-listener SIGINT diagnostic | **100/100 PASS**; maximum observed shutdown **7.65 ms**, median **3.40 ms** | sigint-stress.json, sigint-stress-summary.json |
| Independent checkpoint log observation | **40/40** normal shutdowns and complete expected payload records after shutdown; **14/40** snapshots missing that record before shutdown | checkpoint-observations.json, checkpoint-observations-summary.json |
| Source and book-input preservation | PASS | framework-freeze-before.json, framework-freeze-after.json, final-preservation.json |

[All 251 CTest results](all-tests.md) list every test and duration. All three
equipped exercises ran and passed. No internal SKIP messages were found.
`results.json` records every suite's exit code and start/end times. Public labs
return exit 8; the independent suites were still allowed to finish. Completion
of orchestration is not an all-green result.

## The sole failed exercise: ch13 logging checkpoint

`exercise-ch13-part-checkpoint` fails at
`companion/exercises/ch12/configuration.py:77–79`: the stored snapshot contains
no matching context record (`AssertionError: []`). See `labs.log:347–381`.
Configuration precedence, discovery and invalid-port checks pass. Both echo
exchanges and both normal SIGINT shutdowns complete; the failure is in the final
log assertion. There is no five-second cleanup timeout in this run.

The driver takes the snapshot at line 71, **inside** the running-process context:

1. Send the payload and receive its exact echo.
2. Read the current log file and save that snapshot.
3. Leave the context, sending SIGINT and waiting for normal shutdown.
4. Assert against the snapshot from step 2, without reading the drained log.

Asynchronous delivery does not guarantee that the payload record has reached the
file when the socket echo becomes readable. Draining records during shutdown
cannot update the already-copied Python list. That timing assumption remains in
the restored driver; it was previously documented as open in the 9746d186 and
55c36e41 reports. The previous passing invocation did not establish its absence.

`observe-checkpoint-log.py` independently repeats the same payload and scoped
logging policy 40 times against the new installation, using the unchanged public
harness and five-second grace. A retained read-only file descriptor allows a
second observation after that harness removes its temporary directory. No
polling, added shutdown delay, alternative signal or assertion weakening is used.
This is a separate diagnostic, not a replacement run of the exercise.

Results: **14/40** immediate snapshots lack the required payload record;
**40/40** contain it after normal exit, with status 254 in all trials. Raw before
and after logs are saved for the first trial and every missing-before case;
`checkpoint-observations.json` records each verdict. Thus the diagnostic observes
late delivery, not loss of the record or failed drain. It substantiates the
snapshot-timing cause of the lab failure. It does not measure a population
failure rate or certify arbitrary concurrent use of the logger API.

**Open book-test issue:** observe the record at an appropriate completion point
before checking it. This check-only session leaves the driver and its assertions
unchanged, as requested in the preceding scope instructions. No framework repair
is inferred from this lab's early snapshot.

## Source inspection of the simplification

The author commit changes only `src/log/detail/SpdlogBackend.cpp`: **+5/−19 lines**;
no framework tests change. Exact diff: `source-change.diff`. Paths below are
relative to `/home/voc/projects/snodec/snode.c`.

The invariant being checked is that backend control state remains owned by the
application/event-loop thread, while asynchronous sink work is serialized on one
worker; synchronous sink access resumes only after worker completion.

- The backend mutex and its lock guards are removed. Stdout, rotating-file and
  callback sinks use `_st` types instead of `_mt`.
- `startAsync()` (lines 161–180) retains signal blocking around construction of
  exactly one worker. Deferred startup records are emitted synchronously before
  `asyncStarted` is enabled and the asynchronous logger is installed.
- `emitSemantic()` (lines 269–285) selects the asynchronous queue while running.
  Encoding at line 315 onward snapshots record data and render mode on the
  producer side.
- `updateWorkerLogger()` (lines 491–516) captures shared sink pointers by value;
  the callback decodes and renders its owned record and does not capture `this`.
  Existing queued logger instances retain their captured sinks across subsequent
  producer-side configuration changes.
- The fetched spdlog implementation keeps a shared logger pointer in each queued
  message (`framework-gcc/_deps/spdlog-src/include/spdlog/details/thread_pool.h:29`
  under `build/shutdown-recheck-07ca9a29`). Its queue still has synchronization;
  this commit removes the outer backend/sink locks, not the queue's thread handoff.
- `shutdown()` (lines 182–193) releases the worker logger and joins the pool before
  flushing the sinks. The dependency's `thread_pool-inl.h:45–55` posts termination
  and joins workers; queued records ahead of termination are processed first.
- The prior event-loop signal fix is unchanged. The signal-wait regression still
  passes in 0.11 seconds, and SNodeCAsyncLogDrainTest still verifies all 4,096
  accepted records after free() returns (`framework-tests.log:34,650`).

No ownership violation was identified in this inspected single-producer,
single-worker path. This inspection and the executed suites are not a
ThreadSanitizer run or a guarantee for arbitrary concurrent application calls to
logger configuration/emission APIs. No performance improvement is claimed.

## SIGINT reproduction

The same `sigint-stress.py` diagnostic as the preceding run, with only its source
installation path changed, starts 100 fresh canonical EchoPair processes. Fifty
use disabled logging and fifty use default logging. After an exact binary echo
and peer closure, it alternates delays of 0, 2 and 10 ms before process-directed
SIGINT. All worker masks block SIGINT. Every process exits normally with status
254 under the original five-second grace, without later traffic or a second
signal. No forced kill was required. Timings include Python wait overhead and
are observations, not benchmark claims.

The earlier lost-wake-up failure remains unreproduced. Behavior/lifetime cleanup
still permits forced termination, so those suites alone are not evidence of
normal shutdown; the public lab harness and 100-run diagnostic enforce it.

## Provenance, preservation and status

Fresh git archive, build and installation under `build/shutdown-recheck-07ca9a29`;
new prefix `build/shutdown-recheck-07ca9a29/install-gcc`. All 1,448 tracked source
files match the author tree byte-for-byte. Tree digest:
`2face99fc58fb1ec5374c35d88e6fcd9c7a7d56b52ea44cb00e49eb4825b9a2b`.
GCC Debug, applications and framework tests enabled. `run.py`, suite logs and
export-verification.json record the exact commands and installation provenance.
No prior framework installation supplies these runtime results.

Source freezes remain identical, including after both diagnostics. Tracked and
non-ignored manuscript/ci/companion hashes are unchanged; ignored build outputs
are excluded. ci/companion still match fa62fa1, the restored pre-adaptation state.
Our production and existing test code changes: **+0/−0**. New scripts are review
diagnostics only. No framework edits, exercise fixes, timeout changes or
manuscript refinement. Historical evidence is preserved.

**Outcome:** verification complete, qualified by one reproducible exercise
snapshot-timing failure. No framework CTest, shutdown-stress or other suite fails.
Book refinement remains paused. Formal source-baseline reconciliation (book pin
still 8b8da56) and unfinished P1 work remain pending. No PDF/package build, full
editorial gate or hosted CI run was requested or claimed. Stop and report.
