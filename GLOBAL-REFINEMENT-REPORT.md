# Global Refinement Report

This package is the result of a chapter-by-chapter internal full-book refinement pass over Chapters 1–35. Chapters 36–38 were intentionally left unchanged because they are present but not yet written.

## Global review brief applied

The pass used the full-book review as the editorial brief. The main applied principles were:

- preserve the current architecture of the manuscript;
- avoid radical rewrites;
- preserve the established technical voice;
- normalize terminology around role, configured communication role, registered runtime-visible instance, connection, context, protocol layer, and boundary;
- consolidate excessive short-paragraph runs without removing short paragraphs as a deliberate teaching rhythm;
- keep source-code density stable;
- keep conceptual `text` diagrams where they express layer or boundary structure;
- avoid turning conceptual chapters into API or command manuals;
- strengthen the weaker balance points identified in the review, especially Chapter 19 and Chapter 20;
- keep Chapters 36–38 unchanged.

## Box and callout decision

The manuscript currently uses fenced `text` blocks as layer diagrams, decision diagrams, comparison sketches, and compact conceptual summaries. This pass did not replace them with a new callout system, because doing so would require a parallel Pandoc/LaTeX design decision.

For the final production pass, the recommendation remains:

- keep fenced `text` blocks for true ASCII layer diagrams and dependency sketches;
- consider a distinct callout style for design notes, common mistakes, and durable reminders;
- update the proposal or style guide so it describes the manuscript's actual callout vocabulary.

## Code/example density decision

No broad code expansion was performed. The review judged the manuscript to be concept-heavy and diagram-heavy rather than code-heavy, which matches the proposal's architecture-first intent. More executable continuity should primarily come from the future guided-project chapter, not from scattering many small examples through already stable chapters.

## Chapter-specific changes

### Chapter 01

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 02

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 03

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 04

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 05

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 06

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 07

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 08

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 09

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 10

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 11

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 12

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 13

- Cleaned remaining loose outer-instance wording and aligned it with application-side handle / configured communication role terminology.
- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 14

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 15

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 16

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 17

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 18

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 19

- Added a short TLS capability vs TLS deployment responsibility section to balance Chapter 19 with later deployment material.
- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 20

- Added output-pressure and bounded write-buffer policy section to balance robustness/failure detail with later testing and benchmarking chapters.
- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 24

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 26

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 30

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 31

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 32

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

### Chapter 34

- Conservatively consolidated runs of very short normal prose paragraphs while preserving code blocks, lists, headings, tables, and diagrams.

## Remaining editorial TODOs

- Revisit the proposal after Chapters 36–38 are written, especially the promised callout/box vocabulary.
- Decide the final visual style of conceptual `text` diagrams versus code blocks in the PDF/LaTeX template.
- Use Chapter 37 to provide the complete guided project that ties together the architecture-first material.
- After Chapters 36–38 are written, run one final copyediting pass over the complete manuscript.

## Final terminology sweep

After paragraph normalization, a focused terminology sweep corrected remaining loose references in Chapters 1, 20, and 31 where `instance` could otherwise obscure the distinction between application-side handles, configured communication roles, and registered runtime-visible instances.
