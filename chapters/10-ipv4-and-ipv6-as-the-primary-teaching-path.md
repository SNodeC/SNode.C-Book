## IPv4 and IPv6 as the Primary Teaching Path
### Why IPv4 and IPv6 come first

SNode.C supports more than one lower communication family.

That is one of its strengths.

But when teaching the framework, it is still wise to begin with IPv4 and IPv6 before moving to Unix domain sockets, Bluetooth RFCOMM, or Bluetooth L2CAP.

This is not because the other families are secondary.

It is because IPv4 and IPv6 offer the clearest first view of the framework’s layered design while still staying close to what many readers already know.

They give us a path that is both familiar and revealing.

They are familiar because most readers already understand the broad ideas of host names, addresses, ports, listening servers, and remote peers.

They are revealing because SNode.C does not simply treat them as “normal sockets.” It presents them through the same instance, connection, context, and configuration patterns that govern the rest of the framework.

That makes IPv4 and IPv6 the best primary teaching path.

### Why IPv4 and IPv6 are especially good teaching families in SNode.C

The live repository makes one very important thing clear: the IPv4 and IPv6 stream server/client APIs are intentionally very parallel.

There is a `net::in::stream::SocketServer` and `SocketClient` for IPv4, and a `net::in6::stream::SocketServer` and `SocketClient` for IPv6. In both families, the convenience overloads work by filling the instance configuration and then delegating to the more general parameterless `listen(...)` or `connect(...)` path. That is a beautiful teaching design, because it lets the reader see that the “easy” API and the “configured” API are really one model rather than two separate worlds.    

This is one of the clearest demonstrations of SNode.C’s architecture.

A convenience overload is not magic. It is usually just a readable front door into the configuration model.

That is exactly what a teaching framework should do.

### The shared teaching pattern

For both IPv4 and IPv6, the outer application pattern is the same.

You still have:

- a `SocketServer` or `SocketClient` instance,
- a `SocketContextFactory`,
- a `SocketContext`,
- a runtime started through `core::SNodeC::start()`.

Nothing about moving from IPv4 to IPv6 changes that shape.

This is the first major lesson of the chapter.

> The instance/factory/context/runtime pattern is more fundamental than the specific IP family.

That is why IPv4 and IPv6 are such good teaching companions. They let the reader practice “same shape, different lower-family semantics” in a way that is easier to grasp than jumping immediately to a path-based Unix domain socket or a Bluetooth family.

### The concrete type names already teach the layers

Let us start with the concrete legacy stream server/client types.

For IPv4, a minimal pair typically looks like:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;
```

For IPv6, the parallel pair looks like:

```cpp
using EchoServer6 = net::in6::stream::legacy::SocketServer<MyFactory>;
using EchoClient6 = net::in6::stream::legacy::SocketClient<MyFactory>;
```

These type names are already doing educational work.

The only thing that changes in the example above is the network family namespace:

- `net::in` for IPv4,
- `net::in6` for IPv6.

Everything else in the layered story remains recognizably stable:

- `stream` transport,
- `legacy` connection handling,
- `SocketServer` or `SocketClient` outer role.

This stability is the main reason to teach the two families together.

### The address classes are parallel on purpose

Chapter 8 already introduced the address classes.

Now we can use them to explain why the IPv4/IPv6 teaching path works so well.

The live `net::in::SocketAddress` and `net::in6::SocketAddress` classes have a very similar conceptual interface:

- default constructor,
- host-only constructor,
- port-only constructor,
- host-plus-port constructor,
- construction from an existing `sockaddr`,
- `Hints`,
- `init(...)`,
- `useNext()`,
- `setHost(...)` / `getHost()`,
- `setPort(...)` / `getPort()`,
- canonical-name access,
- string rendering,
- endpoint formatting.  

This is a huge pedagogical advantage.

It means the reader can learn one address pattern and then apply it to both IP families.

At the same time, the framework does not pretend that the families are identical. The default wildcard host differs, the operational semantics differ, and later the dual-stack question appears. But the shared surface gives the reader confidence before the deeper differences matter.

### Default construction: `0.0.0.0` and `::`

One of the best places to compare IPv4 and IPv6 is the meaning of their default addresses.

In the live headers:

- IPv4 defaults to host `0.0.0.0` and port `0`,
- IPv6 defaults to host `::` and port `0`.  

This is exactly the kind of detail a teaching chapter should slow down for.

These are not random defaults.

They express wildcard local addresses in their respective families.

That means:

- a server can listen without being tied to one specific interface,
- a client can allow the local side to be selected automatically,
- and the framework can model “not yet concretely chosen” without using fake null values.

This is one of the first important moments where the reader sees that SNode.C is teaching good socket semantics, not hiding them.

### The convenience `listen(...)` overloads reveal the teaching model

The current IPv4 and IPv6 stream server wrappers are extremely informative here.

For IPv4, the live convenience overloads include forms such as:

- `listen(uint16_t port, ...)`
- `listen(uint16_t port, int backlog, ...)`
- `listen(const std::string& ipOrHostname, uint16_t port, ...)`
- `listen(const std::string& ipOrHostname, uint16_t port, int backlog, ...)` 

For IPv6, the same conceptual overloads exist with the same overall structure. 

The most important thing is not the overload count itself.

The most important thing is what these functions actually do.

They set fields on the configuration object:

- local host,
- local port,
- backlog,

and then call the parameterless `listen(onStatus)` path.

That is a major teaching point.

The reader should understand this as:

> IPv4 and IPv6 convenience APIs are readable shorthands for the same underlying instance-configuration model.

This is one of the cleanest examples in the framework of architecture showing through the surface API.

### The convenience `connect(...)` overloads tell the same story

The live IPv4 and IPv6 client wrappers mirror the server-side idea.

For IPv4, the current wrapper supports forms such as:

- `connect(host, port, ...)`
- `connect(host, port, bindHost, ...)`
- `connect(host, port, bindPort, ...)`
- `connect(host, port, bindHost, bindPort, ...)` 

For IPv6, the same conceptual forms are present. 

And again, these are not alternate models of connection.

They are configuration-setting fronts for the general connect path.

This is one of the reasons it makes sense to teach IPv4 and IPv6 before more exotic families.

The reader can see a very stable connection story:

- remote host and port define the peer,
- optional local bind information can refine the local side,
- the status callback reports the outer result,
- and the rest of the lifecycle continues through the runtime as usual.

### Why IPv4 is still the easiest first concrete example

Although this chapter teaches IPv4 and IPv6 together, IPv4 remains the easiest first concrete example.

That is not because it is more important.

It is because its textual representation and everyday expectations are simpler for many readers.

A first minimal server often looks like this in spirit:

```cpp
using EchoServer4 = net::in::stream::legacy::SocketServer<MyFactory>;

EchoServer4 server("echo4");
server.listen(8080, 5, onStatus);
```

and the matching client like this:

```cpp
using EchoClient4 = net::in::stream::legacy::SocketClient<MyFactory>;

EchoClient4 client("echo4");
client.connect("localhost", 8080, onStatus);
```

This is a teaching sweet spot.

The reader sees host plus port, server plus client, status plus runtime, but without yet having to think about the distinct psychological hurdles of IPv6 textual notation.

### Why IPv6 should follow immediately after IPv4

If a book waits too long before introducing IPv6, readers unconsciously begin to think of IPv4 as the “real” case and everything else as special handling.

That would be a mistake in a book about SNode.C.

Because the live API is so parallel between the two families, the right teaching move is to introduce IPv6 almost immediately after the first stable IPv4 picture.

This helps the reader notice the correct pattern:

- the framework shape remains stable,
- the lower-family semantics shift,
- and the API remains intentionally familiar.

This is a much better lesson than teaching IPv4 in depth and then later treating IPv6 as an appendix.

### The first true difference: textual and conceptual address form

Once the reader has absorbed the structural symmetry, the next step is to become honest about the differences.

The first difference is the simplest one:

IPv4 and IPv6 do not merely differ by “using different numbers.”

They carry different address forms, different wildcard forms, and sometimes different operational assumptions.

That means a reader should not think:

> IPv6 is just IPv4 with longer text.

The framework does not make that mistake.

It gives IPv4 and IPv6 separate namespaces and separate address classes, even though the high-level usage pattern stays intentionally close.

That is exactly the right balance.

### The second true difference: dual-stack thinking

A major practical teaching point enters with IPv6.

The current README explicitly notes that SNode.C supports IPv6 in both single- and dual-stack forms, and the configuration documentation also calls out an `ipv6-only` option for IPv6 server and client instances. 

This is the moment where the book should gently slow down.

Dual-stack behavior is one of those topics that often confuses readers when it is postponed until debugging time.

So the conceptual lesson should be stated early:

> An IPv6 endpoint is not only about IPv6 text syntax. It may also raise the question of whether one socket should handle only IPv6 or both IPv6 and IPv4, depending on OS behavior and configuration.

That is one of the reasons IPv6 deserves its own family and not just an overloaded IPv4 mode.

### Same pattern, different deployment instincts

Another important teaching distinction is not in the API itself but in how developers tend to think when deploying.

With IPv4, many readers instinctively think in terms of:

- localhost testing,
- private LAN addresses,
- simple externally reachable services.

With IPv6, the same reader should be encouraged to think more explicitly about:

- family selection,
- wildcard meaning,
- whether the instance is intended to be IPv6-only,
- and how address resolution may behave.

SNode.C’s design supports both, but the book must help the reader bring the right questions to each family.

### Why both families still use the same protocol logic

At this point, the most important transfer lesson should be stated directly.

If you write a protocol in a `SocketContext`, that protocol does not suddenly become an “IPv4 protocol” or an “IPv6 protocol.”

What changes is the lower communication family and therefore:

- address representation,
- bind/connect configuration,
- and some environmental behavior.

What often remains the same is:

- the context class,
- the factory structure,
- the event-driven lifecycle,
- the outer instance role,
- the status-callback model,
- and the connection abstraction.

This is the real reason IPv4 and IPv6 are the primary teaching path.

They let the reader feel this transfer very clearly without needing to jump into a wholly different kind of endpoint identity such as a Unix path or Bluetooth address.

### A helpful teaching sequence for examples

For this book, the best sequence is not to write one enormous dual-family example immediately.

A better sequence is:

1. show a minimal IPv4 legacy pair,
2. show the corresponding IPv6 legacy pair,
3. point out what changed in code,
4. point out what did **not** change in architecture,
5. then revisit the two again later under TLS.

This sequence keeps the lower-family comparison sharp without overwhelming the reader.

### A small but useful lesson from the live wrappers

The live wrappers make another nice teaching point visible.

Because the convenience overloads directly set fields such as `Local::setPort(...)`, `Local::setHost(...)`, `Remote::setHost(...)`, and `Remote::setPort(...)`, the reader can see that SNode.C thinks in terms of **local** and **remote** address roles even for the simplest IP examples.    

That is another reason to teach IP families first.

The local/remote distinction is easiest to internalize when the endpoint identity is still the familiar host-plus-port shape.

### What changes when we move from IPv4 to IPv6 in code

A reader often wants a direct answer to this question.

In a typical minimal SNode.C teaching example, the code-level changes from IPv4 to IPv6 are often surprisingly small.

Usually they involve:

- changing the family namespace from `net::in` to `net::in6`,
- using the IPv6 `SocketAddress` type,
- adjusting literal host names or addresses as needed,
- and possibly considering IPv6-only versus dual-stack configuration.

That is intentionally modest.

The framework is trying to preserve architectural transfer, not force needless rewrites.

### What does **not** change when we move from IPv4 to IPv6

This question is even more important.

In the normal teaching path, the following do **not** fundamentally change:

- how the runtime is initialized,
- how the event loop is started,
- what a server or client instance is,
- what a context factory is,
- what a context does,
- how connection lifecycle callbacks fit in,
- how status callbacks fit in,
- how the layered type names are read.

This stable core is the real lesson.

If the reader finishes this chapter with only one durable insight, it should be this one.

### A note about learning order and confidence

There is a psychological reason to keep IPv4 and IPv6 together but not identical.

If the book presents IPv6 as if it were mysterious and special, readers become nervous.

If the book presents IPv6 as if it were literally no different from IPv4, readers become overconfident and later confused.

The correct teaching tone is calm and precise:

- the two families are close enough that transfer should feel natural,
- but different enough that the family still matters.

That is exactly the kind of balance SNode.C’s API encourages.

### A subtle live-code note

There is one small reason this chapter is especially worth grounding in the current repository.

The live IPv4 and IPv6 stream wrappers are almost exact mirrors, but not mechanically identical in every line. That is a useful reminder for advanced readers: always treat the current source as the final authority for exact overload behavior.

For the book’s teaching path, however, the important truth remains unchanged:

the two families are architecturally parallel enough to serve as the best primary comparison pair in the framework.

### Common misunderstandings about IPv4 and IPv6 in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “IPv4 is the normal case and IPv6 is an advanced variant.”

Corrected view: both are first-class families in the framework, and they should be learned as parallel primary cases.

#### Misunderstanding 2: “Moving from IPv4 to IPv6 requires a new application architecture.”

Corrected view: in SNode.C, the instance/factory/context/runtime pattern remains the same; the lower-family semantics change.

#### Misunderstanding 3: “Convenience overloads are a separate API model.”

Corrected view: they are readable fronts for the same underlying instance configuration model.

#### Misunderstanding 4: “IPv6 is just IPv4 with longer addresses.”

Corrected view: IPv6 has its own address family, wildcard semantics, and dual-stack questions, even though the high-level API remains intentionally similar.

#### Misunderstanding 5: “Once I understand host and port, I understand the whole story.”

Corrected view: host and port are only the visible tip; status reporting, local/remote roles, wildcarding, and family selection still matter.

### Closing perspective

IPv4 and IPv6 are the best primary teaching path in SNode.C because they let the reader learn the right lesson at the right level.

They are similar enough to make transfer visible. They are different enough to keep the network family concept honest. And the current repository’s live wrappers make that teaching strategy especially strong, because their convenience APIs are structurally parallel and transparently tied to the same configuration model.

This is exactly the kind of chapter that should strengthen confidence.

The reader should leave it thinking:

- I understand why IPv4 is the easiest first concrete example.
- I understand why IPv6 should follow immediately.
- I understand what changes between them.
- And most importantly, I understand what does **not** change.

That is the right preparation for the next two family chapters.

Once IPv4 and IPv6 are secure in the mind, the reader is ready to see just how far the same framework model extends when endpoint identity is no longer host-plus-port at all.

That is where Unix domain sockets come next.
