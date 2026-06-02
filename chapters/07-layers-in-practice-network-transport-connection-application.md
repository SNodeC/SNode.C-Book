## Layers in Practice: Network, Transport, Connection, Application
### Why this chapter comes here

By now, we have built two kinds of understanding.

First, we have learned the **application-facing pattern** of SNode.C:

- instances,
- factories,
- contexts,
- and event-driven lifecycle.

Second, we have learned the **runtime-facing pattern**:

- the `SNodeC` façade,
- the event loop,
- the multiplexer,
- descriptor and timer event processing.

What still remains is the framework’s layered communication model itself.

That is what this chapter explains.

This is an especially important chapter because the word *layered* is easy to say and surprisingly easy to misunderstand. In SNode.C, layering is not a vague architectural slogan. It is a practical way of organizing communication concerns so that:

- lower communication families stay visible,
- common structure can still be reused,
- TLS can be inserted without destroying the application model,
- and higher-level protocol frameworks can be built on top without forgetting what lies beneath.

The goal of this chapter is therefore not to list namespaces mechanically. The goal is to teach the reader how to *think across the layers*.

### The four-layer picture

The README of the current repository presents the framework in four main communication levels:

- network layer,
- transport layer,
- connection layer,
- application layer.

That four-part picture remains the best teaching entry point. It matches the framework’s intent well and still aligns with the current module structure and supported build components. The current top-level build also confirms that `net`, `web`, `express`, `iot`, and related feature components are not accidental extras but deliberate parts of the framework’s layer story.  

A concise first description looks like this:

- the **network layer** answers *where and by what family are we communicating?*
- the **transport layer** answers *what kind of communication form do we assume?*
- the **connection layer** answers *how is the concrete peer connection handled, including encryption?*
- the **application layer** answers *what protocol or framework behavior runs over that connection?*

That sounds abstract, so let us make it concrete immediately.

### The network layer: choosing the communication family

At the network layer, SNode.C distinguishes among several communication families.

The current README presents five primary network families and associates them with dedicated namespaces:

- IPv4 → `net::in`
- IPv6 → `net::in6`
- Unix domain sockets → `net::un`
- Bluetooth RFCOMM → `net::rc`
- Bluetooth L2CAP → `net::l2` 

This is already a very important design choice.

Many frameworks make one lower family feel “normal” and all others feel like special cases. SNode.C instead places these families side by side in one conceptual picture.

That does **not** mean they are identical.

They differ in:

- addressing,
- operating-system behavior,
- binding and connect semantics,
- and practical use cases.

But they are all treated as legitimate lower communication families within one framework story.

#### Why the namespace split matters

The namespace split is more than naming.

It gives the reader a stable way to map concepts to the codebase.

When you see `net::in`, you know you are in the IPv4 family. When you see `net::rc`, you know you are dealing with Bluetooth RFCOMM. When you see `net::l2`, you know you are in Bluetooth L2CAP.

This consistency matters because one of the framework’s strengths is transfer across families.

A reader should be able to ask:

> I understand the structure for `net::in`. What changes if I move to `net::un` or `net::rc`?

That is exactly the right question.

### The network layer is where addresses become meaningful

One of the clearest ways to understand the network layer is through address semantics.

Every network family brings its own `SocketAddress` type.

That means the framework is not pretending that all endpoint identities are the same thing.

An IPv4 address with a port is not the same kind of endpoint as:

- an IPv6 address with a port,
- a Unix domain socket path,
- a Bluetooth device address plus RFCOMM channel,
- or a Bluetooth device address plus L2CAP PSM.

This is a key design virtue.

The framework reuses the *pattern* of addressing while still respecting the *specifics* of each family.

That is the right balance between abstraction and honesty.

### Transport in SNode.C: not all communication is the same shape

Above the network family sits the transport layer.

The current README emphasizes that, in the relevant parts of SNode.C, the main transport abstraction is `stream`. For IPv4 and IPv6 this corresponds to TCP-style connection-oriented communication. The transport layer is presented as a template-based base layer that is then specialized for the individual network families. 

This is one of the places where the framework’s design becomes especially elegant.

It does **not** flatten everything into “a socket.”

Instead, it says:

- first decide which network family you are in,
- then decide what transport form that communication takes.

That distinction is conceptually important even when the concrete transport options are still limited.

#### Why `stream` matters pedagogically

A stream transport gives us a stable mental model for a large part of the framework.

It means the reader can understand:

- establishment of a peer relationship,
- sustained connection lifetime,
- reading and writing over time,
- connection-level timeouts,
- shutdown and disconnection,
- TLS wrapping at the connection layer.

In other words, `stream` is not merely a transport keyword. It is the transport form that allows the rest of the framework story to unfold clearly.

### Transport specializations: where the family and transport meet

Once network family and transport form are combined, we get transport specializations such as:

- `net::in::stream`
- `net::in6::stream`
- `net::un::stream`
- `net::rc::stream`
- `net::l2::stream` 

This is the first place where the mental model becomes especially practical.

When you read a type such as:

```cpp
net::in::stream::legacy::SocketServer<...>
```

you are not looking at one arbitrary long type name.

You are looking at a layered statement.

It says:

- network family: IPv4,
- transport form: stream,
- connection handling: legacy,
- instance role: server.

Once the reader learns to parse types this way, SNode.C becomes much less intimidating.

### The connection layer: where the peer relationship becomes concrete

If the network layer chooses the family and the transport layer chooses the communication form, then the connection layer answers a deeper operational question:

> How is this concrete peer connection handled while it exists?

The README describes the connection layer as the part responsible for physical data exchange and, where applicable, encryption and decryption. It also distinguishes two major connection-layer variants:

- `core::socket::stream::legacy`
- `core::socket::stream::tls` 

This is one of the most important layers in the framework because it is where communication stops being an abstract possibility and becomes an actual managed connection.

#### Why the connection layer is not the same as the transport layer

It is tempting to blur transport and connection together, especially in informal discussion.

But SNode.C benefits from keeping them distinct.

The transport layer tells us the general communication shape: stream-oriented.

The connection layer tells us what concrete machinery handles the active peer relationship over that transport.

That distinction becomes especially valuable when TLS is involved.

### Legacy versus TLS is a layer insertion, not an application rewrite

One of the framework’s most useful architectural properties is the way TLS fits into the model.

The README presents the connection layer as having two versions:

- unencrypted (`legacy`)
- encrypted (`tls`) 

This is an excellent teaching pattern because it helps the reader see TLS for what it is in SNode.C:

not a totally separate application world, but an inserted connection-handling layer.

That means a great deal of application logic can remain conceptually unchanged while the connection handling below it changes.

This has major consequences.

#### What often stays the same

When moving from legacy to TLS, the reader can often keep:

- the same general instance/factory/context structure,
- the same application protocol logic,
- the same runtime understanding,
- the same broad lower-family choice.

#### What changes

What changes is the connection machinery:

- handshake behavior,
- certificate material,
- SNI or peer-validation concerns,
- timing and callback detail around establishment.

That is exactly the kind of change a good layer model should isolate.

### Connection-layer specializations: the practical combinations

The current README makes the next step explicit by listing concrete combinations such as:

- `net::in::stream::legacy`
- `net::in::stream::tls`
- `net::in6::stream::legacy`
- `net::in6::stream::tls`
- `net::un::stream::legacy`
- `net::un::stream::tls`
- `net::rc::stream::legacy`
- `net::rc::stream::tls`
- `net::l2::stream::legacy`
- `net::l2::stream::tls` 

This is where the framework’s design reveals its power most clearly.

Instead of inventing a totally new API family for each situation, SNode.C builds a matrix of meaningful combinations.

This means the reader can think in a structured way:

- pick a network family,
- use the stream transport model,
- choose whether the connection layer is legacy or TLS,
- attach the application protocol.

That is not just convenient.

It is intellectually clean.

### The application layer: where protocols and sub-frameworks live

Above the connection layer sits the application layer.

This is where the framework’s higher-level protocol support becomes visible.

The current README identifies several application-layer families and namespaces:

- HTTP → `web::http`
- WebSocket → `web::websocket`
- Express-like web layer → `express`
- MQTT → `iot::mqtt` 

The current top-level build also confirms these as real supported component families, with targets for HTTP, Express-based HTTP server combinations, WebSocket server/client, MQTT server/client, and MQTT over WebSocket. 

This is an important moment in the book, because it clarifies something readers often wonder early on:

> Is SNode.C basically a socket framework with some extras, or does it genuinely support higher-level protocol systems?

The answer is clearly the second.

But the framework’s real strength is not merely that those higher-level protocols exist.

Its real strength is that they do **not** erase the lower-layer model.

### The application layer is not “above sockets and therefore unrelated”

A common beginner mistake is to imagine a sharp psychological break.

Below: “network code.” Above: “web code” or “MQTT code.”

SNode.C helps the reader avoid that mistake.

HTTP, WebSocket, Express-like web APIs, and MQTT do not float above the lower layers as disconnected universes.

They are application-layer behaviors *carried by* the lower layers.

This is why the layer model matters so much.

A reader who understands the lower layers can ask much better questions about the higher layers.

For example:

- What lower family is my web application actually using?
- Is this MQTT application running natively over a stream connection or via WebSocket?
- Where does TLS sit relative to the web or MQTT layer?
- What part of the model changes if I move a service from IPv4 to Unix domain sockets locally?

These are exactly the kinds of questions SNode.C prepares the reader to ask.

### The build system confirms the layer story

One of the best ways to test whether an architectural description is real is to see whether the build reflects it.

In the current top-level `src/CMakeLists.txt`, the supported components list includes entries such as:

- `core`
- `core-socket-stream-legacy`
- `core-socket-stream-tls`
- `net-in-stream-legacy`
- `net-in6-stream-legacy`
- `net-un-stream-legacy`
- TLS counterparts,
- Bluetooth-related network stream components when enabled,
- `http`, `http-server`, `http-client`,
- multiple `http-server-express-*` combinations,
- `websocket-server`, `websocket-client`,
- `mqtt`, `mqtt-server`, `mqtt-client`,
- and WebSocket-carried MQTT variants. 

This is a strong sign that the layer model is not merely conceptual documentation.

It is embedded in the framework’s actual packaging and component structure.

That matters for the reader because it means the layers are not only educationally neat. They are operationally real.

### A practical way to read long SNode.C type names

At this point, it is worth teaching a specific reading technique.

When you see a long SNode.C type, read it from left to right as a layered stack.

For example:

```cpp
net::in::stream::legacy::SocketClient<MyFactory>
```

should be read as:

- `net::in` → IPv4 family,
- `stream` → connection-oriented stream transport,
- `legacy` → unencrypted connection handling,
- `SocketClient` → client instance role,
- `MyFactory` → per-connection application-context producer.

A similar type such as:

```cpp
net::rc::stream::tls::SocketServer<MyFactory>
```

becomes:

- Bluetooth RFCOMM family,
- stream transport,
- TLS connection handling,
- server instance role,
- application-context factory.

This reading habit is one of the fastest ways to become comfortable with the framework.

### What the layer model gives the reader in practice

It is now worth stepping back and asking what the layer model actually buys us.

#### It gives us controlled variation

A reader can change one part of the stack without imagining that everything has changed.

#### It keeps lower layers visible

That helps both learning and debugging.

A service is not just “a web thing.” It is a web thing over specific lower communication layers.

#### It keeps higher layers meaningful

Because the lower layers are explicit, higher-level protocols do not become vague magic. They stay grounded in a real communication model.

#### It encourages reuse of application structure

The instance/factory/context pattern can be reused across many lower-layer choices.

This is one of the deepest advantages of SNode.C.

### Where Bluetooth fits in this chapter — and why it matters here

Bluetooth must be part of this chapter, not postponed to a later “special topics” corner.

Why?

Because Bluetooth RFCOMM and Bluetooth L2CAP are not exceptions to the model.

They are confirmations of the model.

They show that SNode.C’s layer design is not only about internet-facing families such as IPv4 and IPv6. It can also treat short-range and local-device communication families as first-class participants in the same architectural scheme. The README explicitly places RFCOMM and L2CAP beside IPv4, IPv6, and Unix domain sockets in the network layer table and likewise carries them through the transport and connection specialization tables. 

That is one of the reasons the framework is especially interesting for IoT, embedded, and device-near systems work.

### One protocol, many lower carriers

This chapter becomes most useful when the reader asks the transfer question.

Suppose we write one simple application protocol using a `SocketContext`.

What changes if the same protocol is carried over:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP?

The answer is subtle but beautiful.

Some things change:

- address syntax,
- bind/connect semantics,
- environment assumptions,
- some configuration details,
- operational deployment patterns.

But some things remain remarkably stable:

- the event-driven runtime,
- the instance/factory/context pattern,
- the broad connection lifecycle,
- the application-protocol endpoint concept,
- the idea that TLS can wrap the connection layer,
- the idea that higher-level protocol frameworks can still sit above.

That stable remainder is the true value of the layer model.

### A note on honesty: layers are real, but not walls

A good systems book should avoid two opposite mistakes.

The first mistake is to deny layering and collapse everything into one big communication soup.

The second mistake is to imagine layers as perfectly sealed walls that never influence one another.

SNode.C avoids the first mistake well. As readers, we should avoid the second.

The layers are real and useful, but they still influence each other.

For example:

- a network family affects address shape and configuration,
- the connection layer affects callback timing and security behavior,
- the application layer may care about connection semantics and transport assumptions,
- the runtime must carry all of them coherently.

So the right mental picture is not “independent boxes.”

The right picture is “cooperating layers with clear primary responsibilities.”

### Common misunderstandings about layering in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “The network layer is just another name for sockets.”

Corrected view: the network layer identifies the communication family and therefore shapes addressing, binding, and endpoint identity.

#### Misunderstanding 2: “Transport and connection are the same thing.”

Corrected view: the transport layer expresses the communication form, while the connection layer expresses how a concrete peer relationship is managed over that transport.

#### Misunderstanding 3: “TLS creates a separate application world.”

Corrected view: TLS is best understood as an inserted connection-layer variant, not as a rewrite of the application layer.

#### Misunderstanding 4: “Higher-level protocols make lower layers irrelevant.”

Corrected view: HTTP, WebSocket, Express-like web APIs, and MQTT remain carried by explicit lower layers and are easier to reason about when those remain visible.

#### Misunderstanding 5: “Bluetooth is outside the main framework model.”

Corrected view: Bluetooth RFCOMM and Bluetooth L2CAP are first-class network families in the same architectural scheme as IPv4, IPv6, and Unix domain sockets.

### Closing perspective

If the runtime chapter explained **how the framework keeps moving**, this chapter has explained **what exactly is being carried through that runtime**.

SNode.C’s layered communication model is one of its strongest architectural features.

It gives the reader a way to think clearly about:

- communication family,
- transport shape,
- connection handling,
- and application protocol behavior.

That clarity is what makes the framework scalable in the mind.

A simple echo application, an HTTPS web server, a WebSocket-based service, an MQTT client, and a Bluetooth-facing device endpoint can all belong to one coherent conceptual world.

That is the promise of the layers.

And now that the reader has both the runtime model and the layer model, we are ready for the next step:

to move back downward and examine concrete lower-layer choices in detail, beginning with addresses and address semantics.
