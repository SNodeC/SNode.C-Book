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

If the context is the protocol endpoint, the factory is the construction boundary.

The visible `SocketServer` or `SocketClient` object is the application-side handle. The registered instance is the long-lived runtime-visible server-side or client-side communication role. A `SocketConnection` is one concrete peer relationship under that role. A `SocketContextFactory` creates the protocol endpoint that is attached to such a connection.

That distinction keeps the application architecture readable:

```text
application-side SocketServer / SocketClient handle
  -> registered server/client instance
      -> concrete SocketConnection
          -> SocketContextFactory::create(connection)
              -> SocketContext
                  -> protocol behavior
```

The server or client role does not implement the protocol conversation.

The connection does not decide which application endpoint class should exist.

The context implements the behavior.

The factory creates the context that will contain that behavior.

That is the construction boundary this chapter is about.

### What a `SocketContextFactory` is

A compact definition is:

> A `SocketContextFactory` creates the right per-connection protocol endpoint for a concrete `SocketConnection`.

This definition is deliberately narrow.

The factory does not implement the protocol conversation.

It does not replace the registered server-side or client-side instance.

It does not own the runtime.

It answers one construction question:

> Given this connection, which context object should be attached to it?

That question is small, but it protects an important architectural boundary.

The factory is where construction-time decisions become explicit. The context type can be chosen, stable dependencies can be passed, and a role value can be made visible. Once the context exists, protocol behavior belongs inside the context, not inside the factory that created it.

#### Factory, connection, and context

The three roles should remain distinct:

| Object | Responsibility |
|---|---|
| `SocketConnection` | concrete peer relationship |
| `SocketContext` | protocol behavior for one connection |
| `SocketContextFactory` | context creation for a concrete connection |

This table continues the distinction from Chapter 13.

The connection is the managed peer relationship.

The context is the protocol endpoint attached to that relationship.

The factory creates that endpoint.

When these responsibilities stay separate, application code remains easier to reason about. A reader can ask one question at a time: Which connection exists? Which context was created for it? What protocol behavior does that context implement?

#### The factory interface

The stream factory interface is intentionally narrow.

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

This narrowness is useful. It prevents the factory interface from becoming a second application framework. A concrete factory may still hold stable construction data, but the moment represented by `create(connection)` remains precise: a connection has appeared, and the correct context object must be created for that connection.

### The construction path from connection to context

The factory sits in the connection creation path.

A compact view is:

```text
application-side SocketServer / SocketClient handle
  -> registered server/client instance
      -> concrete SocketConnection
          -> SocketContextFactory::create(connection)
              -> new SocketContext(connection, dependencies...)
                  -> protocol behavior
```

This diagram connects Chapters 9, 13, and 14.

Chapter 9 explained the server/client/connection relationship.

Chapter 13 explained the context as the per-connection protocol endpoint.

This chapter explains the construction step between connection and context.

The factory does not make the connection real. The accept or connect path does that.

The factory does not process protocol messages. The context does that.

The factory creates the context that will handle protocol behavior once attached to the connection.

That is why the factory is a boundary object. It is close to the connection, because it receives the connection. It is close to the protocol, because it creates the context. But it is not itself the connection and not itself the protocol endpoint.

### One fresh context per creation

The most important rule is simple:

> A factory should create a fresh context for the concrete connection it receives.

A `SocketContext` is per-connection.

Therefore, a factory should not reuse one context object across several connections.

It should not treat the context as a singleton.

It should not use one shared protocol shell to represent all peers.

The purpose of the factory is to create a protocol endpoint for one concrete peer relationship.

That means each ordinary call to `create(...)` should be understood as:

```text
this connection
  -> this new protocol endpoint
```

This rule follows directly from Chapter 13.

If the context is one per-connection protocol endpoint, the factory must preserve that relationship.

The framework also supports context replacement as a more advanced connection operation. That does not weaken the construction rule. If a later context switch is used, the new context is still a fresh endpoint object handed to the framework. It is not a reused singleton shared across peers and it is not a hidden global protocol object.

For the ordinary creation path, the rule remains simple: create the context that belongs to the connection you received, then hand it back.

### Construction responsibilities of a factory

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
  -> context creation

Context
  -> protocol behavior
```

The table is not meant to make factories trivial. Some factories need more than one constructor argument. Some factories choose between several context types. Some factories carry role information. The rule is not that every factory must be tiny. The rule is that factory complexity should remain construction complexity.

#### Choosing the context type

A factory can legitimately choose which concrete context type to create.

For many simple applications, there is exactly one concrete context type.

In that case, the factory is almost mechanical. In schematic form:

```cpp
SocketContext* create(SocketConnection* connection) override {
    return new MySocketContext(connection);
}
```

In other applications, the factory may choose among a small set of endpoint types.

That can be reasonable if the choice is a construction-time decision.

It becomes problematic only when the factory starts performing protocol behavior that belongs inside the context. Choosing a context type is construction. Reading protocol frames, interpreting commands, and advancing protocol state are behavior.

#### Passing stable dependencies

Chapter 13 said that a context may depend on application services, but those dependencies should be visible.

Chapter 14 shows the construction boundary where such dependencies can be passed deliberately.

A context may need stable dependencies at construction time. Examples include:

- a role indicator,
- immutable protocol configuration,
- a shared service interface,
- a parser helper,
- a statistics sink,
- a small dispatcher object.

This is a legitimate factory responsibility.

The factory can receive, hold, or capture stable dependencies and pass them into each newly created context.

The discipline is to keep those dependencies meaningful.

A factory should ask:

> What does this context genuinely need in order to behave as the protocol endpoint for this connection?

That question prevents the factory from becoming a dumping ground for unrelated application objects.

Good dependency passing makes the construction path explicit. It says: this context needs this service to implement this protocol. That is very different from hiding a route to the whole application behind the factory.

#### Making role decisions explicit

A factory is often a good place to make role-specific construction decisions.

For example, a protocol may use the same context class on both sides but pass a role value:

```cpp
enum class Role {
    Server,
    Client
};
```

Then the factory can make the role explicit. In schematic form:

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

A server-side factory can create a context configured for server-side protocol behavior. A client-side factory can create the corresponding client-side context. Both factories remain construction code. Neither one becomes the protocol conversation.

#### Keeping construction readable and unsurprising

A good factory is often intentionally simple.

That is a strength.

A developer should be able to open the factory and quickly answer:

- Which context class is created?
- Which constructor arguments are passed?
- Which stable dependencies are encoded?
- Which role decision is made?

If answering those questions requires reading a large amount of unrelated logic, the factory has probably grown too far.

Readable construction is part of the design.

It is acceptable for a factory to express a real construction decision. It is not acceptable for construction code to hide a protocol conversation, a retry policy, a session manager, or a global service locator behind a method named `create(...)`.

### Responsibilities that should stay out of the factory

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

Those concerns belong to the registered instance, its configuration, the flow controller, the runtime, and lower-level framework machinery.

The factory should stay close to one moment:

```text
A connection exists.
Create the context for it.
```

This is the same separation Chapter 13 used for contexts. A context should not become the server/client role; a factory should not become the server/client role either. The registered instance remains the long-lived runtime-visible communication role. The factory remains the construction boundary for connection-local protocol endpoints.

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

Sometimes a context genuinely needs access to one of these things.

But the dependency should be explicit and justified.

The factory should not quietly provide access to everything.

Explicit dependency passing keeps construction readable.

Service location hides the dependency boundary.

That distinction matters because the factory is close to every new connection. If it becomes a hidden gateway to the whole application, every context becomes harder to understand.

#### Large mutable protocol state does not belong in the factory

Connection-local protocol state belongs in the context.

Application-level shared state belongs in an application-level service or model.

The factory should not become the place where large mutable protocol state is accumulated simply because it is convenient.

If the factory holds too much state, it becomes harder to answer a basic question:

```text
What does one context do on one connection?
```

That is a sign that responsibilities are drifting.

Factory state should usually be stable construction state, not evolving per-message protocol state. A role value, a configuration object, or a service reference can be construction state. A partially parsed message, peer conversation phase, or connection-local protocol buffer belongs in the context.

### Ownership and lifecycle

The factory interface returns a raw `SocketContext*`.

This deserves a careful explanation.

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

The connection side of the framework decides what happens after creation. If the factory returns a context, the connection attaches it. If creation fails and returns no context, the connection cannot continue with protocol behavior and closes the relationship. The application author should therefore treat `create(...)` as a narrow handoff point: allocate the correct context, return it, and let the framework manage the connection/context lifecycle from there.

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

The important distinction is not whether a factory has state. The important distinction is what kind of state it has.

Stable construction state is appropriate.

Hidden global orchestration is not.

#### Factory constructor arguments from server and client

The stream server and stream client templates make this dependency path explicit.

Both the `SocketServer` and the `SocketClient` template accept an argument pack:

```cpp
typename... Args
```

Those arguments are forwarded to the concrete `SocketContextFactory` constructor when the application-side server or client handle is constructed.

In schematic form, the pattern is:

```cpp
std::make_shared<SocketContextFactory>(
    std::forward<Args>(args)...
)
```

In other words, the argument pack allows the factory to be preconfigured at the point where the server or client handle is created. The resulting factory object is then part of the shared state used by the registered instance when concrete connections appear.

This means the server or client constructor can provide the stable information the factory needs.

That information may then be stored in the factory and used later when `create(connection)` is called.

The flow is:

```text
SocketServer / SocketClient constructor arguments
  -> SocketContextFactory constructor
      -> stored factory state
          -> create(connection)
              -> SocketContext constructor arguments
```

This is an important distinction.

The argument pack does not mean that arbitrary runtime behavior should be pushed into the factory.

It means that stable construction data can enter the factory at the point where the server or client handle is created.

Used well, this keeps dependency flow explicit:

```text
handle construction
  -> factory construction
      -> context construction
```

The factory remains construction-oriented.

It simply receives the data it needs to create the right context objects later.

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

### Factory design shapes

There is not only one correct factory shape.

The right design depends on what needs to vary at construction time.

Different factory shapes are acceptable when they make construction-time variation explicit.

| Pattern | Use when |
|---|---|
| separate server/client factories | the role distinction should be visible and simple |
| parameterized factory | the context type is the same and only stable constructor data differs |
| context-type-selecting factory | a small, explicit selection among endpoint types is needed |
| preconfigured role factory | higher-level endpoint roles should be fixed at handle construction |

All four patterns can be valid.

The same rule applies to all of them:

> The selection should remain a construction-time decision, not protocol execution.

This section is therefore not a pattern catalogue. It is a set of examples showing how the construction-boundary idea can be expressed without moving protocol behavior into the factory.

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

For example, the role or configuration object may be a constructor argument of the factory itself. In schematic form:

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

The factory is still only expressing a creation decision.

#### What preconfigured factories make possible

Preconfigured factories allow the same framework mechanism to create different communication roles without changing the surrounding server/client machinery.

An application-side server or client handle can pass stable role and dependency information into the factory constructor. The factory can then use that information whenever it creates a context for a new connection.

This can be used for simple role distinctions, such as server-side versus client-side contexts, but also for higher-level endpoint roles:

- model-side endpoints,
- view-side endpoints,
- controller-side endpoints,
- publisher endpoints,
- subscriber endpoints,
- command endpoints,
- event endpoints,
- gateway endpoints,
- adapter endpoints.

The important point in this chapter is still the mechanism, not the full pattern catalogue.

A factory does not implement MVC, publish/subscribe, or gateway behavior by itself. It creates the correctly preconfigured context objects that participate in such patterns.

#### Context-type-selecting factories

Some applications may need a factory that chooses among a small number of context classes.

That can be acceptable when the selection is explicit and construction-time.

For example, a configuration value might decide whether to create a diagnostic context or a normal protocol context.

But the selection should remain simple.

If the factory begins reading from the peer, interpreting protocol frames, or managing state transitions, it has crossed into protocol behavior.

That belongs in the context.

### The strongest factory tests

A useful practical test is:

> If the protocol behavior were removed from the context class, would the factory still appear to contain too much of the application?

If the answer is yes, the factory is probably overgrown.

A good factory should feel incomplete without the context.

That is exactly right.

Its job is to create the protocol endpoint, not to replace it.

Another useful test is:

> Can a developer understand the factory in one glance?

A factory that is hard to skim is often doing more than construction.

One glance does not mean the factory must be trivial. It means the construction decision should be visible. A reader should be able to see which context is created, which stable dependencies are passed, and why that choice belongs at construction time.

### The factory as the Chapter 15 bridge

Chapter 15 will show how the same protocol can be carried over different lower communication families.

The separation is:

```text
SocketContext
  -> protocol behavior

SocketContextFactory
  -> context creation

SocketServer / SocketClient handle
  -> lower-family-specific communication role registration
```

Once protocol behavior is in the context and construction policy is in the factory, lower-family variation becomes easier to manage.

Different server/client types can choose different endpoint families while the factory/context pair preserves the application protocol boundary.

The factory supports that portability story because it keeps context creation separate from the lower-layer role. It does not perform the protocol itself.

### What to remember

- A `SocketContextFactory` is the construction boundary between a concrete `SocketConnection` and the per-connection `SocketContext`.
- The factory creates context objects; the context implements protocol behavior.
- The ordinary creation path should produce a fresh context object for the connection it receives.
- The raw pointer returned by `create(...)` belongs to the framework construction contract, not to arbitrary manual lifetime management.
- Factory constructor arguments are a clean way to pass stable dependencies into future contexts.
- Construction-time selection is acceptable; mid-protocol behavior belongs in the context.
- A good factory is easy to inspect: the reader can see which context type is created and which dependencies are passed.
- Chapter 15 builds on this separation to carry the same protocol over different lower layers.

### Closing perspective

Chapter 13 established the context as the place where protocol behavior lives.

Chapter 14 established the factory as the construction boundary that creates those contexts for concrete connections.

Together, the two chapters separate behavior from construction:

```text
SocketContext
  -> what the protocol endpoint does

SocketContextFactory
  -> how the endpoint object is created for a connection
```

That separation now becomes useful in a broader way.

The same protocol context can often be carried over different lower communication families when the protocol behavior itself does not depend on family-specific address details. The factory is one of the places where that portability becomes practical, because it keeps context construction explicit while the server or client handle chooses the lower-family-specific communication role.

Chapter 15 uses that separation to show how the same protocol can move across different lower layers without turning the application into a pile of special cases.
