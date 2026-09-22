# CI toolchain repair — 22 September 2026

Status: publication CI passes with TeX Live 2026. A second, staged-consumer
test-environment correction passes isolated local tests; its hosted run is pending.

## Confirmed failures and governing requirements

The pushed book revision `6376b74` failed in both workflows:

- [Book package](https://github.com/SNodeC/SNode.C-Book/actions/runs/35666687450): the older fontspec could not resolve `lmmonolt10-bold.otf`, and the older tcolorbox did not recognize `halign upper code`.
- [Companion examples](https://github.com/SNodeC/SNode.C-Book/actions/runs/35666687529): GCC and Clang failed on `std::span` in `HttpMessageParserTest`; Clang additionally diagnosed `std::optional<Request>` copy operations.

The publication job must use a declared toolchain that supports the validated
manuscript configuration. The framework's existing C++20 project policy must
apply to both `src/` and the sibling `tests/` directory, independently of the
compiler's default dialect.

## Changes

The publication workflow uses the Debian TeX Live 2026 image built on 1 July,
pinned to `sha256:3bdf292b53c04ffa3ca694a5114397859bcd39b6b417c212414e1505e7fe8ec5`.
The Ubuntu runner remains the container host. Distribution TeX packages are
removed from the installation step; the image supplies TeX and its fonts.
Commands run under Bash as the container user, without sudo. `xz-utils` is
explicit because the image lacks the decompressor needed by pandoc-crossref.

The exact-image rehearsal exposed another pre-existing mismatch: Pandoc 3.9.0.2
does not generate the caption setup emitted by locally verified Pandoc 3.10.1.
After TeX could load the fonts, the old Pandoc preamble failed at the book's
`clearcaptionsetup` command. CI now pins Pandoc 3.10.1, retaining the locally
verified pandoc-crossref v0.3.24a release. No conditional LaTeX workaround or
manuscript/layout change was introduced.

In the current author SNode.C tree, the existing three CMake standard settings
(C++20, required, extensions off) move from `src/CMakeLists.txt` to the project
root. No application or test C++ changes. Both source directories now inherit
one setting. The two-file change is also captured in the book's existing source
patch; CI continues to reconstruct the author's actual source contents.

Current source identity: HEAD `bb63e8a87aeda88123e8c0d72cb6d298908a9fe6` plus the
attached `framework-cmake.patch`; file-content digest
`f676e6cbeabbd8a14a0e2c64a254f688790c6a2e59a6b37daea28ea4f69a4df6`.
The original reconstruction base remains unchanged. Earlier verification reports
retain their original source identities.

## Local verification

- Clang 19 reproduces the `span` and `optional` errors with C++17; the same
  translation unit passes with C++20 (`parser-before.log`, `parser-after.log`).
- Fresh GCC 16 and Clang 19 CMake configurations give all 167 test translation
  units explicit `-std=c++20`; no global flag was supplied by the harness.
- Reconstruction from the recorded base plus refreshed patch matches the
  current author tree exactly. All 38 source records and 36 complete listings
  pass; source hygiene passes.
- Workflow YAML parses. Shell syntax checks pass. Non-patch source diffs pass
  whitespace checks. The captured patch's blank context lines are valid unified
  diff syntax; reconstruction was checked by applying it.
- The pinned image's manifest and every downloaded layer digest were verified.
  `image-manifest.json` and `image-config.json` record its identity.
- The workflow's installation commands execute inside that image and report
  TeX Live 2026, Pandoc 3.10.1 and the unchanged crossref release. The local
  rootless image rehearsal disables apt's user switching only inside the
  disposable test root; GitHub's container does not need that local adjustment.

- Complete GCC and Clang framework builds pass; all 183 CTests pass with each
  compiler. Both installations pass all four external echo tests. Both companion
  builds, three teaching groups, behavioral suite and SSE/WebSocket suite pass.
- The exact pinned image completes `ci/build-book-package.sh`, including both
  package builds and the archive check (311 unique entries). The final book is
  490 pages with zero warnings and zero bad boxes. All 490 page content streams,
  page labels, contents and index are unchanged. All 1,092 contents destinations
  resolve to their expected printed pages. Six representative book pages and
  representative proposal pages were rendered and visually inspected.
- The separate proposal profiles compile to 11 and 65 pages. They retain
  nonfatal unused-table-caption warnings; the sample also retains its original
  missing bold-monospace shape/substitution warning. The book's font/caption
  cleanup was not applied to those independent profiles. These warnings are
  recorded in `pdf-verification.json`; they do not fail the publication job.

Full logs and disposable build trees are under `build/ci-fix-2026-09-22/`.
The local compiler versions differ from GitHub's Ubuntu toolchains; local success
alone is not represented as a successful hosted workflow run.

## Scope and accounting

Application C++: 0 added / 0 removed. Test C++: 0 added / 0 removed.
Framework CMake: 4 added / 4 removed (three settings and their blank line moved).
Manuscript and typography settings: unchanged. CI configuration and source/evidence
records change separately. The source patch includes the exact current framework
fix; the source manifest and chapter anchor line numbers were refreshed.

OpenWrt, omitted broader runtime validation, and publication completion retain
the author's established scope decisions. This repair does not declare the book
finished.

## Hosted follow-up: staged consumer library discovery

At book commit `0e224a4`, the publication run `35669868538` passed on attempt 2.
Attempt 1 built all outputs but failed while finalizing the artifact upload with
an HTTP 403; the unchanged retry uploaded successfully. In companion run
`35669868745`, GCC passed every step. Clang compiled successfully and passed
182/183 framework tests, exposing a separate staged-install test failure:
`libsnodec-core-mux-epoll.so.2` could not be loaded.

The test must execute against its own temporary installation. Its executable
RUNPATH covers direct libraries but does not supply the search path for their
indirect dependencies. The initial local run silently found those dependencies
in `/usr/local/lib`; its passing result did not establish isolation from the
system framework installation.

As requested by the author, `StagedInstalledConsumerTest.cmake` now sets
`LD_LIBRARY_PATH` to its staged `lib` and `lib/snode.c/web/http` directories.
Both consumers inherit this test-local environment. No system configuration,
application loading policy, assertions, or test selection changes.

With `/usr/local/lib` hidden, the original consumer reproduces the missing epoll
error. After the change, all 183 tests pass with both GCC and Clang under the
same isolation. The test harness provides normal `/dev`, `/proc`, and loopback
networking; preliminary restricted-harness failures are not framework failures.
The committed isolated logs record the successful full runs. Source alignment,
hygiene, and reconstruction from the base plus updated patch also pass.

The author committed the earlier C++20 relocation as
`37b3a1e16de436c818eed807ee8a962f7cbbf43b`. That current HEAD plus the two-line
test-environment change has file-content digest
`c83b6344c09b1b1a106bac2fb47cabd0c21543d6e66c19a5432303378770eebf`.
The earlier source identity and evidence above remain historical.

Additional accounting: application/production code 0 added / 0 removed;
test-support CMake 2 added / 0 removed, comprising one comment and one environment
assignment. This supplies the temporary installation's execution environment
within the existing test; no second library-loading implementation is added.
