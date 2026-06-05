## IPv4 and IPv6 as the First Concrete Network Families

### Why IPv4 and IPv6 come first

Chapter 9 separated the general roles:

- server,
- client,
- connection,
- context factory,
- and context.

This chapter now applies those roles to the first concrete lower-family pair:

```text
IPv4 and IPv6
```

SNode.C supports more than one lower communication family. That is one of its strengths.

IPv4 and IPv6 are a useful first pair because they are familiar enough that most readers already understand the broad ideas of hosts, addresses, ports, listening servers, and remote peers. At the same time, they are different enough to show why SNode.C treats the lower communication family as an explicit architectural choice.

IPv4 and IPv6 are therefore not chosen because Unix domain sockets or Bluetooth are secondary.

They provide a clear first controlled variation:

```text
same server/client/connection model
same factory/context/runtime model
different lower-family semantics
```

This makes them the first concrete specialization of the Part III model.

### The shared IPv4/IPv6 pattern

For both IPv4 and IPv6, the outer application shape stays the same.

A typical stream application still has:

- a `SocketServer` or `SocketClient` instance,
- a `SocketContextFactory`,
- a `SocketContext`,
- a status callback for `listen(...)` or `connect(...)`,
- connection lifecycle callbacks if needed,
- and a runtime started through `core::SNodeC::start()`.

Nothing about moving from IPv4 to IPv6 changes that basic shape.

The first major observation is:

> The instance/factory/context/runtime pattern is more fundamental than the specific IP family.

IPv4 and IPv6 show this without changing endpoint identity as radically as Unix domain sockets or Bluetooth do.

#### Same server/client/context shape

The server/client distinction from Chapter 9 remains stable.

An IPv4 server role and an IPv6 server role are both server roles.

An IPv4 client role and an IPv6 client role are both client roles.

The connection remains the concrete peer relationship.

The context remains the application protocol endpoint attached to that connection.

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

That is the model to keep in mind.

#### Parallel type names

The type names show the parallelism immediately.

For IPv4, a minimal legacy stream pair often begins like this:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;
```

For IPv6, the parallel pair is:

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

This is the kind of layered comparison introduced in Chapter 7.

#### Parallel address classes

Chapter 8 introduced address semantics.

That model now applies directly to the two IP families.

| Family | Address class | Basic endpoint shape |
|---|---|---|
| IPv4 | `net::in::SocketAddress` | host plus port |
| IPv6 | `net::in6::SocketAddress` | host plus port |

The class names differ because the endpoint families differ.

The basic shape is similar because both families use a host-plus-port model.

One address pattern transfers across both IP families.

But the similarity should not be exaggerated. IPv4 and IPv6 have different textual forms, different wildcard forms, and different deployment questions.

The right lesson is:

> The API shape is intentionally parallel where that helps, but the endpoint families remain distinct.

#### Parallel convenience overloads

The stream wrappers make the shared model especially visible.

The IPv4 and IPv6 server wrappers provide parallel `listen(...)` convenience overloads. These overloads set local configuration such as host, port, and backlog, then delegate to the general `listen(onStatus)` path.

Likewise, the IPv4 and IPv6 client wrappers provide parallel `connect(...)` convenience overloads. These overloads set remote host and port, optionally set local bind information, then delegate to the general `connect(onStatus)` path.

So the convenience API is not a separate communication model.

It is a readable front door into the same instance-configuration model.

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

It shows the architectural idea:

> Easy-looking calls set configuration and then use the same underlying role machinery.

### What remains stable

Moving from IPv4 to IPv6 should not feel like changing the application architecture.

The stable core remains the same.

| Aspect | IPv4 | IPv6 | Architectural point |
|---|---|---|---|
| Server role | `SocketServer` | `SocketServer` | role model stays |
| Client role | `SocketClient` | `SocketClient` | role model stays |
| Connection object | `SocketConnection` | `SocketConnection` | concrete peer relationship stays |
| Context factory | same pattern | same pattern | context creation transfers |
| Protocol context | same class can often be used | same class can often be used | protocol logic transfers |
| Runtime | same event-driven model | same event-driven model | runtime understanding transfers |
| Status callback | `SocketAddress`, `State` | `SocketAddress`, `State` | outer role status model stays |
| Lifecycle callbacks | connection callbacks | connection callbacks | connection lifecycle model stays |

This is the main transfer point.

If the application protocol is written in a `SocketContext`, it does not automatically become an "IPv4 protocol" or an "IPv6 protocol." It is application behavior carried over a lower communication family.

What changes is the lower family and therefore the endpoint representation, bind/connect configuration, and deployment environment.

What often remains stable is the protocol class, the factory structure, the connection lifecycle, the runtime, and the overall server/client model.

#### Runtime and role model

The runtime is not replaced when the network family changes.

An IPv4 server and an IPv6 server still participate in the same kind of event-driven runtime. They still register communication intent. They still produce connection objects. They still attach contexts through factories.

IPv4 and IPv6 show that the runtime and role model are not tied to one address family.

#### Factory, context, and protocol logic

The factory/context pattern also transfers.

A simple echo protocol implemented as a `SocketContext` can often be used with both IPv4 and IPv6 roles. The context does not need to care whether the peer endpoint was represented by an IPv4 or IPv6 address unless the application protocol itself inspects or displays that address.

This separation keeps protocol logic from being unnecessarily tied to one lower family.

#### Status and lifecycle callbacks

Chapter 9 distinguished status callbacks from connection lifecycle callbacks.

That distinction still applies here.

A `listen(...)` or `connect(...)` status callback reports outer role status.

Lifecycle callbacks observe concrete connections.

Context callbacks implement protocol behavior.

Moving from IPv4 to IPv6 does not collapse those callback layers. The lower-family namespace changes, but the callback model remains the same.

### What changes

The stable structure does not mean IPv4 and IPv6 are identical.

They are not.

The chapter should teach the difference calmly and precisely.

#### Namespace and address family

The most visible code change is the namespace:

```text
net::in
  -> IPv4

net::in6
  -> IPv6
```

This is not cosmetic. It tells the reader that the lower communication family has changed.

The address class changes too:

```cpp
net::in::SocketAddress
net::in6::SocketAddress
```

Both are host-plus-port address classes, but they belong to different endpoint families.

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

The convenience overloads also make local/remote roles visible.

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

Chapter 8 explained what endpoint identity means.

Chapter 9 explained how servers and clients use endpoint identity.

Chapter 10 shows that IPv4 and IPv6 use the same local/remote role distinction with different address-family semantics.

#### IPv6-only, IPv4-mapped, and dual-stack thinking

IPv6 introduces one additional technical point: deployment can involve IPv6-only behavior, IPv4-mapped IPv6 addresses, or platform-specific dual-stack behavior.

This topic should not overwhelm the first example.

But it should not be hidden either.

The reader should understand that an IPv6 endpoint is not only about writing a different address string. It may also raise configuration and platform questions about whether IPv4 traffic is intentionally included, excluded, or represented through IPv4-mapped IPv6 addresses.

That is one reason SNode.C keeps IPv6 as its own family instead of treating it as an overloaded IPv4 mode.

### From IPv4 to IPv6

The move from IPv4 to IPv6 should make transfer visible without overwhelming the reader.

A useful progression is:

1. show a minimal IPv4 legacy pair,
2. show the corresponding IPv6 legacy pair,
3. point out what changed in code,
4. point out what did not change in architecture,
5. later revisit the same comparison under TLS.

This keeps the lower-family comparison sharp.

It also prepares the next variations: after IPv4 and IPv6, Unix domain sockets and Bluetooth can be introduced as more different endpoint families while the server/client/connection model remains familiar.

#### Start with IPv4

IPv4 remains the easiest first concrete example for many readers.

That is not because it is more important.

It is because its notation and everyday expectations are familiar.

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
client.connect("localhost", 8080, onStatus);
```

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
localhost -> ::1 or another IPv6-capable host name/address
```

The outer structure remains stable.

#### Compare what changed and what did not

Once the IPv4 and IPv6 examples are side by side, the comparison becomes clear.

What changed?

- the network-family namespace,
- the address class,
- address text,
- wildcard representation,
- possible IPv6-specific deployment questions.

What did not change?

- server role,
- client role,
- context factory,
- context class shape,
- runtime startup,
- status callback model,
- connection lifecycle model,
- layered reading of the type name.

This comparison is the core result.

The point is not only IPv4 and IPv6 themselves. The point is controlled variation across lower communication families.

### Stable model, different family semantics

The following table summarizes the chapter.

| Aspect | IPv4 | IPv6 | Teaching point |
|---|---|---|---|
| Namespace | `net::in` | `net::in6` | lower family changes |
| Address class | `net::in::SocketAddress` | `net::in6::SocketAddress` | family-specific endpoint identity |
| Address shape | host + port | host + port | interface is parallel |
| Wildcard host | `0.0.0.0` | `::` | representation differs |
| Server type | `SocketServer` | `SocketServer` | role model stays |
| Client type | `SocketClient` | `SocketClient` | role model stays |
| Protocol context | same class often possible | same class often possible | protocol logic transfers |
| Convenience API | sets config, delegates | sets config, delegates | easy API and configured API are one model |
| Extra concern | simpler first case | IPv6-only / IPv4-mapped / dual-stack questions | deployment semantics differ |

This table connects directly to Chapters 8 and 9.

Chapter 8 explains the address row.

Chapter 9 explains the role and connection rows.

This chapter shows IPv4 and IPv6 as the first concrete comparison pair.

### What to remember

Remember:

- IPv4 and IPv6 are the first concrete comparison pair because they are familiar and structurally parallel.
- IPv4 is not the only "normal" case; IPv6 is also a first-class lower communication family.
- The visible namespace change is `net::in` to `net::in6`.
- Both families use a host-plus-port address shape.
- Their wildcard forms differ: `0.0.0.0` for IPv4 and `::` for IPv6.
- The server/client/factory/context/runtime model stays the same.
- The same protocol context can often be used across both families.
- Convenience `listen(...)` and `connect(...)` overloads set configuration and delegate to the general path.
- IPv6 adds questions around IPv6-only use, IPv4-mapped addresses, and dual-stack behavior.
- The point of the comparison is controlled variation: same architecture, different lower-family semantics.

### Closing perspective

Chapter 9 established the general server/client/connection model.

This chapter specialized that model through IPv4 and IPv6.

The next chapter changes the lower-family assumption more strongly.

Unix domain sockets keep the same broad SNode.C role model, but endpoint identity is no longer host plus port. It becomes local socket-path identity.

That makes Unix domain sockets the right next step.

The reader can now ask:

> What happens when the server/client/connection model remains familiar, but the network-layer address is no longer internet-shaped?
