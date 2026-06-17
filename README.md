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
- `book-files-existing-only.txt` — alternate file order used by the existing-only build target.
- `STRUCTURE.md` — human-readable overview of the manuscript structure.
- `proposal/book-proposal-package.md` — publisher-facing proposal material.
- `chapters/` — one Markdown file per chapter.
- `parts/` — part divider files.
- `examples/` — example source trees used by the guided MiniGateway chapters.

The current manuscript contains all planned chapters and an epilogue. Chapters 37 and 38 contain the MiniGateway guided project. The source trees used by those chapters are:

```text
examples/MiniGateway-Base
examples/MiniGateway-Extended
```

## MiniGateway source and tested-code policy

`examples/MiniGateway-Base` is the authoritative source tree for Chapter 37. `examples/MiniGateway-Extended` is the authoritative source tree for Chapter 38. The chapter listings are explanatory copies of those files and should be updated from the source trees whenever the examples change.

Both MiniGateway versions are intended to be buildable external SNode.C consumer examples. Before publication, they should be built and checked against the SNode.C version or commit named for the manuscript. If a chapter listing and its corresponding example source tree ever disagree, the example source tree is the source of truth and the chapter should be corrected.

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

Install Pandoc and a XeLaTeX-capable TeX distribution. The ordinary manuscript build can be run through the Makefile wrapper:

```bash
make pdf
```

To build the existing-only file list:

```bash
make pdf-existing
```

To generate LaTeX only:

```bash
make tex
```

The same manuscript can also be built directly through CMake:

```bash
cmake -S . -B build
cmake --build build --target pdf
```

The CMake build reads `book-files.txt` and `book-files-existing-only.txt` during configuration. If either file list changes, reconfigure the build directory.

## Proposal / publisher package

The proposal package target creates a clean reviewer-facing archive in `packages/`:

```bash
cmake --build build --target proposal-package
```

The generated archive contains the proposal, manuscript Markdown sources, metadata, structure files, and example source trees needed for publisher or reviewer inspection. It should not include local build directories, editor state, `.git` internals, or other working-directory artifacts.

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
