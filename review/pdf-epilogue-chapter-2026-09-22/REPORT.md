# Concluding chapter heading — 22 September 2026

The author selected **The Principles Behind the Programs** for the chapter after
the epilogue part page. The heading in `manuscript/chapters/epilogue.md` now uses
that wording. The part page retains **Epilogue / What to Take Away from SNode.C**
and its previously approved typography. All chapter prose is unchanged.

The ordinary three-pass PDF build succeeds with **490 pages**. The final LaTeX
log has **zero warnings and zero bad boxes**. The complete console contains one
first-pass label-convergence message, resolved by the remaining passes.

Verification confirms the new contents entry and PDF bookmark, all 1,092 contents
destinations, unchanged printed page labels and chapter starting pages, and an
unchanged index. Only PDF pages 12 and 475 have changed content streams. The
contents page, epilogue part page (474), and chapter opening (475) were rendered
and inspected; the new heading fits cleanly on one line.

Sixty-one manuscript inputs remain byte-identical to the baseline. The remaining
input differs only in its first heading line. Current-tree source alignment and
hygiene checks pass, including 38 chapter evidence records and 36 complete
listings. The framework remains clean at
`bb63e8a87aeda88123e8c0d72cb6d298908a9fe6`.

Build products are in `build/pdf-epilogue-chapter-2026-09-22/`. Logs, hashes, and
verification results accompany this report. The distribution PDF matches the
verified build at the recorded check.

Accounting: **1 manuscript heading line added / 1 removed**; no prose changes,
production application changes, or test/CI implementation changes. Earlier
uncommitted work is preserved. No commit was requested or made.
