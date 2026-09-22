## Unix Domain Sockets

\index{Unix domain sockets}
\index{local IPC}
\index{path identity}


### From host-plus-port to local path identity

A Unix-domain endpoint moves the conversation from network reachability to local IPC.

Unix-domain sockets keep the same SNode.C runtime model, but change endpoint identity more strongly:

```text
host + port
  -> local Unix-domain path
```

That is the next controlled variation in Part III.

With IPv4 and IPv6, an endpoint is described by an address and a port. With Unix domain sockets, an endpoint is described primarily by a local path. The endpoint no longer looks like an internet endpoint at all. It is a local interprocess-communication identity.

The factory and context still describe a stream protocol. The new responsibility is the local rendezvous point: the process must bind a usable path, clients must reach that same namespace, and the service must respect ownership and cleanup of the path. A working context does not resolve any of those deployment questions by itself.

### Same SNode.C model, different endpoint identity

\index{Unix domain sockets!SNode.C model}
\index{endpoint identity}


The transition from IPv4/IPv6 to Unix domain sockets can be summarized as follows.

| Aspect | IPv4 / IPv6 | Unix domain sockets |
|---|---|---|
| Namespace | `net::in`, `net::in6` | `net::un` |
| Endpoint identity | host + port | local path |
| Server bind value | local host + port | local socket path |
| Client target | remote host + port | remote socket path |
| Optional local bind | local host and/or port | local socket path |
| Runtime model | stable | stable |
| Server/client role model | stable | stable |
| Context/factory model | stable | stable |

The key point is the controlled change. The lower family changes. The endpoint identity changes.

The application architecture is preserved.

The table should therefore be read as a transfer map, not as a feature comparison. It shows which ideas move unchanged into the Unix-domain family and which words must be reinterpreted once endpoint identity becomes path-based.

This is the same teaching pattern as in Chapter 10, but the shift is stronger. IPv4 and IPv6 were different internet families with a similar host-plus-port shape. Unix domain sockets change the addressing category itself.

### Path identity in `net::un::SocketAddress`

\index{net::un::SocketAddress@\texttt{net::un::SocketAddress}}
\index{path identity}


The Unix-domain address class is:

```cpp
net::un::SocketAddress
```

Its surface is smaller than the IPv4 and IPv6 address classes because the endpoint identity is smaller. There is no host name to resolve, no internet port number, and no candidate list of remote network addresses. The address object represents a Unix-domain path and the socket-address structure built from it.

Its conceptual surface includes:

- default construction,
- construction from a `sunPath`,
- construction from an existing Unix-domain `sockaddr`,
- initialization,
- `setSunPath(...)` and `getSunPath()`,
- and string rendering.

This surface reflects the family.

A Unix-domain endpoint is a local IPC endpoint identified primarily by a path, not a host with a strange name.

#### Path as endpoint identity

When using Unix domain sockets, the path should be understood as endpoint identity in the local IPC space.

A typical endpoint may look like:

```text
/tmp/my-service.sock
```

In application code this may appear as:

```cpp
net::un::SocketAddress address("/tmp/my-service.sock");
```

The path is the name through which local processes identify the communication endpoint. In practice, it acts as a rendezvous name inside the local operating-system environment: one side creates or binds that endpoint identity, and the other side uses the same identity to reach the service.

This avoids two common wrong instincts:

- treating Unix domain sockets as IP sockets without a network,
- or treating the socket path as an ordinary file with no communication semantics.

The better view is:

```text
path
  -> local endpoint identity
      -> stream communication endpoint
```

That is why Unix domain sockets belong in this part of the book. They are not a new application protocol. They are a different lower-family endpoint model under the same SNode.C stream architecture.

#### Default construction and empty path

Default construction is meaningful in the Unix-domain address model.

The default address has not yet been given a concrete service path. Do not infer from the word *wildcard* that an empty Unix-domain path listens on every pathname in the way an IP wildcard covers local interfaces. The pathname examples in this chapter require an explicit rendezvous name.

There is also a distinction between a pathname and a socket address whose first path byte is zero. The source's `toString()` renders that second form with a leading `@`, a notation associated with the Linux abstract namespace. That rendering is not an input conversion rule: `setSunPath()` stores the supplied string, and `init()` copies its bytes. Do not turn a diagnostic `@name` into a pathname configuration without checking the address representation. The worked applications here use ordinary pathname sockets, whose directory access and cleanup can be inspected directly.

#### Locality as the defining idea

A Unix domain socket is local interprocess communication. It is not used to reach a peer on another machine over an IP network. This changes the deployment questions.

With IPv4 or IPv6 one often asks:

- Which interface should listen?
- Which port should be exposed?
- Which remote host should be contacted?
- Which firewall or routing rule might be involved?

With Unix domain sockets one more often asks:

- Which local path represents this service?
- Which local processes are allowed to connect?
- Where does this endpoint belong in the local service layout?
- Who owns the lifecycle of that path?
- What happens if an old path is left behind?

Unix domain sockets are therefore especially useful for:

- local service boundaries,
- helper daemons,
- internal process-to-process APIs,
- development setups where network exposure is unnecessary,
- appliance-like or embedded systems where components communicate locally.

The lower-family choice is not decorative. It changes the operational shape of the system. The code can keep the same server/client outline, but the questions a developer asks while deploying and diagnosing the application become local-service questions rather than network-reachability questions.

### Server and client use with path-based endpoints

\index{Unix domain sockets!server/client use}
\index{listen()@\texttt{listen()}}
\index{connect()@\texttt{connect()}}


The stream Unix-domain wrappers follow the same SNode.C pattern as the IPv4 and IPv6 wrappers.

The convenience calls set family-specific configuration and then delegate to the general `listen(onStatus)` or `connect(onStatus)` path.

The difference is that the configured value is now a Unix-domain path. That keeps the application code pleasantly familiar while still making the lower-family decision explicit. A reader should see both sides at once: the call shape transfers, but the endpoint value has a different meaning.

#### Server-side `listen(...)`

A Unix-domain stream server typically looks like this in outline:

```cpp
using LocalServer = net::un::stream::legacy::SocketServer<MyFactory>;

LocalServer server("local-service");
server.listen("/tmp/my-service.sock", 5, onStatus);
```

The visible `LocalServer` object is the handle. The `listen(...)` call configures the server-side path and starts a listening flow for that endpoint through the usual runtime path.

The server is still a server role.

The call is still a `listen(...)` call.

The status callback still reports outer role status.

The difference is the endpoint identity:

```text
IPv4 / IPv6:
local host + local port

Unix domain:
local socket path
```

The server-side convenience overloads are path-centered:

| Surface call | Configuration effect |
|---|---|
| `listen(sunPath, ...)` | `Local::setSunPath(sunPath)` |
| `listen(sunPath, backlog, ...)` | `Local::setSunPath(sunPath)` + backlog |

This mirrors the Chapter 10 pattern. A readable convenience call configures the handle and then enters the same registration path.

#### Client-side `connect(...)`

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

#### Local and remote paths

Path-based endpoint identity does not remove the local/remote distinction. It only changes what the endpoint value looks like.

For a Unix-domain server:

```text
local path
  -> path on which the server listens
```

For a Unix-domain client:

```text
remote path
  -> service path to connect to

optional local path
  -> explicit local endpoint for the client side
```

This continues Chapter 9's connection model.

A connection can still have bind, local, and remote address views. The address family has changed, but directional endpoint thinking remains useful. This is one of the main reasons to keep the address family visible in the type system: it prevents the local/remote distinction from being flattened into an unhelpful generic string.

A pathname socket also has a filesystem lifecycle. The current physical Unix-domain implementation checks the path before binding and keeps cleanup tied to the endpoint it owns. A regular file at the requested pathname is not disposable socket state. When a local service fails to start, distinguish an occupied live socket, a stale socket pathname, a non-socket file, and insufficient directory permissions before deciding what to remove. The source test `UnixPhysicalSocketPathSafetyTest` exercises this boundary; unconditional deletion in application startup would bypass it.

### What remains stable

\index{Unix domain sockets!stable model}
\index{SocketContext@\texttt{SocketContext}}


Unix domain sockets change endpoint identity, but they do not require a different application architecture.

#### Server/client/connection/context model

The same core model remains:

| Concept | Meaning with Unix domain sockets |
|---|---|
| Application-side `SocketServer` handle | configures and registers a server-side instance |
| Application-side `SocketClient` handle | configures and registers a client-side instance |
| Registered instance | runtime-visible server/client role using `net::un` endpoint semantics |
| `SocketConnection` | one concrete peer relationship |
| `SocketContextFactory` | creates a context for a connection |
| `SocketContext` | implements protocol behavior |

The server-side instance is still the listening role. The client-side instance is still the connecting role. The connection is still the concrete peer relationship.

The context is still the protocol endpoint attached to that connection.

Therefore, moving from IPv4 to Unix domain sockets should not feel like moving to a different framework. The lower family has changed, not the architecture. For application developers this is an important payoff: once the instance, connection, factory, and context boundaries are understood, a new endpoint family does not force the whole program shape to be relearned.

#### Context and protocol logic

A `SocketContext` implementing a small request/response or streaming protocol does not need to become fundamentally Unix-domain-specific just because it runs over:

```cpp
net::un::stream::legacy
```

The line parser, command responses, and per-peer receive buffer can remain unchanged. Authorization deserves a separate review, however: a rule based on an IP peer address cannot automatically become a rule based on local user identity. The credential query later in this chapter supplies facts for such a policy; it does not choose the policy.

The protocol context may inspect the address if it wants to log or display endpoint information. But the protocol logic itself can often remain the same. This is the separation the book is building toward: lower layers decide how peers are reached, while the context concentrates on what the application protocol does once a connection exists.

#### Legacy and TLS

Chapter 7 introduced `legacy` and `tls` as connection-layer variants. Unix domain sockets fit into that same layer story.

A Unix-domain stream component can participate in the pattern:

```text
net::un
  -> stream
      -> legacy or TLS
```

Here `legacy` is the non-TLS stream connection variant. `tls` adds TLS connection handling.

Unix domain sockets are not a special branch outside the framework. In SNode.C's terminology, they are another lower family in the network-layer part of the stack, while stream transport and connection-layer handling remain recognizable.

### What changes operationally

\index{Unix domain sockets!deployment}
\index{path cleanup}
\index{path ownership}


Unix domain sockets are local, path-based endpoints. That changes deployment habits.

#### Deployment habits

With IP sockets, operational thinking often starts with:

```text
address
port
interface
network reachability
```

With Unix domain sockets, operational thinking starts with:

```text
local path
local process boundary
local access expectations
path ownership
path cleanup
```

That is a real design difference.

Unix domain sockets are often the right choice when the communication should stay inside one machine. They are not the right choice when the peer must be reached over a network.

SNode.C makes that family choice explicit instead of hiding it behind one generic endpoint abstraction. That explicitness is useful during design reviews as well as during debugging: the namespace and address type already tell the reader that this is local IPC, not a network-facing endpoint.

#### Path ownership and cleanup thinking

When an endpoint is identified by a path, responsible design includes path lifecycle thinking.

An application should be clear about:

- where the socket path is placed,
- which process creates it,
- which process is allowed to use it,
- what permissions or ownership expectations belong to the path,
- what happens when the service stops,
- what happens if an old path is left behind.

This does not mean Unix domain sockets are complicated.

It means the family expresses locality through path identity, and application design should respect that. A path under a temporary directory, a runtime directory, or a service-specific directory communicates different operational expectations. The path is part of the service design, not an incidental string literal.

#### Unix domain sockets are not a replacement for IP

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

The architectural boundary is deliberate:

```text
transport query
  -> reports peer facts

application policy
  -> decides whether those facts authorize an operation
```

A same-user rule, a service-account rule, and a command-specific authorization rule are different application policies. The framework does not choose one merely because the peer is local. Tests for the credential query and socket-path handling protect transport facts; the application's trust policy needs its own tests.

### Stream focus and a datagram note

\index{datagram sockets}
\index{stream sockets}


This chapter focuses on stream Unix domain sockets. That keeps the connection and protocol model established in the preceding chapters available while endpoint identity changes.

The SNode.C build also contains a `net-un-dgram` component, but datagram communication introduces a different communication shape and should not distract from the stream-based role model being developed in Chapters 8--12.

The practical lesson is simple: Unix domain sockets are not limited to one possible socket style, but this chapter follows the stream path because the book is still building the layered server/client/connection model.

### Preparing the Bluetooth shift

Unix domain sockets are also a useful bridge to Bluetooth. IPv4 and IPv6 showed host-plus-port endpoint identity. Unix domain sockets showed path-based local endpoint identity.

Bluetooth will introduce endpoint identities that are different again:

```text
Bluetooth address + RFCOMM channel
Bluetooth address + L2CAP PSM
```

After Chapter 11, the reader has seen two kinds of endpoint shift: internet host-plus-port identity and local path identity. Chapter 12 adds device address plus service selector.

The server/client/connection/context model remains available, while the lower-family address semantics change again. That prepares the next chapter: Bluetooth should not feel like an exception to the architecture, but like another controlled variation in endpoint identity.

::: {.snodec-remember title="What to remember"}
- Unix domain sockets replace host-plus-port endpoint identity with local path identity.
- `net::un` selects the Unix-domain family, and `net::un::SocketAddress` represents the path-based endpoint.
- The path-based endpoint changes configuration and deployment concerns while preserving the server/client construction path.
- `listen(sunPath, ...)` configures the server's local Unix-domain path; `connect(sunPath, ...)` configures the client's remote Unix-domain service path.
- `connect(sunPath, bindSunPath, ...)` keeps the local/remote distinction visible even though both endpoints are path-based.
- An empty Unix-domain path is a deferred value, not a general promise of wildcard listening; pathname services need an explicit path and lifecycle policy.
:::

### Public surface of Unix-domain stream roles

\index{net::un::stream::legacy@\texttt{net::un::stream::legacy}}
\index{public headers}


Unix-domain legacy stream roles use the `un` family fragment on both public surfaces. Source files that directly name those roles include:

```cpp
#include <net/un/stream/legacy/SocketServer.h>
#include <net/un/stream/legacy/SocketClient.h>
```

and link the matching component:

```text
net-un-stream-legacy
```

The same include/component rule from the primary families applies; only the family fragment changes. The consolidated mapping is collected in Chapter 32.
