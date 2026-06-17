# Figure workflow

Figures for the book are kept separate from the chapter Markdown.

Recommended layout:

```text
figures/
  src/
    snodec-figure-style.tex
    fig-01-layer-stack.tex
    fig-05-runtime-context.tex
  pdf/
    fig-01-layer-stack.pdf
    fig-05-runtime-context.pdf
```

Only files named `fig-*.tex` are compiled by the CMake `figures` target. Shared style files and templates can therefore live in `figures/src/` without becoming figure targets.

Build all figures:

```sh
cmake --build build --target figures
```

The full manuscript PDF targets depend on `figures`, so figures are rebuilt before the book PDF:

```sh
cmake --build build --target pdf
```

Clean generated figure PDFs and temporary figure build files:

```sh
cmake --build build --target figures-clean
```

Include a generated figure in Markdown like this:

```markdown
![The layered SNode.C communication model.](figures/pdf/fig-01-layer-stack.pdf){#fig:layer-stack width=85%}
```

A new figure source should normally start with:

```tex
\documentclass[tikz,border=6pt]{standalone}
\input{snodec-figure-style.tex}

\begin{document}
\begin{tikzpicture}[snodec diagram]
  % figure content
\end{tikzpicture}
\end{document}
```
