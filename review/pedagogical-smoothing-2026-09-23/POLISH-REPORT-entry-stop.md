# Follow-up 12 — entry stop report

**Status: stopped before P1. No polish item is completed.**

The requested starting branch is `book/pedagogical-smoothing-2026-09-23`,
at `9b82ea4668f96e2b577b2c474a337e02fbb61ae0`. Follow-up 12 is saved
byte-for-byte as [FOLLOWUP-12.md](FOLLOWUP-12.md) and recorded in the work plan.

## Mandatory framework-freeze comparison

Follow-up 12 §0 says: “Compare it with framework-freeze-R2.json at the start
and at the end. Any change stops the run.” PROMPT.md §14 also requires a stop
when the freeze record changes and prohibits substituting another source.

The P0a-method capture compares the author's actual tree at
`/home/voc/projects/snodec/snode.c` with the existing R2 record.

| Field | R2 baseline | Polish entry |
|---|---|---|
| HEAD | `07ca9a2936ee72582df7d159cb06666fe23e30f8` | Identical |
| `git status --porcelain=v1` | Empty | `?? porting/` |
| SHA-256 of `git diff HEAD --binary` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Identical |
| Untracked, non-ignored files | None | 22 files under `porting/` |
| Complete freeze equality | Required | **FAIL — stop** |

The untracked files were enumerated and hashed only to perform the required
freeze capture. Their behavior and contents were not investigated. The
framework was not modified, cleaned, re-pinned or replaced by an archive.

Evidence: [entry capture](framework-freeze-polish-start.json),
[end capture](framework-freeze-polish-end.json), and
[comparison](polish-freeze-comparison.json). The end comparison is also
against R2; equality between start and end does not cure the entry mismatch.

## Item and check status

| Item | Status | Item commit |
|---|---|---|
| P1 — role terminology | Not started: entry freeze mismatch | None |
| P2 — Ch8 responsibility table | Not started: entry freeze mismatch | None |
| P3 — Ch2 shortest path | Not started: entry freeze mismatch | None |
| P4 — Ch13 running value | Not started: entry freeze mismatch | None |
| P5 — MQTT fundamentals and diagram | Not started: entry freeze mismatch | None |
| P6 — Ch18 reference tables | Not started: entry freeze mismatch | None |
| P7 — Ch23 case and Ch23/26 abstraction | Not started: entry freeze mismatch | None |
| P8 — verification constructions | Not started: entry freeze mismatch | None |
| P9 — publisher proposal | Not started: entry freeze mismatch | None |

`check-polish.py` was not created. `check-smoothing.py`, manuscript metrics,
chapter references, source alignment, hygiene and the package/PDF build were
not run for this stopped polish. No labs were run and no companion file
changed. No technical statement was changed, so no new source/header claim
verification is asserted. No publisher-review recommendation was implemented
outside the authorized P1–P9 scope.

## Matrix accounting

The 32-row × 8-dimension matrix was not reassessed after the mandatory stop.
For each dimension, **zero cells were changed or newly certified as ●**.
Existing ●/◐/○ totals remain historical; this run reports no new totals and
does not relabel previously completed work as open. All nine requested polish
items remain uncompleted for the same entry-freeze reason. No file:line
evidence of a completed polish change exists.

## Extent and PDF

No chapter was touched. The previous fresh measurement at the starting
revision remains **110,177 raw whitespace tokens**, before and after this
documentation-only stop. This run did not regenerate the metrics. The count
is 2,161 below 112,338, 2,323 below the 112,500 aim, and 4,823 below 115,000.
No chapter floor, cap or waiver changed.

No PDF was rebuilt. Metadata inspection of the existing completed-P7 artifact
reports **326 pages**:

[Existing reading PDF](/home/voc/projects/snodec/publications/book/build/smoothing-P7-final-extracted/dist/pdf/snodec-book.pdf)

This is the earlier PDF, not a polished edition or a new visual proof.

## Preservation and handoff

The instruction, work-plan entry and stop evidence form one evidence commit;
there are no P1–P9 commits. The preceding task's untracked
`review/publisher-review-2026-09-23/REPORT.md` is preserved without including it
in this scope. PROMPT.md, FOLLOWUP-01.md, FOLLOWUP-11.md, the original R2 freeze,
the manuscript, companion files, tests, source pin and historical reports
remain unchanged. Push the existing work branch without merging, then end
the run under the explicit stop condition.
