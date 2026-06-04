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

Each of those phrases becomes much less abstract once we connect it to the codebase.

### Three models that belong together

The mental model of SNode.C is easiest to keep in mind when it is divided into three smaller models.

The first is the **runtime model**.

It explains how an application starts, how instances declare communication intent, how connections come into existence, and how contexts become active.

The second is the **layer model**.

It explains why the same application shape can often be carried over IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, and TLS.

The third is the **operational model**.

It explains why configuration, callbacks, retry logic, reconnect behavior, flow control, and metrics are not side topics. They are part of the framework's normal way of thinking.

These three models are not separate frameworks. They are three views of the same design.

#### The runtime model

##### The runtime is a central coordinator, not an afterthought

At the top of the runtime picture sits `core::SNodeC`.

The public runtime interface exposes lifecycle functions such as `init(...)`, `start(...)`, `stop()`, `tick(...)`, `free()`, and `state()`. Even without looking at every implementation detail, that public surface already tells us something important: the framework treats initialization, event-loop execution, and shutdown as explicit runtime phases rather than incidental side effects.

This matters because SNode.C is not designed as a passive library that simply waits for the application to call a few helper functions. It has a runtime posture.

That posture becomes clearer when looking at the stream `SocketServer` and `SocketClient` templates.

The public `listen(...)` and `connect(...)` entry points do not perform the whole operation in a blocking procedural sense. They enter the flow-controller path. The flow controller then schedules the actual listening or connecting work for the next runtime tick.

This is an important distinction.

The application does not directly say:

> Do all socket work immediately, here, on this call stack.

It says instead:

> Register this communication intent with the framework and let the runtime advance it through the event system.

When you write:

```cpp
server.listen(...);
client.connect(...);
```

you are not “doing everything now” in the traditional blocking sense.

You are declaring an intention to the runtime. The runtime, together with the flow controller, coordinates the actual activity within the event-driven lifecycle.

That is why the later call to `core::SNodeC::start()` is so important. It is not a ceremonial extra line. It is the point at which the runtime begins processing the scheduled communication activity.

##### The four recurring roles in almost every SNode.C application

A reader can understand a surprising amount of SNode.C by keeping four roles in mind.

The echo pair from Chapter 3 has already shown these roles in a small form. There was a server or client object, a factory, a context, and the runtime that made the whole application move. This chapter now names the pattern more explicitly, so the reader can recognize it again in later protocols.

###### The instance

The instance is the configured communication role.

In user code this role is usually introduced through a `SocketServer` or a `SocketClient` object. That object is the handle through which the application configures and registers listening or connecting behavior.

This distinction is important. In this chapter, the word *instance* does not merely mean "the local C++ variable currently in scope." It means the configured communication role that participates in the runtime. After `listen(...)` or `connect(...)` has registered the role, the active flow can be carried by the framework's shared configuration and flow-controller context.

An instance is not the application protocol itself.

It is the *carrier* of that protocol into the runtime.

###### The connection

The connection is the concrete communication relationship to a peer.

In the stream-oriented parts of SNode.C, this is represented by a `SocketConnection` specialization. It knows things such as local and remote addresses, queued bytes, transmitted bytes, read bytes, and timing information. Connection-level callbacks and diagnostic logging are expressed in terms of that connection object.

That tells us something subtle but important.

SNode.C does not treat a connection as an invisible transport tunnel. It treats it as a visible runtime object with lifecycle, state, addresses, duration, and measurable behavior.

###### The context

The context is the application protocol endpoint attached to one connection.

In the stream layer, a `SocketContext` provides the operations through which protocol code interacts with a peer connection. It can send to the peer, read from the peer, set timeouts, shut down one side of the communication, close the connection, and inspect communication metrics.

It also provides lifecycle hooks such as `onConnected()` and `onDisconnected()` for derived protocol contexts.

This leads to one of the most important mental rules in the framework:

> The instance manages communication setup; the context expresses protocol behavior.

That division is the opposite of the common beginner mistake of putting everything into the server or client object.

###### The factory

The factory creates the context.

A `SocketContextFactory` exists so that each new connection can receive its own protocol endpoint object without the application entry point having to manually build it at the exact moment a peer appears.

Once this clicks, the factory no longer feels like an unnecessary indirection. It becomes obviously correct.

A server may accept many peers over time. Each of those peers needs its own context. The framework therefore asks the factory to produce one.

The same idea applies to clients whenever a connection object is established and the application endpoint needs to attach to it.

##### The main flow: from application startup to peer interaction

We can now describe the normal flow of a SNode.C stream application in a way that remains accurate across many specific variants.

###### Phase 1: Framework initialization

The application starts by calling:

```cpp
core::SNodeC::init(argc, argv);
```

This is the moment when the framework runtime, configuration handling, and surrounding machinery are prepared.

###### Phase 2: Instance creation

The application creates one or more server or client handles.

Through these handles, it creates configured communication roles. These roles may be anonymous or named. In practice, named instances are especially important because they fit naturally with the framework's configuration model.

###### Phase 3: Intent is registered

The application calls `listen(...)` on servers and `connect(...)` on clients.

Mentally, this phase should be understood as *registration of communication intent* rather than as a complete synchronous action.

The stream server and client templates delegate the flow to their flow controllers, and the flow-controller path schedules the real work for a runtime tick. During that registration, the framework retains the necessary shared configuration and shared context state. This is why the local server or client handle seen in Chapter 3 may go out of scope after `listen(...)` or `connect(...)` without making the registered flow disappear.

###### Phase 4: Runtime execution begins

The application calls:

```cpp
core::SNodeC::start();
```

The runtime now begins processing events and advancing the communication lifecycle. It advances the registered communication roles, not merely the lifetime of whichever local handle variable was used to register them.

###### Phase 5: A connection object comes into existence

For a server, this happens when a peer is accepted.

For a client, this happens when the connection attempt succeeds.

At this stage, the connection object becomes available, and connection-level callbacks such as `onConnect`, `onConnected`, and `onDisconnect` can run.

###### Phase 6: A context is created and attached

The framework uses the `SocketContextFactory` to create a `SocketContext` for the connection.

Now application protocol logic has a home.

###### Phase 7: Application behavior reacts to events

The context receives lifecycle calls such as `onConnected()` and `onDisconnected()`, and protocol-specific callbacks handle incoming data or higher-level events.

At that point, the application protocol is alive.

This seven-phase flow is one of the best compact mental models for the framework.

##### Communication roles are durable; contexts are per connection

One common source of confusion in event-driven frameworks is the distinction between long-lived communication roles, short-lived local handles, and per-connection protocol objects.

SNode.C's model becomes much clearer once you explicitly separate these.

The local `SocketServer` or `SocketClient` object is the handle used to configure and register a role. Keeping that handle in scope is clear and harmless, and many examples do exactly that. But the registered role is represented internally through shared configuration and shared flow-controller state. It is not the same thing as the lifetime of one local C++ variable.

The configured communication role is usually durable.

A server role may live for the whole lifetime of the process. A client role may also persist, especially if reconnect behavior is configured.

A context, by contrast, is attached to one specific connection. It lives with that connection and ends with it.

This distinction explains many design choices.

Why does configuration belong naturally on the instance?

Because configuration is usually about the behavior of the communication endpoint as a whole.

Why does application protocol behavior belong naturally in the context?

Because it is expressed relative to one concrete peer connection.

Why does the factory sit between the two?

Because the framework needs a mechanism to produce a fresh per-connection protocol endpoint from the longer-lived communication role.

Once you see this, the structure stops looking arbitrary.

#### The layer model

##### The meaning of “layer-based” in everyday use

The framework's layering can be described in many ways, but for practical work the following four-level view is the most useful.

###### Network family

This answers the question:

> What kind of addressing and lower communication family are we using?

Examples include:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP.

This level determines what a socket address looks like, what endpoint identity means, and what family-specific configuration is relevant.

IPv4 and IPv6 use IP addresses and ports.

Unix domain sockets use filesystem-like or platform-specific local socket identities.

Bluetooth RFCOMM and Bluetooth L2CAP use Bluetooth-specific endpoint concepts. RFCOMM is often easiest to understand as a stream-oriented Bluetooth communication path with a serial-port-like mental flavor. L2CAP sits lower in the Bluetooth stack and has different addressing and configuration implications, but it can still participate in the same SNode.C application shape where the framework provides a compatible abstraction.

That last point is important.

For the application writer, Bluetooth is not merely a strange exception. It is another lower communication family that can carry the same instance/context/factory pattern when the selected SNode.C module supports the required communication form.

###### Transport form

In the main parts of SNode.C discussed here, this is the `stream` model.

The important conceptual point is that the framework treats stream-oriented communication as a reusable transport abstraction that can then be specialized for different network families.

This is why the same conceptual echo application can be useful across several lower layers.

The application still thinks in terms of connections and contexts.

The lower layer decides how peers are addressed and how bytes physically travel.

###### Connection handling

This is where the framework manages concrete peer communication.

At this level, the distinction between legacy and TLS enters the picture.

That is why TLS in SNode.C often feels like “the same application, one layer deeper becomes encrypted” rather than “everything must be redesigned.”

TLS changes important security properties. It introduces certificates, handshakes, validation questions, and failure modes.

But it does not force the application writer to abandon the basic mental model of instances, connections, factories, and contexts.

###### Application protocol

This is where protocol behavior lives.

Sometimes that protocol is very small and custom.

Sometimes it is HTTP.

Sometimes it is WebSocket.

Sometimes it is MQTT.

Sometimes a higher-level framework such as the Express-like web layer builds on top of HTTP routing and middleware concepts.

The value of this layered model is not merely neat taxonomy. Its value is *transfer*.

If you understand where a concern belongs, you can often change one layer without mentally rebuilding the others from scratch.

##### Why lower-layer changes often leave the application shape intact

This is one of the deepest practical strengths of SNode.C.

Suppose you begin with an IPv4 stream legacy application.

At first glance, it may feel as though the type name fully defines the application. But mentally, that is the wrong emphasis.

The better emphasis is this:

- the **instance/context/factory/runtime** pattern defines the application shape;
- the concrete **lower layers** define how that shape is carried.

That is why SNode.C can provide echo-style variants across multiple network families while reusing the same conceptual application structure.

This means that when we later move to:

- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP,
- TLS,

we are not abandoning the learned model.

We are exercising it.

#### The operational model

##### Configuration is not a side channel; it is part of the model

In some frameworks, configuration feels bolted on. There is a runtime model, and then somewhere else there is a pile of settings.

SNode.C is more integrated than that.

The stream `SocketServer` and `SocketClient` templates repeatedly consult their configuration objects while advancing the communication lifecycle. Retry behavior, retry-on-fatal behavior, jitter, retry limits, reconnect behavior, instance requirements, local addresses, remote addresses, backlog settings, and related operational decisions are not external decoration.

They shape what an instance actually does.

That means the correct mental model is not:

> “I have an application, and separately I have some flags.”

The correct model is:

> “An instance is a configured communication role participating in the runtime.”

This is why named instances matter so much.

The instance is not only a variable in a C++ program. It is also a configuration-bearing unit the framework can reason about operationally.

##### Connection callbacks and context callbacks are related but not identical

A subtle but important mental distinction is the difference between connection-level callbacks attached to the instance and lifecycle methods implemented inside the context.

The stream `SocketServer` and `SocketClient` templates support `onConnect`, `onConnected`, and `onDisconnect` callbacks that operate directly on the `SocketConnection` object. These callbacks are part of the instance-level machinery. They are useful for observing, supervising, logging, measuring, or adapting connection-level behavior.

By contrast, the `SocketContext` abstraction requires derived classes to implement protocol-side lifecycle behavior such as `onConnected()` and `onDisconnected()`.

These two layers are connected, but they are not the same thing.

A useful rule of thumb is this:

- if the concern is about the **connection as a connection**, it often belongs in the instance-level callback world;
- if the concern is about the **application protocol behavior** attached to that connection, it often belongs in the context.

Or, even shorter:

> Instance callbacks observe and supervise connections; context callbacks implement protocol behavior.

This distinction becomes especially helpful once TLS, certificate inspection, higher-level protocols, structured web behavior, and MQTT behavior enter the picture.

##### Retry, reconnect, and flow control are part of the mental model too

It is easy to think of retry logic as an operational detail that can be postponed until “production hardening.”

SNode.C suggests a different view.

Both `SocketServer` and `SocketClient` include flow-controller objects in their internal context structures. Both classes integrate retry logic directly into their communication lifecycle, and the client side additionally integrates reconnect behavior.

These are not afterthoughts added outside the model. They are built into the runtime story itself.

This has two consequences.

First, a SNode.C instance is not merely “a socket plus callbacks.”

It is a managed communication role with lifecycle, flow observation, retry behavior, and configuration-driven resilience.

Second, a production-minded SNode.C application does not usually need to reinvent basic lifecycle control from scratch. The framework expects such concerns to exist and gives them a structural place.

##### The framework is event-driven, but still measurable and concrete

Some event-driven systems feel abstract because everything is described in callbacks and nothing feels inspectable.

SNode.C has a different feel.

Even at the context level, the stream `SocketContext` API exposes measurable communication facts such as total sent, total queued, total read, total processed, online-since information, and online duration.

At the instance level, connection callbacks can log or inspect addresses, duration, queued bytes, sent bytes, read bytes, and processed bytes.

This means the framework's event-driven nature does not remove operational concreteness.

A connection is still a thing with addresses, duration, queued bytes, sent bytes, read bytes, and processing totals.

That balance is pedagogically valuable.

It allows the reader to think in events without losing touch with the physical reality of communication.

### Server and client side by side

The server and client mental models are nearly parallel. Seeing them side by side is more useful than reading the same sentence twice.

| Aspect | Server instance | Client instance |
|---|---|---|
| Main intention | Listen for peers | Connect to a peer |
| Public entry point | `listen(...)` | `connect(...)` |
| Runtime role | Registers a listening intention | Registers a connection intention |
| Local handle | Used to configure and register the role | Used to configure and register the role |
| Flow support | Server-side flow controller | Client-side flow controller |
| Connection creation | Peer is accepted | Connection attempt succeeds |
| Context creation | Factory creates one context per accepted connection | Factory creates one context for the established connection |
| Protocol behavior | Lives in the per-connection context | Lives in the per-connection context |
| Resilience focus | Retry listening where configured | Retry connecting and reconnect where configured |

This table also shows why the framework can teach both sides together.

The details differ, but the application shape remains recognizable.

### The mental model in one diagram-shaped idea

If we turn the whole framework into a compact verbal diagram, it looks like this:

```text
Application startup
  -> core::SNodeC::init(...)
  -> create server/client handles
      -> configure communication roles
          -> Config
          -> FlowController / shared context
              -> retain registered flow state
              -> schedule communication work
              -> observe retry/reconnect/termination
          -> SocketConnection
              -> SocketContextFactory
                  -> SocketContext
                      -> protocol behavior
  -> core::SNodeC::start()
      -> runtime advances events
```

This is not a complete implementation diagram.

It is a memory diagram.

It tells the reader where each kind of thought belongs.

When thinking about startup, look at the runtime.

When thinking about listening or connecting, look at the configured role, the local handle that registers it, and the flow controller that carries the active flow.

When thinking about peer state, look at the connection.

When thinking about application protocol behavior, look at the context.

When thinking about per-connection object creation, look at the factory.

When thinking about IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP, legacy streams, and TLS, look at the lower layers that carry the same application shape.

### What to remember

The chapter can be compressed into a small checklist.

Remember:

- The runtime drives progress.
- Instances declare communication roles.
- Local server/client objects are handles for configuring and registering those roles.
- Configuration belongs naturally to instances.
- `listen(...)` and `connect(...)` register communication intent.
- Flow controllers and shared context state carry active communication flows.
- Connections represent concrete peers.
- Factories create per-connection contexts.
- Contexts implement protocol behavior.
- Instance callbacks observe and supervise connections.
- Context callbacks express protocol lifecycle behavior.
- Lower layers carry the same application shape over different communication families.
- Retry, reconnect, flow control, and metrics are part of the normal model, not optional decorations.

This is the mental model to carry into the next chapters.

It also explains why the echo pair from Chapter 3 was more than a small demonstration. That example already contained the pattern: a handle registered a role, a factory created a context, a connection carried peer communication, and the runtime advanced the flow.

Later chapters will add more concrete APIs, more protocols, more configuration detail, and more complete examples. But those details should attach themselves to this structure.

SNode.C becomes much easier to learn when the reader stops asking only:

> “Which class do I need?”

and starts also asking:

> “Which role am I working with?”

That second question is the beginning of understanding the framework.
