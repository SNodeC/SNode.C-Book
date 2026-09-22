# Phase 5h — rendered review, 2026-09-22

Markdown was reread as manuscript authority. Poppler rendered physical pages
142–174 (Part VII opener, all four chapters, following Part opener) and contents
page 5. All 34 pages were visually inspected through the page images/contact
sheets under `build/phase-5h-visual/`. Tables, executable listings, deployment
contracts, learning objectives, recaps and exercises are legible without clipping
or overlap. The web-protocol figure retains its asset, caption and label.

Two prose-only corrections followed the build/render review:

- A long inline framework-test filename in the short-circuit paragraph produced
  an overfull line (75.4909 pt, initially generated TeX lines 12520–12529). Recasting
  the introduction as connected sentences preserves the reference and experiment;
  the final page 154 fits. Initial build output is retained in
  `phase-5h-initial-layout-build.log`.
- The WebSocket frame table initially repeated an empty continuation header on
  page 167. Combining two overlapping frame/message paragraphs preserves outgoing
  fragments, incoming chunks/control frames and all message callbacks. The complete
  table now fits on page 166 without an empty continuation. The figure moves to
  page 167, retaining normal caption flow. Chapter 19 and the following Part opener
  were rendered again (physical pages 165–174, `final-*.png`) and inspected.

Final contents page 5 was re-rendered as `final-contents-005.png`; it shows 6/5/7/7
sections in Chapters 16–19 and the correct chapter/Part start pages. Chapter 19's
subprotocol section now starts on printed page 154, matching the final contents.
Ordinary tables and long listings continue across pages where necessary, without
missing content. Production layout files and figure assets were not changed.

Final full manuscript: **368 pages**, down from 382. Sample package **54 pages**,
proposal **6 pages**. All three final LaTeX logs have zero warnings and bad boxes;
PDF hashes and 336 package files identical to their inputs are recorded in
`phase-5h-exit-checks.json`. This is targeted visual review of the affected Part,
transition and contents, not a new inspection of every unchanged book page.
