# Pedagogical smoothing — resumed run stopped at R4

Date: 2026-09-23. Branch: `book/pedagogical-smoothing-2026-09-23`.
Authority: unchanged `PROMPT.md`, amended by the verbatim `FOLLOWUP-01.md`.

## Outcome

**Stopped at R4.** The exported pinned framework compiles, but its full CTest
suite fails **2 of 183 tests**. Both failures reproduce in a focused rerun:
`EndpointLifetimeCountersTest` and `InetLegacyClientConnectFailureTest`.
The tests expect log records to be visible immediately after disabling file
logging or freeing the event loop. Asynchronous delivery no longer satisfies
that expectation. The expected IPv4 attempt records are present after process
exit, although both assertions counted zero inside the test.

This is the follow-up's stop condition for a failure exposing a changed contract
in the framework. The permitted exception covers timing adjustments to
**companion drivers only**. These failing assertions live in the frozen
framework, so they cannot be repaired within R. No framework source, framework
test, assertion, timeout or skip policy was changed. Transport failure is not
established by these results: the observed mismatch concerns log visibility.

Evidence: `R4-build.log:1209`, `R4-framework-ctest.log`,
`R4-failure-recheck.log`, `R4-log-after-exit.json` and the source locations below.
The build script returns 8 at framework CTest, before installing the requested
new prefix and building the companion. **0/62 companion labs were executed
against a new installation**; this is not 62 failed labs. The old installation
was never used as evidence for this resumed run.

Tokens: **100,338 → 100,323**, delta **−15**. `metrics-after-R.json` is the
current measurement; the original before/after files remain unchanged.

| Absolute threshold | Tokens | Current distance |
|---|---:|---:|
| Must | 107,338 | 7,015 below |
| Wish | 112,338 | 12,015 below |
| Ceiling | 115,000 | 14,677 below |

No floor or cap waivers. No chapter is declared pedagogically complete.
`check-smoothing.py` has not been created or run. P0b-resume and P1–P7 were not
started, because Phase R did not pass its gate.

## Run history

The original P0a and P−1 gates remain intact:
`371a1b09738cb23e3981f2f15c9de9f037390e9c` and
`c70d9d1ca422bf57dbb7940b5112a31896efe8c6`. The original P0b stop was recorded in
`965bcbcfc15c2c3887a3f39287fbcccc3c082a79`: nine anchor checks and eleven file
comparisons differed from the author's frozen tree. That stop was correct.
Its REPORT content is preserved byte-for-byte in `REPORT-P0b-stopped.md`; all
original P0b logs/JSON and metrics-before.json/metrics-after.json remain intact.

Follow-up 01 accepts the public 8b8da56 source re-baseline. R1–R3 resolve the
original source-alignment failure: the fresh checker now reports **zero errors**,
31 chapter/appendix records and 37 exact complete listings. The resumed run
encountered a different failure in the pinned framework's own tests at R4.
The old 62/62 result is historical, not transferred to the new pin. Proposal
verification statements now make that distinction explicit.

## Gates and commits

| Gate | Status | Commit | Evidence |
|---|---|---|---|
| R0 | passed | recorded with R1 | R0-preconditions.json; R0-public-clone.log; framework-freeze-R0.json |
| R1 | pin complete | `e67295c2dfa4e09dd2ea14cdf11e66c08d2eaf52` | pin/manifest/checkout diff; empty patch retained |
| R2 | anchors complete | `e4f8a612695afeb957293920ea92350e4012aede` | R2-anchors.md; exactly nine line-number changes |
| R3 | local claims reconciled | `fa62fa1bf554f4efa7a5c71527cb15b67ead1492` | R-claim-review.md; logging chapter diff |
| R4 / R evidence | **failed; stop evidence only** | containing commit, `review: stop re-baseline at framework logging checks` | R4-build.log; R4-failure-recheck.log; R-stop-checks.json |
| P0b-resume | not started | — | R gate unmet |
| P1, P2, P3, P4+P5, P6, P7 | not started | — | no smoothing changes or chapter splits |

The stop-evidence commit is not the successful `review: re-baseline evidence`
gate required by the follow-up. Its SHA is supplied in the final handoff.
Only the work branch is designated for push; no source-branch push or merge.

## Source and R0

The book resumed clean at 965bcbc on the requested branch. The author tree was
clean at `8b8da56e0349191d4658ca8f820a490539eccd4d`; R0 exactly matches P0a.
A separate public HTTPS clone under `build/rebaseline-8b8da56/public-source`
confirmed that the pin is reachable from origin/master (and was its tip at
collection). No fetch or build ran in the author tree. See R0-preconditions.json.

The manifest contains **1,447** tracked/untracked non-ignored file contents,
with the same sorted `digest  name` digest algorithm as the unchanged checker:
`f00e7f9c16854d70c3d2122272458c581bacd108882ed13004c7d6d2173348ee`.
Version stays 2.0.0. The patch file is empty and its digest check is retained.
Reader instructions use the single public checkout. CI only applies a nonempty
patch. No live reader source authority still relies on the former patch.
Historical review references to that source remain historical.

The R4 and R-stop freezes both match R0/P0a exactly. No framework files were
modified. PROMPT.md remains SHA-256
`c34bbab40ac13289e993af8504344f8d1435e1ec5ca87d4fb7ad6dfac8020155`.

## R1–R3 decisions and inspection

- R1 updates the source env, content manifest, version notes, README, Preface,
  Chapter 2 checkouts, deployment/testing source wording, Further Reading and
  proposal declarations. Changes are identified by the R1 diff. A newly added
  Chapter 2 mention in Further Reading tripped the reference precheck; replacing
  it with the source-version document path restored the existing register.
- R2 changes no path or needle and drops no anchor. The follow-up labels the
  second Config.cpp:1070 anchor as record 24; the repository places it in record
  **26**, and record 24 has no such anchor. Under PROMPT §2, that existing record
  26 was updated to 1071. R2-anchors.md records the conflict.
- R3 corrects the logging chapter's synchronous-format/output cost statement,
  clarifies caller-side format validation and locally qualifies startup/delivery.
  `hexDump` byte lifetime and its disabled-level early return remain true.
  Every inspected claim and source location is listed in R-claim-review.md;
  unchanged-anchor-file contracts are explicitly carried forward. The registry's
  reviewed_tree_sha256 now matches the new manifest.
- D1–D6 smoothing work remains pending. R only applies the follow-up's public-pin
  amendment to D3; it does not create the future Ch2 sidebar or restructure prose.

## Failure diagnosis

| Evidence | Finding |
|---|---|
| tests/unit/core/EndpointLifetimeCountersTest.cpp:607 | Disables log file then reads it immediately, before the logger guard teardown; several summary/retry counts are zero |
| tests/component/net/InetLegacyClientConnectFailureTest.cpp:172 | Calls free and disables file logging, then reads before process teardown; both attempt counts are zero |
| src/log/detail/SpdlogBackend.cpp:194 | Disabling the file sink updates worker configuration, without a caller-visible queue drain |
| src/log/detail/SpdlogBackend.cpp:236 | Active async path submits encoded records to the worker |
| src/log/detail/SpdlogBackend.cpp:459 | Queued worker callbacks retain their selected output sinks |
| R4-log-after-exit.json | Both expected attempt messages occur once after the focused test process exits |

This narrows the failure to a synchronous visibility assumption in the framework
regression tests. It does not decide whether the upstream remedy belongs in
those tests or in a documented flushing contract. Either remedy is outside the
authorized companion-driver exception. No test was weakened to manufacture a pass.

## Verification

| Check | Result | Evidence |
|---|---|---|
| Public pin and clean frozen tree | PASS | R0-preconditions.json; framework-freeze-R-stop.json |
| Source alignment against author tree | PASS, zero errors | R-stop-source-alignment.log |
| Chapter references | PASS | R-stop-references.log |
| Source hygiene | PASS | R-stop-hygiene.log |
| Reference checker tests | PASS | R-stop-reference-tests.log |
| Metrics tests | PASS | R-stop-metrics-tests.log |
| Metrics | measured | metrics-after-R.json |
| Pinned framework compilation | PASS | R4-build.log, 968 build steps |
| Framework CTests | **181/183 pass; 2 fail; no skips** | R4-framework-ctest.log; R4-framework-test-inventory.json |
| Focused failure reproduction | **2/2 fail** | R4-failure-recheck.log |
| New prefix install, external echo and companion build | NOT RUN after CTest failure | ci/build-companion-examples.sh stops at failed framework CTest |
| Companion labs | NOT RUN, 0/62 executed against new installation | same prerequisite failure |
| Teaching, behavior and lifetime smoke checks | NOT RUN against new installation | same prerequisite failure |
| PDF/package build | see R-stop-package.log and R-stop-artifacts.json | final stopped-state artifact refresh |
| Extracted-package hygiene | see R-stop-artifacts.json | final package extraction/check |
| check-smoothing.py | NOT RUN / not yet created | stopped before P1 |

The initial PDF precheck built successfully but exposed two overfull boxes in
its final proposal logs. The evidence-sheet bullet now displays the short pin;
the authoritative declarations retain the full SHA. Final artifacts are checked
separately; initial precheck logs are retained rather than overwritten. Raw log
content is preserved except for normalization of trailing horizontal whitespace.

## Preservation, waivers and remaining work

The manuscript still has 30 numbered chapters plus Appendix A. It retains 37
source markers, 1,033 index entries, 18 figure IDs and 20 rule boxes. Fenced
tokens are **8,151 → 8,145**: the two obsolete git-apply commands were removed
by explicit R1 authority. No application listing was cut. No structure-sensitive
register was changed other than the nine source lines and reviewed tree digest.
No old pass evidence was edited. Production C++ and test implementation changes
are **+0/−0**; no companion driver changed. The existing workflow conditionally
applies the retained patch as requested. Review scripts and reports are evidence
support, not framework or application code.

- **Completed:** R0, R1, R2 and local R3 claim reconciliation; original P0a/P−1.
- **Blocked:** the R gate, by the two pinned-framework logging test failures.
- **Open:** fresh installation/62 labs, P0b-resume and all P1–P7 deliverables,
  including the absolute 7,015-token must gap.
- **Qualified:** source inspection/alignment succeeds, but the new pin has not
  passed full runtime verification. Historical installed-package evidence is not
  a substitute. No new hosted CI or hardware/deployment verification is claimed.
- **Waivers:** none. No post-pass chapter ledger, terminology allowlist, apparatus
  mapping or self-assessment is fabricated for smoothing work not performed.

The work branch is retained for the required push. The run does not proceed
past R4 without a source/test resolution outside this pass's present scope.
