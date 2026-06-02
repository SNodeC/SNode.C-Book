## Unix Domain Sockets
### Why Unix domain sockets deserve a separate chapter

After IPv4 and IPv6, Unix domain sockets are the next best family to study.

They are an excellent teaching step because they force the reader to change one important lower-layer assumption without changing the larger framework model.

With IPv4 and IPv6, endpoint identity is built around host and port.

With Unix domain sockets, endpoint identity is built around a local path.

That is a major semantic shift.

But it is *not* a shift in the overall SNode.C architecture.

You still have:

- a server or client instance,
- a factory,
- a context,
- a connection,
- runtime integration,
- status callbacks,
- and the same broad stream-based communication story.

That makes Unix domain sockets one of the cleanest demonstrations of what the framework’s layering really buys you.

### What changes — and what does not

This chapter should be read with one central question in mind:

> What happens when the lower-family identity stops being host-plus-port and becomes a filesystem-like local path?

The answer is pleasingly balanced.

What changes:

- the address family,
- the endpoint identity,
- bind/connect values,
- some deployment habits,
- the meaning of local and remote addresses.

What does not fundamentally change:

- the instance/factory/context/runtime pattern,
- the stream communication model,
- the distinction between status callbacks and connection lifecycle callbacks,
- the role of the `SocketConnection`,
- the meaning of legacy versus TLS at the connection layer.

That is exactly why Unix domain sockets belong here in the book.

They make the layer model tangible without forcing the reader to relearn the whole framework.

### The Unix domain address model

The current `net::un::SocketAddress` class is intentionally much simpler than the IPv4 and IPv6 address classes.

It is built around:

- default construction,
- construction from a `sunPath`,
- construction from an existing Unix-domain `sockaddr`,
- initialization,
- `setSunPath(...)` and `getSunPath()`,
- and string rendering.

That is exactly the right surface.

A Unix domain socket endpoint is not “a host with a strange name.”

It is a local IPC endpoint identified primarily by a path.

This difference is the first major thing the reader must internalize.

### Locality is the defining idea

A Unix domain socket is not about reaching a remote network host.

It is about local interprocess communication on the same machine.

That has several practical consequences.

First, the endpoint identity is more operating-system-local in character.

Second, deployment questions change. Instead of asking “Which interface and port should I expose?”, the reader often asks “Which path should represent this service locally?”

Third, the mental model of communication becomes more service-local and machine-local.

This makes Unix domain sockets especially attractive for:

- local service boundaries,
- toolchains and helper daemons,
- internal process-to-process APIs,
- development setups where network exposure is unnecessary,
- tightly local embedded or appliance-like systems.

SNode.C’s value here is that it lets the reader use this different lower-family identity without abandoning the rest of the framework model.

### The server-side convenience API

The live `net::un::stream::SocketServer` wrapper is very compact.

Its convenience forms are centered around Unix socket paths:

- `listen(const std::string& sunPath, ...)`
- `listen(const std::string& sunPath, int backlog, ...)`

and these overloads work by setting `Local::setSunPath(...)` and then delegating to the general `listen(onStatus)` path.

This is fully consistent with the teaching pattern we saw earlier for IPv4 and IPv6.

The convenience function is not a separate world.

It is simply a readable way to fill the instance configuration for the correct address family.

That is one of the framework’s most elegant recurring ideas.

### The client-side convenience API

The live `net::un::stream::SocketClient` wrapper is equally revealing.

Its convenience forms are:

- `connect(const std::string& sunPath, ...)`
- `connect(const std::string& sunPath, const std::string& bindSunPath, ...)`

This already teaches two important things.

First, the remote side of a Unix domain client is naturally expressed as a path.

Second, the local side can also be explicitly expressed as a path if desired.

This is a very nice example of how SNode.C preserves the local/remote distinction even in a family where the endpoint identity is path-based rather than host-based.

The reader should notice that the conceptual pattern is unchanged:

- remote endpoint identity still matters,
- local endpoint identity can still matter,
- the instance still expresses the outer communication role,
- the runtime still executes the actual connection lifecycle.

### The shape of a Unix-domain server

A Unix-domain stream server typically feels very much like the IPv4 and IPv6 servers already seen in this book.

In spirit, the code still looks like this:

```cpp
using LocalServer = net::un::stream::legacy::SocketServer<MyFactory>;

LocalServer server("local-service");
server.listen("/tmp/my-service.sock", 5, onStatus);
```

The important thing is not the exact snippet. The important thing is the stability of the pattern.

- There is still a named instance.
- There is still a convenience `listen(...)` call.
- There is still a status callback.
- There is still a runtime start afterwards.

The lower-family identity has changed, but the application architecture has not.

### The shape of a Unix-domain client

A Unix-domain client is just as instructive.

In spirit, it looks like this:

```cpp
using LocalClient = net::un::stream::legacy::SocketClient<MyFactory>;

LocalClient client("local-client");
client.connect("/tmp/my-service.sock", onStatus);
```

or, if a local bind path is also needed:

```cpp
client.connect("/tmp/my-service.sock", "/tmp/my-client.sock", onStatus);
```

Again, the pattern is the real lesson.

The client is still an outer role. The path merely replaces host-plus-port as the endpoint identity.

### Why Unix domain sockets are such a good transfer exercise

Unix domain sockets are the first family in the book where the endpoint identity stops looking like internet communication.

That is why this chapter matters so much.

It lets the reader test whether they have really understood the framework.

A reader who secretly still thinks:

> “SNode.C is basically a TCP framework with extras”

will feel this chapter as a disruption.

A reader who has really internalized the layer model will feel this chapter differently:

> “Ah, the family changed. The rest of the communication architecture remains recognizable.”

That second reaction is exactly what we want.

### Paths are endpoints, not filenames in disguise

It is useful to say this explicitly.

When using Unix domain sockets, the path should be thought of as the *endpoint identity* in the local IPC space.

That does not mean the path is “just a file” in the everyday human sense.

It means the framework is using filesystem-like naming to identify a local communication endpoint.

This matters because readers often bring the wrong instinct to Unix domain sockets.

They either over-network them mentally, or over-filesystem them mentally.

The better view is more precise:

- the path is the endpoint identity,
- the family is local IPC,
- the transport is still stream-oriented,
- the higher architecture is unchanged.

### Local and remote still matter here

One might think that once both sides are “just paths,” the local/remote distinction becomes less meaningful.

That would be a mistake.

The live client wrapper is a good reminder that the distinction still matters. The remote side is the target service path, while the optional local side can also be given an explicit bind path.

So even in Unix-domain communication, SNode.C keeps the directional structure clear:

- the server has a local listening path,
- the client has a remote service path,
- the client may also choose a local endpoint path.

This is a subtle but important continuity with the earlier IP-family chapters.

### Why Unix domain sockets often feel simpler than IP

Many developers find Unix domain sockets pleasantly simple once they stop expecting them to behave like IP networking.

That simplicity comes from several sources.

There is no remote host lookup. There is no interface selection in the IP sense. There is no port number to manage.

Instead, the endpoint identity is usually a local path that is immediately legible in deployment terms.

This simplicity makes Unix domain sockets excellent for local service architectures.

And it also makes them excellent teaching material, because they highlight how much of the framework is independent of IP-specific concepts.

### Why Unix domain sockets are not a replacement for IP

At the same time, the book should not romanticize them.

Unix domain sockets are not “better networking.”

They are a different lower-family choice.

They are extremely useful when communication is local to one machine.

They are not the right family when one process must communicate with a peer on another machine over a network.

SNode.C handles this very well by making the family choice explicit rather than pretending one communication family can represent all situations equally well.

That explicitness helps the reader choose well.

### The context and protocol logic do not need to become Unix-specific

This is one of the chapter’s most important lessons.

A `SocketContext` implementing a small request/response or streaming protocol does not need to become fundamentally “Unix-domain logic” just because it is now running over `net::un::stream::legacy`.

What changes is the carrier.

What often remains stable is:

- how the protocol reacts to `onConnected()`,
- how it reads data,
- how it sends data,
- how it handles disconnection,
- how it thinks in terms of one connection and one context.

That is exactly why the framework’s separation between lower layers and protocol behavior is so valuable.

### Legacy and TLS still make sense here

The earlier layer chapter already taught that `legacy` and `tls` are connection-layer variants, not separate application worlds.

Unix domain sockets fit into that same picture.

That means the reader should not think of Unix domain sockets as a special branch that somehow escapes the rest of the framework’s layering discipline.

They are simply another network family that can still participate in the same transport and connection-layer story.

This is a good place to remind the reader that SNode.C’s power comes from consistency of architectural treatment, not only from the number of supported families.

### Deployment habits are different here

Unix domain sockets change not only code values but operational instincts.

Instead of asking:

- Which IP address should I bind?
- Which port should I expose?

you more often ask:

- Which path should represent this service?
- Who will connect to it locally?
- How should this endpoint fit into my local service layout?

That shift is very healthy for the reader.

It helps make the lower-layer choice feel real rather than decorative.

### A note about cleanup and path ownership thinking

Even without going deep into operating-system mechanics, a teaching book should encourage the correct mindset here.

When a communication endpoint is identified by a path, lifecycle thinking naturally includes questions of local path management.

That is simply a consequence of the family’s semantics.

SNode.C does not erase that reality, and it should not.

The correct lesson is not that Unix domain sockets are complicated.

The correct lesson is that the family expresses locality differently, and responsible application design should respect that.

### Why this chapter prepares the Bluetooth chapters well

Unix domain sockets are also a useful bridge to the Bluetooth chapters.

Why?

Because they help the reader break the mental monopoly of host-plus-port identity without immediately jumping into Bluetooth-specific terminology such as device addresses, channels, and PSMs.

Once a reader has learned:

- “an endpoint can be a path”

it becomes much easier to later accept:

- “an endpoint can be a Bluetooth address plus a channel,”
- or “a Bluetooth address plus a PSM.”

So this chapter is a conceptual stepping stone, not just a feature chapter.

### Stream Unix domain sockets and the broader framework

One more point is worth making explicitly.

The current top-level build also includes a `net-un-dgram` component, which is a reminder that Unix domain communication in the framework is not limited in principle to one communication style only.

But for the book’s main architectural teaching path, stream Unix domain sockets are the right place to focus, because they preserve the same server/client/connection/context model that the reader already knows.

That keeps the learning curve smooth.

### Common misunderstandings about Unix domain sockets in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “Unix domain sockets are just IP sockets without a network.”

Corrected view: they are a different network family with path-based endpoint identity and local-IPC semantics.

#### Misunderstanding 2: “Changing from IPv4 to Unix domain requires a new application architecture.”

Corrected view: in SNode.C, the instance/factory/context/runtime pattern remains stable; the lower-family endpoint identity changes.

#### Misunderstanding 3: “A path-based endpoint means local/remote no longer matter.”

Corrected view: the distinction still matters, and the live client wrapper makes this explicit by supporting both remote and optional local Unix-domain paths.

#### Misunderstanding 4: “Unix domain sockets are only a side feature.”

Corrected view: they are a first-class family in the same layer model as IPv4, IPv6, RFCOMM, and L2CAP.

#### Misunderstanding 5: “Using a local family means the connection model becomes fundamentally different.”

Corrected view: with stream Unix domain sockets, the framework still expresses the same server/client/connection/context pattern.

### Closing perspective

Unix domain sockets are one of the most satisfying chapters in the whole lower-layer part of the book because they prove that the framework’s architecture is genuinely portable across endpoint identities.

The reader has now seen three different kinds of lower-family thinking:

- IPv4,
- IPv6,
- and path-based local IPC.

And yet the larger framework picture has remained recognizable throughout.

That is exactly the sign of a good architectural model.

The lower family can change radically while the communication roles, runtime integration, and application-protocol structure remain stable.

That is what SNode.C is teaching.

And now the reader is ready for the next step:

endpoint identities that are neither host-plus-port nor path-based, but Bluetooth-specific.

That means RFCOMM comes next.
