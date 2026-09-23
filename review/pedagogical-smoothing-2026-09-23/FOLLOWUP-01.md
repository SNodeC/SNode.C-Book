Follow-up 01: accept the source re-baseline to SNode.C 8b8da56 and resume the
pedagogical-smoothing pass

Store this message verbatim as
review/pedagogical-smoothing-2026-09-23/FOLLOWUP-01.md. It is an author
instruction. It amends the scope of review/pedagogical-smoothing-2026-09-23/PROMPT.md,
which stays byte-for-byte unchanged, and resumes the run that stopped at P0b.
Record this scope change in this pass's work-plan section.

1\. Decision
The P0b stop was correct. It was caused by framework drift, not by a book defect.
The author's tree is now clean at 8b8da56e0349191d4658ca8f820a490539eccd4d. That
commit is public on origin/master, still declares version 2.0.0, and is nine
commits past the recorded base 1f0f728.
\- The first six commits contain what the recorded patch captured.
\- Three commits are new: asynchronous logging (e78433d4), semantic log rendering
&#x20; on an async worker (84ff7aab), and -fno-gnu-unique (8b8da56e).
The author accepts re-pinning the book to 8b8da56 now. Readers will check out one
public commit and apply no patch.

2\. Run shape
Continue on book/pedagogical-smoothing-2026-09-23 from its tip (965bcbc).
P0a and P−1 are complete and stay as they are. Run Phase R below, then P0b again,
then P1–P7 exactly as PROMPT.md specifies, with the amendments in section 5.
The run is autonomous: commit at each gate, ask for no author approval, do not
squash.

3\. Phase R: source re-baseline (its own commits)

R0 Preconditions. Stop if any of these fails.
\- In the author's tree (/home/voc/projects/snodec/snode.c), HEAD must be
&#x20; 8b8da56e0349191d4658ca8f820a490539eccd4d and `git status --porcelain=v1` must
&#x20; be empty.
\- Write framework-freeze-R0.json using the P0a method. It must equal the P0a
&#x20; record.
\- Confirm that 8b8da56 is reachable from the public origin/master. Clone
&#x20; [https://github.com/SNodeC/snode.c.git](https://github.com/SNodeC/snode.c.git) into a temporary directory under the
&#x20; book's build directory to do this. Never fetch, build or write anything inside
&#x20; the author's tree.

R1 Pin. Commit: "source-baseline: pin SNode.C 2.0.0 at 8b8da56".
\- In source-baseline/book-source-baseline.env:
&#x20; \- set SNODEC\_REF and SNODEC\_COMMIT to the full 8b8da56 SHA;
&#x20; \- keep SNODEC\_VERSION at 2.0.0;
&#x20; \- set SNODEC\_BASELINE\_RECORDED to the run date;
&#x20; \- set SNODEC\_SOURCE\_LINE to public-commit;
&#x20; \- update the comment.
\- Regenerate source-baseline/framework-working-tree.json with the existing
&#x20; method and file-set rule:
&#x20; \- the file set is every tracked file plus every untracked, non-ignored file;
&#x20; \- each entry is the SHA-256 of the file's content;
&#x20; \- tree\_sha256 is computed over the sorted "digest  name" lines, exactly as
&#x20;   ci/check-source-alignment.py computes it.
&#x20; Set base\_commit and current\_head to 8b8da56 and working\_tree\_status to [].
&#x20; Expect 1,447 files.
\- Make source-baseline/framework-working-tree.patch an empty file and set
&#x20; patch\_sha256 to its digest. Keep the file, and keep the checker's patch check
&#x20; unchanged.
\- An empty `git apply` fails, so remove every reader-facing and CI-facing patch
&#x20; application:
&#x20; \- manuscript/chapters/02-preparing-your-environment.md: the `git apply` lines
&#x20;   at old 136 and 154. Replace them with a checkout of the pinned commit, using
&#x20;   minimal wording.
&#x20; \- source-baseline/SOURCE-VERSION.md and source-baseline/book-source-baseline.md.
&#x20; \- .github/workflows/companion-examples.yml: apply the patch only if the file
&#x20;   is non-empty.
\- Replace every live mention of 1f0f728 (full or short form), and every mention
&#x20; of the working-tree patch as the reader's source authority. This covers
&#x20; README.md, source-baseline/\*, manuscript/frontmatter/preface.md,
&#x20; review/proposal/\*, and any other live file that grep finds. Historical review
&#x20; folders stay unchanged.

R2 Anchors. Commit: "verification: re-anchor source claims to 8b8da56".
In review/verification/source-claims.json, change only these line numbers. Each
needle has been confirmed at the new line. Record numbers use the pre-split
chapter numbering.
&#x20; record 5   src/core/EventLoop.cpp:321          -> 323
&#x20; record 12  src/utils/Config.cpp:1070           -> 1071
&#x20; record 13  src/Log.h:73                        -> 72
&#x20; record 13  src/utils/Config.cpp:536            -> 537
&#x20; record 13  src/utils/Config.cpp:818            -> 819
&#x20; record 13  src/Log.h:173                       -> 202
&#x20; record 13  src/log/SemanticLogger.cpp:697      -> 728
&#x20; record 24  src/utils/Config.cpp:1070           -> 1071
&#x20; record 25  src/CMakeLists.txt:130              -> 131
Change no path or needle, drop no anchor, and verify each one against the
author's tree.

R3 Claim review. Commit "manuscript: reconcile claims with asynchronous logging"
only if a claim actually changes.
\- Scope: every book claim that depends on one of the 11 changed files or on
&#x20; logging behavior.
&#x20; \- The changed files: src/Log.h, src/log/Log.cpp, src/log/Logger.h,
&#x20;   src/log/Logger.cpp, src/log/SemanticLogger.h, src/log/SemanticLogger.cpp,
&#x20;   src/log/detail/SpdlogBackend.h, src/log/detail/SpdlogBackend.cpp,
&#x20;   src/core/EventLoop.cpp, src/utils/Config.cpp, src/CMakeLists.txt.
&#x20; \- The behaviors: record timing and ordering; deferral before start
&#x20;   (Logger::defer in ConfigRoot, and startAsync at start and in free()); pending
&#x20;   records discarded when bootstrap fails (discardPending); flushing at
&#x20;   shutdown; hexDump; the early return at a disabled level; -fno-gnu-unique.
&#x20; \- The chapters: logging (old 13), runtime (old 5), configuration (old 12) and
&#x20;   testing/debugging (old 27), plus every lab or smoke test that reads log
&#x20;   output.
\- Already confirmed, recheck quickly:
&#x20; \- hexDump copies the caller's bytes into the record before returning, so
&#x20;   old ch13:285 stays true;
&#x20; \- a disabled hexDump returns before any formatting, so old ch13:299 stays true.
\- Correct only claims that are now false. Keep each correction local and in the
&#x20; author's voice.
\- Log every claim you check (book file:line, source file:line, verdict) in
&#x20; R-claim-review\.md.
\- A claim whose anchors all lie in files that are byte-identical between the old
&#x20; manifest and the new tree is carried forward; state this in the log.
\- After the review, set reviewed\_tree\_sha256 in source-claims.json to the new
&#x20; tree digest.

R4 Build against the pinned source.
\- Export the pinned tree with `git -C <author tree> archive 8b8da56...` into the
&#x20; book's build directory. Build and install it there under a new prefix, for
&#x20; example build/rebaseline-8b8da56/install-gcc. Use ci/build-companion-examples.sh
&#x20; where it supports this.
\- The 2026-09-22 installation is no longer evidence for this run.
\- If a lab or smoke test fails against the new installation:
&#x20; \- You may adjust a companion driver only when the failure comes from the timing
&#x20;   of asynchronous log delivery and the observable contract the lab asserts stays
&#x20;   the same. Never weaken an assertion.
&#x20; \- A failure that reveals a framework defect or a changed contract stops the run.
&#x20;   Framework changes are out of scope.
\- Repeat the freeze record. It must still match R0.

R gate. Phase R is complete when the full P0b check set passes against the new
installation, including
`check-source-alignment.py --framework /home/voc/projects/snodec/snode.c` with
zero errors. Iterate inside R's scope until it does. Then commit the R evidence:
"review: re-baseline evidence".

4\. Resume
Run P0b again: save metrics-before-resume.json, give its logs a -resume suffix,
and commit. Then run P1–P7 as PROMPT.md specifies.

5\. Amendments to PROMPT.md for the resumed run
\- Source authority is the pinned, frozen 8b8da56 tree. The freeze checks at P3
&#x20; and P7 must match R0.
\- D3: readers no longer need any patch steps. The Ch2 "Edition and source
&#x20; baseline" sidebar holds the pin (commit and version), the checkout command, and
&#x20; the maintainer alignment check. Read the Ch2 row's "patch and alignment
&#x20; mechanics" in that sense.
\- Evidence locations: Phase R may shift lines in Ch2 and in any chapter R3
&#x20; touches. Locate evidence by its content (PROMPT.md §0).
\- Build and runtime evidence comes only from the new installation.
\- The budget thresholds (107,338 / 112,338 / 115,000) and the chapter floors and
&#x20; caps stay absolute as written. Token changes from Phase R count toward them.
\- The stop evidence is historical: P0b-\*.log, P0b-\*.json, metrics-before.json,
&#x20; metrics-after.json, and the current REPORT.md content. Keep those files.
&#x20; Rewrite REPORT.md for the whole run, with a "Run history" section summarizing
&#x20; the P0b stop and its resolution by this follow-up.
\- Phase R stops if:
&#x20; \- the author's tree is not clean at 8b8da56;
&#x20; \- 8b8da56 is not public on origin/master;
&#x20; \- a claim has become false and cannot be corrected locally;
&#x20; \- a lab failure indicates a framework defect or a changed contract.
&#x20; All PROMPT.md §14 conditions apply for the rest of the run.

6\. Operational
When the run ends, whether completed or stopped, push the work branch to origin.
Do not merge it, and do not push to SNode.C-2.0-refinement.

Final message, short and factual:
\- Outcome: completed, or stopped at \<phase> with the condition that stopped it.
\- Commit SHA for each gate: R1, R2, R3 (if any), R evidence, P0b-resume, P1–P7.
\- Source-alignment result.
\- Labs passed, n/62, against the new installation.
\- Global tokens before and after, against 107,338 / 112,338 / 115,000.
\- Result of check-smoothing.py.
\- Floor and cap waivers.
\- Open, qualified and blocked items.
\- Path to REPORT.md.
