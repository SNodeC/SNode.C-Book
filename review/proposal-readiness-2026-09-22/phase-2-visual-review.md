# Phase 2 PDF visual review

Reviewed 2026-09-22. Final artifact:
`build/proposal-readiness-phase-2/snodec-book.pdf` (also copied by the normal target
to `dist/pdf/snodec-book.pdf`). It has 470 physical pages, down from 482 at phase
entry. `phase-2-pdf-checks.json` records zero warnings and zero bad boxes from the
final LaTeX log; `phase-2-pdf-final.log` records the successful ordinary target.

Rendered 49 physical pages at a 1,500-pixel long side using `pdftoppm`. The exact
page inventory and final PDF digest are in `phase-2-rendered-pages.json`.

| Physical pages | Material inspected | Result |
| --- | --- | --- |
| 11–12 | final contents pages | evenly distributed entries; no underfull vertical box after adjusting existing section-row stretch |
| 22–25 | all of Chapter 1 | objectives, side-by-side comparison table, layer figure, recap and exercises readable; no clipping |
| 35–43 | all of Chapter 3 | complete listings retain syntax styling, filenames, and clear transitions; objectives and exercises readable |
| 259–267 | all of Chapter 23 | comparison/API/field tables, server/client listings, lifecycle prose, recap and exercises readable; table continuations retain headers |
| 407–426 | all of Chapter 35 | every listing retained; filename labels stay with the following code; long listings continue normally; exercise box fits on its final page |
| 440–444 | all of Chapter 37 | decision tables, three principles, objectives, recap and exercises readable |

Contact sheets were inspected for all listed pages; the Chapter 1 comparison and
Chapter 35 filename transition were also inspected at full rendered size. The
initial Chapter 35 layout left `SocketStateReporter.h` at the foot of page 415,
with its listing starting on 416. A no-break penalty alone did not prevent the
listing environment's later break opportunity. That attempted mechanism was
removed. The final `Needspace` constraint before filename labels reserves space
for the label and opening code lines; pages 415–416 confirm the correction.

After that final adjustment, all 49 pages were rendered again. Thirteen pages had
changed pixels (listed in the JSON), and all thirteen were inspected anew in the
`changed-1.png` / `changed-2.png` contact sheets. The remaining rendered pages were
pixel-identical to the inspected versions. The temporary images are under
`build/proposal-readiness-phase-2/visual/`; they are regeneration artifacts, not
manuscript authority. No visual review of all 470 pages is claimed.
