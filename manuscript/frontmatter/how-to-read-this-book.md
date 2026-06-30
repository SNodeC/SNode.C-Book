## How to Read This Book {.unnumbered}

The book is organized as a gradual widening of scope.

Parts I and II establish the basic vocabulary: runtime, role, connection, layer, context, factory, configuration, and event processing. These chapters are best read in order. Later chapters rely on their terminology and usually apply it rather than redefining it.

Parts III and IV move from raw communication families to protocol-local behavior. They show how the same design vocabulary appears with IPv4, IPv6, Unix domain sockets, Bluetooth, custom `SocketContext` classes, and context factories.

Parts V and VI explain operational behavior: configuration, diagnostics, TLS, timeouts, retry, reconnect, and failure handling. These chapters are especially useful when an example has to become a service rather than a demonstration.

Parts VII and VIII apply the lower model to web and messaging protocols: HTTP, the Express-like layer, Server-Sent Events, WebSocket, MQTT, and MQTT over WebSocket.

Parts IX and X widen the view to persistence, larger applications, MQTTSuite, components, linking, deployment, and testing. Chapter 32 is the central place for component, public-header, and linking information; protocol chapters only keep the local details that matter for understanding the chapter itself.

Parts XI and XII bring the material together. The MiniGateway chapters first combine the earlier concepts in a guided application that is larger than the introductory examples. The final design chapters then step back from that application and discuss judgment and extension boundaries explicitly.

The book can be read linearly, but it is also useful with the source tree open. When a chapter names a component, public header, example, or source-derived excerpt, treat the source tree as part of the reading experience. The text explains the architecture; the source tree shows where that architecture becomes code.

Different readers may emphasize different routes through the same material. C++ developers and technical system builders can read linearly, or they can first concentrate on Chapters 3--20 to understand the core model before moving into the web, MQTT, persistence, deployment, and MiniGateway chapters.

Teachers and lecturers can treat the book as a course spine: introductory examples, architecture chapters, protocol chapters, system-design chapters, and MiniGateway as an integrating project.

Advanced students benefit from the full progression: echo pair, architecture, network families, contexts and factories, configuration, protocols, systems, and MiniGateway. Makers and prototypers may prefer a practical route through Chapters 1, 3, 5, 7, 16--20, 23--28, 31, 33, and the MiniGateway chapters.

Scientists, domain researchers, and interdisciplinary technical teams may first read the architectural and system-design chapters to understand how sensing, transport, storage, observation, control, and management surfaces fit together, then return to implementation details as needed.
