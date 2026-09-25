## Further Reading {.unnumbered}

```{=latex}
\markboth{FURTHER READING}{FURTHER READING}
```

The book is intentionally focused on SNode.C. The references below give stable background for readers who want to go deeper into the standards, protocols, tools, and systems context that appear throughout the chapters.

### C++ and build systems {.unnumbered}

- ISO/IEC 14882, *Programming Languages — C++*. The language standard is the authoritative reference for C++ itself.
- Bjarne Stroustrup, *The C++ Programming Language*. A broad reference for the language and its design vocabulary.
- Scott Meyers, *Effective Modern C++*. A compact guide to many C++11/14 idioms that remain relevant in framework and application code.
- [CMake build-system documentation](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html), especially the manuals for `cmake-buildsystem(7)`, `cmake-packages(7)`, `cmake(1)`, and `cmake-presets(7)`. These are useful when reading Chapter 27, the installed package exports, and the example build files.
- CMake package configuration examples and the [link-interface reference](https://cmake.org/cmake/help/latest/command/target_link_libraries.html), alongside the documentation for `find_package`, imported targets, `install(EXPORT)`, and generated config files. These are useful background for understanding how a framework becomes consumable outside its own source tree.

### POSIX, Linux, and network programming {.unnumbered}

- POSIX.1, *The Open Group Base Specifications*. This is the standards background for many Unix and POSIX APIs used by Linux-oriented network software.
- W. Richard Stevens, Bill Fenner, and Andrew M. Rudoff, *UNIX Network Programming, Volume 1: The Sockets Networking API*. Still valuable for understanding the socket model beneath higher-level abstractions.
- Michael Kerrisk, *The Linux Programming Interface*. Useful background for Linux system calls, file descriptors, processes, signals, and deployment-oriented behavior.

### TLS and security protocols {.unnumbered}

- [RFC 8446, *The Transport Layer Security (TLS) Protocol Version 1.3*](https://www.rfc-editor.org/rfc/rfc8446.html).
- OpenSSL documentation. Useful when connecting framework-level TLS configuration to the underlying TLS library and certificate material.

### HTTP, Server-Sent Events, and WebSocket {.unnumbered}

- [RFC 9110, *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html).
- [RFC 9112, *HTTP/1.1*](https://www.rfc-editor.org/rfc/rfc9112.html).
- [WHATWG HTML Living Standard, server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html), including the `EventSource` interface. This is protocol background; the compact route in Chapter 19 implements a deliberately narrower Accept policy.
- [RFC 6455, *The WebSocket Protocol*](https://www.rfc-editor.org/rfc/rfc6455.html).

### MQTT and messaging systems {.unnumbered}

- OASIS, [*MQTT Version 3.1.1*](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html). This is the protocol-level-4 reference for the interoperable CONNECT examples.
- OASIS, [*MQTT Version 5.0*](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html). Use it for comparison, not as evidence that the current SNode.C examples implement MQTT 5.
- *MQTT V3.1 Protocol Specification* (International Business Machines Corporation and Eurotech, 2010). Useful historical context for the Stanford-Clark/Nipper design lineage before MQTT moved into OASIS standardization.

### Deployment and embedded Linux {.unnumbered}

- OpenWrt documentation, especially the [SDK guide](https://openwrt.org/docs/guide-developer/toolchain/using_the_sdk), package Makefile, `procd`, UCI, and init-script material. Useful background for package layout, configuration, and deployment on router-class Linux systems.
- [systemd service-unit reference](https://github.com/systemd/systemd/blob/main/man/systemd.service.xml), especially service supervision and restart behavior. Useful when adapting SNode.C applications to service supervision on general-purpose Linux distributions.

### Databases and persistence {.unnumbered}

- MariaDB documentation, especially MariaDB Connector/C and the client-library API documentation. Useful background for applications that move from transient protocol state to durable application state.


### Testing, diagnostics, and runtime inspection {.unnumbered}

- Valgrind documentation and compiler sanitizer documentation for AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer. These tools are useful when moving from example builds to runtime checks.
- `curl`, Mosquitto client tools, `tcpdump`, Wireshark, `strace`, and Linux `perf` documentation. These tools are useful for confirming HTTP/SSE/WebSocket/MQTT behavior, observing network traffic, tracing system calls, and measuring runtime behavior.

### SNode.C project material {.unnumbered}

- The SNode.C repository is the authoritative source for framework development beyond the version discussed in this book. This edition covers the SNode.C 2.0.0 public commit recorded in `source-baseline/SOURCE-VERSION.md` and its content manifest. A framework source reference establishes implementation behavior; a protocol standard establishes the external contract, and the two should be read together.
- The companion source trees under `companion/examples/` are the authoritative sources for the book's compact examples, MiniGateway, and MiniGateway Extended. Public review answers, lab commands, expected observations, and design discussions are in `companion/exercises/`, in the directory for each numbered chapter and `appendix-a/`. The shared README describes prerequisites and equipped labs. Try each exercise before consulting its solution; a local observation does not certify a deployment.

The online tool manuals follow their current releases. Compare their option descriptions with the versions installed for an exercise. Chapter 28 explains how to inspect the OpenWrt feed at main HEAD separately because a feed recipe, an SDK and the framework source have independent version histories.

For the Bluetooth preparation in Chapter 9, consult the BlueZ project's
[`bluetoothctl` manual](https://github.com/bluez/bluez/blob/master/doc/bluetoothctl.rst),
[Adapter API](https://github.com/bluez/bluez/blob/master/doc/org.bluez.Adapter.rst), and
[Device API](https://github.com/bluez/bluez/blob/master/doc/org.bluez.Device.rst). These
cover controller state, discovery, pairing and trust; they do not define the
application protocol implemented by a SNode.C context.

Use the chapter’s public solution beside each experiment; compare its stated observation before consulting a broader reference.
