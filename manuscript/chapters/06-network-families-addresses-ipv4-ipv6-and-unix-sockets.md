## Network Families: Addresses, IPv4/IPv6, and Unix Sockets {#network-families-addresses-ipv4-ipv6-and-unix-sockets}

### Address semantics {#socket-addresses-and-address-semantics}

\index{SocketAddress@\texttt{SocketAddress}}
\index{address semantics}
\index{endpoint identity}


#### From layers to endpoint identity

Every connection begins with an address, but an address is not merely a string to be parsed.

The first concrete choice is the network family. An application may use IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP. That choice changes what an endpoint *is*; the namespace or build component is only the visible consequence.

This chapter therefore asks a narrower question:

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

#### The shared `SocketAddress` pattern

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

This mirrors the layer model from Chapter 4. The application shape may stay recognizable, but the endpoint family still matters.

#### Local and remote endpoint roles

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

#### Endpoint identity by family

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

This table is the concrete continuation of Chapter 4. The network layer chooses the endpoint family; the address class expresses that family in C++.

The useful reading habit is:

::: {.snodec-note title="Address-reading habit"}
Do not ask only what values an address object stores. Ask what kind of endpoint identity those values describe.
:::

##### IPv4: host plus port

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

For a server bind, `0.0.0.0` means that the server is not restricted to one specific local IPv4 interface. Port `0` asks the operating system to select an available local port. That is useful in an isolated test, but a client still needs the actual selected port. The same values should not be copied mechanically into a remote destination: a default-constructed address is an initial value, not evidence that a useful peer has been selected.

The IPv4 class also contains the resolution-oriented pieces that belong to IP-style addressing: `Hints`, canonical-name access, and `useNext()`. That is not accidental API growth. A host name may resolve to more than one candidate endpoint. The address abstraction therefore needs room for resolution and iteration.

##### IPv6: similar shape, different family

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

##### Unix domain sockets: local endpoint identity

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

This is the not-yet-specific Unix-domain value in the address model. It is not the equivalent of a server listening on every IP interface. Before using a pathname listener, give it a concrete path and consider the containing directory's permissions and cleanup policy. The section “Unix domain sockets” distinguishes pathname and abstract-namespace behavior.

Unix domain sockets are pedagogically useful because they break a common habit. They remind the reader that not every endpoint is internet-shaped. The same server/client/context architecture can still appear, but the network-layer identity is different.

##### RFCOMM: Bluetooth address plus channel

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

##### L2CAP: Bluetooth address plus PSM

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

SNode.C gives them distinct address classes because similar Bluetooth vocabulary does not mean identical endpoint semantics.

#### Patterns that repeat across families

The five families differ, but several patterns repeat.

The point of this section is not to list every constructor or every member function. The useful question is:

> What does the API shape teach about endpoint identity?

##### Default construction and wildcard meaning

\index{wildcard address}
\index{default construction}


Default construction is meaningful. It is not uninitialized data.

Across the supported families, default construction supplies the following initial values. Only some have wildcard bind semantics:

| Family | Default value |
|---|---|
| IPv4 | `0.0.0.0`, port `0` |
| IPv6 | `::`, port `0` |
| Unix domain sockets | empty string |
| RFCOMM | `00:00:00:00:00:00`, channel `0` |
| L2CAP | `00:00:00:00:00:00`, PSM `0` |

Socket programming often begins with partial endpoint descriptions.

A server may specify only the service selector it wants to listen on. A client may specify a remote endpoint while leaving its local side broad. A wildcard address often expresses “this endpoint is broad until bind or connect makes it concrete” rather than an error.

##### Constructors teach identity shape

Constructors reveal what each family considers natural.

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

These examples are not application programs. They are anchors for the address model.

##### Setters and getters use family language

Each address class names its fields in the language of its family. That is an important design choice.

The fields remain available through family-specific operations such as:

```cpp
setHost(...)
setPort(...)
setSunPath(...)
setBtAddress(...)
setChannel(...)
setPsm(...)
```

The names teach the endpoint model.

This helps when changing carriers: a port assignment cannot simply become a Unix path assignment, and a channel choice does not establish a valid PSM. Revisit the endpoint's meaning as well as the setter's spelling.

##### String rendering is part of runtime literacy

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

#### Address semantics and the layer model

Try classifying three values before using them: `0.0.0.0:0` for a local IPv4 bind, `127.0.0.1:8080` for a remote IPv4 peer, and `/tmp/snodec.sock` for a local pathname service. The first asks the operating system to select a port; the second names a destination in the current host's loopback network; the third depends on the local filesystem namespace. None of those meanings comes from the text alone without its family and local/remote role.

Chapter 7 adds a useful observation: compare the requested bind address with the actual local address on an established connection. A broad configuration can produce a concrete endpoint. That is why logging only the configured value can leave a connection problem unexplained.

#### Why IP families have richer resolution behavior

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

#### What belongs where?

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
| Wildcard address | Family-specific broad bind identity |
| Default address | Initial value; not necessarily a usable bind or peer identity |
| `toString(...)` | Runtime-readable endpoint representation |

The table is compact. Its job is not to replace the API reference. Its job is to keep the central question visible:

> What kind of endpoint identity am I describing?

Once that question becomes natural, the address classes become much easier to read.

### IPv4 and IPv6 {#ipv4-and-ipv6-as-the-first-concrete-network-families}

\index{IPv4}
\index{IPv6}
\index{network families}


#### Why IPv4 and IPv6 come first

IPv4 and IPv6 are the cleanest place to see the SNode.C server/client model without the extra locality of Unix-domain sockets or the device-near assumptions of Bluetooth.

This chapter keeps that model intact and changes only the first concrete lower-family choice:

```text
IPv4 and IPv6
```

IPv4 and IPv6 form the first concrete comparison pair in this book because they are familiar enough to keep the application shape recognizable, but different enough to make the lower-family boundary visible.

Most readers already have some intuition for hosts, addresses, ports, listening servers, and remote peers. That makes IPv4 and IPv6 a good place to begin the concrete family discussion. At the same time, IPv4 and IPv6 are not the same family. Their namespaces, address classes, textual address forms, wildcard forms, and deployment questions differ. SNode.C makes that difference explicit instead of hiding it behind one overloaded network type.

Use the comparison to hold protocol behavior fixed while changing the endpoint family. A successful exchange on each loopback address will test that claim more directly than two similar type names. A failure on one family will then be a reason to inspect that family's binding and reachability, before changing the shared protocol.

#### What stays shared across IPv4 and IPv6

\index{IPv4!shared model}
\index{IPv6!shared model}
\index{server/client/context model}


For both IPv4 and IPv6, the outer application shape remains recognizable.

A typical stream application still involves:

- an application-side `SocketServer` or `SocketClient` handle,
- a configured instance and a separate activation flow from each `listen(...)` or `connect(...)` call,
- a `SocketContextFactory`,
- a per-connection `SocketContext`,
- a status callback for `listen(...)` or `connect(...)`,
- connection lifecycle callbacks if the application uses them,
- and a runtime started through `core::SNodeC::start()`.

Nothing about moving from IPv4 to IPv6 changes that architectural shape.

IPv4 and IPv6 show this without changing endpoint identity as radically as Unix domain sockets or Bluetooth do. Both IP families still use the familiar host-plus-port idea. That makes the comparison focused: the lower family changes, but the application architecture does not collapse into a different model.

##### Same server/client/context shape

Keep the factory and context files unchanged for the first comparison. The entry points select the family and endpoint; the context still receives bytes through the connection surface. If the change requires editing command parsing or byte reflection, inspect why the protocol acquired an address-family dependency before proceeding.

##### Parallel type names

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

This is the kind of layered reading introduced in Chapter 4. A long SNode.C type name says which lower family is used, which transport form is used, which connection variant is selected, which handle type is visible, and which factory creates the per-connection protocol contexts.

The IPv4/IPv6 comparison is therefore visible before a single socket operation is called. The type name already tells the reader which lower family has been selected.

##### Parallel address classes

\index{net::in::SocketAddress@\texttt{net::in::SocketAddress}}
\index{net::in6::SocketAddress@\texttt{net::in6::SocketAddress}}


The section “Address semantics” introduced address semantics. That model now applies directly to the two IP families.

| Family | Address class | Basic endpoint shape |
|---|---|---|
| IPv4 | `net::in::SocketAddress` | host plus port |
| IPv6 | `net::in6::SocketAddress` | host plus port |

The class names differ because the endpoint families differ. The basic shape is similar because both families use a host-plus-port model.

That is the right balance. One address pattern transfers across both IP families, but the similarity should not be exaggerated. IPv4 and IPv6 have different textual forms, different wildcard forms, and different deployment questions.

The useful lesson is:

::: {.snodec-note title="Parallel-shape note"}
The API shape is intentionally parallel where that helps, but the endpoint families remain distinct.
:::

Here “host” should be read broadly. It may be a numeric address such as `127.0.0.1` or `::1`, or it may be a name that has to be resolved. The convenience API makes the common case readable, but the section “Address semantics”’s address model still matters underneath.

##### Parallel convenience overloads

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

The exact overload count is less important than the pattern.

The architectural idea is:

> Easy-looking calls set configuration and then use the same underlying registration and flow machinery.

This matters for understanding SNode.C code. A short `listen(8080, ...)` call is a convenience surface over the same role configuration and registration model as constructing a `SocketAddress` and calling the more general path.

#### What remains stable

The final comparison table collects the stable and changing surfaces. While reading the code, use a narrower test: does the same protocol produce the same bytes and preserve separate state for each peer? Similar declarations establish where reuse is possible; those observations establish whether the selected composition actually behaves as intended.

If the application protocol is written in a `SocketContext`, it does not automatically become an “IPv4 protocol” or an “IPv6 protocol.” It is application behavior carried over a lower family. The same context class can often be reused when the protocol behavior does not inspect or depend on family-specific address details.

The lower family changes, and with it the endpoint representation, bind/connect configuration, and deployment environment.

What often remains stable is the protocol class, the factory structure, the connection lifecycle, the runtime, and the overall server/client model.

##### Runtime and instance model

IPv4 and IPv6 roles can participate in the same event runtime. Giving them separate instance names makes their configuration and diagnostics distinguishable even when they use one factory/context design. That is useful for a service that deliberately exposes two family-specific listeners: shared protocol behavior does not require one shared listening policy or one ambiguous operational name.

##### Factory, context, and protocol logic

The factory/context pattern also transfers.

A simple echo protocol implemented as a `SocketContext` can often be used with both IPv4 and IPv6 roles. The context does not need to care whether the peer endpoint was represented by an IPv4 or IPv6 address unless the protocol itself inspects, prints, filters, or interprets that address.

This separation keeps protocol logic from being unnecessarily tied to one lower family.

The factory carries the rule for creating the context. The context carries the protocol behavior. The selected IP family supplies the endpoint family and the lower communication path. Keeping those responsibilities separate is what makes the IPv4/IPv6 comparison useful instead of duplicating the whole application.

##### Status and lifecycle callbacks

A status callback reports an activation attempt; connection lifecycle callbacks concern an established peer relationship. Chapter 7 develops that distinction.

A `listen(...)` or `connect(...)` status callback reports outer role status. It sees the relevant address object and a `core::socket::State` value.

Connection lifecycle callbacks observe connections. They receive a `SocketConnection*` and can inspect local and remote addresses, timing, metrics, and connection names.

Context callbacks implement protocol behavior.

Moving from IPv4 to IPv6 does not collapse those callback layers. The lower-family namespace changes, but the callback model remains the same.

The first useful comparison is an observed exchange. Run the same context once over an IPv4 loopback endpoint and once over an IPv6 loopback endpoint. The payload and context callbacks should remain the same; the address type, formatted endpoint, and operating-system family differ. A successful IPv4 run does not establish IPv6 availability, and an IPv6 wildcard listener should not be assumed to replace a separately configured IPv4 role on every platform. The family-specific component tests keep those exchanges separate for exactly this reason.

#### What changes

\index{address family}
\index{wildcard form}


The stable structure does not mean IPv4 and IPv6 are identical. They are not.

The IPv6 discussion stays focused on where SNode.C keeps the architecture stable and where the lower family still matters.

##### Namespace and address family

The most visible code change is the namespace:

```text
net::in
  -> IPv4

net::in6
  -> IPv6
```

This is not cosmetic. It tells the reader that the lower family has changed.

The address class changes too:

```cpp
net::in::SocketAddress
net::in6::SocketAddress
```

Both are host-plus-port address classes, but they belong to different endpoint families. That distinction becomes important in examples, diagnostics, wildcard binding, and deployment.

The namespace is therefore a compact architectural statement:

```text
same stream model
same legacy/TLS layer choice
same server/client handle pattern
different internet family
```

##### Textual address form and wildcard form

The address forms differ while the wildcard-port value stays the same:

| Family | Loopback host | Wildcard host | Wildcard port |
|---|---|---|---|
| IPv4 | `127.0.0.1` | `0.0.0.0` | `0` |
| IPv6 | `::1` | `::` | `0` |

The section “Address semantics” already explained address semantics in detail. Here the important point is simply that the wildcard idea transfers, but its concrete family representation changes.

The reader should not think:

```text
IPv6 is just IPv4 with longer text.
```

IPv6 has its own address family and its own operational questions, even though the SNode.C API is intentionally parallel.

##### Local and remote configuration

The convenience overloads also make local and remote roles visible.

| Role | Endpoint configuration | Additional choice |
|---|---|---|
| Server | local host and port | backlog |
| Client | remote host and port | optional local bind host and port |

This applies the section “Address semantics”; Chapter 7 then develops the lifecycle consequences.

The section “Address semantics” explained what endpoint identity means. Chapter 7 will explain how servers and clients use endpoint identity. The section “IPv4 and IPv6” shows that IPv4 and IPv6 use the same local/remote role distinction with different address-family semantics.

##### IPv6-only, IPv4-mapped, and dual-stack thinking

\index{IPv6!IPv6-only}
\index{IPv6!IPv4-mapped addresses}
\index{dual-stack deployment}


IPv6 introduces one additional technical point: deployment can involve IPv6-only behavior, IPv4-mapped IPv6 addresses, or platform-specific dual-stack behavior.

There are two reasonable service designs. Separate IPv4 and IPv6 listeners make exposure and per-family failures explicit, at the cost of maintaining two endpoint configurations. A deliberately configured dual-stack listener can reduce that duplication, but the application must establish the platform's mapping and bind behavior and interpret mapped peer addresses consistently. Merely choosing an IPv6 wildcard value does not document that policy.

An IPv6 endpoint is not only a different address string. It may also raise configuration and platform questions about whether IPv4 traffic is included, excluded, or represented through IPv4-mapped IPv6 addresses.

That is one reason SNode.C keeps IPv6 as its own family instead of treating it as an overloaded IPv4 mode.

#### From IPv4 to IPv6

The move from IPv4 to IPv6 should make transfer visible without overwhelming the reader.

The useful reading path is simple. First, look at a minimal IPv4 legacy pair. Then look at the corresponding IPv6 legacy pair. Then compare what changed in code and what stayed stable in architecture. Later chapters can repeat the same comparison under TLS.

This keeps the lower-family comparison sharp. It also prepares the next variations: after IPv4 and IPv6, Unix domain sockets and Bluetooth can be introduced as more different endpoint families while the server/client/connection model remains familiar.

##### Start with IPv4

IPv4 remains the easiest first concrete example for many readers. The reason is familiarity, not greater importance: its notation and everyday expectations are familiar.

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

This path shows host plus port, server plus client, status callback, and runtime integration before IPv6 notation or dual-stack questions enter the picture.

##### Move immediately to IPv6

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

The important comparison is:

```text
net::in   -> net::in6
127.0.0.1 -> ::1
```

The outer structure remains stable. The lower family and address notation change.

##### Compare what changed and what did not

Once the IPv4 and IPv6 examples are side by side, the comparison becomes clear. What changed?

- the network-family namespace,
- the address class,
- address text,
- wildcard representation,
- possible IPv6-specific deployment questions.

What did not change?

- application-side server and client handle shape,
- registered instance model,
- connection model,
- context factory,
- context class shape,
- runtime startup,
- status callback model,
- connection lifecycle model,
- layered reading of the type name.

This comparison is the core result. The point is controlled variation across lower families, with IPv4 and IPv6 as the teaching path.

#### Stable model, different family semantics

The following table is the transfer map for the chapter. It shows which ideas stay stable and which ones move with the lower family.

| Aspect | IPv4 | IPv6 | Teaching point |
|---|---|---|---|
| Namespace | `net::in` | `net::in6` | lower family changes |
| Address class | `net::in::SocketAddress` | `net::in6::SocketAddress` | family-specific endpoint identity |
| Address shape | host + port | host + port | interface is parallel |
| Wildcard host | `0.0.0.0` | `::` | representation differs |
| Application-side handle | `SocketServer` / `SocketClient` | `SocketServer` / `SocketClient` | handle shape stays |
| Registered instance | server/client role | server/client role | role model stays |
| Connection | `SocketConnection` | `SocketConnection` | peer relationship model stays |
| Protocol context | same class often possible | same class often possible | protocol logic can transfer |
| Convenience API | sets config, delegates | sets config, delegates | easy API and configured API are one model |
| Extra concern | simpler first case | IPv6-only / IPv4-mapped / dual-stack questions | deployment semantics differ |

This table connects directly to Chapters 6 and 7. The section “Address semantics” explains the address rows. Chapter 7 explains the handle, instance, connection, factory, context, and callback rows.

This chapter shows IPv4 and IPv6 as the first concrete comparison pair.



#### Public surface of the primary families

\index{public headers}
\index{net::in::stream::legacy@\texttt{net::in::stream::legacy}}
\index{net::in6::stream::legacy@\texttt{net::in6::stream::legacy}}


IPv4 and IPv6 are the simplest place to see the source/build pairing. A file that directly names an IPv4 legacy stream role uses the IPv4 public role headers:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

with the matching component:

```text
net-in-stream-legacy
```

The IPv6 variant changes only the family fragment:

```cpp
#include <net/in6/stream/legacy/SocketServer.h>
#include <net/in6/stream/legacy/SocketClient.h>
```

with the corresponding component:

```text
net-in6-stream-legacy
```

The local point is the family selection. Chapter 25 gives the consolidated include/component matrix.

### Unix domain sockets {#unix-domain-sockets}

\index{Unix domain sockets}
\index{local IPC}
\index{path identity}


#### From host-plus-port to local path identity

A Unix-domain endpoint moves the conversation from network reachability to local IPC.

Unix-domain sockets keep the same SNode.C runtime model, but change endpoint identity more strongly:

```text
host + port
  -> local Unix-domain path
```

That is the next controlled variation in Part III.

With IPv4 and IPv6, an endpoint is described by an address and a port. With Unix domain sockets, an endpoint is described primarily by a local path. The endpoint no longer looks like an internet endpoint at all. It is a local interprocess-communication identity.

The factory and context still describe a stream protocol. The new responsibility is the local rendezvous point: the process must bind a usable path, clients must reach that same namespace, and the service must respect ownership and cleanup of the path. A working context does not resolve any of those deployment questions by itself.

#### Same SNode.C model, different endpoint identity

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

This is the same teaching pattern as in the section “IPv4 and IPv6”, but the shift is stronger. IPv4 and IPv6 were different internet families with a similar host-plus-port shape. Unix domain sockets change the addressing category itself.

#### Path identity in `net::un::SocketAddress`

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

##### Path as endpoint identity

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

##### Default construction and empty path

Default construction is meaningful in the Unix-domain address model.

The default address has not yet been given a concrete service path. Do not infer from the word *wildcard* that an empty Unix-domain path listens on every pathname in the way an IP wildcard covers local interfaces. The pathname examples in this chapter require an explicit rendezvous name.

There is also a distinction between a pathname and a socket address whose first path byte is zero. The source's `toString()` renders that second form with a leading `@`, a notation associated with the Linux abstract namespace. That rendering is not an input conversion rule: `setSunPath()` stores the supplied string, and `init()` copies its bytes. Do not turn a diagnostic `@name` into a pathname configuration without checking the address representation. The worked applications here use ordinary pathname sockets, whose directory access and cleanup can be inspected directly.

##### Locality as the defining idea

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

#### Server and client use with path-based endpoints

\index{Unix domain sockets!server/client use}
\index{listen()@\texttt{listen()}}
\index{connect()@\texttt{connect()}}


The stream Unix-domain wrappers follow the same SNode.C pattern as the IPv4 and IPv6 wrappers.

The convenience calls set family-specific configuration and then delegate to the general `listen(onStatus)` or `connect(onStatus)` path.

The difference is that the configured value is now a Unix-domain path. That keeps the application code pleasantly familiar while still making the lower-family decision explicit. A reader should see both sides at once: the call shape transfers, but the endpoint value has a different meaning.

##### Server-side `listen(...)`

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

This mirrors the the section “IPv4 and IPv6” pattern. A readable convenience call configures the handle and then enters the same registration path.

##### Client-side `connect(...)`

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

##### Local and remote paths

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

Chapter 7 develops this connection model in detail.

A connection can still have bind, local, and remote address views. The address family has changed, but directional endpoint thinking remains useful. This is one of the main reasons to keep the address family visible in the type system: it prevents the local/remote distinction from being flattened into an unhelpful generic string.

A pathname socket also has a filesystem lifecycle. The current physical Unix-domain implementation checks the path before binding and keeps cleanup tied to the endpoint it owns. A regular file at the requested pathname is not disposable socket state. When a local service fails to start, distinguish an occupied live socket, a stale socket pathname, a non-socket file, and insufficient directory permissions before deciding what to remove. The source test `UnixPhysicalSocketPathSafetyTest` exercises this boundary; unconditional deletion in application startup would bypass it.

#### What remains stable

\index{Unix domain sockets!stable model}
\index{SocketContext@\texttt{SocketContext}}


Unix domain sockets change endpoint identity, but they do not require a different application architecture.

##### Server/client/connection/context model

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

##### Context and protocol logic

A `SocketContext` implementing a small request/response or streaming protocol does not need to become fundamentally Unix-domain-specific just because it runs over:

```cpp
net::un::stream::legacy
```

The line parser, command responses, and per-peer receive buffer can remain unchanged. Authorization deserves a separate review, however: a rule based on an IP peer address cannot automatically become a rule based on local user identity. The credential query later in this chapter supplies facts for such a policy; it does not choose the policy.

The protocol context may inspect the address if it wants to log or display endpoint information. But the protocol logic itself can often remain the same. This is the separation the book is building toward: lower layers decide how peers are reached, while the context concentrates on what the application protocol does once a connection exists.

##### Legacy and TLS

Chapter 4 introduced `legacy` and `tls` as connection-layer variants. Unix domain sockets fit into that same layer story.

A Unix-domain stream component can participate in the pattern:

```text
net::un
  -> stream
      -> legacy or TLS
```

Here `legacy` is the non-TLS stream connection variant. `tls` adds TLS connection handling.

Unix domain sockets are not a special branch outside the framework. In SNode.C's terminology, they are another lower family in the network-layer part of the stack, while stream transport and connection-layer handling remain recognizable.

#### What changes operationally

\index{Unix domain sockets!deployment}
\index{path cleanup}
\index{path ownership}


Unix domain sockets are local, path-based endpoints. That changes deployment habits.

##### Deployment habits

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

##### Path ownership and cleanup thinking

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

##### Unix domain sockets are not a replacement for IP

Loopback IP is also a credible choice for communication on one machine. It may fit existing HTTP tools or a service expected to move onto another host later. A pathname socket makes a local service boundary and filesystem placement explicit and can support peer-credential policy, but processes in different filesystem namespaces must be given access to the same endpoint. Choose from those requirements rather than assuming that locality alone decides the family.

#### Peer credentials are facts, not authorization

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

#### Stream focus and a datagram note

\index{datagram sockets}
\index{stream sockets}


This chapter focuses on stream Unix domain sockets. That keeps the connection and protocol model established in the preceding chapters available while endpoint identity changes.

The SNode.C build also contains a `net-un-dgram` component, but datagram communication introduces a different communication shape and should not distract from the stream-based role model being developed in Chapters 6–8.

The practical lesson is simple: Unix domain sockets are not limited to one possible socket style, but this chapter follows the stream path because the book is still building the layered server/client/connection model.

#### Preparing the Bluetooth shift

Unix domain sockets are also a useful bridge to Bluetooth. IPv4 and IPv6 showed host-plus-port endpoint identity. Unix domain sockets showed path-based local endpoint identity.

Bluetooth will introduce endpoint identities that are different again:

```text
Bluetooth address + RFCOMM channel
Bluetooth address + L2CAP PSM
```

After the section “Unix domain sockets”, the reader has seen two kinds of endpoint shift: internet host-plus-port identity and local path identity. Chapter 8 adds device address plus service selector.

The server/client/connection/context model remains available, while the lower-family address semantics change again. After the next chapter develops server, client, and connection lifetimes, Bluetooth supplies another controlled variation in endpoint identity.



#### Public surface of Unix-domain stream roles

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

The same include/component rule from the primary families applies; only the family fragment changes. The consolidated mapping is collected in Chapter 25.

::: {.snodec-remember title="What to remember"}
- Socket addresses belong to the network layer: they describe endpoint identity for a selected family.
- SNode.C uses a shared address pattern, but each supported family keeps its own concrete `SocketAddress` type.
- Unix-domain addresses name local rendezvous points; pathname cleanup, directory permissions, and peer credentials need separate decisions.
- IPv4/IPv6 differences appear mainly in endpoint identity, resolution, wildcard forms, and deployment assumptions, not in a new application architecture.
- `connect(sunPath, bindSunPath, ...)` keeps the local/remote distinction visible even though both endpoints are path-based.
:::
