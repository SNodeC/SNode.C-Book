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


## Author-requested Phase 5d follow-up — 2026-09-22

Edited and reread `manuscript/chapters/06-network-families-addresses-ipv4-ipv6-and-unix-sockets.md:409`:
the stream/datagram introduction, public headers/component and lab orientation now
open the Unix-domain section. The credentials section ends with authorization
policy. The introduction names only context/factory separation and event-loop
execution from Chapters 3–5, and points ahead to Chapter 7 for connection lifetimes.
All index occurrences and original registered target/migration identities remain;
two explicit teaching-path references were added (345 current references).
No other manuscript input changes in this follow-up.

Fresh Phase 5d exit checks pass. `check-phase-5d-follow-up.py` retains all previous
assertions, redirects evidence paths, and permits only the author's relocation in
Chapter 6's excerpt order; an exact expected-text assertion checks that relocation
and the one sentence correction against the Phase 5d commit. All excerpt bytes
remain unchanged. Evidence: `metrics-after-phase-5d-follow-up.json`,
`phase-5d-follow-up-exit-checks.json`, `phase-5d-follow-up-results.json`, and
`phase-5d-follow-up-*.log`. Historical Phase 5d evidence remains unchanged.

Chapter 6: 4,168 → 4,175 words; twelve sections; mean section prose 319.83.
Part III: 9,422 → 9,429 / 11,050; book: 133,986 → 133,993. Reserve remains 2,750.
Hygiene/alignment, metric/reference regressions, companion build, all 22 labs,
teaching/behavior/lifetime checks, PDF/package targets and extracted-package hygiene
pass. Full PDF remains 418 pages, samples 54 and proposal 6; warnings/bad boxes are
zero. Physical pages 64–68 were rendered and inspected: the relocated introduction,
headers, credentials, recap and exercises fit without clipping or overlap.
Local images: `build/phase-5d-follow-up-visual/`. No application/test implementation
changes. Initial logs retain a corrected registered-anchor name and sandbox-denied
socket execution; the required local network tests subsequently passed with socket
access. No physical Bluetooth execution is claimed.

Separate commit: `proposal-readiness: phase 5d follow-up — relocate stranded Unix-socket introduction`.
This freshly passed gate is the authorized Phase 5e entry baseline. The author also
clarifies that budgets are ceilings: remove repetition, preserving explanations,
examples and technical qualifications instead of cutting merely to undershoot.


## Phase 5e — Part IV, 2026-09-22

Baseline: `metrics-after-phase-5d-follow-up.json`, after the separate author-requested
Unix introduction correction and freshly passing gate. After:
`metrics-after-phase-5e.json`; assertions: `phase-5e-exit-checks.json`.
Budgets are ceilings. Cuts remove mirrored responsibility statements, repeated
construction summaries and explanatory arrow blocks; they do not remove distinct
examples or technical qualifications merely to undershoot a ceiling.

| Chapter | Words before → after / ceiling | Prose before → after | Fenced words before → after | Sections before → after / ceiling | Mean section prose |
| --- | ---: | ---: | ---: | ---: | ---: |
| 9 | 4,298 → 3,089 / 3,200 | 3,994 → 2,913 | 304 → 176 | 29 → 8 / 8 | 345.75 |
| 10 | 3,867 → 2,265 / 2,800 | 3,576 → 2,129 | 291 → 136 | 27 → 6 / 7 | 328.33 |
| 11 | 3,626 → 2,555 / 2,800 | 3,305 → 2,362 | 321 → 193 | 27 → 7 / 7 | 312.57 |

Part IV: **11,791 → 7,909 / 8,800 words**, including objectives, recaps and exercises.
Reserve used: **0**; remaining: **2,750**. Every original executable excerpt remains
byte-identical and in order within each chapter. Fenced reductions remove `text`
blocks; the line command mapping is now a table. Index occurrences, figures,
source markers and stable topic anchors remain. Edited and reread: all three
chapters, their public solutions, the Part IV opener and the transition into the
unchanged Part V opener. Visual review is recorded separately.

### Objective ↔ exercise mapping

Each chapter opens with three objectives and closes with one recap (five bullets
in Chapters 9–10, four in Chapter 11), then five exercises. Objective callouts
start at line 3; exercise callouts are at Ch9:385, Ch10:294 and Ch11:396.
All public answers below live in `companion/exercises/chNN/README.md`, under the
matching numbered exercise heading.

| Exercise | Tier | Objectives | Public answer / observable lab |
| --- | --- | --- | --- |
| 9.1 | Review | O1 | ch09 §1: consumed bytes, complete commands and lifetime |
| 9.2 | Review | O3 | ch09 §2: inactivity versus progress deadline, queue admission |
| 9.3 | Lab | O1, O2 | ch09 §3; `exercise-ch09-framing` |
| 9.4 | Lab | O2 | ch09 §4; `exercise-ch09-limits` |
| 9.5 | Design | O1, O3 | ch09 §5: parser state versus accepted model and slow-peer policy |
| 10.1 | Review | O1 | ch10 §1: attachment, ownership handoff and refusal |
| 10.2 | Review | O3 | ch10 §2: copied value, reference and shared ownership |
| 10.3 | Lab | O2 | ch10 §3; `exercise-ch10-isolation` |
| 10.4 | Lab | O1 | ch10 §4; `exercise-ch10-refusal` |
| 10.5 | Design | O1, O3 | ch10 §5: two input roles, one model, explicit dependencies |
| 11.1 | Review | O1 | ch11 §1: source/component edits and unchanged protocol files |
| 11.2 | Review | O3 | ch11 §2: carrier change does not transfer authorization |
| 11.3 | Lab | O1, O2 | ch11 §3; `exercise-ch11-part-checkpoint` |
| 11.4 | Lab | O2, O3 | ch11 §4; `exercise-ch11-endpoint-failure` |
| 11.5 | Design | O1, O3 | ch11 §5: local helper versus TLS input |

| Objective | Exercises |
| --- | --- |
| 9.O1 | 9.1, 9.3, 9.5 |
| 9.O2 | 9.3, 9.4 |
| 9.O3 | 9.2, 9.5 |
| 10.O1 | 10.1, 10.4, 10.5 |
| 10.O2 | 10.3 |
| 10.O3 | 10.2, 10.5 |
| 11.O1 | 11.1, 11.3, 11.5 |
| 11.O2 | 11.3, 11.4 |
| 11.O3 | 11.2, 11.4, 11.5 |

### Built and run

All six new registrations pass within **28/28** public labs:
`phase-5e-final-companion.log`, `phase-5e-final-labs.log` and
`phase-5e-final-results.json`. They are registered through the existing companion
CMake/CI path; no hosted run is claimed. Public READMEs give exact commands,
expected observations, setup and limits.

- Framing: 26 two-piece segmentations (including coalesced input) each reconstruct
  the same PONG/OK/unknown-command/PONG replies. Empty lines, CRLF and QUIT closure
  are included. A separate incomplete `PI` case remains quiet during a bounded
  interval before completion. This varies writes, not kernel callback scheduling.
- Length: 4096 bytes preceding newline are admitted, including a carriage return;
  4097 close with or without a delimiter before interpretation. Immediate closure
  may discard the queued error diagnostic. The test requires EOF and permits only
  a prefix of that diagnostic, never an unknown-command response. The initial
  stronger delivery assumption failed (`phase-5e-part-labs.log`); the correction
  aligns with the existing framing contract, without modifying application code.
- Isolation: a pending prefix on one peer does not affect another; closing it and
  opening a replacement does not carry partial input into the new context.
- Refusal: a test-only factory returns `nullptr` once; the first peer sees closure
  without READY. Later creation delegates to the unchanged canonical factory and
  yields READY/PONG. No supplied connection is manually deleted.
- Part IV checkpoint: the same context/factory sources process the framing cases
  over IPv4 and a private Unix path. Recorded replies are identical; the server
  removes its path before fixture-directory cleanup. This is input framing, not
  CSV validation or measurement acceptance.
- Endpoint failure: a nonexistent Unix path fails before protocol readiness, while
  a valid peer gets a command error and can continue with PING. This distinguishes
  endpoint selection from parser behavior.

The canonical line parser and factory remain the only protocol implementation.
The Unix target derives the three entry-point substitutions at configure time
and links the fourth change, the selected Unix component. `protocol.py` reuses the common bounded
process harness; no service, radio, broker or database is needed. The two-piece
cases do not certify every possible receive schedule; output saturation, deadlines,
TLS policy and accepted-model integration are not executed by these labs.

### Retained teaching and editorial decisions

| Distinct content retained | Final manuscript evidence |
| --- | --- |
| Connection/context/factory distinction and generic versus stream surface | Ch9:15, :47 |
| Readiness, attachment/detachment, input accounting, signals and errors | Ch9:71 |
| Entire abridged line context, delimiter/CRLF rules, complete and incomplete overlong input, independent-peer exercise | Ch9:120 |
| Explicit state/dependencies, receive discipline, inactivity versus deadline, shutdown and metric interpretations | Ch9:244 |
| Scoped logging, facade distinction, detach reason and shutdown despite signal return | Ch9:330 |
| Mental reconstruction questions, queue admission and no unbounded shadow queue | Ch9:350, :367 |
| Raw-pointer ownership handoff, null creation, initial attachment and staged replacement excerpts, fresh-context rule | Ch10:17 |
| Context/type/role construction examples and stable dependencies | Ch10:79 |
| Service location versus explicit dependency, parser state versus model ownership | Ch10:148 |
| Argument forwarding plus value/reference/shared-ownership tradeoff table and MiniGateway lifetime example | Ch10:165 |
| Separate, parameterized, preconfigured and selecting factory patterns, all existing examples | Ch10:204 |
| Independent-peer/replacement test and refusal behavior | Ch10:271 |
| Transfer map/figure, context/factory stability and applied rules | Ch11:17, :38, :135 |
| All five carrier type examples, address/deployment tables and TLS qualification | Ch11:87 |
| Echo excerpts and full runnable IPv4/Unix transfer with all commands and peer listing | Ch11:135, :192 |
| Public header/component matrix beside its applied transfer | Ch11:192 |
| Role examples, preconfiguration, explicit lower-family setup | Ch11:281 |
| Specialization, meaningful small duplication, trust differences and configuration transition | Ch11:346 |

The repeated echo-method summary in Chapter 9 is subsumed by its earlier interface
and worked-context discussion; its index entries now accompany the echo-to-line
transition. Chapter 10's repeated ownership section is folded into the interface
and attachment explanation, where its index entries now belong. Chapter 11's
repeated deployment endorsement is folded into the family comparison; the detailed
qualification about when reuse should stop remains. No new generic chapter treatment
replaces the author's explanations, and the unused word allowance is not a reason
to cut further. None of this Part's approved budgets triggers the >35% stop rule;
the content audit above still records preservation explicitly.


## Phase 5f — Part V, current Chapters 12–13 (2026-09-22)

Edited and reread both full chapters, their Part V opener, public solution READMEs,
and the transitions from Chapter 11 and into the unchanged Part VI opener. The
ordered Markdown inputs remain the manuscript authority. This is the Part V pass;
no later chapter is certified here.

### Chapter metrics and preserved teaching

| Chapter | Total before → after | Ceiling | Prose before → after | Fenced before → after | Headings before → after / ceiling | Mean section prose after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 8,615 → 4,273 | 5,400 | 8,104 → 4,023 | 511 → 250 | 73 → 10 / 16 | 391.2 |
| 13 | 3,779 → 2,698 | 2,750 | 3,479 → 2,481 | 300 → 217 | 20 → 7 / 7 | 340.43 |

Part V chapters total **6,971 / 8,150** words; no reserve used, **2,750** remains.
The ceilings do not require filling unused space or cutting substantive content.
Chapter 12 triggers the author’s preservation stop rule. Its reduction comes from
merging the former configuration principles/anatomy treatments: repeated hierarchy,
input-path, naming, scope catalogue, persistence and parameterless-activation
explanations. The detailed qualifications below survive. Chapter 13 retains its
API examples, error semantics, policy timing and diagnostic limitations while
compressing repeated framing around them. The 25 removed text fences contain
restated diagrams, questions or vocabulary; all executable/configuration fences
and complete listings remain byte-identical. See the phase manuscript diff and
`check-phase-5f.py` preservation assertions.

### Objective ↔ exercise mapping

Both chapters open with three observable objectives and close with five recap
bullets followed by two review questions, two labs and one design problem.
Public solutions use the same numbering and objective IDs.

| Exercise | Tier | Objectives | Public solution / executable observation |
| --- | --- | --- | --- |
| 12.1 | Review | O1 | ch12/README.md: peer observation versus configurable endpoint; three views |
| 12.2 | Review | O2 | ch12/README.md: reparse success/failure versus live activity |
| 12.3 | Lab | O1, O2 | ch12/configuration.py precedence: 8080 → 18091 → 18092; file unchanged |
| 12.4 | Lab | O1, O2 | ch12/configuration.py discovery: help narrows scope; port 70000 rejected |
| 12.5 | Design | O2, O3 | ch12/README.md: independent uplinks, disabled admin role and replacement policy |
| 13.1 | Review | O1 | ch13/README.md: origin, boundary, optional identity and connection lifetime |
| 13.2 | Review | O2, O3 | ch13/README.md: ordered overrides, evaluation and confidentiality |
| 13.3 | Lab | O1, O2 | ch13/records.py: four canonical JSON records; no invented peer |
| 13.4 | Lab | O1, O2, O3 | ch12/configuration.py checkpoint: selected endpoint echoes with scoped records |
| 13.5 | Design | O3 | ch13/README.md: submission versus delivery; safe failure evidence |

Solution paths above are relative to `companion/exercises/`. Exact build/test
commands and expected observations are in each README’s numbered lab sections.

| Objective | Exercises that assess it |
| --- | --- |
| 12.O1 | 12.1, 12.3, 12.4 |
| 12.O2 | 12.2, 12.3, 12.4, 12.5 |
| 12.O3 | 12.5 |
| 13.O1 | 13.1, 13.3, 13.4 |
| 13.O2 | 13.2, 13.3, 13.4 |
| 13.O3 | 13.2, 13.4, 13.5 |

### Content-preservation audit

Evidence paths below are `manuscript/chapters/12-configuring-applications-and-named-instances.md`
(Ch12) and `manuscript/chapters/13-logging-diagnostics-and-runtime-introspection.md`
(Ch13). All index occurrences and stable anchors remain; no figure was removed.

| Retained explanation, example or qualification | Evidence |
| --- | --- |
| Named endpoint registration versus explicit activation; all three input paths, pointer/section qualification and convenience calls | Ch12:9, :32 |
| CLI > file > C++ precedence, late registration, shared endpoint settings versus distinct flow controllers | Ch12:111, :117 |
| Anonymous helper clients and local helper servers, operator-facing names, disablement versus lifecycle controls | Ch12:119 |
| Parameterless activation, server/client/TLS required values and application choice over runtime changes | Ch12:178 |
| Application/instance/section scope; representative hierarchy figure, deeper/anonymous-node qualification; variable rename versus operational-key compatibility | Ch12:211 |
| Full section catalogue: local/remote/address families, accepted peer ≠ configurable remote, connection timeouts/block sizes, socket retry/backoff/jitter, server limits, TLS specialization | Ch12:280 |
| API/CLI/INI examples, progressive help and schematic required-value errors | Ch12:375 |
| RUNNING/event-loop-thread reparse, original CLI priority, re-created registered roles, final validation, failure without rollback, frozen bootstrap, future activation/restart choice | Ch12:444 |
| Canonical echo experiment, inspection status 2, commented defaults, one-run override versus write action | Ch12:468 |
| Durable values versus run-specific actions, shown/generated configuration and command-line views | Ch12:507 |
| INI comment metadata, deeper/anonymous nodes, effective/configured/default values, incomplete historical/default/validator information | Ch12:538 |
| snodec-control preview/materialize/canonical save/preflight/run distinctions, optional UI and separate build switches | Ch12:549 |
| Frozen logging and policy snapshots, readable multi-instance files, protocol/factory ownership, FlowHandle/terminateFlow/setOnDestroy distinctions | Ch12:564, :594 |
| Diagnostic evidence table and scope/event/filter figure | Ch13:14 |
| Public logger constructors/defaults, origin versus layer, exact component keys, optional owned identity strings, live-connection derivation without ownership | Ch13:34 |
| Inherited helper/facade differences, private-helper limits, Diagnostic responsibility rule | Ch13:129, :138 |
| Severity versus control, warn/Warning, bounded formatting language/errors, stable observed event names, errno capture and typed categories | Ch13:142 |
| Ordered thresholds, scoped pairs/numeric global option qualification, standalone versus runtime bootstrap, frozen reparse policy and logger creation timing | Ch13:208 |
| Complete canonical SemanticLogging listing and constructed-error qualification | Ch13:237 |
| Versioned JSON/absent fields, terminal/plain validation, quiet versus file sinks, synchronous borrowed binary dump including NUL/empty/unbounded-size semantics | Ch13:273 |
| Disabled dump/formatting versus evaluated arguments, guard without protocol side effects, caching limits and confidentiality | Ch13:295 |
| Attempt/connection/context/session distinctions and counter scopes; reproducible Part V checkpoint | Ch13:313 |

### Built, run, and limits

`phase-5f-final-companion.log` builds the canonical EchoPair and SemanticLogging
through the existing CI path; the four new registrations pass within **32/32**
public labs (`phase-5f-final-labs.log:322–354`, :404). No hosted run is claimed.
The tests share the existing bounded process harness and isolated environment.
The public JSON observer replaces the former duplicate smoke-test assertions;
all previous assertions survive, with absence-of-invented-identity checks added.
Application implementations and printed executable examples remain unchanged.

The precedence fixture reads the one known port assignment, distinguishing comments
from an active assignment; it is not a general configuration parser. Display/help
status 2 is accepted explicitly. The rejected value identifies `--port`, not a
full instance/section path; the command and local help identify that scope. The
checkpoint confirms real loopback reflection at the CLI-selected port in both
logging policies and checks actual semantic context identity. Suppressed output
alone is never taken to mean no activity.

These are startup observations. Runtime reparse, rollback, live listener replacement,
control-tool UI, TLS, broker and deployment behavior are not executed by these
labs. Their retained explanations are editorially reread, not newly runtime-certified.
The Part V checkpoint prepares reproducible named-role operation for MiniGateway;
it does not add a second gateway or logging implementation.


## Phase 5g — Part VI, current Chapters 14–15 (2026-09-22)

Edited and reread both chapters, the Part VI opener, both public solution READMEs,
and transitions from Chapter 13 and into the unchanged Part VII opener. The
reductions consolidate repeated layer descriptions, lifecycle definitions and
summary questions. Budgets are ceilings; unused allowance is not a reason to
remove teaching content. Neither approved chapter budget triggers the >35% stop
rule, and no reserve is used: **2,750 remains**.

| Chapter | Total before → after | Ceiling | Prose before → after | Fenced before → after | Headings before → after / ceiling | Mean section prose after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 14 | 3,789 → 2,576 | 2,950 | 3,592 → 2,511 | 197 → 65 | 21 → 8 / 8 | 292.62 |
| 15 | 4,534 → 2,990 | 3,400 | 4,220 → 2,922 | 314 → 68 | 37 → 8 / 9 | 339.88 |

Part VI chapters: **5,566 / 6,350** words, including pedagogical apparatus.
The 25 removed text fences restate sequences, distinctions or questions. All
executable/configuration fences, C++ listing order, marked complete listings,
index occurrences, figures and stable topic anchors survive unchanged. See
`phase-5g-manuscript.diff` and `check-phase-5g.py`.

### Objective ↔ exercise mapping

Each chapter has three objectives, five recap bullets and five exercises in
order: two reviews, two labs, one design. Paths below are relative to
`companion/exercises/`; the README lab sections contain commands and expected
observations, and all review/design sections contain public answers.

| Exercise | Tier | Objectives | Solution and observation |
| --- | --- | --- | --- |
| 14.1 | Review | O1 | ch14/README.md:3 — wrapper responsibilities and conditional protocol reuse |
| 14.2 | Review | O2, O3 | ch14/README.md:12 — trust/name/SNI; early callback versus secure readiness |
| 14.3 | Lab | O2, O3 | ch14/README.md:23; tls.py policy — three identity outcomes and early null SSL |
| 14.4 | Lab | O1, O3 | ch14/README.md:52; tls.py echo — binary reflection and reciprocal close-notify |
| 14.5 | Design | O1, O2, O3 | ch14/README.md:71 — service/proxy trust, identity and authorization |
| 15.1 | Review | O1, O2 | ch15/README.md:3 — failed activation, lost peer, disablement and NO_RETRY |
| 15.2 | Review | O1, O3 | ch15/README.md:14 — inactivity, deadline, admission and delivery |
| 15.3 | Lab | O1, O2 | ch15/README.md:24; recovery.py retry — two refused attempts, no attachment, natural exit |
| 15.4 | Lab | O1, O2, O3 | ch15/README.md:43; recovery.py checkpoint — TLS identity outcomes, peer restart, fresh connection and echo |
| 15.5 | Design | O2, O3 | ch15/README.md:71 — recovery/queue/deadline budget and replay contract |

| Objective | Exercises that assess it |
| --- | --- |
| 14.O1 | 14.1, 14.4, 14.5 |
| 14.O2 | 14.2, 14.3, 14.5 |
| 14.O3 | 14.2, 14.3, 14.4, 14.5 |
| 15.O1 | 15.1, 15.2, 15.3, 15.4 |
| 15.O2 | 15.1, 15.3, 15.4, 15.5 |
| 15.O3 | 15.2, 15.4, 15.5 |

### Content-preservation audit

Evidence paths are `manuscript/chapters/14-tls-across-the-framework.md` (Ch14)
and `manuscript/chapters/15-timeouts-retries-and-failure-modes.md` (Ch15).
All existing complete/excerpt executable listings and tables retain their
technical content; repeated prose around them is consolidated.

| Retained explanation, example or qualification | Evidence |
| --- | --- |
| TLS position, available-wrapper qualification, carrier identities, layer figure and legacy/TLS comparison | Ch14:17 |
| Both wrapper alias listings, factory/context mapping, conditional reuse and getSSL access | Ch14:48 |
| Ordinary configuration scopes, identity/trust/policy/timing table, client/server SNI distinction | Ch14:100 |
| Explicit trust versus verification-disabled mode, SNI versus expected identity, early SSL_CTX/null SSL timing, shared endpoint policy | Ch14:126 |
| Full DNS-policy sketch, required headers/trust file, IP-identity qualification and three-outcome local fixture | Ch14:134, :147, :151 |
| Transport existence versus secure readiness and context attachment, handshake/shutdown failure | Ch14:163 |
| Bounded existing shutdown, helper joining/idempotence, read observation during STOPPING, forced termination and non-vetoing signal callback | Ch14:176 |
| Unix permissions, Bluetooth discovery/pairing/PSM, supported-carrier transfer and TLS-sensitive protocol examples | Ch14:191 |
| Diagnostic boundary/error capture, scoped identity, privacy, failed-handshake/retry correlation, transfer experiment, proxy trust and deployment responsibility | Ch14:209 |
| Protocol continuity rule; teaching recap and mapped exercises | Ch14:232, :244, :252 |
| Timeout/retry/reconnect/shutdown/termination distinction, owner table and deliberate stop | Ch15:18 |
| All timeout/delay scopes, inactivity versus deadline, instance policy versus independent activation controllers, protocol-timeout examples | Ch15:38 |
| Retry/reconnect figure and rule, both original timer excerpts, retained flow, sibling independence, completion versus termination callbacks | Ch15:85 |
| Retry enablement/count/fatal/timer checks, server/client comparison, scaling cap before jitter, retry-tries 0/1, indefinite versus finite policy | Ch15:138, :146 |
| Fatal category versus retry permission, NO_RETRY semantics, disablement and phase/ownership tables | Ch15:179, :192 |
| Queue defaults/watermark constraints, unchanged CLI example, immutable snapshots, four admission results and admission versus delivery | Ch15:226 |
| Void-send overflow failure, frame atomicity, bounded application alternatives, pipe hysteresis, no resume during shutdown, HTTP fragment failure | Ch15:267 |
| Inactivity/byte/deadline distinction, 4096-byte line example, absolute-deadline renewal qualification, missing extra deadline in teaching server | Ch15:279 |
| Uncertain delivery, idempotency/operation identifiers, diagnostic scopes and Part VI checkpoint | Ch15:298, :300, :321 |
| Five recap bullets and mapped exercises | Ch15:323, :331 |

The single removed self-reference R204 is retired explicitly in the reference
register; the timing explanation remains at Ch15:70. Other migration identities
and intended targets are retained, and both new solution headings are registered.
The reference checker covers 327 current references and all 374 migration identities.

### Built, run, and limits

The four new registrations pass within **36/36** public labs in
`phase-5g-final-labs.log`; `phase-5g-final-companion.log` records their builds.
Ch14 compiles the existing TLS policy probe and derives a TLS entry point from
canonical EchoPair's two wrapper substitutions, sharing its unchanged context.
Ch15 uses unchanged EchoPair and the same TLS fixture. No second echo, TLS policy
implementation or recovery controller was added. Test support is +171/−1 lines
(net +170), including registrations; application code is +0/−0.

The TLS probe observes trusted matching success, trusted wrong-name rejection,
untrusted matching-name rejection and early null SSL. A separate independent TLS
client observes binary reflection and reciprocal close-notify. The checkpoint
then uses a legacy TCP peer to observe failed activation before attachment and
recovery after peer loss, with distinct connection identities, a fresh greeting
and exact echo. It does not claim that this second half exercises TLS reconnect
or automatic application replay. Fixtures use temporary keys/configuration,
loopback, finite retries and bounded waits; OpenSSL and TLS support are required.

The first secure-echo development run used incorrect certificate option names;
local help identified `--cert` and `--cert-key`, and the corrected run passes.
The first full suite exposed a native lab's library lookup outside the selected
installation. Re-execution with that installation's runtime path passes all 36;
no application or previous lab was changed. Both initial logs are retained.
No hosted CI, production PKI, authorization deployment, stalled TLS peer,
concurrent shutdown-path matrix or protocol-deadline implementation is claimed.

### Phase 5g author follow-up: public fixture placement

Chapter 14 now points to `companion/exercises/ch14/` and prints the root-project
lab build and focused CTest command. `tls-runtime.cpp` and `run-tls.py` moved there
unchanged; both current consumers use that single implementation. Public solution
14.3 documents these local files. All objective mappings and observations remain.
Chapter 14 is 2,579 words (2,508 prose + 71 fenced), mean section prose 292.25;
Part VI 5,569 / 6,350. All 36 public labs and the review consumer pass; original
metrics remain historical. See REPORT.md's follow-up and
`metrics-after-phase-5g-follow-up.json` for the authorized next-phase baseline.
