## Building the Same Protocol over Different Lower Layers

### From context/factory separation to lower-family transfer

Chapter 13 separated protocol behavior from the surrounding communication machinery.

Chapter 14 separated context creation from protocol behavior.

This chapter uses both separations together.

The central question is:

> What happens when the same protocol endpoint is carried by different lower communication families?

The short answer is:

```text
protocol behavior
  -> can often remain in the same SocketContext

context creation
  -> can often remain in a small SocketContextFactory

lower-family role
  -> changes through the concrete SocketServer / SocketClient type

endpoint configuration
  -> changes with the address family
```

This is the transfer point of Part IV.

The protocol does not become independent of all lower-layer reality. Address identity, deployment, platform support, and security assumptions still matter.

But when the protocol behavior is properly placed in the `SocketContext`, and when construction choices are kept in the `SocketContextFactory`, much more can transfer than one might first expect.

### The transfer model

The basic transfer model is:

```text
SocketContext
  -> protocol behavior

SocketContextFactory
  -> context creation and role preconfiguration

SocketServer / SocketClient
  -> lower-family-specific outer communication role

SocketAddress / configuration
  -> lower-family-specific endpoint identity
```

This keeps three questions separate.

| Question | Best home |
|---|---|
| What does the protocol do on one connection? | `SocketContext` |
| Which context should be created for this connection? | `SocketContextFactory` |
| Which lower communication family carries the connection? | `SocketServer` / `SocketClient` instance type and configuration |

This separation is the reason the same protocol can often be moved across lower families without rewriting the protocol itself.

### What can transfer

Not everything transfers.

But several important parts often can.

#### Protocol shape

The protocol shape includes questions such as:

- Who sends first?
- What happens when data arrives?
- How are bytes interpreted?
- When is a response sent?
- What state is remembered per connection?
- What causes the connection to close?

These are context-level questions.

They belong to the application protocol endpoint.

A well-written `SocketContext` can answer these questions without immediately depending on whether the connection came from IPv4, IPv6, Unix domain sockets, RFCOMM, or L2CAP.

#### Context behavior

The following parts often remain stable:

- lifecycle handling in `onConnected()` and `onDisconnected()`,
- input handling in `onReceivedFromPeer()`,
- per-connection protocol state,
- use of `sendToPeer(...)`,
- use of `readFromPeer(...)`,
- timeout and close decisions that are protocol-driven,
- metrics interpreted in protocol terms.

This does not mean the context must never inspect lower-family information.

It means lower-family details should enter the context only when they are part of the protocol's meaning.

#### Factory construction policy

The factory may also transfer.

If the same context type is suitable across several lower families, the factory can remain small and familiar.

It may still create:

```cpp
new EchoSocketContext(connection, Role::Server)
```

or:

```cpp
new EchoSocketContext(connection, Role::Client)
```

The outer instance type changes.

The context creation shape can remain recognizable.

This is why Chapters 13 and 14 came before this chapter: a well-factored context and a disciplined factory make lower-family transfer much easier.

### What must change

Lower-family transfer is not the same as pretending all families are identical.

Several things usually change.

#### Instance type

The concrete outer type changes with the lower family.

Examples include:

```cpp
net::in::stream::legacy::SocketServer<MyFactory>
net::in6::stream::legacy::SocketServer<MyFactory>
net::un::stream::legacy::SocketServer<MyFactory>
net::rc::stream::legacy::SocketServer<MyFactory>
net::l2::stream::legacy::SocketServer<MyFactory>
```

and the corresponding client types.

The role model remains:

```text
server
client
connection
context
factory
```

But the namespace and lower-family component change.

#### Address and endpoint configuration

The endpoint identity changes with the lower family.

| Lower family | Endpoint identity |
|---|---|
| IPv4 | host + port |
| IPv6 | host + port |
| Unix domain sockets | local path |
| RFCOMM | Bluetooth address + channel |
| L2CAP | Bluetooth address + PSM |

This changes the values passed to convenience calls, configuration objects, command-line options, and deployment scripts.

The local/remote distinction remains useful.

The concrete address form changes.

#### Deployment assumptions

Deployment also changes.

| Lower family | Deployment consequence |
|---|---|
| IPv4 | network reachability, interface exposure, firewall and routing questions |
| IPv6 | IPv6 addressing, dual-stack or IPv6-only behavior, address notation |
| Unix domain sockets | local IPC, path ownership, path cleanup, local permissions |
| RFCOMM | Bluetooth stack availability, device pairing/discovery concerns, RFCOMM channel semantics |
| L2CAP | Bluetooth stack availability, PSM semantics, device-near communication assumptions |

These differences are real.

The protocol may transfer.

The deployment does not become identical.

### Echo as the smallest transfer example

The echo application gives the smallest useful example.

The protocol behavior lives in one context type:

```cpp
EchoSocketContext::EchoSocketContext(SocketConnection* socketConnection, Role role)
```

The role is stored in the context.

When the connection becomes ready, the client role starts the exchange:

```cpp
if (role == Role::CLIENT) {
    sendToPeer("Hello peer! Nice to see you!!!");
}
```

When data arrives, the context reads a chunk, sends the same bytes back, and reports the processed amount:

```cpp
const std::size_t chunklen = readFromPeer(chunk, 4096);

if (chunklen > 0) {
    sendToPeer(chunk, chunklen);
}

return chunklen;
```

The factories then create role-specific contexts:

```cpp
return new EchoSocketContext(socketConnection, EchoSocketContext::Role::SERVER);
```

and:

```cpp
return new EchoSocketContext(socketConnection, EchoSocketContext::Role::CLIENT);
```

This is the important shape:

```text
same context type
  -> role-specific construction
      -> same receive behavior
          -> different possible outer carriers
```

Echo is only a small microscope.

The larger lesson is that protocol behavior can remain stable when it is placed in the context and when family-specific concerns stay outside the protocol core.

### One protocol, several carriers

A compact comparison makes the transfer visible.

| Carrier | Endpoint identity | What changes | What may remain |
|---|---|---|---|
| IPv4 | host + port | address/configuration/deployment | context, factory shape, protocol behavior |
| IPv6 | host + port | address form, IPv6 semantics, deployment | context, factory shape, protocol behavior |
| Unix domain sockets | local path | local IPC path and lifecycle | context, factory shape, protocol behavior |
| RFCOMM | Bluetooth address + channel | Bluetooth stack and channel semantics | context, factory shape, protocol behavior |
| L2CAP | Bluetooth address + PSM | Bluetooth stack and PSM semantics | context, factory shape, protocol behavior |

The table should not be read as a promise that every protocol works unchanged everywhere.

It should be read as a design test.

If the protocol's meaning is independent of the lower-family identity, the context can often remain stable.

If the protocol's meaning depends on lower-family identity, the context may need to specialize.

### Designing for lower-family transfer

A protocol that should travel well across lower families should be designed with clear boundaries.

#### Keep endpoint identity out of core protocol behavior unless it matters

If the protocol does not conceptually care whether the peer is identified by host/port, path, channel, or PSM, then those details should not dominate the context.

For example, an echo protocol does not inherently care whether the peer arrived through:

- IPv4,
- IPv6,
- Unix domain sockets,
- RFCOMM,
- or L2CAP.

The context can think in terms of:

```text
connection became ready
data arrived
data was processed
response was sent
connection ended
```

That is the correct level for many application protocols.

#### Keep per-connection state in the context

Connection-local protocol state belongs in the context.

That makes the protocol endpoint portable because the state travels with the connection, not with the outer instance or lower-family setup.

Good context state is:

- explicit,
- protocol-named,
- connection-local where possible,
- and independent of lower-family details unless those details are part of protocol meaning.

#### Keep lower-family setup in the instance and configuration

The lower-family-specific setup belongs outside the protocol core.

This includes:

- choosing `net::in`, `net::in6`, `net::un`, `net::rc`, or `net::l2`,
- choosing legacy or TLS connection handling,
- setting address, path, channel, or PSM values,
- configuring local and remote endpoints,
- selecting deployment-specific options.

These choices are real and important.

They should not be hidden inside the protocol behavior unless the protocol truly needs them.

#### Use factories for role and construction differences

Factories are the right place to keep construction differences visible.

A server-side context may receive:

```cpp
Role::Server
```

A client-side context may receive:

```cpp
Role::Client
```

A publisher-side endpoint may receive:

```cpp
Role::Publisher
```

A command-sink endpoint may receive:

```cpp
Role::CommandSink
```

The point is not the exact enum.

The point is the boundary:

```text
factory
  -> creates the right endpoint

context
  -> behaves as that endpoint
```

### Preconfigured factories and endpoint roles

Chapter 14 explained that server and client constructors can forward an argument pack into the factory constructor.

That makes it possible to preconfigure factories with stable role and dependency information.

This matters for lower-family transfer because the same mechanism can create role-specific endpoints over different carriers.

Examples include:

- producer / consumer,
- command source / command sink,
- event source / event receiver,
- requester / request handler,
- model-side / view-side / controller-side endpoints.

This chapter uses those roles only lightly.

The mechanism matters here because it supports transfer:

```text
same endpoint role
  -> preconfigured factory
      -> context created for each connection
          -> lower family selected by outer instance
```

The broader discussion of higher-level communication patterns belongs later.

Chapter 35 returns to patterns such as publisher/subscriber, request/response, command/event, gateway, adapter, bridge, local proxy, protocol translator, and device façade. Here the focus is narrower: how context/factory separation lets one protocol shape survive lower-family changes.

### Same protocol shape does not mean same deployment

This distinction is essential.

The same protocol shape may run over several lower families, but the resulting systems are not operationally identical.

An IPv4 service may be reachable over a LAN or wider network.

An IPv6 service raises IPv6 addressing and deployment questions.

A Unix-domain service is local to one host and depends on path placement and local access.

An RFCOMM service depends on Bluetooth stack support and RFCOMM channel semantics.

An L2CAP service depends on Bluetooth stack support and PSM semantics.

TLS adds its own certificate, trust, and connection-layer deployment questions.

So the correct statement is not:

```text
The lower family does not matter.
```

The correct statement is:

```text
The lower family matters, but it does not always have to rewrite the protocol endpoint.
```

That is the balance SNode.C is designed to make practical.

### When reuse should stop

Lower-family transfer is useful only when it preserves clarity.

There are cases where reuse should stop.

#### Family-specific semantics may be part of the protocol

A protocol may genuinely depend on a lower-family detail.

For example, a Bluetooth-oriented protocol may care about device identity in a way that is not equivalent to an IP address or a Unix-domain path.

A local IPC protocol may depend on path placement or local access assumptions.

If those details are part of the protocol's meaning, hiding them would be dishonest.

In that case, the context should be allowed to know what it needs to know.

#### Deployment-specific protocols may deserve separate contexts

Sometimes two deployments look similar at first but differ enough that one shared context becomes awkward.

A local diagnostic Unix-domain service may have different assumptions than a network-facing service.

A Bluetooth device-near endpoint may have different lifecycle expectations than an IP service.

If one context becomes full of conditionals trying to cover all deployments, separate contexts may be clearer.

#### Small duplication can be healthier than over-abstraction

Experienced C++ developers often try to remove duplication aggressively.

That is not always the right instinct here.

A small amount of explicit outer-layer difference can be healthier than a giant abstraction that erases meaningful distinctions.

A good design may have:

- one stable protocol context,
- small family-specific instance declarations,
- clear family-specific configuration,
- small role-specific factories,
- and explicit deployment choices.

This is not failure.

It is clean factoring.

### What remains stable and what changes

The following table summarizes the chapter.

| Concern | Often stable | Often changes |
|---|---|---|
| Protocol behavior | `SocketContext` logic | only when family semantics matter |
| Context creation | factory shape and role construction | factory constructor data or selected context type |
| Outer role | server/client/connection model | concrete namespace and instance type |
| Endpoint identity | local/remote distinction | host/port, path, channel, PSM |
| Runtime model | event-driven lifecycle | operational startup/configuration details |
| Deployment | broad application intent | reachability, locality, platform, security assumptions |

This table is the practical transfer model.

Reuse is strongest when the stable column stays honest and the changing column is not hidden.

### Configuration becomes visible here

Lower-family transfer naturally makes configuration more visible.

A family transfer may change:

- selected instance type,
- local endpoint values,
- remote endpoint values,
- role-specific factory arguments,
- TLS or legacy selection,
- named instance configuration,
- startup arguments,
- deployment files.

That is why the next part of the book turns to configuration.

Configuration is not merely operational convenience. It is one of the places where architectural variation becomes explicit.

This chapter shows why configuration matters.

Chapter 16 begins to explain its philosophy.

### What to remember

Remember:

- Lower-family transfer is possible when protocol behavior is properly placed in `SocketContext`.
- The factory creates the right context for each connection.
- Preconfigured factories can express role-specific endpoints.
- The server/client instance type usually changes with the lower family.
- Address and endpoint configuration change with the lower family.
- Deployment assumptions still matter.
- The same context can often be reused if the protocol does not depend on lower-family semantics.
- The same factory shape can often be reused if context construction remains stable.
- Small family-specific outer code is often healthier than over-generalized abstraction.
- Reuse should stop when it hides real semantic differences.
- Chapter 35 returns later to higher-level communication patterns.
- Chapter 16 begins the configuration view because lower-family transfer makes configuration visible.

### Closing perspective

Part IV moved from raw connections to application protocol structure.

Chapter 13 explained the protocol endpoint.

Chapter 14 explained context creation.

This chapter showed how those two separations make lower-family transfer possible.

The result is the central pattern:

```text
SocketContext
  -> protocol behavior

SocketContextFactory
  -> construction and role preconfiguration

SocketServer / SocketClient
  -> lower-family-specific outer role

configuration
  -> endpoint identity and deployment shape
```

With that structure in place, SNode.C is no longer just a set of socket-family APIs.

It becomes a communication architecture in which protocol behavior, context creation, lower-family selection, and operational configuration each have a clear place.

The next part begins the configuration view.

It shows how applications are shaped, named, and operated in practice.
