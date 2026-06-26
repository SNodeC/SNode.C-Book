## Socket Addresses and Address Semantics

\index{SocketAddress@\texttt{SocketAddress}}
\index{address semantics}
\index{endpoint identity}


### From layers to endpoint identity

Chapter 7 showed how SNode.C communication choices are encoded in the layer stack.

The first of those choices is the network family. An application may use IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP. That choice changes what an endpoint *is*; the namespace or build component is only the visible consequence.

It therefore asks a narrower but important question:

> What does endpoint identity mean for each supported family?

When people first learn network programming, they often treat addresses as simple input values. An IP address is a string. A port is a number. A Unix domain socket is a path. A Bluetooth endpoint is a device address plus a service selector.

That view is understandable, but it is too shallow for a framework like SNode.C.

In SNode.C, addresses are part of the network layer. They are not incidental parameters passed into `listen(...)` and `connect(...)` and then forgotten. The address type tells the framework and the reader what kind of endpoint identity is being described.

That affects practical questions:

- how a server binds,
- how a client selects a peer,
- what a wildcard endpoint means,
- what local and remote identity mean,
- how diagnostics should render the endpoint,
- and, in the IP families, how a name can resolve to candidate addresses.

Therefore, SNode.C does not collapse all endpoints into one vague address class. It uses a shared pattern, but preserves the family-specific meaning.

### The shared `SocketAddress` pattern

\index{SocketAddress@\texttt{SocketAddress}}
\index{address classes}


The common base is:

```cpp
net::SocketAddress<SockAddrT>
```

That template already tells us something useful.

A SNode.C address is backed by a concrete socket-address structure and length, and it participates in the framework's broader socket-address abstraction. The template parameter keeps the operating-system address representation visible enough for the family-specific class to remain honest.

The shared base gives the framework a common shape. The derived family classes preserve the differences.

That is the right compromise for this part of the design:

::: {.snodec-note title="Endpoint identity note"}
One address pattern, but no false claim that all endpoint identities mean the same thing.
:::

This mirrors the layer model from Chapter 7. The application shape may stay recognizable, but the endpoint family still matters.

### Local and remote endpoint roles

\index{local endpoint}
\index{remote endpoint}


Before looking at the concrete families, it helps to separate two questions that are often mixed together.

The first question is:

> What kind of endpoint identity does this family use?

The second question is:

> Is this address being used as a local endpoint or as a remote peer endpoint?

A server usually starts with a local bind identity. It may bind to a specific interface, a wildcard address, a Unix-domain path, a Bluetooth address, or a service selector.

A client usually starts with a remote peer identity. It may connect to a host and port, a Unix-domain path, a Bluetooth device and channel, or a Bluetooth device and PSM.

But the distinction is not absolute. A client may also have a local-side address. A server may later observe the remote addresses of connected peers. The same address class can therefore appear in different roles.

This is one reason address semantics deserve careful treatment. A value such as `0`, `""`, or `00:00:00:00:00:00` is not meaningful by itself. It becomes meaningful in a family and in a role.

### Endpoint identity by family

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

This table is the concrete continuation of Chapter 7. The network layer chooses the endpoint family; the address class expresses that family in C++.

The useful reading habit is:

::: {.snodec-note title="Address-reading habit"}
Do not ask only what values an address object stores. Ask what kind of endpoint identity those values describe.
:::

#### IPv4: host plus port

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

The default IPv4 address is wildcard-oriented:

```text
0.0.0.0
```

with port:

```text
0
```

For a server, `0.0.0.0` naturally means that the server is not restricted to one specific local IPv4 interface. Port `0` means that the concrete service selector has not yet been fixed and may be selected later by the operating system if used in that way.

The IPv4 class also contains the resolution-oriented pieces that belong to IP-style addressing: `Hints`, canonical-name access, and `useNext()`. That is not accidental API growth. A host name may resolve to more than one candidate endpoint. The address abstraction therefore needs room for resolution and iteration.

#### IPv6: similar shape, different family

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

The default IPv6 host is:

```text
::
```

with port:

```text
0
```

This gives IPv6 the same broad wildcard-oriented starting point as IPv4, but in IPv6 vocabulary.

The similarity is useful, but it should not hide the family boundary. IPv6 has its own address syntax, operational behavior, and deployment consequences. SNode.C gives IPv4 and IPv6 a similar address interface where that helps, while preserving the fact that they are different endpoint families.

#### Unix domain sockets: local endpoint identity

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

Default construction uses the empty string:

```text
""
```

In the SNode.C address model, that is the wildcard or not-yet-specific Unix-domain endpoint identity.

Unix domain sockets are pedagogically useful because they break a common habit. They remind the reader that not every endpoint is internet-shaped. The same server/client/context architecture can still appear, but the network-layer identity is different.

#### RFCOMM: Bluetooth address plus channel

\index{RFCOMM}
\index{Bluetooth!RFCOMM}
\index{channel}


The RFCOMM address class is:

```cpp
net::rc::SocketAddress
```

An RFCOMM endpoint is:

```text
Bluetooth device address
  + RFCOMM channel
```

A concrete remote endpoint may look like this:

```cpp
net::rc::SocketAddress remote("00:11:22:33:44:55", 3);
```

The Bluetooth address identifies the device. The RFCOMM channel selects the service within the RFCOMM family. The channel should not just be translated into “a Bluetooth port number.” That wording would pull the reader back into IP vocabulary. A channel is the service selector used by RFCOMM.

Default construction is wildcard-oriented in the SNode.C model:

```text
00:00:00:00:00:00
```

with channel:

```text
0
```

That means the address can express a broad or deferred Bluetooth endpoint identity until the application or configuration makes it more specific.

#### L2CAP: Bluetooth address plus PSM

\index{L2CAP}
\index{Bluetooth!L2CAP}
\index{PSM}


The L2CAP address class is:

```cpp
net::l2::SocketAddress
```

It belongs to the same Bluetooth world as RFCOMM, but it uses a different service selector:

```text
Bluetooth device address
  + PSM
```

A concrete remote endpoint may look like this:

```cpp
net::l2::SocketAddress remote("00:11:22:33:44:55", 0x1001);
```

The Bluetooth address again identifies the device. The PSM identifies the L2CAP service endpoint.

Default construction follows the same wildcard-oriented Bluetooth pattern:

```text
00:00:00:00:00:00
```

with PSM:

```text
0
```

RFCOMM and L2CAP therefore share the idea of Bluetooth device identity, but they do not share the same service selector vocabulary. RFCOMM uses a channel. L2CAP uses a PSM.

That is why SNode.C gives them distinct address classes. Similar Bluetooth vocabulary does not mean identical endpoint semantics.

### Patterns that repeat across families

The five families differ, but several patterns repeat.

The point of this section is not to list every constructor or every member function. The useful question is:

> What does the API shape teach about endpoint identity?

#### Default construction and wildcard meaning

\index{wildcard address}
\index{default construction}


Default construction is meaningful. It is not uninitialized data.

Across the supported families, the default address expresses a wildcard-like, broad, or deferred endpoint identity:

| Family | Default / wildcard shape |
|---|---|
| IPv4 | `0.0.0.0`, port `0` |
| IPv6 | `::`, port `0` |
| Unix domain sockets | empty string |
| RFCOMM | `00:00:00:00:00:00`, channel `0` |
| L2CAP | `00:00:00:00:00:00`, PSM `0` |

This matters because socket programming often begins with partial endpoint descriptions.

A server may specify only the service selector it wants to listen on. A client may specify a remote endpoint while leaving its local side broad. A wildcard address is not an error. It is often the correct expression of “this endpoint is broad until bind or connect makes it concrete.”

#### Constructors teach identity shape

Constructors reveal what each family considers natural.

Port-only construction makes sense for IPv4 and IPv6 because a server often listens on a service port without caring which local interface receives the connection.

Path construction makes sense for Unix domain sockets because the path is the local endpoint identity.

Channel construction makes sense for RFCOMM because an RFCOMM service can be described by a channel while the Bluetooth address remains wildcarded.

PSM construction makes sense for L2CAP for the same reason, but in L2CAP vocabulary.

Full constructors express a fully specified peer or an explicitly specified local endpoint:

```cpp
net::in::SocketAddress ip4("127.0.0.1", 8080);
net::in6::SocketAddress ip6("::1", 8080);
net::un::SocketAddress un("/tmp/snodec.sock");
net::rc::SocketAddress rc("00:11:22:33:44:55", 3);
net::l2::SocketAddress l2("00:11:22:33:44:55", 0x1001);
```

These examples are not application programs. They are anchors for the address model.

#### Setters and getters use family language

Each address class names its fields in the language of its family. That is an important design choice.

The framework does not force all address data through vague names such as `value1` and `value2`, or through a single generic key-value map. It uses names such as:

```cpp
setHost(...)
setPort(...)
setSunPath(...)
setBtAddress(...)
setChannel(...)
setPsm(...)
```

The names teach the endpoint model.

A host is not a Unix path. A Unix path is not a Bluetooth address. An RFCOMM channel is not an L2CAP PSM.

The API vocabulary preserves those differences.

#### String rendering is part of runtime literacy

All concrete address classes provide string rendering.

That may look secondary, but it is part of operational readability. A framework that cannot report endpoint identity clearly is harder to teach, harder to debug, and harder to operate.

Address rendering appears in places such as:

- startup logging,
- listen and connect callbacks,
- error messages,
- status output,
- diagnostic traces,
- and teaching examples.

A good address string is often the first evidence a reader sees that a server has bound the expected endpoint or that a client tried to connect to the expected peer.

### Address semantics and the layer model

This chapter is the first concrete network-layer chapter after the general layer model.

The runtime may still advance registered instances in the same broad way. The application may still use a factory and a context. The connection layer may still distinguish non-TLS stream handling from TLS stream handling.

But the network layer changes the meaning of the endpoint being bound or connected. That is why `SocketAddress` is such a useful bridge between architecture and code.

It shows:

- what counts as endpoint identity in each family,
- how wildcarding is expressed in that family,
- which values naturally belong together,
- how local and remote endpoint roles are described,
- and how higher layers can stay similar while lower identity rules differ.

This is the practical value of separating layers. The application writer does not have to relearn the whole framework for every family, but neither does the framework pretend that every family has the same endpoint semantics.

### Why IP families have richer resolution behavior

\index{address resolution}
\index{DNS}


IPv4 and IPv6 differ from Unix domain sockets, RFCOMM, and L2CAP in one especially important way.

Their address classes expose resolution-oriented API pieces:

- `Hints`,
- `useNext()`,
- canonical-name access.

This reflects the fact that internet-style host names may resolve to more than one candidate endpoint.

A name such as:

```text
example.org
```

is not necessarily one concrete address. It may produce several candidates. The framework's address abstraction therefore leaves room for iterating through them.

Therefore, the IP-family address classes are richer in this specific area. The richness is not accidental; it reflects the semantics of the family.

That distinction also prevents a false generalization. Unix domain sockets, RFCOMM, and L2CAP do not need to mimic IP name resolution merely to fit a common abstract shape. They keep the address model appropriate to their own family.

### What belongs where?

The following table summarizes the address-level meaning of common terms.

| Concept | Address-layer meaning |
|---|---|
| Address family | The endpoint universe the address belongs to |
| Host | IP-family peer or local-interface identity |
| Port | IP-family service selector |
| Unix path | Local operating-system endpoint identity |
| Bluetooth address | Bluetooth device identity |
| RFCOMM channel | RFCOMM service selector |
| L2CAP PSM | L2CAP service selector |
| Wildcard/default address | Broad or deferred endpoint identity |
| `toString(...)` | Runtime-readable endpoint representation |

The table is compact. Its job is not to replace the API reference. Its job is to keep the central question visible:

> What kind of endpoint identity am I describing?

Once that question becomes natural, the address classes become much easier to read.

::: {.snodec-remember title="What to remember"}
- Socket addresses belong to the network layer: they describe endpoint identity for a selected family.
- SNode.C uses a shared address pattern, but each supported family keeps its own concrete `SocketAddress` type.
- IPv4 and IPv6 use host-plus-port identity and add resolution-oriented behavior such as hints, canonical names, and candidate iteration.
- Unix domain sockets use local socket path identity.
- RFCOMM and L2CAP use Bluetooth device identity with different service selectors: channel for RFCOMM, PSM for L2CAP.
- Default construction is meaningful and wildcard-oriented in family-specific ways.
:::

### Closing perspective

Chapter 7 explained the communication stack. This chapter made the first layer of that stack concrete by studying endpoint identity.

Chapter 9 can therefore ask the next architectural question with sharper vocabulary: how do server instances, client instances, and concrete connections use those endpoint identities while the runtime advances the communication flow?

