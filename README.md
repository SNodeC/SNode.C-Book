# Layered Network Programming with SNode.C

**Building Multi-Protocol Applications in Modern C++**

This repository contains the Markdown source for an architecture-first book about SNode.C. The book is positioned as a SNode.C book, not as a general survey of C++ networking libraries. It teaches layered, event-driven, multi-protocol network programming through the concrete structure of SNode.C.

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
- `examples/` — example source trees when present.

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

Install Pandoc and a XeLaTeX-capable TeX distribution, then run:

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

The CMake build reads `book-files.txt` and `book-files-existing-only.txt` during configuration. If either file list changes, reconfigure the build directory.

## Proposal / publisher package

The proposal package target creates a clean reviewer-facing archive in `packages/`:

```bash
cmake --build build --target proposal-package
```

The generated archive should contain only the publisher/reviewer-facing source files and should not include local build directories, editor state, `.git` internals, or other working-directory artifacts.

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

