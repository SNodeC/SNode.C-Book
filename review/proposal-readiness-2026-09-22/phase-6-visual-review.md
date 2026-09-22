# Phase 6 — PDF and editorial review, 2026-09-23

Edited and reread the three Markdown proposal sources against their rendered text.
The final PDFs are identified by SHA-256 in `phase-6-exit-checks.json`.

Rendered with `pdftoppm -scale-to 1400 -png`, then inspected with the image viewer:

- `dist/pdf/book-proposal-package.pdf`, all physical pages **1–8**:
  title/pitch, project snapshot, reader and learning path, five comparables,
  complete Part and chapter tables, revision status, author evidence, repository
  figures and method, verification limits, outstanding author items.
- `dist/pdf/book-proposal-sample-package.pdf`, physical pages **9, 10, 14, 23,
  32, 52, 56**: revised sample guide, all five chapter openings, and the final
  exercises including the integrated checkpoint.

The table columns in the proposal were adjusted locally in Markdown to give the
Part titles and revision descriptions room. The Part and repository tables fit
on single pages; the chapter table repeats its header on continuation. An initial
chapter-table generation error in the Appendix A row was corrected before final
review and is now guarded by comparison with the actual Markdown heading.
Typography, callouts, table alignment, page numbers, and section transitions are
legible in all inspected pages; no clipping or overlap was observed. No production
style was changed. Rendered inspection files remain in the ignored build directory
`build/phase-6-visual-review/`.

The full manuscript text and the entire five-sample body compare equal to the
fresh entry package after removing physical-page footers and whitespace; see
`phase-6-pdf-text-preservation.json`. This is a text-preservation check, not a new
visual inspection of every manuscript or sample page. The manuscript's full
visual history remains the Phase 5 record. Final build logs contain zero LaTeX
warnings and zero bad boxes for all three PDFs.

Final extents: full manuscript **310**, proposal/evidence **8**, combined
proposal/evidence/guide/samples **56** physical pages. The proposal-source TOC
sums to 310 using 14 preliminary pages and the actual printed division starts
recorded in `phase-6-manuscript-pagination.json`.
