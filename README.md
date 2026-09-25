# Layered Network Programming with SNode.C

[![Book package](https://github.com/SNodeC/SNode.C-Book/actions/workflows/book-package.yml/badge.svg)](https://github.com/SNodeC/SNode.C-Book/actions/workflows/book-package.yml)
[![Companion examples](https://github.com/SNodeC/SNode.C-Book/actions/workflows/companion-examples.yml/badge.svg)](https://github.com/SNodeC/SNode.C-Book/actions/workflows/companion-examples.yml)

**Building Multi-Protocol Applications in Modern C++**

This repository contains a teaching book for an advanced student or C++ developer learning layered, event-driven network programming with SNode.C. With the stated C++ and tool prerequisites, a reader can work through the explanations, examples, and public sample solutions without a lecturer. The approved structure has 32 chapters in 11 Parts, followed by a closing essay and an optional contributor appendix.

The central idea is that communication software becomes easier to build, extend, test, and deploy when the important boundaries remain visible:

```text
lower communication family
  -> transport form
      -> connection handling
          -> protocol meaning
              -> application role
```

The book is written for experienced C++ developers, advanced students, and system builders who want to understand how SNode.C organizes network applications and larger network systems.

## What this repository contains

- `production/metadata/metadata.yaml` — Pandoc/LaTeX metadata for the book build.
- `production/metadata/proposal-metadata.yaml` — article-style Pandoc/LaTeX metadata for proposal PDFs.
- `production/cmake/` — reusable CMake path, tool, and Pandoc build helpers.
- `manuscript/book-files.txt` — main manuscript file order.
- `STRUCTURE.md` — human-readable overview of the manuscript structure.
- `source-baseline/SOURCE-VERSION.md` — exact SNode.C source snapshot used for manuscript alignment.
- `review/proposal/book-proposal-package.md` — publisher-facing proposal material.
- `review/proposal/evidence-sheet.md` — conservative evidence/adoption status sheet for acquisition review.
- `review/proposal/sample-chapters.md` — short bridge inserted before sample chapters in the proposal-sample PDF.
- `manuscript/frontmatter/` — preface, reading guidance, conventions, author note, and acknowledgements.
- `manuscript/chapters/` — one Markdown file per chapter.
- `manuscript/parts/` — part divider files.
- `manuscript/backmatter/` — further reading material and the generated-index entry point.
- `companion/examples/` — complete source trees for compact chapter examples and the guided MiniGateway project.
- `review/verification/` — non-manuscript verification notes for source/package checks, including the machine-readable SNode.C source baseline.

The current manuscript contains all planned front matter, chapters, an epilogue, and back matter. The printed chapters refer to compact examples as electronic companion material. In this source package, that companion material is stored below `companion/examples/` in source trees named `HttpUpgrade-Server`, `HttpUpgrade-Client`, `SSE-Server`, `SSE-EventSource-Client`, `WebSocket-Echo-ServerSubprotocol`, `WebSocket-Echo-ClientSubprotocol`, `LineProtocol-Server`, `LineProtocol-Client`, `MQTT-ClientRole`, and `MariaDB-Minimal`. Chapters 30 and 31 contain the larger MiniGateway guided project. The source trees used by those final chapters are:

```text
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```


## Target SNode.C source version

This package targets SNode.C **2.0.0** using framework `master` HEAD. Readers compare that checkout with the edition manifest; no patch is required. The file manifest records the exact source contents; CI reads `source-baseline/book-source-baseline.env` and verifies them before building. See `source-baseline/SOURCE-VERSION.md` for the checkout instructions.

The current proposal-readiness work and executed checks are documented in [the phase report](review/proposal-readiness-2026-09-22/REPORT.md). Structural migration is Phase 5a; Part-by-Part condensation and remaining teaching apparatus follow in separate sessions. The proposal dossier retains its Phase 3 pagination until the authorized Phase 6 refresh.

The manuscript is not intended to describe arbitrary future states of the SNode.C repository. If a newer checkout changes component names, public headers, examples, or package layout, those changes must be reviewed before the manuscript is updated.

## Example source and tested-code policy

The compact source trees in `companion/examples/` are intended to be complete buildable versions of the shorter manuscript fragments. The printed book should refer to them as electronic companion material rather than as printed-book contents. They are teaching examples, not replacements for the source snippets in the chapters. The directory `companion/examples/` also contains an aggregate CMake project that configures, builds, and installs/deploys all companion examples together.

`companion/examples/MiniGateway` is the authoritative source tree for Chapter 30. `companion/examples/MiniGateway-Extended` is the authoritative source tree for Chapter 31. The chapter listings are explanatory copies of those files and should be updated from the source trees whenever the examples change.

MiniGateway and MiniGateway Extended are buildable external SNode.C consumer examples checked against the SNode.C source snapshot recorded in `source-baseline/SOURCE-VERSION.md`. If a chapter listing and its corresponding example source tree ever disagree, the example source tree is the source of truth and the chapter should be corrected.

The package preserves author-confirmed local verification as historical evidence in `review/verification/history/`. It does not relabel old results as current 2.0 verification. The current verification notes describe the source/listing checks, framework CTest run, GCC/Clang companion builds, and selected application smoke tests. Actual results belong to the specific GitHub Actions run, including any failures or skips. No full MQTT/MariaDB/OpenWrt integration claim follows from a selected HTTP/SSE smoke test.

The migration adds `EchoPair` (Chapter 3) and `SemanticLogging` (Chapter 14). Complete printed code blocks carrying a `snodec-source` marker are checked against their companion source files by `ci/check-source-alignment.py`. Unmarked illustrative or abridged excerpts remain explanatory material, not separately certified executables.


## Heading convention

For Pandoc/XeLaTeX with `documentclass: book` and `--top-level-division=part`, the manuscript uses this heading convention:

```markdown
# Part title

## Chapter title

### Section

#### Subsection

##### Subsubsection
```

Manual chapter numbers are not part of chapter headings. LaTeX/Pandoc numbers parts, chapters, and sections.

## Build

Install Python 3.9 or newer, Pandoc, `pandoc-crossref`, and a XeLaTeX-capable TeX distribution. The manuscript is built through CMake:

```bash
cmake -S . -B build
cmake --build build --target pdf
```

The manuscript PDF build uses LaTeX indexing support. The `pdf` target generates LaTeX, runs `xelatex`, runs `makeindex`, and then runs `xelatex` twice more so that index pages and cross-references settle.

To generate LaTeX only:

```bash
cmake --build build --target tex
```

To build the publisher-facing proposal PDF as a compact article-style acquisition dossier, including the attached evidence sheet:

```bash
cmake --build build --target proposal
```

The explicit alias is also available:

```bash
cmake --build build --target proposal-pdf
```

To build the proposal plus selected sample chapters:

```bash
cmake --build build --target proposal-sample-pdf
```

The CMake build reads `manuscript/book-files.txt` during configuration. If the manuscript file list changes, reconfigure the build directory. The root `CMakeLists.txt` is intentionally small; manuscript, proposal, figure, package, and baseline targets are defined in the corresponding subdirectory `CMakeLists.txt` files.

## Continuous integration

Two GitHub Actions workflows verify the publication package and companion examples:

```text
.github/workflows/book-package.yml
.github/workflows/companion-examples.yml
```

The **Book package** workflow builds the compact proposal PDF, proposal-with-sample-chapters PDF, full manuscript PDF, and publisher/reviewer archive from source. It uploads the generated PDFs and package archive as workflow artifacts.

The **Companion examples** workflow checks out the immutable SNode.C snapshot, runs the configured framework tests, builds the companion examples with a GCC/Clang matrix, and runs selected behavioral smoke tests. Inspect the actual run for execution status: the smoke tests start the SSE server, read a measurement event stream, start MiniGateway Extended, inject one measurement through the Unix-domain input role, and verify the resulting HTTP/SSE state. The workflow intentionally avoids broad network integration tests, external MQTT broker orchestration, OpenWrt package builds, and long-running service tests.

The underlying checks are also available as local scripts:

```bash
bash ci/check-source-hygiene.sh
python3 ci/check-source-alignment.py
bash ci/build-book-package.sh
bash ci/build-companion-examples.sh
bash ci/run-behavior-smoke-tests.sh
```

## Source package and publisher/reviewer package

During editing, a source package may contain the Markdown manuscript, proposal source, metadata, figures, filters, LaTeX support, and example source trees without a freshly generated full manuscript PDF. Such a package is useful for inspection and refinement, but the full PDF must be rebuilt before distribution.

The `proposal-package` target creates the final publisher/reviewer archive in `dist/packages/`:

```bash
cmake --build build --target proposal-package
```

That generated archive is intended to contain the generated article-style proposal PDF, the generated proposal-with-sample-chapters PDF, the manuscript PDF, the manuscript/proposal sources, the proposal evidence sheet, front matter, back matter, source-version pin, metadata, structure files, filters, LaTeX support, figures, and example source trees needed for publisher or reviewer inspection. It should not include local build directories, editor state, `.git` internals, or other working-directory artifacts.

## Positioning

This book is:

```text
an architecture-first guide to SNode.C
a layered network-programming book
a framework book for mature C++ readers
a practical design guide for multi-protocol applications
```

This book is not:

```text
a general C++ networking survey
a Boost.Asio replacement tutorial
a beginner C++ book
a pure IoT recipe book
a complete TLS, HTTP, MQTT, Bluetooth, or database reference
```

Publication builds use Pandoc **3.9.0.2** and pandoc-crossref **v0.3.24a**
(the latter reports Pandoc3.9.0.2 as its build/ABI version). Install that pair
or point CMake's `PANDOC` and `PANDOC_CROSSREF_FILTER` at those binaries.
The shared compatibility guard checks the active executables before building.
