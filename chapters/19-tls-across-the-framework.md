## TLS Across the Framework
### Why TLS belongs here in the book

TLS is one of the best architectural tests in the whole framework.

If SNode.C’s layering is real, then TLS should not feel like a separate world.

It should feel like a meaningful change in one layer of the communication model while the larger application structure remains recognizable.

That is exactly what the framework does.

This chapter therefore is not only about certificates and encrypted transport. It is about one of the most important architectural promises SNode.C makes to the reader:

> security can be inserted into the connection layer without forcing the whole application model to collapse and be rebuilt.

That is a very strong promise.

And it is one of the reasons SNode.C is especially suitable for serious networked systems rather than only toy examples.

### The big picture: TLS is a connection-layer choice

Earlier chapters already introduced the layered model:

- network family,
- transport form,
- connection handling,
- application protocol.

TLS belongs above the lower communication family and transport form, but below the application protocol.

That means:

- IPv4 can be carried with legacy connection handling or TLS connection handling,
- IPv6 can be carried with legacy connection handling or TLS connection handling,
- Unix domain sockets can still participate in the same connection-layer distinction,
- and even Bluetooth-facing families still fit into the same architectural story.

This is one of the most important conceptual lessons in the entire book.

TLS is not “an application protocol feature.” TLS is not “a different runtime.” TLS is a connection-layer specialization.

### The live code confirms the architecture very clearly

The current live TLS wrappers for IPv4 make this beautifully explicit.

The TLS server type is not a wholly separate hand-built application class. It is a type alias built by combining:

- the existing `net::in::stream::SocketServer` shell,
- a TLS `SocketAcceptor`,
- and a TLS-specific configuration type.

The TLS client type is built in the same style from:

- the existing `net::in::stream::SocketClient` shell,
- a TLS `SocketConnector`,
- and a TLS-specific configuration type.

This is exactly the kind of code shape a teaching book hopes to find.

It means the framework is not merely *described* as layered.

It is actually implemented that way.

### What changes when TLS is inserted

TLS changes real things.

A mature chapter should be very honest about that.

When TLS is inserted, the following kinds of concerns become real:

- certificate material,
- private key material,
- trust anchors or CA configuration,
- handshake success and failure,
- SSL/TLS initialization and shutdown timeouts,
- peer validation policy,
- SNI and name-related concerns,
- error handling at the encryption boundary.

These are not superficial details.

They are exactly why TLS belongs in a dedicated chapter.

But it is equally important to notice what often remains stable.

### What often does **not** change

When a legacy application is moved to TLS in SNode.C, many architectural elements often remain surprisingly stable:

- the server or client outer role,
- the instance/factory/context pattern,
- the runtime story,
- the connection lifecycle shape,
- the protocol endpoint logic,
- the basic server/client relationship,
- the use of `sendToPeer(...)` and `readFromPeer(...)` through the context.

This is exactly the payoff of the framework’s design.

A reader should not conclude that TLS is trivial.

But the reader *should* conclude that TLS does not require a fresh architectural worldview.

That is the right lesson.

### The TLS wrappers are intentionally parallel to the legacy ones

A particularly important teaching point is the structural parallelism between legacy and TLS wrappers.

In the live code, the TLS wrappers reuse the outer server/client shell and simply change the connection-layer machinery and config type.

That means the reader can still think in familiar terms:

- create a server or client instance,
- configure it,
- attach a context factory,
- activate `listen()` or `connect()`,
- let the runtime create concrete peer connections,
- let the context implement protocol behavior.

This is the same broad shape the reader has already learned.

That continuity is one of the strongest features of the framework.

### The TLS connection object proves the layer boundary

The live `core::socket::stream::tls::SocketConnection` is one of the clearest architectural pieces in the codebase.

It is still a `SocketConnection`, but it is specialized with:

- a TLS reader,
- a TLS writer,
- SSL startup and shutdown logic,
- handshake behavior,
- SSL timeouts,
- and access to the underlying `SSL*`.

This is a wonderful confirmation of the framework’s structure.

The connection object remains the connection object.

But its reader/writer machinery and internal lifecycle are now TLS-aware.

That is exactly how a cleanly layered system should handle encryption.

### TLS should not leak prematurely into the context

This is one of the most important design rules of the chapter.

A `SocketContext` should only become TLS-aware when the protocol logic genuinely needs TLS-specific information.

In many applications, the protocol endpoint does not need to care.

It still needs only to:

- react to `onConnected()`,
- read from the peer,
- send to the peer,
- maintain protocol state,
- respond to disconnects.

That means TLS should usually remain primarily a connection-layer and configuration concern rather than being injected into ordinary protocol logic everywhere.

This is one of the ways SNode.C protects the clarity of application code.

### But TLS-specific inspection still has a real place

At the same time, a good framework should not hide TLS completely.

There are real cases where the application or operator needs visibility into:

- which certificate was presented,
- whether handshake succeeded,
- which SSL object exists on the connection,
- whether peer validation passed or failed,
- or what TLS-specific timeout or shutdown behavior occurred.

The live TLS connection class exposes `getSSL()`, which is a strong signal that SNode.C does not forbid such visibility. It simply keeps it at the right layer.

That is exactly the right compromise.

TLS-specific inspection is possible when it matters, but it does not have to contaminate every ordinary protocol endpoint.

### The TLS config types show the intended composition model

The current live IPv4 TLS config types reinforce the same point very elegantly.

`net::in::stream::tls::config::ConfigSocketServer` is built as a TLS-config specialization on top of the non-TLS IPv4 stream server config.

`net::in::stream::tls::config::ConfigSocketClient` is built the same way on top of the non-TLS IPv4 stream client config.

This is exactly what the architecture chapters argued should happen.

TLS configuration is not a whole separate application-configuration universe.

It is an added specialization layered on top of an already meaningful communication-role configuration.

That is one of the strongest structural confirmations in the codebase.

### The `tls` section in configuration is one of the clearest section boundaries

The earlier configuration chapters introduced the section model:

- `local`
- `remote`
- `connection`
- `socket`
- `server`
- `tls`

TLS is one of the most satisfying examples of why the section model works so well.

The `tls` section groups exactly the settings that belong to the TLS specialization rather than scattering them across unrelated parts of the configuration model.

This means the reader can think clearly:

- the communication role still has its local and remote identity,
- it still has connection and socket behavior,
- and it additionally has TLS-specific settings when encrypted operation is desired.

That is architectural clarity in practical configuration form.

### The most important TLS settings conceptually

A teaching chapter does not need to turn into a long OpenSSL option catalog.

What matters most is the conceptual grouping of the main TLS concerns.

A TLS-enabled instance usually needs to think about:

- certificate chain,
- certificate key,
- key password if relevant,
- CA certificate or CA directory,
- cipher or protocol policy,
- SSL/TLS initialization timeout,
- SSL/TLS shutdown timeout,
- SNI-related behavior,
- peer validation policy.

That list is important not because every application needs every item equally, but because it teaches the reader what kind of change TLS really introduces.

TLS is not “just turn encryption on.”

It is a serious connection-layer policy and identity configuration.

### Why handshake behavior changes the mental timeline slightly

In legacy communication, it is easy for beginners to think of connection establishment as a single simple transition.

TLS makes the timeline slightly richer.

A physical or transport-level connection can exist, and then TLS handshake activity must still complete before the connection is fully ready in the stronger sense relevant to secure communication.

This is one of the reasons the framework’s distinction between `onConnect` and `onConnected` is so valuable.

Even without turning the chapter into a deep state-machine analysis, the reader should understand this much:

TLS adds meaningful intermediate work to the path from lower-layer connection to fully usable secure endpoint.

That is another reason it belongs at the connection layer.

### TLS and server/client symmetry

Another satisfying property of the framework is that TLS does not destroy the larger server/client symmetry.

A TLS server is still fundamentally:

- a server role,
- a configuration-bearing instance,
- a factory of secure per-connection endpoints.

A TLS client is still fundamentally:

- a client role,
- a configuration-bearing instance,
- an initiator of secure per-connection endpoints.

TLS enriches and complicates the connection layer, but it does not break the higher structural symmetry.

That is exactly what a good layered design should accomplish.

### TLS and diagnostics become even more important together

The diagnostics chapter becomes especially relevant here.

Once TLS enters the picture, visibility matters even more.

Why?

Because secure communication failures are often more subtle than plain socket failures.

A developer may need to understand:

- whether the transport connection existed at all,
- whether handshake began,
- whether handshake succeeded,
- whether peer trust failed,
- whether certificates were missing or mismatched,
- whether timeout occurred during initialization or shutdown.

This is why SNode.C’s layered visibility model is so useful.

The framework already provides:

- instance-level lifecycle hooks,
- connection-level counters and addresses,
- TLS-specific connection access,
- logger levels and verbose levels,
- configuration display and command-line generation.

Those pieces become especially valuable in TLS scenarios.

### TLS does not erase the lower family beneath it

A subtle but very important point belongs here.

Once TLS is active, the reader should not start imagining that the lower family has disappeared.

It has not.

A TLS connection is still carried over some lower communication family and transport form.

That means it still matters whether the carrier beneath TLS is:

- IPv4,
- IPv6,
- Unix domain,
- RFCOMM,
- or L2CAP.

TLS does not abolish those distinctions.

It specializes the connection layer that sits above them.

That is one of the reasons the earlier lower-family chapters were so important.

### The cleanest migration story: legacy first, TLS second

From a teaching perspective, the best migration pattern is usually:

1. understand the legacy application first,
2. understand its context and factory clearly,
3. understand its lower-family configuration clearly,
4. then introduce TLS as a connection-layer upgrade.

This is much better than teaching TLS as the primary first exposure.

Why?

Because the reader can then see very clearly what TLS changed and what it did not change.

That makes the architecture much easier to trust.

### When protocol logic really should care about TLS

Although most of the chapter has emphasized clean separation, there are honest cases where protocol logic or higher-layer behavior really does care about TLS.

Examples include:

- protocols whose identity model depends on peer certificates,
- application behavior that adapts to secure versus insecure modes,
- logging or auditing that must record TLS properties,
- applications that expose certificate or handshake details to higher layers.

In those cases, the design should still remain disciplined.

Do not let every ordinary context become TLS-heavy by default.

Instead, let TLS-specific meaning rise into the protocol only when the protocol genuinely requires it.

That is the right balance between abstraction and honesty.

### A good rule of thumb for writing TLS-capable applications in SNode.C

A very useful design rule is this:

Write the protocol endpoint as if secure and insecure transport are the same conversation whenever that is honestly true.

Then let:

- the instance type,
- the connection-layer wrapper,
- and the TLS section of the configuration

carry the secure-transport differences.

Only promote TLS details into the protocol logic when the protocol semantics truly require them.

This one rule will keep a great deal of application code cleaner.

### Common misunderstandings about TLS in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “TLS creates a completely separate application architecture.”

Corrected view: in SNode.C, TLS is primarily a connection-layer specialization built on the same outer server/client structure.

#### Misunderstanding 2: “If TLS is enabled, the protocol endpoint must become TLS-heavy.”

Corrected view: most ordinary protocol logic should remain focused on the application conversation unless TLS-specific semantics genuinely matter.

#### Misunderstanding 3: “TLS hides the lower communication family.”

Corrected view: the lower family still matters; TLS sits above it as connection-layer handling.

#### Misunderstanding 4: “TLS configuration is a separate side system.”

Corrected view: TLS configuration is layered into the same configuration model through the `tls` section and TLS-specific config types built on top of non-TLS config.

#### Misunderstanding 5: “A secure connection becomes opaque and harder to reason about.”

Corrected view: the framework keeps TLS visible at the right layer, including connection-level SSL access and configuration-level policy control.

### A good one-paragraph summary of the chapter

TLS in SNode.C is best understood as a connection-layer specialization that reuses the same outer server/client shells, the same runtime model, and the same instance/factory/context pattern while adding secure reader/writer machinery, handshake behavior, certificate and trust configuration, and TLS-specific timing and policy concerns. This lets secure and insecure variants of the same broad application remain architecturally close without pretending that the security differences are trivial.

That is the heart of the chapter.

### Closing perspective

This chapter is one of the strongest confirmations of SNode.C’s architecture.

The framework does not merely *say* that it is layered.

It demonstrates that layering concretely by allowing TLS to enter as a serious, visible, but well-contained specialization.

That is exactly what readers need in a modern communication framework.

They need security that is real, but not architecturally chaotic.

SNode.C provides that.

And once the reader understands TLS this way, the next major topic becomes natural.

After secure transport, the next thing the reader must understand is how the framework behaves when communication is slow, interrupted, delayed, retried, or partially failing over time.

That means the next chapter is about timeouts, retries, and failure modes.
