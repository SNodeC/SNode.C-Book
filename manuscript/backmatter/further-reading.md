## Further Reading {.unnumbered}

```{=latex}
\markboth{FURTHER READING}{FURTHER READING}
```

The book is intentionally focused on SNode.C. The references below give stable background for readers who want to go deeper into the standards, protocols, tools, and systems context that appear throughout the chapters.

### C++ and build systems {.unnumbered}

- ISO/IEC 14882, *Programming Languages — C++*. The language standard is the authoritative reference for C++ itself.
- Bjarne Stroustrup, *The C++ Programming Language*. A broad reference for the language and its design vocabulary.
- Scott Meyers, *Effective Modern C++*. A compact guide to many C++11/14 idioms that remain relevant in framework and application code.
- CMake documentation, especially the manuals for `cmake-buildsystem(7)`, `cmake-packages(7)`, `cmake(1)`, and `cmake-presets(7)`. These are useful when reading Chapter 32, the installed package exports, and the example build files.
- CMake package configuration examples and the documentation for `find_package`, imported targets, `install(EXPORT)`, and generated config files. These are useful background for understanding how a framework becomes consumable outside its own source tree.

### POSIX, Linux, and network programming {.unnumbered}

- POSIX.1, *The Open Group Base Specifications*. This is the standards background for many Unix and POSIX APIs used by Linux-oriented network software.
- W. Richard Stevens, Bill Fenner, and Andrew M. Rudoff, *UNIX Network Programming, Volume 1: The Sockets Networking API*. Still valuable for understanding the socket model beneath higher-level abstractions.
- Michael Kerrisk, *The Linux Programming Interface*. Useful background for Linux system calls, file descriptors, processes, signals, and deployment-oriented behavior.

### TLS and security protocols {.unnumbered}

- RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*.
- OpenSSL documentation. Useful when connecting framework-level TLS configuration to the underlying TLS library and certificate material.

### HTTP, Server-Sent Events, and WebSocket {.unnumbered}

- RFC 9110, *HTTP Semantics*.
- RFC 9112, *HTTP/1.1*.
- WHATWG HTML Living Standard, section on server-sent events and the `EventSource` interface.
- RFC 6455, *The WebSocket Protocol*.

### MQTT and messaging systems {.unnumbered}

- OASIS, *MQTT Version 3.1.1*.
- OASIS, *MQTT Version 5.0*.
- *MQTT V3.1 Protocol Specification* (International Business Machines Corporation and Eurotech, 2010). Useful historical context for the Stanford-Clark/Nipper design lineage before MQTT moved into OASIS standardization.

### Deployment and embedded Linux {.unnumbered}

- OpenWrt documentation, especially the build-system, package Makefile, `procd`, UCI, and init-script material. Useful background for package layout, configuration, and deployment on router-class Linux systems.
- systemd documentation, especially unit files, service supervision, logging, and restart behavior. Useful when adapting SNode.C applications to service supervision on general-purpose Linux distributions.

### Databases and persistence {.unnumbered}

- MariaDB documentation, especially MariaDB Connector/C and the client-library API documentation. Useful background for applications that move from transient protocol state to durable application state.


### Testing, diagnostics, and runtime inspection {.unnumbered}

- Valgrind documentation and compiler sanitizer documentation for AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer. These tools are useful when moving from example builds to runtime checks.
- `curl`, Mosquitto client tools, `tcpdump`, Wireshark, `strace`, and Linux `perf` documentation. These tools are useful for confirming HTTP/SSE/WebSocket/MQTT behavior, observing network traffic, tracing system calls, and measuring runtime behavior.

### SNode.C project material {.unnumbered}

- The SNode.C repository is the authoritative source for framework development beyond the version discussed in this book. This edition covers the SNode.C\textsubscript{\texttt{v1.0.2}} baseline.
- The companion source trees under `companion/examples/` are the authoritative sources for the book's compact examples, MiniGateway, and MiniGateway Extended.
