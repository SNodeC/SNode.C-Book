# Follow-up 14 — final polish and freeze gate

**Complete; publisher freeze gate passed.** All 296 matrix cells are ●. Local and hosted GCC 13.3.0 / Clang 18.1.3 runs pass 66/66 labs and all required framework, consumer, smoke and lifetime checks. The book package and source checks pass, and the author-tree freeze equals R2. The manuscript is now frozen for publisher submission; no further broad refinement follows.

Work began at d4ff44d. A–D are committed and pushed on `book/pedagogical-smoothing-2026-09-23`. The author instruction is preserved verbatim in `FOLLOWUP-14.md`. No teaching passage, listing, example or explanation was cut. The manuscript grows by 115 tokens, from 110,955 to 111,070.

## Item commits

| Group | Commit | Result |
|---|---|---|
| A | `94e4838` | Correct article and Ch32 lab-to-chapter mappings, verified against ch04/ch06/ch32 CMake and READMEs |
| B | `d27b2ef` | Correct connection-variant and named-instance wording; retain the configuration example and design-role meanings |
| C | `859fd61` | Add all seven specified reinforcement links, retaining every targeted block and explanation |
| D | `ca2f768` | Record prior hosted logs, compiler versions and unchanged shared loader policy; reproduce with the hosted Ubuntu toolchains |

## Freeze gate

| Requirement | Result |
|---|---|
| Matrix all ● | **PASS:** 37/37 in each of E, D, G, X, T, L, S and C; 296 ●, 0 ◐, 0 ○ |
| Book package | **PASS:** main book 328 pages; proposal 9; sample 61; package built twice |
| Local companion labs | **PASS:** GCC 13.3.0 **66/66**, Clang 18.1.3 **66/66**, plus framework/external/smoke/lifetime suites |
| Hosted companion labs | **PASS:** run [36039311975](https://github.com/SNodeC/SNode.C-Book/actions/runs/36039311975), pushed `ca2f768`; GCC 13.3.0 **66/66**, Clang 18.1.3 **66/66**, all job steps successful |
| Frozen-source alignment | **PASS:** fresh public clone at 07ca9a2936ee72582df7d159cb06666fe23e30f8, zero errors |
| Author-tree freeze | **PASS:** start/end records both equal framework-freeze-R2.json in all four fields; only `?? porting/` ignored |

The hosted gate is established on A–D (`ca2f768`), whose compiled inputs match this final evidence commit. The evidence commit adds review/checker records and current proposal measurements, not companion or framework code. A subsequent automatically triggered evidence-push run is separate from the completed run above; its result is not claimed here.

## Companion verification

Local runs used separate workspaces, homes, build trees and installation prefixes inside an Ubuntu 24.04.4 root filesystem under the book build directory. Bubblewrap supplied a read-only root filesystem and fresh public framework clone, private `/tmp`, and UID 1000. The author's framework tree was never mounted. The host kernel remains shared; this reproduces the workflow commands and compiler distribution, not every property of the hosted VM.

The local compiler versions are **GNU 13.3.0** (`13.3.0-6ubuntu2~24.04.1`) and **Clang 18.1.3** (`1ubuntu1`). Both workflow scripts exited 0. Each passed:

- all **185/185 framework tests**;
- all **4/4 external Echo consumer tests**;
- all **66/66 public exercise labs** under the workflow's bare CTest invocation;
- teaching smoke tests, behavioral smoke tests, and all selected SSE lifetime/WebSocket echo checks.

The framework and companions were built using `ci/build-companion-examples.sh`, without changing its flags or timeouts. The public-lab command was exactly `ctest --test-dir build/ci-book-examples --output-on-failure --no-tests=error`, with no caller `LD_LIBRARY_PATH`. The existing workflow's teaching, behavioral and lifetime commands followed. `followup-14-evidence/run-local.sh` and `launch.sh` record the invocation; compiler, CTest, smoke and lifetime logs are preserved alongside them. The book archives were made at C (`859fd61`); D changes only review records, so their compiled inputs and manuscript are identical to pushed `ca2f768`.

### Hosted history and current run

| Hosted run / book commit | GCC | Clang |
|---|---|---|
| [36002150169](https://github.com/SNodeC/SNode.C-Book/actions/runs/36002150169) / `f19a658` | GNU 13.3.0; **failure**, framework 185/185, external 4/4, labs 65/66 | Clang 18.1.3; **success**, framework 185/185, external 4/4, labs 66/66 |
| [36002653903](https://github.com/SNodeC/SNode.C-Book/actions/runs/36002653903) / `d4ff44d` | GNU 13.3.0; **success**, framework 185/185, external 4/4, labs 66/66 | Clang 18.1.3; **success**, framework 185/185, external 4/4, labs 66/66 |
| [36039311975](https://github.com/SNodeC/SNode.C-Book/actions/runs/36039311975) / `ca2f768` | GNU 13.3.0; **success**, framework 185/185, external 4/4, labs 66/66; all smoke/lifetime steps pass | Clang 18.1.3; **success**, framework 185/185, external 4/4, labs 66/66; all smoke/lifetime steps pass |

The first historical GCC failure is `exercise-ch07-ip-families`: an `IDENTITY` line interleaves with asynchronous diagnostic output, and `families.py` fails converting the resulting port text. It is **not a shared-library loader failure**. This observation remains recorded; a later success is not evidence that this intermittent diagnostic/test interaction was repaired. No parser, assertion, diagnostic option, timeout or test logic was changed. Both jobs in the successor run passed, including smoke/lifetime steps. The supplied historical job logs and conclusions are preserved rather than overwritten.

Hosted Clang 18.1.3 builds the frozen source successfully. Therefore the follow-up's conditional instruction to pin a failing hosted compiler does not apply. The shared Linux inherited-RPATH policy from f19a658 passes the loader cases under both compilers, and no second loader policy or additional companion change is needed.

### Framework follow-up outside this branch

Local host **Clang 21.1.8** remains a known compatibility issue for the next SNode.C release: `src/tools/snodec-control/src/ConfigActions.cpp:296`, `-Werror,-Wnrvo`. Follow-up 14 explicitly permits using the hosted working Clang version. The frozen framework is unmodified, and no warning suppression or framework-behavior investigation was introduced. This book pass does not claim to fix Clang 21 compatibility.

## Status matrix

E = entry; D = depth; G = gradient; X = explicitness; T = theory–example; L = language; S = structure; C = continuity. ● = met; ◐ = partly met; ○ = open. These are scoped issue-register assessments, not a claim that every conceivable editorial improvement has been exhausted. Rows other than 33 retain the Follow-up 13 assessments. The explicit Follow-up 14 criterion closes row 33 through purposeful reinforcement and links; it does not require or claim cuts.

| Row | Issue | E | D | G | X | T | L | S | C |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Canonical terminology | ● | ● | ● | ● | ● | ● | ● | ● |
| 2 | Opening gradient | ● | ● | ● | ● | ● | ● | ● | ● |
| 3 | Runtime/layer split | ● | ● | ● | ● | ● | ● | ● | ● |
| 4 | Event-loop model before internals | ● | ● | ● | ● | ● | ● | ● | ● |
| 5 | Shortest route to the first program | ● | ● | ● | ● | ● | ● | ● | ● |
| 6 | Application/system split | ● | ● | ● | ● | ● | ● | ● | ● |
| 7 | Express example before inventory | ● | ● | ● | ● | ● | ● | ● | ● |
| 8 | MQTT conversation and fundamentals | ● | ● | ● | ● | ● | ● | ● | ● |
| 9 | CMake starts with a consumer | ● | ● | ● | ● | ● | ● | ● | ● |
| 10 | Configuration follows one port | ● | ● | ● | ● | ● | ● | ● | ● |
| 11 | Interpretation after capstone listings | ● | ● | ● | ● | ● | ● | ● | ● |
| 12 | Three explained extension excerpts | ● | ● | ● | ● | ● | ● | ● | ● |
| 13 | Expanded architectural synthesis | ● | ● | ● | ● | ● | ● | ● | ● |
| 14 | Application-facing recovery settings | ● | ● | ● | ● | ● | ● | ● | ● |
| 15 | Chapter and Part seams | ● | ● | ● | ● | ● | ● | ● | ● |
| 16 | Taxonomy has one teaching home | ● | ● | ● | ● | ● | ● | ● | ● |
| 17 | Protocol chapters end with a transition | ● | ● | ● | ● | ● | ● | ● | ● |
| 18 | Edition/verification voice contained | ● | ● | ● | ● | ● | ● | ● | ● |
| 19 | Concrete actors replace abstraction stacks | ● | ● | ● | ● | ● | ● | ● | ● |
| 20 | Logging explanation and current wording | ● | ● | ● | ● | ● | ● | ● | ● |
| 21 | Testing starts from a problem | ● | ● | ● | ● | ● | ● | ● | ● |
| 22 | Performance stance and limits | ● | ● | ● | ● | ● | ● | ● | ● |
| 23 | Appendix entry supports different readers | ● | ● | ● | ● | ● | ● | ● | ● |
| 24 | TLS configuration is on the page | ● | ● | ● | ● | ● | ● | ● | ● |
| 25 | Experience precedes formal vocabulary | ● | ● | ● | ● | ● | ● | ● | ● |
| 26 | Address-comparison seam | ● | ● | ● | ● | ● | ● | ● | ● |
| 27 | Core mechanism readable without the lab | ● | ● | ● | ● | ● | ● | ● | ● |
| 28 | Part II checkpoint interface printed | ● | ● | ● | ● | ● | ● | ● | ● |
| 29 | A distinct IoT worked decision | ● | ● | ● | ● | ● | ● | ● | ● |
| 30 | Native/composed MQTT trace | ● | ● | ● | ● | ● | ● | ● | ● |
| 31 | One-peer timeline before distinctions | ● | ● | ● | ● | ● | ● | ● | ● |
| 32 | Verification phrasing restored to baseline | ● | ● | ● | ● | ● | ● | ● | ● |
| 33 | Purposeful, explicitly linked repetition | ● | ● | ● | ● | ● | ● | ● | ● |
| 34 | References and narrative order | ● | ● | ● | ● | ● | ● | ● | ● |
| 35 | Slips and register | ● | ● | ● | ● | ● | ● | ● | ● |
| 36 | Apparatus and placement | ● | ● | ● | ● | ● | ● | ● | ● |
| 37 | Cadence and style without shortening | ● | ● | ● | ● | ● | ● | ● | ● |

| Dimension | ● | ◐ | ○ |
|---|---:|---:|---:|
| E | 37 | 0 | 0 |
| D | 37 | 0 | 0 |
| G | 37 | 0 | 0 |
| X | 37 | 0 | 0 |
| T | 37 | 0 | 0 |
| L | 37 | 0 | 0 |
| S | 37 | 0 | 0 |
| C | 37 | 0 | 0 |

Total: **296 ●, 0 ◐, 0 ○**. No matrix cell remains qualified. The eight changed cells are 33/E, 33/D, 33/G, 33/X, 33/T, 33/L, 33/S and 33/C; each changes from ◐ to ●. The executable gate is a separate assessment.

## Evidence for every changed cell

Paths below are relative to the repository root. Chapter evidence uses the authoritative Markdown, not PDF line extraction. All seven requested locations are linked, including the two subitems each in Chapters 4 and 7.

| Changed cell | File:line evidence and assessment |
|---|---|
| 33/E | `manuscript/frontmatter/conventions.md:13`; `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:452`: the definition points to its glossary, and the build explicitly identifies the already-completed Chapter 2 route. |
| 33/D | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:152` and `:177`: both startup snippets and the full per-connection explanation remain, with explicit reference back. |
| 33/G | `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:343` and `:530`: the comparison adds instance names and activation; the later Chapter 8 pointer adds pathname/lifetime context. |
| 33/X | `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:139`: the complete Chapter 3 listing is named and the repeated snippets' transfer-boundary purpose is explicit. |
| 33/T | `manuscript/chapters/18-the-express-like-framework.md:247`: the framework counterpart connects to the earlier trace and states its extra `/outside` 404 and counted-visit observations. |
| 33/L | `manuscript/frontmatter/conventions.md:13`; `manuscript/chapters/29-testing-debugging-and-benchmarking.md:391`: short local links retain the existing explanation and vocabulary. |
| 33/S | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:452`; `manuscript/chapters/07-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:343`: added introductions identify the purpose of both retained blocks without moving or deleting them. |
| 33/C | `manuscript/chapters/04-the-snodec-runtime-mental-model.md:177`; `manuscript/chapters/12-building-the-same-protocol-over-different-lower-layers.md:139`; `manuscript/chapters/18-the-express-like-framework.md:247`; `manuscript/chapters/29-testing-debugging-and-benchmarking.md:391`: back-references and the single-run/general-benchmark transition connect the repeated teaching material. |

A and B maintain already-met rows by correcting the introduced article/reference errors and terminology residue. `FOLLOWUP-14-CLAIMS.md` records the CMake/README mapping verification and frozen-source checks. Ch32's companion README already matched its targets and needed no edit. The kept role inventory contains 327 role occurrences and 29 allowed carrier occurrences. No application code, configuration example, existing lab assertion, timeout or driver logic changed.

## Extent and retained material

Counts use `ci/manuscript-metrics.py`: whitespace tokens in raw manuscript inputs, including markup and fences. “Before” is d4ff44d; “after” is the completed A–C manuscript. Every touched chapter is listed, including those whose count is unchanged.

| Chapter / section | Before | After | Change |
|---|---:|---:|---:|
| Ch3 — Your First Working Program: The Echo Pair | 3,004 | 3,023 | +19 |
| Ch4 — The SNode.C Runtime Mental Model | 2,907 | 2,926 | +19 |
| Ch5 — Layers in Practice | 2,903 | 2,903 | +0 |
| Ch7 — Network Families: Addresses, IPv4/IPv6, and Unix Sockets | 4,218 | 4,241 | +23 |
| Ch12 — Building the Same Protocol over Different Lower Layers | 2,583 | 2,598 | +15 |
| Ch18 — The Express-Like Framework | 2,225 | 2,242 | +17 |
| Ch26 — From Applications to Systems: MQTTSuite | 3,897 | 3,897 | +0 |
| Ch29 — Testing, Debugging, and Benchmarking | 4,361 | 4,373 | +12 |
| Ch30 — Building MiniGateway | 4,591 | 4,597 | +6 |
| Ch32 — Architectural Judgment: Choosing the Right Layer and Boundary | 3,165 | 3,165 | +0 |
| Conventions Used in This Book | 823 | 827 | +4 |
| **Full book** | **110,955** | **111,070** | **+115** |
| Prose/markup outside fences | 103,079 | 103,194 | +115 |
| Fenced tokens | 7,876 | 7,876 | 0 |

The net growth is **0.104%**, within the requested approximate 100–400-token range. All chapter floors and caps pass without waivers. The earlier 107,338 must target is exceeded by 3,732; the book is 1,268 below the 112,338 wish threshold and 3,930 below the 115,000 ceiling. These figures disclose the previously accepted overall extent; they do not authorize shortening.

All **130 fenced blocks in touched files are byte-identical** to d4ff44d (`followup-14-evidence/retained-fences.json`). Diff review confirms the retained teaching explanations and examples. The book has 328 PDF pages; the proposal has 9; the separately paginated sample package has 61. Selected physical book pages 39, 47, 70, 164, 264, 303 and 304 were rendered and visually checked for the changed build/link/exercise material: no clipping or overlap. The exercise block continues cleanly onto page 304. Proposal page 1 and sample page 61 also render correctly, including the updated extent and corrected exercise references. Final LaTeX reference checks and the package's 454 unique archive entries pass.

## Checks and accounting

| Check | Result |
|---|---|
| check-smoothing.py | PASS, 16 groups; chapter floors/caps and ceiling pass |
| check-polish.py | PASS, 9 groups; 46 verification constructions; proposal figures agree |
| check-final.py | PASS, including all new Follow-up 14 regression guards |
| Editorial checker tests | PASS, 17 polish + 17 final tests; alternative wording/soft-wrap and mutation checks included |
| manuscript-metrics.py | Fresh `metrics-after-followup-14.json`, 111,070 tokens |
| check-chapter-references.py | PASS, 32 chapters + Appendix A, 56 topics, 314 current references, 374 historical dispositions |
| check-source-alignment.py | PASS, fresh public 07ca9a29 clone, 1,448 source files, 33 evidence records, 37 exact complete listings, zero errors |
| check-source-hygiene.sh | PASS, including its six regression tests |
| build-book-package.sh | PASS, two builds, PDFs 328/9/61 pages, 454 unique archive entries, no unresolved final references |

Editorial checker support changes by +43/−3 lines; its test support by +44/−3 lines. Application production code, companion CMake, workflow configuration and existing runtime test logic each change by **0 lines** in Follow-up 14. Documentation, generated measurements and evidence are accounted separately. The whole-build invariant remains that every exercise target resolves its installed SNode.C dependencies under the workflow's bare CTest command, without relying on an inherited caller library-path variable. The existing shared Linux RPATH policy supplies that behavior; no second policy was added.

## Freeze comparison and final disposition

`framework-freeze-followup-14-start.json` and `framework-freeze-followup-14-end.json` each equal the unchanged `framework-freeze-R2.json`:

| Field | R2 / start / end |
|---|---|
| HEAD | `07ca9a2936ee72582df7d159cb06666fe23e30f8` |
| Porcelain status after removing only `?? porting/` | empty |
| SHA-256 of `git diff HEAD --binary` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Untracked nonignored files outside porting/ | `[]` |

The empty filtered status establishes that there are no untracked files to digest outside the ignored directory. Its contents were not read, moved, excluded or modified. The fresh public clone is clean at the same commit. All existing commits and historical reports remain intact.

All Follow-up 14 item groups and submission-gate checks are closed. The Clang 21 framework compatibility issue remains outside this branch for the next framework release. The historical Ch7 diagnostic interleaving failure remains recorded and unrepaired; both new local and hosted lab runs pass unchanged. No claim is made that a passing rerun eliminates that intermittent interaction. The final evidence is committed and the work branch pushed without merging. Further broad refinement is not authorized.
