# Manuscript Structure

**Layered Network Programming with SNode.C**  
**Building Multi-Protocol Applications in Modern C++**

This structure belongs to an architecture-first SNode.C book. The manuscript is not positioned as a general C++ networking survey. Its subject is layered network programming with SNode.C: lower communication families, transport form, connection handling, protocol meaning, configuration, diagnostics, deployment, and application roles.

The manuscript currently contains the planned front matter, all planned chapters, an epilogue, and back matter.

The publisher-facing proposal material now also includes a separate evidence sheet that distinguishes public repository evidence, author-confirmed professional context, and adoption claims that are not yet made.

## Front matter

- Preface — **present**
- How to Read This Book — **present**
- Conventions Used in This Book — **present**
- Author and Framework Note — **present**
- Acknowledgements — **present**

## Part I — Getting Oriented

- 01. Why SNode.C Exists — **present**
- 02. Preparing Your Environment — **present**
- 03. Your First Working Program: The Echo Pair — **present**
- 04. Reading the Codebase with Confidence — **present**

## Part II — The SNode.C Architecture

- 05. The Mental Model of SNode.C — **present**
- 06. Core Runtime and Event Processing — **present**
- 07. Layers in Practice: Network, Transport, Connection, Application — **present**

## Part III — Networking Foundations in SNode.C

- 08. Socket Addresses and Address Semantics — **present**
- 09. Servers, Clients, and Connections — **present**
- 10. IPv4 and IPv6 as the Primary Teaching Path — **present**
- 11. Unix Domain Sockets — **present**
- 12. Bluetooth in SNode.C: RFCOMM and L2CAP — **present**

## Part IV — From Raw Connections to Application Protocols

- 13. Writing `SocketContext` Classes Well — **present**
- 14. Writing `SocketContextFactory` Classes Well — **present**
- 15. Building the Same Protocol over Different Lower Layers — **present**

## Part V — Configuration and Operational Behavior

- 16. Configuration Philosophy in SNode.C — **present**
- 17. Application and Instance Configuration in Detail — **present**
- 18. Logging, Diagnostics, and Runtime Introspection — **present**

## Part VI — Secure and Robust Communication

- 19. TLS Across the Framework — **present**
- 20. Timeouts, Retries, and Failure Modes — **present**

## Part VII — Web Protocols and Web Applications

- 21. The HTTP Layer — **present**
- 22. The Express-Like Framework — **present**
- 23. Server-Sent Events and Real-Time HTTP — **present**
- 24. WebSocket and Protocol Upgrade — **present**

## Part VIII — IoT and Message-Oriented Systems

- 25. MQTT Support in SNode.C — **present**
- 26. MQTT over WebSocket — **present**
- 27. Designing IoT Systems with Multiple Protocols — **present**

## Part IX — Persistence and Full Systems

- 28. Database Support and Application State — **present**
- 29. Learning from the Applications in `src/apps` — **present**
- 30. From Applications to Systems — **present**
- 31. MQTTSuite as a Reference Ecosystem — **present**

## Part X — Building, Porting, and Maintaining

- 32. CMake Components and Linking Strategy — **present**
- 33. Deployment on Linux and OpenWrt — **present**
- 34. Testing, Debugging, and Benchmarking — **present**

## Part XI — Designing with SNode.C

- 35. Architectural Judgment: Choosing the Right Layer and Boundary — **present**
- 36. Extending the Framework Safely — **present**

## Part XII — Building a MiniGateway Application

- 37. Building MiniGateway — **present**
- 38. Extending, Testing, and Deploying MiniGateway — **present**

## Epilogue

- What to Take Away from SNode.C — **present**

## Back matter

- Further Reading — **present**
- Index — **present; infrastructure and curated entries added**

## Example source trees

The protocol and persistence chapters refer to electronic companion examples that are shown in shortened form in the printed manuscript. In this source package, those companion examples are stored as compact source trees:

```text
examples/HttpUpgrade-Server
examples/HttpUpgrade-Client
examples/SSE-Server
examples/SSE-EventSource-Client
examples/WebSocket-Echo-ServerSubprotocol
examples/WebSocket-Echo-ClientSubprotocol
examples/LineProtocol-Server
examples/LineProtocol-Client
examples/MQTT-ClientRole
examples/MariaDB-Minimal
```

The directory `examples/` also has an aggregate `CMakeLists.txt` for configuring, building, and installing/deploying all companion examples together. The aggregate verification note is recorded in `verification/examples-aggregate-build-verification.md`.

The final technical part uses two larger source trees as source-of-truth examples:

```text
examples/MiniGateway-Base
examples/MiniGateway-Extended
```

Chapter 37 uses the base version. Chapter 38 uses the extended version to show how a SNode.C application can be extended without disturbing existing protocol surfaces.
