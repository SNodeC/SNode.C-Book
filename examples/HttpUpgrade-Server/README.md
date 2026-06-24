# HttpUpgrade-Server

Compact server-side HTTP upgrade example used by Chapter 21.

It shows the HTTP/Express boundary only: a route receives an HTTP request and calls
`res->upgrade(...)`. The example links the WebSocket server upgrade factory at
compile/link time so the upgrade selector can resolve the name `websocket`
without relying on a later dynamic module lookup.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build
```
