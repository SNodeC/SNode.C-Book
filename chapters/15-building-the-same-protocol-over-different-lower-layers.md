## Building the Same Protocol over Different Lower Layers

### From context and factory separation to lower-family transfer

Chapter 13 placed application protocol behavior in the `SocketContext`. Chapter 14 placed context construction in the `SocketContextFactory`. This chapter uses both separations together.

The central question is:

> What does the separation buy us when the lower communication family changes?

The short answer is that a protocol can often keep its core shape even when the carrier changes:

```text
SocketContext
  -> protocol behavior

SocketContextFactory
  -> context creation, role preconfiguration, and stable dependency passing

application-side SocketServer / SocketClient handle
  -> selects the concrete lower-family server/client type

registered server/client instance
  -> long-lived runtime-visible communication role

SocketAddress / configuration
  -> lower-family-specific endpoint identity and deployment shape
```

This is where the design discipline from Chapters 13 and 14 becomes visible across lower families. The protocol does not become independent of all lower-layer reality.

Address identity, local/remote meaning, deployment, platform support, pairing, permissions, TLS, retry behavior, and operational configuration still matter. But when protocol behavior lives in a `SocketContext`, and when construction choices remain in a `SocketContextFactory`, much more can transfer than one might first expect.

The lower family matters. It does not always have to rewrite the protocol endpoint. That balance is the main idea of this chapter.

### The lower-family transfer model

The transfer model keeps four questions apart:

| Question | Best home |
|---|---|
| What does the protocol do on one connection? | `SocketContext` |
| Which context should be created for this connection? | `SocketContextFactory` |
| Which lower communication family is selected? | the application-side server/client handle type and its registration |
| Which endpoint identity and deployment values are used? | `SocketAddress`, configuration, and startup/deployment data |

This separation is the reason the same protocol core can often move across lower families without rewriting the protocol itself.

Figure~\ref{fig:snodec-lower-family-transfer} shows the same idea as a transfer model: the protocol-side boundary remains stable, while the lower-family side changes endpoint identity, concrete server/client type, configuration, and deployment assumptions.

![The lower-family transfer model. The protocol-side boundary remains stable while endpoint families change address types, concrete server/client types, configuration, and deployment assumptions.](figures/pdf/fig-04-lower-family-transfer-model.pdf){#fig:snodec-lower-family-transfer width=95% latex-placement="tbp"}

The visible server/client type changes because the application selects a different lower-family specialization. The registered instance then carries that configured lower-family role into the runtime. The concrete `SocketConnection` represents one peer relationship under that role. The factory creates the per-connection context for that connection. The context implements the protocol endpoint.

This is not merely a naming exercise.

It prevents one common design mistake: putting lower-family setup, protocol behavior, context construction, and deployment policy into the same class. SNode.C makes those boundaries visible. Application code becomes easier to move across families when it respects them.

### What can remain stable

Not everything transfers. But several important parts often can.

#### Protocol shape

The protocol shape includes questions such as:

- Who sends first?
- What happens when data arrives?
- How are bytes interpreted?
- When is a response sent?
- What state is remembered per connection?
- What causes the connection to close?
- What happens when the peer disconnects?
- What errors or signals matter to the protocol?

These are context-level questions. They belong to the application protocol endpoint.

A well-written `SocketContext` can answer these questions without immediately depending on whether the connection came from IPv4, IPv6, Unix domain sockets, RFCOMM, or L2CAP.

That does not mean the context must be blind to its carrier.

It means the context should only depend on lower-family facts when those facts are part of the protocol's meaning.

#### Context behavior

The following parts often remain stable:

- lifecycle handling in `onConnected()` and `onDisconnected()`,
- input handling in `onReceivedFromPeer()`,
- per-connection protocol state,
- use of `sendToPeer(...)`,
- use of `readFromPeer(...)`,
- timeout and close decisions that are protocol-driven,
- metrics interpreted in protocol terms.

This is the main reason Chapter 13 emphasized context discipline.

A context that is truly a per-connection protocol endpoint is easier to carry to another lower family. A context that quietly performs address selection, deployment decisions, reconnect policy, or global orchestration is much harder to move.

The useful question is:

::: {.snodec-rule title="Protocol/carrier rule"}
Does this code describe the protocol conversation, or does it describe the carrier and deployment environment?
:::

Protocol conversation belongs in the context. Carrier and deployment concerns usually belong outside it.

#### Factory construction policy

The factory may also transfer. If the same context type is suitable across several lower families, the factory can remain small and recognizable.

It may still create:

```cpp
new EchoSocketContext(connection, Role::Server)
```

or:

```cpp
new EchoSocketContext(connection, Role::Client)
```

The application-side server/client handle type changes. The endpoint identity changes. The deployment setting changes.

The context construction shape can still remain familiar.

This is why Chapters 13 and 14 came before this chapter. A well-factored context and a disciplined factory make lower-family transfer practical. The factory does not make the protocol portable by magic. It keeps the construction boundary clean enough that portability can be judged honestly.

### What changes with the lower family

Lower-family transfer is not the same as pretending all families are identical. Several things usually change.

#### Server/client handle type and registered instance

The visible server/client handle type changes because the application chooses a different lower-family specialization.

Examples include:

```cpp
net::in::stream::legacy::SocketServer<MyFactory>
net::in6::stream::legacy::SocketServer<MyFactory>
net::un::stream::legacy::SocketServer<MyFactory>
net::rc::stream::legacy::SocketServer<MyFactory>
net::l2::stream::legacy::SocketServer<MyFactory>
```

and the corresponding client types.

The role model remains recognizable:

```text
application-side handle
  -> registered instance
      -> connection
          -> factory
              -> context
```

But the selected namespace and lower-family component change.

That change is meaningful. `net::in`, `net::in6`, `net::un`, `net::rc`, and `net::l2` are not decorative names. They select different endpoint families, address semantics, platform requirements, and deployment assumptions.

#### Address and endpoint configuration

The endpoint identity changes with the lower family.

| Lower family | Endpoint identity |
|---|---|
| IPv4 | host + port |
| IPv6 | host + port |
| Unix domain sockets | local path |
| RFCOMM | Bluetooth address + channel |
| L2CAP | Bluetooth address + PSM |

This changes the values passed to convenience calls, configuration objects, command-line options, and deployment scripts. The local/remote distinction remains useful. The concrete address form changes.

That is the central transfer lesson from Chapters 8 through 12. The framework model can remain stable while the meaning of an endpoint changes. A good design does not hide that change. It places it where it belongs.

#### Deployment assumptions

Deployment also changes.

| Lower family | Deployment consequence |
|---|---|
| IPv4 | network reachability, interface exposure, firewall and routing questions |
| IPv6 | IPv6 addressing, dual-stack or IPv6-only behavior, address notation |
| Unix domain sockets | local IPC, path ownership, path cleanup, local permissions |
| RFCOMM | Bluetooth stack availability, pairing/trust setup, channel semantics |
| L2CAP | Bluetooth stack availability, pairing/trust setup, PSM semantics |

These differences are real. The protocol may transfer. The deployment does not become identical.

For Bluetooth, for example, the protocol may still be a simple stream protocol. But the devices still need the platform Bluetooth stack, suitable permissions, adapter state, and pairing/trust setup before SNode.C can communicate between them. For Unix domain sockets, the same protocol may run locally, but path placement and cleanup become part of the service design. For IP families, routing, exposure, firewall behavior, and address selection remain operational concerns.

The correct design statement is therefore not:

```text
The lower family does not matter.
```

The correct design statement is:

```text
The lower family matters, but it does not always have to rewrite the protocol endpoint.
```

### Echo as the smallest transfer microscope

The echo application gives the smallest useful example. Echo is not interesting because echo is sophisticated. It is interesting because it exposes the placement boundary.

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

The point is not that every real protocol is as simple as echo.

The point is that the echo example makes the boundary visible:

- receive behavior belongs in the context,
- role construction belongs in the factory,
- lower-family selection belongs in the server/client handle type and configuration,
- endpoint identity belongs in the address/configuration layer,
- deployment remains outside the protocol core unless the protocol genuinely depends on it.

A more complex protocol can grow from the same discipline.

### One protocol, several carriers

A compact comparison makes the transfer visible.

| Carrier | Endpoint identity | What changes | What may remain |
|---|---|---|---|
| IPv4 | host + port | address/configuration/deployment | context, factory shape, protocol behavior |
| IPv6 | host + port | address form, IPv6 semantics, deployment | context, factory shape, protocol behavior |
| Unix domain sockets | local path | local IPC path and lifecycle | context, factory shape, protocol behavior |
| RFCOMM | Bluetooth address + channel | Bluetooth stack, pairing/trust setup, channel semantics | context, factory shape, protocol behavior |
| L2CAP | Bluetooth address + PSM | Bluetooth stack, pairing/trust setup, PSM semantics | context, factory shape, protocol behavior |

This table is not a portability guarantee. It is a design test.

If the protocol's meaning is independent of the lower-family identity, the context can often remain stable. If the protocol's meaning depends on lower-family identity, the context may need to specialize.

The table is useful precisely because it does not hide the changing column. It shows how far reuse can go before honesty requires a different context, a different factory, or a different deployment shape.

### Designing for lower-family transfer

A protocol that should travel well across lower families should be designed with clear boundaries. The following rules are not mechanical requirements. They are design habits that make transfer easier to reason about.

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

A protocol may still inspect lower-family data for logging, diagnostics, authorization, routing, or policy. That is not forbidden. The important question is whether the lower-family detail is part of the protocol meaning or merely part of the carrier.

#### Keep per-connection state in the context

Connection-local protocol state belongs in the context.

That makes the protocol endpoint portable because the state travels with the connection, not with the outer handle or lower-family setup.

Good context state is:

- explicit,
- protocol-named,
- connection-local where possible,
- updated at understandable lifecycle and input points,
- and independent of lower-family details unless those details are part of protocol meaning.

This follows directly from Chapter 13. A context is the per-connection protocol endpoint. If a value describes the state of this conversation with this peer, the context is often the right scope for it.

#### Keep lower-family setup in the handle, instance, and configuration

The lower-family-specific setup belongs outside the protocol core.

This includes:

- choosing `net::in`, `net::in6`, `net::un`, `net::rc`, or `net::l2`,
- choosing legacy or TLS connection handling,
- setting address, path, channel, or PSM values,
- configuring local and remote endpoints,
- selecting retry or reconnect behavior,
- selecting deployment-specific options.

These choices are real and important. They should not be hidden inside the protocol behavior unless the protocol truly needs them.

The visible server/client handle and its configuration define what will be registered. The registered instance then participates in the runtime as a lower-family-specific communication role. Keeping this distinction clear prevents protocol code from becoming the place where deployment decisions are quietly made.

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

Construction-time variation is healthy when it makes the protocol roles clear. It becomes unhealthy when the factory begins to execute the protocol conversation. That boundary was the main lesson of Chapter 14, and it becomes especially useful when the same protocol travels across carriers.

### Preconfigured factories and endpoint roles

Chapter 14 explained that server and client constructors can forward an argument pack into the factory constructor. That makes it possible to preconfigure factories with stable role and dependency information. This matters for lower-family transfer because the same mechanism can create role-specific endpoints over different carriers.

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
          -> lower family selected by application-side handle and configuration
```

The broader discussion of higher-level communication patterns belongs later.

Later chapters return to patterns such as publisher/subscriber, request/response, command/event, gateways, adapters, bridges, and protocol translators. Here the narrower point is lower-family transfer: a factory can keep endpoint construction stable while the outer communication family changes.

### Same protocol shape does not mean same deployment

This distinction is essential. The same protocol shape may run over several lower families, but the resulting systems are not operationally identical. An IPv4 service may be reachable over a LAN or wider network.

An IPv6 service raises IPv6 addressing and deployment questions. A Unix-domain service is local to one host and depends on path placement and local access. An RFCOMM service depends on Bluetooth stack support, pairing/trust setup, adapter state, and RFCOMM channel semantics.

An L2CAP service depends on Bluetooth stack support, pairing/trust setup, adapter state, and PSM semantics. TLS adds certificate, trust, and connection-layer deployment questions. So lower-family transfer must be understood as an architectural separation, not as a promise that deployment disappears.

A good design lets the stable protocol core remain visible while keeping the family-specific deployment surface explicit.

### When reuse should stop

Lower-family transfer is useful only when it preserves clarity. There are cases where reuse should stop.

#### Family-specific semantics may be part of the protocol

A protocol may genuinely depend on a lower-family detail.

For example, a Bluetooth-oriented protocol may care about device identity in a way that is not equivalent to an IP address or a Unix-domain path.

A local IPC protocol may depend on path placement or local access assumptions.

A network-facing protocol may treat remote address information as part of authentication, rate limiting, routing, or trust decisions.

If those details are part of the protocol's meaning, hiding them would be dishonest. In that case, the context should be allowed to know what it needs to know.

#### Deployment-specific protocols may deserve separate contexts

Sometimes two deployments look similar at first but differ enough that one shared context becomes awkward. A local diagnostic Unix-domain service may have different assumptions than a network-facing service. A Bluetooth device-near endpoint may have different lifecycle expectations than an IP service.

A TLS-protected network service may have different trust assumptions than a local IPC service. If one context becomes full of conditionals trying to cover all deployments, separate contexts may be clearer. This is not a failure of abstraction.

It is a sign that the protocol meaning has diverged.

#### Small duplication can be healthier than over-abstraction

Experienced C++ developers often try to remove duplication aggressively. That is not always the right instinct here.

A small amount of explicit outer-layer difference can be healthier than a giant abstraction that erases meaningful distinctions.

A good design may have:

- one stable protocol context,
- small family-specific handle declarations,
- clear family-specific configuration,
- small role-specific factories,
- and explicit deployment choices.

This is not failure. It is clean factoring. The goal is not to make all lower families look identical.

The goal is to keep the stable protocol core stable and the real family-specific differences visible.

### What remains stable and what changes

The following table summarizes the chapter.

| Concern | Often stable | Often changes |
|---|---|---|
| Protocol behavior | `SocketContext` logic | only when family semantics matter |
| Context creation | factory shape and role construction | factory constructor data or selected context type |
| Application-side handle | conceptual server/client shape | concrete lower-family type |
| Registered instance | long-lived runtime-visible communication role | configured family, endpoint identity, operational behavior |
| Endpoint identity | local/remote distinction | host/port, path, channel, PSM |
| Runtime model | event-driven lifecycle | operational startup/configuration details |
| Deployment | broad application intent | reachability, locality, platform, pairing, permissions, security assumptions |

This table is the practical transfer model. Reuse is strongest when the stable column stays honest and the changing column is not hidden.

### Configuration becomes visible here

Lower-family transfer naturally makes configuration more visible.

A family transfer may change:

- selected server/client handle type,
- registered instance name,
- local endpoint values,
- remote endpoint values,
- role-specific factory arguments,
- TLS or legacy selection,
- retry or reconnect behavior,
- startup arguments,
- deployment files,
- platform or permission requirements.

That is why the next part of the book turns to configuration. Configuration is not merely operational convenience. It is one of the places where architectural variation becomes explicit.

Once the same protocol can be carried over different lower families, configuration becomes more than a collection of values. It is where endpoint identity, selected lower family, role naming, TLS/legacy choice, retry behavior, and deployment-specific variation become visible.

This chapter shows why configuration matters. Chapter 16 begins to explain its philosophy.

::: {.snodec-remember title="What to remember"}
- Lower-family transfer is possible when protocol behavior is kept in the `SocketContext`.
- The factory keeps context creation, role preconfiguration, and stable dependency passing separate from protocol behavior.
- The application-side server/client type and the registered instance change with the lower family; the protocol endpoint may remain stable.
- Endpoint identity and configuration change with the lower family: host/port, path, channel, or PSM.
- Deployment assumptions still matter; protocol reuse does not make systems operationally identical.
- Reuse should stop when lower-family semantics become part of the protocol's meaning.
- Small family-specific outer code is often clearer than an over-generalized abstraction.
- Chapter 16 begins the configuration view because lower-family transfer makes configuration visible.
:::

### Closing perspective

Part IV moved from raw connections to application protocol structure. Chapter 13 explained the protocol endpoint. Chapter 14 explained context creation.

This chapter showed how those two separations make lower-family transfer possible.

The result is the central pattern:

```text
SocketContext
  -> protocol behavior

SocketContextFactory
  -> construction and role preconfiguration

application-side SocketServer / SocketClient handle
  -> concrete lower-family selection

registered server/client instance
  -> runtime-visible configured communication role

configuration
  -> endpoint identity and deployment shape
```

With that structure in place, SNode.C is no longer just a set of socket-family APIs.

It becomes a communication architecture in which protocol behavior, context creation, lower-family selection, registration, and operational configuration each have a clear place.

The next part begins the configuration view. It shows how applications are shaped, named, configured, and operated in practice.
