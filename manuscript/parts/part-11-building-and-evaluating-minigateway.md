# Building and Evaluating MiniGateway

The previous parts supplied the pieces: network families, protocol layers, configuration, diagnostics, persistence, deployment, testing, and system-level vocabulary. This part combines those pieces into one deliberately small application.

MiniGateway combines web administration, SSE observation, MQTT integration, and shared application state. The final checkpoint exercises mixed inputs and observer lifetimes before asking which responsibilities need independent operation.

Chapter 28 builds MiniGateway around a shared measurement model, a web role, and an MQTT integration role. Chapter 29 then extends that system as MiniGateway Extended by adding a Unix-domain socket input role without disturbing the existing HTTP, SSE, MQTT, or model boundaries. Chapter 30 then uses the completed system to examine architectural choices and their costs.
