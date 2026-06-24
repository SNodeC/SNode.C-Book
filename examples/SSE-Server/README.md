# SSE-Server

Compact server-side Server-Sent Events example used by Chapter 23.

It exposes `/events`, rejects requests that do not accept `text/event-stream`,
sends the event-stream response header, and then writes event records as response
fragments.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build
```
