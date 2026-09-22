## Writing `SocketContextFactory` Classes Well {#writing-socketcontextfactory-classes-well}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain the ownership handoff when a factory returns a context or refuses creation.
- **O2.** Diagnose whether partial input leaks between peers or into a replacement connection.
- **O3.** Choose how stable settings and shared services reach each new context.
:::

\index{SocketContextFactory@\texttt{SocketContextFactory}}
\index{factory design}
\index{context construction}

A `SocketContext` owns per-connection protocol behavior; a `SocketContextFactory` defines how such contexts are created.

For the line protocol, creating a new context also creates a new receive buffer. For an application with a shared measurement model, creation must additionally supply access to that model without sharing the receive buffer. The same small interface serves both cases, but the dependency and lifetime decisions need to be explicit.

### The factory interface and attachment

\index{SocketContextFactory@\texttt{SocketContextFactory}}
\index{factory interface}

The stream factory interface is narrow. Its essential method is:

```cpp
virtual core::socket::stream::SocketContext*
create(core::socket::stream::SocketConnection* socketConnection) = 0;
```

\index{ownership}
\index{lifecycle}

The interface receives a `SocketConnection*` and returns a `SocketContext*`. The raw pointer return is part of the framework construction contract: the factory creates the context object, returns it once, and the connection side of the framework attaches and manages it. Application code should not keep separate ownership of that object or delete it manually.

\index{SocketConnection@\texttt{SocketConnection}!context attachment}
\index{SocketContextFactory@\texttt{SocketContextFactory}!create}

The pinned stream-connection source in `src/core/socket/stream/SocketConnection.cpp` shows the same boundary in compact form. The connection asks the factory to create a context for `this` connection, attaches the result when creation succeeds, and closes the connection if no context can be created:

```cpp
void SocketConnection::setSocketContext(
    const std::shared_ptr<SocketContextFactory>& socketContextFactory) {
    SocketContext* socketContext = socketContextFactory->create(this);

    if (socketContext != nullptr) {
        setSocketContext(socketContext);
    } else {
        close();
    }
}
```

The next step is equally important: the newly created context is attached to the connection. If a context already exists, the new one is staged as a replacement rather than treated as a shared global endpoint.

```cpp
void SocketConnection::setSocketContext(SocketContext* socketContext) {
    if (this->socketContext == nullptr) {
        this->socketContext = socketContext;
        socketContext->attach();
    } else {
        newSocketContext = socketContext;
    }
}
```

\index{context construction}
\index{connection-to-context path}

\index{fresh context per connection}
\index{per-connection state}

The most important rule is simple:

::: {.snodec-rule title="Factory responsibility rule"}
A factory should create a fresh context for the concrete connection it receives.
:::

The framework also supports context replacement as a more advanced connection operation. That does not weaken the construction rule. If a later context switch is used, the new context is still a fresh endpoint object handed to the framework. It is not a reused singleton shared across peers and it is not a hidden global protocol object.

### Construction responsibilities of a factory

\index{factory responsibilities}
\index{dependency injection}

A useful contrast is:

| Belongs in the factory | Does not belong in the factory |
|---|---|
| choosing the context type | protocol message handling |
| passing stable dependencies | read/write behavior |
| setting role-specific constructor arguments | retry or reconnect policy |
| creating one fresh context | global orchestration |
| keeping construction readable | service-location dumping ground |
| making construction-time choices | mid-protocol state transitions |

Factories may need several arguments, select a context type, or carry role information. Their complexity should remain construction complexity.

A factory can legitimately choose which concrete context type to create. For many simple applications, there is exactly one concrete context type.

In that case, the factory is almost mechanical. In schematic form:

```cpp
SocketContext* create(SocketConnection* connection) override {
    return new MySocketContext(connection);
}
```

In other applications, the factory may choose among a small set of endpoint types. That can be reasonable if the choice is a construction-time decision.

It becomes problematic only when the factory starts performing protocol behavior that belongs inside the context. Choosing a context type is construction. Reading protocol frames, interpreting commands, and advancing protocol state are behavior.

A context may need stable dependencies at construction time. Examples include:

- a role indicator,
- immutable protocol configuration,
- a shared service interface,
- a parser helper,
- a statistics sink,
- a small dispatcher object.

The factory can hold stable dependencies and pass them to each new context. Each dependency should answer a specific protocol need rather than provide hidden access to the entire application.

A factory is often a good place to make role-specific construction decisions.

For example, a protocol may use the same context class on both sides but pass a role value:

```cpp
enum class Role { Server, Client };
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

The role decision is visible at construction; neither factory executes the conversation.

### Responsibilities that should stay out of the factory

\index{factory anti-patterns}
\index{protocol behavior}

Parsing, authentication exchanges and mid-protocol state transitions belong to the context. Retry, reconnect, accept-loop tuning and event sequencing belong to the registered instance, flow controller and runtime. Splitting those behaviors across construction and endpoint code makes the conversation harder to follow.

A factory may pass explicit stable services into a context. That is different from becoming a service locator.

A context may need a database facade, dispatcher or statistics service. Pass that dependency explicitly; do not hide a route to unrelated registries and session stores behind the factory.

Connection-local protocol state belongs in the context. Application-level shared state belongs in an application-level service or model.

The factory should not become the place where large mutable protocol state is accumulated simply because it is convenient.

Factory state should usually be stable construction state, not evolving per-message protocol state. A role value, a configuration object, or a service reference can be construction state. A partially parsed message, peer conversation phase, or connection-local protocol buffer belongs in the context.

### Passing shared application state

\index{shared application state}
\index{dependency passing}

A factory can keep references to immutable settings, a statistics service, dispatcher, logger abstraction or application model. The dependencies must remain valid for every context that receives them.

The stream server and stream client templates make this dependency path explicit.

Both the `SocketServer` and the `SocketClient` template accept an argument pack:

```cpp
typename... Args
```

Those arguments are forwarded to the concrete `SocketContextFactory` constructor when the server/client handle is constructed.

In schematic form, the pattern is:

```cpp
std::make_shared<SocketContextFactory>(std::forward<Args>(args)...)
```

The argument pack allows the factory to be preconfigured at the point where the server or client handle is created. The resulting factory object is then part of the shared state used by the registered instance when connections appear.

This means the server or client constructor can provide the stable information the factory needs. That information may then be stored in the factory and used later when `create(connection)` is called.

Stable data enters at handle construction and is passed into each context later. This permits explicit dependency passing, not arbitrary runtime behavior or access to the whole application through the factory.

The form of the dependency also records a lifetime decision:

| Form passed into the context | Useful when | Obligation |
|---|---|---|
| immutable value copied into each context | each conversation needs stable settings | later changes to the original value do not update existing copies |
| reference to an application-owned model | one clearly scoped application object outlives all users | construction and shutdown order must preserve that lifetime |
| shared ownership of a service | users must retain the service independently | avoid cycles and remember that shared ownership does not make mutation thread-safe |

None of these forms is universally best. MiniGateway's model reference is readable because `main()` owns the model across runtime execution. A helper-local model would make the same reference unsafe. Copying an immutable parser limit can be simpler than making every connection observe live configuration. Shared ownership is useful when independent retention is required, but adds a lifetime relationship that must still be explained.

### Factory design shapes

\index{factory design shapes}
\index{parameterized factories}
\index{preconfigured factories}

There is more than one correct factory shape. The right design depends on what needs to vary at construction time. Different factory shapes are acceptable when they make construction-time variation explicit.

| Pattern | Use when |
|---|---|
| separate server/client factories | the role distinction should be visible and simple |
| parameterized factory | the context type is the same and only stable constructor data differs |
| context-type-selecting factory | a small, explicit selection among endpoint types is needed |
| preconfigured role factory | higher-level endpoint roles should be fixed at handle construction |

::: {.snodec-warning title="Factory-scope warning"}
The selection should remain a construction-time decision, not protocol execution.
:::

Separate server-side and client-side factories can be useful when the two roles should be visible. This is especially clear when both sides use the same context type but receive different role arguments. The benefit is readability.

Small duplication is often acceptable when it makes the communication roles clearer.

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

This can be a clean design when the factory remains easy to read and the variation is stable. The factory is still only expressing a creation decision.

Preconfigured factories allow the same framework mechanism to create different communication roles without changing the surrounding server/client machinery.

A server/client handle can pass stable role and dependency information into the factory constructor. The factory can then use that information whenever it creates a context for a new connection.

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

The important point is still the mechanism, not a full pattern catalogue: a factory does not implement a higher-level application pattern by itself, but creates the correctly preconfigured context objects that participate in such patterns.

Some applications may need a factory that chooses among a small number of context classes. That can be acceptable when the selection is explicit and construction-time. For example, a configuration value might decide whether to create a diagnostic context or a normal protocol context.

The selection should remain simple. If the factory begins reading from the peer, interpreting protocol frames, or managing state transitions, it has crossed into protocol behavior, and that belongs in the context.

### The strongest factory tests

\index{factory tests}
\index{construction tests}

A readable factory should reveal its context type, constructor arguments, and ownership assumptions quickly. That is a useful review question, but behavior gives a stronger test.

Create two peers through the same server and leave a partial command pending on one. The other should complete its own command independently. Then disconnect the first and open a replacement peer. Its new context should begin with fresh protocol state, while an intentionally shared application model should retain the state owned by the application. This distinguishes fresh contexts from shared services without testing the spelling of `new` or the number of constructor arguments.

The failure path also has a contract: returning `nullptr` from `create(...)` causes the connection to close, as the source anchor shows. A test factory that deliberately refuses one connection can exercise that outcome. It should observe closure at the peer boundary and no protocol-ready context callback for the refused context; it should not manually delete a connection supplied by the framework.

Chapter 11 will show how the same protocol can be carried over different lower families.

Keep the context's input buffer and the factory's dependencies fixed while changing only the outer endpoint selection. The next chapter performs that comparison with a runnable line server, so reuse is checked through returned bytes as well as through similar declarations.

::: {.snodec-remember title="What to remember"}
- The factory creates context objects; the context implements protocol behavior.
- The ordinary creation path should produce a fresh context object for the connection it receives.
- The raw pointer returned by `create(...)` belongs to the framework construction contract, not to arbitrary manual lifetime management.
- Factory constructor arguments are a clean way to pass stable dependencies into future contexts.
- Construction-time selection is acceptable; mid-protocol behavior belongs in the context.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace a returned context pointer through attachment and later detachment. Contrast returning `nullptr`; explain why the factory must not retain ownership or share the same context between peers.
2. **Review (O3).** Compare a copied parser limit, a model reference and shared service ownership. Give one lifetime obligation for each, including what shared ownership does not guarantee.
3. **Lab (O2).** Build the fresh-context lab. Leave `PI` pending on one peer while another receives `OK`. Abandon the partial peer and send `NG` on a replacement; expect an unknown-command response, then successful independent `PING` replies.
4. **Lab (O1).** Run the refusing-factory lab. Expect the first peer to close before `READY`, while the next receives `READY` and answers `PING`. Identify the construction failure separately from a parser rejection.
5. **Design (O1, O3).** Supply one measurement model to contexts on two input roles with different immutable parser limits. Choose value, reference or shared ownership for each dependency; justify shutdown order and where future protocol authentication would run.

Public answers, commands, and observations: `companion/exercises/ch10/README.md`.
:::
