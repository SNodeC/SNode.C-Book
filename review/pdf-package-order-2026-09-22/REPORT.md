# Package loading order — 22 September 2026

The preceding modifications were committed as `cb7fce2` before this pass. The
package-order correction is complete and remains uncommitted. The ordinary PDF
rebuild produces **490 pages, zero LaTeX warnings, and zero bad boxes**.

## Cause and change

The governing invariant is that both contents formatting and paragraph spacing
must initialize successfully while retaining the established layout. Pandoc's
standard template loaded `parskip` before the book header loaded `tocloft`.
`parskip` patches `\@starttoc`; `tocloft` expects the original definition when
installing its optional contents hooks and therefore declined that final step.
The warning did not disable its previously defined contents formatting.

The book's existing authority, `production/metadata/metadata.yaml`, now sets
Pandoc's standard `indent: true` option to omit the automatic `parskip` block,
then explicitly loads `\usepackage{tocloft,parskip}` in its existing header.
Despite the template option's name, explicit `parskip` preserves the book's
unindented paragraphs and their spacing. The metadata comment explains this.
`tocloft` can now install its hooks, and `parskip` can apply its spacing patch.

Removing either package would discard required formatting behavior. Changing
their order uses their existing interfaces and removes the automatic loading
block from the generated preamble. No new loading mechanism, copied template,
warning filter, or patch to package internals is needed. The book's `tex` and
`pdf` targets consume the same metadata; packaging uses that book output. The
independent proposal profile does not load `tocloft` and needs no ordering change.

The cause was traced through the local CMake targets, generated LaTeX, Pandoc's
installed `templates/common.latex`, and the installed `tocloft.sty` and
`parskip.sty`. The generated preamble and final package log confirm the corrected
order. The final log contains no failed package-patch diagnostics.

## Verification

- A clean three-pass build succeeds, with zero warnings in the final LaTeX log.
  Its first-pass reference, page-label, and table-width convergence messages are
  retained in `clean-build-console.txt`; these are not persistent defects.
- The subsequent ordinary three-pass rebuild has **zero warnings in its entire
  console output**, zero overfull/underfull boxes, and no failed package patches.
  Neither warning thresholds nor warning reporting were changed.
- All 490 PDF page content streams remain byte-identical to the preceding
  verified build. Comparison of 13,536 resolved PDF objects finds equivalence
  after ignoring only creation dates, font-subset prefixes, and PDF storage
  details. The precise comparison rules and file hashes are recorded in
  `pdf-equivalence.json`.
- All printed page labels and all 38 chapter starting pages remain unchanged.
  All 1,092 generated contents entries resolve to their expected PDF page labels.
  The contents and index files are byte-identical to the baseline. Independent
  MakeIndex regeneration matches the delivered index: 1,033 accepted entries,
  none rejected, and no index warnings.
- Twenty-one pages were rendered at 100 dpi and compared pixel for pixel with
  the baseline, covering the entire contents sequence plus representative prose,
  code, headings, table/figure placement, and index. All match. Eight of those
  pages were visually inspected: PDF pages 2, 6, 12, 13, 17, 24, 410, and 489.
- The generated document body and all 62 Markdown manuscript inputs are
  byte-identical to this pass's starting point. Source alignment and hygiene
  checks pass: 38 chapter evidence records and 36 exact complete listings.
  The current local framework remains clean at
  `bb63e8a87aeda88123e8c0d72cb6d298908a9fe6`, with file-content digest
  `df2fbdbe844f3368f5ed142973d82c0008a057c13d87dda6b7670e45cc3eacb8`.
- A later equivalent build replaced the distributed PDF during verification.
  Resolved-object comparison confirms equivalence under the same normalization
  rules; both hashes are in `distribution-equivalence.json`. This snapshot
  precedes the subsequently requested epilogue-title change.

Build products and rendered comparisons are in
`build/pdf-package-order-2026-09-22/`; durable logs and results accompany this
report. This is targeted verification of package loading and layout preservation,
not a new editorial review or publication sign-off.

## Accounting and scope

Book configuration: **4 lines added / 1 removed**: two explanatory comments, one
standard metadata option, and replacement of the existing package declaration.
Application production code: **0 added / 0 removed**. Test/CI implementation:
**0 added / 0 removed**. Manuscript text: **0 added / 0 removed**. Review records
and captured verification output are documentation, accounted separately.

The previous checkpoint commit includes the earlier refinements. This package
loading change and its review records remain uncommitted. Proposal typography,
OpenWrt, and publication completion were not expanded into this task; broader
runtime validation remains omitted by the author's decision.
