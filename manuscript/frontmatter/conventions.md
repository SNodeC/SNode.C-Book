## Conventions Used in This Book {.unnumbered}

Code identifiers, paths, component names, command names, and configuration keys are written in monospace, for example `SocketContext`, `net-in-stream-legacy`, `CMakeLists.txt`, and `--help`.

Shell examples assume a POSIX-like shell unless stated otherwise. Commands are intended to show the shape of the workflow. Local installation prefixes, compiler choices, package-manager paths, and service names may differ between systems.

C++ listings are teaching excerpts. Some are complete files from the companion examples; others are shortened to keep attention on the relevant boundary. When a listing is described as abridged or source-derived, it should be read as an explanatory slice, not as a replacement for the full file.

The companion example trees under `companion/examples/` are the checked source of truth for the larger examples. Printed excerpts are selected to explain the relevant boundary; when a complete file matters, read the companion source tree beside the chapter.

The book's electronic source package is maintained in the [SNode.C Book repository](https://github.com/SNodeC/SNode.C-Book). Use the package for this edition: a newer repository checkout may contain a different manuscript and different examples. Chapter 2 establishes the package location used by later commands. The source-baseline manifest records framework file contents, while the listing check compares complete marked examples with their companion files. Run `ci/check-source-alignment.py --framework /path/to/snode.c` from the book directory to check that agreement; it does not execute the programs.

Companion builds check compilation and linking; selected smoke tests exercise paths such as SSE output and the MiniGateway Extended Unix-domain input. The publication build checks the book, figures, index, and package. Framework tests, companion tests, and publication checks cover different work. The native MQTT CONNECT-byte check does not cover MQTT-over-WebSocket, full broker interoperability, or restart behavior. Service- and hardware-dependent exercises require their own environments; compilation alone is not a record of execution. No OpenWrt SDK build or device run is claimed for this edition.

The word role is used deliberately. It usually means the part an object or configured instance plays in the communication architecture: server role, client role, protocol role, context role, or deployment role. It does not imply a separate operating-system process unless the text says so.

The word layer is also used deliberately. A layer is not decoration in the diagrams. It marks a boundary where one kind of responsibility should not silently collapse into another.

An endpoint handle and a flow handle are different objects. The endpoint handle configures a named server or client. A flow handle is the shared controller returned by one explicit `listen(...)` or `connect(...)` call. Several flows can use the same endpoint configuration. Chapters 5, 9, and 20 develop the distinction where it affects lifetime, activation, and recovery.
