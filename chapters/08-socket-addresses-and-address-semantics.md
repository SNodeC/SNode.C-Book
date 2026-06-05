## Socket Addresses and Address Semantics

### Why addresses deserve their own chapter

Chapter 7 showed that the network layer chooses the endpoint family.

This chapter explains what endpoint identity means inside each of those families.

When people first learn network programming, they often treat addresses as simple input values. An IP address is a string. A port is a number. A Unix domain socket is a path. A Bluetooth endpoint is a device address plus a smaller service selector.

That view is understandable, but it is too shallow for a framework like SNode.C.

In SNode.C, addresses are not incidental parameters passed into `listen(...)` and `connect(...)` and then forgotten. They are part of the framework's layer model.

The address type tells the framework and the reader what kind of endpoint identity exists at the network layer. It also shapes:

- how a server binds,
- how a client chooses a peer,
- what a wildcard endpoint means,
- what local versus remote identity means,
- what string rendering and diagnostics should look like,
- and, in the IP families, how name resolution can produce candidate endpoints.

That is why SNode.C gives each network family its own concrete `SocketAddress` type instead of pretending that all endpoints are the same thing.

### The shared `SocketAddress` pattern

SNode.C has a common template base:

```cpp
net::SocketAddress<SockAddrT>
```

That base already tells us something important: a SNode.C address is not just a string plus a number. It is backed by a concrete socket-address structure and length, and it still participates in the framework's broader socket-address abstraction.

The shared base gives the framework a common pattern, while the family-specific classes preserve the differences.

That is exactly the right architectural compromise:

> One address pattern, but no false claim that all endpoint identities mean the same thing.

### Family-specific address semantics

The concrete address families are:

| Family | Class | Endpoint identity |
|---|---|---|
| IPv4 | `net::in::SocketAddress` | host plus port |
| IPv6 | `net::in6::SocketAddress` | host plus port |
| Unix domain sockets | `net::un::SocketAddress` | local socket path |
| Bluetooth RFCOMM | `net::rc::SocketAddress` | Bluetooth address plus channel |
| Bluetooth L2CAP | `net::l2::SocketAddress` | Bluetooth address plus PSM |

This table is the concrete continuation of Chapter 7: the network layer chooses the endpoint family, and the table shows how that choice becomes C++ API.

#### IPv4: host plus port

The IPv4 address class is:

```cpp
net::in::SocketAddress
```

Its conceptual surface includes:

- default construction,
- construction from host,
- construction from port,
- construction from host plus port,
- construction from an existing `sockaddr_in`,
- `setHost(...)` and `getHost()`,
- `setPort(...)` and `getPort()`,
- canonical-name access,
- `Hints`,
- `useNext()`,
- and string rendering.

This is richer than a naive "string plus number" wrapper.

Its default host is:

```text
0.0.0.0
```

and the default port is:

```text
0
```

That means default IPv4 construction is wildcard-oriented. For a server, this naturally represents the idea of listening on the wildcard address. For a client-side local address, it can mean that the operating system may choose the local side when the connection is established.

A fully specified IPv4 remote endpoint might look like:

```cpp
net::in::SocketAddress remote("127.0.0.1", 8080);
```

A server-side wildcard port binding might be expressed as:

```cpp
net::in::SocketAddress local(8080);
```

The point is not to memorize every constructor, but to understand what each constructor expresses about endpoint identity.

#### IPv6: similar shape, different semantics

The IPv6 address class is:

```cpp
net::in6::SocketAddress
```

It has a surface very similar to the IPv4 class:

- default construction,
- construction from host,
- construction from port,
- construction from host plus port,
- construction from an existing `sockaddr_in6`,
- `setHost(...)` and `getHost()`,
- `setPort(...)` and `getPort()`,
- canonical-name access,
- `Hints`,
- `useNext()`,
- and string rendering.

That similarity is useful because it teaches the reader that IPv4 and IPv6 share a host-plus-port shape in SNode.C. But similar API does not mean identical operational semantics.

The default IPv6 host is:

```text
::
```

and the default port is:

```text
0
```

So default IPv6 construction is also wildcard-oriented.

A concrete IPv6 endpoint might look like:

```cpp
net::in6::SocketAddress remote("::1", 8080);
```

The reader should resist two opposite mistakes: treating IPv6 as completely unrelated to IPv4, or treating it as merely IPv4 with longer strings.

The better view is:

> SNode.C gives IPv4 and IPv6 a similar address interface where the similarity is useful, while preserving the fact that they are different endpoint families.

#### Unix domain sockets: local endpoint identity

The Unix domain socket address class is:

```cpp
net::un::SocketAddress
```

Its conceptual surface is simpler:

- default construction,
- construction from a socket path,
- construction from an existing `sockaddr_un`,
- initialization,
- `setSunPath(...)` and `getSunPath()`,
- and string rendering.

That simpler surface is not a weakness. It reflects the family.

A Unix domain socket endpoint is a local endpoint identity, normally represented by a path-like value:

```cpp
net::un::SocketAddress local("/tmp/snodec.sock");
```

Default construction uses an empty path string. In SNode.C's address model, that empty string acts as the wildcard indicator for Unix domain socket addressing.

This is conceptually different from IP addressing. There is no remote host plus port pair; there is a local operating-system endpoint identity. A Unix domain socket is not just another IP socket with different syntax.

That makes Unix domain sockets pedagogically useful: they break the habit of thinking that every network endpoint is internet-shaped.

#### RFCOMM: Bluetooth address plus channel

The RFCOMM address class is:

```cpp
net::rc::SocketAddress
```

Its conceptual surface includes:

- default construction,
- construction from Bluetooth address,
- construction from channel,
- construction from Bluetooth address plus channel,
- construction from an existing `sockaddr_rc`,
- initialization,
- `setBtAddress(...)` and `getBtAddress()`,
- `setChannel(...)` and `getChannel()`,
- and string rendering.

An RFCOMM endpoint is not host plus port. It is better understood as:

```text
Bluetooth device address
  + RFCOMM channel
```

For example:

```cpp
net::rc::SocketAddress remote("00:11:22:33:44:55", 3);
```

Default construction uses the wildcard Bluetooth address conceptually represented as:

```text
00:00:00:00:00:00
```

with channel `0` until a more specific channel is configured.

The channel should not simply be described as "a Bluetooth port number." It is a service selector inside the RFCOMM communication family.

That distinction matters because it keeps the reader from translating every endpoint model back into IP vocabulary. A Bluetooth RFCOMM address is not an IP-style address with different formatting; it belongs to a different endpoint family.

#### L2CAP: Bluetooth address plus PSM

The L2CAP address class is:

```cpp
net::l2::SocketAddress
```

It mirrors the RFCOMM pattern closely, but with a different service selector:

- default construction,
- construction from Bluetooth address,
- construction from PSM,
- construction from Bluetooth address plus PSM,
- construction from an existing `sockaddr_l2`,
- initialization,
- `setBtAddress(...)` and `getBtAddress()`,
- `setPsm(...)` and `getPsm()`,
- and string rendering.

An L2CAP endpoint is:

```text
Bluetooth device address
  + PSM
```

For example:

```cpp
net::l2::SocketAddress remote("00:11:22:33:44:55", 0x1001);
```

Default construction again uses the wildcard Bluetooth address conceptually represented as:

```text
00:00:00:00:00:00
```

with PSM `0` until a more specific PSM is configured.

RFCOMM and L2CAP both belong to the Bluetooth world, but their service selectors are not the same thing: RFCOMM uses a channel, while L2CAP uses a PSM.

That is why SNode.C gives them distinct address classes instead of hiding both behind one ambiguous Bluetooth endpoint type. Similar Bluetooth vocabulary does not mean identical endpoint semantics.

### Cross-family address behavior

Once the five concrete families are understood, several cross-family patterns become visible.

These patterns should be learned as concepts, not as a list of signatures.

#### Default construction and wildcard meaning

Default construction is meaningful; it is not just uninitialized data.

Across the supported families, it expresses a wildcard-like or deferred endpoint identity:

| Family | Default / wildcard shape |
|---|---|
| IPv4 | `0.0.0.0`, port `0` |
| IPv6 | `::`, port `0` |
| Unix domain sockets | empty string |
| RFCOMM | `00:00:00:00:00:00`, channel `0` |
| L2CAP | `00:00:00:00:00:00`, PSM `0` |

This matters because socket programming often begins with partial endpoint descriptions.

A server may specify only the service selector it wants to listen on.

A client may specify a remote endpoint while leaving its local endpoint broad or system-selectable.

A wildcard address is not an error. It is often the correct expression of "let this endpoint be broad until bind or connect makes it concrete."

#### Constructors teach semantics

A reader can learn a surprising amount from constructor sets alone.

Across the five families, constructors expose what each endpoint family considers natural identity.

Port-only construction makes sense for IPv4 and IPv6 because a server often listens on a port without caring which local interface receives the connection.

Path-only construction makes sense for Unix domain sockets because the path is the endpoint identity.

Channel-only construction makes sense for RFCOMM because a local service can be described by its channel while the Bluetooth address remains wildcarded.

PSM-only construction makes sense for L2CAP for the same reason, but in L2CAP's own vocabulary.

Full constructors express a fully specified remote endpoint or an explicitly bound local endpoint:

```cpp
net::in::SocketAddress ip4("127.0.0.1", 8080);
net::in6::SocketAddress ip6("::1", 8080);
net::un::SocketAddress un("/tmp/snodec.sock");
net::rc::SocketAddress rc("00:11:22:33:44:55", 3);
net::l2::SocketAddress l2("00:11:22:33:44:55", 0x1001);
```

These examples are not meant to introduce a full application. They are code anchors for the address model.

#### Setters and getters use family language

Each address class provides setters and getters appropriate to its family.

That is not only for programmer comfort.

It reinforces the framework's educational idea:

> Endpoint identity should be named in the language of its family.

So instead of forcing everything through generic key-value access, the framework uses names such as:

```cpp
setHost(...)
setPort(...)
setSunPath(...)
setBtAddress(...)
setChannel(...)
setPsm(...)
```

The names themselves teach what kind of endpoint the reader is configuring.

#### String rendering and diagnostics

All five concrete address classes provide string rendering.

This may seem secondary, but it is part of runtime literacy.

A framework that reports endpoint identity poorly becomes harder to operate. Good address rendering helps in:

- startup logging,
- status callbacks,
- error reporting,
- connect and listen diagnostics,
- teaching examples.

A good address string is often the first thing a reader or operator sees when a connection succeeds or fails.

#### Local and remote endpoint thinking

Address semantics become clearer once the reader thinks in local-versus-remote pairs.

A server usually cares first about a **local bind address**.

A client usually cares first about a **remote peer address**.

But both sides may have both identities conceptually present.

For example:

- a server may bind to a wildcard local address,
- a client may leave its local side wildcarded,
- a Unix domain server may bind a local path,
- a Bluetooth server may listen on a wildcard Bluetooth address plus channel or PSM,
- a Bluetooth client may specify the remote device while leaving the local side broad.

Once this is understood, address classes stop feeling like static data containers. They become endpoint-role objects.

### Address semantics and the layer model

This chapter is the concrete continuation of Chapter 7: the address classes are where the network layer becomes tangible.

They show:

- what counts as endpoint identity in each family,
- how wildcarding works in that family,
- which values belong naturally together,
- how higher layers can stay similar while lower identity rules differ.

In that sense, `SocketAddress` is one of the clearest bridges between architecture and code.

The application layer may still use the same context/factory pattern. The runtime may still drive events in the same way. But the network layer changes the meaning of the endpoint being bound or connected.

That is the point of separating the layers.

### Why IP families have richer resolution behavior

IPv4 and IPv6 differ from Unix domain, RFCOMM, and L2CAP in one especially important way.

Their address classes expose resolution-oriented API pieces:

- `Hints`,
- `useNext()`,
- canonical-name access.

This reflects the fact that internet-style host names may resolve to more than one candidate endpoint. A name such as:

```text
example.org
```

is not always a single concrete address.

It may produce several candidates, and the framework's address abstraction leaves room for iterating through them.

That is why the IP-family address classes are richer in this specific area. The richness is not accidental feature growth; it reflects the semantics of the family.

### What belongs where?

This table summarizes the address-level meaning of common concepts.

| Concept | Address-layer meaning |
|---|---|
| Address family | Which endpoint universe the address belongs to |
| Host | IP-family peer or local interface identity |
| Port | IP-family service selector |
| Unix path | Local operating-system endpoint identity |
| Bluetooth address | Bluetooth device identity |
| RFCOMM channel | RFCOMM service selector |
| L2CAP PSM | L2CAP service selector |
| Wildcard/default address | Broad or deferred endpoint identity |
| `toString(...)` | Runtime-readable representation |

The table is deliberately simple. Its job is not to replace the API documentation. Its job is to help the reader ask the right question:

> What kind of endpoint identity am I describing?

### What to remember

Remember:

- Socket addresses belong to the network layer.
- Each network family has its own concrete address class.
- IPv4 and IPv6 use host plus port.
- Unix domain sockets use local socket path identity.
- RFCOMM uses Bluetooth address plus channel.
- L2CAP uses Bluetooth address plus PSM.
- Default construction is meaningful and wildcard-oriented, not uninitialized data.
- Constructors reveal what each family considers natural endpoint identity.
- Setters and getters use the language of the family.
- Similar API shape does not mean identical endpoint semantics.
- Address rendering is part of runtime diagnostics.
- Local and remote endpoint roles shape how addresses are interpreted.

### Closing perspective

Chapter 7 taught the communication layer stack.

This chapter made the network layer concrete by studying endpoint identity.

That prepares the next step. Once we understand what an address means, we can return to server and client roles with better precision. `listen(...)` and `connect(...)` do not merely receive arbitrary strings or numbers; they receive family-specific endpoint descriptions.

A server binds to an endpoint identity.

A client connects to an endpoint identity.

The next chapters can now discuss server and client construction, lower-layer choices, and connection behavior with this address model in place.
