# SNode.C book: persistent working instructions

## Active work plan

Before manuscript refinement, read `review/EDITORIAL-WORK-PLAN.md`. It is the
persistent authority for the agreed remaining work, acceptance criteria, and
progress. The user does not need to repeat it in later conversations.

When asked to continue refining the book, resume the next unfinished item in that
plan. Update its progress and evidence before ending a work session. Respect a
narrower current request; a question or planning request does not automatically
start a full manuscript editing session. Later explicit user instructions take
precedence; record accepted scope changes in the plan.

## Non-negotiable editorial constraints

- Refine existing passages; do not replace parts with newly written treatments.
- Preserve the author's reading/writing style, explanatory depth, cumulative
  teaching method, and the 38-chapter structure.
- There is no shortening target, word budget, or desired percentage reduction.
  Incidental shortening from removing redundant material is acceptable. Do not
  trim examples, explanations, or useful reinforcement just to make the book shorter.
- Distinguish deliberate pedagogical reinforcement from repetition that adds no
  new explanation, application, consequence, or useful reminder.
- Read the Markdown inputs in `manuscript/book-files.txt`, not the PDF, as the
  manuscript authority. PDF regeneration and visual review remain separate work.

## Source authority and technical evidence

- Use the author's current SNode.C working tree, including uncommitted changes.
  Its local location is `/home/voc/projects/snodec/snode.c`.
- Do not substitute a clean `master` checkout, a remote branch, or the recorded
  base commit alone. A base commit plus local changes identifies the source used.
- If that path is unavailable, locate the intended current working tree or obtain
  the missing location; do not silently change source authority.
- Inspect current source and working-tree state before relying on prior evidence.
  A saved manifest records an earlier snapshot; it does not override newer author
  changes. Record drift and reconcile claims and evidence with the current tree.
- Do not modify the framework as part of book refinement without separate scope
  authorization. Preserve existing changes in both repositories.
- Keep printed complete listings and companion sources consistent. Distinguish
  source inspection, compilation, runtime tests, and deployment validation.
- Never claim that a limitation was fixed merely because it was documented, or
  that a chapter was editorially refined merely because its code builds.

## Engineering and completion discipline

Follow the user's engineering instructions for companion implementation work:
trace ownership and lifetime first, prefer reduction or modification, and obtain
explicit approval before implementation if a correct fix genuinely requires net
production-code growth. Documentation and test support are accounted separately;
line-count compression is not architectural simplification.

Use the work plan's completion criteria. Report completed, qualified, pending,
and blocked work accurately. Do not declare the full refinement complete while
required editorial work or verification remains. Preserve historical verification
as historical; attach fresh evidence to the actual files and source tree checked.
