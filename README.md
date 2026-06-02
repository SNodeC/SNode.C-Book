# SNode.C Book Project

This project was split from the uploaded master manuscript `snode.md`.

## Heading convention

For Pandoc/XeLaTeX with `documentclass: book` and `--top-level-division=part`:

```markdown
# Part title

## Chapter title

### Section

#### Subsection

##### Subsubsection
```

Manual chapter numbers were removed from chapter headings in the generated files. LaTeX/Pandoc will number parts, chapters, and sections.

## Build

Install Pandoc and a XeLaTeX-capable TeX distribution, then run:

```bash
make pdf
```

This uses `book-files.txt`, which includes TODO placeholders for planned-but-missing chapters.

To build only chapters present in the uploaded master manuscript:

```bash
make pdf-existing
```

To generate LaTeX only:

```bash
make tex
```

## Files

- `metadata.yaml` — Pandoc metadata for book output.
- `book-files.txt` — complete planned book order, including TODO placeholders.
- `book-files-existing-only.txt` — only chapters actually present in the uploaded master.
- `STRUCTURE.md` — overview of parts and chapter status.
- `proposal/book-proposal-package.md` — proposal package, not part of the main book build by default.
- `chapters/` — one Markdown file per planned chapter.
- `parts/` — part divider files.

## Missing planned chapters

The uploaded master manuscript did not contain the following planned chapters:

- Chapter 2: Preparing Your Environment
- Chapter 4: Reading the Codebase with Confidence
- Chapter 36: Extending the Framework Safely
- Chapter 37: A Complete Guided Project
- Chapter 38: Where to Go Next

They are present as TODO placeholders so the project structure remains stable.
