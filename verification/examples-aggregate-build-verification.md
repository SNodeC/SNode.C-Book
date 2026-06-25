# Companion Examples Aggregate Build Status

This note records the build status for the aggregate companion-example project under `examples/`. It is package evidence, not manuscript prose, and is not intended to appear in the printed book.

## Scope

The current aggregate project is:

```text
examples/CMakeLists.txt
```

It is intended to configure, build, and deploy the compact companion examples and the two MiniGateway final-project examples:

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

The companion examples require the SNode.C `Book` tag commit recorded in `SOURCE-VERSION.md`. That commit contains two SNode.C public header-surface fixes exposed by the companion examples:

1. The concrete EventSource convenience headers, such as `web/http/legacy/in/EventSource.h`, are installed with the HTTP client component.
2. `database/mariadb/MariaDBClient.h` exposes the complete `MariaDBCommandSequence` type needed by the fluent MariaDB command-sequence API.

These are SNode.C fixes, not book-example workarounds. The companion examples intentionally use the public consumer-facing headers they require.

## Last reported aggregate build

The author reported a clean rebuild of the aggregate examples project with parallel make before the later WebSocket echo completion change:

```bash
make clean
make -j26
```

That reported build completed successfully and produced the following targets:

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

## Later WebSocket echo completion

After the reported aggregate build, the WebSocket echo companion example was completed by adding the missing server-side echo subprotocol module and by correcting the subprotocol deployment shape. The current WebSocket echo set now consists of:

```text
HttpUpgrade-Server
HttpUpgrade-Client
WebSocket-Echo-ServerSubprotocol
WebSocket-Echo-ClientSubprotocol
```

The current aggregate target set therefore additionally includes:

```text
websocket-echo-server-subprotocol
```

The earlier compile/link result does not cover this later WebSocket completion change.

## Current status

- MiniGateway Step 8 build/run smoke status is recorded separately in `verification/minigateway-step8-author-verification.md`.
- The aggregate examples project has a reported successful build for the pre-WebSocket-completion target set.
- The current aggregate examples project should be rebuilt and redeployed once more before final release, because the WebSocket echo server subprotocol was added after the last reported aggregate build.
- The SNode.C source pin in `SOURCE-VERSION.md` points to the `Book` tag commit containing the required public-header fixes listed above.

Recommended final local check:

```bash
cd examples
find . -type f \( -name '*.cpp' -o -name '*.h' -o -name '*.hpp' -o -name 'CMakeLists.txt' \) -exec touch {} +
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec -DCMAKE_INSTALL_PREFIX=/path/to/deploy-prefix
cmake --build build --target all-examples -j26
cmake --build build --target deploy-examples
```
