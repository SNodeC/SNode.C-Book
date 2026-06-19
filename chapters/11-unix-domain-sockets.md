## Unix Domain Sockets

### From host-plus-port to local path identity

Chapter 10 used IPv4 and IPv6 as the first concrete lower-family comparison. Both families still used a host-plus-port endpoint identity.

This chapter keeps the same SNode.C runtime model, but changes endpoint identity more strongly:

```text
host + port
  -> local Unix-domain path
```

That is the next controlled variation in Part III.

With IPv4 and IPv6, an endpoint is described by an address and a port. With Unix domain sockets, an endpoint is described primarily by a local path. The endpoint no longer looks like an internet endpoint at all. It is a local interprocess-communication identity.

The larger SNode.C model remains recognizable:

- an application-side `SocketServer` or `SocketClient` handle,
- a registered server-side or client-side instance,
- a concrete `SocketConnection`,
- a socket-context factory,
- a per-connection socket context,
- runtime integration,
- status callbacks,
- connection lifecycle callbacks,
- and the same broad stream-based server/client/connection model.

This shows that SNode.C's role model is not tied to host-plus-port addressing. The point of the chapter is therefore not only to introduce another address class. It is to test whether the mental model from the previous chapters survives when the most familiar shape of a socket endpoint disappears.

### Same SNode.C model, different endpoint identity

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

The key point is the controlled change. The lower communication family changes. The endpoint identity changes.

The application architecture does not need to be reinvented.

The table should therefore be read as a transfer map, not as a feature comparison. It shows which ideas move unchanged into the Unix-domain family and which words must be reinterpreted once endpoint identity becomes path-based.

This is the same teaching pattern as in Chapter 10, but the shift is stronger. IPv4 and IPv6 were different internet families with a similar host-plus-port shape. Unix domain sockets change the addressing category itself.

### Path identity in `net::un::SocketAddress`

The Unix-domain address class is:

```cpp
net::un::SocketAddress
```

Its surface is intentionally smaller than the IPv4 and IPv6 address classes because the endpoint identity is smaller. There is no host name to resolve, no internet port number, and no candidate list of remote network addresses. The address object represents a Unix-domain path and the socket-address structure built from it.

Its conceptual surface includes:

- default construction,
- construction from a `sunPath`,
- construction from an existing Unix-domain `sockaddr`,
- initialization,
- `setSunPath(...)` and `getSunPath()`,
- and string rendering.

This surface reflects the family.

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

The path is not just a filename in the everyday document sense. It is the name through which local processes identify the communication endpoint. In practice, it acts as a rendezvous name inside the local operating-system environment: one side creates or binds that endpoint identity, and the other side uses the same identity to reach the service.

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

In the SNode.C address vocabulary used here, an empty Unix-domain path acts as the wildcard or deferred endpoint indicator for this family. It gives SNode.C a way to represent an address object whose concrete path has not yet been made specific.

The point is not to turn this into a long operating-system detour. The important point is consistency across families:

| Family | Default / wildcard shape |
|---|---|
| IPv4 | `0.0.0.0`, port `0` |
| IPv6 | `::`, port `0` |
| Unix domain sockets | empty path |

The wildcard idea transfers.

The concrete representation changes. This is the useful reading habit for all lower families in SNode.C: the abstract role of a default address may be comparable, but the actual meaning is always expressed in the vocabulary of the selected family.

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

The visible `LocalServer` object is the application-side handle. The `listen(...)` call configures the server-side path and registers the server-side instance through the usual runtime path.

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

This mirrors the Chapter 10 pattern. A readable convenience call configures the application-side handle and then enters the same registration path.

#### Client-side `connect(...)`

A Unix-domain stream client has the same overall shape:

```cpp
using LocalClient = net::un::stream::legacy::SocketClient<MyFactory>;

LocalClient client("local-client");
client.connect("/tmp/my-service.sock", onStatus);
```

Here the visible `LocalClient` object is again the application-side handle. The `connect(...)` call configures the remote Unix-domain service path and registers the client-side instance through the usual runtime path.

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

### What remains stable

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
| `SocketContext` | implements application protocol behavior |

The server-side instance is still the listening role. The client-side instance is still the connecting role. The connection is still the concrete peer relationship.

The context is still the protocol endpoint attached to that connection.

Therefore, moving from IPv4 to Unix domain sockets should not feel like moving to a different framework. The lower family has changed, not the architecture. For application developers this is an important payoff: once the instance, connection, factory, and context boundaries are understood, a new endpoint family does not force the whole program shape to be relearned.

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

The same context class can often be reused when the protocol behavior does not depend on family-specific address details.

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

This matters because Unix domain sockets are not a special branch outside the framework. In SNode.C's terminology, they are another lower communication family in the network-layer part of the stack, while stream transport and connection-layer handling remain recognizable.

### What changes operationally

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

It means the family expresses locality through path identity, and application design should respect that. A path under a temporary directory, a runtime directory, or a service-specific directory communicates different operational expectations. The book does not need to prescribe one layout here, but the chapter should make clear that the path is part of the service design, not an incidental string literal.

#### Unix domain sockets are not a replacement for IP

Unix domain sockets are not better or worse IP sockets. They answer a different design question.

They are excellent when communication is local to one machine. They are not suitable when a process must communicate with a peer on another machine over a network.

The right question is therefore not:

```text
Are Unix domain sockets better than IP?
```

The better question is:

```text
Is this communication local enough that path-based IPC is the right lower family?
```

This keeps the comparison architectural rather than emotional. The lower family should match the communication boundary.

### Stream focus and a datagram note

It focuses on stream Unix domain sockets. That is intentional for architectural continuity. Stream Unix-domain sockets preserve the server/client/connection/context model used throughout this part of the book.

The SNode.C build also contains a `net-un-dgram` component. That is useful to know, but it is not the focus here. Datagram communication introduces a different communication shape and should not distract from the stream-based role model being developed in Chapters 8--12.

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
- The application-side handle, registered instance, connection, factory, context, callbacks, and runtime model remain structurally familiar.
- `listen(sunPath, ...)` configures the server's local Unix-domain path; `connect(sunPath, ...)` configures the client's remote Unix-domain service path.
- `connect(sunPath, bindSunPath, ...)` keeps the local/remote distinction visible even though both endpoints are path-based.
- The empty Unix-domain path is the family's wildcard or deferred endpoint representation in the SNode.C address model.
:::

### Closing perspective

Chapter 10 showed that IPv4 and IPv6 are closely related host-plus-port families.

This chapter changed the endpoint identity to a Unix-domain path while keeping the same broad SNode.C role model.

The next chapter changes the endpoint identity again.

Bluetooth RFCOMM and L2CAP are neither host-plus-port nor path-based. They use Bluetooth device addresses together with family-specific service selectors.

That makes Bluetooth the next controlled variation in the lower-layer part of the book.
