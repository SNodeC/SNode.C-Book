## Layers in Practice {#layers-in-practice}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Decode a public type, header and component to locate a layer choice.
- **O2.** Predict what changes and what remains shared when family, connection variant or protocol changes.
- **O3.** Confirm a layer selection through component discovery, linking and an observable reply.
:::

### Reading public types and components {#reading-public-types-and-components}

The echo pair now has identifiable runtime objects: a handle configures an instance, a flow advances an activation, and a context serves a connection. Keep that picture fixed. The next question is what can change beneath the context while its byte-reflection behavior remains the same. Choosing IPv4 instead of a local Unix socket, or TLS instead of non-TLS handling, should lead us to a particular part of the composition rather than to a rewrite of the whole program.

We will follow one proposed change through four views. The C++ type selects the composition, its public header makes that type available to the compiler, the component supplies its installed build requirements, and runtime configuration supplies the endpoint and policy. A successful link confirms agreement among the first three; the running program is still needed to establish the fourth. Keeping those checks separate makes a long type name useful instead of intimidating.

The source tree, public headers, C++ names, and installed components expose related views of a layer choice. Their purposes differ: navigating implementation, including declarations, selecting a type, and linking an external program.

| View | IPv4, stream, non-TLS example |
|---|---|
| source path | `src/net/in/stream/legacy` |
| C++ namespace | `net::in::stream::legacy` |
| public include | `<net/in/stream/legacy/SocketServer.h>` |
| CMake component | `net-in-stream-legacy` |

\index{naming convention}
\index{names as architecture}

```cpp
net::in::stream::legacy::SocketServer
```

```cpp
#include <net/in/stream/legacy/SocketServer.h>
```

The type selects a server or client side; its public header supplies the declaration. Include the highest public type directly named by the source, rather than every lower implementation header.

\index{component names}
\index{public include paths}
\index{names as architecture}

```cpp
net::in::stream::legacy::SocketClient<MyFactory>
```

Read this as network-facing code, IPv4 family, stream transport, non-TLS connection handling, client-side handle, and factory for per-connection contexts. The handle configures the instance; its name records the stack that runtime work will use.

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

Here the family is Bluetooth RFCOMM, connection handling is TLS, and the selected type is a server. The factory still supplies per-connection contexts.

::: {.snodec-rule title="Layer-reading rule"}
Read a SNode.C communication type as a stack description before reading it as an isolated API name.
:::

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

These public type headers share the `net-in-stream-legacy` component. Selecting IPv6 and TLS instead yields `net-in6-stream-tls`; spelling alone supplies neither endpoint configuration nor security policy.

::: {.snodec-note title="Reading habit"}
When a SNode.C name feels long, do not shorten it mentally too early. First ask which decisions it records.
:::

### Layers in practice {#layers-in-practice-network-transport-connection-application}

\index{layer model}
\index{network families}
\index{transport form}
\index{connection handling}
\index{application protocol}
\index{layered architecture}
\index{communication stack}
\index{network layer}
\index{transport layer}
\index{connection layer}
\index{application layer}

Layers describe where a responsibility lives, not just directory names. The practical task is to assign a change to its owning layer, then check the consequences in the others. Names and components locate the owner; they do not settle the whole design decision.

| Layer | Main question | Examples |
|---|---|---|
| Network | Which endpoint family are we using? | IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP |
| Transport | What communication form is assumed? | `stream` |
| Connection | How is the concrete peer relationship handled? | `legacy`, `tls` |
| Application | What protocol behavior runs above the connection? | custom context, HTTP, WebSocket, Express-like routing, MQTT |


The runtime tells us how progress happens: event-loop dispatch, descriptor readiness, timers, queued work, timeouts, signals, and cleanup. The layer stack tells us what kind of communication is progressing. A instance might be an IPv4 legacy client, an IPv6 TLS server, or a Unix-domain HTTP endpoint; all participate in the runtime without becoming the same communication structure.

These names describe SNode.C's decomposition of a program. They are not a renaming of the OSI layers or a claim that Bluetooth L2CAP and IP occupy identical positions in their respective protocol stacks. Compare the endpoint-facing surface offered to a SNode.C stream composition, while retaining the underlying protocol's own semantics for reliability, packet boundaries, security, and deployment.

### The network layer: endpoint identity

\index{network layer}
\index{endpoint identity}


The network layer answers the first concrete communication question:

> Which kind of endpoint identity are we using?

This is where SNode.C chooses among network families.

| Family | Namespace fragment | Typical endpoint identity |
|---|---|---|
| IPv4 | `net::in` | IPv4 address and port |
| IPv6 | `net::in6` | IPv6 address and port |
| Unix domain sockets | `net::un` | local socket path or local socket identity |
| Bluetooth RFCOMM | `net::rc` | Bluetooth device address and RFCOMM channel |
| Bluetooth L2CAP | `net::l2` | Bluetooth device address and L2CAP PSM |

The families retain their own endpoint semantics. IPv4 and IPv6 use network addresses and ports. Unix domain sockets live in a local operating-system namespace. Bluetooth RFCOMM and L2CAP use Bluetooth-specific addressing and deployment assumptions. Binding, connecting, permissions, diagnostics, and operational behavior can differ significantly.

The design point is subtler:

::: {.snodec-note title="Endpoint-semantics note"}
SNode.C reuses the application shape without pretending that endpoint semantics are the same.
:::



A common address interface can be useful when an application chooses endpoint families dynamically and stores them in one collection. Family-specific types make different operations and fields visible to the compiler, but require explicit selection or dispatch when the family itself is a runtime choice. SNode.C's concrete address types favor that visibility. The application must still decide how to represent a user-selected endpoint before it reaches the concrete family API.


Chapter 7 gives address semantics their detailed treatment. A Unix socket path, an IP port, and a Bluetooth channel or PSM remain different endpoint facts even when the context above them is reusable.

Try the smallest family change first. Begin with the IPv4 echo server type and replace the family selection with Unix domain sockets. Keep the stream form, legacy variant and echo factory. The public server header moves from the `net/in` path to `net/un`, and the corresponding component becomes `net-un-stream-legacy`. The context can still reflect the bytes it reads; it does not need to interpret an IP address to implement that behavior.

At this point, predict the observable result of the example. The two family-server builds in the lab use the same source and reflect the same payload. Byte equality supports reuse of the echo context. Assess each endpoint identity separately for its reach, access controls and deployment rules; byte equality answers the protocol question. Those questions belong to the address chapter. Here, the important skill is locating the changed selection and finding the matching header and component without altering protocol code.

### The transport layer: communication form

\index{transport layer}
\index{stream transport}

For the early and central chapters, the important transport form is `stream`. It gives the framework a model for connection-oriented byte communication: establishing a peer relationship, reading and writing byte sequences, observing lifetime, shutting down, applying timeouts, and inserting TLS below the application protocol.

The family selects endpoint identity; transport selects the communication relationship. Combined, these choices appear in `net::in::stream`, `net::in6::stream`, `net::un::stream`, `net::rc::stream`, and `net::l2::stream`. They let a context use a compatible stream surface while addressing and deployment remain family-specific. Choosing that surface does not remove the protocol's responsibility for framing records or interpreting payloads.

For echo, a stream means that a callback consumes available bytes and sends bytes onward. Neither the family name nor the number of send calls defines a record boundary for a future measurement protocol. If one sender writes a measurement in two pieces, the parser must preserve enough state to assemble it. Reusing the stream interface therefore preserves a useful operation shape while leaving message interpretation above it. Ask this question before changing a buffer: is the problem how bytes travel, or what those bytes mean together?

### The connection layer: managing the peer relationship

\index{connection layer}
\index{peer relationship}
\index{TLS!connection layer}




The connection layer manages the concrete peer relationship. `legacy` is the established name for the non-TLS stream variant; it does not mean obsolete. `tls` adds TLS-secured handling to the stream. That distinction is separate from the transport choice: stream describes the communication form, while the connection machinery determines how that relationship is established and maintained.

TLS changes handshakes, certificate material, peer validation, SNI or hostname concerns, timing, failure modes, and diagnostics. The application can often retain its server/client handle shape, instance, factory/context pattern, protocol behavior, event runtime, and network family choice. An unchanged context is a reuse benefit; operating the secured service still requires security policy.

A transport connection, completed handshake, and accepted peer identity are distinct observations. Chapter 15 examines those obligations and their callback timing.

Core variants are `core-socket-stream-legacy` and `core-socket-stream-tls`. Concrete components combine family and variant: `net-in-stream-legacy`, `net-in-stream-tls`, `net-in6-stream-legacy`, `net-in6-stream-tls`, `net-un-stream-legacy`, and `net-un-stream-tls`. Public type headers follow the same structure:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/tls/SocketServer.h>
#include <net/in6/stream/legacy/SocketServer.h>
#include <net/un/stream/legacy/SocketServer.h>
```

Include the public header for the type the source file names, not the whole lower socket stack manually. Bluetooth uses `net-rc-stream-legacy`, `net-rc-stream-tls`, `net-l2-stream-legacy`, and `net-l2-stream-tls` where support and build options make those components available. Read each as family, stream transport, and non-TLS or TLS connection handling; check availability separately from interpreting the name.

Next hold IPv4 and echo fixed while selecting TLS. The server type and include path choose the TLS connection variant, and the installed component must agree. That selection does not provide a certificate, private key or trust decision by itself. An echo function can be unchanged while connection establishment now fails because the security configuration is incomplete. That is the expected consequence of assigning security to a distinct part of the program: the failure can occur before the context has any application bytes to reflect.

This is why a layer decision has two answers. The primary change is the connection variant. Its consequences include setup material, timing and diagnostics. Listing those consequences is not a reason to place certificate handling inside the echo parser. It is a reason to test the new connection contract before using unchanged protocol behavior as evidence that the conversion worked.

### The application layer: protocol behavior

\index{application layer}
\index{protocol behavior}

Above the connection layer, communication receives meaning. A small custom protocol may use a derived `SocketContext`, as the echo pair in Chapter 3 does. Higher framework support includes HTTP, WebSocket, Express-like routing, MQTT, and MQTT over WebSocket. Persistence belongs to the larger application architecture; it is not another communication layer in this stack.

Higher protocols retain the underlying stream connection. A web server supplies web behavior over a selected stream stack. MQTT over WebSocket additionally carries one application protocol through another: the lower connection, HTTP upgrade, WebSocket subprotocol, and MQTT session each have a distinct success condition.

Representative components are `http`, `http-server`, `http-client`, `http-server-express`, `websocket-server`, `websocket-client`, `mqtt`, `mqtt-server`, `mqtt-client`, `mqtt-server-websocket`, and `mqtt-client-websocket`. Express server components also encode network-family and connection-variant choices: `http-server-express-legacy-in`, `-in6`, `-rc`, and `-un`; the corresponding TLS names replace `legacy` with `tls`. Read these as architectural statements rather than memorizing the inventory.

A source file naming an Express IPv4 legacy WebApp uses its public Express header:

```cpp
#include <express/legacy/in/WebApp.h>
```

That header represents a WebApp over HTTP over its stream connection. A source file that also directly names a lower socket client includes that client's public header too.

A missing HTTP response can begin at several boundaries. The client may address the wrong listener; TLS may reject the peer; the HTTP parser may reject the request; or the selected route may never finish its response. The route handler is only one candidate. Trace the observations in that order before changing application logic.

The same habit applies to MQTT over WebSocket. Establishing the lower connection does not establish that the HTTP upgrade selected the intended WebSocket subprotocol, and a successful upgrade does not establish that the MQTT session was accepted. Each layer has its own success condition. Later protocol chapters make those conditions concrete.

Finally keep the lower IPv4 legacy stream selection and replace byte reflection with a line protocol. The context now accumulates partial input, finds complete lines and decides what each line means. Its factory must create that protocol object. The lower server header and component can stay unchanged because they still provide the same kind of connection. A changed application protocol is therefore a different case from the family and TLS changes above: the bytes acquire new meaning even though the lower composition is stable.

Use these three experiments as a reading method. First state the intended behavior in ordinary words. Then name the layer responsible, select its public type and header, and check the installed component. Finally list the obligations that remain unchanged and the consequences that need a runtime observation. This order prevents a plausible-looking include path from becoming the entire argument for a design.

### The build system as confirmation

\index{build system}
\index{component architecture}


Use the first echo pair to check a proposed layer change. Keep the context and factory fixed, then compare the public type header, type alias, and component for these two selections:

| Selection | Public server header | Component |
|---|---|---|
| IPv4, non-TLS stream | `<net/in/stream/legacy/SocketServer.h>` | `net-in-stream-legacy` |
| IPv4, TLS stream | `<net/in/stream/tls/SocketServer.h>` | `net-in-stream-tls` |

After changing the selection, rebuild the consumer and configure the TLS variant with its certificate and trust policy. A successful link establishes build consumption; test the handshake and peer identity separately before comparing the echoed bytes.

This comparison is a design exercise, not a complete TLS conversion recipe. Its expected result is a list of three different obligations: select the C++ type, consume its installed component, and configure its operational behavior. Chapter 15 supplies the security details; Chapter 27 explains the component dependency rules. The echo protocol's byte reflection remains a separate responsibility throughout.

A useful failed-build prediction completes the comparison. If a consumer requests a nonexistent component, CMake cannot construct the intended imported target, so there is no executable yet whose socket behavior could be tested. If the correct component links but the program cannot reach its peer, inspect configuration and runtime evidence next. If the peer is reached but reflected bytes differ, return to the context contract. Each outcome narrows a different part of the path.

The component lab deliberately introduces only the first kind of failure in a temporary copy. Restoring the component then permits the same source to build and reflect bytes. Keep both observations: restoration shows that the build choice agrees with the type, while the reply shows the selected composition can execute the protocol in that local experiment.

### Reuse and cross-layer consequences

\index{network families}
\index{protocol reuse}
\index{layer boundaries}
\index{cross-layer responsibility}

Suppose one context protocol moves from IPv4 to IPv6, Unix sockets, RFCOMM, or L2CAP. Address syntax, binding and connection semantics, permissions, required equipment, deployment, configuration, and diagnostics may change. The runtime, instance, factory/context pattern, and broad connection lifecycle remain recognizable. Transfer means separating those changes from the reusable behavior, not declaring network families interchangeable.

RFCOMM and L2CAP exercise this same model near devices. IoT and machine-to-machine systems may combine device communication, network transport, web interfaces, message integration, and deployment constraints. Treat Bluetooth as a network family with concrete discovery, pairing, permissions, and hardware requirements, rather than as an exception to the architecture.

Two mistakes obscure this model: collapsing all communication into one responsibility, and imagining perfectly sealed layers. TLS changes timing and configuration; protocol buffering affects backpressure; moving to a Unix path changes security assumptions. Layers isolate concerns enough to reason locally while preserving those cross-layer consequences.

For a measurement gateway, identify both the primary owner and the downstream effect of each change. A new endpoint family changes how input arrives; its context parses records. The accepted model owns ordering across inputs. HTTP or SSE can observe that state without becoming its authority. An observer subscription is another resource: remove it before destroying the object captured by its callback. The next chapter's model checkpoint makes that lifetime obligation observable alongside event-runtime reasoning.

The next step is to follow that work through the shared event loop.

::: {.snodec-remember title="What to remember"}
- Public types, headers, and components express corresponding layer choices.
- The runtime advances communication; the layers identify the communication being advanced.
- A network-family change can reuse protocol behavior while changing addressing, security, and deployment obligations.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Decode `net::rc::stream::tls::SocketServer<MyFactory>`. Give the matching public header and component, then name what the type does not configure.
2. **Review (O1, O2).** Compare IPv4→Unix, legacy→TLS and echo→line protocol. For each change, name the affected type, header and component and what stays unchanged.
3. **Lab (O2, O3).** Build and run the same echo source with IPv4 and Unix server selections only. Expect identical reflected bytes. Identify the changed type/header/component; address semantics are not this experiment’s learning objective.
4. **Lab (O1, O3).** Run the component experiment: a missing component fails configuration, while the matching component configures, links and reflects bytes. Name the layer represented by the missing selection.
5. **Design (O2).** Add Unix measurement input beside IPv4 input. Specify the type, header and component choices and the protocol/model behavior that remains shared. Leave runtime ownership to the preceding chapter’s design.

Public solutions and bounded lab commands: `companion/exercises/ch05/README.md`.
:::
