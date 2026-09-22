## How to Read This Book {.unnumbered}

The book is organized as a gradual widening of scope.

Parts I and II establish the basic vocabulary: runtime, role, connection, layer, context, factory, configuration, and event processing. These chapters are best read in order. Later chapters rely on their terminology and usually apply it rather than redefining it.

Parts III and IV move from raw communication families to protocol-local behavior. They show how the same design vocabulary appears with IPv4, IPv6, Unix domain sockets, Bluetooth, custom `SocketContext` classes, and context factories.

Parts V and VI explain operational behavior: configuration, diagnostics, TLS, timeouts, retry, reconnect, and failure handling. These chapters are especially useful when an example has to become a service rather than a demonstration.

Parts VII and VIII apply the lower model to web and messaging protocols: HTTP, the Express-like layer, Server-Sent Events, WebSocket, MQTT, and MQTT over WebSocket.

Parts IX and X widen the view to persistence, larger applications, MQTTSuite, components, linking, deployment, and testing. Chapter 25 is the central place for component, public-header, and linking information; protocol chapters only keep the local details that matter for understanding the chapter itself.

Part XI brings the material together. The MiniGateway chapters first combine the earlier concepts in a guided application that is larger than the introductory examples. The final design chapter steps back from that application and discusses judgment explicitly. Appendix A follows the epilogue as an optional path into source navigation and framework extension.

The book can be read linearly, but it is also useful with the source tree open. When a chapter names a component, public header, example, or source-derived excerpt, treat the source tree as part of the reading experience. The text explains the architecture; the source tree shows where that architecture becomes code.

The opening chapters use a more direct tutorial voice because they prepare the reader to build and read the first complete programs. Later chapters become more architectural and reference-oriented: they assume the vocabulary is available and use it to classify protocols, roles, configuration surfaces, deployment choices, and extension points.

Alternative routes are most useful when they have a concrete destination:

- To build an external application, begin with Chapters 1–5 and the echo pair. Follow Chapters 6–15 as the application acquires addressing, protocol state, configuration, and recovery policy. The checkpoint is a program whose build dependencies and connection lifetimes you can explain, not merely one that connects successfully.
- To build a web-and-MQTT gateway, keep the same foundation, then read Chapters 16–23 before MiniGateway in Chapters 28 and 29. Chapters 24, 25, 26, 27 and 30 supply the process, build, operational, testing, and design decisions needed to take that example further. This route suits a practical prototype, but it still depends on the earlier ownership and configuration model.
- To maintain or extend the framework, use Appendix A's source-reading workflow, read Chapters 4–15 closely, and follow the protocol chapters relevant to the change. Chapters 24, 25 and 27 and Appendix A connect the source tree, public components, tests, and extension boundary. The checkpoint is an explanation of who else consumes the behavior you plan to change.

For a course, the linear sequence supplies the common vocabulary and MiniGateway supplies the integrating project. A researcher or technical collaborator interested first in system shape can begin with Chapters 22, 24 and 30, then return to the implementation chapters for each chosen role. Those chapters support design discussion; they do not replace the practical prerequisites for implementing the result.

For a first practical milestone, complete the echo pair and explain which object owns its protocol behavior. For the web milestone, build the SSE companions and observe an event with a separate client. For the integration milestone, follow a measurement from MiniGateway input through the model to HTTP and SSE observation. The intervening architectural chapters give names to the decisions those exercises expose. Reading a table of roles is useful; being able to locate those roles in a running example is the stronger check of understanding.
