Follow-up 15: one refinement pass — HEAD sources, factual corrections, production fixes, linked copy-edit

Store this message verbatim as review/pedagogical-smoothing-2026-09-23/FOLLOWUP-15.md. It is an author instruction. PROMPT.md and FOLLOWUP-01, -11, -12, -13 and -14 remain the governing scope, except where §0 overrides them. Record it in the work plan. This follow-up reopens the frozen manuscript by author decision. Afterwards it is frozen again.

0. Starting point and rules

- Book repository: main is a strict ancestor of book/pedagogical-smoothing-2026-09-23. Fast-forward main to the branch tip with --ff-only; stop if that is not possible. Push, then do this pass on main.
- SOURCE RULE (overrides every framework-freeze and pin rule in FU-11 to FU-14):
  - Never pin any repository to a commit or tag.
  - Always use default-branch HEAD: SNodeC/snode.c master, SNodeC/MQTTSuite master, SNodeC/OpenWRT main, SNodeC/SNode.C-Book main.
  - No commit SHA or tag may appear as a checkout or fetch target, or as a reader instruction, in:
    - manuscript/, companion/, ci/ and .github/
    - source-baseline/\*.env and source-baseline/SOURCE-VERSION.md
  - Observed HEAD SHAs are evidence only. Record them in the report at start and end, never as targets.
  - If a HEAD moves during the pass, re-run the affected checks against the new HEAD and report it.
  - Tool and container versions (Pandoc, pandoc-crossref, the TeX Live image, compilers) are not repositories. Keep them fixed but mutually compatible (C1).
- Author framework tree:
  - Never modify it. Ignore porting/.
  - Record HEAD and `git status --porcelain=v1` at start and end. Any change stops the run.
  - This replaces the framework-freeze-R2 digest comparison.
- NO CUTS (unchanged): do not delete any teaching passage, listing, example or explanation. Where a repetition is involved, add a linking sentence, or turn the second occurrence into an explicit reference back that keeps its content.
- Every edit is local and keeps the author's voice. No structural reorganization and no new manuscript code. Correcting or reformatting existing code is allowed only where an item below says so.
- VERIFY FIRST:
  - Before each edit, confirm the finding at HEAD and record file:line evidence.
  - If a finding does not reproduce, skip it and report it.
  - Existence is not execution.
- Line numbers refer to 8328dfc. Locate each passage by content if HEAD has moved.
- Size: total at most 115,000 tokens, with each chapter within its cap.
- Commits: one per item group (A–D), then one evidence commit.

1. Items

A. Source identity on HEAD
A1 Baseline and checker

- source-baseline/book-source-baseline.env: set SNODEC\_REF=master. Remove SNODEC\_COMMIT as a target; commit provenance may remain only inside framework-working-tree.json.
- ci/check-source-alignment.py: today it requires SNODEC\_REF to equal a full SHA, and chapter evidence to contain that SHA. Change it so that:
  - a fresh clone of master HEAD is checked against the manifest's content digests and anchors;
  - chapter evidence references the manifest, not a SHA;
  - on drift it fails and names the changed files ("master has drifted from the edition manifest").
- .github/workflows/companion-examples.yml (L43) and ci/build-companion-examples.sh: build against master HEAD and log the observed SHA.
- source-baseline/SOURCE-VERSION.md: rewrite the reader checkout without a SHA.
  A2 Framework references in the manuscript
- Locations: preface.md:36; ch02:19; the Ch2 "Edition and source baseline" sidebar (ch02:132–187, especially :163, :173, :175–182, :186).
- Readers clone master, then run the alignment checker to confirm the checkout still matches this edition.
- Explain what drift means for the reader and what to do about it. Rewrite ch02:175 ("Do not build … newer checkout") to fit this drift-check model.
- Keep the teaching about separating source, build and install locations.
  A3 OpenWrt (ch28:253–285; further-reading.md:67)
- Evaluate only SNodeC/OpenWRT main HEAD, file net/snode.c/Makefile.
- Facts to re-verify (observed on 25 Sep):
  - PKG\_VERSION:=2.0.0
  - PKG\_SOURCE\_VERSION:=OpenWRT, a snode.c tag three commits behind master
  - spdlog 1.17.0 fetched through a hashed Download/spdlog step, with FETCHCONTENT\_FULLY\_DISCONNECTED=ON
  - net-un-phy is listed and is a valid 2.0 target (snode.c src/net/un/phy/CMakeLists.txt)
- ch28:255–257 is stale and incorrect: it claims 1.0.1, an "OpenWRT branch", an "old net-un-phy", and that a recipe port is required. Rewrite it so that:
  - it links the feed's main branch, with no commit;
  - it tells the reader what to check in the recipe at HEAD (PKG\_VERSION; PKG\_SOURCE\_VERSION versus snode.c master; logger download; module list) instead of asserting a snapshot;
  - it keeps the rehearsal procedure unchanged.
- Re-rate every row of the table at ch28:276–284 against HEAD:
  - logger dependency and component graph: now met by the recipe;
  - source selection: state the recipe's snode.c ref versus master;
  - consumer application and runtime ownership: remain reader/deployment evidence.
- further-reading.md:67: remove "records the inspected OpenWrt feed revision".
- Report only (outside this repo): the feed fetches the tag OpenWRT instead of snode.c master.
  A4 MQTTSuite (ch26:331–343; ch02:186)
- Reference MQTTSuite master HEAD, with no revision.
- Re-verify at HEAD, with file:line evidence:
  - the bridge publication path (mqttbridge/lib/Mqtt.cpp);
  - the store path (mqttstore/lib/Mqtt.cpp and MariaDbStorage.cpp): the raw insert is submitted, and storeProjections does not wait for the raw insert's success callback.
- Add ci/check-external-anchors.py:
  - shallow-clone MQTTSuite master and OpenWRT main;
  - assert that every path and symbol the manuscript names still exists (for example MariaDbStorage::store, storeProjections, net/snode.c/Makefile, PKG\_VERSION 2.x);
  - fail with a clear drift message.

B. Technical corrections
B1 LineProtocol QUIT (ch10:184–214; companion/examples/LineProtocol-Server/LineCommandServerContext.cpp:37–73)

- Problem: after QUIT calls close(), the loop keeps interpreting further buffered lines and queues replies after closure.
- Fix: stop interpreting lines once QUIT requests closure (for example, clear the buffer and return). Apply the same fix in the book listing and the companion.
- Add one sentence near ch10's closure paragraph.
- Add a coalesced "QUIT\nPING\n" case to companion/exercises/ch10/protocol.py. Expect closure and no PONG.
- Re-run the Ch12 and Appendix A labs that use this server.
  B2 Express consumer component (ch25:67–85, :89–119; ch27:181–191, :338–364)
- For installed consumers of \<express/legacy/in/WebApp.h>, teach http-server-express-legacy-in as the canonical component. It is a compiled SHARED library in the framework (src/express/legacy/in/CMakeLists.txt).
- Show the dependency tree from that target.
- Keep the in-tree snode.c fragment unchanged; it matches src/apps/CMakeLists.txt:49. Add one sentence explaining the in-tree versus installed choice.
- Result must agree with ch27:155, :217, :249–251 and every companion Express example.
  B3 Compiler wording (ch02:73–88)
- Separate the minimum accepted by the build (GCC 12.2, Clang 13.0) from the versions verified in this edition's CI (take them from the hosted run).
- State that Clang 21 currently fails the framework build under -Werror (-Wnrvo in src/tools/snodec-control/src/ConfigActions.cpp:296), and that this is a framework follow-up.
  B4 Ch2 install list (ch02:95–112): add libasio-dev to the optional command, labelled "(Chapter 1 comparison lab)". Keep :455–457.
  B5 Ch6 wording
- :109 — "public EventLoop::tick" becomes the internal path reached through SNodeC::tick().
- :120 — rewrite the second sentence plainly.
- :165–169 — the warning box must name the operation: atNextTick queues the callback for a later event-loop turn instead of running it on the caller's stack.
  B6 Ch29:327 — "tools verify architectural lifetime assumptions" becomes "can expose violations of those assumptions on the paths a run executes".
  B7 Ch4:219–228 — state that the omitted prefixes carry echoserver and conn=1, or show one prefixed line.
  B8 APPLICATION macro
- Verify its expansion at src/express/Router.h:68.
- Explain it in one sentence at its first use (ch25:168).
- Add a back-pointer at its first use in ch30 (≈:789).
  B9 Ch21
- :45 — "This broker" becomes "The SNode.C broker implementation".
- :190–206 — explain the four Mqtt constructor arguments in one sentence, after verifying their meaning in src/iot/mqtt/client/Mqtt.h.
  B10 Ch15:148 — put the "verification mode zero without a trust source" fact into a snodec-warning box. Keep the prose.
  B11 Ch31:231–242 — mark /tmp/minigateway-measurements.sock as a teaching default and point to Ch7's path-ownership guidance (ch07:551–570).
  Dropped (refuted): SSE listener re-entrancy. The HTTP server context's SocketContext::onWriteError is a no-op, and detachment is deferred.

C. Production and tests
C1 Pandoc and pandoc-crossref

- Problem: .github/workflows/book-package.yml:30–42 installs Pandoc 3.10.1, but pandoc-crossref v0.3.24a reports "built with Pandoc v3.9.0.2" (verified).
- Select a mutually matching pair and apply it to the local build path as well.
- Add a workflow step that fails when `pandoc --version` differs from the Pandoc version reported by `pandoc-crossref --version`.
- Rebuild the PDF. Compare page count and resolved cross-references with the previous build.
  C2 Listing width
- Problem: 53 fenced code lines exceed 100 characters; 31 are in ch30, and the longest is 170 characters (ch30:593). production/metadata/metadata.yaml:214–217 sets breaklines=true and breakatwhitespace=false, so these lines break mid-identifier in print.
- Determine the frame width from the PDF and record it.
- Reformat the affected companion sources and their exact listings together (formatting only), so that no printed line wraps. Source alignment must stay green.
- Add a guard for the chosen width.
  C3 Flaky Ch7 lab
- Problem: companion/exercises/ch07/family-server.cpp:15 writes IDENTITY to std::cout, which interleaves with asynchronous log output. families.py:49–54 then parses a corrupted line. This was recorded in FOLLOWUP-14-REPORT (hosted run 36002150169).
- Fix: emit the identity record on a channel that logging does not share. Keep every assertion.
- Run the lab at least 50 times with each compiler and report the counts.
  C4 Index
- Remove the duplicate \index{configuration hierarchy} (ch13:211/213) and \index{safe extension} (appendix-a:165/167).
- Normalize split keys to one heading each: "instances" vs "instance!…", and "Unix domain sockets" vs "Unix-domain sockets!…".
  C5 Apparatus
- ch14:326 — make the Part V checkpoint a heading, as in the other Parts.
- ch21:21 — give the figure the same width/placement attributes as its neighbours.
- ch30:1264–1297 — keep the printed README (NO CUTS), but align its configure line with the book's CMAKE\_PREFIX\_PATH convention in both the companion README and the printed copy.
  C6 Further Reading: complete edition, publisher and year for every book entry, verifying each.

D. Linked copy-edit (NO CUTS)
D1 Release-notes voice: remove "now" and historical framing at

- ch10:363 ("now exposes … existing void send surface")
- ch13:560, ch16:263, ch17:266, ch27:302, ch29:125
- appendix-a:307, appendix-a:341 ("an old singleton-controller sketch")
- ch25:270 ("a removed macro interface")
  D2 Ch14 compressed sentences (:132, :225, :229–233, :290–292): expand into plain sentences.
  D3 Repetition links
- ch07:
  - L448–460 (Unix address-class passage) and L464–466 (default construction): make each an explicit reference back to L119–135, keeping its content.
  - L517–532: add one linking sentence for the local/remote restatement.
- ch13: introduce the help block (L395–403), the third INI copy (L448–456) and the parameterless-activation passage (L483–495) as the earlier example seen again at a new step.
- Endpoint-identity tables at ch07:56–62 and ch12:113–121: link back to ch05:108–116. Leave the Ch9 and Ch13 tables; they do different work.
- ch12:159–166: the snippets must match ch03:205–215 exactly, or be labelled "schematic". Prefer exact.
- ch26:53–64 and :99–150: add a back-reference to ch23:175–236 and say what Ch26 adds.
  D4 Seams
- ch32:237: bridge the flow-API paragraph to the chapter's closing principle, or move it within the chapter.
- epilogue:67: "final design chapters" becomes "final design chapter".
  D5 Cadence
- Merge adjacent one-sentence paragraphs, keeping every sentence: ch08:86–109 and :244–270; ch10:95–118; ch24:397–413; the short runs in ch02; the epilogue.
- Vary about half of the ch13 section openers that restate the running values (:22, :30, :113, :207, :274, :365, :499, :532, :590).
- Vary the ch30 listing bridges (:351, :574, :665, :924, :1084, :1165).

2. Checks

- Extend check-final.py with regression guards for:
  - no commit/tag checkout target anywhere covered by A1;
  - no "Clang 13.0 or newer";
  - libasio-dev present in the Ch2 install list;
  - the coalesced QUIT lab case exists;
  - the canonical Express target in the ch25/ch27 installed-consumer examples;
  - no "now exposes/receives/distinguishes/include/carries";
  - no duplicate index directives or split index keys;
  - the listing-width limit;
  - the Pandoc/crossref guard step exists.
    Do not distort correct prose to satisfy a brittle check; improve the checker instead.
- Then run:
  - check-smoothing.py, check-polish.py and check-final.py;
  - ci/manuscript-metrics.py and ci/check-chapter-references.py;
  - ci/check-source-alignment.py against a fresh snode.c master clone;
  - ci/check-external-anchors.py and ci/check-source-hygiene.sh;
  - ci/build-book-package.sh;
  - the companion build and all 66 labs with GCC and with the workflow's Clang;
  - the C3 repetition runs.
- Push, then record the hosted book-package and companion-examples runs: IDs, compiler and Pandoc versions, and every job's conclusion.

3. Report: FOLLOWUP-15-REPORT.md

- Observed HEAD SHAs at start and end for snode.c master, MQTTSuite master, OpenWRT main and SNode.C-Book main. Evidence only.
- For each item: verified or not, file:line evidence, the change, and its commit. List skipped items with the reason.
- Status matrix: 37 rows × 8 dimensions, with file:line evidence for every changed cell. Explain every ◐ or ○.
- Gate table:
  - book package green, with page count and the Pandoc/crossref pair used;
  - labs 66/66 with GCC and 66/66 with Clang, local results plus hosted run IDs;
  - C3 repetition counts;
  - alignment against master HEAD;
  - external anchors;
  - author tree unchanged.
- Outside this repo:
  - the OpenWRT recipe fetches tag OpenWRT instead of snode.c master;
  - the Clang 21 -Wnrvo failure is a framework follow-up.
- Tokens before and after, for each touched chapter and in total.

4. Operational
   Push main. Final message, short:

- commit SHA for each group;
- the observed HEADs;
- matrix totals;
- gate status with run IDs;
- tokens and page count;
- anything not closed, with the reason.

## 5. Small clarifications

These clarifications do not replace or refine any earlier instruction. They are appended to FOLLOWUP-15 and apply in addition to it.

### E1 Canonical MQTTSuite repository identity

Where repository identity is written in scripts, reports, clone commands, or checks, use the canonical GitHub repository name:

`SNodeC/mqttsuite`

Do not use `SNodeC/MQTTSuite` as the canonical identifier. This does not change A4's requirement to use the repository's default branch `master` HEAD without pinning a commit or tag.

### E2 Ch32 flow-API paragraph

For D4, keep the flow-API paragraph currently near ch32:237 in its present structural position.

Do **not** move the paragraph. Add or revise the local bridge so that the paragraph connects naturally to the chapter's closing architectural principle and epilogue transition. This preserves §0's rule of no structural reorganization.

### E3 Pandoc / pandoc-crossref compatibility guard

For C1, the compatibility check must verify the actual Pandoc version against which the installed `pandoc-crossref` binary reports it was built.

Extract:

- the active Pandoc version from `pandoc --version`;
- the Pandoc build/ABI version reported by `pandoc-crossref --version`.

Fail the build if those versions do not match.

Do not implement this as a brittle comparison of complete `--version` output strings; parse only the relevant version values so harmless changes in surrounding version text do not break the check.


After this pass the manuscript is frozen again. A further follow-up is justified only by an actual technical error, broken build, broken reference, production defect, or drift reported by the HEAD checks.
