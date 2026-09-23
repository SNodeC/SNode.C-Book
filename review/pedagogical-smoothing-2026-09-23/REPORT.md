# Pedagogical smoothing — Follow-up 11 run

## Run history

- **P0b stop:** source alignment found framework drift; the run stopped in
  `965bcbc`. [Original report](REPORT-P0b-stopped.md) and P0b evidence remain historical.
- **Phase R at 8b8da56:** the public pin and anchors were reconciled; framework
  and exercise failures left the gate qualified. The subsequent adaptations were
  reverted. [Historical report](REPORT-R4-before-continuation.md).
- **9746d186–07ca9a29:** the author added shutdown log draining, moved signal
  processing to the event-loop thread, then simplified logging synchronization.
  [Initial verification](shutdown-recheck-9746d186/REPORT.md),
  [signal investigation](shutdown-investigation-9746d186/REPORT.md),
  [signal-fix verification](shutdown-recheck-55c36e41/REPORT.md), and
  [simplification verification](shutdown-recheck-07ca9a29/REPORT.md) are completed
  historical work. The only carried-forward driver change is
  [2e71f2a's completed-log observation](checkpoint-log-fix/REPORT.md).
- **Phase R2 at 07ca9a29:** Follow-up 11 resumes from `a2ecd9c`, preserving all
  commits and the unfinished P1 snapshot. A fresh public clone confirms the pin.
  The 1,448-file manifest and three prescribed anchors are updated; one local
  dispatch-condition claim is corrected. Fresh build/runtime verification passes: framework 185/185, external Echo
  4/4, labs 62/62, and all smoke/lifetime suites. P1 is complete at 100,780 tokens; P2–P7 remain.

## Governing scope and source

[PROMPT.md](PROMPT.md), [FOLLOWUP-01 §5](FOLLOWUP-01.md), and
[FOLLOWUP-11](FOLLOWUP-11.md) govern this run. PROMPT.md remains unchanged.
Follow-ups 02–10 authorize no new work. No timeout or assertion changes.
The previous report is preserved as [REPORT-before-FOLLOWUP-11.md](REPORT-before-FOLLOWUP-11.md).

Author source: `/home/voc/projects/snodec/snode.c`, clean at
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. The freeze authority is
[framework-freeze-R2.json](framework-freeze-R2.json). The new source digest is
`2face99fc58fb1ec5374c35d88e6fcd9c7a7d56b52ea44cb00e49eb4825b9a2b`.
The retained patch is empty. The reviewed claim digest now matches the new source manifest.

A pre-existing ignored `build/rebaseline-R2-07ca9a29` directory was preserved.
This run uses a new archive/build/prefix beneath
`build/rebaseline-R2-07ca9a29-followup11`, verified against all 1,448 frozen files.
No fetch, build or edit occurs in the author's framework tree.

## Gates

| Gate | Commit | State / evidence |
|---|---|---|
| R2 scope and R0 preconditions | `8fd9a23` | [R2-preconditions.json](R2-preconditions.json), fresh public clone and freeze |
| R2 R1 pin | `4762369` | Live declarations, full manifest and empty patch |
| R2 R2 anchors | `69ac502` | [R2-anchor-review.md](R2-anchor-review.md); all anchors verified |
| R2 R3 claim review | `cfd65ab` | [R2-claim-review.md](R2-claim-review.md); only manuscript Ch5:89 changed |
| R2 evidence | `2be416b` | [R2-build/results.json](R2-build/results.json), [R2-entry-results.json](R2-entry-results.json) |
| P0b-R2-resume | `77226ab` | All 13 groups pass, including 62/62 labs; P0b-R2-resume-results.json |
| P1 | `c603b8f` | Snapshot reread notes in [P1-context-review-notes.md](P1-context-review-notes.md) |
| P2 | `9df7d00` | 32 chapters + A; all 62 labs pass; P2-registry-review.md |
| P3 | `0deb8b3` | 33 apparatus units; 66/66 labs; P3-gate-notes.md |
| P4/P5 | this tier gate commit | 109,970 tokens; P4-P5-api-review.md and P5-core-mechanism-review.md |
| P6/P7 | pending | Seams and full exit verification |

Static entry checks pass: chapter references, source alignment (zero errors,
31 chapter/appendix records, 37 complete listings), source hygiene, metrics,
both checker test suites, package build and extracted-package hygiene.
Compilation and all runtime suites pass; results are recorded separately under
R2-build/ and summarized in R2-results.json. No skips. A separate P0b resume
gate follows.

## Remaining work

The absolute must/wish/ceiling remain **107,338 / 112,338 / 115,000** tokens.
The original review baseline is **100,338**. Snapshot vocabulary work counts
against the final total. No floor or cap waiver exists; check-smoothing.py has
not yet been created or run. No chapter assessment or apparatus completion is
claimed. D1–D6 content/structure work and P2–P7 remain pending.

P1 counts compare c7b76c1 with the fresh manuscript in terminology-counts.md.
The complete carrier inventory and design-role survivors are in
terminology-allowlist.md. References, alignment and hygiene all pass.

Production-code changes: +0/−0. Existing tests/drivers and timeouts: +0/−0.
New review orchestration is evidence support, not application implementation.
The author framework is unchanged. Push only the work branch when the run ends;
do not merge.

P3 fresh total: **108,701** tokens. All 66 labs pass against the R2 installation; no assertions/timeouts changed. API/source review and mechanical gate details are in P3-api-review.md and P3-gate-notes.md. The complete CMake listing in Ch31 is synchronized at 60 lines by removing seven blank separators only. Remaining floor/cap checks await the final tier and seam pass.
