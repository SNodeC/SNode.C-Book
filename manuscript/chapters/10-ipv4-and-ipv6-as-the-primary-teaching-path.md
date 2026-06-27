## IPv4 and IPv6 as the First Concrete Network Families

\index{IPv4}
\index{IPv6}
\index{network families}


### Why IPv4 and IPv6 come first

Chapter 9 separated the server/client handle, the registered instance, the concrete `SocketConnection`, the context factory, and the per-connection context.

This chapter keeps that model intact and changes only the first concrete lower-family choice:

```text
IPv4 and IPv6
```

IPv4 and IPv6 form the first concrete comparison pair in this book because they are familiar enough to keep the application shape recognizable, but different enough to make the lower-family boundary visible.

Most readers already have some intuition for hosts, addresses, ports, listening servers, and remote peers. That makes IPv4 and IPv6 a good place to begin the concrete family discussion. At the same time, IPv4 and IPv6 are not the same family. Their namespaces, address classes, textual address forms, wildcard forms, and deployment questions differ. SNode.C makes that difference explicit instead of hiding it behind one overloaded network type.

IPv4 and IPv6 are therefore not chosen because Unix domain sockets or Bluetooth are secondary. They are chosen because they provide a controlled first variation:

```text
same handle / instance / connection model
same factory / context / runtime model
different lower-family semantics
```

That controlled variation is the main teaching value of this chapter. The reader can see what changes when the lower family changes, and just as importantly, what does not change.

### What stays shared across IPv4 and IPv6

\index{IPv4!shared model}
\index{IPv6!shared model}
\index{server/client/context model}


For both IPv4 and IPv6, the outer application shape remains recognizable.

A typical stream application still involves:

- an application-side `SocketServer` or `SocketClient` handle,
- a registered server-side or client-side instance after `listen(...)` or `connect(...)`,
- a `SocketContextFactory`,
- a per-connection `SocketContext`,
- a status callback for `listen(...)` or `connect(...)`,
- connection lifecycle callbacks if the application uses them,
- and a runtime started through `core::SNodeC::start()`.

Nothing about moving from IPv4 to IPv6 changes that architectural shape.

The first major observation is:

::: {.snodec-rule title="Family-independent pattern"}
The handle / instance / connection / factory / context / runtime pattern is more fundamental than the specific IP family.
:::

IPv4 and IPv6 show this without changing endpoint identity as radically as Unix domain sockets or Bluetooth do. Both IP families still use the familiar host-plus-port idea. That makes the comparison focused: the lower family changes, but the application architecture does not collapse into a different model.

#### Same server/client/context shape

The server/client distinction from Chapter 9 remains stable.

An IPv4 server handle and an IPv6 server handle are both handles used to configure and register server-side instances.

An IPv4 client handle and an IPv6 client handle are both handles used to configure and register client-side instances.

After registration, the instance remains the runtime-visible role. The connection remains the concrete peer relationship. The context remains the application protocol endpoint attached to that connection.

So the first teaching comparison is not:

```text
IPv4 code versus completely different IPv6 code
```

It is:

```text
one SNode.C communication model
  -> specialized through IPv4
  -> specialized through IPv6
```

That is the model to keep in mind while reading the examples. The lower namespace changes, the address family changes, and deployment assumptions may change. The server/client/connection/context pattern remains structurally the same.

#### Parallel type names

\index{net::in@\texttt{net::in}}
\index{net::in6@\texttt{net::in6}}
\index{type naming}


The type names show the parallelism immediately.

For IPv4, a minimal legacy stream pair often begins like this:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;
```

For IPv6, the corresponding pair is:

```cpp
using EchoServer6 = net::in6::stream::legacy::SocketServer<MyFactory>;
using EchoClient6 = net::in6::stream::legacy::SocketClient<MyFactory>;
```

The first visible difference is the network-family namespace:

```text
net::in   -> IPv4
net::in6  -> IPv6
```

The rest of the layered name remains recognizably stable:

```text
stream
  -> legacy
      -> SocketServer / SocketClient
          -> MyFactory
```

This is the kind of layered reading introduced in Chapter 7. A long SNode.C type name says which lower family is used, which transport form is used, which connection variant is selected, which handle type is visible, and which factory creates the per-connection protocol contexts.

The IPv4/IPv6 comparison is therefore visible before a single socket operation is called. The type name already tells the reader which lower family has been selected.

#### Parallel address classes

\index{net::in::SocketAddress@\texttt{net::in::SocketAddress}}
\index{net::in6::SocketAddress@\texttt{net::in6::SocketAddress}}


Chapter 8 introduced address semantics. That model now applies directly to the two IP families.

| Family | Address class | Basic endpoint shape |
|---|---|---|
| IPv4 | `net::in::SocketAddress` | host plus port |
| IPv6 | `net::in6::SocketAddress` | host plus port |

The class names differ because the endpoint families differ. The basic shape is similar because both families use a host-plus-port model.

That is the right balance. One address pattern transfers across both IP families, but the similarity should not be exaggerated. IPv4 and IPv6 have different textual forms, different wildcard forms, and different deployment questions.

The useful lesson is:

::: {.snodec-note title="Parallel-shape note"}
The API shape is intentionally parallel where that helps, but the endpoint families remain distinct.
:::

Here “host” should be read broadly. It may be a numeric address such as `127.0.0.1` or `::1`, or it may be a name that has to be resolved. The convenience API makes the common case readable, but Chapter 8’s address model still matters underneath.

#### Parallel convenience overloads

The stream wrappers make the shared model especially visible.

The IPv4 and IPv6 server wrappers provide parallel `listen(...)` convenience overloads. These overloads set local configuration such as host, port, and backlog, then delegate to the general `listen(onStatus)` path.

Likewise, the IPv4 and IPv6 client wrappers provide parallel `connect(...)` convenience overloads. These overloads set the remote host and port, optionally set local bind information, and then delegate to the general `connect(onStatus)` path.

So the convenience API is not a separate communication model. It configures the handle and then enters the same registration path that Chapter 9 described.

The pattern can be summarized like this:

| Surface call expresses | Configuration effect |
|---|---|
| `listen(port, ...)` | local port |
| `listen(port, backlog, ...)` | local port + backlog |
| `listen(host, port, ...)` | local host + local port |
| `listen(host, port, backlog, ...)` | local host + local port + backlog |
| `connect(host, port, ...)` | remote host + remote port |
| `connect(host, port, bindHost, ...)` | remote endpoint + local host |
| `connect(host, port, bindPort, ...)` | remote endpoint + local port |
| `connect(host, port, bindHost, bindPort, ...)` | remote endpoint + full local bind endpoint |

The exact overload count is less important than the pattern.

The architectural idea is:

> Easy-looking calls set configuration and then use the same underlying registration and flow machinery.

This is important for understanding SNode.C code. A short `listen(8080, ...)` call is not a different runtime concept from constructing a `SocketAddress` and calling the more general path. It is a convenience surface over the same role configuration and registration model.

### What remains stable

Moving from IPv4 to IPv6 should not feel like changing the application architecture. The stable core remains the same.

| Aspect | IPv4 | IPv6 | Architectural point |
|---|---|---|---|
| Application-side handle | `SocketServer` / `SocketClient` | `SocketServer` / `SocketClient` | handle shape stays |
| Registered instance | server-side or client-side role | server-side or client-side role | role model stays |
| Connection object | `SocketConnection` | `SocketConnection` | concrete peer relationship stays |
| Context factory | same pattern | same pattern | context creation transfers |
| Protocol context | same class often possible | same class often possible | protocol logic can transfer |
| Runtime | same event-driven model | same event-driven model | runtime understanding transfers |
| Status callback | `SocketAddress`, `State` | `SocketAddress`, `State` | outer role status model stays |
| Lifecycle callbacks | connection callbacks | connection callbacks | connection lifecycle model stays |

This is the main transfer point.

If the application protocol is written in a `SocketContext`, it does not automatically become an “IPv4 protocol” or an “IPv6 protocol.” It is application behavior carried over a lower family. The same context class can often be reused when the protocol behavior does not inspect or depend on family-specific address details.

The lower family changes, and with it the endpoint representation, bind/connect configuration, and deployment environment.

What often remains stable is the protocol class, the factory structure, the connection lifecycle, the runtime, and the overall server/client model.

#### Runtime and instance model

The runtime is not replaced when the network family changes.

An IPv4 server and an IPv6 server still participate in the same kind of event-driven runtime. They still register communication intent through `listen(...)`. They still produce connection objects. They still attach contexts through factories.

The same applies on the client side. An IPv4 client and an IPv6 client both register connection intent through `connect(...)`, enter the runtime machinery, and produce concrete connection episodes when the connection succeeds.

IPv4 and IPv6 therefore show that the runtime and instance model are not tied to one address family. The event loop does not become an “IPv4 event loop” or an “IPv6 event loop.” The lower family affects the physical and address layer. The runtime architecture remains the same.

#### Factory, context, and protocol logic

The factory/context pattern also transfers.

A simple echo protocol implemented as a `SocketContext` can often be used with both IPv4 and IPv6 roles. The context does not need to care whether the peer endpoint was represented by an IPv4 or IPv6 address unless the protocol itself inspects, prints, filters, or interprets that address.

This separation keeps protocol logic from being unnecessarily tied to one lower family.

The factory carries the rule for creating the context. The context carries the protocol behavior. The selected IP family supplies the endpoint family and the lower communication path. Keeping those responsibilities separate is what makes the IPv4/IPv6 comparison useful instead of duplicating the whole application.

#### Status and lifecycle callbacks

Chapter 9 distinguished status callbacks from connection lifecycle callbacks. That distinction still applies here.

A `listen(...)` or `connect(...)` status callback reports outer role status. It sees the relevant address object and a `core::socket::State` value.

Connection lifecycle callbacks observe connections. They receive a `SocketConnection*` and can inspect local and remote addresses, timing, metrics, and connection names.

Context callbacks implement protocol behavior.

Moving from IPv4 to IPv6 does not collapse those callback layers. The lower-family namespace changes, but the callback model remains the same.

### What changes

\index{address family}
\index{wildcard form}


The stable structure does not mean IPv4 and IPv6 are identical. They are not.

The goal is not to turn this into a full IPv6 chapter, but to show where SNode.C keeps the architecture stable and where the lower family still matters.

#### Namespace and address family

The most visible code change is the namespace:

```text
net::in
  -> IPv4

net::in6
  -> IPv6
```

This is not cosmetic. It tells the reader that the lower family has changed.

The address class changes too:

```cpp
net::in::SocketAddress
net::in6::SocketAddress
```

Both are host-plus-port address classes, but they belong to different endpoint families. That distinction becomes important in examples, diagnostics, wildcard binding, and deployment.

The namespace is therefore a compact architectural statement:

```text
same stream model
same legacy/TLS layer choice
same server/client handle pattern
different internet family
```

#### Textual address form and wildcard form

The textual address form changes.

IPv4 examples often use addresses such as:

```text
127.0.0.1
0.0.0.0
```

IPv6 examples often use addresses such as:

```text
::1
::
```

The wildcard form also changes:

| Family | Wildcard host | Wildcard port |
|---|---|---|
| IPv4 | `0.0.0.0` | `0` |
| IPv6 | `::` | `0` |

Chapter 8 already explained address semantics in detail. Here the important point is simply that the wildcard idea transfers, but its concrete family representation changes.

The reader should not think:

```text
IPv6 is just IPv4 with longer text.
```

IPv6 has its own address family and its own operational questions, even though the SNode.C API is intentionally parallel.

#### Local and remote configuration

The convenience overloads also make local and remote roles visible.

For a server, the most important early configuration is local:

```text
local host
local port
backlog
```

For a client, the most important early configuration is remote:

```text
remote host
remote port
```

and, optionally:

```text
local bind host
local bind port
```

This directly continues Chapter 8 and Chapter 9.

Chapter 8 explained what endpoint identity means. Chapter 9 explained how servers and clients use endpoint identity. Chapter 10 shows that IPv4 and IPv6 use the same local/remote role distinction with different address-family semantics.

#### IPv6-only, IPv4-mapped, and dual-stack thinking

\index{IPv6!IPv6-only}
\index{IPv6!IPv4-mapped addresses}
\index{dual-stack deployment}


IPv6 introduces one additional technical point: deployment can involve IPv6-only behavior, IPv4-mapped IPv6 addresses, or platform-specific dual-stack behavior.

This topic should not overwhelm the first example. It should also not be hidden.

At this stage, do not try to master every platform switch. Notice instead that IPv6 is a separate endpoint family with deployment semantics of its own.

An IPv6 endpoint is not only a different address string. It may also raise configuration and platform questions about whether IPv4 traffic is included, excluded, or represented through IPv4-mapped IPv6 addresses.

That is one reason SNode.C keeps IPv6 as its own family instead of treating it as an overloaded IPv4 mode.

### From IPv4 to IPv6

The move from IPv4 to IPv6 should make transfer visible without overwhelming the reader.

The useful reading path is simple. First, look at a minimal IPv4 legacy pair. Then look at the corresponding IPv6 legacy pair. Then compare what changed in code and what stayed stable in architecture. Later chapters can repeat the same comparison under TLS.

This keeps the lower-family comparison sharp. It also prepares the next variations: after IPv4 and IPv6, Unix domain sockets and Bluetooth can be introduced as more different endpoint families while the server/client/connection model remains familiar.

#### Start with IPv4

IPv4 remains the easiest first concrete example for many readers. That is not because it is more important. It is because its notation and everyday expectations are familiar.

A minimal IPv4 server may look like this in outline:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;

EchoServer4 server("echo4");
server.listen(8080, 5, onStatus);
```

The matching client may look like this:

```cpp
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;

EchoClient4 client("echo4");
client.connect("127.0.0.1", 8080, onStatus);
```

The numeric loopback address keeps the family comparison explicit. A host name may also be used where name resolution is desired, but `127.0.0.1` makes it clear that this first example is deliberately IPv4.

This path shows host plus port, server plus client, status callback, and runtime integration before IPv6 notation or dual-stack questions enter the picture.

#### Move immediately to IPv6

IPv6 should follow soon after the first stable IPv4 picture.

If IPv6 appears only much later, IPv4 can start to look like the normal case and IPv6 like an advanced appendix. That would be the wrong lesson for SNode.C.

The IPv6 version should feel deliberately close:

```cpp
using EchoServer6 = net::in6::stream::legacy::SocketServer<MyFactory>;

EchoServer6 server("echo6");
server.listen(8080, 5, onStatus);
```

and:

```cpp
using EchoClient6 = net::in6::stream::legacy::SocketClient<MyFactory>;

EchoClient6 client("echo6");
client.connect("::1", 8080, onStatus);
```

The important comparison is:

```text
net::in   -> net::in6
127.0.0.1 -> ::1
```

The outer structure remains stable. The lower family and address notation change.

#### Compare what changed and what did not

Once the IPv4 and IPv6 examples are side by side, the comparison becomes clear. What changed?

- the network-family namespace,
- the address class,
- address text,
- wildcard representation,
- possible IPv6-specific deployment questions.

What did not change?

- application-side server and client handle shape,
- registered instance model,
- connection model,
- context factory,
- context class shape,
- runtime startup,
- status callback model,
- connection lifecycle model,
- layered reading of the type name.

This comparison is the core result. The point is controlled variation across lower families, with IPv4 and IPv6 as the teaching path.

### Stable model, different family semantics

The following table is the transfer map for the chapter. It shows which ideas stay stable and which ones move with the lower family.

| Aspect | IPv4 | IPv6 | Teaching point |
|---|---|---|---|
| Namespace | `net::in` | `net::in6` | lower family changes |
| Address class | `net::in::SocketAddress` | `net::in6::SocketAddress` | family-specific endpoint identity |
| Address shape | host + port | host + port | interface is parallel |
| Wildcard host | `0.0.0.0` | `::` | representation differs |
| Application-side handle | `SocketServer` / `SocketClient` | `SocketServer` / `SocketClient` | handle shape stays |
| Registered instance | server/client role | server/client role | role model stays |
| Connection | `SocketConnection` | `SocketConnection` | peer relationship model stays |
| Protocol context | same class often possible | same class often possible | protocol logic can transfer |
| Convenience API | sets config, delegates | sets config, delegates | easy API and configured API are one model |
| Extra concern | simpler first case | IPv6-only / IPv4-mapped / dual-stack questions | deployment semantics differ |

This table connects directly to Chapters 8 and 9. Chapter 8 explains the address rows. Chapter 9 explains the handle, instance, connection, factory, context, and callback rows.

This chapter shows IPv4 and IPv6 as the first concrete comparison pair.

::: {.snodec-remember title="What to remember"}
- IPv4 and IPv6 are the first concrete lower-family comparison because they are familiar, parallel, and still meaningfully different.
- `net::in` selects IPv4; `net::in6` selects IPv6.
- Both families use host-plus-port endpoint identity, but their textual forms, wildcard forms, and deployment questions differ.
- The server/client handle, registered instance, connection, factory, context, and runtime model stay structurally the same.
- Convenience `listen(...)` and `connect(...)` overloads set configuration and then delegate to the general registration path.
- Protocol contexts can often be reused across IPv4 and IPv6 when the protocol itself does not depend on address-family details.
:::

### Public surface of the primary families

\index{public headers}
\index{net::in::stream::legacy@\texttt{net::in::stream::legacy}}
\index{net::in6::stream::legacy@\texttt{net::in6::stream::legacy}}


IPv4 and IPv6 are the simplest place to see the source/build pairing. A file that directly names an IPv4 legacy stream role uses the IPv4 public role headers:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

with the matching component:

```text
net-in-stream-legacy
```

The IPv6 variant changes only the family fragment:

```cpp
#include <net/in6/stream/legacy/SocketServer.h>
#include <net/in6/stream/legacy/SocketClient.h>
```

with the corresponding component:

```text
net-in6-stream-legacy
```

The local point is the family selection. Chapter 32 gives the consolidated include/component matrix.

### Closing perspective

IPv4 and IPv6 keep the familiar host-plus-port view while introducing the lower-family distinction that later chapters vary. Unix-domain sockets are the next controlled change: the role model remains stable, but endpoint identity becomes local and path-based.

