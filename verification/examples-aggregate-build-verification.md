# Companion Examples Aggregate Build Verification

This note records the local build status for the aggregate companion-example project under `examples/`. It is package evidence, not manuscript prose, and is not intended to appear in the printed book.

## Scope

The current aggregate project is:

```text
examples/CMakeLists.txt
```

It is intended to configure and build the compact companion examples and the two MiniGateway final-project examples:

```text
examples/HttpUpgrade-Server
examples/HttpUpgrade-Client
examples/SSE-Server
examples/SSE-EventSource-Client
examples/WebSocket-Echo-ServerSubprotocol
examples/WebSocket-Echo-ClientSubprotocol
examples/MQTT-ClientRole
examples/MariaDB-Minimal
examples/MiniGateway-Base
examples/MiniGateway-Extended
```

## Required SNode.C public-header fixes

The successful build was performed against a locally installed SNode.C package after fixing two SNode.C public header-surface issues exposed by the companion examples:

1. The concrete EventSource convenience headers, such as `web/http/legacy/in/EventSource.h`, must be installed with the HTTP client component.
2. `database/mariadb/MariaDBClient.h` must expose the complete `MariaDBCommandSequence` type needed by the fluent MariaDB command-sequence API.

These are SNode.C fixes, not book-example workarounds. The companion examples intentionally use the public consumer-facing headers they require.

## Reported local build command

The author reported a clean rebuild of the aggregate examples project with parallel make:

```bash
make clean
make -j26
```

## Reported built targets

The local build completed successfully and produced the following targets:

```text
http-upgrade-server
http-upgrade-client
sse-server
sse-eventsource-client
websocket-echo-client-subprotocol
mqtt-client-role
mariadb-minimal
minigateway-base
minigateway-extended
```

The build log reached `100%` and ended with:

```text
[100%] Built target sse-server
```

## Status

The reported build verified the aggregate example set as it existed at the time of the check. The WebSocket echo example was completed later, as described below; therefore the current aggregate project should be rebuilt and redeployed once more before final release. The SNode.C source pin in `SOURCE-VERSION.md` now points to the `Book` tag commit containing the required public-header fixes listed above.

## Later WebSocket echo completion note

After the reported aggregate build, the WebSocket echo companion example was completed by adding the missing server-side echo subprotocol module and by correcting the subprotocol deployment shape. The updated WebSocket echo set now consists of:

```text
HttpUpgrade-Server
HttpUpgrade-Client
WebSocket-Echo-ServerSubprotocol
WebSocket-Echo-ClientSubprotocol
```

The earlier compile/link result does not cover this later WebSocket completion change. The aggregate examples should be rebuilt and redeployed once more before final release.
