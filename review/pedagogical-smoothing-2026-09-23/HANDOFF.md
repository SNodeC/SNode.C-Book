# Independent review handoff

The author requests a snapshot of the current book repository for Claude to
review the state and recommend how to proceed. Refinement is paused. This is a
work-in-progress snapshot, not completion of a phase or approval of the prose.

## Read first

1. PROMPT.md: the original pedagogical-smoothing specification, unchanged.
2. FOLLOWUP-01.md and the subsequent FOLLOWUP files: author amendments and scope.
3. ../EDITORIAL-WORK-PLAN.md: persistent scope and progress.
4. REPORT.md: gate history and latest verification evidence.

## Editorial state

P0a and P−1 are complete. Phase R and P0b have historical qualified evidence.
P1 vocabulary work was interrupted for framework investigation. This snapshot
preserves the previously uncommitted changes in 38 manuscript files and the
three existing P1 JSON evidence files exactly as they stood. P1 remains
incomplete: committing the snapshot does not certify rereading, source claims,
metrics, cross-references, PDF layout or the phase exit criteria. P2–P7 have not
started. The file named metrics-after-P1.json is a saved work-in-progress
measurement, not a completed P1 gate or a fresh measurement for this handoff.
No manuscript text is changed as part of creating the snapshot.

## Framework and exercise state

The latest checked framework is clean 07ca9a2936ee72582df7d159cb06666fe23e30f8.
The framework repository was read-only throughout the book-side verification.
Fresh-build evidence: shutdown-recheck-07ca9a29/REPORT.md.

- Framework: 185/185 tests pass; external echo: 4/4 pass.
- Teaching, behavior and lifetime checks pass.
- SIGINT reproduction: 100/100 pass, original five-second grace.
- That run exposed one exercise-driver log-snapshot timing defect (61/62 labs).
- The authorized driver-only fix is committed in 2e71f2a. It reads the completed
  log after normal shutdown, preserving every assertion, timeout, API and user
  invocation. Its checkpoint passes 40 consecutive runs; all 62 exercises pass.
  Evidence: checkpoint-log-fix/REPORT.md.

The book's recorded source pin is still 8b8da56. The pin, manifest, source-claim
anchors and any affected text have NOT yet been formally reconciled to 07ca9a29.
Do not treat runtime verification against the newer installation as completion
of that source-baseline work or of any editorial phase.

## Questions for the independent review

- Are the unfinished P1 edits technically precise and pedagogically useful?
  Review them in context rather than accepting vocabulary substitutions wholesale.
- What source-baseline reconciliation is necessary before resuming the pass?
- Which P1 requirements and checks remain, and does the original P1–P7 sequence
  still provide the best next steps under the author's amendments?

Historical reports and build logs are preserved. Do not infer current failures
from superseded runs or infer editorial completion from passing runtime tests.
No new builds, tests or full manuscript review were run for this snapshot.
The work branch is book/pedagogical-smoothing-2026-09-23; it is not merged into
SNode.C-2.0-refinement.
