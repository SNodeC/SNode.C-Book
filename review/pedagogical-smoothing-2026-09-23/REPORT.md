# Pedagogical smoothing — resumed under the CTest exception

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
| R evidence | qualified; author directs continuation | containing `review: re-baseline evidence` commit; R-results.json |
| P0b-resume | next | new installation only |
| P1–P7 | pending | no pedagogical smoothing edits yet |

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
an assertion that the network exchange itself failed. No shutdown timeout or
assertion has been relaxed, and no framework workaround is added.

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

Open: P0b-resume and P1–P7. Qualified: framework and companion CTests as above;
the author directs continuation, and all failures remain visible. No framework
changes are authorized. Floor/cap waivers: none. No new hosted CI, hardware or
deployment validation is claimed. Push only the work branch on final completion
or a later non-overridden stop condition.
