# Part XII Event-Driven Revision Note

This pass revises Chapter 37 and the MiniGateway source tree so the application reacts to measurement events through the local `MeasurementBus` instead of repeatedly checking the current measurement state.

Changes:

- The SSE route subscribes to `MeasurementBus` and sends an event only when a new measurement is published.
- The previous repeated SSE state check was removed.
- The MiniGateway source contains no `std::mutex`, `std::lock_guard`, or synchronization layer.
- The source contains no periodic measurement scan.
- `/simulate` is used as a small teaching input boundary so the reader can create one measurement event without real hardware.
- The chapter now begins with an overview of the application's purpose and concrete usage.
- Chapter 38 wording was adjusted so it no longer refers to a fixed measurement interval.

The MiniGateway source tree is included under `examples/minigateway`.
