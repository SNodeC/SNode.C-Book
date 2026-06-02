## Writing `SocketContextFactory` Classes Well
### Why the factory deserves its own chapter

At first glance, `SocketContextFactory` may seem too small to deserve a full chapter.

Its interface is tiny.

In the current live code, the abstract factory essentially asks for one thing only: implement `create(SocketConnection*)` and return a concrete `SocketContext*`.

So why spend a whole chapter on it?

Because the factory sits at an important architectural boundary.

It is the point where the framework moves from:

- the outer communication role,
- and the concrete connection object,

into:

- the protocol endpoint that will actually behave on that connection.

That boundary is small in API surface, but large in architectural meaning.

A badly designed factory makes a codebase feel tangled very quickly. A well-designed factory keeps the whole application calm.

### The factory in one sentence

A good short definition is this:

> A `SocketContextFactory` creates the right per-connection protocol endpoint for a newly established `SocketConnection`.

This definition is deliberately narrow.

It does **not** say that the factory should:

- orchestrate the whole application,
- manage global protocol state,
- act as a configuration registry,
- or become a dependency container for everything in sight.

Its job is to create the right context for the right connection.

That is already important enough.

### The live interface is intentionally minimal

The current live `core::socket::stream::SocketContextFactory` abstraction confirms this minimalist intention very clearly.

It has:

- a protected default constructor,
- a virtual destructor,
- deleted copy and move operations,
- and one essential pure virtual method:

```cpp
virtual core::socket::stream::SocketContext*
create(core::socket::stream::SocketConnection* socketConnection) = 0;
```

That is all.

This is a strong design signal.

The framework is telling the reader:

> Do not turn the factory into a second protocol layer. Keep it focused on creating contexts.

That is exactly the right lesson.

### Why the factory exists at all

A reader might still ask a reasonable question:

Why not just construct the context directly somewhere inside the server or client?

The answer is architectural clarity.

A server may accept many connections over time. A client may establish, lose, and re-establish connections over time. Each of those concrete connections needs its own protocol endpoint.

The framework therefore needs a systematic way to say:

> When a new connection becomes real, create the right context for it.

That is the factory’s job.

If that responsibility were pushed into ad hoc lambdas, giant conditionals, or outer instance code, the framework would become much harder to reason about.

The factory solves exactly that problem.

### The factory is where construction policy lives

A useful way to think about the factory is this:

The context contains **protocol behavior**. The factory contains **protocol-endpoint construction policy**.

That is a very important distinction.

A good factory answers questions like:

- Which concrete context type should be created for this connection?
- What constructor arguments does that context need?
- Should the created context represent a client role or server role?
- Which stable dependencies should be passed into the context?

A good factory should **not** try to perform the protocol itself.

That belongs to the context.

### The live echo example shows the ideal small pattern

The current live echo code is an excellent teaching example here.

Its two concrete factory classes are extremely small.

They do one thing each:

- the server-side factory creates an `EchoSocketContext` with role `SERVER`,
- the client-side factory creates an `EchoSocketContext` with role `CLIENT`.

That is beautiful design.

The factories do not duplicate the protocol behavior. They do not start reading or writing. They do not manage runtime flow. They simply decide which role-specific context should be attached to the connection.

This is exactly the kind of disciplined minimalism the reader should aim for.

### The first rule: keep the factory boring

This may sound strange, but it is one of the most useful design rules in the chapter.

A good `SocketContextFactory` should usually be a little boring.

That is not an insult.

It is praise.

A boring factory is often a sign of a healthy architecture.

It means:

- the protocol behavior is living in the context where it belongs,
- the outer communication role is living in the instance where it belongs,
- the connection remains the concrete peer relationship,
- and the factory is doing its narrow job cleanly.

The more “exciting” a factory becomes, the more likely it is that responsibilities are being mixed.

### The second rule: create one context per connection and mean it

This sounds obvious, but it matters deeply.

The factory should create a fresh context that truly belongs to the connection it is given.

That means the reader should think clearly in per-connection terms.

A context is not a global singleton. It is not a reusable shared protocol shell. It is not one object that should somehow represent all peers at once.

The whole point of the factory is to create a fresh protocol endpoint for one concrete peer relationship.

This is one of the architectural habits that keeps SNode.C applications understandable even as they grow.

### The third rule: let constructor arguments express stable protocol dependencies

The factory is a good place to decide which stable dependencies a context needs at construction time.

For example, a context might reasonably need:

- a role indicator,
- a shared immutable configuration object,
- a reference-counted service interface,
- a protocol parser helper,
- a small shared registry or dispatcher object.

The key word here is **stable**.

A good factory passes in dependencies that define how the context should operate.

It should not try to inject half the application universe indiscriminately.

When factories become giant dependency funnels, the resulting contexts often become hard to understand and hard to test mentally.

### The fourth rule: do not make the factory a service locator

A common architectural mistake is to let a factory become a secret passage to everything in the application.

The code still “works,” but the design quality drops sharply.

A bad factory starts to behave like this:

- create the context,
- give it a logging registry,
- give it a metrics manager,
- give it a service map,
- give it a global session store,
- give it database handles,
- give it unrelated orchestration callbacks,
- give it access to half the process.

At that point the factory is no longer expressing construction policy.

It is acting like a dependency dumping ground.

That usually means the protocol boundary is already being eroded.

A good factory should instead ask a disciplined question:

> What does this context genuinely need in order to be the protocol endpoint for this connection?

### The fifth rule: keep role decisions explicit

The live echo example shows this very well.

The factory decides whether the context should act in server role or client role.

That is a very good use of a factory.

A context often needs some role-specific knowledge at construction time.

It may need to know:

- whether it initiates the conversation,
- whether it expects the first frame from the peer,
- whether it behaves as producer or consumer first,
- whether it represents one side of an otherwise symmetric protocol.

The factory is often the cleanest place to make that decision explicit.

This is much better than creating one ambiguous context and then letting it discover its role through scattered runtime guesses.

### The sixth rule: do not hide major protocol branching in the factory

A factory can legitimately decide *which context type* to create.

But there is an important boundary.

If the factory begins containing large branches that effectively implement protocol logic, then the design is drifting.

For example, a factory that merely chooses among a small set of concrete endpoint classes is often fine.

A factory that starts doing things like:

- parsing initial bytes,
- deciding mid-protocol transitions,
- managing authentication logic,
- controlling conversation flow,
- or holding large mutable protocol state,

is usually no longer “just a factory.”

In such cases, protocol behavior is leaking out of the context and into the construction boundary.

That makes the application harder to teach and harder to reason about.

### The connection pointer is not an inconvenience — it is the whole point

The live interface passes a `SocketConnection*` into `create(...)`.

That is not just an implementation detail.

It is the precise statement of what the framework needs from the factory.

The new context must be attached to a specific concrete connection.

That means the factory’s mental model should always be:

- here is the new concrete peer relationship,
- now create the protocol endpoint that belongs on it.

This keeps the architecture grounded.

The factory is not creating contexts in the abstract. It is creating them *for a particular connection*.

### The factory should preserve, not blur, the instance/context boundary

A good `SocketContextFactory` helps protect one of the framework’s most important boundaries.

The instance:

- remains the outer communication role.

The context:

- remains the per-connection protocol endpoint.

The factory:

- bridges between them without collapsing them.

This is a surprisingly powerful design effect.

Because the bridge is small and explicit, the rest of the framework stays legible.

The moment the factory starts absorbing instance responsibilities or context responsibilities, that clarity begins to fade.

### Passing shared application state: what is reasonable

Some readers reasonably worry that a “small factory” sounds too idealized for real applications.

Real applications do sometimes need shared services or shared state.

That is true.

The important question is *how* those are introduced.

A good factory may absolutely capture or store references to stable shared resources, such as:

- a shared protocol configuration,
- a thread-safe statistics object,
- a shared dispatcher,
- a reference-counted service interface.

But the test is still the same.

Those resources should help the context be the right protocol endpoint. They should not turn the context into an uncontrolled portal to the whole application.

This is a matter of design discipline, not prohibition.

### Construction logic should remain easy to read in one glance

A useful practical standard is this:

A developer should be able to open a factory class and understand its construction logic almost immediately.

That means a good factory should usually answer questions like:

- Which context class is created?
- What constructor arguments are passed?
- What role or stable dependencies are being encoded?

without forcing the reader to scroll through a maze of side effects.

This is another reason the live echo factories are such good examples.

A reader can understand them in seconds.

That is not because they are trivial. It is because they respect the architectural boundary.

### Symmetry between server-side and client-side factories is good when it is real

The current echo example also teaches a subtle but important style lesson.

The server-side and client-side factories are separate, but symmetrical.

That is very often a good pattern.

If the server and client roles share the same broad endpoint type but differ in one role-specific construction decision, separate tiny factories are often cleaner than one over-generalized “smart” factory.

A reader should not be afraid of small duplication when that duplication keeps the structure obvious.

Clarity is usually more valuable than cleverness here.

### When one factory type may still be appropriate

There are cases where one reusable factory type is still the right design.

For example:

- if the role is provided as a constructor parameter,
- if the context type is identical and only a small stable dependency differs,
- if the application intentionally wants one parameterized factory abstraction reused in several outer roles.

That can be perfectly reasonable.

But the same rule still applies:

the factory should stay construction-oriented, not protocol-oriented.

The moment it starts becoming a hidden protocol engine, the design is drifting.

### Ownership and raw-pointer return type: what the interface is saying

The current factory interface returns a raw `SocketContext*`.

In modern C++ discussions, that can make readers nervous if they assume every raw pointer implies unsafe design.

Here, the important thing is to read the interface in architectural context.

The factory is transferring a newly created protocol endpoint into the framework-managed connection/context lifecycle.

That means the design intention is not “manual random ownership everywhere.”

It is “construct the endpoint object the framework will then manage in its own lifecycle.”

The most important practical rule for the reader is therefore simple:

Create the right concrete endpoint object and let the framework’s architecture own the larger lifecycle story.

### The factory should not know more than necessary about runtime flow

Because the factory lives at an important boundary, readers may be tempted to use it as a place to smuggle runtime coordination in.

That is usually unwise.

A good factory does not need to know too much about:

- event-loop sequencing,
- retry logic,
- reconnection policy,
- accept-per-tick tuning,
- or multiplexer details.

Those concerns belong elsewhere in the framework.

The factory should remain close to one decisive moment only:

> A concrete connection exists. Which protocol endpoint should be attached to it?

That focus is what keeps it healthy.

### The strongest factory test

A very good practical test for a `SocketContextFactory` is this:

If you erased the protocol behavior from the context class, would the factory still appear to contain “too much of the application”?

If the answer is yes, the factory is likely overgrown.

A good factory should feel incomplete without the context.

That is exactly right.

Its job is to create the protocol endpoint, not to replace it.

### Common mistakes when writing `SocketContextFactory` classes

It helps to clear away a few mistakes explicitly.

#### Mistake 1: Making the factory too smart

Corrected view: keep the factory focused on construction policy, not protocol behavior.

#### Mistake 2: Sharing one context object across several connections

Corrected view: create a fresh context for each concrete connection.

#### Mistake 3: Turning the factory into a service locator

Corrected view: pass only the stable dependencies the endpoint really needs.

#### Mistake 4: Hiding role decisions implicitly

Corrected view: make server/client or similar role distinctions explicit at construction time when they matter.

#### Mistake 5: Using the factory as a workaround for unclear protocol design

Corrected view: if protocol logic is drifting into the factory, it is often a sign the context itself needs better design.

### A good `SocketContextFactory` in one paragraph

A good `SocketContextFactory` is a small, readable construction boundary that creates one fresh protocol endpoint per connection, passes in only the stable dependencies that endpoint genuinely needs, keeps role decisions explicit when necessary, and resists the temptation to absorb protocol behavior, global orchestration, or runtime responsibilities that belong elsewhere in the framework.

That is the standard the reader should aim for.

### Closing perspective

This chapter is short in surface API and large in architectural importance.

The factory is one of the smallest interfaces in the framework, but it protects one of the most valuable boundaries:

- outer communication role on one side,
- per-connection protocol endpoint on the other.

When that boundary is kept clean, the framework feels elegant. When that boundary is blurred, the codebase gets muddy very quickly.

That is why the factory deserves care even though its interface is tiny.

The reader should now have a calm, practical standard in mind:

- keep the factory small,
- keep it readable,
- keep it construction-oriented,
- let the context carry the behavior.

That is the right style for SNode.C.

And with that, the book is ready for an especially satisfying next step:

showing how the *same protocol logic* can be carried over different lower communication families without changing its essential shape.

That means the next chapter is the natural culmination of this whole architectural sequence.
