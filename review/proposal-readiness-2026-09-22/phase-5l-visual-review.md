# Phase 5l — PDF visual review, 2026-09-23

Markdown remains the manuscript authority. This record covers the separate visual
review of the built artifacts, not a substitute for the editorial reread recorded
in chapter-ledger.md.

The final PDFs are under `dist/pdf/`. Their hashes, page counts, zero-warning and
zero-bad-box checks are recorded in `phase-5l-exit-checks.json`. The final layout
rebuild is `phase-5l-layout-final.log`.

| Artifact | Pages before → after | Visually inspected PDF pages (one-based) |
| --- | ---: | --- |
| snodec-book.pdf | 322 → 322 | 7–8 (contents), 250–287 (Part XI through the epilogue transition) |
| book-proposal-sample-package.pdf | 54 → 54 | 31 and 38 (the two changed Ch28 passages), 50–54 (Ch30 tables, recap and checkpoint exercises) |
| book-proposal-package.pdf | 6 → 6 | Proposal source unchanged; build and automated checks only in this phase |

Poppler page images and contact sheets are retained as local build artifacts under
`build/phase-5l-visual/`. All initial full-manuscript contact sheets were inspected.
After the listing-spacing change, full-manuscript pages 271–287 were rerendered and
all five final contact sheets (`final/complete-01.png` through `complete-05.png`)
were inspected again. Final contents pages 7–8 and sample pages 31 and 38 were
also inspected individually. Sample pages 50–54 were inspected individually;
the subsequent Ch29 spacing change does not affect the sample set.

The first review exposed an isolated opening line at a Ch29 listing page break.
Applying the existing `\Needspace{9\baselineskip}` command before each of that
chapter's eight listing introductions keeps their starts together. Final review
confirmed the introductions and starts, readable continued listings, the complete
architecture figure, wrapped identifiers, decision-table continuations and
exercise callouts. No clipped content, overlapping text or margin overflow was
observed on the reviewed pages. The closing transition and contents remain clear.
No production filter or LaTeX style was changed.

The proposal-source and TOC refresh remains Phase 6. The appendix and closing
editorial work remains Phase 5m; neither is certified by this scoped review.
