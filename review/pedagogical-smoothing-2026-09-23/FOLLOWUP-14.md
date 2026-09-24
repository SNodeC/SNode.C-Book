Follow-up 14: close the remaining matrix cells and the CI gate

Store this message verbatim as
review/pedagogical-smoothing-2026-09-23/FOLLOWUP-14.md. It is an author
instruction. PROMPT.md, FOLLOWUP-01, FOLLOWUP-11, FOLLOWUP-12 and FOLLOWUP-13
remain the governing scope; this follow-up adds only the items below. Record
it in the work plan.

This follow-up exists because Follow-up 13 introduced two errors (a wrong
article and swapped chapter references) and left the CI gate open. It
qualifies under the rule agreed for Follow-up 13: a later follow-up only for
an actual error, broken reference or broken build. After it, the manuscript is
frozen.

0. Starting point and rules
- Continue on book/pedagogical-smoothing-2026-09-23 from d4ff44d or its
  current tip. Line numbers refer to d4ff44d; locate each passage by its
  content if the tip is newer.
- Framework freeze: 07ca9a2936ee72582df7d159cb06666fe23e30f8, with the same
  rules as Follow-up 13:
  - The untracked porting/ directory in the author's tree is outside the
    source authority. Ignore it; never modify the author's tree.
  - At start and end, compare these against framework-freeze-R2.json: HEAD,
    `git status --porcelain=v1` minus the "?? porting/" entry, the digest of
    `git diff HEAD --binary`, and the untracked files outside porting/.
  - Run ci/check-source-alignment.py against a fresh public clone checked out
    at that commit.
  - Any other change to the author's tree stops the run.
- NO CUTS. The author's decision stands: "I do not want to cut the manuscript
  down." Do not delete any teaching passage, listing, example or explanation.
  Where a repetition is involved, add a linking sentence, or turn the second
  occurrence into an explicit reference back that keeps its content.
- Every edit is local and keeps the author's voice. No structural changes and
  no new manuscript code.
- Size: net growth of about 100–400 tokens. Total at most 115,000 tokens; each
  chapter within its cap.
- One commit per item group (A–D), then one evidence commit.

1. Items (file:line at d4ff44d)

A. Errors introduced by Follow-up 13
- ch05:92: "A instance might be…" becomes "An instance might be…".
- Ch32 Exercise 3 (ch32:250) runs `model-ownership`, which is Chapter 6's
  Part II checkpoint lab. Its text says "observations from Chapter 4"; change
  it to Chapter 6.
- Ch32 Exercise 4 (ch32:251) runs `model-instances`, which is Chapter 4's lab.
  Its text says "Use the Chapter 6 model observations"; change it to
  Chapter 4.
- Verify both mappings against companion/exercises/ch04, ch06 and ch32
  (CMakeLists.txt and README.md) before editing. Also check that the ch32
  README's wording matches.

B. Terminology residue (register row 1). Decide by meaning.
- ch26:251: "security mode (`legacy`/plain or TLS)" becomes "connection
  variant (`legacy`/plain or TLS)".
- ch29:347: "protocol/security mode" becomes "protocol and connection variant".
- ch30:1134 and :1136: the instance is named, and the role is what it
  realizes. Example wording: "The web role is realized by the instance named
  `web`…"; "The instance name `mqtt-uplink` identifies the MQTT integration
  role in configuration and diagnostics." Keep the configuration example
  unchanged.
- Update terminology-allowlist.md if any kept "role" changes status.

C. Register row 33: link repetitions without cutting.
   A ● for row 33 means every remaining repetition is purposeful or
   explicitly linked. Make these seven explicit:
- conventions:13: keep the sentence, and tie it to the glossary, for example
  "Role, defined in the glossary below, is a design responsibility…". Do not
  delete the glossary row.
- ch03:452-460: before the configure/build block, add one sentence saying the
  build already exists if the reader followed Chapter 2's shortest path, and
  that these commands repeat it for a fresh playground.
- ch04:177: the sentence "It should not be used as a global protocol
  singleton." repeats ch04:132. Turn it into a reference back, for example "As
  noted above, it is not a global protocol singleton." Also introduce the
  second init/start snippet (ch04:152-164) as the same two calls seen above,
  now placed in the startup sequence. Keep both snippets.
- ch07:
  - Introduce the full comparison at ch07:341-379 as extending the alias pair
    shown at ch07:262-274 with instance names and activation calls. Keep both.
  - The second "Chapter 8 develops…" sentence (ch07:528) should either say
    what Chapter 8 adds for pathname sockets or refer back to the earlier
    pointer at ch07:414. Do not merely repeat it.
- ch12:135-179: open "Echo as the smallest transfer microscope" with a pointer
  to the complete Chapter 3 listing, and say that the snippets are repeated
  here to show the transfer boundary. Keep the snippets.
- ch18:247: introduce the framework-test paragraph as the counterpart of the
  trace at ch18:64-66, for example "The framework test checks the trace
  followed above…", and state what it adds: the `/outside` 404 case and the
  counted handler visits.
- ch29:391-395: add a transition marking the move from the single-run
  experiment to general benchmarking distinctions, for example "Beyond this
  single run, …". Keep those paragraphs.

D. Companion CI gate (freeze gate)
- Background:
  - Follow-up 13's commit I (f19a658) added a shared inherited-RPATH policy
    for Linux exercise targets.
  - Local verification stopped because the frozen framework does not build
    with local Clang 21.1.8: `-Werror,-Wnrvo` in
    src/tools/snodec-control/src/ConfigActions.cpp:296.
  - That is a framework-side compatibility issue with a newer compiler, not a
    book defect. Do not patch the frozen framework.
- Read the hosted companion-examples results for f19a658 and for the later
  evidence commit (run 36002150169 and its successor). Use `gh` if available;
  otherwise use the Actions pages that can be fetched. Record the GCC and
  Clang versions each job used and every job's conclusion.
- If a hosted job fails because a lab cannot find a shared library at run
  time: fix the cause once, at the shared companion build/test configuration
  level. Change no assertion, timeout or test logic.
- If the hosted Clang job fails only because the frozen framework does not
  compile with that compiler (-Wnrvo or similar): pin the workflow's Clang to
  the Ubuntu 24.04 distribution version with which the frozen framework
  builds. Record the reason in the workflow comment and the report. Do not add
  warning-suppression flags to the framework build without an explicit author
  decision; if pinning is not possible, stop and report the options.
- Local verification:
  - Run the workflow's commands with GCC and with the Clang version the
    workflow uses: framework build, companion build, all 66 labs.
  - Record local Clang 21 as a known framework incompatibility (framework
    follow-up), not as a book failure.
- Push, then record the hosted run results. Mark them "hosted CI pending" only
  if they cannot be observed.

2. Checks
- Extend check-final.py with regression guards:
  - no "A instance";
  - Ch32 Exercise 3 names `model-ownership` together with Chapter 6, and
    Exercise 4 names `model-instances` together with Chapter 4;
  - no "security mode";
  - no "role is named";
  - the Ch3, Ch4, Ch7, Ch12, Ch18 and Ch29 link sentences are present, where
    this can be tested without brittle wording.
- check-final.py guards mechanically testable regressions. Do not distort
  correct prose or Markdown to satisfy a brittle assertion; when the
  manuscript meets the intended rule, improve the checker instead.
- Then run:
  - check-smoothing.py, check-polish.py and check-final.py;
  - ci/manuscript-metrics.py and ci/check-chapter-references.py;
  - ci/check-source-alignment.py against the fresh clone at 07ca9a29;
  - ci/check-source-hygiene.sh;
  - ci/build-book-package.sh (PDF);
  - the companion build and all labs, as described in D.

3. Report: FOLLOWUP-14-REPORT.md
- The status matrix: 37 rows × 8 dimensions (●/◐/○), with file:line evidence
  for every cell that changed since FINAL-POLISH-REPORT.md. Target all ●;
  explain any cell left ◐ or ○.
- Freeze-gate table:
  - matrix all ●;
  - book package green, with PDF page count;
  - companion labs 66/66 with GCC and 66/66 with Clang, local results and
    hosted run IDs with compiler versions;
  - frozen-source alignment green;
  - author-tree freeze unchanged.
- Framework follow-up (outside this branch): the Clang 21 -Wnrvo failure at
  ConfigActions.cpp:296, for the next SNode.C release.
- Tokens before/after, for each chapter touched and in total, and the commit
  SHA for each item group.

4. Operational
Push the work branch when done. Do not merge.

Final message, short:
- commit SHAs for A–D;
- matrix totals per dimension;
- freeze-gate status, with hosted run IDs;
- tokens and page count;
- anything not closed, with the reason.

After this pass the manuscript is frozen for publisher submission. A further
follow-up is justified only by an actual technical error, broken build, broken
reference or production defect.