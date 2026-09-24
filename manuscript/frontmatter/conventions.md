## Conventions Used in This Book {.unnumbered}

Code identifiers, paths, component names, command names, and configuration keys are written in monospace, for example `SocketContext`, `net-in-stream-legacy`, `CMakeLists.txt`, and `--help`.

Shell examples assume a POSIX-like shell unless stated otherwise. Commands are intended to show the shape of the workflow. Local installation prefixes, compiler choices, package-manager paths, and service names may differ between systems.

C++ listings are teaching excerpts. Some are complete files from the companion examples; others are shortened to keep attention on the relevant boundary. When a listing is described as abridged or source-derived, it should be read as an explanatory slice, not as a replacement for the full file.

The companion example trees under `companion/examples/` are the checked source of truth for the larger examples. Printed excerpts are selected to explain the relevant boundary; when a complete file matters, read the companion source tree beside the chapter.

The [SNode.C Book repository](https://github.com/SNodeC/SNode.C-Book) contains the electronic source package. The “Edition and source baseline” sidebar in Chapter 2 explains how to select its framework source, check alignment, and distinguish compilation from the different runtime labs. Use that setup before following later build commands.

Role, defined in the glossary below, is a design responsibility in a system, such as a web interface or MQTT uplink. It does not imply a separate operating-system process unless the design says so.

The word layer is also used deliberately. A layer is not decoration in the diagrams. It marks a boundary where one kind of responsibility should not silently collapse into another.

An endpoint handle and a flow handle are different objects. The endpoint handle configures an instance, which may be named or anonymous. A flow handle is the shared controller returned by one explicit `listen(...)` or `connect(...)` call. Several flows can use the same endpoint configuration. Chapters 4, 8 and 16 develop the distinction where it affects lifetime, activation, and recovery.

### Vocabulary for the examples

The same program can be described from the application, configuration, connection and protocol viewpoints. The terms below distinguish those viewpoints. They are a reference for the chapters that develop each idea, not a list to memorize before running the first example. When a sentence says that something survives, stops or changes, first identify which of these objects it describes. Two things drawn beside each other need not share a lifetime.

| Term | Meaning in this book |
|---|---|
| **Endpoint handle** | The C++ object used by application code to configure a server or client, such as `SocketServer`, `SocketClient` or `WebApp`. After its first use in a chapter, **handle** has this meaning unless qualified. An arbitrary C++ object is simply an object. |
| **Instance** | The configuration-and-runtime identity created through an endpoint handle. It supplies the shared configuration and callbacks used by that endpoint's operations. Dropping a local handle is not a definition of when all its runtime work ends. |
| **Named instance** | An instance with a name addressable through configuration, the command line and logs. The name identifies which endpoint's settings an operator is changing; it is not a count of connected peers. |
| **Anonymous instance** | An instance without such a name. Omitting a name does not eliminate the configuration or the objects needed to make progress. |
| **Flow; flow handle** | A flow is one explicit `listen()` or `connect()` activation and its controller. Its flow handle refers to that shared controller. Several flows may use one instance, and automatic retries continue an existing flow. |
| **Connection** | One peer relationship, represented by `SocketConnection`. It has its own lifetime and may outlast the listening flow that accepted it. |
| **Context; factory** | A context (`SocketContext`) handles the protocol on a connection. A factory (`SocketContextFactory`) creates contexts. Sharing a factory does not mean sharing every connection's protocol state. |
| **Network family** | The choice that determines how peers are addressed: IPv4, IPv6, Unix domain, RFCOMM or L2CAP. Its permissions and platform prerequisites remain relevant when protocol code is reused. |
| **Transport form** | The communication form within a network family, such as a stream. A stream supplies ordered bytes; the application protocol must still identify its own messages. |
| **Connection variant** | The choice between legacy and TLS connection handling where supported. It concerns the stream connection, independently of which application protocol interprets its bytes. |
| **Carrier** | In the MQTT chapters only, the native stream or WebSocket path beneath MQTT. This is the book's name for that comparison, not a framework API type. |
| **Role** | A design responsibility in a system, such as a web interface or MQTT uplink. It does not imply a separate process, handle or connection unless the design makes that choice. |
| **Acceptance; accepted state** | Acceptance is the model's authoritative state transition after validation. Accepted state is what the model has adopted; receipt of bytes, a queued write or a notification is a separate event. |

