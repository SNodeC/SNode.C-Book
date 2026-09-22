# Phase 5m — final manuscript audit, 2026-09-23

This audit covers the ordered manuscript and public teaching material after the
approved condensation. It does not refresh or certify the proposal's dated market
and revision claims; that work is Phase 6. All evidence paths below are relative
to this report directory unless they explicitly name repository files.

## Global targets

| Measure | Phase 0 measured baseline | Final | Acceptance |
| --- | ---: | ---: | --- |
| Total whitespace words | 151,924 | 100,338 | ≤115,000; stretch ≤105,000 met |
| Prose words | 136,829 | 92,187 | Reduction from prose/repeated framing |
| Fenced words, including text diagrams | 15,095 | 8,151 | No executable listing cuts in this phase |
| Chapter headings, level 3 and deeper | 1,020 | 252 | ≤550 |
| Mean chapter-section prose words | 124.13 | 334.87 | ≥250; every chapter and appendix also ≥250 |
| Closing perspective sections | 15 | 0 | 0 |
| Rule boxes | 30 | 20 | ≤20, author amendment |
| Text fences | 478 | 45 | ≤250 |
| Forbidden authoring phrases | Historical baseline recorded in metrics | 0 | Active hygiene guards |
| Shell fence labels | sh / shell | sh | One label |
| Teaching units with objectives / exercises / recap | 0 / 0 / 38 recaps | 31 / 31 / 31 | All 30 numbered chapters plus Appendix A |

Sources: `metrics-before.json`, `metrics-after-phase-5m.json`,
`check-phase-5m.py` and `phase-5m-exit-checks.json`. The Phase 0 baseline's two-word
measurement difference from the requested baseline was recorded in that phase;
this audit uses its measured 151,924. Total reduction is **51,586 words**; the
Phase 5m change alone is **−3,123**, comprising −1,770 prose and −1,353 text-fence
words. The remaining nine arrow-containing text blocks describe specific runtime,
acceptance, endpoint, build or database paths, not another general layer-stack
illustration. Their locations are listed below for an inspectable distinction.

## Chapter budgets and teaching contract

The final checker parses rendered headings with Pandoc as well as measuring source.
Every unit has exactly three observable objectives and five mapped exercises in
the order review, review, lab, lab, design, with matching public answer headings.
Every objective is exercised and every exercise names an objective. One recap of
at most five bullets precedes exercises; objectives precede the first subsection.
The current callouts and all twenty applied rules were reread in this phase:
objectives/recaps do not merely repeat chapter titles. This is a scoped teaching
and global audit, not a second full technical prose reread of previous Parts.

| Unit | Words / ceiling | Deep headings / ceiling | Mean section prose | Public solution directory |
| --- | ---: | ---: | ---: | --- |
| 1 | 1,821 / 1,850 | 5 / 5 | 327.00 | `companion/exercises/ch01/` |
| 2 | 3,006 / 3,350 | 8 / 9 | 331.50 | `companion/exercises/ch02/` |
| 3 | 2,568 / 2,650 | 6 / 6 | 321.83 | `companion/exercises/ch03/` |
| 4 | 4,075 / 5,300 | 13 / 15 | 297.38 | `companion/exercises/ch04/` |
| 5 | 2,983 / 3,700 | 10 / 11 | 278.10 | `companion/exercises/ch05/` |
| 6 | 4,175 / 5,200 | 12 / 15 | 319.83 | `companion/exercises/ch06/` |
| 7 | 3,084 / 3,650 | 9 / 10 | 324.67 | `companion/exercises/ch07/` |
| 8 | 2,170 / 2,200 | 5 / 5 | 393.40 | `companion/exercises/ch08/` |
| 9 | 3,089 / 3,200 | 8 / 8 | 345.75 | `companion/exercises/ch09/` |
| 10 | 2,265 / 2,800 | 6 / 7 | 328.33 | `companion/exercises/ch10/` |
| 11 | 2,555 / 2,800 | 7 / 7 | 312.57 | `companion/exercises/ch11/` |
| 12 | 4,273 / 5,400 | 10 / 16 | 391.20 | `companion/exercises/ch12/` |
| 13 | 2,698 / 2,750 | 7 / 7 | 340.43 | `companion/exercises/ch13/` |
| 14 | 2,579 / 2,950 | 8 / 8 | 292.25 | `companion/exercises/ch14/` |
| 15 | 2,990 / 3,400 | 8 / 9 | 339.88 | `companion/exercises/ch15/` |
| 16 | 2,471 / 2,600 | 6 / 6 | 368.17 | `companion/exercises/ch16/` |
| 17 | 2,065 / 2,350 | 5 / 5 | 382.80 | `companion/exercises/ch17/` |
| 18 | 3,269 / 3,300 | 7 / 7 | 398.00 | `companion/exercises/ch18/` |
| 19 | 3,000 / 3,050 | 7 / 7 | 363.14 | `companion/exercises/ch19/` |
| 20 | 2,005 / 2,350 | 5 / 5 | 359.60 | `companion/exercises/ch20/` |
| 21 | 1,782 / 2,100 | 4 / 4 | 409.25 | `companion/exercises/ch21/` |
| 22 | 2,922 / 2,950 | 8 / 8 | 348.50 | `companion/exercises/ch22/` |
| 23 | 3,826 / 3,900 | 10 / 10 | 334.80 | `companion/exercises/ch23/` |
| 24 | 5,591 / 6,200 | 17 / 17 | 304.35 | `companion/exercises/ch24/` |
| 25 | 3,903 / 4,100 | 10 / 10 | 328.00 | `companion/exercises/ch25/` |
| 26 | 3,596 / 3,700 | 10 / 10 | 327.30 | `companion/exercises/ch26/` |
| 27 | 4,169 / 4,200 | 10 / 10 | 376.60 | `companion/exercises/ch27/` |
| 28 | 3,818 / 3,850 | 6 / 6 | 291.50 | `companion/exercises/ch28/` |
| 29 | 2,541 / 3,150 | 6 / 6 | 279.50 | `companion/exercises/ch29/` |
| 30 | 1,850 / 1,900 | 6 / 6 | 287.00 | `companion/exercises/ch30/` |
| A | 3,694 / 4,700 | 9 / 10 | 389.00 | `companion/exercises/appendix-a/` |

Full exercise/objective mappings are in `phase-5m-exit-checks.json` and the per-Part
entries in `chapter-ledger.md`; the new appendix entry records both directions.
There are **93 objectives and 155 exercises**, including **62 lab registrations**.
All 62 execute successfully in `phase-5m-final-labs.log:1160`. Public answers include
commands, expected observations and their limits. Existing earlier solutions and
lab implementations are preserved, not rewritten to pass a changed check.

Chapter 27 retains its documented 400-word reserve allocation: ceiling 4,200.
The planned allocation remains 112,650 and reserve remaining 2,350; this phase
uses none. Front matter is 1,980 / 2,500; Part openers are 1,356 / 1,650; back
matter is 781 / 1,000. The epilogue essay is 1,388 / 1,900, four headings and mean
338.75. Its author-approved exception forbids objectives, recap and exercises;
its philosophical section and final closing passage are mechanically unchanged.

## Running-project checkpoints

The Part openers were reread against their closing-chapter exercises and public
solutions. The full lab run executes the reused tests behind each checkpoint.

| Part | Closing unit | Runnable observation and interpretation |
| --- | --- | --- |
| I | 3 | Measurement-shaped bytes and independent peers; reflection is not domain acceptance |
| II | 5 | Shared acceptance order and observer removal; one model owner |
| III | 8 | IP/Unix identities and owned cleanup; Bluetooth selectors separate from physical radio |
| IV | 11 | Same reconstructed commands over IP/Unix; endpoint versus protocol failure |
| V | 13 | Configuration precedence, actual echo and scoped diagnostics |
| VI | 15 | Three TLS identity outcomes, failed activation and recovery after peer loss |
| VII | 19 | Shared accepted state through SSE observers; separate WebSocket negotiation/message checks |
| VIII | 22 | Subscriber-observed broker delivery versus acceptance during gateway MQTT outage |
| IX | 24 | Committed database row after client restart versus transient gateway restart |
| X | 27 | Fresh external build/install, endpoint diagnosis and bounded timing |
| XI | 30 | Shared HTTP/Unix order, invalid CSV, observer reconnect and in-memory restart |

Appendix A adds source-reading and bounded consumer-extension observations through
existing abstractions. It modifies no framework source and adds no parallel parser.
The CI workflow's normal CTest discovery includes the new registrations
(`.github/workflows/companion-examples.yml:82`). A new hosted run is not claimed.
Optional radio/OpenWrt/service deployment and the manual equipped MiniGateway MQTT
extension remain separate from these passing local lab observations.

## Preservation, references and execution

The checker compares this phase against the completed Phase 5l commit. All **293
executable/configuration fences**, **37 complete source markers**, **1,033 index
entries** and **18 figure IDs** remain. Application code, prior lab drivers, source
manifest/order, Chapters 1–30, Part openers and production styles are unchanged.
The prior phase was freshly verified before editing; its detailed preservation
assertions and all ten check groups passed (`phase-5m-entry-*`).

All existing reference labels, target sets and migration identities are retained;
three new Appendix A references in the public exercise guide/answers are registered.
**298 current references, 39 stable topics and 374 historical dispositions** pass,
including the author's combined R275/R276 seam. Six reference regression checks
pass inside source hygiene (`phase-5m-final-source-recheck.log`).

All ten final check groups pass (`phase-5m-final-results.json`): source hygiene,
alignment, metric regressions, companion build, all labs, teaching, behavior,
lifetime, PDF/package build and extracted-package hygiene. The final spacing-only
edit and answer-file correction did not change runtime implementations; the final
PDF/package rebuild and source recheck are recorded separately. The all-chapter
checker subsequently passes against the final files and artifacts.

The five samples retain ≥20% prose reduction and ≥250 mean section prose. Their
current reductions are recorded in `phase-5m-exit-checks.json`; they were not edited
in this phase. The full PDF is **310 pages** (322 on entry; Phase 0's recorded
artifact was 490), combined samples **54**, proposal **6**. All three final LaTeX
logs have zero warnings and zero bad boxes. **365** archive files match the working
inputs; visual scope and fixes are in `phase-5m-visual-review.md`.

## Retained arrow-block inventory

These blocks make specific paths inspectable. Generic appendix/epilogue stack
repetitions were removed or converted into connected prose and decision tables.

- `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:240` — framework-managed connection.
- `manuscript/chapters/22-designing-iot-systems-with-multiple-protocols.md:120` — sensor reading.
- `manuscript/chapters/23-database-support-and-application-state.md:283` — delete old rows.
- `manuscript/chapters/28-building-minigateway.md:19` — new measurement.
- `manuscript/chapters/28-building-minigateway.md:36` — GET /health.
- `manuscript/chapters/28-building-minigateway.md:162` — domain fact.
- `manuscript/chapters/28-building-minigateway.md:201` — http-server-express-legacy-in.
- `manuscript/chapters/28-building-minigateway.md:414` — MeasurementModel::accept(measurement).
- `manuscript/chapters/28-building-minigateway.md:1014` — stream SocketConnection.

## Completion boundary

Phase 5m and the manuscript-wide Phase 5 targets are **completed**. Proposal
positioning, revision-status prose, current TOC/page extents and evidence-sheet
refresh remain **Phase 6**, not work silently completed by rebuilding the package.
No acquisitions decision, new hosted CI, deployment validation or performance
capacity is inferred from the checks above.
