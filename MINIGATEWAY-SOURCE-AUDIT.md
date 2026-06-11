# MiniGateway source audit

This audit checks the MiniGateway source tree embedded in Chapter 37 against the current SNode.C and MQTTSuite usage shape.

## Scope

The checked MiniGateway scope is intentionally unchanged:

- simulated measurements
- HTTP `/health`
- HTTP `/status`
- SSE `/events`
- native IPv4 MQTT client role
- MQTT session/topic configuration
- role-aware diagnostics

No TLS, persistence, MQTT-over-WebSocket, authentication, web frontend, or real sensor hardware was added.

## Corrections made

1. Replaced the invalid include `<core/socket/stream/Client.h>` with `<core/socket/stream/SocketClient.h>`.
   The SNode.C template helper `core::socket::stream::Client(...)` is defined in `core/socket/stream/SocketClient.h`.

2. Added `<string>` to `Measurement.h`, because the header declares `std::string toPayload(...)` directly.

3. Kept the MQTTSuite-style MQTT client shape:

```text
configured stream client
  -> SocketContextFactory
      -> iot::mqtt::SocketContext
          -> project-specific iot::mqtt::client::Mqtt subclass
```

4. Kept the SNode.C Express/SSE shape:

```text
express::legacy::in::WebApp
  -> app.get(...)
  -> response JSON / SSE fragments
  -> app.listen(...)
  -> core::SNodeC::start()
```

5. Removed the previous `std::mutex` / `std::lock_guard` synchronization from the guided-project sources. MiniGateway is presented as a single SNode.C event-loop application, so the domain state, observer list, and MQTT client registry do not need thread synchronization in this chapter.

## Static checks performed

- All files referenced in Chapter 37 are present in the source archive.
- The chapter source blocks and the downloadable source package contain the same corrected sources.
- The source package no longer contains the invalid `core/socket/stream/Client.h` include.
- The source package contains the required `<string>` include in `Measurement.h`.
- The source package contains no `<mutex>`, `std::mutex`, or `std::lock_guard` usage.

## Important limitation

I could not run a real compile against an installed SNode.C package in this sandbox because SNode.C is not installed here. The audit is therefore a source/API-shape audit against the current GitHub sources and the MQTTSuite usage pattern, plus local consistency checks of the generated files.
