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
