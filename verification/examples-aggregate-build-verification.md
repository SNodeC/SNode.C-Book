# Companion Examples Author Verification

This note records the current author-confirmed local verification status for the companion-example project under `examples/`. It is package evidence, not manuscript prose, and is not intended to appear in the printed book.

## Verification baseline

The examples were checked against the SNode.C book baseline recorded in `SOURCE-VERSION.md` and `verification/book-source-baseline.env`:

```text
Repository: https://github.com/SNodeC/snode.c.git
Release tag: v1.0.2
Commit: 6e475262084ae2dab2daef8781ab9e4adb82d18e
Verification date: 2026-06-27
Verification type: author-confirmed local build and behavior check
```

This verification is intentionally described as author-confirmed local verification. It is not presented as independent continuous-integration evidence. The pinned public release tag and commit make the check reproducible by a later CI job or reviewer-run build.

## Scope

The aggregate companion-example project is:

```text
examples/CMakeLists.txt
```

The verification covers the current companion-example set shipped with this package:

```text
examples/HttpUpgrade-Server
examples/HttpUpgrade-Client
examples/SSE-Server
examples/SSE-EventSource-Client
examples/WebSocket-Echo-ServerSubprotocol
examples/WebSocket-Echo-ClientSubprotocol
examples/LineProtocol-Server
examples/LineProtocol-Client
examples/MQTT-ClientRole
examples/MariaDB-Minimal
examples/MiniGateway-Base
examples/MiniGateway-Extended
```

## Required SNode.C public-header baseline

The companion examples require the SNode.C `v1.0.2` release-tag commit recorded above. That commit contains the public header surface expected by the examples, including:

1. the concrete EventSource convenience headers, such as `web/http/legacy/in/EventSource.h`, installed with the HTTP client component;
2. `database/mariadb/MariaDBClient.h` exposing the complete `MariaDBCommandSequence` type needed by the fluent MariaDB command-sequence API.

These are SNode.C public-surface requirements, not book-example workarounds. The companion examples intentionally use the consumer-facing headers they require.

## Author-confirmed result

The complete companion-example set configured, compiled, linked, installed/deployed where applicable, ran where intended, and behaved as expected against the pinned SNode.C `v1.0.2` baseline before the later single-exit style rewrite. Because that rewrite now touches the example source trees and the matching manuscript listings, the full companion-example set requires a fresh author re-check.

| Area | Status | Evidence type |
|---|---:|---|
| SNode.C baseline | confirmed | release tag `v1.0.2` and exact commit pin |
| Aggregate companion-example configure/build/link | pending re-check | example sources were mechanically aligned to single-exit style after previous confirmation |
| HTTP upgrade examples | pending re-check | part of the aggregate example set after style pass |
| SSE server and EventSource client examples | pending re-check | SSE server source changed for single-exit route/subscriber flow |
| WebSocket echo client/server subprotocol examples | pending re-check | part of the aggregate example set after style pass |
| Line protocol server/client examples | pending re-check | source and Chapter 13 listing already aligned to single-exit style |
| MQTT client-role example | pending re-check | part of the aggregate example set after style pass |
| MariaDB minimal example | pending re-check | part of the aggregate example set after style pass |
| MiniGateway-Base | pending re-check | MQTT publish and SSE subscriber flow changed for single-exit style |
| MiniGateway-Extended | pending re-check | MQTT publish, SSE subscriber flow, and Unix-socket line handling changed for single-exit style |

## MiniGateway coverage summary

MiniGateway-specific details are retained in `verification/minigateway-step8-author-verification.md`. In summary, the confirmed smoke coverage includes:

- configure and build `examples/MiniGateway-Base/`;
- run the MiniGateway-Base executable;
- check `/health`, `/status`, and `/simulate`;
- check `/events` with `Accept: text/event-stream`;
- check `/events` without `Accept: text/event-stream`, expecting non-SSE rejection or fallback behavior;
- configure and build `examples/MiniGateway-Extended/`;
- run the MiniGateway-Extended executable;
- check `/health`, `/status`, and `/simulate`;
- check `/events` with `Accept: text/event-stream`;
- check `/events` without `Accept: text/event-stream`, expecting non-SSE rejection or fallback behavior;
- check the Unix-domain socket measurement input path in the extended example.

## Reproducibility note

A later CI job or independent reviewer check should use the same public baseline:

```bash
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout v1.0.2
git rev-parse HEAD
```

The final command is expected to print:

```text
6e475262084ae2dab2daef8781ab9e4adb82d18e
```

The examples should then be configured against that installed SNode.C package, preferably through an isolated installation prefix rather than an unrelated system installation.

## Line-protocol example coverage

`examples/LineProtocol-Server` and `examples/LineProtocol-Client` are included in the aggregate example CMake project. They follow the same public SNode.C IPv4 legacy stream role pattern used by the repository echo example, but replace byte reflection with a small command protocol. The author confirmed that both new examples compiled and ran successfully before the broader single-exit style pass. A fresh confirmation is required for the current example set.

## Conclusion

The companion-example set was previously verified by author-confirmed local build and behavior checks against SNode.C `v1.0.2`, commit `6e475262084ae2dab2daef8781ab9e4adb82d18e`. Because the example sources and matching manuscript listings were subsequently aligned to single-exit style, the aggregate example status is pending a fresh author re-check.
