# Companion Examples: Verification Scope

## Current source

- SNode.C CMake version: `2.0.0`
- Framework commit: `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`
- Book source: the commit identified by the accompanying CI run or review report.

The aggregate project under `companion/examples/` builds the existing protocol,
persistence, and MiniGateway examples plus the new `EchoPair` and
`SemanticLogging` teaching projects. `MQTT-ClientRole` is a library example, not
a standalone executable; the WebSocket subprotocols are loadable modules.

## Evidence classes

| Check | What it establishes | Limit |
|---|---|---|
| Source/listing check | Marked complete listings equal their companion files | Does not compile illustrative excerpts |
| Framework CTest run | Results for the configured framework suite | Skips and environment limits must be read |
| GCC/Clang companion build | The aggregate project compiles and links on the tested toolchain | Not a claim of every runtime path |
| Selected smoke tests | Echo peer exchange, public logging JSON, SSE, and MiniGateway Extended Unix/HTTP/SSE behavior | No external MQTT broker or MariaDB orchestration |
| Author-local history | Earlier explicitly confirmed local results | Historical source only; not new 2.0 confirmation |

The executable checks are in `ci/build-companion-examples.sh`,
`ci/run-teaching-smoke-tests.py`, and `ci/run-behavior-smoke-tests.py`. The public
workflow records the book SHA and checks the framework SHA. A workflow definition
is a recipe; a particular successful run is the execution evidence.

No current-snapshot author confirmation, all-platform certification, complete
security audit, or exhaustive protocol conformance is implied. Review the actual
run's failed, passed, and skipped tests before stating the result.

The pre-migration author verification is preserved in
`history/examples-aggregate-build-verification.md`, without changing its date or
source pin. MiniGateway details are separated in
`minigateway-step8-author-verification.md`.
