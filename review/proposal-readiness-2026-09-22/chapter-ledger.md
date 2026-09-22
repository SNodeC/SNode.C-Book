# Phase 2 chapter ledger

Date: 2026-09-22. Measurement authority: `ci/manuscript-metrics.py`.
Before: `metrics-before-phase-2.json`; after: `metrics-after-phase-2.json`.
Prose counts include Markdown, objectives, recaps, and exercises; fenced code is
excluded. Section averages use non-overlapping level 3–6 section bodies, excluding
headings and preambles, exactly as in Phase 0. Filename labels remain next to
complete listings; they are not separate conceptual sections.

| Chapter | Prose before | Prose after | Reduction | Sections before → after | Average section prose after | Editorial state |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [1](../../manuscript/chapters/01-why-snodec-exists.md) | 2,343 | 1,604 | 31.54% | 10 → 5 | 303.40 | edited and reread in context |
| [3](../../manuscript/chapters/03-your-first-working-program-the-echo-pair.md) | 2,674 | 1,934 | 27.67% | 23 → 6 | 306.67 | edited and reread in context |
| [23](../../manuscript/chapters/23-server-sent-events-and-real-time-http.md) | 3,664 | 2,843 | 22.41% | 31 → 7 | 390.29 | edited and reread in context |
| [35](../../manuscript/chapters/35-building-minigateway.md) | 2,378 | 1,752 | 26.32% | 35 → 6 | 275.83 | edited and reread in context |
| [37](../../manuscript/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md) | 2,395 | 1,868 | 22.00% | 15 → 6 | 292.50 | edited and reread in context |

## Objectives and exercises

Each sample has three observable objectives and three exercises: one review,
one lab, and one design problem. The mappings below cover both directions.
Objective and exercise wording are in the linked chapter's opening and closing
callouts; public solution sections use the same numbers and objective IDs.
`phase-2-exit-checks.json` verifies the IDs and three tiers mechanically.

| Chapter | Objective | Exercise | Public solution and evidence of learning |
| --- | --- | --- | --- |
| 1 | O1: distinguish protocol and state ownership | 1 — review | `companion/exercises/ch01/README.md`, §1: shared sequencing authority |
| 1 | O2: compare two built echo servers | 2 — lab | `ch01/solution.py`: 20,480 binary bytes and a later session on both servers |
| 1 | O3: select a framework under constraints | 3 — design | `ch01/README.md`, §3: Linux gateway versus native Windows utility |
| 3 | O1: distinguish handle, factory, context | 1 — review | `ch03/README.md`, §1: creation and ownership handoff |
| 3 | O2: change greeting and observe reflection | 2 — lab | `ch03/greeting-client.cpp` and `solution.py`: actual EchoPair plus controlled peer |
| 3 | O3: locate endpoint versus protocol failure | 3 — design | `ch03/README.md`, §3: connection result, receive count, initial greeting |
| 23 | O1: explain typed events and release | 1 — review | `ch23/README.md`, §1: field dispatch and disconnect-to-unsubscribe lifetime |
| 23 | O2: compare acceptance and observation | 2 — lab | `ch23/solution.py`: matching POST/event data, restricted Accept, current-state reconnect |
| 23 | O3: choose bounded recovery policy | 3 — design | `ch23/README.md`, §3: queue/history bounds, expired IDs, disconnected UI |
| 35 | O1: trace the common acceptance path | 1 — review | `ch35/README.md`, §1: MQTT decode → model → observers |
| 35 | O2: observe HTTP/SSE without MQTT | 2 — lab | `ch35/solution.py`: matching state and events, process restart resets sequence |
| 35 | O3: distinguish durable/delivery/origin guarantees | 3 — design | `ch35/README.md`, §3: transactional state and explicit origin contract |
| 37 | O1: identify authority over ordering | 1 — review | `ch37/README.md`, §1: gateway sequence versus producer sample number |
| 37 | O2: observe order and unsubscribe | 2 — lab | `ch37/model-ownership.cpp`: inputs 900,2,1; accepted 1,2,3; one observer detached |
| 37 | O3: choose operational boundaries | 3 — design | `ch37/README.md`, §3: privileged collector, bounded IPC, independent recovery |

All abbreviated solution paths above are relative to `companion/exercises/`.
The lab build commands and observable expected outputs are public in each README;
all five CTest lab cases were run, not merely registered. See `phase-2-labs.log`.
The compiler run is `phase-2-companion.log`; the initial harness errors and their
resolution are explained in REPORT.md rather than omitted.

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
