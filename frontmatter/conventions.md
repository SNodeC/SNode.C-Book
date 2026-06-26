## Conventions Used in This Book {.unnumbered}

Code identifiers, paths, component names, command names, and configuration keys are written in monospace, for example `SocketContext`, `net-in-stream-legacy`, `CMakeLists.txt`, and `--help`.

Shell examples assume a POSIX-like shell unless stated otherwise. Commands are intended to show the shape of the workflow. Local installation prefixes, compiler choices, package-manager paths, and service names may differ between systems.

C++ listings are teaching excerpts. Some are complete files from the companion examples; others are shortened to keep attention on the relevant boundary. When a listing is described as abridged or source-derived, it should be read as an explanatory slice, not as a replacement for the full file.

The companion example trees under `examples/` are the checked source of truth for the larger examples. Printed excerpts are selected to explain the relevant boundary; when a complete file matters, read the companion source tree beside the chapter.

The word role is used deliberately. It usually means the part an object or configured instance plays in the communication architecture: server role, client role, protocol role, context role, or deployment role. It does not imply a separate operating-system process unless the text says so.

The word layer is also used deliberately. A layer is not decoration in the diagrams. It marks a boundary where one kind of responsibility should not silently collapse into another.
