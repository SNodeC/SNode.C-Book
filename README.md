# Layered Network Programming with SNode.C

**Building Multi-Protocol Applications in Modern C++**

This repository contains the structured Markdown source for an architecture-first book about SNode.C. The book is positioned as a SNode.C book, not as a general survey of C++ networking libraries. It teaches layered, event-driven, multi-protocol network programming through the concrete structure of SNode.C.

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

- `metadata.yaml` — Pandoc/LaTeX metadata for the book build.
- `book-files.txt` — main manuscript file order.
- `STRUCTURE.md` — human-readable overview of the manuscript structure.
- `SOURCE-VERSION.md` — exact SNode.C source snapshot used for manuscript alignment.
- `proposal/book-proposal-package.md` — publisher-facing proposal material.
- `proposal/evidence-sheet.md` — conservative evidence/adoption status sheet for acquisition review.
- `frontmatter/` — preface, reading guidance, conventions, author note, and acknowledgements.
- `chapters/` — one Markdown file per chapter.
- `parts/` — part divider files.
- `backmatter/` — further reading material and the generated-index entry point.
- `examples/` — complete source trees for compact chapter examples and the guided MiniGateway project.
- `verification/` — non-manuscript verification notes for source/package checks, including the machine-readable SNode.C source baseline.

The current manuscript contains all planned front matter, chapters, an epilogue, and back matter. The printed chapters refer to compact examples as electronic companion material. In this source package, that companion material is stored below `examples/` for the HTTP-upgrade, SSE, WebSocket echo server/client subprotocol, line-protocol server/client, MQTT-role, and MariaDB examples. Chapters 37 and 38 contain the larger MiniGateway guided project. The source trees used by those final chapters are:

```text
examples/MiniGateway-Base
examples/MiniGateway-Extended
```


## Target SNode.C source version

This package is aligned with the SNode.C source baseline recorded in `SOURCE-VERSION.md`. The reader-facing release tag is `v1.0.2`; the authoritative source pin is the full commit SHA `6e475262084ae2dab2daef8781ab9e4adb82d18e`. Later verification scripts should read `verification/book-source-baseline.env` so this baseline is not duplicated in multiple places.

The manuscript is not intended to describe arbitrary future states of the SNode.C repository. If a newer checkout changes component names, public headers, examples, or package layout, those changes must be reviewed before the manuscript is updated.

## Example source and tested-code policy

The compact source trees in `examples/` are intended to be complete buildable versions of the shorter manuscript fragments. The printed book should refer to them as electronic companion material rather than as printed-book contents. They are teaching examples, not replacements for the source snippets in the chapters. The directory `examples/` also contains an aggregate CMake project that configures, builds, and installs/deploys all companion examples together.

`examples/MiniGateway-Base` is the authoritative source tree for Chapter 37. `examples/MiniGateway-Extended` is the authoritative source tree for Chapter 38. The chapter listings are explanatory copies of those files and should be updated from the source trees whenever the examples change.

Both MiniGateway versions are intended to be buildable external SNode.C consumer examples. Before publication, they should be built and checked against the SNode.C source snapshot recorded in `SOURCE-VERSION.md`. If a chapter listing and its corresponding example source tree ever disagree, the example source tree is the source of truth and the chapter should be corrected.

The current package records author-confirmed local verification history for the companion-example set in `verification/examples-aggregate-build-verification.md`. The example sources and matching manuscript listings were later aligned to single-exit style and are now marked for fresh author re-check. MiniGateway-specific details are retained in `verification/minigateway-step8-author-verification.md`. The verification notes target the SNode.C `v1.0.2` release tag and its exact pinned commit. These files are package evidence, not manuscript prose, and they are not presented as independent continuous-integration evidence.

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

Install Pandoc, `pandoc-crossref`, and a XeLaTeX-capable TeX distribution. The manuscript is built through CMake:

```bash
cmake -S . -B build
cmake --build build --target pdf
```

The manuscript PDF build uses LaTeX indexing support. The `pdf` target generates LaTeX, runs `xelatex`, runs `makeindex`, and then runs `xelatex` twice more so that index pages and cross-references settle.

To generate LaTeX only:

```bash
cmake --build build --target tex
```

To build the publisher-facing proposal PDF, including the attached evidence sheet:

```bash
cmake --build build --target proposal
```

The CMake build reads `book-files.txt` during configuration. If the manuscript file list changes, reconfigure the build directory.

## Source package and publisher/reviewer package

During editing, a source package may contain the Markdown manuscript, proposal source, metadata, figures, filters, LaTeX support, and example source trees without a freshly generated full manuscript PDF. Such a package is useful for inspection and refinement, but the full PDF must be rebuilt before distribution.

The `proposal-package` target creates the final publisher/reviewer archive in `packages/`:

```bash
cmake --build build --target proposal-package
```

That generated archive is intended to contain both generated PDFs, the manuscript/proposal sources, the proposal evidence sheet, front matter, back matter, source-version pin, metadata, structure files, filters, LaTeX support, figures, and example source trees needed for publisher or reviewer inspection. It should not include local build directories, editor state, `.git` internals, or other working-directory artifacts.

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
