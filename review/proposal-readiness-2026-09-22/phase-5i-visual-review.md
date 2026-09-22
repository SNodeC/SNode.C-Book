# Phase 5i — PDF visual review, 2026-09-22

Reviewed the generated full PDF after the final successful package build. Hashes,
page counts and zero-warning/bad-box checks are in `phase-5i-exit-checks.json`.
Full manuscript: 368 → 358 pages; sample PDF: 54; proposal PDF: 6.

Rendered using Poppler:

```sh
pdftoppm -f 174 -l 193 -scale-to 1300 -png dist/pdf/snodec-book.pdf build/phase-5i-visual/page
pdftoppm -f 5 -l 6 -scale-to 1400 -png dist/pdf/snodec-book.pdf build/phase-5i-visual/contents
```

Inspected all twenty Part/transition pages via five four-page contact sheets,
plus both contents pages directly. Rendered PNGs are reproducible build artifacts
under `build/phase-5i-visual/`; this record is the committed evidence.

| Physical pages | Review |
| --- | --- |
| 5–6 | Updated section titles and page numbers align; no collisions or clipped entries. |
| 174 | Part VIII opener and checkpoint fit the existing typography. |
| 175–180 | Chapter 20 objectives, complete client listing, packet/context/component tables, diagnostic list, recap and exercises are readable and inside margins. |
| 181–185 | Chapter 21 carrier comparison, figure/caption, aliases, packet bytes, diagnostic table, CMake fragments and teaching callouts fit. |
| 186–192 | Chapter 22 boundary figure/caption, role/carrier/process/failure tables, fan-out example, eight-step recipe, recap and exercises fit. The conversation table continues across pages 188–189 with its header repeated and no lost row. |
| 193 | Part IX transition remains clean. |

No clipping, overlap, blank unintended pages, lost table rows or damaged callout
borders observed in this affected span. Chapter-closing white space follows the
existing chapter-break style. No layout repair, production-formatting change or
warning suppression was required. This is targeted affected-page review, not a
claim of a new visual audit of every unchanged page or proposal text refresh.
