## The Mental Model of SNode.C
### Why a mental model matters more than memorizing APIs

A framework like SNode.C can be approached in two very different ways.

The first way is to treat it as a list of names.

One memorizes that there is a `SocketServer`, a `SocketClient`, a `SocketContext`, a `SocketContextFactory`, several `listen(...)` overloads, several `connect(...)` overloads, multiple namespaces for different network families, and later still more types for HTTP, WebSocket, Express-like routing, and MQTT.

That approach can produce small successes quickly, but it has a hard limit. The moment the application becomes slightly less standard, the reader begins asking structural questions that a mere list of names cannot answer.

Why is a context created per connection?

Why does a factory exist at all?

What exactly does the runtime do after `listen(...)` or `connect(...)` is called?

Why can so much of the same application logic survive a change from IPv4 to Unix domain sockets or Bluetooth?

Why does TLS feel like an inserted layer rather than a completely different application model?

These are not API questions. They are mental-model questions.

The second way to learn SNode.C is therefore the better one: learn the shape of the framework first, and let the individual APIs attach themselves to that shape.

That is the goal of this chapter.

A good mental model does not tell you every detail. It tells you what kind of thing each part *is*, what job it has, where the boundaries are, and how control and data move through the system.

Once that is clear, most of SNode.C becomes much easier to predict.

### The shortest accurate picture of SNode.C

If we compress the framework to one sentence, we can say this:

> SNode.C is an event-driven, layer-based framework in which server and client instances create per-connection application contexts that run on top of configurable lower communication layers.

That sentence contains almost the entire book.

Let us unpack it carefully.

- **event-driven** means the user does not manually drive the communication loop with blocking read/write logic in application code;
- **layer-based** means network family, transport, connection handling, and application protocol are conceptually separated;
- **server and client instances** are the outer communication objects the user creates;
- **per-connection application contexts** are the concrete protocol endpoints that react to events;
- **configurable lower communication layers** means the same general application shape can be reused across IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, and, where appropriate, TLS.

Each of those phrases becomes much less abstract once we connect it to the current codebase.

### The runtime is a central coordinator, not an afterthought

At the top of the runtime picture sits `core::SNodeC`.

In the current repository, `core::SNodeC` offers the static lifecycle functions `init(...)`, `start(...)`, `stop()`, `tick(...)`, `free()`, and `state()`. Even without seeing the implementation details, the public surface already tells us something important: the framework treats initialization, event-loop execution, and shutdown as explicit runtime phases rather than incidental side effects. 

This matters because SNode.C is not designed as a passive library that simply waits for you to call a few helper functions. It has a runtime posture.

That posture becomes even clearer in the current `SocketServer` and `SocketClient` templates. In both classes, the actual begin-listening or begin-connecting work is not performed directly and synchronously inside the public `listen(...)` or `connect(...)` entry point. Instead, the operation is scheduled via `core::EventReceiver::atNextTick(...)`, and the framework then proceeds when the event system is ready.  

This is a crucial mental-model point.

When you write:

```cpp
server.listen(...);
client.connect(...);
```

you are not “doing everything now” in a blocking procedural sense.

You are *declaring an intention to the runtime*, which then coordinates the actual activity within its event-driven lifecycle.

That is why the later call to `core::SNodeC::start()` is so important. It is not a ceremonial extra line. It is the moment the runtime begins processing the scheduled communication activity. 

### The four recurring roles in almost every SNode.C application

A reader can understand a surprising amount of SNode.C by keeping four roles in mind.

#### The instance

The instance is the outer communication object.

This is a `SocketServer` or a `SocketClient`. It owns configuration, participates in the runtime lifecycle, and is responsible for initiating listening or connecting behavior.

An instance is not the application protocol itself.

It is the *carrier* of that protocol into the runtime.

#### The connection

The connection is the concrete communication relationship to a peer.

In the stream-oriented parts of SNode.C, this is represented by a `SocketConnection` specialization. It knows things such as local and remote addresses, queued bytes, transmitted bytes, read bytes, and timing information. The current core templates even show that on-connect and on-disconnect diagnostics are expressed in terms of the `SocketConnection`, including addresses, online duration, and transferred totals.  

That tells us something subtle but important:

SNode.C does not treat a connection as an invisible transport tunnel. It treats it as a visible runtime object with lifecycle, state, and measurable behavior.

#### The context

The context is the application protocol endpoint attached to one connection.

In the current core headers, `core::socket::stream::SocketContext` explicitly offers operations such as `sendToPeer(...)`, `readFromPeer(...)`, `setTimeout(...)`, `shutdownRead()`, `shutdownWrite()`, `close()`, and metrics accessors such as total sent, total queued, total read, and total processed. It also requires the derived class to provide `onConnected()` and `onDisconnected()`, and it is clearly designed as the point where protocol behavior is written. 

This leads to one of the most important mental rules in the framework:

> The instance manages communication setup; the context expresses protocol behavior.

That division is the opposite of the common beginner mistake of putting everything into the server or client object.

#### The factory

The factory creates the context.

A `SocketContextFactory` exists so that each new connection can receive its own protocol endpoint object without the application entry point having to manually build it at the exact moment a peer appears.

Once this clicks, the factory no longer feels like an unnecessary indirection. It becomes obviously correct.

A server may accept many peers over time. Each of those peers needs its own context. The framework therefore asks the factory to produce one.

The same idea applies to clients whenever a connection object is established and the application endpoint needs to attach to it.

### The main flow: from application startup to peer interaction

We can now describe the normal flow of a SNode.C stream application in a way that remains accurate across many specific variants.

#### Phase 1 — Framework initialization

The application starts by calling `core::SNodeC::init(argc, argv);`. 

This is the moment when the framework runtime, configuration handling, and surrounding machinery are prepared.

#### Phase 2 — Instance creation

The application creates one or more instances.

These may be anonymous or named. In practice, named instances are especially important because they fit naturally with the framework’s configuration model.

#### Phase 3 — Intent is registered

The application calls `listen(...)` on servers and `connect(...)` on clients.

Mentally, this phase should be understood as *registration of communication intent* rather than as a complete synchronous action.

The current core templates make this explicit by scheduling the real work at the next runtime tick.  

#### Phase 4 — Runtime execution begins

The application calls `core::SNodeC::start();`. 

The runtime now begins processing events and advancing the communication lifecycle.

#### Phase 5 — A connection object comes into existence

For a server, this happens when a peer is accepted.

For a client, this happens when the connection attempt succeeds.

At this stage, the connection object becomes available, and connection-level callbacks such as `onConnect` and `onConnected` can run.

#### Phase 6 — A context is created and attached

The framework uses the `SocketContextFactory` to create a `SocketContext` for the connection.

Now application protocol logic has a home.

#### Phase 7 — Application behavior reacts to events

The context receives lifecycle calls such as `onConnected()`, `onDisconnected()`, and data-related callbacks like `onReceivedFromPeer()` in the echo example.

At that point, your application protocol is alive.

This seven-phase flow is one of the best compact mental models for the framework.

### Instances are durable; contexts are per connection

One common source of confusion in event-driven frameworks is the distinction between long-lived outer objects and short- or medium-lived per-connection objects.

SNode.C’s model becomes much clearer once you explicitly separate these.

The instance is usually durable.

A server instance may live for the whole lifetime of the process. A client instance may also persist, especially if reconnect behavior is configured.

A context, by contrast, is attached to one specific connection. It lives with that connection and ends with it.

This distinction explains many design choices.

Why does configuration belong naturally on the instance?

Because configuration is usually about the behavior of the communication endpoint as a whole.

Why does application protocol behavior belong naturally in the context?

Because it is expressed relative to one concrete peer connection.

Why does the factory sit between the two?

Because the framework needs a mechanism to produce a fresh per-connection protocol endpoint from the longer-lived instance.

Once you see this, the structure stops looking arbitrary.

### The meaning of “layer-based” in everyday use

The framework’s layering can be described in many ways, but for practical work the following four-level view is the most useful.

#### Network family

This answers the question: *what kind of addressing and lower communication family are we using?*

Examples include:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP.

This level determines what a socket address looks like, what endpoint identity means, and what family-specific configuration is relevant.

#### Transport form

In the main parts of SNode.C discussed here, this is the `stream` model.

The important conceptual point is that the framework treats stream-oriented communication as a reusable transport abstraction that can then be specialized for different network families.

#### Connection handling

This is where the framework manages concrete peer communication.

At this level, the distinction between legacy and TLS enters the picture.

That is why TLS in SNode.C often feels like “the same application, one layer deeper becomes encrypted” rather than “everything must be redesigned.”

#### Application protocol

This is where your protocol behavior lives.

Sometimes that protocol is very small and custom. Sometimes it is HTTP. Sometimes WebSocket. Sometimes MQTT. Sometimes a higher-level framework such as the Express-like web layer builds on top of those.

The value of this layered model is not merely neat taxonomy. Its value is *transfer*.

If you understand where a concern belongs, you can often change one layer without mentally rebuilding the others from scratch.

### Why lower-layer changes often leave the application shape intact

This is one of the deepest practical strengths of SNode.C.

Suppose you begin with an IPv4 stream legacy application.

At first glance, it may feel as though the type name fully defines the application. But mentally, that is the wrong emphasis.

The better emphasis is this:

- the **instance/context/factory/runtime** pattern defines the application shape,
- the concrete **lower layers** define how that shape is carried.

That is why the repository can generate echo variants across multiple network families while reusing the same conceptual application structure. We already saw this in the live `src/apps/echo` setup, where multiple network families and both legacy/TLS modes are assembled around the same core echo context idea.   

This means that when we later move to:

- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP,
- TLS,

we are not abandoning the learned model.

We are exercising it.

### Configuration is not a side channel; it is part of the model

In some frameworks, configuration feels bolted on. There is a runtime model, and then somewhere else there is a pile of settings.

SNode.C is more integrated than that.

Even in the current `SocketServer` and `SocketClient` templates, configuration is central. The internal logic repeatedly consults the config object for retry behavior, retry-on-fatal behavior, jitter, retry limits, reconnect behavior, instance requirements, and more. The public convenience overloads for `listen(...)` and `connect(...)` also mutate configuration before delegating to the parameterless forms.    

That means the correct mental model is not:

> “I have an application, and separately I have some flags.”

The correct model is:

> “An instance is a configured communication role participating in the runtime.”

This is why named instances matter so much.

The instance is not only a variable in your C++ program. It is also a configuration-bearing unit the framework can reason about operationally.

### Connection callbacks and context callbacks are related but not identical

A subtle but important mental distinction is the difference between connection-level callbacks attached to the instance and lifecycle methods implemented inside the context.

The current `SocketServer` and `SocketClient` templates support `onConnect`, `onConnected`, and `onDisconnect` callbacks that operate directly on the `SocketConnection` object. These callbacks are wrapped by the framework with diagnostic logging and are part of the instance-level machinery.  

By contrast, the `SocketContext` abstraction requires derived classes to implement `onConnected()` and `onDisconnected()` as protocol-side lifecycle behavior. 

These two layers are connected, but they are not the same thing.

A useful rule of thumb is this:

- if your concern is about the **connection as a connection**, it often belongs in the instance-level callback world;
- if your concern is about the **application protocol behavior** attached to that connection, it often belongs in the context.

This distinction becomes especially helpful once TLS, certificate inspection, higher-level protocols, and structured web or MQTT behavior enter the picture.

### Retry, reconnect, and flow control are part of the mental model too

It is easy to think of retry logic as an operational detail that can be postponed until “production hardening.”

The current core templates suggest a different view.

Both `SocketServer` and `SocketClient` include flow-controller objects in their internal context structures. Both classes integrate retry logic directly into their communication lifecycle, and the client side additionally integrates reconnect behavior. These are not afterthoughts added outside the model. They are built into the runtime story itself.  

This has two consequences for the mental model.

First, a SNode.C instance is not merely “a socket plus callbacks.”

It is a managed communication role with lifecycle, flow observation, retry behavior, and configuration-driven resilience.

Second, a production-minded SNode.C application does not usually need to reinvent basic lifecycle control from scratch. The framework expects such concerns to exist and gives them a structural place.

### The framework is event-driven, but still measurable and concrete

Some event-driven systems feel abstract because everything is described in callbacks and nothing feels inspectable.

SNode.C has a different feel.

Even at the context level, the current `SocketContext` API exposes measurable communication facts such as total sent, total queued, total read, total processed, online-since strings, and online duration. At the instance template level, the default connection callbacks also log these metrics on disconnect.   

This means the framework’s event-driven nature does not remove operational concreteness.

A connection is still a thing with addresses, duration, queued bytes, sent bytes, read bytes, and processing totals.

That balance is pedagogically valuable.

It allows the reader to think in events without losing touch with the physical reality of communication.

### The mental model of a server in one paragraph

A server instance in SNode.C is a configured, runtime-managed communication role that registers a listening intention with the framework, participates in event-loop execution, accepts incoming peer connections through its lower communication layer, creates one application context per connection via a factory, and then lets those contexts express protocol behavior over the resulting connection objects.

If a reader really understands that sentence, the server side of the framework is no longer mysterious.

### The mental model of a client in one paragraph

A client instance in SNode.C is a configured, runtime-managed communication role that registers a connection intention with the framework, participates in event-loop execution, establishes peer connections through its lower communication layer, creates one application context per connection via a factory, and then lets those contexts express protocol behavior over the resulting connection objects, optionally supported by retry and reconnect behavior driven by configuration and flow control.

That is the client side in one sentence.

### The mental model of the whole framework in one diagram-shaped idea

If we turn the whole framework into a verbal diagram, it looks like this:

- **Application startup** initializes the runtime.
- **Instances** declare communication roles.
- **Configuration** shapes those roles.
- **Runtime scheduling** activates listening and connecting work.
- **Connections** come into existence.
- **Factories** create per-connection contexts.
- **Contexts** implement protocol behavior.
- **Lower layers** carry the communication.
- **Higher layers** build richer protocols without discarding the same basic model.

That is the whole picture.

Once the reader sees SNode.C like this, many later details become placement questions rather than mystery questions.

Where does this concern belong?

- configuration,
- instance,
- connection,
- context,
- lower layer,
- higher layer,
- runtime lifecycle.

This is exactly what a good mental model should provide.

### Common beginner misunderstandings — and the corrected view

It is useful to end the chapter by naming a few misunderstandings explicitly.

#### Misunderstanding 1: “The server class is where the protocol logic belongs.”

Corrected view: the server class is the outer communication role; the protocol logic belongs primarily in the context.

#### Misunderstanding 2: “The factory is just ceremony.”

Corrected view: the factory is what allows a clean transition from long-lived instance to per-connection protocol endpoint.

#### Misunderstanding 3: “`listen(...)` or `connect(...)` fully does the job immediately.”

Corrected view: these calls register intent and integrate with the event-driven runtime; the real work is coordinated by the framework lifecycle.  

#### Misunderstanding 4: “Changing lower communication families means changing the whole application model.”

Corrected view: changing the lower family often changes addressing, configuration, and some practical details, but the instance/factory/context/runtime pattern remains largely stable.

#### Misunderstanding 5: “Configuration is secondary.”

Corrected view: configuration is a first-class part of the framework model and deeply shapes instance behavior.

### Closing perspective

A framework becomes teachable when its parts can be described in a few stable roles.

SNode.C reaches that point because it has a strong internal regularity.

It has:

- a runtime,
- configured instances,
- concrete connections,
- per-connection contexts,
- factories that bridge between the two,
- and a layered communication model that keeps lower and higher concerns meaningfully separated.

This is the mental model that the rest of the book will keep reusing.

When we later discuss IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, Express-like routing, MQTT, and multi-instance applications, we will not be starting over each time.

We will be applying the same model to richer cases.

That is the real sign that the model is good.

It scales without changing its shape.
