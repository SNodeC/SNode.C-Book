## Network Families: Addresses, IPv4/IPv6, and Unix Sockets {#network-families-addresses-ipv4-ipv6-and-unix-sockets}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain how family and local/remote role change an address's meaning, including defaults.
- **O2.** Compare observed IPv4 and IPv6 endpoints while holding protocol behavior fixed.
- **O3.** Choose a local producer endpoint and justify path ownership, cleanup, and authorization.
:::

### Address semantics {#socket-addresses-and-address-semantics}

\index{SocketAddress@\texttt{SocketAddress}}
\index{address semantics}
\index{endpoint identity}

Every connection begins with an address, but an address is not merely a string to be parsed.

The first concrete choice is the network family. An application may use IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP. That choice changes what an endpoint *is*; the namespace or build component is only the visible consequence.

In SNode.C, addresses are part of the network layer. They are not incidental parameters passed into `listen(...)` and `connect(...)` and then forgotten. The address type tells the framework and the reader what kind of endpoint identity is being described.

Binding, peer selection, wildcard meaning, local/remote direction, diagnostics, and IP name resolution all depend on the chosen family.

\index{SocketAddress@\texttt{SocketAddress}}
\index{address classes}

The common base is:

```cpp
net::SocketAddress<SockAddrT>
```

A SNode.C address is backed by a concrete socket-address structure and length, and it participates in the framework's broader socket-address abstraction. The template parameter keeps the operating-system address representation visible enough for the family-specific class to remain honest.

::: {.snodec-note title="Endpoint identity note"}
One address pattern, but no false claim that all endpoint identities mean the same thing.
:::

This mirrors the layer model from Chapter 4. The application shape may stay recognizable, but the endpoint family still matters.

\index{local endpoint}
\index{remote endpoint}

A server usually starts with a local bind identity. It may bind to a specific interface, a wildcard address, a Unix-domain path, a Bluetooth address, or a service selector.

A client usually starts with a remote peer identity. It may connect to a host and port, a Unix-domain path, a Bluetooth device and channel, or a Bluetooth device and PSM.

But the distinction is not absolute. A client may also have a local-side address. A server may later observe the remote addresses of connected peers. The same address class can therefore appear in different roles.

This is one reason address semantics deserve careful treatment. A value such as `0`, `""`, or `00:00:00:00:00:00` is not meaningful by itself. It becomes meaningful in a family and in a role.

\index{endpoint identity}
\index{network family}

The concrete address families are:

| Family | Class | Endpoint identity |
|---|---|---|
| IPv4 | `net::in::SocketAddress` | host plus port |
| IPv6 | `net::in6::SocketAddress` | host plus port |
| Unix domain sockets | `net::un::SocketAddress` | local socket path |
| Bluetooth RFCOMM | `net::rc::SocketAddress` | Bluetooth address plus channel |
| Bluetooth L2CAP | `net::l2::SocketAddress` | Bluetooth address plus PSM |

### Concrete address types and their fields

\index{IPv4}
\index{net::in::SocketAddress@\texttt{net::in::SocketAddress}}
\index{host and port}

The IPv4 address class is:

```cpp
net::in::SocketAddress
```

Its identity shape is host plus port.

Here, *host* may mean a numeric IPv4 address or a name that has to be resolved. The port is the IP service selector. Together, they describe an endpoint in the IPv4 family.

A concrete remote endpoint may look like this:

```cpp
net::in::SocketAddress remote("127.0.0.1", 8080);
```

A server-side address that binds to a port on the IPv4 wildcard address may be expressed as:

```cpp
net::in::SocketAddress local(8080);
```

For a server bind, `0.0.0.0` means that the server is not restricted to one specific local IPv4 interface. Port `0` asks the operating system to select an available local port. That is useful in an isolated test, but a client still needs the actual selected port. The same values should not be copied mechanically into a remote destination: a default-constructed address is an initial value, not evidence that a useful peer has been selected.

The IPv4 class also contains the resolution-oriented pieces that belong to IP-style addressing: `Hints`, canonical-name access, and `useNext()`. That is not accidental API growth. A host name may resolve to more than one candidate endpoint. The address abstraction therefore needs room for resolution and iteration.

\index{IPv6}
\index{net::in6::SocketAddress@\texttt{net::in6::SocketAddress}}

The IPv6 address class is:

```cpp
net::in6::SocketAddress
```

Its surface deliberately resembles the IPv4 address class. It has the same host-plus-port teaching shape, the same need for name resolution, and the same idea that a host may be a numeric address or a resolvable name.

A concrete loopback endpoint may look like this:

```cpp
net::in6::SocketAddress remote("::1", 8080);
```

The similarity is useful, but it should not hide the family boundary. IPv6 has its own address syntax, operational behavior, and deployment consequences. SNode.C gives IPv4 and IPv6 a similar address interface where that helps, while preserving the fact that they are different endpoint families.

\index{Unix domain sockets}
\index{net::un::SocketAddress@\texttt{net::un::SocketAddress}}
\index{path identity}

The Unix domain socket address class is:

```cpp
net::un::SocketAddress
```

Its endpoint identity is not host plus port.

It is a local socket identity, normally represented by a path-like value:

```cpp
net::un::SocketAddress local("/tmp/snodec.sock");
```

This is conceptually different from IP addressing. There is no remote internet host and no port number. The endpoint belongs to the local operating-system namespace.

Default construction uses the empty string. This is the not-yet-specific Unix-domain value in the address model. It is not the equivalent of a server listening on every IP interface. Before using a pathname listener, give it a concrete path and consider the containing directory's permissions and cleanup policy. The section “Unix domain sockets” distinguishes pathname and abstract-namespace behavior.

\index{RFCOMM}
\index{Bluetooth!RFCOMM}
\index{channel}

The RFCOMM address class is:

```cpp
net::rc::SocketAddress
```

A concrete remote endpoint may look like this:

```cpp
net::rc::SocketAddress remote("00:11:22:33:44:55", 3);
```

The Bluetooth address identifies the device. The RFCOMM channel selects the service within the RFCOMM family. The channel should not just be translated into “a Bluetooth port number.” That wording would pull the reader back into IP vocabulary. A channel is the service selector used by RFCOMM.

\index{L2CAP}
\index{Bluetooth!L2CAP}
\index{PSM}

The L2CAP address class is:

```cpp
net::l2::SocketAddress
```

A concrete remote endpoint may look like this:

```cpp
net::l2::SocketAddress remote("00:11:22:33:44:55", 0x1001);
```

The Bluetooth address again identifies the device. The PSM identifies the L2CAP service endpoint.

### Defaults, construction, and observation

\index{wildcard address}
\index{default construction}

Default construction is meaningful. It is not uninitialized data.

The initial endpoint descriptions differ by family. Wildcard bind identities and configured field strings must be distinguished:

| Family | Default value |
|---|---|
| IPv4 | `0.0.0.0`, port `0` |
| IPv6 | `::`, port `0` |
| Unix domain sockets | empty string |
| RFCOMM | unspecified device, channel `0` |
| L2CAP | unspecified device, PSM `0` |

For Bluetooth, `getBtAddress()` initially returns an empty configured string; an explicit `00:00:00:00:00:00` denotes the wildcard device address. Neither supplies a discovered remote service. Constructors reveal what each family considers natural.

Port-only construction makes sense for IPv4 and IPv6 because a server often listens on a service port without caring which local interface receives the connection.

Path construction makes sense for Unix domain sockets because the path is the local endpoint identity.

Channel construction makes sense for RFCOMM because an RFCOMM service can be described by a channel while the Bluetooth address remains wildcarded.

PSM construction makes sense for L2CAP for the same reason, but in L2CAP vocabulary.

Full constructors express a fully specified peer or an explicitly specified local endpoint:

```cpp
net::in::SocketAddress ip4("127.0.0.1", 8080);
net::in6::SocketAddress ip6("::1", 8080);
net::un::SocketAddress unixAddress("/tmp/snodec.sock");
net::rc::SocketAddress rfcommAddress("00:11:22:33:44:55", 3);
net::l2::SocketAddress l2capAddress("00:11:22:33:44:55", 0x1001);
```

The fields remain available through family-specific operations such as:

```cpp
setHost(...)
setPort(...)
setSunPath(...)
setBtAddress(...)
setChannel(...)
setPsm(...)
```

This helps when changing carriers: a port assignment cannot simply become a Unix path assignment, and a channel choice does not establish a valid PSM. Revisit the endpoint's meaning as well as the setter's spelling.

All concrete classes render their addresses for startup logging, callbacks and diagnostics. Compare the requested identity with the actual endpoint before attributing a failure to the protocol.

Try classifying three values before using them: `0.0.0.0:0` for a local IPv4 bind, `127.0.0.1:8080` for a remote IPv4 peer, and `/tmp/snodec.sock` for a local pathname service. The first asks the operating system to select a port; the second names a destination in the current host's loopback network; the third depends on the local filesystem namespace. None of those meanings comes from the text alone without its family and local/remote role.

Chapter 7 adds a useful observation: compare the requested bind address with the actual local address on an established connection. A broad configuration can produce a concrete endpoint. That is why logging only the configured value can leave a connection problem unexplained.

\index{address resolution}
\index{DNS}

The IP address classes additionally expose resolution-oriented API pieces:

- `Hints`,
- `useNext()`,
- canonical-name access.

A hostname can produce several candidates; the address abstraction allows iteration through them.

That distinction also prevents a false generalization. Unix domain sockets, RFCOMM, and L2CAP do not need to mimic IP name resolution merely to fit a common abstract shape. They keep the address model appropriate to their own family.

### IPv4 and IPv6 {#ipv4-and-ipv6-as-the-first-concrete-network-families}

\index{IPv4}
\index{IPv6}
\index{network families}

Use the comparison to hold protocol behavior fixed while changing the endpoint family. A successful exchange on each loopback address will test that claim more directly than two similar type names. A failure on one family will then be a reason to inspect that family's binding and reachability, before changing the shared protocol.

\index{IPv4!shared model}
\index{IPv6!shared model}
\index{server/client/context model}

Keep the factory and context files unchanged for the first comparison. The entry points select the family and endpoint; the context still receives bytes through the connection surface. If the change requires editing command parsing or byte reflection, inspect why the protocol acquired an address-family dependency before proceeding.

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

`net::in` selects IPv4 and `net::in6` selects IPv6. The factory and connection variant stay fixed in this comparison.

\index{net::in::SocketAddress@\texttt{net::in::SocketAddress}}
\index{net::in6::SocketAddress@\texttt{net::in6::SocketAddress}}

### Convenience calls configure the endpoint

The stream wrappers make the shared model especially visible.

For both IP families, the convenience overloads set endpoint configuration before delegating: server `listen(...)` calls set the local host, port, and backlog; client `connect(...)` calls set the remote host and port, with optional local bind information. The general paths are `listen(onStatus)` and `connect(onStatus)`, respectively.

So the convenience API is not a separate communication model. It configures the handle and then enters the same registration path that Chapter 7 will examine.

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

### Protocol reuse and separate family observations

When comparing the two families, ask: does the same protocol produce the same bytes and preserve separate state for each peer? Similar declarations establish where reuse is possible; those observations establish whether the selected composition actually behaves as intended.

If the application protocol is written in a `SocketContext`, it does not automatically become an “IPv4 protocol” or an “IPv6 protocol.” It is application behavior carried over a lower family. The same context class can often be reused when the protocol behavior does not inspect or depend on family-specific address details.

IPv4 and IPv6 roles can participate in the same event runtime. Giving them separate instance names makes their configuration and diagnostics distinguishable even when they use one factory/context design. That is useful for a service that deliberately exposes two family-specific listeners: shared protocol behavior does not require one shared listening policy or one ambiguous operational name.

Status callbacks report activation attempts; connection callbacks observe peers; context methods implement protocol behavior. Chapter 7 develops those distinctions.

The first useful comparison is an observed exchange. Run the same context once over an IPv4 loopback endpoint and once over an IPv6 loopback endpoint. The payload and context callbacks should remain the same; the address type, formatted endpoint, and operating-system family differ. A successful IPv4 run does not establish IPv6 availability, and an IPv6 wildcard listener should not be assumed to replace a separately configured IPv4 role on every platform. The family-specific component tests keep those exchanges separate for exactly this reason.

\index{address family}
\index{wildcard form}

The address class changes too:

```cpp
net::in::SocketAddress
net::in6::SocketAddress
```

The address forms differ while the wildcard-port value stays the same:

| Family | Loopback host | Wildcard host | Wildcard port |
|---|---|---|---|
| IPv4 | `127.0.0.1` | `0.0.0.0` | `0` |
| IPv6 | `::1` | `::` | `0` |

### Choosing a dual-stack policy

\index{IPv6!IPv6-only}
\index{IPv6!IPv4-mapped addresses}
\index{dual-stack deployment}

IPv6 introduces one additional technical point: deployment can involve IPv6-only behavior, IPv4-mapped IPv6 addresses, or platform-specific dual-stack behavior.

There are two reasonable service designs. Separate IPv4 and IPv6 listeners make exposure and per-family failures explicit, at the cost of maintaining two endpoint configurations. A deliberately configured dual-stack listener can reduce that duplication, but the application must establish the platform's mapping and bind behavior and interpret mapped peer addresses consistently. Merely choosing an IPv6 wildcard value does not document that policy.

### An IPv4/IPv6 comparison

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

The IPv6 version follows the same shape:

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

\index{public headers}
\index{net::in::stream::legacy@\texttt{net::in::stream::legacy}}
\index{net::in6::stream::legacy@\texttt{net::in6::stream::legacy}}

IPv4 and IPv6 are the simplest place to see the source/build pairing. A file that directly names an IPv4 legacy stream role uses the IPv4 public role headers:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

with the matching component:

`net-in-stream-legacy`.

The IPv6 variant changes only the family fragment:

```cpp
#include <net/in6/stream/legacy/SocketServer.h>
#include <net/in6/stream/legacy/SocketClient.h>
```

with the corresponding component:

`net-in6-stream-legacy`.

The local point is the family selection. Chapter 25 gives the consolidated include/component matrix.

### Unix domain sockets {#unix-domain-sockets}

\index{Unix domain sockets}
\index{local IPC}
\index{path identity}

The factory and context still describe a stream protocol. The new responsibility is the local rendezvous point: the process must bind a usable path, clients must reach that same namespace, and the service must respect ownership and cleanup of the path. A working context does not resolve any of those deployment questions by itself.

\index{Unix domain sockets!SNode.C model}
\index{endpoint identity}

\index{net::un::SocketAddress@\texttt{net::un::SocketAddress}}
\index{path identity}

The Unix-domain address class is:

```cpp
net::un::SocketAddress
```

The Unix-domain class stores a path and the corresponding socket-address structure. It provides constructors for a default value, a path, or an existing socket address, plus initialization, `setSunPath(...)`, `getSunPath()` and string rendering. There is no host resolver or remote IP candidate list.

In application code this may appear as:

```cpp
net::un::SocketAddress address("/tmp/my-service.sock");
```

The path is the name through which local processes identify the communication endpoint. In practice, it acts as a rendezvous name inside the local operating-system environment: one side creates or binds that endpoint identity, and the other side uses the same identity to reach the service.

Default construction is meaningful in the Unix-domain address model.

The default address has not yet been given a concrete service path. Do not infer from the word *wildcard* that an empty Unix-domain path listens on every pathname in the way an IP wildcard covers local interfaces. The pathname examples in this chapter require an explicit rendezvous name.

There is also a distinction between a pathname and a socket address whose first path byte is zero. The source's `toString()` renders that second form with a leading `@`, a notation associated with the Linux abstract namespace. That rendering is not an input conversion rule: `setSunPath()` stores the supplied string, and `init()` copies its bytes. Do not turn a diagnostic `@name` into a pathname configuration without checking the address representation. The worked applications here use ordinary pathname sockets, whose directory access and cleanup can be inspected directly.

Unix-domain sockets serve local process boundaries: helper daemons, internal APIs, and embedded services that need no network exposure. Ask which process owns the path, which peers can reach its namespace, and who may connect. Those local-service questions replace routing and firewall questions; they do not replace protocol validation.

### Listening and connecting by path

\index{Unix domain sockets!server/client use}
\index{listen()@\texttt{listen()}}
\index{connect()@\texttt{connect()}}

The stream Unix-domain wrappers follow the same SNode.C pattern as the IPv4 and IPv6 wrappers.

The convenience calls set family-specific configuration and then delegate to the general `listen(onStatus)` or `connect(onStatus)` path.

A Unix-domain stream server typically looks like this in outline:

```cpp
using LocalServer = net::un::stream::legacy::SocketServer<MyFactory>;

LocalServer server("local-service");
server.listen("/tmp/my-service.sock", 5, onStatus);
```

The visible `LocalServer` object is the handle. The `listen(...)` call configures the server-side path and starts a listening flow for that endpoint through the usual runtime path.

The server-side convenience overloads are path-centered:

| Surface call | Configuration effect |
|---|---|
| `listen(sunPath, ...)` | `Local::setSunPath(sunPath)` |
| `listen(sunPath, backlog, ...)` | `Local::setSunPath(sunPath)` + backlog |

A Unix-domain stream client has the same overall shape:

```cpp
using LocalClient = net::un::stream::legacy::SocketClient<MyFactory>;

LocalClient client("local-client");
client.connect("/tmp/my-service.sock", onStatus);
```

Here the visible `LocalClient` object is again the handle. The `connect(...)` call configures the remote Unix-domain service path and creates its connecting flow through the usual runtime path.

If the client also needs an explicit local bind path, the call can express that too:

```cpp
client.connect("/tmp/my-service.sock", "/tmp/my-client.sock", onStatus);
```

The client-side convenience overloads are also path-centered:

| Surface call | Configuration effect |
|---|---|
| `connect(sunPath, ...)` | `Remote::setSunPath(sunPath)` |
| `connect(sunPath, bindSunPath, ...)` | `Remote::setSunPath(sunPath)` + `Local::setSunPath(bindSunPath)` |

This keeps the local/remote distinction visible. The remote path is the service endpoint the client wants to reach.

The optional local path describes the client's own local endpoint identity. Most simple clients do not need to spell this out, but the overload exists because the model still distinguishes the peer being contacted from the local endpoint used for the connection.

For a server the path names its listener; for a client it names the service, with an optional separate local bind path.

Chapter 7 develops this connection model in detail.

A connection can still have bind, local, and remote address views. The address family has changed, but directional endpoint thinking remains useful. This is one of the main reasons to keep the address family visible in the type system: it prevents the local/remote distinction from being flattened into an unhelpful generic string.

A pathname socket also has a filesystem lifecycle. The current physical Unix-domain implementation checks the path before binding and keeps cleanup tied to the endpoint it owns. A regular file at the requested pathname is not disposable socket state. When a local service fails to start, distinguish an occupied live socket, a stale socket pathname, a non-socket file, and insufficient directory permissions before deciding what to remove. The source test `UnixPhysicalSocketPathSafetyTest` exercises this boundary; unconditional deletion in application startup would bypass it.

\index{Unix domain sockets!stable model}
\index{SocketContext@\texttt{SocketContext}}

A `SocketContext` implementing a small request/response or streaming protocol does not need to become fundamentally Unix-domain-specific just because it runs over:

```cpp
net::un::stream::legacy
```

The line parser, command responses, and per-peer receive buffer can remain unchanged. Authorization deserves a separate review, however: a rule based on an IP peer address cannot automatically become a rule based on local user identity. The credential query later in this chapter supplies facts for such a policy; it does not choose the policy.

Chapter 4 introduced `legacy` and `tls` as connection-layer variants. Unix domain sockets fit into that same layer story.

The `net::un` family supports the same stream connection-layer choice where those components are available. Locality does not select a security policy automatically.

### Path ownership and deployment

\index{Unix domain sockets!deployment}
\index{path cleanup}
\index{path ownership}

When an endpoint is identified by a path, responsible design includes path lifecycle thinking.

An application should be clear about:

- where the socket path is placed,
- which process creates it,
- which process is allowed to use it,
- what permissions or ownership expectations belong to the path,
- what happens when the service stops,
- what happens if an old path is left behind.

A temporary, runtime, or service-specific directory communicates different ownership and access expectations. The path is part of the service design.

Loopback IP is also a credible choice for communication on one machine. It may fit existing HTTP tools or a service expected to move onto another host later. A pathname socket makes a local service boundary and filesystem placement explicit and can support peer-credential policy, but processes in different filesystem namespaces must be given access to the same endpoint. Choose from those requirements rather than assuming that locality alone decides the family.

### Peer credentials are facts, not authorization

\index{Unix-domain sockets!peer credentials}
\index{PeerCredentials@\texttt{PeerCredentials}}

A pathname selects a local endpoint, but it does not by itself express an application's trust decision. SNode.C provides a separate credential query for a connected Unix-domain socket:

```cpp
#include <net/un/PeerCredentials.h>

const net::un::PeerCredentials peer = net::un::peerCredentials(fd);
if (peer.status == net::un::PeerCredentialsStatus::Success) {
    // Apply the application's policy to peer.uid and peer.gid.
}
```

Here `fd` is an already available connected Unix-domain socket descriptor. The function does not open a connection or authenticate an application protocol. A successful result provides peer user and group facts; the optional process identifier is available on Linux and is not supplied by the `getpeereid()` path used on supported BSD/macOS targets.

Check the status before using the fields. `Unsupported` means that the platform query is unavailable. `Error` means that the query failed and the result carries an error number. Neither case should be read as a successful credential check with default-valued identifiers.

A same-user rule, a service-account rule, and a command-specific authorization rule are different application policies. The framework does not choose one merely because the peer is local. Tests for the credential query and socket-path handling protect transport facts; the application's trust policy needs its own tests.

\index{datagram sockets}
\index{stream sockets}

This chapter focuses on stream Unix domain sockets. That keeps the connection and protocol model established in the preceding chapters available while endpoint identity changes.

The SNode.C build also contains a `net-un-dgram` component, but datagram communication introduces a different communication shape and should not distract from the stream-based role model being developed in Chapters 6–8.

\index{net::un::stream::legacy@\texttt{net::un::stream::legacy}}
\index{public headers}

Unix-domain legacy stream roles use the `un` family fragment on both public surfaces. Source files that directly name those roles include:

```cpp
#include <net/un/stream/legacy/SocketServer.h>
#include <net/un/stream/legacy/SocketClient.h>
```

and link the matching component:

`net-un-stream-legacy`.

Chapter 25 collects the include/component matrix. The public family lab holds EchoPair’s context and factory fixed while comparing IPv4, IPv6 and a temporary Unix path. It checks returned bytes, actual local/remote identities, and cleanup before the Part checkpoint chooses a carrier for a local measurement producer.

::: {.snodec-remember title="What to remember"}
- Socket addresses belong to the network layer: they describe endpoint identity for a selected family.
- SNode.C uses a shared address pattern, but each supported family keeps its own concrete `SocketAddress` type.
- Unix-domain addresses name local rendezvous points; pathname cleanup, directory permissions, and peer credentials need separate decisions.
- IPv4/IPv6 differences appear mainly in endpoint identity, resolution, wildcard forms, and deployment assumptions, not in a new application architecture.
- `connect(sunPath, bindSunPath, ...)` keeps the local/remote distinction visible even though both endpoints are path-based.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Compare `0.0.0.0:0`, an empty Unix path, and a zero Bluetooth selector. Which is usable for the proposed local bind, and what must a remote client still learn?
2. **Review (O3).** A Unix credential query returns `Unsupported`. Explain why neither a reachable pathname nor default-valued user/group fields can replace an authorization decision.
3. **Lab (O1, O2).** Build the IP-family lab. Send the same measurement-shaped bytes over IPv4 and IPv6 loopback. Expect exact reflection and family-specific local/remote identities; identify which endpoint the operating system selected for the producer.
4. **Lab (O3).** Build the Unix-path lab in a private temporary directory. Expect exact reflection, a named producer and service, removal of the server-owned path after shutdown, and an untouched unrelated file. Explain who removes the producer path.
5. **Design (O1, O2, O3).** Choose between loopback IP and a pathname socket for a local measurement producer that may later move to another host. Justify reachability, exposure, discovery, credentials, and cleanup without changing the protocol.

Public answers, commands, and observations: `companion/exercises/ch06/README.md`.
:::
