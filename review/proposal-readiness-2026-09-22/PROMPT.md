# Task: Make the SNode.C-2.0 branch proposal-ready for a specialist technical publisher

Repository: SNodeC/SNode.C-Book, branch SNode.C-2.0.
Work branch: Create a new branch on top on SNode.C-2.0 called SNode.C-2.0-refinement

Goal: a publisher proposal package (proposal + evidence sheet + sample chapters + full
manuscript PDF) that an acquisitions editor can accept. Priority order: proposal
document and sample chapters first, then book-wide hygiene, then structural condensation.

## Execution control (one phase per session)
- In Phase 0, store this prompt verbatim as
  review/proposal-readiness-2026-09-22/PROMPT.md. Later sessions read it from there.
- Each session executes exactly ONE phase: the phase named in the session request, or,
  if none is named, the first phase whose status in REPORT.md is not "completed".
- Before starting, re-verify that the previous phase meets its exit criteria by
  re-running metrics and the listed checks; do not trust the recorded status alone.
  If it does not, report the gap and stop.
- At the end of the phase:
  - write metrics-after-phase-<N>.json;
  - update the status table in REPORT.md (phase | status | commit | date | evidence)
    and review/EDITORIAL-WORK-PLAN.md;
  - commit as "proposal-readiness: phase <N> — <summary>";
  - then STOP. Do not begin the next phase, even if time remains.
- A phase that misses its exit criteria ends as "qualified" or "blocked" with the
  reason. It is never marked "completed".
- Phase 5 runs as sub-phases, each in its own session: 5a (apply the approved TOC and
  fix cross-references), then 5b, 5c, … (condensation, one Part per session).

## Out of scope (do not touch, do not report)
- source-baseline/**, version identifiers, commit hashes, Chapter 2 reconstruction
  instructions, the SNode.C framework repository. Version drift is expected; it is
  not a finding.
- Historical review folders (review/*-2026-09-2x/, review/editorial/**,
  review/verification/history/**): preserve as history.

## Where things go
- Manuscript text: manuscript/{frontmatter,parts,chapters,backmatter}/*.md; order in
  manuscript/book-files.txt; update STRUCTURE.md when structure changes.
- Proposal: review/proposal/book-proposal-package.md, evidence-sheet.md,
  sample-chapters.md (and review/proposal/CMakeLists.txt if the sample set changes).
- New companion code (exercise solutions, comparison example):
  companion/examples/<Name>/ and register it in companion/examples/CMakeLists.txt.
- Callout styling: production/filters/snodec-callouts.lua and production/latex/**.
- Tooling: ci/manuscript-metrics.py (new), ci/check-source-hygiene.sh (extend).
- This pass's reports and evidence: review/proposal-readiness-2026-09-22/
  (PROMPT.md, REPORT.md, metrics-before.json, metrics-after-phase-<N>.json,
  chapter-ledger.md, RESTRUCTURE-PLAN.md, build logs).

## Targets (measurable acceptance; global targets apply at the end of Phase 5)
- Total words ≤ 115,000 (stretch 105,000). Code listings are not cut to meet this;
  the reduction comes from prose.
- Chapter headings (### and deeper) ≤ 550; average section length ≥ 250 words.
- "Closing perspective" sections: 0. Keep at most one "What to remember" box per
  chapter, ≤ 5 bullets, no bullet restating the chapter title.
- snodec-rule boxes ≤ 12: keep only rules that decide something.
- `text` fences ≤ 250. Remove arrow-chain blocks that restate the layer stack
  already shown in Fig. 1; convert the rest to tables or prose.
- Forbidden-phrase hits: 0, enforced by ci/check-source-hygiene.sh.
- Every chapter ends with 3–5 exercises in a new `.snodec-exercise` callout. At least
  one per chapter must be hands-on with an observable outcome. Solutions for coding
  exercises go under companion/examples/ and must build in CI.
- PDF build: zero LaTeX warnings and zero bad boxes, as currently. Report page counts
  before and after.

Forbidden-phrase list (authoring notes in reader text). Also scan for similar ones:
- ch11:363 "the chapter should make clear"
- ch21:399 "the published edition should make them available"
- ch29:448 "`testpost` should be presented as a focused example"
- ch29:454 "useful for Chapter 29" (a chapter citing itself)
- ch34:580 "The benchmarking tone should be ..."
Also add these patterns as guards:
- "in the manuscript" / "manuscript material";
- "the chapter should" / "the book should" / "this chapter should";
- "published edition";
- "should be presented as".

## Phase 0 — Author scope revision
This instruction is an explicit author scope change and supersedes conflicting items
in AGENTS.md and review/EDITORIAL-WORK-PLAN.md:
- A shortening target now applies (see Targets). Removing redundant prose, duplicate
  summaries, and restated framing is required, not incidental.
- Chapter consolidation is permitted, but only after the author approves
  RESTRUCTURE-PLAN.md (Phase 4 gate).
- Keep: the author's teaching approach, technical depth of explanations and code,
  the cumulative progression, the MiniGateway capstone.

Record this as "Author scope revision — proposal readiness, 2026-09-22" in
review/EDITORIAL-WORK-PLAN.md, and amend the "Non-negotiable editorial constraints"
section of AGENTS.md to reference it. Store this prompt as PROMPT.md. Commit before
continuing.

## Phase 0 (continued) — Measurement
Create ci/manuscript-metrics.py. Count words as whitespace tokens over the files in
manuscript/book-files.txt. It must report:
- total words, per-file words, prose words vs. words inside code fences;
- heading counts by level;
- callout counts by class (snodec-remember/rule/note/warning/checklist/exercise);
- fenced-block counts by language;
- "Closing perspective" sections;
- hits for the forbidden-phrase list;
- occurrences of "role", "boundary/boundaries", "visible", "is not a",
  "does not prove", "does not by itself";
- manual "Chapter N" references.

Write metrics-before.json. Baseline to reproduce, or record the difference:
- total words: 151,922;
- chapter headings (### and deeper): 1,020;
- "Closing perspective": 15; snodec-remember: 38; snodec-rule: 30;
- text fences: 478; cpp fences: 205; exercise callouts: 0.

Create REPORT.md with the phase status table.

## Phase 1 — Book-wide hygiene (no structural change)
1\. Rewrite or remove every forbidden-phrase hit and add the guards to the hygiene script.
2\. Remove all "Closing perspective" sections. Fold any sentence carrying new content
   into the chapter's final paragraph or its "What to remember" box.
3\. Merge or trim snodec-rule boxes to the target. Drop near-tautologies.
4\. Collapse mirrored server/client, IPv4/IPv6, RFCOMM/L2CAP sentence pairs into
   one table or one sentence where they add no new information.
5\. Reduce verification/provenance language inside chapters ("does not prove",
   "companion evidence", CI scope talk). Keep each necessary provenance fact once, in
   Conventions or one short back-matter note "About the companion material". Do not
   change version statements.
6\. Normalize shell fences to one label (sh). Keep snodec-source markers intact.
7\. Run check-source-hygiene.sh, check-source-alignment.py, build-companion-examples.sh,
   and the pdf target. Record results.

## Phase 2 — Sample chapters to exemplary standard (1, 3, 23, 35, 37)
These five chapters decide acquisition. For each one:
- cut ≥ 20% of prose words (code excluded);
- lower heading density to target;
- add exercises with solutions;
- reread in context.

Chapter-specific work:
- Ch. 1: replace the five-line comparison block with a compact, fair comparison.
  Build an echo server in standalone Asio as companion/examples/Comparison-AsioEcho.
  It must compile in CI and be shown side by side with EchoPair, in ≤ 1,200 words.
  State SNode.C's real costs: platform support (verify from framework source and
  state it plainly), one event loop per process, and ecosystem size.
- Ch. 3: tighten the "instance/handle/role" vocabulary passage to the minimum a first
  program needs; defer the rest to Ch. 5.
- Ch. 35: keep all listings; cut surrounding restatement.
- Ch. 37: this is the model chapter. Extend the decision-table approach only if it
  replaces restated endorsements elsewhere in the chapter.

Record per-chapter before/after metrics in chapter-ledger.md.

## Phase 3 — Proposal package rewrite (review/proposal/)
book-proposal-package.md must contain:
1\. A one-paragraph pitch: problem, reader, what they can do afterwards, why this
   author.
2\. One primary reader: an experienced C++ developer building multi-protocol Linux
   services. One secondary market: course adoption, with the course's actual
   context. Reduce makers, scientists, and interdisciplinary teams to one sentence.
3\. Comparable titles: 4–6 real books with author, publisher, year, and one line of
   differentiation each. Candidates to verify:
   - Stevens/Fenner/Rudoff, UNIX Network Programming Vol. 1;
   - Radchuk, Boost.Asio C++ Network Programming Cookbook;
   - Torjo, Boost.Asio C++ Network Programming;
   - Van Winkle, Hands-On Network Programming with C;
   - Casciaro/Mammino, Node.js Design Patterns;
   - Williams, C++ Concurrency in Action.
   Verify every bibliographic detail. Drop any title you cannot verify. Never
   invent one.
4\. A revised TOC with estimated pages per part and total pages, taken from the
   actual PDF build.
5\. A "Revision plan" section: what changes between this proposal and final
   manuscript, stated with the measurable targets, and completed vs. remaining.
6\. Author platform and market evidence. Use only verifiable facts. Where evidence is
   missing, insert a clearly marked [AUTHOR TO SUPPLY] item, for example:
   - course adoption letters;
   - known users or deployments;
   - talks;
   - dated repository statistics.
   Fabricating adoption, sales, or endorsements is forbidden.
7\. Remove internal process language (review passes, agent workflow, CI history)
   from the proposal. Keep verification claims short and true.

Also:
- Update evidence-sheet.md to match; keep it conservative.
- Update sample-chapters.md to describe what each sample demonstrates.
- Build `proposal`, `proposal-sample-pdf`, `proposal-package`; record page counts.

## Phase 4 — Restructure plan (approval gate)
Write RESTRUCTURE-PLAN.md proposing a consolidated TOC with a word budget per chapter
that reaches the total target. Evaluate these candidate merges and argue for or
against each one:
- Chapters 5–7 → 2 chapters;
- Chapters 8, 10, 11 → 1 chapter on network families;
- Chapters 16–17 → 1 chapter;
- Chapters 29–31 → 1 "SNode.C in larger systems" chapter;
- Chapter 4 (reading the framework source) and Chapter 38 (extending the framework)
  → a contributor-oriented appendix.

Also include:
- an old→new chapter map;
- every manual "Chapter N" reference affected;
- index and figure impact;
- the risk to the capstone progression.

Do not edit the manuscript in this phase. End with status "awaiting author approval".

## Phase 5 — Execute approved restructure and full condensation
Start only after the author's approval is recorded in EDITORIAL-WORK-PLAN.md.
- 5a:
  - apply only the approved plan;
  - update book-files.txt, part files, STRUCTURE.md, README positioning, and every
    cross-reference;
  - add a check that every "Chapter N" reference resolves to the intended chapter,
    using the old→new map;
  - rebuild and rerun all checks.
- 5b, 5c, …: one Part per session.
  - Condense that Part's chapters to their word budgets with the Phase 1–2 rules.
  - Add exercises.
  - Rerun all checks.
- The final sub-phase also regenerates the proposal TOC and page counts.

## Phase exit criteria
Phase 0:
- scope revision committed in AGENTS.md and EDITORIAL-WORK-PLAN.md;
- PROMPT.md stored;
- ci/manuscript-metrics.py committed;
- metrics-before.json reproduces the baseline figures, or records the difference;
- REPORT.md status table exists.
Phase 1:
- forbidden-phrase hits = 0, with guards active in check-source-hygiene.sh;
- "Closing perspective" = 0;
- snodec-rule ≤ 12;
- one shell fence label;
- hygiene, source-alignment, companion builds, and pdf target pass.
- Global word and heading targets are NOT required yet; report the delta.
Phase 2, for each of Ch. 1, 3, 23, 35, 37:
- prose words reduced by ≥ 20%;
- average section length ≥ 250 words;
- 3–5 exercises, with solutions that build.
Also:
- Comparison-AsioEcho builds in CI;
- chapter-ledger.md is complete for all five chapters.
Phase 3:
- the proposal contains all 7 required sections;
- every comparable title is verified, with its source recorded in REPORT.md;
- the proposal, proposal-sample-pdf, and proposal-package targets build;
- page counts recorded.
Phase 4:
- RESTRUCTURE-PLAN.md complete;
- no changes under manuscript/ in this phase (verify with git diff);
- status "awaiting author approval".
Phase 5a:
- approved TOC applied;
- cross-reference check passes;
- full build passes.
Phase 5b onward:
- that Part meets its chapter word budgets and the exercise requirement;
- all checks pass.
- The final sub-phase must also meet every global target.

## Working rules
- Existence is not execution. Every claim in REPORT.md cites the file path and line,
  the diff, the metrics delta, or the build log that proves it. Distinguish:
  - edited and reread;
  - edited, not yet reread;
  - built;
  - run;
  - not verified.
- Refine existing passages. Do not replace chapters with generic new prose. Match
  the author's voice.
- Keep printed complete listings and companion files identical (snodec-source
  markers); run check-source-alignment.py after every listing change.
- Never squash away the scope-revision commit.


Run Phase 0 only now.

\## Author amendment — teaching book (2026-09-22)
This amendment supersedes conflicting items above. The book is a teaching book: the
reader learns SNode.C and layered network programming from the book itself.

\### Reader and market
\- Primary reader: a learner working through the book — an advanced student or a
&#x20; C++ developer — who has the stated prerequisites but no SNode.C knowledge. The book
&#x20; must teach this reader without a lecturer.
\- Phase 3, item 2 is replaced accordingly: position the book as a teaching book for
&#x20; learning layered, event-driven network programming in C++ with SNode.C.
\- Course use is a secondary benefit, stated in one sentence. Mention the framework's
&#x20; origin in the course "Network and Distributed Systems" (FH Upper Austria, Hagenberg).
&#x20; Do not build the proposal around course adoption.

\### Pedagogical elements (sample chapters in Phase 2, all others in Phase 5)
\- Every chapter opens with a "Learning objectives" callout (\`.snodec-objectives\`,
&#x20; styled in production/filters and production/latex).
&#x20; \- It contains 3–5 observable objectives (explain, implement, diagnose, decide).
&#x20; \- No objective may restate the chapter title.
\- Every chapter closes with "What to remember" (≤ 5 bullets), then exercises.
\- Exercises come in three tiers:
&#x20; 1\. review questions (conceptual);
&#x20; 2\. labs (build, run, observe, each with an expected outcome);
&#x20; 3\. design problems (choose and justify).
\- Every exercise maps to at least one objective, and every objective has at least
&#x20; one exercise. Record the mapping in chapter-ledger.md.
\- All solutions are public, so a reader working alone can check their work:
&#x20; \- lab solutions go in companion/exercises/\<chapter>/ and build in CI;
&#x20; \- review-question answers and design-problem discussions go in one back-matter
&#x20;   section, "Solutions and discussion", or in companion/exercises/\<chapter>/README.md.
\- The snodec-rule cap is 20 instead of 12. Keep rules that state a principle the
&#x20; reader must apply.

\### Learning path
\- MiniGateway becomes a running project: Phase 4 must evaluate milestones starting in
&#x20; the early chapters, with Ch. 35–36 as the final integration.
\- Plan the TOC so each Part ends with a checkpoint the reader can run and verify.
\- Phase 3 replaces the reading routes in the proposal with one clear learning path
&#x20; plus at most two shortcuts (for example, "web and MQTT gateway first").

\### Added exit criteria
\- Phase 1: the snodec-rule exit criterion becomes ≤ 20.
\- Phase 2, for each sample chapter:
&#x20; \- objectives are present;
&#x20; \- all three exercise tiers are present;
&#x20; \- the objective↔exercise table is complete;
&#x20; \- lab solutions build;
&#x20; \- the other solutions exist.
\- Phase 3: the proposal states the teaching-book positioning and the learning path.
\- Final Phase 5 sub-phase: every chapter meets all pedagogical elements.

\<paste the amendment block here>
