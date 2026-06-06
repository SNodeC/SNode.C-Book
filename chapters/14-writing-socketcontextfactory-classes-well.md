## Writing `SocketContextFactory` Classes Well

### From protocol endpoint to construction boundary

Chapter 13 explained where application protocol behavior belongs.

It belongs in the `SocketContext`.

This chapter explains how such contexts are created for concrete connections.

The transition is small in API surface but important in design:

```text
SocketConnection
  -> SocketContextFactory::create(connection)
      -> SocketContext
```

A server or client instance represents the outer communication role.

A `SocketConnection` represents one concrete peer relationship.

A `SocketContext` implements the protocol behavior for that relationship.

A `SocketContextFactory` creates the context that belongs to that connection.

That is the construction boundary this chapter is about.

### What a `SocketContextFactory` is

A compact definition is:

> A `SocketContextFactory` creates the right per-connection protocol endpoint for a concrete `SocketConnection`.

This definition is deliberately narrow.

The factory does not implement the protocol conversation.

It does not replace the server or client instance.

It does not own the runtime.

It answers one construction question:

> Given this connection, which context object should be attached to it?

That question is small, but it protects an important architectural boundary.

#### Factory, connection, and context

The three roles should remain distinct:

| Object | Responsibility |
|---|---|
| `SocketConnection` | concrete peer relationship |
| `SocketContext` | protocol behavior for one connection |
| `SocketContextFactory` | construction policy for creating a context for a connection |

This table continues the distinction from Chapter 13.

The connection is the peer relationship.

The context is the protocol endpoint.

The factory creates that endpoint.

When these responsibilities stay separate, application code remains easier to reason about.

#### The live interface

The live stream factory interface is intentionally narrow.

Its essential method is:

```cpp
virtual core::socket::stream::SocketContext*
create(core::socket::stream::SocketConnection* socketConnection) = 0;
```

The interface receives a `SocketConnection*` and returns a `SocketContext*`.

That shape says exactly what the framework needs:

```text
A concrete connection exists.
Create the protocol endpoint that belongs to it.
```

The factory is therefore not a general-purpose object creation service.

It is the construction bridge between a connection and the protocol context that will run on that connection.

### The creation flow

The factory sits in the connection creation path.

A compact view is:

```text
SocketServer / SocketClient
  -> concrete SocketConnection
      -> SocketContextFactory::create(connection)
          -> new SocketContext(connection, dependencies...)
              -> protocol behavior
```

This diagram connects Chapters 9, 13, and 14.

Chapter 9 explained the server/client/connection relationship.

Chapter 13 explained the context as the per-connection protocol endpoint.

This chapter explains the construction step between connection and context.

The factory does not make the connection real.

It does not process protocol messages.

It creates the context that will handle protocol behavior once attached to the connection.

### One fresh context per connection

The most important rule is simple:

> A factory should create a fresh context for the concrete connection it receives.

A `SocketContext` is per-connection.

Therefore, a factory should not reuse one context object across several connections.

It should not treat the context as a singleton.

It should not use one shared protocol shell to represent all peers.

The purpose of the factory is to create a protocol endpoint for one concrete peer relationship.

That means each call to `create(...)` should be understood as:

```text
this connection
  -> this new protocol endpoint
```

This rule follows directly from Chapter 13.

If the context is one per-connection protocol endpoint, the factory must preserve that one-to-one relationship.

### What belongs in a factory

A factory contains construction policy.

That means it may reasonably decide:

- which concrete context type should be created,
- which stable constructor arguments should be passed,
- which role-specific value the context should receive,
- which explicit application services the context needs,
- and how to keep construction readable.

It should not perform the protocol itself.

A useful contrast is:

| Belongs in the factory | Does not belong in the factory |
|---|---|
| choosing the context type | protocol message handling |
| passing stable dependencies | read/write behavior |
| setting role-specific constructor arguments | retry or reconnect policy |
| creating one fresh context | global orchestration |
| keeping construction readable | service-location dumping ground |
| making construction-time choices | mid-protocol state transitions |

The boundary is:

```text
Factory
  -> construction policy

Context
  -> protocol behavior
```

#### Choosing the context type

A factory can legitimately choose which concrete context type to create.

For many simple applications, there is exactly one concrete context type.

In that case, the factory is almost mechanical:

```cpp
SocketContext* create(SocketConnection* connection) override {
    return new MySocketContext(connection);
}
```

In other applications, the factory may choose among a small set of endpoint types.

That can be reasonable if the choice is a construction-time decision.

It becomes problematic only when the factory starts performing protocol behavior that belongs inside the context.

#### Passing stable dependencies

A context may need stable dependencies at construction time.

Examples include:

- a role indicator,
- immutable protocol configuration,
- a shared service interface,
- a parser helper,
- a statistics sink,
- a small dispatcher object.

This is a legitimate factory responsibility.

The factory can hold or capture stable dependencies and pass them into each newly created context.

The discipline is to keep those dependencies meaningful.

A factory should ask:

> What does this context genuinely need in order to behave as the protocol endpoint for this connection?

That question prevents the factory from becoming a dumping ground for unrelated application objects.

#### Making role decisions explicit

A factory is often a good place to make role-specific construction decisions.

For example, a protocol may use the same context class on both sides but pass a role value:

```cpp
enum class Role {
    Server,
    Client
};
```

Then the factory can make the role explicit:

```cpp
SocketContext* create(SocketConnection* connection) override {
    return new EchoSocketContext(connection, Role::Server);
}
```

A separate client-side factory might use:

```cpp
SocketContext* create(SocketConnection* connection) override {
    return new EchoSocketContext(connection, Role::Client);
}
```

This kind of factory is small, but useful.

The role decision is visible.

The context receives the information it needs.

The factory still remains construction-oriented.

#### Keeping construction readable and unsurprising

A good factory is often intentionally uninteresting.

That is a strength.

A developer should be able to open the factory and quickly answer:

- Which context class is created?
- Which constructor arguments are passed?
- Which stable dependencies are encoded?
- Which role decision is made?

If answering those questions requires reading a large amount of unrelated logic, the factory has probably grown too far.

Readable construction is part of the design.

### What does not belong in a factory

Because the factory sits at an important boundary, it is tempting to put too much into it.

That should be avoided.

#### Protocol behavior does not belong in the factory

The factory should not parse protocol messages.

It should not decide mid-protocol transitions.

It should not control conversation flow.

It should not perform authentication steps that belong to the protocol endpoint.

Those are context responsibilities.

If protocol behavior starts moving into the factory, the application becomes harder to understand because the protocol is split across construction code and endpoint code.

The factory should create the endpoint.

The context should behave as the endpoint.

#### Runtime flow control does not belong in the factory

The factory should not manage:

- retry logic,
- reconnect policy,
- event-loop sequencing,
- accept-loop tuning,
- or multiplexer details.

Those concerns belong to the instance, configuration, flow controller, runtime, and lower-level framework machinery.

The factory should stay close to one moment:

```text
A connection exists.
Create the context for it.
```

#### Global service location does not belong in the factory

A factory may pass explicit stable services into a context.

That is different from becoming a service locator.

A service-locator-style factory starts to behave as a hidden doorway to the entire application:

- global registries,
- database handles,
- unrelated service maps,
- orchestration callbacks,
- metrics systems,
- configuration trees,
- and session stores.

Sometimes a context needs access to one of these things.

But the dependency should be explicit and justified.

The factory should not quietly provide access to everything.

#### Large mutable protocol state does not belong in the factory

Connection-local protocol state belongs in the context.

Application-level shared state belongs in an application-level service or model.

The factory should not become the place where large mutable protocol state is accumulated simply because it is convenient.

If the factory holds too much state, it becomes harder to answer a basic question:

```text
What does one context do on one connection?
```

That is a sign that responsibilities are drifting.

### Ownership and lifecycle

The factory interface returns a raw `SocketContext*`.

In modern C++ this deserves a careful explanation.

The raw pointer return should not be read as permission for arbitrary manual ownership throughout the application.

It should be read as part of this framework contract:

```text
The factory creates a new endpoint object.
The object is handed into the framework-managed connection/context lifecycle.
```

The practical rule is:

> Create the right concrete context object and hand it back to the framework.

The factory should not keep accidental ownership of the created context.

It should not share the same context object across several connections.

It should not create an object whose lifetime is unclear.

The raw pointer belongs to this construction boundary.

It is not an invitation to unmanaged lifetime design elsewhere in the application.

### Factory design patterns

There is not only one correct factory shape.

The right design depends on what needs to vary at construction time.

| Pattern | Use when |
|---|---|
| separate server/client factories | the role distinction should be visible and simple |
| parameterized factory | the context type is the same and only stable constructor data differs |
| context-type-selecting factory | a small, explicit selection among endpoint types is needed |

All three patterns can be valid.

The same rule applies to all of them:

> The selection should remain construction policy, not protocol execution.

#### Separate server/client factories

Separate server-side and client-side factories can be useful when the two roles should be visible.

This is especially clear when both sides use the same context type but receive different role arguments.

The benefit is readability.

The server construction path is explicit.

The client construction path is explicit.

No hidden role inference is required.

Small duplication is often acceptable when it makes the communication roles clearer.

#### Parameterized factories

A single reusable factory type may also be appropriate.

For example, the role or configuration object may be a constructor argument of the factory itself:

```cpp
class EchoSocketContextFactory : public SocketContextFactory {
public:
    explicit EchoSocketContextFactory(Role role)
        : role(role) {
    }

    SocketContext* create(SocketConnection* connection) override {
        return new EchoSocketContext(connection, role);
    }

private:
    Role role;
};
```

This can be a clean design when the factory remains easy to read and the variation is stable.

The factory is still only expressing construction policy.

#### Context-type-selecting factories

Some applications may need a factory that chooses among a small number of context classes.

That can be acceptable when the selection is explicit and construction-time.

For example, a configuration value might decide whether to create a diagnostic context or a normal protocol context.

But the selection should remain simple.

If the factory begins reading from the peer, interpreting protocol frames, or managing state transitions, it has crossed into protocol behavior.

That belongs in the context.

### Passing shared application state

Real applications often need shared services.

A small factory does not mean an isolated factory.

It may capture or store references to shared resources such as:

- immutable protocol configuration,
- a thread-safe statistics object,
- a reference-counted service interface,
- a dispatcher,
- a logger abstraction,
- or an application model needed by the protocol.

The important distinction is between explicit dependency passing and uncontrolled service location.

Good dependency passing looks like:

```text
This context needs this service to implement this protocol.
```

Uncontrolled service location looks like:

```text
The context can reach everything through the factory.
```

The first is a design choice.

The second erodes the boundary.

### The strongest factory test

A useful practical test is:

> If the protocol behavior were removed from the context class, would the factory still appear to contain too much of the application?

If the answer is yes, the factory is probably overgrown.

A good factory should feel incomplete without the context.

That is exactly right.

Its job is to create the protocol endpoint, not to replace it.

Another useful test is:

> Can a developer understand the factory in one glance?

A factory that is hard to skim is often doing more than construction.

### The factory as the Chapter 15 bridge

Chapter 15 will show how the same protocol can be carried over different lower communication families.

Chapter 14 is the necessary bridge to that idea.

The separation is:

```text
SocketContext
  -> protocol behavior

SocketContextFactory
  -> construction policy

SocketServer / SocketClient
  -> lower-family-specific communication role
```

Once this separation is clear, the same context logic can often be reused while different server/client types choose different lower families.

The factory is the place where the correct context is created for whichever connection the lower-family role produces.

That makes it part of the portability story.

Not because it performs the protocol.

Because it keeps protocol construction separate from the lower-layer role.

### What to remember

Remember:

- A `SocketContextFactory` creates a `SocketContext` for a concrete `SocketConnection`.
- The factory contains construction policy, not protocol behavior.
- A fresh context should be created for each connection.
- The factory may choose a context type.
- The factory may pass stable dependencies into the context.
- Role decisions can belong in the factory when they affect construction.
- The factory should not parse protocol data or control protocol flow.
- The factory should not manage retry, reconnect, runtime flow, or lower-level event processing.
- The factory should not become a service locator for the whole application.
- The raw pointer return represents handoff into the framework-managed connection/context lifecycle.
- A good factory is small, readable, and unsurprising.
- Chapter 15 uses this separation to carry the same protocol over different lower layers.

### Closing perspective

Chapter 13 explained how to write the protocol endpoint well.

This chapter explained how such endpoints are created.

The distinction is central:

```text
SocketContext
  -> behavior

SocketContextFactory
  -> construction
```

When that boundary is clean, the rest of the application remains easier to understand.

The outer instance remains the communication role.

The connection remains the concrete peer relationship.

The context remains the protocol endpoint.

The factory remains the construction bridge.

The next chapter can now use this separation directly.

If protocol behavior lives in the context and context creation lives in the factory, the same protocol can be carried over different lower communication families without changing its essential shape.

That is the next step.
