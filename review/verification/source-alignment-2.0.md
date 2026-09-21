# SNode.C 2.0 source-alignment scope

Framework source: `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`, project version
`2.0.0`. Book starting point: `ccbe53b35dc0013c252e31335aa2aae69cf2659e`.

This pass keeps the 38-chapter order and the MiniGateway application architecture.
It is a source-alignment pass, not another acquisition review or compression pass.

## Chapter responsibilities

| Area | Chapters | Treatment |
|---|---|---|
| Semantic logging | 18 | Reconstructed around the public facade, semantic scope, typed errors, startup policy, output, and diagnostic cost |
| Framework testing | 34 | Reconstructed around registered unit, component, policy, staged-installed, and external-consumer checks; debugging/deployment/benchmarking reasoning retained |
| Startup and source navigation | 2-4 | Current source checkout, build switches, complete chapter echo companion, tests/docs/tools navigation |
| Runtime and context lifecycle | 6, 9, 13, 19 | Coordinated shutdown, attempt/connection/context distinction, inherited logging, TLS cleanup |
| Unix transport | 11 | Peer credentials as transport facts, separate from authorization |
| Configuration | 16-17 | Comment metadata, target-driven control tooling, logging and resource-policy placement |
| Resource/streaming contracts | 20-21, 23-24 | Queue admission, watermarks, HTTP parser/server policies, SSE streaming exception, descriptor ownership, WebSocket receiver limits |
| Source examples and build/deployment | 29, 32-33, 38 | Current logging excerpts, source/test distinctions, build flags, public headers, ABI rebuilds, and regression taxonomy |
| Protocol and capstone listings | 3, 21, 23-25, 28-29, 35-36, 38 | Removed obsolete macro calls; complete marked listings synchronized with companion files |
| Stable architecture | Other chapters | Structure and conceptual explanation retained; baseline/reference checks only where relevant |

Figures 14 and 18 retain their figure IDs and source filenames but now depict
semantic logging and actual evidence categories. The other figures are unchanged.
A final publisher-format figure polish remains a separate production activity.

## Reproducibility controls

- `source-baseline/book-source-baseline.env` drives the framework checkout.
- `ci/check-source-alignment.py` checks the source declaration and exact marked
  complete listings. Unmarked illustrative excerpts are not falsely classified as
  separately built programs.
- `ci/build-companion-examples.sh` checks the framework checkout, enables its
  registered CTest suite, installs it, checks its external echo project, and builds
  the book companions. The supplied-installation path explicitly reports that it
  has not verified the framework commit or run framework tests.
- New teaching smoke checks observe the complete echo and public-logging programs.
  Existing selected SSE and MiniGateway Extended checks remain distinct.
- Verification logs are uploaded per compiler. Passed, failed, and skipped results
  must be read for the exact workflow run.
- Publication/package checks retain figure/reference/index builds and reject
  duplicate archive entries.

## Evidence and limits

Current results are run-specific. No test result is invented by this scope note.
Original author-local confirmations retain their original source pin and date in
`history/`; they are not silently transferred to this edition.

The source review uses current public headers, implementation, test registrations,
and selected test bodies. Historical logging migration reports are not used as an
independent authority when they disagree with current code. In particular,
`<Log.h>` and `snode::log` are the application facade, while existing context
helpers still return the lower-level object-scoped logger type.

Remaining external validation includes full MQTT/broker exchange, MariaDB service
integration, Bluetooth/platform checks, OpenWrt deployment, load/long-duration
behavior, and independent technical review. The presence of a test or a passing
selected CI path is not universal protocol, security, or deployment certification.
