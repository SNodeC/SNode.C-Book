Follow-up 13: final polish and freeze gate

Store this message verbatim as
review/pedagogical-smoothing-2026-09-23/FOLLOWUP-13.md. It is an author
instruction. PROMPT.md, FOLLOWUP-01, FOLLOWUP-11 and FOLLOWUP-12 remain the
governing scope; this follow-up adds only the items below. Record it in the
work plan.

0. Starting point and rules

- Continue on book/pedagogical-smoothing-2026-09-23 from its current tip.
  Line numbers below refer to b98eb4a; if the tip is newer, locate each
  passage by its content.
- Framework freeze: 07ca9a2936ee72582df7d159cb06666fe23e30f8.
  - The untracked porting/ directory in the author's tree is outside the source
    authority. Ignore it; never modify the author's tree.
  - At start and end, compare these against framework-freeze-R2.json: HEAD,
    `git status --porcelain=v1` minus the "?? porting/" entry, the digest of
    `git diff HEAD --binary`, and the untracked files outside porting/.
  - Run ci/check-source-alignment.py against a fresh public clone checked out at
    that commit.
  - Any other change to the author's tree stops the run.
- Scope: exactly the items in section 1. No structural changes and no new
  manuscript code.
- Every edit is local and keeps the author's voice. Keep every technical claim;
  verify any statement you change against the frozen source.
- Size: roughly neutral. Total at most 115,000 tokens; each chapter within its
  cap (5% waivers as in PROMPT.md §4).
- Deliberate reinforcement is part of the teaching method. Compress repetition
  only where it adds nothing; never remove a distinction the chapter exists to
  teach.
- One commit per item group (A–I), then one evidence commit.

1. Items (file:line at b98eb4a)

A. Real errors

- appA:110: change "the source-reading introduction in Chapter 4" to
  Chapter 5, where "Reading public types and components" now opens.
- ch13:152: `echo local --port 8080` must use the instance `echoserver`, in the
  same command form the chapter uses elsewhere.
- ch31:186: fix the grammar of "perform the same startup work … that
  `MiniGatewayMqttClient.*` plays" while keeping its meaning.

B. Terminology (register row 1). Decide by meaning, not by search-and-replace.

- "role": keep it where it means a system or application responsibility.
  Change it where it denotes an instance, a server/client side or another
  runtime object:
  - how-to-read:5 and :24
  - the Part V opener ("the echo role") and the Part VI opener
  - ch14:16, :155, :223
  - ch16:181, :235
- "stream modes" (ch03:508, ch25:197, ch27:41), "connection mode" (ch12:194;
  appA:79, :131, :137) and "legacy or TLS mode" (ch29:325): use "connection
  variant", or "transport form" where the transport is meant.
- "address family" (ch26:249): use "network family"; it refers to the book's
  abstraction.
- "configured instance" (ch03:59, ch04:206, ch05:92): simplify to "instance"
  only where the adjective adds nothing.
- ch08:292 "Instance callbacks": use the same term as the table at ch08:258,
  or change both consistently. Align the rule box at ch08:309 too.
- Record every kept "role" in terminology-allowlist.md with a one-line reason.

C. Register row 26

- ch07:248: replace "that claim" with the claim itself: the protocol does not
  depend on the network family.

D. Redundancy (row 33), by selective compression. A ● for row 33 means that
the remaining repetition is pedagogically purposeful. It does not mean
every repeated concept has been eliminated.

- Ch1: teach the sequence-number example once. Merge ch01:44 into the runway
  (ch01:29-37) or reduce it to a brief reminder.
- Ch3: replace the repeated configure/build commands (ch03:452-460) with a
  reference to the Chapter 2 route, plus the one command this chapter needs.
- Ch4: show init/start once (ch04:48-66 vs 152-163). Remove the repeated
  "global protocol singleton" sentence (ch04:132 vs 177).
- Ch7: show the IPv4/IPv6 alias pairs once (ch07:262-276 vs 343-379).
- Ch8: keep the API category table. Replace the code lists that repeat it
  (ch08:167-239) with prose pointing to the table's rows, keeping only what the
  table lacks.
- Ch12: reduce "Echo as the smallest transfer microscope" (ch12:135-179) to a
  short reference to Ch3's listing. Keep one role-endpoint catalogue: the Ch11
  list (ch11:253-263), shortened, with ch12:303-344 referring to it.
- Ch13: show the dotted-key INI example once plus the multi-instance example
  (currently at ch13:93, 159, 461, 584). Use 18091 wherever the example stands
  for the running story's file value.
- Ch18: reduce ch18:247-254 to the test-selection facts; the trace is already
  explained at ch18:64-66.
- Ch21: keep "connection ≠ session ≠ subscription ≠ delivery" prominent in the
  opening and the milestone table. Compress the later restatements
  (ch21:51-53, 251-255) so each adds a new observation instead of repeating the
  claim.
- Ch25/Ch27: keep both trees, since they teach different things. Make Ch27's
  consumer subgraph refer back to Ch25's application tree and state what it adds
  (the build/component view).
- Ch29: remove the restated throughput/latency/tail distinctions (ch29:391-401)
  that repeat ch29:349-351. Keep the concrete experiment.
- Ch32 Exercises 3 and 4: keep the labs but raise the question to synthesis.
  Ask the reader to interpret the Ch4/Ch6 observations against MiniGateway's
  final architecture: acceptance authority, observer lifetime and restart,
  together with the Part XI checkpoint. Do not re-ask the same question.
- Conventions: make the prose at conventions:13 and :17 refer to the glossary
  table instead of restating its rows.

E. Stale or dangling references (row 34)

- ch01:39: reconnect "takes a different path" to its contrast, which is now
  six paragraphs earlier.
- ch02:449: the playground is configured in this chapter, not "in Chapter 3".
- ch21:23: move the subscription instruction after the SUBSCRIBE/SUBACK
  narrative (ch21:27), or fold it into the figure caption.
- ch29:22: fold the former abstract into the new opening (ch29:16-20) or
  remove it.

F. Slips and register (row 35)

- ch13:93 and :159: covered by D.
- ch03:232: "can log them … and sends" becomes "logs them … and sends".
- ch01:164: "node.js" becomes "Node.js".
- ch16:194: "Retry is policy, not morality." becomes "Retry is an operational
  policy, not an automatic improvement."
- ch02:138, ch02:173 and further-reading:58: write "SNode.C 2.0.0" instead of
  SNode.C\textsubscript{\texttt{2.0.0}}. Check the manuscript for any other
  occurrence.
- ch26:110-138: immediately above the block, add the label "Illustrative role
  map — not SNode.C configuration syntax".

G. Apparatus and placement (row 36)

- Ch25 "What to remember" (ch25:289-291): 3–5 bullets covering the reading
  order, the entry point as assembly point, and source versus tested behavior.
- Ch5 "What to remember" (ch05:241-244): at least 3 bullets.
- Ch20 (ch20:389-391): put the component/header note in the standard
  `::: {.snodec-note title="Build note"}` box; the transition stays outside it.
- Ch13 (ch13:630) and Ch14 (ch14:337): move the public-answer pointer to the
  end of the exercise block, as in every other chapter.
- Appendix A (appA:322-341): move "Observed descriptor populations" directly
  after "Following a public type into the runtime" (appA:52-94), or add a
  bridging paragraph that states its purpose. Keep its anchor.

H. Cadence and style (row 37)

- Smooth runs of one-sentence paragraphs and bullets locally, without creating
  overloaded paragraphs:
  - ch08:157-247
  - ch10:253-324
  - ch12:351-383
  - ch13:222-328
  - ch23:42-72
- ch27:274-294 lists the actual default-value compile definitions a packager
  can set. Keep all 19 names, but present them compactly (one inline list or a
  compact two-column table) instead of a 19-line bullet run.
- Ch30: the post-listing sentences share one template ("… now …; the next …
  below …"). Vary about five of them, keeping each one's content: the
  responsibility implemented, what it does not know, the invariant, and why the
  next file follows.

I. Companion CI (freeze gate)

- Symptom: in the companion-examples workflow, exercise-ch06-deferred-work and
  exercise-ch09-selectors fail with loader errors on both GCC and Clang
  (installed SNode.C libraries not found at runtime); 64 of 66 labs pass.
- Confirm the cause from the CI logs, or by reproducing the workflow's ctest
  step exactly as it runs:
  - companion-examples.yml:84 sets no library path;
  - ci/build-companion-examples.sh:34 does;
  - Chapter 28 documents that DT\_RUNPATH covers only direct dependencies.
- Fix the cause once, at the companion build/test configuration level, for all
  exercise targets: for example, a shared helper that sets the test
  environment's library path from SNODEC\_PREFIX, or the linker policy used by
  Chapter 28's lifecycle lab.
- Change no assertion, timeout or test logic.
- If the chosen policy affects what Chapter 28 says about loader paths, keep the
  chapter consistent with it.
- Verify with GCC and with Clang by running the workflow's commands locally.
  After pushing, record the hosted run results if they can be observed;
  otherwise mark them "hosted CI pending".

2. Checks

- Fix check-polish.py assertion 2: exempt the Conventions glossary table and
  Appendix A's two-row reading path, and keep the rule everywhere else.
- Add check-final.py, asserting:
  - Appendix A contains no "introduction in Chapter 4" and names Chapter 5 for
    the type/header/component comparison;
  - Ch13 contains no "echo local --port";
  - none of these remain: "stream modes", "connection mode", "legacy or TLS
    mode", "Retry is policy, not morality", "node.js",
    "\textsubscript{\texttt{2.0.0}}";
  - item B's old-sense role phrases are gone outside the allowlist;
  - Ch25 and Ch5 each have at least 3 recap bullets;
  - Ch20 contains a Build note box;
  - each chapter's answer pointer is the last content line of its exercise
    block;
  - the Ch26 illustrative label is present;
  - Appendix A's descriptor section follows the runtime-reading section or is
    preceded by a bridge paragraph;
  - Ch32 Exercises 3 and 4 differ from the Ch4 Ex3 and Ch6 Ex4 questions.
- check-final.py guards mechanically testable regressions. Do not distort
  otherwise correct prose or Markdown structure to satisfy a brittle assertion.
  When the manuscript meets the intended rule, improve the checker instead.
- Then run:
  - check-smoothing.py, check-polish.py and check-final.py;
  - ci/manuscript-metrics.py and ci/check-chapter-references.py;
  - ci/check-source-alignment.py against the fresh clone at 07ca9a29;
  - ci/check-source-hygiene.sh;
  - ci/build-book-package.sh (PDF);
  - the companion build and all labs, with GCC and with Clang, exactly as the
    workflow runs them.

3. Report: FINAL-POLISH-REPORT.md

- Status matrix: 37 rows × 8 dimensions (●/◐/○), with file:line evidence for
  every cell that changed. Target all ●; explain any cell left ◐.
- Freeze-gate table:
  - matrix all ●;
  - book package green, with PDF page count;
  - companion labs 66/66 on GCC and 66/66 on Clang, local results and hosted
    status;
  - frozen-source alignment green.
- Tokens before/after, for each chapter touched and in total.
- Check results, the freeze comparison, and the commit SHA for each item group.

4. Operational
   Push the work branch when done. Do not merge.

Final message, short:

- commit SHAs for A–I;
- matrix totals per dimension;
- freeze-gate status;
- tokens and page count;
- anything not closed, with the reason.

After this pass the manuscript is frozen for publisher submission. Do not start
further broad refinement. A later follow-up is justified only by an actual
technical error, broken build, broken reference or production defect.
