# PDF box fixes — 21 September 2026

All 25 box warnings in the historical audit are resolved in the ordinary,
integrated PDF build. The PDF remains **490 pages**. No manuscript words or code
listings were removed or rewritten, and all 38 chapter starting pages are unchanged.

This closes the author's bad-box request. It does not declare publication
production complete. Font and other non-box warnings were investigated and
reported, but their configuration was not changed.

## Result

| Diagnostic | Audited baseline | Final book log |
|---|---:|---:|
| Overfull horizontal boxes | 2 | 0 |
| Underfull horizontal boxes | 12 | 0 |
| Overfull vertical boxes | 0 | 0 |
| Underfull vertical boxes | 11 | 0 |
| Total | 25 | 0 |

The final three-pass build console also contains zero box-warning emissions.
All 18 figure logs and the contact-sheet log contain zero box warnings. No
badness thresholds, fuzz tolerances, or warning filters were changed.

Output: `dist/pdf/snodec-book.pdf`.
Build directory: `build/pdf-box-fixes-2026-09-21/`.
The preceding audit in `review/pdf-box-audit-2026-09-21/` remains historical and
unchanged. `warnings-resolved.json` maps every baseline warning to its correction.

## Cause and corrections

The governing layout invariant is that the complete manuscript must fit its
existing text area with readable word and vertical spacing. The underlying
problems were forced full justification in short recap and introduction text,
unbreakable slash compounds, unfavorable paragraph boundaries, and a page-bottom
policy that stretched pages containing fixed-height material. One floating figure
could also interrupt a continuing table. The fixes belong to those existing
formatting responsibilities; they do not change the technical explanation.

- **Recaps:** the existing shared recap definition now uses hyphenation-aware
  ragged-right setting. A finite 3 em allowance gives recap lists natural spacing
  while retaining useful hyphenation. It is scoped to that box type. The existing
  breakable-box behavior, title, colors, padding, and font sizes remain intact.
  The `ragged2e` package supplies the standard implementation, including list
  handling; no custom parallel list formatter was introduced.
- **Part introductions:** the existing right inset now has stretchable space,
  preserving both 13% insets and the italic presentation without stretched words.
- **Prose:** discretionary breaks were added after slashes in Chapters 12, 17, 20,
  and 27. Four existing paragraphs in Chapters 18, 32, and 34 were divided at
  existing sentence boundaries. Every word is retained.
- **Page bottoms:** the main matter uses natural page bottoms. The back matter
  explicitly restores its original flush-bottom policy. This prevents artificial
  vertical stretching around tables, code, and figures while retaining the
  existing page geometry and code size.
- **Figure 34.1:** its existing placement preference changed from `tbp` to `hbp`.
  It now follows the completed table and its introducing paragraph on printed
  page 388, with the following explanation below it. It no longer floats above
  the table continuation.

The integrated visual check caught and corrected an intermediate Chapter 4
spillover. The delivered version keeps that chapter's complete closing section
on its original page and introduces no extra pages.

## Verification

- The ordinary CMake `pdf` target completed its three XeLaTeX passes and MakeIndex
  step. A later copy in `dist` has a different creation timestamp and generated
  font-subset identifiers. Comparison of all 13,536 resolved document objects,
  including decoded streams, confirms equivalence after normalizing those
  incidental differences and excluding storage containers. Both hashes and the
  precise comparison rules are preserved in `pdf-equivalence.json`.
- All 62 manuscript inputs were compared with checkpoint `fcbe51a`. They are
  identical after normalizing whitespace and only the intended formatting
  controls: discretionary slash breaks, page-bottom commands, and Figure 34.1's
  placement attribute. The normalized source word count is **151,914 before and
  after**. This is a whitespace-based manuscript-source count, including listings
  and markup, not a count of prose alone.
- All **779 non-LaTeX fenced blocks** are unchanged byte for byte in their
  contents and fence information. The source-alignment checker also confirms
  all **36 explicitly marked complete listings** against companion sources and
  checks all **38 chapter evidence records**.
- Source alignment was checked against the author's current local SNode.C tree,
  clean at `bb63e8a87aeda88123e8c0d72cb6d298908a9fe6`, with file-content digest
  `df2fbdbe844f3368f5ed142973d82c0008a057c13d87dda6b7670e45cc3eacb8`.
  No framework or companion source was modified. Existing source-hygiene checks
  passed. Runtime tests were not rerun for these formatting-only changes.
- The final book log contains no unresolved-reference or rerun warnings. All
  **1,092 entries in the generated contents file** resolve to PDF destinations
  carrying the expected printed page label, including entries below the displayed
  contents depth.
- MakeIndex was independently rerun against the final index input: 1,033 entries
  accepted, zero rejected, zero warnings. Its output is byte-identical to the
  index used by the final PDF.
- Targeted visual review covers all 23 originally affected pages, every chapter
  recap (including the three continuations), all 12 numbered part introductions
  and the epilogue introduction, Chapter 4's closure, Figure 34.1 and its table,
  the contents, and all eight index pages. Text, tables, figures, code, and page
  furniture fit in the inspected areas. This is a targeted production check,
  not a claim that all 490 pages received a new editorial review.

The exact page inventory, hashes, diagnostic logs, content comparison, and
reference verification are preserved beside this report. Rendered inspection
images remain in the ignored build directory.

## Other warnings — report only

### Font shape

The book still reports:

```text
LaTeX Font Warning: Font shape `TU/LatinModernMono(0)/b/n' undefined
using `TU/LatinModernMono(0)/m/n' instead
LaTeX Font Warning: Some font shapes were not available, defaults substituted.
```

These are one missing bold-upright shape and its final summary. Regular Latin
Modern Mono is substituted where bold monospace is requested. The later summary
does not indicate a second missing font. The author explicitly requested reporting
this issue while continuing the box fixes; font settings remain unchanged.

For a subsequent font fix, the recommended candidate is to retain Latin Modern
Mono for regular text and explicitly assign its installed companion files
`lmmonolt10-bold.otf` and `lmmonolt10-boldoblique.otf` for bold and bold italic.
A separate, isolated XeLaTeX proof loads those shapes without font warnings. The
tested regular and bold sample both measure 162.75 pt. This establishes a working
candidate, not a full-book font-change verification; applying it still requires
an integrated rebuild and visual check. The proof source and log are preserved.

### Unused table-caption setup

Generated LaTeX line 47 declares `\captionsetup[table]{skip=6pt}`. The current book
contains 165 `longtable` environments and none has a caption, so that table-caption
setting is never consumed. The caption package reports the unused declaration
at the end of the document. This is harmless for the current PDF: it does not
indicate lost table content, a missing required caption, or a spacing defect.
The generated declaration was left unchanged.

### Contents package

The pre-existing `tocloft` warning that `\@starttoc` was already redefined remains.
It is outside this box-fix scope. The current contents were nevertheless checked
visually and their destinations verified as described above.

## Change accounting and limits

| Category | Added lines | Removed lines |
|---|---:|---:|
| Manuscript formatting | 19 | 9 |
| Shared LaTeX / metadata configuration | 4 | 1 |
| Companion or framework production code | 0 | 0 |
| Tests and CI implementation | 0 | 0 |

The small configuration growth loads the existing typography package and sets
the existing recap style; there is no new application implementation. Review
reports, logs, and the persistent work plan are separate documentation/evidence.

OpenWrt remains deferred. Broader runtime validation remains intentionally omitted.
Full publication completion and unrelated production-warning cleanup remain
outside this pass. No commit was made for these layout changes.
