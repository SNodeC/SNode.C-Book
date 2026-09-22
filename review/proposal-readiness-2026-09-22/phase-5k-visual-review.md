# Phase 5k — PDF visual review, 2026-09-22

Final full manuscript: **338 → 322 pages**. Samples: **54**; proposal: **6**.
All three final LaTeX logs have zero warnings and bad boxes; hashes and package
contents are recorded in `phase-5k-exit-checks.json`.

Rendered the final PDF with Poppler:

```sh
pdftoppm -f 218 -l 251 -scale-to 1300 -png dist/pdf/snodec-book.pdf build/phase-5k-visual/page
pdftoppm -f 6 -l 7 -scale-to 1400 -png dist/pdf/snodec-book.pdf build/phase-5k-visual/contents
```

Inspected all 34 physical Part/transition pages through nine contact sheets and
both contents pages directly. Reproducible images remain under the build directory.

| Physical pages | Inspection |
| --- | --- |
| 6–7 | Updated Part X entries, all ten sections per chapter and following Part page numbers align and fit. |
| 218–222 | Part opening, objectives, warnings/linker fragments and complete multi-page component graph are legible; the graph heading is numbered correctly. |
| 223–225 | Full header/component matrix repeats its heading across pages; long names wrap within cells. Ownership rule, checklist and linking fragments fit. |
| 226–229 | Feature/default list, tests/export explanations, complete external CMake example, reading recipe and closing callouts fit without clipped lines. |
| 230–234 | Deployment figure, dependency table, RPATH qualification, path blocks and complete Linux service/configuration/peer listings remain readable. |
| 235–238 | OpenWrt heading is numbered correctly; recipe table, procd script and walkthrough continue cleanly. Deployment checklist, recap and exercises retain their borders and numbering. |
| 239–245 | Test taxonomy table, full-page architecture figure, address excerpt, named-test list and source-policy/installed-consumer/ASan material fit. |
| 246–249 | Debugging/regression material, complete benchmark and qualifications fit. The exercise callout continues with its remaining four items on 249. |
| 250–251 | Part XI and MiniGateway transition remain clean. |

The initial build had a 52.41289pt overfull paragraph containing three long test
names (`phase-5k-layout-initial.log:2263`). A short bullet list retains every name
and removes the overflow. Visual review then caught two headings directly after
index commands rendered as literal Markdown. Blank lines restore their heading
status; `check-phase-5k.py` now compares actual Pandoc heading nodes with source
counts for all three chapters. Final rendered text has no literal `###`.

No production style, font size, margin or warning threshold changed. Final
inspection found no clipping, collisions, lost table rows or broken callout
borders. This is targeted review of the affected Part and contents; the proposal
source refresh remains Phase 6.
