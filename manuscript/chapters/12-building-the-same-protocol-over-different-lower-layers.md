## Building the Same Protocol over Different Lower Layers {#building-the-same-protocol-over-different-lower-layers}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Identify the source, component and endpoint changes needed to transfer the line protocol.
- **O2.** Verify identical reconstructed replies across IPv4 and Unix-domain network families.
- **O3.** Decide when network-family-specific identity or trust assumptions require a different protocol policy.
:::

\index{network-family transfer}
\index{protocol reuse}
\index{network families}

The line protocol now gives us something concrete to transfer: a receive buffer, three commands, response rules, and a factory that creates one parser per connection. This chapter keeps those files fixed while changing the endpoint that carries their bytes.

Address identity, deployment, platform support, permissions, TLS and retry behavior still matter. The context and factory separation lets us ask which protocol decisions remain valid when those conditions change.

### The network-family transfer model {#the-lower-family-transfer-model}

\index{network-family transfer}
\index{network families}
\index{network-family choice}

The transfer model keeps four questions apart:

| Question | Best home |
|---|---|
| What does the protocol do on one connection? | `SocketContext` |
| Which context should be created for this connection? | `SocketContextFactory` |
| Which network family is selected? | the server/client handle type and its registration |
| Which endpoint identity and deployment values are used? | `SocketAddress`, configuration, and startup/deployment data |

This separation is the reason the same protocol core can often move across network families without rewriting the protocol itself.

Figure \ref{fig:snodec-lower-family-transfer} shows the same idea as a transfer model: the protocol-side boundary remains stable, while the network-family side changes endpoint identity, concrete server/client type, configuration, and deployment assumptions. It is a portability map for deciding what may stay stable and what must be reselected.

![The network-family transfer model. Branches show possible network-family selections for the same context abstraction, subject to protocol assumptions and platform support; they do not imply identical deployment behavior.](assets/figures/pdf/fig-04-lower-family-transfer-model.pdf){#fig:snodec-lower-family-transfer width=95% latex-placement="tbp"}

### What can remain stable

\index{protocol shape}
\index{context behavior}
\index{factory construction policy}

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

That does not mean the context must be blind to its network family.

It means the context should only depend on network-family facts when those facts are part of the protocol's meaning.

Input handling, per-peer state, sending/reading, and protocol-driven timeout or close decisions may transfer. Address selection, deployment and reconnect policy should remain explicit outside the context.

The useful question is:

::: {.snodec-rule title="Protocol/network-family rule"}
Does this code describe the protocol conversation, or does it describe the network-family and deployment environment?
:::

Protocol conversation belongs in the context. Network-family and deployment concerns usually belong outside it.

The factory may also transfer. If the same context type is suitable across several network families, the factory can remain small and recognizable.

It may still create:

```cpp
new EchoSocketContext(connection, Role::Server)
```

or:

```cpp
new EchoSocketContext(connection, Role::Client)
```

### Selecting endpoints and deployment

\index{handle type}
\index{endpoint configuration}
\index{deployment assumptions}

Network-family transfer is not the same as pretending all families are identical. Several things usually change.

The visible server/client handle type changes because the application chooses a different network-family specialization.

Examples include:

```cpp
net::in::stream::legacy::SocketServer<MyFactory>
net::in6::stream::legacy::SocketServer<MyFactory>
net::un::stream::legacy::SocketServer<MyFactory>
net::rc::stream::legacy::SocketServer<MyFactory>
net::l2::stream::legacy::SocketServer<MyFactory>
```

and the corresponding client types.

The selected namespace and component change the endpoint semantics and platform requirements.

The endpoint identity changes with the network family.

| Network family | Endpoint identity |
|---|---|
| IPv4 | host + port |
| IPv6 | host + port |
| Unix domain sockets | local path |
| RFCOMM | Bluetooth address + channel |
| L2CAP | Bluetooth address + PSM |

These values enter convenience calls, configuration and deployment scripts. Local/remote direction remains useful even though the address form changes.

Deployment also changes.

| Network family | Deployment consequence |
|---|---|
| IPv4 | network reachability, interface exposure, firewall and routing questions |
| IPv6 | IPv6 addressing, dual-stack or IPv6-only behavior, address notation |
| Unix domain sockets | local IPC, path ownership, path cleanup, local permissions |
| RFCOMM | Bluetooth stack availability, pairing/trust setup, channel semantics |
| L2CAP | Bluetooth stack availability, pairing/trust setup, PSM semantics |

Bluetooth additionally needs a supported adapter and any pairing/trust required by its service. TLS adds certificate and trust configuration. The same byte protocol does not establish equivalent reachability or security.

### Echo as the smallest transfer microscope

\index{echo pair!network-family transfer}

The complete Chapter 3 listing supplies these snippets, repeated here to show the transfer boundary. The echo application gives the smallest useful example. Echo is interesting not because it is sophisticated, but because it exposes the placement boundary.

The protocol behavior lives in one context type:

```cpp
EchoSocketContext::EchoSocketContext(SocketConnection* socketConnection, Role role)
```

The server/client selector is stored in the context.

When the connection becomes ready, the client side starts the exchange:

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

The factories then create side-specific contexts:

```cpp
return new EchoSocketContext(socketConnection, EchoSocketContext::Role::SERVER);
```

and:

```cpp
return new EchoSocketContext(socketConnection, EchoSocketContext::Role::CLIENT);
```

\index{protocol reuse}
\index{network families}

The network-family comparison is useful as a design test, not as a promise of automatic portability. If the protocol's meaning is independent of host/port, path, channel, or PSM, the same context and factory shape can often remain recognizable while the outer handle, address, configuration, and deployment surface change. If the protocol's meaning depends on one of those facts, the context should specialize instead of pretending that all network families are the same.

This is the useful transfer question:

::: {.snodec-rule title="Network-family transfer test"}
Can the protocol conversation stay honest when the network family changes, or has network-family identity become part of the protocol meaning?
:::

### A worked transfer: the line server over IPv4 and Unix sockets

Changing the network family changes the public type header and the linked component when application code directly names that stream type. The protocol context can remain stable, but the source/build front door follows the selected network family and connection variant.

| Network family / connection variant | Public include | Matching component |
|---|---|---|
| IPv4 legacy stream server | `<net/in/stream/legacy/SocketServer.h>` | `net-in-stream-legacy` |
| IPv6 legacy stream server | `<net/in6/stream/legacy/SocketServer.h>` | `net-in6-stream-legacy` |
| Unix-domain legacy stream server | `<net/un/stream/legacy/SocketServer.h>` | `net-un-stream-legacy` |
| IPv4 TLS stream server | `<net/in/stream/tls/SocketServer.h>` | `net-in-stream-tls` |

Chapter 27 gives the complete matrix. Here the point is the transfer rule: keep protocol behavior stable where possible, and change the public type and component selection deliberately.

Use the complete `LineProtocol-Server` companion from Chapter 10. This exercise needs the installed IPv4 and Unix-domain legacy stream components and Python 3 for an independent client. It does not require Bluetooth hardware. Create two copies in a new private working directory, using the book-package variable from Chapter 2:

```sh
export SNODEC_TRANSFER=$(mktemp -d)
cp -R "$SNODEC_BOOK_SOURCE/companion/examples/LineProtocol-Server" "$SNODEC_TRANSFER/ipv4"
cp -R "$SNODEC_BOOK_SOURCE/companion/examples/LineProtocol-Server" "$SNODEC_TRANSFER/unix"
printf '%s\n' "$SNODEC_TRANSFER"
```

Keep that directory path available in each terminal used below. In the `unix` copy, make four type, address, header and component edits:

| Location | IPv4 selection | Unix-domain selection |
|---|---|---|
| `main.cpp` public include | `<net/in/stream/legacy/SocketServer.h>` | `<net/un/stream/legacy/SocketServer.h>` |
| `LineProtocolServer` alias | `net::in::stream::legacy` | `net::un::stream::legacy` |
| first `server.listen(...)` argument | `8090` | `"/tmp/line-transfer.sock"` |
| both component references in `CMakeLists.txt` | `net-in-stream-legacy` | `net-un-stream-legacy` |

Leave `LineCommandServerContext.cpp`, its header, and `LineCommandServerContextFactory.h` unchanged. The status callback already names `LineProtocolServer::SocketAddress`, so its address type follows the selected server alias. The instance name stays `lineprotocolserver`; these are separate processes, and keeping that name makes their configuration paths directly comparable.

Build both consumers against the installation prepared earlier:

```sh
for family in ipv4 unix; do
    cmake -S "$SNODEC_TRANSFER/$family" -B "$SNODEC_TRANSFER/$family-build" \
      -DCMAKE_PREFIX_PATH="$HOME/.local/snodec"
    cmake --build "$SNODEC_TRANSFER/$family-build" --parallel 4
done
```

In one terminal, run the IPv4 server with an explicit loopback bind:

```sh
"$SNODEC_TRANSFER/ipv4-build/line-protocol-server" --log-level=6 \
  lineprotocolserver local --host=127.0.0.1 --port=18090
```

In another, run the Unix-domain server with its socket inside the private exercise directory:

```sh
"$SNODEC_TRANSFER/unix-build/line-protocol-server" --log-level=6 \
  lineprotocolserver local --sun-path="$SNODEC_TRANSFER/line.sock"
```

The command-line values override the source defaults. Chapter 13 explains the instance and section syntax in detail; here it lets the exercise keep deployment values outside the parser. If port `18090` is already occupied, choose another unused port and change the client below to match. A listening failure is not a failed protocol-transfer test.

With both listeners ready, run this independent peer from a terminal with the same `SNODEC_TRANSFER` value:

```python
import os
import socket

endpoints = [
    ("IPv4", socket.AF_INET, ("127.0.0.1", 18090)),
    ("Unix", socket.AF_UNIX, os.path.join(os.environ["SNODEC_TRANSFER"], "line.sock")),
]

for name, family, endpoint in endpoints:
    with socket.socket(family, socket.SOCK_STREAM) as peer:
        peer.settimeout(2)
        peer.connect(endpoint)
        with peer.makefile("rb") as replies:
            assert replies.readline() == b"READY\n"
            peer.sendall(b"PI")
            peer.sendall(b"NG\nSTATUS\n")
            assert replies.readline() == b"PONG\n"
            assert replies.readline() == b"OK\n"
            peer.sendall(b"QUIT\n")
            assert replies.read(1) == b""
    print(name, "READY, PONG, OK, then closure")
```

The expected output reports the same conversation for both families. The two writes deliberately avoid making a complete-command-per-write assumption, although the operating system can still combine them into one receive. Repeat the framing and length-limit cases from Chapter 10 if the context itself changes.

For a network-family-specific failure, change only the Unix client's target to a nonexistent name inside the exercise directory. Connection establishment should fail before `READY`; the parser has not received an invalid command. Restore the target, repeat the successful exchange, then stop both servers with `Ctrl-C` and inspect the socket-path cleanup. This gives three distinct pieces of evidence: the unchanged protocol files, the same observed conversation, and different endpoint failure conditions.

### Designing for network-family transfer {#designing-for-lower-family-transfer}

\index{network-family transfer!design rules}
\index{endpoint identity}

If the protocol does not conceptually care whether the peer is identified by host/port, path, channel, or PSM, then those details should not dominate the context.

A protocol may still inspect network-family data for logging, diagnostics, authorization, routing, or policy. That is not forbidden. The important question is whether the network-family detail is part of the protocol meaning or only needed to establish and operate the connection.

Keep the frame accumulator, parser state and pending request with the connection. They should change at explicit lifecycle and input points, independently of the outer endpoint’s setup.

The network-family-specific setup belongs outside the protocol core.

This includes:

- choosing `net::in`, `net::in6`, `net::un`, `net::rc`, or `net::l2`,
- choosing legacy or TLS connection handling,
- setting address, path, channel, or PSM values,
- configuring local and remote endpoints,
- selecting retry or reconnect behavior,
- selecting deployment-specific options.

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

These are construction-time choices. The factory supplies the construction-time selection; interpreting its protocol belongs in the resulting context.

\index{preconfigured factories}
\index{application roles}

Chapter 11 explained that server and client constructors can forward an argument pack into the factory constructor. That makes it possible to preconfigure factories with stable application-purpose and dependency information. This matters for network-family transfer because the same mechanism can create role-specific endpoints over different network families.

Examples include:

- producer / consumer,
- command source / command sink,
- event source / event receiver,
- requester / request handler,
- model-side / view-side / controller-side endpoints.

The same preconfigured endpoint can be created over another network family when its assumptions still hold. Later MiniGateway chapters apply these roles to publishers, subscribers, gateways and adapters.

### When reuse should stop

\index{over-abstraction}
\index{protocol specialization}

Network-family transfer is useful only when it preserves clarity. There are cases where reuse should stop.

A protocol may genuinely depend on a network-family detail. For example, a Bluetooth-oriented protocol may care about device identity in a way that is not equivalent to an IP address or a Unix-domain path.

A local IPC protocol may depend on path placement or local access assumptions. A network-facing protocol may treat remote address information as part of authentication, rate limiting, routing, or trust decisions.

If those details are part of the protocol's meaning, hiding them would be dishonest. In that case, the context should be allowed to know what it needs to know.

Sometimes two deployments look similar at first but differ enough that one shared context becomes awkward. A local diagnostic Unix-domain service may have different assumptions than a network-facing service. A Bluetooth device-near endpoint may have different lifecycle expectations than an IP service.

A TLS-protected network service may have different trust assumptions than a local IPC service. If one context becomes full of conditionals trying to cover all deployments, separate contexts may be clearer. This is not a failure of abstraction. It is a sign that the protocol meaning has diverged.

Experienced C++ developers often try to remove duplication aggressively. That is not always the right instinct here. A small amount of explicit outer-layer difference can be healthier than a giant abstraction that erases meaningful distinctions.

A good design may have:

- one stable protocol context,
- small family-specific handle declarations,
- clear family-specific configuration,
- small role-specific factories,
- and explicit deployment choices.

This is clean factoring rather than failure. The goal is not to make all network families look identical. The goal is to keep the stable protocol core stable and the real family-specific differences visible.

\index{configuration!network-family transfer}

Network-family transfer naturally makes configuration more visible. Changing the network family may change the selected handle type, instance name, local and remote endpoint values, factory arguments, TLS/legacy choice, retry policy, startup arguments, deployment files, and platform or permission requirements. Configuration is where that variation becomes explicit instead of leaking into protocol code.

::: {.snodec-remember title="What to remember"}
- A protocol can often keep its context and factory shape while the network family changes.
- Network-family choice, endpoint identity, configuration, and deployment remain explicit; they are not hidden by reuse.
- Reuse should stop when network-family semantics become part of the protocol's meaning.
- Small family-specific outer code is often clearer than an over-generalized abstraction.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** List the type, address, header and component edits in the worked transfer and the protocol files left unchanged. Explain why the status callback’s address type follows the server alias.
2. **Review (O3).** A local service authorizes commands by Unix peer credentials. Explain why moving its parser to an IP listener does not transfer that authorization policy.
3. **Lab (O1, O2).** Build and run the Part IV checkpoint. Send the same fragmented and coalesced command sequence over IPv4 and a private Unix path. Expect identical reconstructed replies, partial-prefix silence, `QUIT` closure and Unix-path cleanup.
4. **Lab (O2, O3).** Run the endpoint-failure lab. Expect a nonexistent Unix path to fail before `READY`; on the valid path, expect an unknown command to receive an error while a later `PING` still succeeds. Distinguish endpoint and protocol failure.
5. **Design (O1, O3).** Choose the reusable core and explicit variations for a local measurement helper and a TLS network input. Keep framing separate from trust, configuration and model acceptance; justify any distinct contexts or factory dependencies.

Public answers, commands, and observations: `companion/exercises/ch12/README.md`.
:::
