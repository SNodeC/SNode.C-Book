# Phase 5g — rendered review, 2026-09-22

The Markdown inputs were reread as manuscript authority. Poppler rendered physical
pages 128–144 (Part VI opener, both chapters, Part VII transition) and contents
pages 4–5. All 19 pages were visually inspected. Local images and contact sheets:
`build/phase-5g-visual/`. The figures, tables, complete/excerpt listings, objectives,
rules, warning, recaps and exercises remain legible without clipping or overlap.
The existing production formatting and figure assets were not changed.

Two corrections followed the first render:

- Chapter 14's recap had a single-line continuation on physical page 135. Tightening
  its overlapping bullets keeps the full recap on page 134 and the exercises on
  page 135, and makes trust/name/SNI an explicit reminder.
- Chapter 15's failure-visibility sentence produced an underfull line (badness
  1365, generated TeX lines 11267–11270). Two connected sentences preserve its
  diagnostic requirements and eliminate that bad box without formatting changes.

The corrected pages 134–135 and 143 were rendered and inspected again as
`final-*.png`. Final contents pages 4–5 show eight sections in each chapter and the
correct following Part. The complete affected Part was reviewed in the initial
render; the final text edits change only those re-reviewed pages. Both figures
retain their original IDs and captions. Normal table continuation headers remain.

Final artifacts: full manuscript 382 pages (was 392), sample package 54 and
proposal 6. All three final LaTeX logs have zero warnings and zero bad boxes.
`phase-5g-exit-checks.json` records PDF hashes and 326 package files identical to
their inputs. `phase-5g-final-artifact-refresh.log` records the corrected build.
This is targeted visual review of the changed Part and contents, not a new visual
certification of every unchanged page in the book.
