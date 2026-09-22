\# Task: Make the SNode.C-2.0 branch proposal-ready for a specialist technical publisher

Repository: SNodeC/SNode.C-Book, branch SNode.C-2.0.
Work branch: Create a new branch on top on SNode.C-2.0 called SNode.C-2.0-refinement

Goal: a publisher proposal package (proposal + evidence sheet + sample chapters + full
manuscript PDF) that an acquisitions editor can accept. Priority order: proposal
document and sample chapters first, then book-wide hygiene, then structural condensation.

\## Execution control (one phase per session)
\- In Phase 0, store this prompt verbatim as
&#x20; review/proposal-readiness-2026-09-22/PROMPT.md. Later sessions read it from there.
\- Each session executes exactly ONE phase: the phase named in the session request, or,
&#x20; if none is named, the first phase whose status in REPORT.md is not "completed".
\- Before starting, re-verify that the previous phase meets its exit criteria by
&#x20; re-running metrics and the listed checks; do not trust the recorded status alone.
&#x20; If it does not, report the gap and stop.
\- At the end of the phase:
&#x20; \- write metrics-after-phase-\<N>.json;
&#x20; \- update the status table in REPORT.md (phase | status | commit | date | evidence)
&#x20;   and review/EDITORIAL-WORK-PLAN.md;
&#x20; \- commit as "proposal-readiness: phase \<N> — \<summary>";
&#x20; \- then STOP. Do not begin the next phase, even if time remains.
\- A phase that misses its exit criteria ends as "qualified" or "blocked" with the
&#x20; reason. It is never marked "completed".
\- Phase 5 runs as sub-phases, each in its own session: 5a (apply the approved TOC and
&#x20; fix cross-references), then 5b, 5c, … (condensation, one Part per session).

\## Out of scope (do not touch, do not report)
\- source-baseline/\*\*, version identifiers, commit hashes, Chapter 2 reconstruction
&#x20; instructions, the SNode.C framework repository. Version drift is expected; it is
&#x20; not a finding.
\- Historical review folders (review/\*-2026-09-2x/, review/editorial/\*\*,
&#x20; review/verification/history/\*\*): preserve as history.

\## Where things go
\- Manuscript text: manuscript/{frontmatter,parts,chapters,backmatter}/\*.md; order in
&#x20; manuscript/book-files.txt; update STRUCTURE.md when structure changes.
\- Proposal: review/proposal/book-proposal-package.md, evidence-sheet.md,
&#x20; sample-chapters.md (and review/proposal/CMakeLists.txt if the sample set changes).
\- New companion code (exercise solutions, comparison example):
&#x20; companion/examples/\<Name>/ and register it in companion/examples/CMakeLists.txt.
\- Callout styling: production/filters/snodec-callouts.lua and production/latex/\*\*.
\- Tooling: ci/manuscript-metrics.py (new), ci/check-source-hygiene.sh (extend).
\- This pass's reports and evidence: review/proposal-readiness-2026-09-22/
&#x20; (PROMPT.md, REPORT.md, metrics-before.json, metrics-after-phase-\<N>.json,
&#x20; chapter-ledger.md, RESTRUCTURE-PLAN.md, build logs).

\## Targets (measurable acceptance; global targets apply at the end of Phase 5)
\- Total words ≤ 115,000 (stretch 105,000). Code listings are not cut to meet this;
&#x20; the reduction comes from prose.
\- Chapter headings (### and deeper) ≤ 550; average section length ≥ 250 words.
\- "Closing perspective" sections: 0. Keep at most one "What to remember" box per
&#x20; chapter, ≤ 5 bullets, no bullet restating the chapter title.
\- snodec-rule boxes ≤ 12: keep only rules that decide something.
\- \`text\` fences ≤ 250. Remove arrow-chain blocks that restate the layer stack
&#x20; already shown in Fig. 1; convert the rest to tables or prose.
\- Forbidden-phrase hits: 0, enforced by ci/check-source-hygiene.sh.
\- Every chapter ends with 3–5 exercises in a new \`.snodec-exercise\` callout. At least
&#x20; one per chapter must be hands-on with an observable outcome. Solutions for coding
&#x20; exercises go under companion/examples/ and must build in CI.
\- PDF build: zero LaTeX warnings and zero bad boxes, as currently. Report page counts
&#x20; before and after.

Forbidden-phrase list (authoring notes in reader text). Also scan for similar ones:
\- ch11:363 "the chapter should make clear"
\- ch21:399 "the published edition should make them available"
\- ch29:448 "\`testpost\` should be presented as a focused example"
\- ch29:454 "useful for Chapter 29" (a chapter citing itself)
\- ch34:580 "The benchmarking tone should be ..."
Also add these patterns as guards:
\- "in the manuscript" / "manuscript material";
\- "the chapter should" / "the book should" / "this chapter should";
\- "published edition";
\- "should be presented as".

\## Phase 0 — Author scope revision
This instruction is an explicit author scope change and supersedes conflicting items
in AGENTS.md and review/EDITORIAL-WORK-PLAN.md:
\- A shortening target now applies (see Targets). Removing redundant prose, duplicate
&#x20; summaries, and restated framing is required, not incidental.
\- Chapter consolidation is permitted, but only after the author approves
&#x20; RESTRUCTURE-PLAN.md (Phase 4 gate).
\- Keep: the author's teaching approach, technical depth of explanations and code,
&#x20; the cumulative progression, the MiniGateway capstone.

Record this as "Author scope revision — proposal readiness, 2026-09-22" in
review/EDITORIAL-WORK-PLAN.md, and amend the "Non-negotiable editorial constraints"
section of AGENTS.md to reference it. Store this prompt as PROMPT.md. Commit before
continuing.

\## Phase 0 (continued) — Measurement
Create ci/manuscript-metrics.py. Count words as whitespace tokens over the files in
manuscript/book-files.txt. It must report:
\- total words, per-file words, prose words vs. words inside code fences;
\- heading counts by level;
\- callout counts by class (snodec-remember/rule/note/warning/checklist/exercise);
\- fenced-block counts by language;
\- "Closing perspective" sections;
\- hits for the forbidden-phrase list;
\- occurrences of "role", "boundary/boundaries", "visible", "is not a",
&#x20; "does not prove", "does not by itself";
\- manual "Chapter N" references.

Write metrics-before.json. Baseline to reproduce, or record the difference:
\- total words: 151,922;
\- chapter headings (### and deeper): 1,020;
\- "Closing perspective": 15; snodec-remember: 38; snodec-rule: 30;
\- text fences: 478; cpp fences: 205; exercise callouts: 0.

Create REPORT.md with the phase status table.

\## Phase 1 — Book-wide hygiene (no structural change)
1\. Rewrite or remove every forbidden-phrase hit and add the guards to the hygiene script.
2\. Remove all "Closing perspective" sections. Fold any sentence carrying new content
&#x20;  into the chapter's final paragraph or its "What to remember" box.
3\. Merge or trim snodec-rule boxes to the target. Drop near-tautologies.
4\. Collapse mirrored server/client, IPv4/IPv6, RFCOMM/L2CAP sentence pairs into
&#x20;  one table or one sentence where they add no new information.
5\. Reduce verification/provenance language inside chapters ("does not prove",
&#x20;  "companion evidence", CI scope talk). Keep each necessary provenance fact once, in
&#x20;  Conventions or one short back-matter note "About the companion material". Do not
&#x20;  change version statements.
6\. Normalize shell fences to one label (sh). Keep snodec-source markers intact.
7\. Run check-source-hygiene.sh, check-source-alignment.py, build-companion-examples.sh,
&#x20;  and the pdf target. Record results.

\## Phase 2 — Sample chapters to exemplary standard (1, 3, 23, 35, 37)
These five chapters decide acquisition. For each one:
\- cut ≥ 20% of prose words (code excluded);
\- lower heading density to target;
\- add exercises with solutions;
\- reread in context.

Chapter-specific work:
\- Ch. 1: replace the five-line comparison block with a compact, fair comparison.
&#x20; Build an echo server in standalone Asio as companion/examples/Comparison-AsioEcho.
&#x20; It must compile in CI and be shown side by side with EchoPair, in ≤ 1,200 words.
&#x20; State SNode.C's real costs: platform support (verify from framework source and
&#x20; state it plainly), one event loop per process, and ecosystem size.
\- Ch. 3: tighten the "instance/handle/role" vocabulary passage to the minimum a first
&#x20; program needs; defer the rest to Ch. 5.
\- Ch. 35: keep all listings; cut surrounding restatement.
\- Ch. 37: this is the model chapter. Extend the decision-table approach only if it
&#x20; replaces restated endorsements elsewhere in the chapter.

Record per-chapter before/after metrics in chapter-ledger.md.

\## Phase 3 — Proposal package rewrite (review/proposal/)
book-proposal-package.md must contain:
1\. A one-paragraph pitch: problem, reader, what they can do afterwards, why this
&#x20;  author.
2\. One primary reader: an experienced C++ developer building multi-protocol Linux
&#x20;  services. One secondary market: course adoption, with the course's actual
&#x20;  context. Reduce makers, scientists, and interdisciplinary teams to one sentence.
3\. Comparable titles: 4–6 real books with author, publisher, year, and one line of
&#x20;  differentiation each. Candidates to verify:
&#x20;  \- Stevens/Fenner/Rudoff, UNIX Network Programming Vol. 1;
&#x20;  \- Radchuk, Boost.Asio C++ Network Programming Cookbook;
&#x20;  \- Torjo, Boost.Asio C++ Network Programming;
&#x20;  \- Van Winkle, Hands-On Network Programming with C;
&#x20;  \- Casciaro/Mammino, Node.js Design Patterns;
&#x20;  \- Williams, C++ Concurrency in Action.
&#x20;  Verify every bibliographic detail. Drop any title you cannot verify. Never
&#x20;  invent one.
4\. A revised TOC with estimated pages per part and total pages, taken from the
&#x20;  actual PDF build.
5\. A "Revision plan" section: what changes between this proposal and final
&#x20;  manuscript, stated with the measurable targets, and completed vs. remaining.
6\. Author platform and market evidence. Use only verifiable facts. Where evidence is
&#x20;  missing, insert a clearly marked [AUTHOR TO SUPPLY] item, for example:
&#x20;  \- course adoption letters;
&#x20;  \- known users or deployments;
&#x20;  \- talks;
&#x20;  \- dated repository statistics.
&#x20;  Fabricating adoption, sales, or endorsements is forbidden.
7\. Remove internal process language (review passes, agent workflow, CI history)
&#x20;  from the proposal. Keep verification claims short and true.

Also:
\- Update evidence-sheet.md to match; keep it conservative.
\- Update sample-chapters.md to describe what each sample demonstrates.
\- Build \`proposal\`, \`proposal-sample-pdf\`, \`proposal-package\`; record page counts.

\## Phase 4 — Restructure plan (approval gate)
Write RESTRUCTURE-PLAN.md proposing a consolidated TOC with a word budget per chapter
that reaches the total target. Evaluate these candidate merges and argue for or
against each one:
\- Chapters 5–7 → 2 chapters;
\- Chapters 8, 10, 11 → 1 chapter on network families;
\- Chapters 16–17 → 1 chapter;
\- Chapters 29–31 → 1 "SNode.C in larger systems" chapter;
\- Chapter 4 (reading the framework source) and Chapter 38 (extending the framework)
&#x20; → a contributor-oriented appendix.

Also include:
\- an old→new chapter map;
\- every manual "Chapter N" reference affected;
\- index and figure impact;
\- the risk to the capstone progression.

Do not edit the manuscript in this phase. End with status "awaiting author approval".

\## Phase 5 — Execute approved restructure and full condensation
Start only after the author's approval is recorded in EDITORIAL-WORK-PLAN.md.
\- 5a:
&#x20; \- apply only the approved plan;
&#x20; \- update book-files.txt, part files, STRUCTURE.md, README positioning, and every
&#x20;   cross-reference;
&#x20; \- add a check that every "Chapter N" reference resolves to the intended chapter,
&#x20;   using the old→new map;
&#x20; \- rebuild and rerun all checks.
\- 5b, 5c, …: one Part per session.
&#x20; \- Condense that Part's chapters to their word budgets with the Phase 1–2 rules.
&#x20; \- Add exercises.
&#x20; \- Rerun all checks.
\- The final sub-phase also regenerates the proposal TOC and page counts.

\## Phase exit criteria
Phase 0:
\- scope revision committed in AGENTS.md and EDITORIAL-WORK-PLAN.md;
\- PROMPT.md stored;
\- ci/manuscript-metrics.py committed;
\- metrics-before.json reproduces the baseline figures, or records the difference;
\- REPORT.md status table exists.
Phase 1:
\- forbidden-phrase hits = 0, with guards active in check-source-hygiene.sh;
\- "Closing perspective" = 0;
\- snodec-rule ≤ 12;
\- one shell fence label;
\- hygiene, source-alignment, companion builds, and pdf target pass.
\- Global word and heading targets are NOT required yet; report the delta.
Phase 2, for each of Ch. 1, 3, 23, 35, 37:
\- prose words reduced by ≥ 20%;
\- average section length ≥ 250 words;
\- 3–5 exercises, with solutions that build.
Also:
\- Comparison-AsioEcho builds in CI;
\- chapter-ledger.md is complete for all five chapters.
Phase 3:
\- the proposal contains all 7 required sections;
\- every comparable title is verified, with its source recorded in REPORT.md;
\- the proposal, proposal-sample-pdf, and proposal-package targets build;
\- page counts recorded.
Phase 4:
\- RESTRUCTURE-PLAN.md complete;
\- no changes under manuscript/ in this phase (verify with git diff);
\- status "awaiting author approval".
Phase 5a:
\- approved TOC applied;
\- cross-reference check passes;
\- full build passes.
Phase 5b onward:
\- that Part meets its chapter word budgets and the exercise requirement;
\- all checks pass.
\- The final sub-phase must also meet every global target.

\## Working rules
\- Existence is not execution. Every claim in REPORT.md cites the file path and line,
&#x20; the diff, the metrics delta, or the build log that proves it. Distinguish:
&#x20; \- edited and reread;
&#x20; \- edited, not yet reread;
&#x20; \- built;
&#x20; \- run;
&#x20; \- not verified.
\- Refine existing passages. Do not replace chapters with generic new prose. Match
&#x20; the author's voice.
\- Keep printed complete listings and companion files identical (snodec-source
&#x20; markers); run check-source-alignment.py after every listing change.
\- Never squash away the scope-revision commit.


Run Phase 0 only now.
