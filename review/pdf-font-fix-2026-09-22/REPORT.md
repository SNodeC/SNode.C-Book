# Font shapes and unused table-caption setup — 22 September 2026

The approved font mapping is applied, and the subsequently authorized unused
table-caption setting is removed. The ordinary rebuilt book remains **490 pages**
with **zero font-shape warnings, zero unused table-caption warnings, and zero
overfull/underfull boxes**. All manuscript files and code listings are unchanged.

## Changes

The book's existing font authority is `production/metadata/metadata.yaml`, which
Pandoc passes to XeLaTeX through its standard `monofontoptions` setting. Bold
monospace requests previously fell back to regular Latin Modern Mono because the
bold shape was not registered. The existing font selection now explicitly maps:

- Bold upright: `lmmonolt10-bold.otf`.
- Bold italic: `lmmonolt10-boldoblique.otf` (the companion bold-oblique design).

Regular and ordinary italic selection remain unchanged. The fonts are already
available in the installed Latin Modern collection, also provided by the build
workflow's existing `fonts-lmodern` dependency. No font substitution warning is
filtered and no synthetic emboldening is used.

Pandoc's default LaTeX template also declares `\captionsetup[table]{skip=6pt}`
whenever the document contains tables. All 165 tables in this book are uncaptioned,
so that override is never used. The book header now calls the caption package's
standard `\clearcaptionsetup[skip]{table}` interface to remove that unused spacing
option. Figure captions and other caption settings are retained. No warning
filter, copied Pandoc template, or generated-file patch was introduced.

## Verification

- The ordinary three-pass `pdf` target succeeds. Both the final book log and the
  complete final build console contain zero font-shape, unused-table-caption,
  overfull-box, or underfull-box warnings. A later copy in `dist` has incidental
  timestamp/font-subset differences; resolved-object comparison verifies its
  equivalence to the build output. Exact comparison rules and both hashes are
  preserved in `pdf-equivalence.json`.
- A proof using the book's actual generated preamble exercises regular, italic,
  bold, and bold-oblique text at 8, 9, 10, and 12 pt. All four shapes load and
  render without font-shape warnings. The final book embeds the companion bold
  face where bold is requested; bold oblique is additionally covered by the proof.
- Optical-size differences were measured rather than assumed away. The test
  string has identical regular/bold width at 9 and 10 pt. At 8 pt the regular
  optical design is slightly wider; at 12 pt it is slightly narrower than the
  scaled companion bold. No compensating font scaling was added. The actual
  book still has zero bad boxes and unchanged chapter starting pages.
- Targeted visual checks cover 12 pages: contents, CMake and C++ listings,
  subsection and section headings, large chapter headings, SSE/MiniGateway
  listings, the Chapter 34 table/figure sequence, a figure with small bold text,
  and the index. The four-style font proof was also inspected. The final pages
  were re-rendered after caption cleanup and match the inspected font-fixed
  pages pixel for pixel. All 490 page content streams are unchanged by that
  caption cleanup.
- All 1,092 generated contents entries resolve to PDF destinations with the
  expected printed page labels. Independent MakeIndex regeneration from the final
  index input matches the delivered index exactly: 1,033 entries accepted,
  none rejected, and no index warnings.
- All 62 manuscript inputs remain byte-identical to this pass's starting
  snapshot. Source alignment against the author's current local SNode.C tree
  and source-hygiene checks pass: 38 chapter evidence records and 36 exact complete
  listings. No source or companion application code was changed.

The build is in `build/pdf-font-fix-2026-09-22/`; durable logs, hashes, and check
results are stored beside this report. This is targeted verification of the
authorized typography changes, not a new full-book editorial review.

## Accounting and remaining scope

This pass adds five configuration lines to the existing book metadata: three
font-option lines, one explanatory comment, and one caption-option removal.
Application production code: **0 added / 0 removed**. Tests and CI implementation:
**0 added / 0 removed**. Manuscript text: **0 added / 0 removed**. Earlier uncommitted
box fixes and their historical evidence were preserved.

The pre-existing `tocloft` warning about an already redefined `\@starttoc` remains
outside this request. The separate proposal font profile was not changed or
rebuilt. OpenWrt and publication completion remain deferred; broader runtime
validation remains omitted by author decision. No commit was made.
