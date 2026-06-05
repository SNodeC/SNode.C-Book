## Unix Domain Sockets

### From host-plus-port to local path identity

Chapter 10 compared IPv4 and IPv6 as two host-plus-port families.

This chapter keeps the same SNode.C server/client/connection model but changes the endpoint identity:

```text
host + port
  -> local Unix-domain path
```

That is a significant lower-family shift.

With IPv4 and IPv6, an endpoint is described by an address and a port. With Unix domain sockets, an endpoint is described primarily by a local path.

The larger SNode.C model remains recognizable:

- a server or client instance,
- a socket-context factory,
- a socket context,
- a concrete connection,
- runtime integration,
- status callbacks,
- connection lifecycle callbacks,
- and the same broad stream-based communication story.

This shows that SNode.C's role model is not tied to host-plus-port addressing.

### Same model, different endpoint identity

The transition from IPv4/IPv6 to Unix domain sockets can be summarized as follows.

| Aspect | IPv4 / IPv6 | Unix domain sockets |
|---|---|---|
| Namespace | `net::in`, `net::in6` | `net::un` |
| Endpoint identity | host + port | local path |
| Server bind value | local host + port | local socket path |
| Client target | remote host + port | remote socket path |
| Optional local bind | local host and/or port | local socket path |
| Runtime model | same | same |
| Server/client role model | same | same |
| Context/factory model | same | same |

The key point is the controlled change.

The lower communication family changes.

The endpoint identity changes.

The application architecture does not need to be reinvented.

### The Unix-domain address model

The Unix-domain address class is:

```cpp
net::un::SocketAddress
```

It is intentionally simpler than the IPv4 and IPv6 address classes.

Its conceptual surface includes:

- default construction,
- construction from a `sunPath`,
- construction from an existing Unix-domain `sockaddr`,
- initialization,
- `setSunPath(...)` and `getSunPath()`,
- and string rendering.

This simpler surface reflects the family.

A Unix-domain endpoint is not a host with a strange name. It is a local IPC endpoint identified primarily by a path.

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

The path is not merely a filename in the everyday document sense. It is the name through which local processes identify the communication endpoint.

This avoids two common wrong instincts:

- treating Unix domain sockets as IP sockets without a network,
- or treating the socket path as an ordinary file with no communication semantics.

The better view is:

```text
path
  -> local endpoint identity
      -> stream communication endpoint
```

#### Default construction and empty path

Default construction is meaningful in the Unix-domain address model.

In the terminology used in Chapter 8, an empty Unix-domain path acts as the wildcard or deferred endpoint indicator.

That gives SNode.C a way to represent an address object whose concrete path has not yet been made specific.

The important point is not to turn this into a long operating-system detour. The important point is consistency:

| Family | Default / wildcard shape |
|---|---|
| IPv4 | `0.0.0.0`, port `0` |
| IPv6 | `::`, port `0` |
| Unix domain sockets | empty path |

The wildcard idea transfers.

The concrete representation changes.

#### Locality as the defining idea

A Unix domain socket is local interprocess communication.

It is not used to reach a peer on another machine over an IP network.

This changes the deployment questions.

With IPv4 or IPv6 one often asks:

- Which interface should listen?
- Which port should be exposed?
- Which remote host should be contacted?

With Unix domain sockets one more often asks:

- Which local path represents this service?
- Which local processes are allowed to connect?
- Where does this endpoint belong in the local service layout?
- Who owns the lifecycle of that path?

Unix domain sockets are therefore especially useful for:

- local service boundaries,
- helper daemons,
- internal process-to-process APIs,
- development setups where network exposure is unnecessary,
- appliance-like or embedded systems where components communicate locally.

The lower-family choice is not decorative. It changes the operational shape of the system.

### Server and client use

The stream Unix-domain wrappers follow the same SNode.C pattern as the IPv4 and IPv6 wrappers.

The convenience calls set family-specific configuration and then delegate to the general `listen(onStatus)` or `connect(onStatus)` path.

The difference is that the configured value is now a Unix-domain path.

#### Server-side `listen(...)`

A Unix-domain stream server typically looks like this in outline:

```cpp
using LocalServer = net::un::stream::legacy::SocketServer<MyFactory>;

LocalServer server("local-service");
server.listen("/tmp/my-service.sock", 5, onStatus);
```

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

This mirrors the Chapter 10 pattern.

A readable convenience call fills the instance configuration for the correct lower family and then uses the same underlying role machinery.

#### Client-side `connect(...)`

A Unix-domain stream client has the same overall shape:

```cpp
using LocalClient = net::un::stream::legacy::SocketClient<MyFactory>;

LocalClient client("local-client");
client.connect("/tmp/my-service.sock", onStatus);
```

If the client also needs an explicit local bind path, the call can express that too:

```cpp
client.connect("/tmp/my-service.sock", "/tmp/my-client.sock", onStatus);
```

The client-side convenience overloads are also path-centered:

| Surface call | Configuration effect |
|---|---|
| `connect(sunPath, ...)` | `Remote::setSunPath(sunPath)` |
| `connect(sunPath, bindSunPath, ...)` | `Remote::setSunPath(sunPath)` + `Local::setSunPath(bindSunPath)` |

This keeps the local/remote distinction visible.

The remote path is the service endpoint the client wants to reach.

The optional local path describes the client's own local endpoint identity.

#### Local and remote paths

Path-based endpoint identity does not remove the local/remote distinction.

It changes what local and remote mean.

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

A connection can still have bind, local, and remote address views. The address family has changed, but directional endpoint thinking remains useful.

### What remains stable

Unix domain sockets change endpoint identity, but they do not require a different application architecture.

#### Server/client/connection/context model

The same core roles remain:

| Role | Meaning with Unix domain sockets |
|---|---|
| `SocketServer` | listens on a local Unix-domain path |
| `SocketClient` | connects to a Unix-domain service path |
| `SocketConnection` | represents one concrete peer relationship |
| `SocketContextFactory` | creates a context for a connection |
| `SocketContext` | implements application protocol behavior |

The server is still the outer listening role.

The client is still the outer connecting role.

The connection is still the concrete peer relationship.

The context is still the protocol endpoint attached to that connection.

This is why moving from IPv4 to Unix domain sockets should not feel like moving to a different framework.

#### Context and protocol logic

A `SocketContext` implementing a small request/response or streaming protocol does not need to become fundamentally Unix-domain-specific just because it runs over:

```cpp
net::un::stream::legacy
```

What changes is the carrier.

What often remains stable is:

- how the protocol reacts to connection establishment,
- how it reads data,
- how it sends data,
- how it handles disconnection,
- how it thinks in terms of one connection and one context.

The protocol context may inspect the address if it wants to log or display endpoint information, but the protocol logic itself can often remain the same.

#### Legacy and TLS

Chapter 7 introduced `legacy` and `tls` as connection-layer variants.

Unix domain sockets fit into that same layer story.

A Unix-domain stream component can participate in the same pattern:

```text
net::un
  -> stream
      -> legacy or TLS
```

This matters because Unix domain sockets are not a special branch outside the framework.

In SNode.C's terminology, they are another lower communication family in the network-layer part of the stack, while stream transport and connection-layer handling remain recognizable.

### What changes operationally

Unix domain sockets are local, path-based endpoints.

That changes deployment habits.

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

SNode.C makes that family choice explicit instead of hiding it behind one generic endpoint abstraction.

#### Path ownership and cleanup thinking

When an endpoint is identified by a path, responsible design includes path lifecycle thinking.

An application should be clear about:

- where the socket path is placed,
- which process creates it,
- which process is allowed to use it,
- what happens when the service stops,
- what happens if an old path is left behind.

This does not mean Unix domain sockets are complicated.

It means the family expresses locality through path identity, and application design should respect that.

#### Unix domain sockets are not a replacement for IP

Unix domain sockets are not "better IP."

They are a different lower-family choice.

They are excellent when communication is local to one machine. They are not suitable when a process must communicate with a peer on another machine over a network.

The right question is therefore not:

```text
Are Unix domain sockets better than IP?
```

The better question is:

```text
Is this communication local enough that path-based IPC is the right lower family?
```

### Stream focus and a datagram note

This chapter focuses on stream Unix domain sockets.

That is intentional for architectural continuity.

Stream Unix-domain sockets preserve the server/client/connection/context model used throughout this part of the book.

The build also contains a `net-un-dgram` component. That is useful to know, but it is not the focus here. Datagram communication introduces a different communication shape and should not distract from the stream-based role model being developed in Chapters 8–12.

### Preparing the Bluetooth shift

Unix domain sockets are also a useful bridge to Bluetooth.

IPv4 and IPv6 showed host-plus-port endpoint identity.

Unix domain sockets showed path-based local endpoint identity.

Bluetooth will introduce endpoint identities that are different again:

```text
Bluetooth address + RFCOMM channel
Bluetooth address + L2CAP PSM
```

After Unix domain sockets, that shift should feel less surprising.

The server/client/connection/context model remains available, while the lower-family address semantics change again.

### What to remember

Remember:

- Unix domain sockets replace host-plus-port identity with local path identity.
- The namespace is `net::un`.
- The address class is `net::un::SocketAddress`.
- The path is the local IPC endpoint identity.
- Default construction corresponds to an empty path as wildcard or deferred endpoint identity.
- `listen(sunPath, ...)` configures the server's local Unix-domain path.
- `connect(sunPath, ...)` configures the client's remote Unix-domain service path.
- `connect(sunPath, bindSunPath, ...)` also configures the client's local path.
- Local and remote still matter, even when both are path-based.
- The server/client/connection/context model remains stable.
- Deployment thinking shifts toward local path placement, access, ownership, and cleanup.
- Unix domain sockets are a local IPC family, not a replacement for network communication.
- The next lower-family shift is Bluetooth address plus channel or PSM.

### Closing perspective

Chapter 10 showed that IPv4 and IPv6 are closely related host-plus-port families.

This chapter changed the endpoint identity to a Unix-domain path while keeping the same broad SNode.C role model.

The next chapter changes the endpoint identity again.

Bluetooth RFCOMM and L2CAP are neither host-plus-port nor path-based. They use Bluetooth device addresses together with family-specific service selectors.

That makes Bluetooth the next controlled variation in the lower-layer part of the book.
