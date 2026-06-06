## TLS Across the Framework

### From visible runtime behavior to secure connection handling

Chapter 18 showed how configured communication roles become visible at runtime.

Chapter 19 begins the next part of the book by adding secure connection handling to the same architecture.

TLS does not introduce a second application model.

It changes the connection layer.

That is the central idea of this chapter:

> TLS changes the connection layer; it does not replace the application architecture.

A TLS-enabled SNode.C application still has:

- server and client roles,
- named instances,
- configuration sections,
- factories,
- contexts,
- connection lifecycle,
- runtime diagnostics.

What changes is the connection handling between the lower transport and the application protocol.

### TLS as a connection-layer specialization

The layered model is:

```text
network family
  -> transport form
      -> connection handling
          -> application protocol
```

TLS belongs in the connection-handling position.

It sits above the lower communication family and transport form.

It sits below the application protocol.

That means:

```text
IPv4 stream
  -> legacy connection handling
      -> protocol context

IPv4 stream
  -> TLS connection handling
      -> protocol context
```

The lower family still exists.

The server/client role still exists.

The context still implements the protocol conversation.

TLS adds secure connection handling between those parts.

A more general view is:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection layer
          -> SocketContext
```

Where a TLS wrapper exists for a lower family, the same pattern applies.

The architectural model is not limited to IPv4, but concrete support depends on the available TLS wrapper for that family.

### Legacy and TLS streams side by side

A compact comparison makes the teaching point visible.

| Concern | Legacy stream | TLS stream |
|---|---|---|
| outer server/client role | same model | same model |
| lower family | IPv4, IPv6, Unix, etc. | still present |
| connection machinery | legacy reader/writer | TLS reader/writer |
| setup work | socket/connect/listen | socket/connect/listen plus TLS handshake |
| shutdown work | socket shutdown/close | socket shutdown/close plus TLS shutdown / close-notify handling |
| configuration | `local` / `remote` / `socket` / `server` | `local` / `remote` / `socket` / `server` plus `tls` |
| context behavior | protocol endpoint | usually unchanged |
| diagnostics | lifecycle/counters/errors | lifecycle/counters/errors plus TLS-specific handshake/shutdown failures |

This table is the chapter in miniature.

TLS adds real work.

It does not erase the surrounding framework structure.

### The wrapper shape in code

The code shape confirms the model.

The TLS server is not a completely separate hand-built server type.

It reuses the ordinary IPv4 stream server shell and changes the connection-layer pieces.

In simplified form, the shape is:

```cpp
using SocketServer =
    net::in::stream::SocketServer<
        core::socket::stream::tls::SocketAcceptor,
        net::in::stream::tls::config::ConfigSocketServer,
        SocketContextFactoryT,
        Args...>;
```

The client has the same idea:

```cpp
using SocketClient =
    net::in::stream::SocketClient<
        core::socket::stream::tls::SocketConnector,
        net::in::stream::tls::config::ConfigSocketClient,
        SocketContextFactoryT,
        Args...>;
```

The important parts are:

| Part | Meaning |
|---|---|
| `net::in::stream::SocketServer` / `SocketClient` | existing outer server/client shell |
| TLS `SocketAcceptor` / `SocketConnector` | TLS-aware connection-layer creation |
| TLS config type | configuration extended with TLS settings |
| `SocketContextFactoryT` | same factory pattern as before |
| context type | protocol endpoint, usually unchanged |

This is the architectural payoff.

The outer role remains familiar.

The connection machinery changes.

The protocol endpoint can often remain the same.

### What TLS changes

TLS changes real parts of the communication path.

It adds concerns that do not exist in a plain legacy stream.

The most important ones are:

- certificate chain,
- private key,
- optional key password,
- CA certificate or CA directory,
- peer validation policy,
- SNI-related behavior,
- cipher or protocol policy,
- TLS initialization timeout,
- TLS shutdown timeout,
- handshake success and failure,
- close-notify and shutdown behavior,
- TLS-specific diagnostics.

These are not superficial options.

They are part of secure connection handling.

TLS is therefore not just “turn encryption on.”

It adds identity, trust, handshake, shutdown, and failure behavior to the connection layer.

### What usually stays stable

TLS often leaves the higher-level application structure unchanged.

The following parts usually remain recognizable:

- server/client role,
- instance name,
- configuration hierarchy,
- factory pattern,
- context pattern,
- connection lifecycle vocabulary,
- protocol endpoint logic,
- use of `sendToPeer(...)`,
- use of `readFromPeer(...)`.

This is why TLS is teachable inside the same architecture.

The reader does not need to learn a new framework model.

The reader needs to understand where the secure connection layer fits.

### The TLS connection object as the layer boundary

The TLS connection object is the clearest boundary.

It is still a stream `SocketConnection`.

But it is specialized with TLS-aware machinery:

- TLS reader,
- TLS writer,
- SSL startup,
- SSL handshake,
- SSL shutdown,
- TLS initialization timeout,
- TLS shutdown timeout,
- access to the underlying `SSL*`.

The connection remains the connection.

The reader/writer behavior and internal lifecycle become TLS-aware.

This is the right layer for encryption.

The context can still talk to the peer through the same conceptual operations.

The connection layer handles the secure transport details.

#### `getSSL()` as TLS-specific access

The TLS connection exposes access to the underlying `SSL*`.

That is useful, but it should be understood carefully.

`getSSL()` is an escape hatch at the TLS connection boundary.

It is appropriate when TLS properties genuinely matter.

Examples include:

- certificate inspection,
- auditing,
- peer identity checks,
- TLS-specific diagnostics,
- application behavior that depends on TLS details.

It should not make every ordinary protocol context TLS-dependent by default.

A protocol context should care about TLS only when TLS has protocol meaning.

### TLS configuration and the `tls` section

TLS configuration is added to the existing configuration model.

It does not create a separate configuration universe.

The IPv4 TLS server configuration is built by layering TLS configuration on top of the normal IPv4 stream server configuration.

The IPv4 TLS client configuration follows the same pattern for clients.

Conceptually:

```text
family-specific stream configuration
  + TLS configuration
      -> TLS-enabled stream configuration
```

This matches the section model from Chapters 16 and 17.

A TLS-enabled instance still has the ordinary sections that describe endpoint identity and socket behavior.

It additionally has a `tls` section for secure connection handling.

```text
instance
  -> local
  -> remote
  -> socket
  -> server
  -> connection
  -> tls
```

The `tls` section groups TLS-specific concerns such as:

- certificate chain,
- private key,
- key password,
- CA certificate,
- CA directory,
- cipher or protocol policy,
- SNI behavior,
- peer validation policy,
- initialization timeout,
- shutdown timeout.

This section boundary matters.

Endpoint identity stays in `local` and `remote`.

Socket and retry behavior stay in `socket`.

Server-specific listen behavior stays in `server`.

TLS-specific security and handshake policy belongs in `tls`.

### TLS adds work between connection creation and readiness

TLS changes the connection timeline.

A plain stream connection can often be described simply:

```text
transport connection exists
  -> connection is ready
      -> protocol context works
```

TLS adds handshake work:

```text
transport connection exists
  -> TLS handshake starts
      -> TLS handshake succeeds
          -> secure connection is ready
              -> protocol context works
```

This is why the lifecycle distinction between early connection creation and full readiness matters.

A useful reading is:

| Boundary | Meaning |
|---|---|
| `onConnect` | connection object exists |
| TLS handshake | secure connection setup is in progress |
| `onConnected` | connection is ready for protocol work |
| context `onConnected()` | protocol endpoint can begin its conversation |

TLS does not make the lifecycle impossible to understand.

It makes the middle part more meaningful.

### TLS also affects shutdown

TLS also adds work at the end of a connection.

A legacy stream shutdown may be mostly socket shutdown and close behavior.

A TLS stream may also need TLS shutdown behavior, including close-notify handling.

A useful model is:

```text
protocol wants to close
  -> connection begins shutdown
      -> TLS shutdown / close-notify handling
          -> underlying socket shutdown / close
              -> disconnect summary
```

This matters because failures and timeouts can occur during shutdown as well as during setup.

A TLS-enabled connection therefore has two important TLS-sensitive phases:

```text
startup
  -> handshake

shutdown
  -> TLS shutdown / close-notify
```

Both phases belong to the connection layer.

Both phases are relevant for diagnostics.

### TLS does not erase the lower family

A TLS connection is still carried over a lower communication family.

The lower family does not disappear just because the connection is encrypted.

The application may still need to know whether the carrier beneath TLS is:

- IPv4,
- IPv6,
- Unix domain sockets,
- or another supported lower family with a TLS wrapper.

This affects endpoint configuration, address semantics, deployment shape, and diagnostics.

TLS specializes connection handling above the lower transport.

It does not replace the lower transport.

That is why the earlier lower-family chapters still matter.

### Protocol contexts should stay TLS-independent when possible

A `SocketContext` should usually describe the application protocol.

It should not become TLS-heavy unless TLS has protocol meaning.

For many protocols, the conversation is the same after the secure connection is ready.

The context still needs to:

- react to `onConnected()`,
- read from the peer,
- send to the peer,
- maintain protocol state,
- respond to disconnects.

That means the same protocol endpoint may often work over legacy and TLS streams.

The instance type and configuration decide whether the connection is secure.

The context implements the conversation.

#### When protocol logic should care about TLS

There are also honest cases where higher-level logic should care about TLS.

Examples include:

- protocols whose identity model depends on peer certificates,
- applications that audit TLS properties,
- applications that adapt behavior depending on secure versus insecure transport,
- systems that expose certificate or handshake details to higher layers,
- protocols that bind authorization to TLS peer identity.

In those cases, TLS-specific meaning may rise into protocol logic.

But it should rise deliberately.

Do not make every ordinary context TLS-aware just because the transport is TLS.

### TLS and diagnostics

TLS makes diagnostics more important.

A plain socket failure is already meaningful.

A TLS failure may involve several additional questions:

- Did the lower transport connection exist?
- Did the TLS handshake start?
- Did the handshake succeed?
- Was certificate material present?
- Was the peer trusted?
- Did SNI select the expected context?
- Did initialization timeout?
- Did shutdown timeout?
- Was close-notify received or treated as EOF?

Chapter 18’s visibility model applies directly.

Use configuration display to inspect TLS settings.

Use ordinary logs for lifecycle events.

Use `PLOG` or TLS-specific error reporting where system or library context matters.

Use `VLOG` for handshake, shutdown, certificate, and trust diagnostics that are too detailed for normal output.

Use connection identity and counters to connect TLS events to a concrete peer relationship.

TLS does not require a new diagnostic philosophy.

It makes the existing one more important.

### A useful teaching path: legacy first, TLS second

The clearest way to understand TLS in SNode.C is:

```text
legacy stream first
  -> then TLS stream
```

First understand the legacy application:

- server or client role,
- instance configuration,
- factory,
- context,
- lower-family endpoint,
- connection lifecycle.

Then introduce TLS as a connection-layer upgrade.

This lets the reader see what changed and what stayed stable.

It also avoids presenting TLS as a completely new application architecture.

TLS is easier to understand when the non-TLS shape is already clear.

### A rule of thumb for TLS-capable applications

A useful rule is:

> Write the protocol endpoint as if secure and insecure transport are the same conversation whenever that is honestly true.

Then let:

- the instance type,
- the connection-layer wrapper,
- the TLS configuration,
- and the diagnostics

carry the secure-transport differences.

Only promote TLS details into protocol logic when the protocol semantics require it.

This keeps application code cleaner.

It also keeps the architecture readable.

### What to remember

Remember:

- TLS is a connection-layer specialization.
- TLS changes the connection layer; it does not replace the application architecture.
- The lower communication family still exists beneath TLS.
- TLS changes reader/writer behavior, handshake, shutdown, certificate/trust configuration, and failure modes.
- TLS usually does not change the context/factory pattern.
- Protocol contexts should remain TLS-independent unless TLS has protocol meaning.
- TLS configuration belongs in the `tls` section.
- TLS server/client wrappers preserve the ordinary server/client model.
- `getSSL()` gives TLS-specific access at the connection boundary.
- TLS diagnostics require configuration, lifecycle, connection, and TLS-specific visibility.
- TLS affects both startup and shutdown.
- Chapter 20 continues with timeouts, retries, and failure modes.

### Closing perspective

Chapter 19 showed how secure connection handling fits into the same architecture.

TLS is serious.

It introduces handshake behavior, shutdown behavior, certificate material, trust policy, and new failure modes.

But it remains contained in the connection layer and its configuration.

That balance is the important architectural lesson.

```text
same application shape
  -> TLS-aware connection handling
      -> secure protocol conversation
```

The next chapter continues with communication over time.

It looks at timeouts, retries, and failure modes.
