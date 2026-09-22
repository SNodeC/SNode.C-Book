# Phase 5j — PDF visual review, 2026-09-22

Reviewed the final generated full PDF after the successful package build. Hashes,
page counts and zero-warning/bad-box checks are in `phase-5j-exit-checks.json`.
Full manuscript: 358 → 338 pages; sample PDF: 54; proposal PDF: 6.

Rendered using Poppler:

```sh
pdftoppm -f 193 -l 219 -scale-to 1300 -png dist/pdf/snodec-book.pdf build/phase-5j-visual/page
pdftoppm -f 6 -l 6 -scale-to 1400 -png dist/pdf/snodec-book.pdf build/phase-5j-visual/contents
```

Inspected all 27 Part/transition pages via seven contact sheets and contents page
6 directly. PNGs under `build/phase-5j-visual/` are reproducible build artifacts.

| Physical pages | Review |
| --- | --- |
| 6 | Updated Chapter 23/24 headings and page numbers align without clipping. |
| 193 | Part IX opening and checkpoint fit the existing typography. |
| 194–203 | Chapter 23 objectives, boundary figure, classification/API tables, complete listings, transaction qualifications and closing callouts are legible and within margins. The comparison table repeats its header across 194–195. |
| 204–212 | Chapter 24 application table, dependency graph, complete snippets, role figure, process-choice table and pseudo-configuration fit. Continued tables repeat headers; listings retain all lines. |
| 213–217 | MQTTSuite figure and role/build/name tables, storage qualifications and worked trace are readable. Both closing callouts now fit on 217. |
| 218–219 | Part X and Chapter 25 transition remain clean. |

Initial review found a 51.8219pt overfull type-name paragraph in Chapter 23 and
an almost-empty exercise continuation page in Chapter 24. A short type list and
removal of repeated deployment/role endorsements fixed them. No technical listing,
font, margin, production style or warning threshold changed. Final images show
no clipping, collisions, lost rows or damaged callout borders in the affected span.
This is targeted visual review; the proposal source refresh remains Phase 6.
