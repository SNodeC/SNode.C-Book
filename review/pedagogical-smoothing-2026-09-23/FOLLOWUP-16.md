Follow-up 16: author code style for sources and listings, last wording fixes, CI evidence for HEAD

Store this message verbatim as
review/pedagogical-smoothing-2026-09-23/FOLLOWUP-16.md. It is an author
instruction. PROMPT.md and Follow-ups 01, 11–15 remain the governing scope,
except where §0 overrides them. Record it in the work plan. This pass reopens
the frozen manuscript by author decision; afterwards it is frozen again.

Attached author style files (the authority for item A):

- `_clang-format`: the author's clang-format style.
- `_cmake-format.py`: the author's cmake-format configuration.
- `clang-format.cmake`, `cmake-format.cmake`: the author's CMake modules that
  add the format commands.

Before using them, confirm that the two style files are byte-identical to the
framework's `.clang-format` and `.cmake-format.py` at `Book-1.0`. Confirm
that the two modules match the framework's `cmake/clang-format.cmake` and
`cmake/cmake-format.cmake`. The framework also has `cmake/format.cmake`, which
defines the `format` target. Record the result. If they differ, stop and
report.

0. Starting point and rules

- Work on main from HEAD (06677fb or later). Line numbers refer to 06677fb;
  locate each passage by its content if HEAD has moved.
- Sources: keep the current pin. The book uses the `Book-1.0` tags of
  SNodeC/snode.c, SNodeC/mqttsuite and SNodeC/OpenWRT, as recorded in
  source-baseline/. Do not change pins, tags or the manifest.
- Author framework tree:
  - Never modify it. Ignore porting/.
  - Record HEAD and `git status --porcelain=v1` at start and end. Any change
    stops the run.
- NO CUTS: do not delete any teaching passage, listing, example or
  explanation. Merging sentences is allowed only when every statement is kept.
- VERIFY FIRST: confirm each finding at HEAD before editing and record
  file:line evidence. If a finding does not reproduce, skip it and report it.
- Item A is formatting only. Change no identifier, string, code logic,
  assertion, timeout or test behavior. Comment wording must not change; only
  the line breaks produced by ReflowComments may.
- Size: at most 115,000 tokens in total, and every chapter within its cap.
- Commits: A, B, then one evidence commit.

1. Items

A. Apply the author's style to the book's sources, CMake files and listings
Problem: Follow-up 15 (C2) reformatted some companion files with
right-aligned references and pointers (`const std::string &error`,
`SocketConnection *socketConnection`). It also moved constructor-initializer
commas to the line ends (MiniGateway ConfigSections.cpp). Untouched listings
and the framework follow the author's style. Both styles now appear in Ch3,
12, 17, 19, 24, 25, 30 and 31.

A1 Style files and the one width override

- Add the author's `_clang-format` unchanged as the repository root
  `.clang-format`, and `_cmake-format.py` unchanged as `.cmake-format.py`.
- The author's clang-format ColumnLimit is 140, but printed code must fit the
  measured 90-column frame (ci/check-listing-width.py). Add
  `companion/.clang-format` containing only `BasedOnStyle:
  InheritParentConfig` and `ColumnLimit: 90`, with a comment naming this
  follow-up. All other settings come from the root file.
- The cmake-format line\_width is 80, within the frame. Use it unchanged, with
  no override.
- Do not edit the author's files to silence deprecation warnings.
- Choose tool versions by calibration against the framework at `Book-1.0`, so
  that the book formats exactly as the framework does:
  - clang-format: the version that parses `.clang-format` without error and
    for which `clang-format --dry-run --Werror` is clean on a representative
    framework set (src/core, src/net, src/express, src/web, src/iot). Prefer
    the version the hosted runner provides.
  - cmake-format (cmakelang): the version for which `cmake-format --check` is
    clean on the framework's CMakeLists.txt and cmake/\*.cmake files.
  - If no available version is clean on the framework, use the hosted runner's
    clang-format and the latest cmakelang. Report the framework delta without
    changing the framework.
  - Record both versions.

A2 Format target (same mechanism as the framework)

- Add `cmake/format.cmake`, `cmake/clang-format.cmake` and
  `cmake/cmake-format.cmake` to the book, following the author's modules and
  the framework's `format` target. Keep their structure, `find_program`
  detection, `format-cmds` custom command and warning text. Adapt only the
  file globs to the book:
  - clang-format: companion/\*\*/\*.cpp, \*.hpp, \*.tpp, \*.h;
  - cmake-format: every CMakeLists.txt, cmake/*.cmake, production/cmake/*.cmake
    and \*.cmake.in in the book repository;
  - both: filter out build directories ("/build/", "\_deps", CMake output
    trees) as the author's filter\_items function does.
- Include the modules from the root CMakeLists.txt so that
  `cmake --build <dir> --target format` formats the book as the framework does.
- Add `format-check` beside it. It runs the same file sets through
  `clang-format --dry-run --Werror` and `cmake-format --check`, so that CI and
  local builds use one definition of the checked files.

A3 Reformat

- Run the `format` target. The expected consequences of the author's style
  are:
  - `PointerAlignment: Left`;
  - `BreakConstructorInitializers` and `BreakInheritanceList: BeforeComma`
    (leading commas restored);
  - `IncludeBlocks: Regroup` with `SortIncludes` (include groups may move);
  - `BinPackArguments`/`BinPackParameters: false`;
  - no short functions or lambdas on one line;
  - 4-space indentation with `NamespaceIndentation: All`;
  - for CMake files: canonical command case, upper-case keywords, dangling
    parentheses aligned to the statement, 4-space indentation, 80 columns.
- Rebuild every companion target to confirm that include regrouping and
  CMake argument sorting changed no behavior.
- Update the exact listings (`<!-- snodec-source: … -->`) from the
  reformatted sources. ci/check-source-alignment.py must stay green, with 37
  exact listings.
- Recheck prose that describes a listing's layout: line references, "the first
  line …", include order. Correct any statement the reformatting made
  inaccurate.

A4 Manuscript snippets that are not exact listings

- Snippets stated to be copied from a companion file must match that file
  exactly after reformatting. Example: ch12:144–184 against EchoPair (as
  required by FU15 D3).
- Framework-derived excerpts (for example Ch6, Ch11 and the Ch15 aliases) must
  stay faithful to the framework source at Book-1.0. Do not reformat them.
- Other C++ snippets:
  - Apply the author's visible rules by hand, keeping every token:
    left-aligned `&`/`*`, 4-space indentation, attached braces, BeforeComma
    initializer and inheritance lists.
  - Running clang-format with the companion configuration on a snippet is
    allowed only when the snippet is a syntactically complete unit; review the
    result.
- CMake snippets: apply canonical command case, upper-case keywords and
  dangling parentheses only where the fragment is syntactically complete.
  Leave partial fragments unchanged.

A5 Guards

- CI: install the recorded clang-format and cmakelang versions, run
  `format-check` in the companion-examples workflow and in
  ci/build-companion-examples.sh, and log both tool versions.
- Extend check-final.py with a regression guard: no fenced C++ block in the
  manuscript contains a right-aligned reference or pointer declaration
  (`Type &name`, `Type *name`). Exclude `&&`, unary `*x`/`&x` and
  multiplication. It guards mechanically testable regressions; improve the
  checker rather than distorting correct code or prose.
- Keep ci/check-listing-width.py green at 90 columns.

B. Last wording and cadence fixes (NO CUTS)

- ch13:207: "Our running value, `echoserver.local.port = 18092`" reads as a
  file assignment, but the file holds 18091 and 18092 is the command-line
  override. Write it as the effective value 18092 of `echoserver.local.port`.
- ch13:595: "address-family differences" becomes "network-family differences".
- ch02:71: keep the fact that Clang 21 currently fails the framework build
  under -Werror (-Wnrvo) and that this is a framework follow-up. Move the
  source file:line (`ConfigActions.cpp:296`) out of learner prose into the
  report.
- ch02:167: "immutable `Book-1.0` tag" becomes "the edition tag `Book-1.0`"
  (git tags can be moved).
- ch02:178:
  - Remove "or move the tag"; readers cannot move the remote tag. Keep "do not
    bypass the check".
  - Split the paragraph into two or three paragraphs, keeping every sentence:
    (1) checker result and mismatch procedure; (2) kinds of evidence and
    equipped labs; (3) MQTTSuite, OpenWrt and the source-baseline pointer.
- ch04:219 and :228: :228 repeats :219 (`echoserver` and `conn=1` in the
  prefixes). Fold them into one statement next to the excerpt, keeping the
  interpretation sentence.
- ch07:
  - :524: join the added link sentence with "This keeps the local/remote
    distinction visible" so the fact is stated once.
  - :530 and :532: join the added Chapter 8 pointer with "A connection can
    still have bind, local, and remote address views" so the three views are
    stated once.
- ch08: finish the FU15 D5 merge, keeping every sentence.
  - :95, :97 and :99 become one paragraph.
  - :262, :264, :266 and :268 become one or two paragraphs.

C. CI evidence for HEAD

- The last recorded hosted runs (36121014960 labs, 36121014927 book package)
  tested 98f091d. Commits c83bb54, 423ad8d and 06677fb then changed CI and
  build inputs.
- After pushing A and B, record both hosted workflows for the final HEAD:
  - run IDs;
  - compiler versions;
  - Pandoc and pandoc-crossref versions;
  - clang-format and cmakelang versions;
  - every job's conclusion.
- Local verification:
  - the companion build and all 66 labs with GCC and with the workflow's
    Clang;
  - `format-check`;
  - ci/build-book-package.sh, with PDF page count.

2. Checks
   Run and record:

- check-smoothing.py, check-polish.py and check-final.py;
- ci/manuscript-metrics.py and ci/check-chapter-references.py;
- ci/check-listing-width.py;
- ci/check-source-alignment.py against Book-1.0;
- ci/check-external-anchors.py and ci/check-source-hygiene.sh;
- `format-check`;
- the book package;
- the companion build and all 66 labs with GCC and Clang.

3. Report: FOLLOWUP-16-REPORT.md

- The style-file identity check against the framework at Book-1.0.
- Tool calibration: the versions tried and the framework check results.
- Observed Book-1.0 SHAs, and the author tree at start and end.
- For each item: whether it was verified, file:line evidence, the change and
  its commit. List skipped items with the reason.
- Formatting evidence:
  - the ColumnLimit override;
  - the files reformatted;
  - any prose adjusted after reformatting;
  - that the build and all labs produce identical results;
  - exact-listing count.
- Status matrix: 37 rows × 8 dimensions over the 75 applicable cells, with
  file:line evidence for every changed cell. Target all ●; explain any ◐ or ○.
- Gate table:
  - book package green, with page count;
  - labs 66/66 GCC and 66/66 Clang, local and hosted with run IDs;
  - alignment against Book-1.0;
  - external anchors;
  - `format-check`;
  - author tree unchanged.
- Outside this repo: the Clang 21 -Wnrvo framework follow-up
  (src/tools/snodec-control/src/ConfigActions.cpp:296).
- Tokens before and after, for each touched chapter and in total.

4. Operational
   Push main. Final message, short:

- commit SHAs for A and B;
- tool versions;
- matrix totals;
- gate status with hosted run IDs;
- tokens and page count;
- anything not closed, with the reason.

After this pass the manuscript is frozen again. A later follow-up is
justified only by an actual technical error, broken build, broken reference
or production defect.
