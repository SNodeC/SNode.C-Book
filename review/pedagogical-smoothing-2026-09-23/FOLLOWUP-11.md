Follow-up 11: consolidate scope, re-pin to SNode.C 07ca9a29, finish P1 from the
snapshot, then run P2–P7

Store this message verbatim as
review/pedagogical-smoothing-2026-09-23/FOLLOWUP-11.md. It is an author
instruction. PROMPT.md stays unchanged.

1. Authoritative scope from now on

- The authoritative scope is PROMPT.md, as amended by FOLLOWUP-01 §5 and by
  this follow-up. Wherever FOLLOWUP-01 says 8b8da56, read 07ca9a29.
- FOLLOWUP-02 through FOLLOWUP-10 are historical. Their verification tasks are
  complete; do not act on them. No timeout changes and no test adaptations are
  authorized.
- The only companion change carried forward from those follow-ups is the driver
  fix in 2e71f2a: the ch12 checkpoint reads the completed log after normal
  shutdown, and its assertions are unchanged.
- Keep every existing commit. Continue from a2ecd9c.

2. Framework freeze

- Source authority: /home/voc/projects/snodec/snode.c, clean at
  07ca9a2936ee72582df7d159cb06666fe23e30f8 and public on origin/master.
- Record framework-freeze-R2.json at the start, using the P0a method. The record
  must stay identical until P7.
- If the tree changes at any point, stop and report. Do not re-pin and do not
  investigate framework behavior. A framework defect also stops the run.

3. Phase R2: re-pin to 07ca9a29
   Use the method of FOLLOWUP-01 §3 (R0–R4), in its own commits, with these
   specifics.

- Pin

  - Update book-source-baseline.env.
  - Regenerate the manifest: 1,448 files; base\_commit and current\_head both
    07ca9a29; working\_tree\_status []; empty patch.
  - Replace every live mention of 8b8da56, full or short: README.md,
    source-baseline/*, preface.md, Ch2, review/proposal/*, and any other live
    file that grep finds.

- Anchors (in record 5; record numbers are pre-split)

  - src/core/EventLoop.cpp:224 "TickStatus EventLoop::tick" -> 244
  - src/core/EventLoop.cpp:323 "bool EventLoop::reconfigure()" -> 343
  - src/core/EventLoop.cpp:215, needle "eventLoopState == State::RUNNING ||
    eventLoopState == State::STOPPING": this needle no longer exists. Re-anchor
    to line 224 with the needle "(eventLoopState == State::RUNNING &&
    stopsig == 0) || eventLoopState == State::STOPPING".
  - Verify that every other anchor still matches. Change nothing else.

- Claim review (log it in R2-claim-review\.md)

  - The three new framework commits:
    - 9746d186: drain asynchronous logs during shutdown;
    - 55c36e41: keep process signals on the event-loop thread;
    - 07ca9a29: simplify asynchronous logging synchronization.
  - Changed source files: src/core/EventLoop.cpp and .h, src/log/Logger.cpp and
    .h, src/log/detail/SpdlogBackend.cpp and .h.
  - Known behavior changes:
    - The signal handler only records the signal.
    - \_tick logs the signal and calls stop() on the event-loop thread.
    - \_tick dispatches the multiplexer only while RUNNING with no pending stop
      signal, or while STOPPING.
    - free() ends with Logger::shutdown(), which drains pending asynchronous
      records.
  - Known false claim: old ch05:89, about when \_tick dispatches.
  - Also review:
    - the signal and shutdown statements in old chapters 5, 9 (the signal-close
      case), 14, 15 and 27;
    - every statement about log output at shutdown.
  - Correct only claims that are false, and keep each correction local.

- Build and run

  - Export 07ca9a29 with git archive into the book build directory. Build it and
    install it to a new prefix.
  - Run the full P0b check set against that installation. Required:
    - source alignment with zero errors;
    - 62/62 labs;
    - all smoke and lifetime suites;
    - the framework tests, recorded as build evidence.
  - Change no timeout and no assertion.
  - Then set reviewed\_tree\_sha256 to the new tree digest.

4. P1: finish from the snapshot
   The vocabulary edits in a2ecd9c are the basis for P1. They were not made in one
   sitting, so reread every changed passage in its context before gating.

- Check each substitution for technical precision: handle vs instance vs named
  instance vs flow, and network family vs connection variant. Correct errors;
  do not revert wholesale.
- Resolve the remaining context-dependent terms:
  - "communication role" (22 occurrences);
  - "server instance" and "client instance" (7 together);
  - "server role" and "client role" (3 each).
    Keep a term only where it means a system-design role. Otherwise use the
    canonical term.
- "carrier" may remain only in:
  - the two MQTT chapters;
  - the Conventions glossary entry;
  - the preserved anchor IDs #carrier-and-protocol-decisions and
    \#choosing-the-carrier-at-each-boundary.
    List every remaining use in terminology-allowlist.md.
- Write terminology-counts.md, comparing c7b76c1 with the end of P1.
- Regenerate metrics-after-P1.json from a fresh measurement.
- Run the chapter-reference, source-alignment and hygiene checks.
- Commit the P1 gate.

5. P2–P7
   Run P2–P7 exactly as PROMPT.md specifies, with the FOLLOWUP-01 §5 amendments,
   pinned at 07ca9a29. The budget thresholds stay absolute: 107,338 / 112,338 /
   115,000. Tokens already added in P1 count toward them.

6. Stop conditions
   PROMPT.md §14 applies, and the run also stops if:

- the framework freeze record changes;
- a framework defect appears;
- a claim has become false and cannot be corrected locally.
  On a stop, report and end the run. Do not wait for, or investigate, framework
  changes.

7. REPORT.md
   Rewrite it for the whole run, beginning with a concise run history:

- the P0b stop;
- Phase R at 8b8da56;
- the 9746d186–07ca9a29 framework investigation, in a few lines with links;
- Phase R2 at 07ca9a29.
  Keep all historical files.

8. Operational
   When the run ends, push the work branch. Do not merge. The final message
   follows FOLLOWUP-01 §6, listing the R2 commits in place of the R commits.
