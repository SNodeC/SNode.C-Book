# Building a MiniGateway Application

The previous parts supplied the pieces: communication families, protocol layers, configuration, diagnostics, persistence, deployment, testing, and system-level vocabulary. This part combines those pieces into one deliberately small application.

MiniGateway is the construction capstone. It shows how web administration, SSE observation, MQTT integration, shared application state, configuration, diagnostics, and deployment thinking become one coherent SNode.C program instead of a loose collection of examples.

Chapter 35 builds MiniGateway around a shared measurement model, a web role, and an MQTT integration role. Chapter 36 then extends that system as MiniGateway Extended by adding a Unix-domain socket input role without disturbing the existing HTTP, SSE, MQTT, or model boundaries.
