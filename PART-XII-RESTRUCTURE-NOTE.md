# Part XII restructuring note

This package restructures Chapter 37 and Chapter 38 without changing the MiniGateway feature scope.

## Chapter 37

Chapter 37 now follows construction stages rather than a flat file listing:

1. build target,
2. domain model,
3. internal state-change bus,
4. MiniGateway-specific configuration,
5. MQTT integration role,
6. HTTP/SSE role,
7. runtime assembly.

The complete MiniGateway source remains included in the chapter, but each file now appears where its responsibility is introduced.

## Chapter 38

Chapter 38 now follows operational stages:

1. extension rule,
2. MQTT-over-WebSocket carrier variation,
3. persistence boundary,
4. replacing the simulated sensor,
5. bounded SSE observation,
6. generated configuration,
7. testing by boundaries,
8. debugging,
9. deployment,
10. OpenWrt-style constrained deployment,
11. process-split decisions.

The chapter stays aligned with the book-wide structure: stage-based explanation, boundary vocabulary, compact diagrams, and `What to remember` summary.
