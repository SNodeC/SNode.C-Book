# Pedagogical smoothing — checkpoint fixed; refinement paused

Author handoff: the remaining P1 manuscript edits and three P1 JSON evidence
files are preserved in a work-in-progress snapshot for independent review.
P1 remains incomplete; no editorial gate is certified by this commit. See
[HANDOFF.md](HANDOFF.md) for the current state and suggested review questions.
No new tests or manuscript edits were made for this handoff.

Current author instruction: FOLLOWUP-10.md authorizes fixing only the exercise
verification timing while retaining APIs and usage. The ch13 checkpoint now
reads its completed log after normal shutdown, using a retained read-only handle.
All assertions and timeouts are unchanged. **40/40 repeated checkpoint runs** and
**62/62 public exercises pass** against unchanged clean framework 07ca9a29.
Only companion/exercises/ch12/configuration.py changes outside review evidence;
no framework, example/lab program, API, CLI or manuscript changes. See
[the fix and validation](checkpoint-log-fix/REPORT.md).
Book refinement remains paused. Earlier results below are historical.

Earlier author instruction: FOLLOWUP-09.md requests verification of logging
synchronization simplification at clean **07ca9a2936ee72582df7d159cb06666fe23e30f8**.
Fresh framework **185/185 PASS**, external echo **4/4 PASS**, public exercises
**61/62 PASS**, teaching/behavior/lifetime PASS; zero skips. The only failure is
ch13's early asynchronous log snapshot, not SIGINT cleanup. Separate observation
finds its payload missing before shutdown in 14/40 cases but present afterwards
in 40/40, all with normal exit. SIGINT stress passes **100/100** (maximum observed
shutdown 7.65 ms). No tests, timeouts, source or manuscript files changed. See
[the current recheck and diagnosis](shutdown-recheck-07ca9a29/REPORT.md).
Book work remains paused; the following earlier verification entries are history.

Earlier author instruction: FOLLOWUP-08.md requests another verification and
report. Clean framework **55c36e418a831573ac9b5284830f4bd0d5074bac** passes the
fresh build, **185/185 framework tests**, **4/4 external echo tests**, **62/62
public exercises**, and teaching/behavior/lifetime checks, with zero skips.
The dedicated SIGINT reproduction passes **100/100** trials with the original
five-second grace (maximum observed shutdown 7.74 ms). All twelve previously
failing exercises now pass unchanged. No framework, manuscript, test or timeout
edits; source and book inputs preserved. See
[the complete new verification](shutdown-recheck-55c36e41/REPORT.md).
Book refinement has not resumed and the recorded source pin remains 8b8da56.
The earlier verification and investigation notes below are historical.

Follow-up 07 requests detailed investigation only. The new trace confirms SIGINT
on the logging worker while main remains in epoll; a later listener connection
releases the stall. Focused unchanged rerun: 8/12 pass, four reproduce this exact
worker-signal/main-wait failure. No tests or timeouts changed. See
[the detailed investigation](shutdown-investigation-9746d186/REPORT.md).

Prior verification instruction: FOLLOWUP-06.md accepts clean framework 9746d186 and
requests full verification followed by a stop. Verification is complete: framework
**184/184 PASS**, external echo **4/4 PASS**, public labs **50/62 PASS, 12 SIGINT
shutdown failures**, and teaching/behavior/lifetime suites PASS. No skips.
The new log-drain regression passes; a separate hang remains before the drain call.
All original timeouts and tests are unchanged. No manuscript refinement resumed.
See [the full recheck report](shutdown-recheck-9746d186/REPORT.md) and
[all individual test results](shutdown-recheck-9746d186/all-tests.md).
P1 vocabulary edits remain incomplete and uncommitted. Earlier results below
are historical; the recorded book source pin remains 8b8da56.

Active branch: `book/pedagogical-smoothing-2026-09-23`. Date: 2026-09-23.
PROMPT.md is unchanged; FOLLOWUP-01.md authorizes the public re-baseline and
FOLLOWUP-02.md explicitly directs continuation despite the failing CTests.

## Run history

P0a and P−1 remain complete in 371a1b09738cb23e3981f2f15c9de9f037390e9c and
c70d9d1ca422bf57dbb7940b5112a31896efe8c6. Original P0b stopped correctly at
965bcbcfc15c2c3887a3f39287fbcccc3c082a79 on framework drift. Its report content
is preserved in REPORT-P0b-stopped.md; original P0b logs and before/after metrics
are untouched. Follow-up 01 resolves that source drift. The attempted R4 stop
and findings are preserved in REPORT-R4-before-continuation.md; Follow-up 02
supersedes that stop. R continues with failed checks explicitly qualified.

## Gate record

| Gate | Status | Commit / evidence |
|---|---|---|
| R0 | passed | R0-preconditions.json; public clone; identical P0a/R0 freezes |
| R1 | complete | e67295c2dfa4e09dd2ea14cdf11e66c08d2eaf52 |
| R2 | complete | e4f8a612695afeb957293920ea92350e4012aede |
| R3 | local claims reconciled | fa62fa1bf554f4efa7a5c71527cb15b67ead1492; R-claim-review.md |
| R evidence | qualified; author directs continuation | 1ceb6ef527386a18421e419fcce3122f0ccd472c; R-results.json |
| P0b-resume | qualified; author directs continuation | containing entry-gate commit; P0b-resume-results.json, lab-repair-review.md |
| P1 | incomplete; paused by author | vocabulary edits preserved in independent-review snapshot; no P1 gate completion |
| P2–P7 | not started | 07ca9a29 shutdown checks pass; ch13 driver fixed and 62/62 labs pass; source reconciliation and explicit resumption pending |

## Source and review

The clean author tree is frozen at public 8b8da56e0349191d4658ca8f820a490539eccd4d,
version 2.0.0. A separate HTTPS clone confirmed origin/master reachability.
R0/R4/R-stop/R-gate freezes equal P0a. No writes, fetches or builds in the author
tree. The 1,447-file digest is
f00e7f9c16854d70c3d2122272458c581bacd108882ed13004c7d6d2173348ee.
The patch is empty; its check is unchanged. Readers check out the public commit.
R2 changes exactly nine line numbers and no path/needle. The follow-up's second
Config.cpp:1070 anchor labeled record 24 actually lives in record 26; updated
that existing anchor, as documented in R2-anchors.md.

R3 corrects synchronous hex-dump rendering/output cost, clarifies caller-side
format validation, and qualifies deferred startup and output visibility. Borrowed
bytes are copied before return; the disabled-level early return remains true.
R-claim-review.md records book/source evidence and byte-identical carried-forward
contracts. The reviewed tree digest is updated after that inspection.

## Build and execution evidence

R4-build.log records a fresh export and 968 successful framework build steps.
Framework CTest passes **181/183** with no skips; both failures reproduce:
EndpointLifetimeCountersTest and InetLegacyClientConnectFailureTest. Their
in-process reads precede asynchronous record visibility. Expected attempt records
appear after exit (R4-log-after-exit.json). No framework tests were changed.

Following Follow-up 02, installation completed manually after the failed CTest
stage (R4-install.log). All **4 external echo tests pass** (R4-external-echo.log).
The new prefix is `build/rebaseline-8b8da56/install-gcc`; all resumed runtime
checks use it. The 2026-09-22 installation supplies no resumed evidence.

R-results.json records passing metrics, references, source alignment, hygiene,
companion compilation, package build, both checker test suites, teaching,
behavior, lifetime and extracted-package hygiene. Source alignment reports zero
errors, 31 records and 37 exact complete listings.

The companion CTest run passes **51/62** (R-labs.log). Ten failures are SIGINT
shutdown timeouts; one is a scoped-record snapshot race. R4-shutdown-diagnosis.json
and R4-shutdown-backtrace.log reproduce a successful echo followed by a process
still waiting in epoll with its logging worker present after SIGINT. This is not
an assertion that the network exchange itself failed. At this R gate no shutdown timeout or assertion had been relaxed. Follow-up 03
subsequently authorizes longer shutdown grace; no framework workaround is added.

The authorized timing correction in companion/exercises/ch12/configuration.py:71
waits up to five seconds for the expected payload log, reading complete JSON
lines, before running all existing semantic assertions. Its focused recheck
(R-driver-timing-recheck.log) encountered the separate shutdown timeout before
that observation; no passing validation is claimed for it yet. Production C++
changes: +0/−0; test-driver change: +11/−1 (net +10 lines).

A source-reference precheck caught a new Chapter 2 mention in Further Reading;
using the source-version document path preserves the existing register. Initial
PDF logs exposed two overfull boxes from the full SHA in the evidence-sheet
bullet; it now uses the short pin while authoritative declarations retain the
full SHA. Later final LaTeX logs contain no warnings/bad boxes. Precheck failures
remain recorded. Proposal runtime claims distinguish historical passes from the
current qualified verification rather than claiming 62/62 for this pin.

## Metrics, preservation and outstanding work

Current tokens: **100,338 → 100,323**, delta −15. Must/wish/ceiling remain
**107,338 / 112,338 / 115,000**; the must gap is 7,015. metrics-after-R.json
records the result. Original before/after metrics are historical and unchanged.
No floor or cap waivers. check-smoothing.py has not yet been created/run.

Structure, 37 source markers, 1,033 index entries, 18 figures and 20 rules are
preserved. Fenced tokens change 8,151 → 8,145 only from the two explicitly
removed patch-application commands. No application listing was cut. The prompt
SHA-256 remains c34bbab40ac13289e993af8504344f8d1435e1ec5ca87d4fb7ad6dfac8020155.
D1–D6 smoothing changes remain pending; only the public-pin amendment to D3 has
been applied. No fabricated chapter assessment or apparatus completion is claimed.

Open: P1–P7. Qualified: framework and companion CTests as above;
the earlier continuation has been superseded by Follow-up 05; failures remain visible. No framework
changes are authorized. Floor/cap waivers: none. No new hosted CI, hardware or
deployment validation is claimed. Push only the work branch on final completion
or a later non-overridden stop condition.

## P0b resume and author-requested lab fixes

Follow-ups 03/04 authorize longer normal SIGINT grace and diagnosed lab repairs.
The full resumed suite executes all 62 labs: 51 pass, 11 fail after 60 seconds
on graceful shutdown. All 12 other check groups pass, including the new-prefix
smoke suites and package build (P0b-resume-results.json). Metrics-before-resume.json
records 100,323 tokens; no manuscript changed. The old P0b evidence is untouched.

Lab-driver repairs consolidate complete-record waiting, handle partial live JSON,
and allow inner shutdown grace in nested checkpoint timeouts. Three regression
tests pass; the focused integration rerun passes 11/12, with the quiet logging
checkpoint still blocked by framework shutdown before its scoped observation.
See lab-repair-review.md for exact scope, evidence and source diagnosis. The
framework records SIGINT and STOPPING but leaves the event-loop thread waiting
in epoll; forced kill remains failure. Framework source is unchanged and frozen.
P0b is qualified under the explicit continuation, not marked all checks passed.
