# Phase 3 PDF visual review

Reviewed 22 September 2026. The final artifact identities and page counts are in
`phase-3-pdf-checks.json`; all three final LaTeX logs are preserved alongside it.

## Inspected output

- Proposal/evidence PDF: all six pages rendered and inspected. The pitch and
  reader positioning lead the document; Part estimates and the chapter TOC are
  readable; the revision table fits; the evidence sheet occupies a separate page.
- Combined sample PDF: the same six proposal/evidence pages, the guide on page 7,
  and every sample page 8–54 were rendered and inspected. Original chapters
  1, 3, 23, 35, and 37 start on pages 8, 12, 21, 30, and 50 respectively.
- Complete manuscript: rebuilt at 470 pages and checked for warnings/bad boxes.
  No new 470-page visual reread is claimed; its manuscript and layout inputs are
  unchanged in this phase.

## Layout corrections and final observations

The proposal profile reuses the established book monospaced bold font mappings
and caption cleanup. Its generated navigation TOC was redundant with the book
TOC presented in the proposal, so it is disabled. The evidence sheet and sample
guide each start on a new page. Each selected chapter begins on its own page.

The first sample render showed split recap/exercise boxes with short continuation
fragments. Short sample teaching callouts now stay together. The Chapter 23
server-route heading initially stood alone at the bottom of a page; reserving
space after sample subheadings moves it beside its explanatory table. Complete
code listings remain present and may continue across pages normally.

All six proposal pages and all 48 guide/sample pages were inspected through
rendered contact sheets, with page renders retained for detail. After the callout
adjustment, changed pages 8, 12, 19–21, 28–30, 48–50, and 53–54 were inspected
again. After the heading adjustment, changed pages 21–28 were inspected again;
image comparison confirmed all other guide/sample pages identical to the prior
reviewed render. Final pages show no clipped text, overlapping elements, broken
tables, or stranded subheadings. Exercise-only chapter endings intentionally
leave room below the exercises rather than starting the next sample there.

Rendering command (repository root):

```sh
pdftoppm -f 7 -l 54 -scale-to 1200 -png dist/pdf/book-proposal-sample-package.pdf build/proposal-readiness-phase-2/phase-3-visual/approved-sample
```

Local review images are under `build/proposal-readiness-phase-2/phase-3-visual/`:
`proposal-1.png` through `proposal-6.png`, `proposal-contact.png`,
`sample-contact-1.png` through `sample-contact-6.png`, `final-changed-1.png`,
`final-changed-2.png`, `heading-changed-1.png`, and `approved-sample-07.png`
through `approved-sample-54.png`. They are reproducible build outputs, not
manuscript inputs. Final artifact checks and the stable final build console
report zero warnings and zero bad boxes.
