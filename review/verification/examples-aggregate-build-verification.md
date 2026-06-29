# Companion Examples Author Verification

This note records the current author-confirmed local verification status for the companion-example project under `companion/examples/`. It is package evidence, not manuscript prose, and is not intended to appear in the printed book.

## Verification baseline

The examples were checked against the SNode.C book baseline recorded in `source-baseline/SOURCE-VERSION.md` and `source-baseline/book-source-baseline.env`:

```text
Repository: https://github.com/SNodeC/snode.c.git
Release tag: v1.0.2
Commit: 6e475262084ae2dab2daef8781ab9e4adb82d18e
Verification date: 2026-06-28
Verification type: author-confirmed local configure/build/run and runtime smoke check
```

This verification is author-confirmed local verification. It is not presented as independent continuous-integration evidence. The pinned public release tag and commit make the check reproducible by a later CI job or reviewer-run build.

## Scope

The aggregate companion-example project is:

```text
companion/examples/CMakeLists.txt
```

The verification covers the current companion-example set shipped with this package:

```text
companion/examples/HttpUpgrade-Server
companion/examples/HttpUpgrade-Client
companion/examples/SSE-Server
companion/examples/SSE-EventSource-Client
companion/examples/WebSocket-Echo-ServerSubprotocol
companion/examples/WebSocket-Echo-ClientSubprotocol
companion/examples/LineProtocol-Server
companion/examples/LineProtocol-Client
companion/examples/MQTT-ClientRole
companion/examples/MariaDB-Minimal
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```

## Required SNode.C public-header baseline

The companion examples require the SNode.C `v1.0.2` release-tag commit recorded above. That commit contains the public header surface expected by the examples, including:

1. the concrete EventSource convenience headers, such as `web/http/legacy/in/EventSource.h`, installed with the HTTP client component;
2. `database/mariadb/MariaDBClient.h` exposing the complete `MariaDBCommandSequence` type needed by the fluent MariaDB command-sequence API.

These are SNode.C public-surface requirements, not book-example workarounds. The companion examples intentionally use the consumer-facing headers they require.

## Author-confirmed result

The author confirmed that the complete companion-example set configured, compiled, linked, installed/deployed where applicable, ran where intended, and behaved as expected against the pinned SNode.C `v1.0.2` baseline.

| Area | Status | Evidence type |
|---|---:|---|
| SNode.C baseline | confirmed | release tag `v1.0.2` and exact commit pin |
| Aggregate companion-example configure/build/link | confirmed | author-confirmed local verification |
| HTTP upgrade examples | confirmed | author-confirmed local build/run behavior check |
| SSE server and EventSource client examples | confirmed | author-confirmed local build/run behavior check |
| WebSocket echo client/server subprotocol examples | confirmed | author-confirmed local build/run behavior check |
| Line protocol server/client examples | confirmed | author-confirmed local build/run behavior check |
| MQTT client-role example | confirmed | author-confirmed local build/run behavior check |
| MariaDB minimal example | confirmed | author-confirmed local build/run behavior check in the author's local service environment |
| MiniGateway | confirmed | author-confirmed local build/run/runtime smoke check |
| MiniGateway Extended | confirmed | author-confirmed local build/run/runtime smoke check |

## MiniGateway coverage summary

MiniGateway-specific details are retained in `review/verification/minigateway-step8-author-verification.md`. In summary, the confirmed smoke coverage includes:

- configure and build `companion/examples/MiniGateway/`;
- run the MiniGateway executable;
- check `/health`, `/status`, and `/simulate`;
- check `/events` with `Accept: text/event-stream`;
- check MQTT measurement input and measurement output behavior;
- configure and build `companion/examples/MiniGateway-Extended/`;
- run the MiniGateway Extended executable;
- check `/health`, `/status`, and `/simulate`;
- check `/events` with `Accept: text/event-stream`;
- check MQTT measurement input and measurement output behavior;
- check the Unix-domain socket measurement input path in MiniGateway Extended.

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

`companion/examples/LineProtocol-Server` and `companion/examples/LineProtocol-Client` are included in the aggregate example CMake project. They follow the same public SNode.C IPv4 legacy stream role pattern used by the repository echo example, but replace byte reflection with a small command protocol. The author confirmed that both examples compiled, linked, ran, and behaved as expected in the current verification pass.

## Conclusion

The companion-example set is considered verified for this manuscript package based on the author-confirmed local configure/build/run and behavior result against SNode.C `v1.0.2`, commit `6e475262084ae2dab2daef8781ab9e4adb82d18e`. No `pending re-check` status remains in this verification note.
