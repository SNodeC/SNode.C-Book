## Socket Addresses and Address Semantics
### Why addresses deserve their own chapter

When people first learn network programming, they often treat addresses as simple input values.

An IP address is a string. A port is a number. A Unix domain socket is a path. A Bluetooth endpoint is some address plus some smaller number.

That view is understandable, but it is too shallow for a framework like SNode.C.

In SNode.C, addresses are not incidental parameters passed into `listen(...)` and `connect(...)` and then forgotten.

They are part of the framework’s layer model.

The address type tells the framework — and the reader — what kind of endpoint identity exists at the network layer. It also shapes:

- how a server binds,
- how a client chooses a peer,
- what a wildcard endpoint means,
- what local versus remote identity means,
- what string rendering and diagnostics should look like,
- and, in some cases, how name resolution behaves.

That is why SNode.C gives each network family its own concrete `SocketAddress` type instead of pretending that all endpoints are the same thing.

This chapter explains that design choice and teaches the reader how to think about endpoint identity across the five supported families:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP.

### The general idea: one pattern, five concrete families

The current repository provides a common template base in `net::SocketAddress<SockAddrT>`, and each network family builds a concrete address class on top of it. The generic base already tells us that a SNode.C address is not just text: it is backed by a concrete socket-address structure and length, and it still participates in the framework’s broader socket-address abstraction. That gives the framework a shared pattern while allowing each family to keep its own semantics. 

The family-specific concrete classes are:

- `net::in::SocketAddress`
- `net::in6::SocketAddress`
- `net::un::SocketAddress`
- `net::rc::SocketAddress`
- `net::l2::SocketAddress`     

This is exactly the right architectural compromise.

There is a common address *pattern*, but there is no false claim that an IPv4 endpoint and a Unix domain socket path are “basically the same thing.”

They are not.

### What a socket address means in SNode.C

A socket address in SNode.C should be understood as an object that answers three questions at once.

#### What family does this endpoint belong to?

An address always belongs to a network family.

That family determines the underlying `sockaddr` variant, the meaning of the address fields, and what kinds of operations are valid.

#### What endpoint identity does this family use?

For IPv4 and IPv6, that is host plus port.

For Unix domain sockets, that is primarily a local path.

For Bluetooth RFCOMM, that is device address plus channel.

For Bluetooth L2CAP, that is device address plus PSM.

#### How should this endpoint be rendered and initialized?

Each concrete address class exposes operations for setting the relevant identity fields and rendering them meaningfully via `toString(...)` or similar endpoint-formatting methods.

This is not only cosmetic. Good string rendering is part of operational understanding.

When a listen or connect callback logs an address, the user should be able to understand what endpoint identity is actually in play.

### Wildcards are not “empty values”

One of the most important conceptual points in this chapter is the meaning of a default-constructed address.

A default address is usually not “missing” or “unset” in the ordinary application sense.

It is often a **wildcard** or **system-selectable** endpoint.

That is a deep and useful idea.

A wildcard local address often means:

- a server may listen on all relevant interfaces, or
- a client may let the operating system choose its local side automatically.

This is especially important when a reader begins to think about local-versus-remote roles.

The local side of an endpoint is often partly or fully wildcarded until binding or connecting makes it concrete.

This is not a bug. It is part of normal socket semantics, and SNode.C reflects that honestly.

### IPv4 addresses: host plus port, but not only that

The current `net::in::SocketAddress` class offers the following conceptual surface:

- default construction,
- construction from host,
- construction from port,
- construction from host plus port,
- construction from an existing `sockaddr_in`,
- `setHost(...)` / `getHost()`,
- `setPort(...)` / `getPort()`,
- canonical-name access,
- formatted string rendering,
- and endpoint formatting. It also carries a `Hints` structure and a `useNext()` mechanism, which strongly suggest address-resolution iteration rather than only one flat stored endpoint. 

That is already richer than a naïve “host and port” wrapper.

#### The default host is meaningful

The current header stores the default host as `0.0.0.0` and the default port as `0`. That is a very strong signal that the default object is intentionally wildcard-like. 

This means that when an IPv4 server listens without pinning itself to one specific interface, it can naturally be understood as listening on the wildcard host.

Likewise, an unbound local client side can be thought of as letting the operating system choose a suitable local address and ephemeral port.

#### Why `Hints` and `useNext()` matter

The presence of `Hints` and `useNext()` in the IPv4 address class tells us that SNode.C’s IPv4 addressing story includes name-resolution behavior that may produce more than one possible endpoint candidate. That is an important mental refinement.

A hostname is not always just one address.

It may resolve to a sequence of possibilities, and the address abstraction leaves room for that reality.

That makes the IPv4 address class more realistic and more useful than a simple pair of strings and numbers.

### IPv6 addresses: similar shape, different semantics

The current `net::in6::SocketAddress` class has almost the same conceptual surface as the IPv4 class:

- default construction,
- host-only, port-only, and host-plus-port construction,
- existing-`sockaddr_in6` construction,
- `Hints`,
- `useNext()`,
- host and port setters/getters,
- canonical name,
- string rendering,
- endpoint formatting. 

That similarity is important pedagogically.

It teaches the reader that IPv4 and IPv6 are different families, but they still fit the same higher-level pattern in SNode.C.

#### The default host is `::`

The current header stores the default host as `::` and the default port as `0`. Again, this confirms that the default IPv6 address is not “blank.” It is the IPv6 wildcard shape. 

This is one of the clearest examples of why default construction has real endpoint meaning in the framework.

#### Similar API, different operational questions

Because the IPv6 address class looks so similar to the IPv4 one, a reader might initially think that the only difference is the textual form of the address.

That is not true.

The class similarity is an *API-level teaching advantage*, but operationally IPv6 raises its own questions:

- pure IPv6 versus dual-stack behavior,
- wildcard binding in IPv6 terms,
- textual rendering differences,
- and name-resolution differences.

So the right conclusion is not “IPv6 is the same.”

The right conclusion is:

> SNode.C gives IPv4 and IPv6 a similar address interface because that similarity is real and useful — but the families remain operationally distinct.

### Unix domain socket addresses: locality made explicit

The current `net::un::SocketAddress` class is much simpler than the IP-family address classes.

It is built around:

- default construction,
- construction from a `sunPath`,
- construction from an existing `sockaddr_un`,
- initialization,
- `setSunPath(...)` / `getSunPath()`,
- and string rendering. 

This simpler surface is not a limitation. It reflects the actual semantics of the family.

A Unix domain socket endpoint is usually identified by a local path, not by host-plus-port ideas.

#### Why Unix domain addresses are conceptually different

A Unix domain socket address is a strong reminder that “network programming” is not only about network interfaces and IP addresses.

It can also mean local interprocess communication with filesystem-like endpoint identity.

This matters a great deal for teaching.

A reader who only learns networking through IP may begin to think that remote host identity is always central.

Unix domain sockets break that habit in a good way. They teach that endpoint identity can also be local, path-based, and operating-system-centric.

#### Why this family belongs in the same chapter

The fact that Unix domain sockets fit cleanly into the same general `SocketAddress` pattern is one of the framework’s strengths.

It lets the reader see both the shared pattern and the concrete semantic difference.

That is exactly what a good abstraction should do.

### RFCOMM addresses: Bluetooth endpoint identity in the same framework

The current `net::rc::SocketAddress` class provides:

- default construction,
- construction from Bluetooth address,
- construction from channel,
- construction from Bluetooth address plus channel,
- construction from an existing `sockaddr_rc`,
- initialization,
- `setBtAddress(...)` / `getBtAddress()`,
- `setChannel(...)` / `getChannel()`,
- and string rendering. 

This is an excellent example of SNode.C’s layer model at work.

A Bluetooth RFCOMM endpoint is clearly not an IP endpoint.

But it is still an address-bearing participant in the same architectural story.

#### Device address plus channel

RFCOMM’s endpoint idea is not “host plus port.”

It is better understood as:

- Bluetooth device identity,
- plus logical service channel.

That means the reader must resist the temptation to translate everything back into internet-language mentally.

A channel is not simply “a Bluetooth port number.”

It plays a service-identification role inside a different lower communication family.

#### Why RFCOMM is pedagogically valuable

RFCOMM helps demonstrate that the framework’s address abstractions are genuinely general rather than internet-centric.

It also prepares the reader to think well about device-near and IoT scenarios where Bluetooth is a primary communication option rather than a side feature.

### L2CAP addresses: same Bluetooth world, different service semantics

The current `net::l2::SocketAddress` class mirrors the RFCOMM pattern closely, but with a key semantic difference.

It offers:

- default construction,
- construction from Bluetooth address,
- construction from PSM,
- construction from Bluetooth address plus PSM,
- construction from an existing `sockaddr_l2`,
- initialization,
- `setBtAddress(...)` / `getBtAddress()`,
- `setPsm(...)` / `getPsm()`,
- and string rendering. 

#### PSM is not the same as channel

This is one of the places where it is important not to flatten the model too aggressively.

Both RFCOMM and L2CAP are Bluetooth-related families. Both use a Bluetooth address. Both attach a smaller service-like identifier.

But that identifier is *not the same thing* in the two families.

RFCOMM uses a channel. L2CAP uses a PSM.

That difference is exactly why SNode.C gives them distinct concrete address classes instead of trying to unify them into one Bluetooth-address type with some ambiguous second number.

This is a very good design decision.

### Constructors teach semantics

A reader can learn a surprising amount from constructor sets alone.

Across the five address families, the constructors tell a consistent story.

#### Default construction means wildcard or deferred specificity

The default constructor usually represents either a wildcard endpoint or a not-yet-fully-specific endpoint that will become concrete later.

#### Single-argument constructors expose the most natural partial identity

Examples include:

- port-only for IPv4 and IPv6,
- path-only for Unix domain sockets,
- channel-only for RFCOMM,
- PSM-only for L2CAP.

This is not arbitrary.

It reflects the most natural “partial endpoint” for each family.

A server often needs exactly that kind of partial specification.

#### Full constructors expose a concrete remote or fully specified local endpoint

Host-plus-port or Bluetooth-address-plus-channel/PSM constructors express a more concrete endpoint identity.

This makes them especially natural for remote-side configuration and for explicitly bound local addresses.

### Setters and getters are not merely convenience

Each address class provides setters and getters appropriate to its family.

That is not only for programmer comfort.

It reinforces the framework’s core educational idea:

> Endpoint identity should be named in the language of its family.

So instead of forcing everything through a generic key-value abstraction, the framework says:

- `setHost(...)`
- `setPort(...)`
- `setSunPath(...)`
- `setBtAddress(...)`
- `setChannel(...)`
- `setPsm(...)`

This is one of those small design choices that improves learnability enormously.

The names themselves teach what kind of endpoint the reader is configuring.

### String rendering is part of runtime literacy

All five concrete address classes expose `toString(...)`, and the IP-family classes also expose endpoint-formatting functionality.     

This may seem secondary, but it is actually part of runtime literacy.

A framework that logs or reports endpoint identity in poor ways becomes harder to operate.

SNode.C’s address objects keep formatting behavior close to endpoint semantics, which is exactly where it belongs.

This matters in practical situations such as:

- startup logging,
- status callbacks,
- error reporting,
- connect/listen diagnostics,
- teaching examples.

A good address string is often the first thing a reader or operator sees.

### Local and remote address thinking

Address semantics become much clearer once the reader starts thinking in local-versus-remote pairs.

A server usually cares most about a **local bind address**. A client usually cares most about a **remote peer address**. But both may have both sides conceptually present.

This is especially important because wildcard local addresses are often useful and normal.

For example:

- a client may leave its local side wildcarded,
- a server may bind to all interfaces,
- a Unix domain client may allow the local side to be chosen implicitly,
- a Bluetooth client may specify only the remote endpoint while leaving the local side less explicit.

Once the reader understands this, the address classes stop feeling like static data containers and start feeling like endpoint-role objects.

### Address semantics and the layer model

This chapter is not separate from the earlier layer chapter.

It is the concrete form of that chapter.

The address classes are where the network layer becomes tangible.

They show the reader:

- what counts as endpoint identity in each family,
- how wildcarding works in that family,
- which values belong naturally together,
- how higher layers can stay similar while lower identity rules differ.

In that sense, `SocketAddress` is one of the clearest bridges between architecture and code.

### Why IP families have richer resolution behavior

The IPv4 and IPv6 address classes differ from Unix domain, RFCOMM, and L2CAP in one especially interesting way.

They carry `Hints`, canonical-name access, and `useNext()` support. That strongly suggests a resolution pipeline in which a textual host may map to more than one candidate endpoint representation.  

This is a nice reminder that internet-style addressing often includes a name-resolution layer that local path addresses and Bluetooth endpoint specifications do not mirror in the same way.

So the richer IP-address API is not accidental feature growth.

It reflects actual differences in the semantics of those families.

### What readers should memorize — and what they should not

A teaching book should help the reader decide what deserves memorization.

For socket addresses in SNode.C, the reader does **not** need to memorize every constructor signature immediately.

What the reader *should* memorize is the conceptual map:

- IPv4 and IPv6: host plus port,
- Unix domain: path,
- RFCOMM: Bluetooth address plus channel,
- L2CAP: Bluetooth address plus PSM,
- default construction often means wildcard or deferred specificity,
- each family has its own concrete address class because endpoint identity is genuinely different.

If those ideas are stable, the concrete API becomes easy to rediscover.

### Common misunderstandings about addresses in SNode.C

It is worth clearing away a few misunderstandings explicitly.

#### Misunderstanding 1: “A socket address is just a string plus a number.”

Corrected view: a socket address is a family-specific endpoint identity object backed by a concrete address structure and family semantics.

#### Misunderstanding 2: “Default construction means uninitialized.”

Corrected view: default construction often intentionally expresses a wildcard or system-selectable endpoint.

#### Misunderstanding 3: “Bluetooth addresses are just IP-style addresses with different formatting.”

Corrected view: Bluetooth RFCOMM and L2CAP use different endpoint identity semantics from IP families, including channel and PSM distinctions.

#### Misunderstanding 4: “Unix domain sockets are just another IP family.”

Corrected view: Unix domain sockets are path-based local IPC endpoints and should be thought of in that local-operating-system sense.

#### Misunderstanding 5: “All address classes should have exactly the same surface.”

Corrected view: SNode.C keeps a shared pattern while allowing family-specific semantics to remain explicit, which is precisely the right design.

### Closing perspective

Socket addresses are where SNode.C’s lower-layer honesty becomes visible.

The framework does not hide the fact that different communication families identify endpoints differently.

Instead, it makes that difference explicit and teachable.

That gives the reader several advantages at once:

- clearer reasoning about bind and connect behavior,
- better understanding of wildcard semantics,
- more meaningful logging and diagnostics,
- and a stronger grip on how the network layer shapes the rest of the stack.

This also prepares the way for the next chapter.

Now that we understand what endpoint identity looks like, we can move from addresses to the larger communication roles built around them:

servers, clients, and the concrete connection objects that tie them to the runtime.
