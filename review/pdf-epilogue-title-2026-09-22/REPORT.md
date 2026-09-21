# Epilogue opening as a part page — 22 September 2026

The epilogue opening now matches the numbered part pages: a centered **Epilogue**
label, the same vertical separation, and the centered title **What to Take Away
from SNode.C**. The author explicitly confirmed the canonical framework spelling
and requested the same label size as "Part XYZ".

The opening in `manuscript/parts/part-13-epilogue.md` uses the existing unnumbered
LaTeX part command. Its label uses `\huge`, followed by the book class's 20 pt
vertical skip; the title inherits the existing `\Huge` bold part style. The
shared part-page placement and introduction formatting are unchanged. The plain
contents entry and stable destination label remain separate from the displayed
two-level heading, preserving navigation without exposing line-break commands
to bookmarks. No new formatter or shared-style exception was introduced.

## Verification

- The ordinary three-pass PDF rebuild has zero warnings in its complete console
  and final log, zero bad boxes, and no failed package patches. The package-order
  correction remains active. The immediately preceding title-change build had
  one first-pass label-convergence message; its final log was also clear.
- The PDF remains 490 pages. Only PDF page 474 (printed page 452) has a changed
  content stream. All other pages, including the contents, remain unchanged.
- All 1,092 contents destinations resolve to the expected printed page labels.
  Page labels and all 38 chapter starting pages are unchanged. The index remains
  identical and independently regenerates without warnings or rejected entries.
- The heading was visually compared with Part XII on PDF page 456. Measurements
  in `heading-measurements.json` confirm identical fonts and sizes for both
  label and title, identical vertical positions, and identical vertical gaps.
  Both labels use the same Latin Modern Roman bold font at 20.6625 PDF points;
  both titles use it at 24.7871 PDF points. These correspond to the book class's
  `\huge` and `\Huge` sizes. Both lines are centered to within 0.02 PDF point.
- The epilogue page and relevant contents pages were rendered and inspected.
  The final rebuild retains the inspected appearance.
- Sixty-one manuscript inputs are byte-identical to the pass's baseline. In the
  remaining input, only the heading/navigation markup changes; all prose remains
  byte-identical. Current-tree source alignment and hygiene checks pass.

Build files and visual checks are in `build/pdf-epilogue-title-2026-09-22/`.
Durable logs, measurements, and verification results accompany this report.

## Accounting

This follow-up changes one manuscript heading into six lines of existing LaTeX
document markup: **6 lines added / 1 removed**, with no prose changes. Application
production code and test/CI implementation: **0 added / 0 removed**. No additional
production configuration changes are needed beyond the separately documented
package-order correction.

Checkpoint `cb7fce2` remains the last commit. The package-order correction, this
title refinement, and their review records remain uncommitted. Publication
completion and OpenWrt remain deferred; broader runtime validation remains omitted.
