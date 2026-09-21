# Combined editorial pass — 21 September 2026

The outcome report is `refinement-2026-09-21.md`; `evidence-2026-09-21.json`
identifies the final source, manuscript inputs and checks. The persistent work
ledger remains `../EDITORIAL-WORK-PLAN.md`.

`pass-baseline-2026-09-21.json` records the editorial starting point after the
previous technical pass. `change-accounting-2026-09-21.json` compares against it,
not against the Git commit preceding the user's existing changes. `repetition-map.md`
records primary teaching locations, resolved/retained repetition and all figures.

The root verification logs belong to the final recorded source unless their names
explicitly indicate an earlier rehearsal or initial harness run. The author edited
the framework during this work, so earlier cohorts are retained separately:

- `verified-clean-2e52b6b/`: clean source after per-call flow and reconfiguration changes.
- `verified-binary-logging-initial/`: first binary-logging snapshot; one HTTP diagnostic
  expectation failed. The body-dump layout had gained an eight-byte grouping gap.
- `verified-binary-logging/`: the updated renderer and expectation passed all 183
  framework tests; later source checking detected the subsequent MQTT logging guard.
- `../verification/refinement-2026-09-21/`: the preceding technical refinement,
  with its original manifest and patch preserved.

The editorial harness errors are retained as such. The first service harness tried
to restart a transient unit after systemd had discarded its stopped definition;
the corrected rehearsal restores and restarts it while loaded. The first precedence
harness counted a commented default beside an active assignment; the corrected
harness selects active assignments first, matching Chapter 17's instructions.
The initial WebSocket harness used debug level 5 while asserting trace-level
application observations. Level 6 exposes those observations; the corrected run
passed. A later precedence rerun was accidentally given the external regression
fixture, which requires an explicit port, instead of Chapter 3's companion echo
with its C++ default of 8080. The recorded rerun uses the Chapter 3 executable,
exactly as Chapter 17 requires. None of these errors was repaired by changing the
application under test.

`config-precedence-2026-09-21.log` and `transfer-check-2026-09-21.log` are initial
exercise rehearsals. The corresponding `*-current-*` logs are fresh repetitions.
Probes in `probes/` extract the printed peer/configuration examples where practical,
use bounded temporary resources, and do not change framework or companion code.
No PDF reading, regeneration, visual QA, OpenWrt execution, live database run,
full MQTT-broker interoperability, Bluetooth-hardware run, or sustained-load
claim is made by this directory.

The Chapter 24 rehearsal deployed the already-built client/server echo modules
into `/tmp/snodec-book-current-install`. Its scratch client copied the companion
`HttpUpgrade-Client` sources, changed only the requested name from
`subprotocol, echo` to `editorial-unsupported`, and built against the same installed
package. `probes/verify-websocket-negotiation.py` ran both clients and an independent
HTTP upgrade request against a temporary loopback listener with isolated config.
The current log records selection, text echo, closure and unsupported-name rejection;
it does not test or fix the separately tracked binary-input behavior.
