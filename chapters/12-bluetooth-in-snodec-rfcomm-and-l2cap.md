## Bluetooth in SNode.C: RFCOMM and L2CAP
### Why Bluetooth belongs in the main story

Bluetooth must not be treated as an appendix in a book about SNode.C.

That would give the wrong impression.

In SNode.C, Bluetooth is not a bolt-on curiosity. It is one of the framework’s real lower communication families. It sits beside IPv4, IPv6, and Unix domain sockets in the larger architecture.

That matters for two reasons.

First, it confirms that the framework’s layer model is genuinely broad.

Second, it makes SNode.C especially interesting for IoT, embedded, and device-near systems work, where local radio-based communication may be just as important as internet-based communication.

This chapter therefore does not present Bluetooth as “special support.”

It presents Bluetooth as a first-class family with two distinct lower-layer identities:

- RFCOMM
- L2CAP

And the central teaching lesson is this:

> Even when the lower-family endpoint identity becomes Bluetooth-specific, the larger SNode.C communication model remains stable.

### The two Bluetooth families in SNode.C

SNode.C provides two Bluetooth-related network families:

- `net::rc` for RFCOMM
- `net::l2` for L2CAP

These are not two names for the same thing.

They are two different Bluetooth endpoint models, each with its own address semantics and its own convenience API shapes.

That is exactly why the framework gives them distinct namespaces and distinct concrete `SocketAddress` classes.

This is a very good design choice.

If the framework had tried to flatten them into one vague “Bluetooth socket” abstraction, it would have become harder to teach and easier to misuse.

### The first major difference: channel versus PSM

The most important conceptual difference between RFCOMM and L2CAP in SNode.C is the endpoint identity.

RFCOMM uses:

- Bluetooth device address
- plus **channel**

L2CAP uses:

- Bluetooth device address
- plus **PSM**

This difference is not superficial.

It is the reason the two families deserve separate treatment.

A reader should therefore avoid the lazy habit of thinking:

> “Both are Bluetooth, so the second number must mean the same thing.”

It does not.

In RFCOMM, the service-like endpoint selector is the channel. In L2CAP, it is the PSM.

SNode.C’s API helps the reader get this right because the family-specific setters and getters are explicit.

### The address classes make the distinction precise

The current live `net::rc::SocketAddress` class is built around:

- default construction,
- Bluetooth-address construction,
- channel construction,
- Bluetooth-address-plus-channel construction,
- `setBtAddress(...)` / `getBtAddress()`,
- `setChannel(...)` / `getChannel()`,
- and string rendering.

The current live `net::l2::SocketAddress` class mirrors the same basic pattern, but uses:

- Bluetooth-address construction,
- PSM construction,
- Bluetooth-address-plus-PSM construction,
- `setBtAddress(...)` / `getBtAddress()`,
- `setPsm(...)` / `getPsm()`,
- and string rendering.

This is exactly the right degree of symmetry.

The shared pattern teaches confidence. The differing field names teach correctness.

### Why Bluetooth is the perfect proof of the architecture

Unix domain sockets already taught the reader that endpoint identity need not be host-plus-port.

Bluetooth now pushes that lesson even further.

Here, endpoint identity is neither:

- IP host plus port,
- nor local filesystem path.

Instead, it is Bluetooth-specific identity.

And yet the larger framework model remains recognizable.

You still have:

- a server or client instance,
- a factory,
- a context,
- a connection,
- a stream transport model,
- legacy or TLS connection handling,
- status callbacks,
- runtime integration.

That is why Bluetooth is such an important chapter.

It proves that SNode.C’s structure is genuinely portable across very different lower communication families.

### The RFCOMM server-side convenience API

The current live `net::rc::stream::SocketServer` wrapper provides the server convenience forms one would expect for the RFCOMM family.

Its convenience overloads are built around:

- `listen(channel, ...)`
- `listen(channel, backlog, ...)`
- `listen(btAddress, channel, ...)`
- `listen(btAddress, channel, backlog, ...)`

These overloads work by filling the instance configuration through `Local::setChannel(...)` and, where provided, `Local::setBtAddress(...)`, then delegating to the general `listen(onStatus)` path.

This is the same teaching pattern we already saw for IPv4, IPv6, and Unix domain sockets.

That is exactly what we want.

Bluetooth should feel different in *endpoint semantics*, not alien in *framework structure*.

### The RFCOMM client-side convenience API

The current live `net::rc::stream::SocketClient` wrapper mirrors the server-side idea with RFCOMM-specific client forms such as:

- `connect(btAddress, channel, ...)`
- `connect(btAddress, channel, bindBtAddress, ...)`
- `connect(btAddress, channel, bindChannel, ...)`
- `connect(btAddress, channel, bindBtAddress, bindChannel, ...)`

This is very instructive.

It shows that even in a Bluetooth family, SNode.C still keeps the local-versus-remote distinction clear.

The remote side is the target Bluetooth address plus channel. The local side can also be refined with a local Bluetooth address, a local channel, or both.

That continuity is one of the framework’s strongest design qualities.

### The L2CAP server-side convenience API

The current live `net::l2::stream::SocketServer` wrapper provides the corresponding L2CAP server forms:

- `listen(psm, ...)`
- `listen(psm, backlog, ...)`
- `listen(btAddress, psm, ...)`
- `listen(btAddress, psm, backlog, ...)`

The pattern is the same as RFCOMM, but the endpoint semantics are different.

Instead of configuring a channel, the server configures a PSM.

This is precisely the kind of difference SNode.C wants to preserve clearly.

The framework is saying:

- yes, these two Bluetooth families are structurally parallel,
- no, they are not semantically interchangeable.

That is excellent API design.

### The L2CAP client-side convenience API

The current live `net::l2::stream::SocketClient` wrapper continues the same structure on the client side with forms such as:

- `connect(btAddress, psm, ...)`
- `connect(btAddress, psm, bindBtAddress, ...)`
- `connect(btAddress, psm, bindPsm, ...)`
- `connect(btAddress, psm, bindBtAddress, bindPsm, ...)`

Again, this is a strong sign that the framework is teaching the right lesson.

The family-specific endpoint details change. The communication-role structure does not.

A reader who really understands this will begin to feel at home in the framework even when the lower family becomes unfamiliar.

### One strong pattern across both Bluetooth families

At this point, the most useful summary is simple.

For both RFCOMM and L2CAP, SNode.C keeps the same higher-level application pattern:

- create a server or client instance,
- configure endpoint identity in the family’s own language,
- attach a context factory,
- let the runtime create concrete connections,
- let the context implement protocol behavior.

The lower-family identity changes from channel to PSM. The larger framework shape does not.

This is one of the deepest transfer lessons in the whole lower-layer part of the book.

### What a typical RFCOMM example feels like

In spirit, a simple RFCOMM server still looks familiar:

```cpp
using RcServer = net::rc::stream::legacy::SocketServer<MyFactory>;

RcServer server("echo-rc");
server.listen(16, 5, onStatus);
```

or with explicit local Bluetooth address:

```cpp
server.listen("10:3D:1C:AC:BA:9C", 16, 5, onStatus);
```

A corresponding client still feels like a normal SNode.C client in shape:

```cpp
using RcClient = net::rc::stream::legacy::SocketClient<MyFactory>;

RcClient client("echo-rc-client");
client.connect("10:3D:1C:AC:BA:9C", 16, onStatus);
```

The important thing is not the literal example values.

The important thing is that the server/client structure remains calm and recognizable while the endpoint semantics become Bluetooth-specific.

### What a typical L2CAP example feels like

The same is true for L2CAP.

A simple L2CAP server still looks structurally familiar:

```cpp
using L2Server = net::l2::stream::legacy::SocketServer<MyFactory>;

L2Server server("echo-l2");
server.listen(0x1001, 5, onStatus);
```

and the client side likewise remains structurally stable:

```cpp
using L2Client = net::l2::stream::legacy::SocketClient<MyFactory>;

L2Client client("echo-l2-client");
client.connect("10:3D:1C:AC:BA:9C", 0x1001, onStatus);
```

Again, the point is not to turn the chapter into a list of values.

The point is to show that the communication family changes while the SNode.C application shape remains stable.

### Why Bluetooth is especially important for IoT readers

For IoT and embedded readers, this chapter carries a message larger than the API itself.

It shows that SNode.C is not only useful when everything is already framed as internet-facing TCP/IP communication.

It is also useful for systems that must speak locally over Bluetooth.

That matters a great deal in real device architectures.

A serious IoT system may mix several communication worlds:

- local device-near communication,
- local machine-local IPC,
- network communication over IPv4 or IPv6,
- secure transport,
- higher-level web or MQTT protocols.

SNode.C’s value is that it lets these worlds be understood as parts of one architecture rather than as disconnected programming domains.

### A note on Bluetooth and TLS

Earlier in the book we established that `legacy` and `tls` are connection-layer choices, not separate application worlds.

Bluetooth fits into that same model.

That means the reader should not think of RFCOMM or L2CAP as somehow outside the possibility of connection-layer encryption treatment in the framework.

The deeper teaching point is this:

Once the family and transport are chosen, the connection-layer story still remains meaningful.

That is one of the strongest confirmations that the framework’s layering is real and not just decorative.

### BlueZ and platform reality

A good technical book should remain honest about platform reality.

Bluetooth support in SNode.C depends on the Bluetooth stack and development support being available on the platform. The current repository documentation and build structure both reflect this. The README treats BlueZ development files as optional dependencies, and the top-level build includes Bluetooth-related supported components conditionally rather than pretending that they always exist everywhere.

That is the right posture.

The framework exposes Bluetooth as a first-class family, but it also respects the fact that the platform must actually provide the necessary Bluetooth support.

This is not a weakness.

It is simply an honest reflection of system reality.

### Why the local-versus-remote distinction still matters here

Because Bluetooth endpoint identity is often unfamiliar to readers coming from IP-first backgrounds, it is especially important to preserve the local/remote distinction clearly.

The live client wrappers do exactly that.

They let the reader specify:

- the remote Bluetooth address and channel or PSM,
- optionally a local Bluetooth address,
- optionally a local channel or PSM.

This matters because it reinforces a deep structural truth of the framework:

lower-family identity changes do not remove communication roles.

There is still a local side and a remote side. There is still a bound identity and a peer identity. There is still a connection between them.

### Why RFCOMM and L2CAP should not be merged conceptually

It is worth saying this very directly.

A reader should not leave this chapter thinking:

> “RFCOMM and L2CAP are the same chapter because they are both Bluetooth.”

They are in the same chapter because they are the two Bluetooth families supported in the framework and because comparing them teaches the right lesson.

But they should not be merged conceptually.

RFCOMM is not L2CAP with different spelling. PSM is not channel with a different type name.

SNode.C’s API helps prevent this confusion by making the distinction explicit in the type system and convenience methods.

That is exactly why the framework is teachable here.

### The best lesson of the chapter

If the reader remembers only one major lesson from this chapter, it should be this one:

> Bluetooth in SNode.C is not a special exception to the framework. It is one more place where the same architecture proves itself.

That is the correct intellectual result.

A reader who understands the chapter well will start to feel that the framework is not “growing more complicated” as new families appear.

Instead, the reader will feel that the same stable architecture is being exercised under different endpoint semantics.

That is exactly the sign of a good framework and a good mental model.

### Common misunderstandings about Bluetooth in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Bluetooth support is an extra feature outside the main architecture.”

Corrected view: RFCOMM and L2CAP are first-class lower communication families inside the same layer model as IPv4, IPv6, and Unix domain sockets.

#### Misunderstanding 2: “RFCOMM and L2CAP are basically the same thing.”

Corrected view: they are distinct Bluetooth families with distinct endpoint semantics, especially channel versus PSM.

#### Misunderstanding 3: “Once the endpoint is Bluetooth-specific, the rest of the framework model changes too.”

Corrected view: the larger SNode.C architecture remains stable; the lower-family identity changes.

#### Misunderstanding 4: “Bluetooth means local/remote roles become less important.”

Corrected view: the live client APIs preserve the local-versus-remote distinction very clearly.

#### Misunderstanding 5: “Bluetooth support means the framework is trying to hide platform reality.”

Corrected view: the framework exposes Bluetooth as a first-class family while still honestly depending on Bluetooth stack support being present on the platform.

### Closing perspective

This chapter completes the lower-family tour in a very satisfying way.

The reader has now seen endpoint identities in several fundamentally different forms:

- host plus port,
- path,
- Bluetooth address plus channel,
- Bluetooth address plus PSM.

And yet the framework’s higher-level model has remained remarkably stable throughout.

That is the architectural success of SNode.C.

It lets the lower family differ radically without forcing the whole application model to fracture.

That is what makes the framework valuable for full-stack protocol work and especially for IoT-oriented systems.

And now that the reader has seen all these lower-family carriers, the book is ready to move upward again.

The next chapters can return to application construction and system design with a much stronger lower-layer foundation underneath them.
