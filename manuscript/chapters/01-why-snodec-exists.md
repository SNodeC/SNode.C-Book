## Why SNode.C Exists {#why-snodec-exists}

\index{SNode.C}
\index{event-driven network applications}
\index{layered architecture}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain why protocol behavior and shared application state need different owners.
- **O2.** Trace buffer ownership and the read/write progression in two echo implementations.
- **O3.** Decide whether SNode.C fits a service given platform, runtime, and integration constraints.
:::

### A framework that teaches systems

\index{SNode.C!teaching context}
\index{systems thinking}
\index{network frameworks}


Many networking frameworks make the first connection convenient. That matters when a developer wants to start a server or move data without studying the whole architecture.

Convenience has a cost when it hides the communication model. One endpoint becomes several, TLS is added, configuration becomes operationally important, and deployment matters. The reader needs to understand how those concerns fit together.

SNode.C is interesting because it takes a different path. It is a layered, event-driven C++ framework that keeps the structure of networked applications visible without reducing networking to socket helpers, HTTP handlers, or MQTT utilities.


> By the end of the book, you should be able to build servers and clients with SNode.C, understand why its architecture has the shape it has, and extend that architecture without breaking its conceptual boundaries.

Consider a measurement that first arrives through a local socket and is later also accepted from MQTT. If each input callback assigns the sequence number, the application has two places that decide its ordering. If both callbacks hand a parsed value to one model, that decision has one owner. MiniGateway will make this example concrete. The point of the early layer vocabulary is to prepare the reader to recognize such a decision in code, including the cost of keeping several roles around one shared model.


\index{multi-protocol applications}
\index{M2M communication}
\index{IoT}


A common problem is **collapse of layers**. A small program begins with a socket; parsing, configuration, retries, and logging collect in the same class. It works, but its structure becomes hard to explain.

Another is **one-protocol tunnel vision**: treating every concern as an HTTP route, a string over a socket, or an MQTT message. Each entry point is useful, but the application needs places for concerns that outlive one conversation.


SNode.C separates network family, transport, connection handling, and application protocol. Its contexts, factories, and instances make those choices explicit. HTTP, TLS, WebSocket, and MQTT build on that recurring structure.

This gives the reader transfer: IPv4, IPv6, Unix-domain sockets, and Bluetooth have different endpoint identities and deployment assumptions, but their architectural questions remain comparable.



For each abstraction, this book explains why it exists, shows its use in a working example, and asks what changes when another family, TLS, or a higher protocol is added. It assumes basic network-layer knowledge and the C++ prerequisites stated in the preface; no prior SNode.C knowledge is needed.


### Where SNode.C fits: two echo servers

SNode.C is not trying to replace every C++ networking approach. It is most useful when an application needs explicit communication roles, layered protocol structure, runtime-visible configuration, diagnostics, and several transport or protocol surfaces within one architectural model.


Direct POSIX sockets give explicit operating-system control. Standalone Asio and Boost.Asio provide asynchronous I/O primitives with broad platform support; focused web frameworks offer a shorter route to an HTTP service. SNode.C supplies a more prescribed combination of protocol layers, endpoint configuration, and diagnostics. The best fit depends on which responsibilities the application wants to assemble itself.

Compare the `Comparison-AsioEcho` companion with Chapter 3's `EchoPair`. Both implement asynchronous TCP byte reflection. This is a comparison of ownership and I/O flow, not a throughput benchmark:

| Decision | EchoPair (SNode.C) | Standalone Asio echo |
|---|---|---|
| Start listening | named `SocketServer` and `listen(...)` | `tcp::acceptor` and `async_accept(...)` |
| Own one peer's behavior | factory creates an `EchoSocketContext` | accept handler creates a shared `Session` |
| Receive bytes | framework calls `onReceivedFromPeer()` | session starts `async_read_some(...)` |
| Return bytes | `sendToPeer(...)` queues output | `async_write(...)` completes the whole chunk |
| Keep buffers alive | send copies bytes into framework-managed output | session buffer survives until write completion |
| Advance operations | `core::SNodeC::start()` | `asio::io_context::run()` |
| Endpoint policy | named configuration and state callbacks | this example parses a port argument and reports errors |

These are **function excerpts**, reflowed from the companion sources; surrounding class declarations are omitted. The left excerpt is `EchoPair/EchoSocketContext.cpp`; the right excerpts are `Comparison-AsioEcho/main.cpp`, both under `companion/examples/`.

```{=latex}
\begingroup
\lstdefinestyle{snodec-excerpt}{style=snodec-cpp,basicstyle=\ttfamily\scriptsize}
\noindent\begin{minipage}[t]{0.48\linewidth}
\textbf{EchoPair: receive callback}
```

```{.cpp style="snodec-excerpt"}
std::size_t
EchoSocketContext::onReceivedFromPeer() {
    char chunk[4096];
    const std::size_t chunkLen =
        readFromPeer(chunk, sizeof(chunk));
    if (chunkLen > 0) {
        log().debug() << "Data to reflect: "
            << std::string(chunk, chunkLen);
        sendToPeer(chunk, chunkLen);
    }
    return chunkLen;
}
```

```{=latex}
\end{minipage}\hfill
\begin{minipage}[t]{0.48\linewidth}
\textbf{Asio: read, write, read again}
```

```{.cpp style="snodec-excerpt"}
void read() {
    socket.async_read_some(asio::buffer(bytes),
        [self = shared_from_this()](
            std::error_code error, std::size_t size) {
            if (!error) { self->write(size); }
        });
}

void write(std::size_t size) {
    asio::async_write(socket,
        asio::buffer(bytes.data(), size),
        [self = shared_from_this()](
            std::error_code error, std::size_t) {
            if (!error) { self->read(); }
        });
}
```

```{=latex}
\end{minipage}\par\medskip\endgroup
```

The Asio session starts another read only after its write finishes, so the buffer cannot be overwritten while a write still uses it. Each completion handler captures shared ownership of the session. On EOF or an error, it schedules no further operation; releasing the last handler destroys the socket. EchoPair delegates connection lifetime and output buffering to the framework while supplying the context callbacks. Neither approach removes the need to reason about ownership.

The complete Asio source is `companion/examples/Comparison-AsioEcho/main.cpp`; the paired solution in `companion/exercises/ch01` builds both servers and sends the same bytes to each. After the environment setup in Chapter 2, run that lab and return to this table. Chapter 3 prints the complete EchoPair implementation. The Asio example deliberately omits TLS, reconnection, and application configuration; those can be built with Asio, but they are additional design work.

There are real costs to choosing SNode.C. Its documented build and deployment target is **Linux**, including OpenWrt; this book does not promise native Windows or macOS support. Its runtime has **one event loop per process**: blocking a callback holds up unrelated connections, and independent event loops require separate processes. Asio lets an application choose how it runs its I/O contexts. SNode.C also has a **small ecosystem** centered on its framework examples and MQTTSuite; plan for more direct source reading and fewer ready-made integrations than in a broad general-purpose ecosystem. These are practical constraints, not adoption statistics.

Asio's [platform and build documentation](https://think-async.com/Asio/asio-1.30.2/doc/asio/using.html) describes its cross-platform, normally header-only use. For a one-off portable TCP client, that narrower dependency may be a better fit. SNode.C becomes useful when several communication surfaces need to share an application model and remain recognizable in configuration and diagnostics.

### Source version used by this book

\index{SNode.C!source baseline}
\index{source baseline}
\index{SNode.C 2.0.0}


SNode.C is an active framework. This book describes the public architecture, component names, public include paths, examples, and package layout as they exist in the SNode.C\textsubscript{\texttt{2.0.0}} baseline used for this edition. When reading a newer repository checkout, some implementation details, component inventories, or example applications may have changed.

### Why “layered” matters here

\index{layered architecture!motivation}
\index{boundary discipline}
\index{protocol boundaries}


Figure \ref{fig:snodec-layer-stack} is the first compact view of that structure: each row names a design question that becomes more concrete in later chapters, from endpoint family up to application role.

![The SNode.C design layers. Upward arrows indicate increasing application specificity, not callback order or exclusive ownership.](assets/figures/pdf/fig-01-layer-stack.pdf){#fig:snodec-layer-stack width=90% latex-placement="tbp"}

The rows distinguish endpoint identity, stream transport, connection lifecycle and security, protocol meaning, and application responsibility. The measurement example shows why these distinctions matter. Moving a local input from a Unix-domain socket to IPv4 changes how a peer is addressed and admitted. It need not change how a parsed measurement enters the shared model. Adding TLS changes connection establishment and security; it does not decide the measurement's acceptance order.

The separation also explains what cannot be reused unchanged. An MQTT input must interpret topics and payloads, while an HTTP route interprets requests. Both can hand a measurement to the same model, and an SSE observer can report its accepted state. A common model does not erase protocol-specific framing, permissions, or failure handling. Each layer owns a different part of the path.

\index{node.js}
\index{event loop!node.js comparison}

Like node.js, SNode.C advances communication through an event loop, but event-driven execution alone does not assign these responsibilities. SNode.C expresses them through C++ types, public include paths, ownership, and build components. Longer type names and explicit component choices are the cost of seeing the structure before execution; addresses and timeouts remain runtime configuration.

The later MQTTSuite broker, integrator, bridge, command-line, and store roles extend this argument to a larger system. The useful question remains the same: when another communication surface is added, which responsibility changes, and which owner should remain shared?

### From the first connection to shared state

\index{roles}
\index{handle}
\index{connection}
\index{context}
\index{factory}


Although the details come later, the recurring SNode.C application shape can already be previewed. The runtime advances the listening or connecting work of an instance; connections receive per-connection contexts through factories; those contexts hold the application protocol behavior.

Chapter 3 makes this pattern executable; Chapter 4 names it more formally.


The echo pair exposes server and client creation, context construction, callback flow, data input and output, runtime startup, and the boundary between framework logic and application logic with very little distraction.


Keep the measurement example from the opening in mind. Adding another input should force a decision about addressing and parsing; it should not quietly create a second authority for measurement ordering. That is the kind of judgment the later chapters will make concrete. First, the framework must be built and its smallest communication path made observable.

::: {.snodec-remember title="What to remember"}
- Separate communication choices from protocol behavior and shared application state.
- A factory supplies per-connection contexts; the runtime advances the connections.
- Linux support, one event loop per process, and a small ecosystem affect the framework choice.
- The echo pair exposes ownership and callback flow before higher protocols add complexity.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** A local socket and MQTT both supply measurements. Explain why assigning sequence numbers in both callbacks creates competing authority.
2. **Review (O2).** Why must Asio finish writing before it reads again? Explain why EchoPair can return from its callback with a stack buffer.
3. **Lab (O2).** After Chapter 2, build and run the paired echo solution. Send the same binary payload, larger than either receive buffer, to both servers. Expect exact byte equality; explain why matching bytes say nothing about message boundaries or throughput.
4. **Lab (O2).** After Chapter 2, build both servers and run the independent-peers lab. Leave one peer idle while another sends bytes; close the idle peer and send again. Expect both replies unchanged.
5. **Design (O3).** Choose between SNode.C and standalone Asio for a Linux multi-protocol gateway and a native Windows TCP utility. Justify each choice using explicit constraints rather than code length.

Public solutions and lab commands: `companion/exercises/ch01/README.md`.
:::
