## MQTT over WebSocket
### Why this chapter deserves to stand on its own

The previous chapter introduced MQTT as a full application-layer family in SNode.C.

It already hinted at something especially interesting:

MQTT in the framework does not exist only in a native direct form.

It also exists as a WebSocket-carried protocol.

That composition deserves its own chapter because it is one of the clearest demonstrations of SNode.C’s architectural reach.

MQTT over WebSocket is not just a convenience feature.

It is a multi-layer composition in which all of the following remain visible and meaningful:

- the lower communication family,
- the stream transport,
- legacy or TLS connection handling,
- the HTTP layer,
- the HTTP upgrade boundary,
- the WebSocket layer,
- the WebSocket subprotocol layer,
- and finally the MQTT protocol family itself.

That is a remarkable stack.

And yet in SNode.C it still remains teachable.

This chapter explains why.

### The composition in one sentence

A good short definition is this:

> MQTT over WebSocket in SNode.C is MQTT expressed as a WebSocket subprotocol on top of the HTTP upgrade stack.

That sentence is simple, but it contains the whole architectural story.

It tells us that MQTT over WebSocket is not:

- ordinary native MQTT,
- ordinary HTTP,
- ordinary WebSocket without higher meaning,
- or some ad hoc mixture of the three.

It is a layered composition with a very clear semantic order.

### Why MQTT-over-WebSocket exists at all

A good technical book should pause on this question.

Why would a framework support MQTT over WebSocket instead of only native MQTT?

Because real systems often need MQTT semantics in environments where WebSocket is the more natural higher transport carrier.

That can happen when:

- the communication path already lives inside a web-facing architecture,
- a browser-adjacent or web infrastructure context matters,
- upgrade-based routing is already present,
- or protocol interoperability in a HTTP/WebSocket environment is desired.

The important point for the book is not to over-theorize the deployment scenarios.

The important point is to see what the framework is proving architecturally:

> the MQTT protocol family can remain itself while being carried over a richer, web-upgraded transport path.

That is exactly the kind of layered portability SNode.C was designed to support.

### The live build structure makes the composition explicit

The current live build structure is especially instructive here.

On the server side, the codebase builds both:

- `mqtt-server`
- and `mqtt-server-websocket`

On the client side, it builds both:

- `mqtt-client`
- and `mqtt-client-websocket`

This is already a strong architectural statement.

The framework is not treating MQTT-over-WebSocket as an application example glued together somewhere outside the protocol layers.

It is building it as an explicit supported protocol composition.

That is exactly the right design choice.

### The same MQTT protocol core participates in both worlds

One of the most satisfying architectural facts in the live code is that the MQTT-over-WebSocket story does not require a second completely separate MQTT semantics layer.

Instead, the framework keeps a shared MQTT protocol core and then composes it differently depending on the carrier.

That is exactly what a good full-stack framework should do.

A reader should see this as the high-level analogue of an earlier lesson from the lower families:

- the same protocol meaning,
- carried over a different lower path.

Now, however, the carrier difference is higher in the stack:

- native MQTT directly over the lower stream connection,
- or MQTT as a WebSocket subprotocol.

### The live `SubProtocol` class is the key architectural bridge

The most important live file for understanding this composition is `iot::mqtt::SubProtocol`.

It is templated on a WebSocket subprotocol role type and combines that role with MQTT-specific protocol behavior through `MqttContext`.

This is a very powerful design.

It means the framework is not creating a separate bespoke MQTT-over-WebSocket code path for every use case.

Instead, it defines a reusable MQTT subprotocol layer that can sit on top of a WebSocket subprotocol role.

That is exactly what layered architecture should look like.

### Server and client forms are almost beautifully small

The live server and client headers make this even more concrete.

On the server side:

- `iot::mqtt::server::SubProtocol`

is simply an alias of:

- `iot::mqtt::SubProtocol<web::websocket::server::SubProtocol>`

And on the client side:

- `iot::mqtt::client::SubProtocol`

is the corresponding alias of:

- `iot::mqtt::SubProtocol<web::websocket::client::SubProtocol>`

This is one of the most elegant architectural moves in the whole codebase.

The composition is almost perfectly visible in the type itself.

That is exactly the kind of thing a book like this should celebrate, because it shows that the abstractions are not only theoretical. They are paying off directly in the current live design.

### Why this type alias design is so good

The beauty of the two alias definitions is that they preserve both:

- reuse,
- and role clarity.

The generic MQTT-over-WebSocket logic is shared. The server/client role distinction remains explicit.

That is often the ideal outcome in a communication framework.

Too much reuse would blur the roles. Too little reuse would duplicate the protocol layer wastefully.

Here the balance is excellent.

### The composition stack should be read from bottom to top

A very helpful reading habit for this chapter is to read the stack in upward order.

For MQTT over WebSocket, the stack is conceptually:

1. lower communication family,
2. stream transport,
3. legacy or TLS connection handling,
4. HTTP layer,
5. HTTP upgrade,
6. WebSocket layer,
7. WebSocket subprotocol role,
8. MQTT semantics.

This is one of the richest protocol stacks in the framework, but it is still understandable because each layer has already been introduced earlier in the book.

That is exactly why the chapter works best here rather than earlier.

### MQTT-over-WebSocket does not erase MQTT identity

One possible misunderstanding is worth addressing directly.

A reader might worry that once MQTT is carried over WebSocket, it somehow stops being “real MQTT” and becomes just a web-flavored message stream.

The live architecture shows the opposite.

Because MQTT-over-WebSocket is built through a real MQTT subprotocol layer, the MQTT identity remains explicit.

The packet model, session thinking, publish-related behavior, and MQTT protocol semantics are not dissolved into generic WebSocket message handling.

That is exactly the right design outcome.

### WebSocket does not disappear either

The converse is also true.

WebSocket does not disappear simply because MQTT is riding on top of it.

The WebSocket layer still matters.

It still provides:

- the upgraded context,
- framing,
- control messages,
- client/server WebSocket roles,
- and the subprotocol layer boundary.

This is an important lesson because it teaches the reader to think about composite stacks without flattening them.

A good framework makes each layer visible enough that the reader can reason about where a concern belongs.

SNode.C does that very well here.

### MQTT-over-WebSocket is one of the strongest arguments for the subprotocol architecture

The previous WebSocket chapter introduced subprotocols conceptually.

This chapter now shows why they matter so much.

Without a real subprotocol architecture, MQTT-over-WebSocket would likely become one of two bad things:

- a hard-coded special case inside the WebSocket layer,
- or an application-level tangle that duplicates protocol-handling logic.

SNode.C avoids both.

By giving WebSocket subprotocols their own structured place, the framework lets MQTT-over-WebSocket be expressed as a normal, clean extension of the WebSocket layer.

That is excellent architectural practice.

### The live code also shows that runtime events still matter here

The live `iot::mqtt::SubProtocol` is not just a static adapter.

It includes:

- connection callbacks,
- message-start handling,
- message-data handling,
- message-end handling,
- disconnection handling,
- signal handling,
- and a dedicated `OnReceivedFromPeerEvent` event receiver.

This is very important for understanding the runtime story.

MQTT-over-WebSocket is not simply “messages show up somehow.”

It is a runtime-driven protocol composition.

The earlier chapters on event processing, contexts, diagnostics, and failure behavior remain relevant all the way up this stack.

That is one of the strongest themes of the book, and this chapter confirms it beautifully.

### Why the extra event receiver is architecturally interesting

The dedicated `OnReceivedFromPeerEvent` inside the generic MQTT subprotocol is especially revealing.

It shows that the composition is not only about reusing types. It is also about fitting MQTT protocol processing into the event-driven model cleanly.

This is exactly the kind of detail that proves the stack has been designed, not merely glued together.

A full-stack communication framework must ensure that each composed layer still behaves properly inside the runtime. The live code here gives strong evidence that SNode.C is doing that work seriously.

### The client/server packaging tells the operator story too

The presence of distinct installable artifacts for:

- MQTT native client/server,
- and MQTT-over-WebSocket client/server,

is also important operationally.

It tells the reader that the framework expects these to be real deployment choices, not just internal source-layout distinctions.

That matters because one of the strengths of SNode.C is that its architectural distinctions are often mirrored in:

- code structure,
- type structure,
- build structure,
- and deployment packaging.

That consistency is one of the reasons the framework is so teachable.

### Native MQTT and MQTT-over-WebSocket are siblings, not parent and child

A subtle but useful way to frame the architecture is this:

Native MQTT and MQTT-over-WebSocket are sibling ways of carrying the same protocol family.

One is not simply a “special version” of the other in a shallow sense.

They are two different compositions:

- one direct,
- one layered through WebSocket and HTTP upgrade.

This matters because it helps the reader avoid the wrong mental model.

MQTT-over-WebSocket is not merely “native MQTT with extra headers.”

It is a distinct protocol stack composition that happens to preserve the MQTT application-layer semantics above it.

### When the protocol stays the same but the carrier changes

This chapter is also one of the best places to reconnect with Chapter 15.

There we asked how the same protocol shape can survive movement across lower carriers.

MQTT-over-WebSocket now shows that the same principle applies even when the carrier change happens high in the stack.

The MQTT family remains MQTT.

But the carrying stack becomes:

- native direct stream-based transport,
- or HTTP upgrade into WebSocket and then MQTT as a subprotocol.

This is a richer and more advanced version of the same architectural lesson.

That makes the chapter especially satisfying.

### Diagnostics and failure behavior remain multi-layered here

A good operations-minded chapter should also say this plainly.

MQTT-over-WebSocket problems can occur at several different layers:

- lower connection establishment,
- TLS if present,
- HTTP upgrade,
- WebSocket control and framing,
- subprotocol selection,
- MQTT protocol behavior itself.

That is not a weakness.

It is simply the reality of a composed stack.

And it is exactly why SNode.C’s emphasis on visibility, runtime structure, and layer clarity matters so much.

A framework like this must make the stack understandable when something goes wrong.

The current architecture is well suited to that.

### Why this composition matters so much for integration systems

MQTT-over-WebSocket is one of the clearest examples of the framework’s usefulness in real integration systems.

It connects two worlds that are often treated separately:

- message-oriented MQTT systems,
- and web/upgraded WebSocket infrastructures.

SNode.C does not force the user to treat those worlds as disconnected.

It provides a structured way to compose them.

That is precisely the kind of capability that matters in broader IoT, dashboard, integration, and broker-adjacent systems.

### Common misunderstandings about MQTT over WebSocket in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “MQTT-over-WebSocket is just native MQTT with a different port.”

Corrected view: it is a layered composition through HTTP upgrade and the WebSocket subprotocol architecture.

#### Misunderstanding 2: “Once MQTT rides on WebSocket, the MQTT layer becomes less important.”

Corrected view: SNode.C keeps MQTT protocol identity explicit through its dedicated MQTT subprotocol layer.

#### Misunderstanding 3: “Once MQTT is present, the WebSocket layer becomes irrelevant.”

Corrected view: the WebSocket layer still matters for upgrade, framing, control messages, and subprotocol hosting.

#### Misunderstanding 4: “This composition is only an application example, not a first-class framework feature.”

Corrected view: the live build produces dedicated client/server MQTT-over-WebSocket artifacts, and the composition is modeled explicitly in the type and module structure.

#### Misunderstanding 5: “This chapter is only about transport tricks.”

Corrected view: it is really about how SNode.C composes protocol layers while keeping each layer’s identity intact.

### A good one-paragraph summary of the chapter

MQTT over WebSocket in SNode.C is a first-class layered protocol composition in which MQTT is expressed as a WebSocket subprotocol above the HTTP upgrade stack. The framework preserves MQTT protocol semantics through a dedicated generic `iot::mqtt::SubProtocol` layer, specializes it cleanly for WebSocket client and server roles, and packages it explicitly on both sides. This allows the same MQTT family to be carried either natively or through the web-upgrade stack without collapsing the architectural distinction among HTTP, WebSocket, subprotocol hosting, and MQTT itself.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the strongest demonstrations yet that SNode.C is a framework for protocol architecture, not only for protocol usage.

The reader has now seen a stack in which:

- HTTP matters,
- upgrade matters,
- WebSocket matters,
- subprotocols matter,
- and MQTT still remains itself above all of them.

That is exactly the kind of layered clarity a serious communication framework should provide.

And once the reader understands this composition, the next step becomes very natural.

Now that MQTT, WebSocket, HTTP, Bluetooth, and the lower carrier choices are all in view, the book can finally ask the more realistic systems question:

how an IoT system combines several of these protocol families at once without losing architectural clarity.
