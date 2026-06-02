## Building the Same Protocol over Different Lower Layers
### Why this chapter is the architectural payoff

Up to this point, the book has done a great deal of patient groundwork.

We have learned:

- the mental model of SNode.C,
- the runtime model,
- the layer model,
- the communication-role model,
- the address semantics of the major lower families,
- and the proper roles of `SocketContext` and `SocketContextFactory`.

All of that preparation leads naturally to one central architectural question:

> Can the same protocol logic really be carried across different lower layers without losing its shape?

This chapter answers that question.

And the answer is: yes — within the scope where the protocol logic genuinely belongs above the lower-family identity.

This is one of the most important chapters in the whole book, because it turns the framework’s architectural claims into something the reader can actually feel.

If this chapter works, the reader will no longer experience SNode.C as a collection of separate APIs.

They will start experiencing it as one coherent communication architecture whose lower carrier can change while the protocol endpoint model remains remarkably stable.

### What this chapter does — and does not — claim

It is important to begin with honesty.

This chapter does **not** claim that every protocol can be moved unchanged across every lower family.

That would be simplistic and false.

Lower-family choices really do matter.

They affect:

- address identity,
- bind/connect configuration,
- deployment assumptions,
- platform availability,
- security posture,
- operational expectations.

What this chapter *does* claim is more precise and more valuable:

> When the protocol logic is properly kept in the `SocketContext`, and when the lower-family differences are genuinely lower-layer concerns, the same essential protocol behavior can often be carried across very different lower communication families with surprisingly little architectural change.

That is exactly what SNode.C is built to make possible.

### The repository’s echo application already demonstrates the principle

The live repository itself already contains the right teaching clue.

The echo application is not implemented as one isolated example for one socket family only. Instead, the repo organizes echo as a stable protocol idea that can be combined with multiple lower communication families and with both legacy and TLS connection handling.

This is not an accident.

It is a statement of framework philosophy.

The protocol behavior remains conceptually stable. The lower carrier changes. The build and type system assemble the combinations.

That is exactly the architectural lesson this chapter aims to make explicit and teachable.

### The central distinction: protocol shape versus carrier details

To understand this chapter well, the reader must separate two things very clearly.

#### Protocol shape

The protocol shape includes questions like:

- Who sends first?
- What happens when data arrives?
- How are messages interpreted?
- When is a response sent?
- What state is remembered per connection?
- When does the connection close?

These are context-level questions.

They belong to the application protocol endpoint.

#### Carrier details

Carrier details include questions like:

- Is the endpoint identified by host and port?
- Is it identified by a Unix path?
- Is it identified by Bluetooth address and channel?
- Is it identified by Bluetooth address and PSM?
- Is TLS inserted in the connection layer?

These are lower-layer questions.

They matter greatly, but they are not the same kind of question as protocol shape.

SNode.C’s architecture is strong precisely because it helps the reader keep those categories apart.

### The protocol endpoint should not care too early about the carrier

A good `SocketContext` is often much more portable across lower layers than readers first expect.

Why?

Because the context usually works through a connection-facing interface that already abstracts the essential peer operations:

- read from peer,
- send to peer,
- set timeouts,
- close or half-close,
- observe metrics.

That means the context does not usually need to know whether the bytes arrived via:

- IPv4,
- IPv6,
- Unix domain sockets,
- RFCOMM,
- or L2CAP.

As long as the protocol really lives at the application level, the lower carrier can often remain outside the context’s immediate concern.

This is one of the deepest architectural strengths of the framework.

### The same echo protocol over different families

The echo example is the cleanest way to make this concrete.

The essential echo protocol shape is tiny:

- a context exists for one connection,
- if this endpoint is the client role, it may start by sending a message,
- when data arrives, it reads the data,
- it sends the data back,
- it reacts to connection and disconnection lifecycle events.

None of those steps inherently require knowledge of whether the carrier is IPv4, IPv6, Unix domain, RFCOMM, or L2CAP.

That is the entire point.

The same protocol endpoint shape can be carried by different lower families because the context operates through the connection abstraction rather than through raw family-specific socket handling.

### What actually changes when the lower layer changes

Now let us be concrete about what *does* change.

#### The instance type

The outer instance type changes to reflect the chosen lower family.

Examples:

- `net::in::stream::legacy::SocketServer<...>`
- `net::in6::stream::legacy::SocketServer<...>`
- `net::un::stream::legacy::SocketServer<...>`
- `net::rc::stream::legacy::SocketServer<...>`
- `net::l2::stream::legacy::SocketServer<...>`

and the corresponding client types.

#### The address configuration

The values passed through convenience APIs or configuration change accordingly:

- host and port for IPv4 and IPv6,
- path for Unix domain sockets,
- Bluetooth address and channel for RFCOMM,
- Bluetooth address and PSM for L2CAP.

#### Deployment assumptions

The reader’s operational mindset changes:

- local IPC for Unix domain sockets,
- Bluetooth stack availability for RFCOMM and L2CAP,
- dual-stack questions for IPv6,
- interface exposure questions for IP families.

These are real differences.

But notice what has *not* yet changed.

The protocol endpoint model itself is still intact.

### What often does **not** change

This is the more important half of the chapter.

When the protocol is properly factored, the following often remain stable:

- the `SocketContext` type,
- the broad `SocketContextFactory` idea,
- the use of lifecycle hooks such as `onConnected()` and `onDisconnected()`,
- the receive-processing logic in `onReceivedFromPeer()`,
- the per-connection state structure,
- the use of `sendToPeer(...)`,
- the use of `readFromPeer(...)`,
- the event-driven runtime story.

This stable remainder is the real architectural treasure.

Without it, every new lower family would feel like a new framework.

With it, the reader starts to feel genuine transfer.

### The right way to design for portability across lower layers

A reader who wants the same protocol logic to travel well across different lower carriers should follow a few principles.

#### Keep endpoint identity out of the core protocol behavior unless it truly matters

If the protocol does not conceptually care whether the peer is known by host/port, path, channel, or PSM, then the context should not be overfilled with lower-family assumptions.

#### Keep per-connection protocol state in the context

This makes the endpoint logic portable because it remains connection-local and protocol-local.

#### Keep carrier-specific setup in instance configuration and factory selection

That is where lower-family differences belong most naturally.

#### Let the connection abstraction do its job

Use the context through the connection-facing surface rather than reaching around it conceptually toward family-specific socket handling.

This is exactly the separation SNode.C is designed to support.

### The factory often changes less than expected

Another satisfying architectural lesson is that the factory may need less change than the reader first imagines.

If the same context type is appropriate across several lower families, the factory can remain nearly identical.

Sometimes the only thing that changes is the outer instance type used by the application.

Sometimes even the server-side and client-side factory classes remain the same tiny role-specific creators they were before.

This is one of the reasons Chapters 13 and 14 came before this chapter.

A well-factored context and a disciplined factory make lower-layer portability dramatically easier.

### Family-portable does not mean deployment-identical

A very important caution belongs here.

Even when the same protocol logic can be reused cleanly, the resulting applications are not therefore “the same deployment.”

For example:

- an IPv4 variant may be reachable across a LAN or wider network,
- a Unix domain variant is local to the host,
- an RFCOMM variant depends on Bluetooth communication semantics and Bluetooth-stack availability,
- an L2CAP variant does likewise with different endpoint semantics.

So the reader should not confuse **architectural portability** with **operational sameness**.

The framework supports the first. It does not deny the second.

That is the right balance.

### A useful mental exercise: one protocol, five carriers

At this point, the reader should be encouraged to perform a deliberate mental exercise.

Take one small protocol endpoint — perhaps an echo-like request/response protocol, or a framed text command protocol — and ask:

- What would remain unchanged over IPv4?
- What would remain unchanged over IPv6?
- What would remain unchanged over Unix domain sockets?
- What would remain unchanged over RFCOMM?
- What would remain unchanged over L2CAP?

Then ask the complementary question:

- What would I have to reconfigure or redeploy differently in each case?

If the reader can answer those two sets of questions clearly, then they have really understood the framework.

### When a protocol should *not* be forced across every lower layer

A mature design chapter should also say what **not** to do.

There are times when portability across lower layers becomes the wrong goal.

For example:

- if the protocol itself assumes properties that belong to one family only,
- if the deployment model is inherently tied to one carrier,
- if the protocol depends on identity or addressing details that are family-specific,
- or if readability would be damaged by over-generalizing the code.

In such cases, the right design may not be “one context everywhere.”

The real architectural lesson is not blind reuse.

It is *clean factoring*.

Clean factoring lets the reader see when reuse is natural and when divergence is honest.

### A small amount of duplication is often healthy

This point is especially important for experienced C++ developers.

Sometimes the best way to carry the same protocol across several lower layers is not to produce one ultra-clever abstraction that tries to erase every difference.

Sometimes it is better to keep:

- one stable protocol context,
- small clear family-specific instance declarations,
- perhaps tiny role-specific or family-specific entry-point code,
- and explicit outer configuration.

This kind of small duplication is often much healthier than over-abstraction.

SNode.C’s design supports this very well because the major responsibilities are already separated cleanly.

### The chapter’s most important code-design lesson

If the same protocol logic should run across several lower families, write the context so that it thinks in terms of:

- peer communication,
- protocol messages,
- protocol state,
- connection lifecycle,

and *not* in terms of:

- IP literals,
- Unix paths,
- Bluetooth channels,
- Bluetooth PSM values,

unless those things are truly part of the protocol semantics.

This may be the single most important practical design lesson in the whole chapter.

### The role of configuration becomes more visible here

As protocols move across lower families, one design choice in SNode.C becomes even more valuable:

configuration is a first-class part of the model.

That means the same broad application can often be carried into a different lower-family deployment by changing:

- the selected instance type,
- instance configuration values,
- startup arguments,
- or named-instance config-file settings,

while leaving the protocol endpoint behavior largely unchanged.

This is one of the reasons the framework’s configuration model matters so much. It is not only operational convenience. It is architectural leverage.

### The deeper lesson: SNode.C teaches communication roles, not only transports

By now the reader should be able to see something deeper than mere API reuse.

SNode.C is not teaching only “how to use sockets of different kinds.”

It is teaching how to think in terms of:

- communication roles,
- per-connection endpoints,
- protocol-local behavior,
- runtime-driven lifecycle,
- and lower-carrier substitution where appropriate.

That is a much more durable skill than simply learning one convenience overload after another.

This chapter is where that becomes most visible.

### Common misunderstandings about cross-layer protocol reuse

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “If the same protocol can run across several lower layers, then the lower layers do not matter.”

Corrected view: the lower layers matter greatly for endpoint identity, configuration, deployment, and operational assumptions. The point is not that they do not matter. The point is that they do not always have to infect the protocol logic.

#### Misunderstanding 2: “The right abstraction is always one giant family-erasing protocol class.”

Corrected view: clean factoring matters more than maximal flattening. A little explicit outer-layer difference is often healthier than over-generalization.

#### Misunderstanding 3: “If a context ever mentions family-specific details, then the architecture has failed.”

Corrected view: sometimes protocol behavior truly does care about lower-layer details. The goal is not dogma. The goal is honest separation where it makes sense.

#### Misunderstanding 4: “Cross-family reuse means deployment is the same everywhere.”

Corrected view: architectural reuse and deployment sameness are different things. The first may hold while the second clearly does not.

#### Misunderstanding 5: “This chapter is only about echo.”

Corrected view: echo is only the teaching microscope. The real lesson is about how protocol endpoint logic can remain stable while the lower carrier changes.

### A good one-paragraph summary of the chapter

A protocol in SNode.C can often be carried across several lower communication families when its behavior is properly factored into a per-connection `SocketContext`, its creation policy is kept clean in a `SocketContextFactory`, and its family-specific concerns remain where they belong — in instance type selection, configuration, and deployment — rather than leaking prematurely into the protocol endpoint itself.

That is the architectural heart of the chapter.

### Closing perspective

This chapter is the culmination of the entire lower-layer and endpoint-design sequence.

The reader has now seen why the framework’s architecture matters so much.

It matters because it allows the same essential protocol shape to survive meaningful changes in the lower communication carrier.

That is not a trick. It is not accidental. It is the direct result of the framework’s clean separation of:

- outer role,
- connection,
- context,
- factory,
- runtime,
- and lower-layer family identity.

Once the reader feels that clearly, SNode.C becomes much easier to trust and much easier to extend.

And that is the perfect moment to move into the next major phase of the book.

Now that protocol logic, endpoint design, and lower-layer transfer are secure, we can turn toward the framework’s configuration philosophy and show how these applications are actually shaped, named, and operated in practice.
