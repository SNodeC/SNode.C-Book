# Phase 2 chapter ledger

Date: 2026-09-22; updated for the same-phase author follow-up. Measurement authority: `ci/manuscript-metrics.py`.
Before: `metrics-before-phase-2.json`; after: `metrics-after-phase-2.json`.
Prose counts include Markdown, objectives, recaps, and exercises; fenced code is
excluded. Section averages use non-overlapping level 3–6 section bodies, excluding
headings and preambles, exactly as in Phase 0. Filename labels remain next to
complete listings; they are not separate conceptual sections.

| Chapter | Prose before | Prose after | Reduction | Sections before → after | Average section prose after | Editorial state |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [1](../../manuscript/chapters/01-why-snodec-exists.md) | 2,343 | 1,723 | 26.46% | 10 → 5 | 327.00 | edited and reread in context |
| [3](../../manuscript/chapters/03-your-first-working-program-the-echo-pair.md) | 2,674 | 1,987 | 25.69% | 23 → 6 | 315.50 | edited and reread in context |
| [23](../../manuscript/chapters/18-server-sent-events-and-real-time-http.md) | 3,664 | 2,897 | 20.93% | 31 → 7 | 398.00 | edited and reread in context |
| [35](../../manuscript/chapters/28-building-minigateway.md) | 2,378 | 1,863 | 21.66% | 35 → 6 | 294.33 | edited and reread in context |
| [37](../../manuscript/chapters/30-architectural-judgment-choosing-the-right-layer-and-boundary.md) | 2,395 | 1,859 | 22.38% | 15 → 6 | 291.00 | edited and reread in context |

## Objectives and exercises

Each sample has three observable objectives and five exercises: two review,
two labs, and one design problem, as required by the author's Phase 2 follow-up.
The mappings below cover both directions. Public README solution sections use the
same exercise numbers and objective IDs; `check-phase-2.py` verifies that match.
Chapter 1 O2 is achievable by reading its comparison; both labs follow Chapter 2.

| Chapter | Objective | Exercise | Public solution and evidence of learning |
| --- | --- | --- | --- |
| 1 | O1 | 1 — review | `ch01/README.md §1`: shared sequencing authority |
| 1 | O2 | 2 — review | `ch01/README.md §2`: buffer lifetime and callback progression |
| 1 | O2 | 3 — lab | `ch01/solution.py`: identical 20,480-byte stream and a later connection |
| 1 | O2 | 4 — lab | `ch01/independent-peers.py`: one idle/closed peer does not stop another |
| 1 | O3 | 5 — design | `ch01/README.md §5`: Linux gateway versus native Windows utility |
| 3 | O1 | 1 — review | `ch03/README.md §1`: handle, factory, and context ownership |
| 3 | O1 | 2 — review | `ch03/README.md §2`: initiation versus reflection |
| 3 | O2 | 3 — lab | `ch03/greeting-client.cpp and solution.py`: changed greeting and binary reflection |
| 3 | O3 | 4 — lab | `ch03/occupied-port.py`: bind error while original listener keeps working |
| 3 | O3 | 5 — design | `ch03/README.md §5`: endpoint versus protocol diagnosis |
| 23 | O1 | 1 — review | `ch23/README.md §1`: disconnect releases the response subscription |
| 23 | O1 | 2 — review | `ch23/README.md §2`: record boundary and MessageEvent fields |
| 23 | O2 | 3 — lab | `ch23/solution.py`: matching POST/event data, restricted Accept, reconnect |
| 23 | O2 | 4 — lab | `ch23/observers.py`: common accepted data and independent disconnection |
| 23 | O3 | 5 — design | `ch23/README.md §5`: bounded queues/history and visible recovery |
| 35 | O1 | 1 — review | `ch35/README.md §1`: MQTT decode → shared model → outputs |
| 35 | O1 | 2 — review | `ch35/README.md §2`: validation precedes acceptance |
| 35 | O2 | 3 — lab | `ch35/solution.py`: HTTP/SSE agreement without MQTT; restart resets state |
| 35 | O1 | 4 — lab | `ch35/validation.cpp`: invalid input changes neither state nor notifications |
| 35 | O3 | 5 — design | `ch35/README.md §5`: durable ordering and origin-filter ownership |
| 37 | O1 | 1 — review | `ch37/README.md §1`: acceptance order versus producer numbering |
| 37 | O3 | 2 — review | `ch37/README.md §2`: endpoint policy versus independently cancellable flows |
| 37 | O2 | 3 — lab | `ch37/model-ownership.cpp`: ordering and explicit unsubscribe |
| 37 | O2 | 4 — lab | `ch37/model-instances.cpp`: shared order 1,2 versus independent 1 and 1 |
| 37 | O3 | 5 — design | `ch37/README.md §5`: privileged collector and IPC/recovery ownership |

All abbreviated solution paths are relative to `companion/exercises/`.
Each README explains both lab commands and expected outcomes. All ten CTest cases
were run and passed (`phase-2-follow-up-labs.log`); the existing CI job discovers
both cases per chapter through CTest. The new validation and model-instance
executables compile the canonical model/codec; no production implementation is
copied or altered (`phase-2-follow-up-companion.log`). Hosted CI was not run here.

## Editorial reread and preservation

- Chapter 1: retained the competing-sequence example, layer figure, first-echo
  progression, and the source-version paragraph. Replaced the five-line comparison
  with a side-by-side implementation/responsibility table and bounded discussion.
  The practical lab follows environment preparation; it does not assume an
  unprepared reader can build in Chapter 1. Prerequisites agree with the preface.
- Chapter 3: retained all five complete source/build listings, ownership handoff,
  callback interpretation, public-header selection, build and run commands. The
  first-program vocabulary now defers detailed instance/flow treatment to Chapter 5,
  whose runtime-model explanation was reread to verify that destination. Removed
  repeated extracts of code already printed in full and their mirrored explanation;
  no algorithm or complete listing was cut to reach a prose target.
- Chapter 23: retained both complete programs and the substantive observer lifetime,
  parser limits, queue policy, and retry/replay distinctions. Consolidated scattered
  API/lifecycle/field subsections. The public-header note now precedes the recap,
  so the chapter actually ends with recap and exercises.
- Chapter 35: preserved every fenced block byte-for-byte, including all code,
  commands, text output, and the nested README. Kept model lifetime, static MQTT
  registry scope, CONNACK/SUBACK distinction, topic feedback risk, and the full
  progression toward Chapter 36. Removed repeated purpose and guarantee summaries.
  File labels keep each complete listing identifiable inside six conceptual sections.
- Chapter 37: retained the main decision tables, both worked decisions, three
  applicable rule boxes, and the independent-flow versus independent-endpoint
  distinction. Removed mirrored bad-instinct/misunderstanding lists and the second
  table repeating the sequence-owner decision. Reviewed its transition to Chapter 38.

The five revised Markdown chapters were reread as connected prose with their
listing locations; source alignment checks all complete listings separately.
All other ordered manuscript inputs are byte-identical to phase entry, including
the deliberate author epilogue restoration. `check-phase-2.py` verifies those
preservation claims, all sample figure/index/source markers, and Chapter 35 fences.
Visual review is recorded separately in `phase-2-visual-review.md`.

## Same-phase follow-up reread

The five chapter endings and their public answers were reread together after
expansion; the surrounding chapter arguments and preserved listing locations
were checked in context. The new Chapter 1 excerpts are explicitly labeled,
12 and 16 lines long, and match the companion functions after whitespace removal.
The comparison table remains; its whole section is below 1,200 words. The layer
argument now follows the measurement path through carrier, protocol, and shared
state; the node.js comparison explains why an event loop alone does not determine
ownership. The protocol inventory is removed in favor of that connected example.

Chapter 35 introduces source assembly in four dependency steps before its source
tree. All its original fences remain byte-identical. Chapter 37 trims two framing
passages and a table instruction to accommodate the extra exercises while keeping
its decision tables and applied rules. Chapters 3 and 23 change only their exercise
callouts. The remaining manuscript inputs, including the author's epilogue, are
unchanged. Current measurements include all added teaching prose; comparison code
and local layout fences are excluded from prose exactly like other fences.

Initial Phase 2 results remain in REPORT.md and its original logs; the follow-up
entry snapshot is `metrics-before-phase-2-follow-up.json`. Current rendered-page
inspection is recorded in `phase-2-follow-up-visual-review.md`.


## Phase 5a identity migration — 2026-09-22

The Phase 2 measurements and objective/exercise rows above retain their original
chapter identifiers as historical evidence. Their chapter links now resolve to
the current manuscript. Objective IDs O1–O3 and exercise numbers 1–5 are unchanged;
each row for an old chapter maps to the corresponding current chapter below.
This is a structural reread of references and transitions, not a new sample rewrite.

| Phase 2 identity | Current chapter | Current public solution directory | Lab target |
| --- | --- | --- | --- |
| 1 | 1 | `companion/exercises/ch01/` | `ch01-lab` |
| 3 | 3 | `companion/exercises/ch03/` | `ch03-lab` |
| 23 | 18 | `companion/exercises/ch18/` | `ch18-lab` |
| 35 | 28 | `companion/exercises/ch28/` | `ch28-lab` |
| 37 | 30 | `companion/exercises/ch30/` | `ch30-lab` |

The corresponding README answers, lab source files, CMake subdirectories, targets,
and CTest names moved together. `phase-5a-labs.log` records all ten passing tests.
`phase-5a-exit-checks.json` records current prose reductions, section averages,
objective/exercise mappings, and public-answer coverage under these identities.
No new lab, objective, exercise, or learning milestone was added in Phase 5a.
The integrated checkpoint assigned to current Chapter 30 remains Phase 5l work;
the epilogue remains an essay without exercises, as the author approved.


## Phase 5b — Part I (current numbering), 2026-09-22

Baseline: `metrics-after-author-seam-edits.json`; after:
`metrics-after-phase-5b.json`. These rows supplement the historical sample records.
Every ceiling includes markup and all fenced words. The fenced-word reductions
below remove only text diagrams/restatement, not executable listings.

| Chapter | Total before → after / budget | Prose before → after | Fenced before → after | H before → after / ceiling | Mean section prose words |
| --- | --- | --- | --- | --- | --- |
| 1 | 1821 → 1821 / 1850 | 1724 → 1724 | 97 → 97 | 5 → 5 / 5 | 327.0 |
| 2 | 2945 → 3006 / 3350 | 2639 → 2755 | 306 → 251 | 16 → 8 / 9 | 331.5 |
| 3 | 2566 → 2568 / 2650 | 1988 → 2026 | 578 → 542 | 6 → 6 / 6 | 321.83 |

Chapter 1 is reread and retained without prose edits: it already meets its budget,
comparison/excerpt requirements and teaching contract. Chapter 2 is edited and
reread: its eight connected sections retain preparation commands and add three
objectives, five recap bullets, five exercises, and the Lab environment guidance.
Chapter 3 is edited and reread: two redundant text blocks are removed, and Lab 3
now includes the Part I measurement-transport checkpoint. The surrounding code,
callback explanation, recap, and mapped labs remain. Both sample chapters retain
the original ≥20% prose reductions (Chapter 1: 26.42%; Chapter 3: 24.23%).
Chapter 2's objectives, recap, and exercises total 286 content words, below the
400-word apparatus allowance (301 including callout delimiters and titles).

### Objective ↔ exercise coverage

| Exercise | Tier | Objective(s) | Public answer/discussion |
| --- | --- | --- | --- |
| 1.1 | Review | O1 | `companion/exercises/ch01/README.md`, answer 1 |
| 1.2 | Review | O2 | `companion/exercises/ch01/README.md`, answer 2 |
| 1.3 | Lab | O2 | `companion/exercises/ch01/README.md`, answer 3 |
| 1.4 | Lab | O2 | `companion/exercises/ch01/README.md`, answer 4 |
| 1.5 | Design | O3 | `companion/exercises/ch01/README.md`, answer 5 |
| 2.1 | Review | O1 | `companion/exercises/ch02/README.md`, answer 1 |
| 2.2 | Review | O3 | `companion/exercises/ch02/README.md`, answer 2 |
| 2.3 | Lab | O2 | `companion/exercises/ch02/README.md`, answer 3 |
| 2.4 | Lab | O3 | `companion/exercises/ch02/README.md`, answer 4 |
| 2.5 | Design | O1, O2, O3 | `companion/exercises/ch02/README.md`, answer 5 |
| 3.1 | Review | O1 | `companion/exercises/ch03/README.md`, answer 1 |
| 3.2 | Review | O1 | `companion/exercises/ch03/README.md`, answer 2 |
| 3.3 | Lab | O2 | `companion/exercises/ch03/README.md`, answer 3 |
| 3.4 | Lab | O3 | `companion/exercises/ch03/README.md`, answer 4 |
| 3.5 | Design | O3 | `companion/exercises/ch03/README.md`, answer 5 |

Reverse mapping: Ch1 O1→1, O2→2/3/4, O3→5; Ch2 O1→1/5,
O2→3/5, O3→2/4/5; Ch3 O1→1/2, O2→3, O3→4/5. All objectives
have exercises and all exercises have objectives. Review/design answers are in
the listed public READMEs. All chapters close with one recap (≤5 bullets), then
exactly two review questions, two labs, and one design problem.

### Built and run

- Ch1: canonical EchoPair and Asio; `exercise-ch01` and
  `exercise-ch01-independent-peers` pass.
- Ch2: `ch02-lab` reuses canonical EchoPair; `exercise-ch02-consumer` and
  `exercise-ch02-component` each configure and build an independent external
  consumer, inspect its package cache, and verify exact `environment-ready` bytes.
  The second first diagnoses an intentional missing component in a temporary copy.
- Ch3: `ch03-lab`, `exercise-ch03`, and `exercise-ch03-occupied-port` pass.
  Lab 3 checks greeting/binary reflection plus two measurement peers, reflection
  of an invalid value, and continued service after the other peer closes. This
  establishes transport, not domain acceptance; no new model/parser is introduced.

Evidence: `phase-5b-final-companion.log`, `phase-5b-final-labs.log`,
`phase-5b-exit-checks.json`; commands are in each public README. The existing
GitHub workflow registers/runs these via the chapter CMake subdirectory; this
session executed the same local commands, not a hosted CI run.
An initial attempt incorrectly expected a zero help exit; the failure log
`phase-5b-initial-labs.log` is retained. The final environment labs observe an
actual bounded byte exchange using the existing peer/process harness.

Chapter 2 and Conventions distinguish equipped labs (broker/database/hardware)
from local-only observations, and list MQTT, MariaDB, TLS, and Bluetooth needs by
Part. Later Parts' lab implementations remain for their own sessions. Front matter
now states the independent learner, public-solution workflow and one learning path
with two shortcuts. Edited Markdown, solutions and the Part I/II transition were
reread; PDF evidence is separately recorded in `phase-5b-visual-review.md`.


## Phase 5c — Part II, 2026-09-22

Edited and reread: Chapters 4–5, their public solutions, and the Part II opener.
The unchanged Part III transition was reread in context. Before figures come from
`metrics-after-phase-5b.json`; after figures from `metrics-after-phase-5c.json`.

| Chapter | Total before → after / budget | Prose before → after | Fenced before → after | Sections before → after / ceiling | Mean section prose |
| --- | --- | --- | --- | --- | --- |
| 4 | 7,809 → 4,338 / 5,300 | 7,296 → 4,290 | 513 → 48 | 55 → 14 / 15 | 294.50 |
| 5 | 5,188 → 2,983 / 3,700 | 5,089 → 2,908 | 99 → 75 | 47 → 10 / 11 | 278.10 |

Part II is **7,321 / 9,000 words**. No reserve used; 2,750 remains. The fenced
reduction is entirely removed `text` blocks, not executable listings. The original
C++ fences remain byte-identical and in order. Both chapters have three objectives,
one five-bullet recap, and five exercises in the order review/review/lab/lab/design.
Apparatus content words are 297 and 312 respectively.

### Objective ↔ exercise coverage

| Exercise | Tier | Objective(s) | Public solution |
| --- | --- | --- | --- |
| 4.1 | Review | O1 | `companion/exercises/ch04/README.md`, answer 1 |
| 4.2 | Review | O2 | same README, answer 2 |
| 4.3 | Lab | O3 | same README, answer 3; canonical model-instances target |
| 4.4 | Lab | O1 | same README, answer 4; canonical EchoPair and existing independent-peers script |
| 4.5 | Design | O1, O2, O3 | same README, answer 5 |
| 5.1 | Review | O1 | `companion/exercises/ch05/README.md`, answer 1 |
| 5.2 | Review | O2 | same README, answer 2 |
| 5.3 | Lab | O1, O2 | same README, answer 3; `deferred-work.cpp` |
| 5.4 | Lab | O3 | same README, answer 4; canonical model-ownership target |
| 5.5 | Design | O1, O2, O3 | same README, answer 5 |

Reverse mapping: Ch4 O1→1/4/5, O2→2/5, O3→3/5; Ch5 O1→1/3/5,
O2→2/3/5, O3→4/5. Every objective has an exercise and every exercise has an
objective. Public answers explain both expected outcomes and their limits.

### Executed labs and checkpoint

Using the common public configuration, build `ch04-lab ch05-lab`, then run
`ctest --test-dir build/labs -R '^exercise-ch0[45]-' --output-on-failure -V`.
The actual fresh session build directory is `build/proposal-readiness-phase-5c-examples`.

- `exercise-ch04-model-instances`: shared model assigns 1,2; separate owners each
  start at 1. Reuses `ch30/model-instances.cpp` and the canonical model.
- `exercise-ch04-independent-peers`: an active peer receives exact binary bytes
  while another is idle, and continues after the idle peer closes. Reuses the
  existing peer harness and EchoPair; does not terminate the listening flow.
- `exercise-ch05-deferred-work`: empty trace before start, RUNNING dispatch,
  trace 1,2,3, child observes that the first callback has returned. Explicit checks
  remain active in release builds. No latency/fairness guarantee is inferred.
- `exercise-ch05-model-checkpoint`: producer sequences 900,2,1 become accepted
  order 1,2,3. Remove one observer between acceptance calls; it retains 1,2 while
  the other sees all three. Reuses `ch30/model-ownership.cpp` and the canonical
  MiniGateway model, without requiring the later chapter. This executes model
  ownership/removal, not event-loop scheduling, transport teardown or persistence.

All four pass within **16/16** public labs. Evidence: `phase-5c-final-companion.log`,
`phase-5c-final-labs.log`, `phase-5c-runtime-results.json`, `phase-5c-exit-checks.json`.
CMake registration follows the existing CI discovery path; no hosted run is claimed.
The initial missing imported-core-target scope was fixed with the lab directory's
explicit `find_package(snodec REQUIRED COMPONENTS core)`; its failed configuration
log remains `phase-5c-initial-companion.log`.

### Content-preservation audit

Chapter 4's stop rule was evaluated before claiming completion. Condensation
removes repeated definitions, inventories and arrow chains inherited from the
merged chapters; it retains the substantive teaching, as the following final
locations show. No budget-driven removal of a distinct explanation was needed.

| Retained teaching | Final manuscript evidence |
| --- | --- |
| Endpoint/handle/flow distinction, retries, independent activations, reference-capture lifetimes | Ch4:53 and :117 |
| Connection callbacks versus context behavior, factories and per-peer state | Ch4:77 |
| Shared model versus per-peer partial record, with observable contrast | Ch4:111 and public answer 4.3 |
| Configuration, flow control, metrics at their distinct stages | Ch4:164 |
| Source/type/header/component views (intro ≤300 words), type decoding | Ch4:192 and :252 |
| Runtime versus layers; OSI qualification; all five network families | Ch4:224 and :290 |
| Common-address versus family-specific tradeoff, stream framing | Ch4:315 and :325 |
| Legacy/TLS distinction, operational/security obligations and public components | Ch4:334 |
| Protocol carriers, Express/MQTT/WebSocket composition and failure diagnosis | Ch4:360 |
| Build selection versus runtime configuration, cross-layer consequences | Ch4:383 and :404 |

The four existing applied rule boxes, both chapter figures, index entries and all
executable listings remain. Chapter 5 keeps its source excerpts, public stepping
restriction, runtime state/status distinction, thread ownership, event publication
versus separate queued callbacks, multiplexer stages, descriptor lifecycle, timers,
and coordinated shutdown. Its final section applies that reasoning to the mapped
Part II checkpoint. Visual evidence is separate in `phase-5c-visual-review.md`.


## Author-requested Phase 5c follow-up — 2026-09-22

The author requested one Part II correction before Phase 5d: merge the duplicated
public-type/name treatment, retain its stable anchor and registered references,
and leave the build section as an applied legacy-to-TLS comparison. Implemented
and reread in `manuscript/chapters/04-the-mental-model-and-layers-in-practice.md:192`.
The merged treatment is 256 whitespace tokens including its heading and syntax;
all index occurrences, code excerpts (including order), and the Layer-reading
rule remain. The build comparison now asks for separate build, handshake/identity,
and byte-reflection observations. No exercises, applications or other chapters change.

Chapter 4: 4,338 → 4,075 words, 14 → 13 sections; Part II: 7,321 → 7,058.
Fresh Phase 5c assertions pass, including the original budgets and pedagogy, source
intro cap, reference targets, all executable fences, index and figure preservation.
Hygiene/alignment, metric/reference tests, companion build, all sixteen labs,
teaching/behavior/lifetime checks, PDF/package builds, archive identity and
extracted-package hygiene pass. See `phase-5c-follow-up-results.json`,
`phase-5c-follow-up-*.log`, `metrics-after-phase-5c-follow-up.json` and
`phase-5c-follow-up-exit-checks.json`. The wrapper `check-phase-5c-follow-up.py`
retains historical assertions and redirects only metrics/log/result paths;
historical Phase 5c evidence remains unchanged. The reference register updates
only line evidence; the source-reading anchor's registered targets remain intact.

Rendered physical pages 44–45 and 47–48 were inspected after rebuilding: the merged
mapping, Layer-reading rule, applied table, recap and exercises fit without clipping
or overlap. Images are local build outputs in `build/phase-5c-follow-up-visual/`.

PDF pages: full 438 → 436; samples 54 and proposal 6 unchanged.
All final PDF warnings/bad boxes are zero. Full words: 140,336 → 140,073.
No reserve used; 2,750 remains. Application/test code growth: zero.

Separate commit: `proposal-readiness: phase 5c follow-up — remove triple name/component explanation`.
This freshly passed follow-up is the authorized Phase 5d entry baseline; the author
explicitly requests Phase 5d next in the same session.


## Phase 5d — Part III completed, 2026-09-22

Baseline: the separately committed author-requested Phase 5c follow-up;
`metrics-after-phase-5c-follow-up.json`. After: `metrics-after-phase-5d.json` and
`phase-5d-exit-checks.json`. Chapter counts include all pedagogical apparatus.
Edited and reread: Chapters 6–8, the Part III opener, and all three public solution
READMEs. The unchanged Part IV opener was reread for the transition. Rendered-page
review is separate in `phase-5d-visual-review.md`.

| Chapter | Words before → after | Budget | Prose before → after | Fenced words before → after | Sections before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 6 | 8,080 → 4,168 | 5,200 | 7,615 → 3,952 | 465 → 216 | 63 → 12 / 15 | 319.25 |
| 7 | 4,859 → 3,084 | 3,650 | 4,629 → 3,032 | 230 → 52 | 32 → 9 / 10 | 324.67 |
| 8 | 2,613 → 2,170 | 2,200 | 2,463 → 2,059 | 150 → 111 | 25 → 5 / 5 | 393.40 |

Part III totals **9,422 / 11,050** words. No reserve used; 2,750 remains.
All original C++ excerpts remain byte-identical and in order within their chapters.
Fenced-word reductions remove explanatory `text` blocks, not executable listings.
Each chapter opens with three objectives and ends with one five-bullet recap,
then five exercises: two review questions, two labs and one design problem.

### Objective ↔ exercise mapping and public solutions

All numbered answers are in `companion/exercises/chNN/README.md`, under matching
exercise headings. The chapter objective callouts begin at line 3; exercise
callouts begin at Ch6:600, Ch7:363, and Ch8:273.

| Chapter.exercise | Tier | Objectives | Public answer / executable observation |
| --- | --- | --- | --- |
| 6.1 | Review | O1 | ch06/README.md §1: configured defaults versus usable local/remote endpoints |
| 6.2 | Review | O3 | ch06/README.md §2: unsupported credentials and authorization |
| 6.3 | Lab | O1, O2 | ch06/README.md §3; `exercise-ch06-ip-families` |
| 6.4 | Lab | O3 | ch06/README.md §4; `exercise-ch06-unix-path` |
| 6.5 | Design | O1, O2, O3 | ch06/README.md §5: local producer endpoint and deployment obligations |
| 7.1 | Review | O1 | ch07/README.md §1: handle, flow, connection and role lifetimes |
| 7.2 | Review | O2 | ch07/README.md §2: callback stage and borrowed-pointer lifetime |
| 7.3 | Lab | O3 | ch07/README.md §3; `exercise-ch07-independent-peers` |
| 7.4 | Lab | O2 | ch07/README.md §4; `exercise-ch07-occupied-endpoint` |
| 7.5 | Design | O1, O2, O3 | ch07/README.md §5: independent destinations, shared accepted state |
| 8.1 | Review | O1 | ch08/README.md §1: device identity and family-specific selector |
| 8.2 | Review | O2 | ch08/README.md §2: ordered diagnosis of an equipped exchange |
| 8.3 | Lab | O1 | ch08/README.md §3; `exercise-ch08-selectors`; optional physical extension |
| 8.4 | Lab | O3 | ch08/README.md §4; `exercise-ch08-part-checkpoint` |
| 8.5 | Design | O2, O3 | ch08/README.md §5: BLE advertisement versus supported stream input |

| Objective | Exercises |
| --- | --- |
| 6.O1 | 6.1, 6.3, 6.5 |
| 6.O2 | 6.3, 6.5 |
| 6.O3 | 6.2, 6.4, 6.5 |
| 7.O1 | 7.1, 7.5 |
| 7.O2 | 7.2, 7.4, 7.5 |
| 7.O3 | 7.3, 7.5 |
| 8.O1 | 8.1, 8.3 |
| 8.O2 | 8.2, 8.5 |
| 8.O3 | 8.4, 8.5 |

### Built and run

All six new registrations pass within **22/22** public labs; exact commands and
observations are in `phase-5d-final-labs.log`, with build evidence in
`phase-5d-final-companion.log` and exit assertions in `phase-5d-exit-checks.json`.
The ordinary companion CMake discovery path includes all three new directories.
No hosted CI execution is claimed.

- IP families: exact binary measurement-shaped bytes over IPv4 and IPv6 loopback;
  producer/service identities match the opposite server observations. Rendered
  names are resolved within the chosen family before comparing endpoints.
- Unix path: identical bytes and opposite pathname identities; each endpoint
  removes its owned path, while an unrelated sentinel survives. These assertions
  occur before temporary-directory cleanup, so fixture cleanup cannot hide a leak.
- Independent peers: existing fixture observes one peer progressing while another
  is idle and after that peer closes. No shared-model behavior is inferred.
- Occupied endpoint: existing fixture observes a second listener's activation
  failure while the original listener continues reflecting bytes.
- Bluetooth selectors: public getters expose an empty initial configured device
  string and zero selectors; initialization retains one chosen device with channel
  16 and PSM 4097. This opens no radio socket.
- Part III checkpoint: the same canonical EchoPair context/factory handles the
  same bytes over loopback IP and a private Unix path, with identity and cleanup
  observations. Echoing bytes does not assign accepted measurement order.

`family-server.cpp` is one thin driver compiled for five carriers, reusing the
canonical context/factory. Its optional RFCOMM and L2CAP targets build. The public
RFCOMM two-host procedure is an **optional equipped extension, not run** here;
physical Bluetooth delivery remains unverified. IPv6 loopback and installed
Bluetooth development/components are required for the mandatory local tests.

### Content-preservation audit

The author stop rule applies to Chapter 6. Its cuts remove the repeated family
introductions, mirrored descriptions and stack-arrow blocks inherited from the
merge. Distinct explanations and examples remain at the following final locations;
no substantive topic was removed to meet the budget.

| Retained teaching | Final chapter evidence |
| --- | --- |
| Local/remote direction, family-specific address meaning and endpoint identity | Ch6:9, :64 |
| Defaults, constructors, initialization, rendered versus actual observations | Ch6:173 |
| IPv4/IPv6 resolution, concrete endpoints, convenience overloads | Ch6:242, :281 |
| Context reuse with separate family observations and dual-stack policy | Ch6:302, :331 |
| Complete existing IPv4/IPv6 comparison excerpts | Ch6:341 |
| Pathname/abstract Unix identities, listening/connecting, datagram distinction | Ch6:409, :447 |
| Directory access, path cleanup/ownership and deployment | Ch6:526 |
| Credential query/status, unsupported result and authorization decision | Ch6:547 |
| Public family headers/components | Ch6:242 and :447 |

Chapter 7 retains independent flow control, shared endpoint configuration, retry
ownership, connection surfaces/counters, TLS readiness, detach/disconnect timing,
factory dependencies and per-peer state (sections at :51, :84, :134, :204, :252,
:297, :317, :327). Both applied rules and its figure remain. Chapter 8 retains
service-selector distinctions, local/remote direction, conditional components,
Classic/BLE distinction, equipment preparation and both interactive `bluetoothctl`
blocks (:13, :97, :161, :201, :234). Every index occurrence and existing executable
excerpt remains; the preservation checker verifies those claims against the
committed entry baseline.
