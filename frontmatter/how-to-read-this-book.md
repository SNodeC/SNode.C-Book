## How to Read This Book {.unnumbered}

The book is organized as a gradual widening of scope.

Parts I and II establish the basic vocabulary: runtime, role, connection, layer, context, factory, configuration, and event processing. These chapters are best read in order. Later chapters rely on their terminology and usually apply it rather than redefining it.

Parts III and IV move from raw communication families to protocol-local behavior. They show how the same design vocabulary appears with IPv4, IPv6, Unix domain sockets, Bluetooth, custom `SocketContext` classes, and context factories.

Parts V and VI explain operational behavior: configuration, diagnostics, TLS, timeouts, retry, reconnect, and failure handling. These chapters are especially useful when an example has to become a service rather than a demonstration.

Parts VII and VIII apply the lower model to web and messaging protocols: HTTP, the Express-like layer, Server-Sent Events, WebSocket, MQTT, and MQTT over WebSocket.

Parts IX and X widen the view to persistence, larger applications, MQTTSuite, components, linking, deployment, and testing. Chapter 32 is the central place for component, public-header, and linking information; protocol chapters only keep the local details that matter for understanding the chapter itself.

Parts XI and XII bring the material together. The design chapters discuss judgment and extension boundaries. The MiniGateway chapters then use the earlier concepts in a guided application that is larger than the introductory examples.

The book can be read linearly, but it is also useful with the source tree open. When a chapter names a component, public header, example, or source-derived excerpt, treat the source tree as part of the reading experience. The text explains the architecture; the source tree shows where that architecture becomes code.
