# HttpUpgrade-Client

Compact client-side HTTP upgrade example used by Chapter 21.

The client prepares an HTTP request, names the requested upgrade protocol as
`websocket`, and installs the WebSocket client upgrade factory through the linked
registration path.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build
```
