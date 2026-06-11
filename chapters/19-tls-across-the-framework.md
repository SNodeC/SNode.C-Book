## TLS Across the Framework

### From runtime visibility to secure connection handling

Chapter 18 closed the operational visibility part of the book. It treated configuration, generated command lines, logging, connection identity, counters, durations, and protocol decisions as diagnostic evidence.

Chapter 19 begins the next part by adding secure connection handling to the same architecture.

Security and robustness do not remove the SNode.C model. They add stricter connection-layer responsibilities, more timing-sensitive transitions, and more failure states.

TLS does not introduce a second application model. It changes the connection layer.

That is the central idea of this chapter:

> TLS changes the connection layer; it does not replace the application architecture.

A TLS-enabled SNode.C application still has:

- application-side server/client handles,
- registered runtime-visible server/client instances,
- configuration sections,
- factories,
- contexts,
- connection lifecycle,
- runtime diagnostics.

What changes is the connection handling between the lower transport and the application protocol.

That distinction matters. TLS is serious: it brings identity material, trust material, handshake behavior, shutdown behavior, close-notify semantics, timeout handling, and TLS-specific diagnostics. But those concerns have a place in the architecture. They belong to secure connection handling and its configuration. They should not be spread randomly through the protocol context merely because encryption is involved.

### TLS as a connection-layer specialization

The layered model is:

```text
lower communication family
  -> transport form
      -> connection handling
          -> application protocol
```

TLS belongs in the connection-handling position. It sits above the lower communication family and transport form. It sits below the application protocol.

That means:

```text
IPv4 stream
  -> legacy connection handling
      -> protocol context

IPv4 stream
  -> TLS connection handling
      -> protocol context
```

The lower family still exists. The registered server/client instance still exists. The context still implements the protocol conversation.

TLS adds secure connection handling between those parts.

A more general view is:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection layer
          -> SocketContext
```

Where a TLS wrapper exists for a lower family, this pattern applies. The chapter uses IPv4 examples because they are familiar, not because the architectural idea is IPv4-specific. The same connection-layer specialization can be expressed for other lower communication families where the corresponding TLS stream components are available.

The important point is not that every lower family has identical deployment meaning. IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP still have different endpoint identities and operating-system assumptions. The point is that TLS does not erase that lower-family identity. It specializes the stream connection handling above it.

### Legacy and TLS streams as neighboring connection variants

A compact comparison makes the teaching point visible.

| Concern | Legacy stream | TLS stream |
|---|---|---|
| application-side handle | selects a lower-family stream role | selects a lower-family TLS stream role |
| registered instance | same runtime-visible role model | same runtime-visible role model |
| lower family | IPv4, IPv6, Unix domain sockets, Bluetooth, etc. | still present beneath TLS |
| connection machinery | legacy reader/writer | TLS reader/writer |
| setup work | socket/connect/listen | socket/connect/listen plus SSL object setup and TLS handshake |
| shutdown work | socket shutdown/close | socket shutdown/close plus TLS shutdown and close-notify handling |
| configuration | `local` / `remote` / `socket` / `server` / `connection` | ordinary sections plus `tls` |
| context behavior | protocol endpoint | often unchanged after secure readiness |
| diagnostics | lifecycle, counters, errors | lifecycle, counters, errors plus TLS-specific handshake, trust, and shutdown diagnostics |

This table is the chapter in miniature. TLS adds real work. It does not erase the surrounding framework structure.

That is why TLS is easiest to understand after the legacy stream shape is already clear. The legacy stream shows the connection model without secure transport. The TLS stream then shows which parts are added by secure connection handling.

### The TLS wrapper shape in code

The code shape confirms the model. The TLS server is not a completely separate hand-built server type. It reuses the ordinary IPv4 stream server shell and changes the connection-layer pieces.

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
| `net::in::stream::SocketServer` / `SocketClient` | existing lower-family stream server/client shell |
| TLS `SocketAcceptor` / `SocketConnector` | TLS-aware connection-layer creation |
| TLS config type | ordinary stream configuration extended with TLS settings |
| `SocketContextFactoryT` | the factory construction pattern from Chapter 14 |
| context type | the per-connection protocol endpoint from Chapter 13 |

The application still selects a concrete server/client handle type. That type registers a server-side or client-side instance as before. The TLS specialization changes the acceptor or connector, the reader/writer behavior, and the configuration type used beneath that handle.

This is the architectural payoff. The handle/instance model remains recognizable. The connection machinery changes.

The protocol endpoint can often remain stable.

### What TLS adds to the connection layer

TLS changes real parts of the communication path. It adds concerns that do not exist in a plain legacy stream.

The most important groups are:

| TLS concern | Architectural meaning |
|---|---|
| identity material | certificate chain, private key, optional key password |
| trust material | CA certificate, CA directory, default CA directory use, accepting unknown certificates |
| policy | cipher list, SSL/TLS options, peer validation choices |
| SNI behavior | client-side SNI, server-side SNI certificate selection, optional forced SNI |
| timing | TLS initialization timeout and TLS shutdown timeout |
| shutdown semantics | close-notify handling and unexpected EOF behavior |
| diagnostics | handshake, trust, timeout, shutdown, and TLS-library error visibility |

These are not superficial options. They are part of secure connection handling. TLS is therefore not just “turn encryption on.”

It adds identity, trust, handshake timing, shutdown semantics, and new diagnostic surfaces to the connection layer.

That is why the `tls` configuration section exists. The section is not decorative. It is the place where secure connection handling receives its configuration.

### What can remain stable above TLS

TLS often leaves the higher-level application structure recognizable.

The following parts can often remain stable:

- application-side handle usage shape,
- registered instance naming,
- configuration hierarchy,
- factory pattern,
- context pattern,
- connection lifecycle vocabulary,
- protocol endpoint logic,
- use of `sendToPeer(...)`,
- use of `readFromPeer(...)`.

This is why TLS is teachable inside the same architecture. The reader does not need to learn a new framework model. The reader needs to understand where the secure connection layer fits.

The word *often* matters. TLS independence is not a universal law. It is a design result that holds when the protocol conversation after secure connection readiness is the same. If the protocol uses peer certificates, secure-transport properties, or SNI-derived policy as part of its own semantics, then TLS meaning may deliberately rise into the protocol layer.

### The TLS connection object as the layer boundary

The TLS connection object is the clearest boundary.

It is still a stream `SocketConnection`.

But it is specialized with TLS-aware machinery:

- TLS reader,
- TLS writer,
- SSL object setup,
- SSL handshake,
- SSL shutdown,
- TLS initialization timeout,
- TLS shutdown timeout,
- close-notify handling,
- access to the underlying `SSL*`.

The connection remains the connection. The reader/writer behavior and internal lifecycle become TLS-aware. This is the right layer for encryption.

The context can still talk to the peer through the same conceptual operations. It sends data, reads data, reacts to connection readiness, and maintains protocol state. The connection layer handles the secure transport details that make that communication confidential, integrity-protected, and identity-aware.

#### `getSSL()` as TLS-specific access

The TLS connection exposes access to the underlying `SSL*`. That is useful, but it should be understood carefully.

`getSSL()` is not the normal protocol interface.

It is TLS-specific access at the connection boundary. It is appropriate when TLS properties genuinely matter.

Examples include:

- certificate inspection,
- auditing,
- peer identity checks,
- TLS-specific diagnostics,
- application behavior that depends on TLS details.

It should not make every ordinary protocol context TLS-dependent by default. A protocol context should care about TLS only when TLS has protocol meaning.

### TLS configuration and the `tls` section

TLS configuration is added to the existing configuration model. It does not create a separate configuration universe.

The IPv4 TLS server configuration is built by layering TLS configuration on top of the normal IPv4 stream server configuration.

The IPv4 TLS client configuration follows the same pattern for clients.

Conceptually:

```text
family-specific stream configuration
  + TLS configuration
      -> TLS-enabled stream configuration
```

This matches the section model from Chapters 16 and 17.

A TLS-enabled instance still has the ordinary sections that describe endpoint identity, socket behavior, connection behavior, and server/client role behavior.

It additionally has a `tls` section for secure connection handling.

```text
instance
  -> local
  -> remote
  -> socket
  -> server/client-specific sections
  -> connection
  -> tls
```

The `tls` section groups TLS-specific responsibilities:

| Responsibility | Representative settings |
|---|---|
| certificate identity | certificate chain, private key, key password |
| trust material | CA certificate, CA directory, default CA directory use |
| trust policy | accepting or rejecting unknown certificates |
| protocol/cipher policy | cipher list and SSL/TLS options |
| timing | initialization timeout and shutdown timeout |
| shutdown behavior | close-notify / EOF handling |
| SNI behavior | client-side SNI and server-side SNI certificate selection |

This section boundary matters.

Endpoint identity stays in `local` and `remote`.

Socket and retry behavior stay in `socket`.

Server-specific listen behavior stays in server-side sections. TLS-specific security, handshake, trust, and shutdown policy belong in `tls`.

#### Client-side and server-side SNI

SNI appears on both sides of the TLS relationship, but with different meanings.

On the client side, SNI is a name sent during TLS setup so the peer can select an appropriate TLS identity.

On the server side, SNI is used to select certificate material for the requested name. A server-side configuration may also require SNI instead of silently falling back to a master certificate.

That distinction keeps the direction visible:

```text
client side
  -> send SNI

server side
  -> select SNI certificate
  -> optionally require SNI
```

SNI is therefore not just another string option. It is part of TLS identity selection during handshake.

### TLS adds work between connection creation and readiness

TLS changes the connection timeline.

A plain stream connection can often be described simply:

```text
transport connection exists
  -> connection is ready
      -> protocol context works
```

TLS adds SSL setup and handshake work:

```text
transport connection exists
  -> SSL object is created and configured
      -> TLS handshake starts
          -> TLS handshake succeeds
              -> secure connection is ready
                  -> protocol context is attached
                      -> protocol context works
```

This is why the lifecycle distinction between early connection creation and full readiness matters.

A useful reading is:

| Boundary | Meaning |
|---|---|
| `onConnect` | connection object exists and TLS setup can begin |
| TLS handshake | secure connection setup is in progress |
| `onConnected` | connection is ready for protocol work |
| context `onConnected()` | protocol endpoint can begin its conversation |

TLS does not make the lifecycle impossible to understand. It makes the middle part more meaningful.

The architecture remains legible because there is still a boundary between transport connection existence, TLS readiness, and protocol-context behavior.

### TLS also affects shutdown

TLS also adds work at the end of a connection. A legacy stream shutdown may be mostly socket shutdown and close behavior. A TLS stream may also need TLS shutdown behavior, including close-notify handling.

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

Both phases belong to the connection layer. Both phases are relevant for diagnostics.

Close-notify is not an application message. It is part of the TLS connection ending correctly. A missing or unexpected close-notify can therefore be a connection-layer diagnostic fact even when the application protocol itself has already decided to close.

This is one reason TLS diagnostics belong together with connection lifecycle visibility.

### TLS does not erase the lower family

A TLS connection is still carried over a lower communication family. The lower family does not disappear just because the connection is encrypted.

The application may still need to know whether the carrier beneath TLS is:

- IPv4,
- IPv6,
- Unix domain sockets,
- Bluetooth RFCOMM,
- Bluetooth L2CAP,
- or another supported lower family with a TLS wrapper.

This affects endpoint configuration, address semantics, deployment shape, permissions, pairing/trust setup for Bluetooth carriers, local path behavior for Unix-domain sockets, and diagnostics.

TLS specializes connection handling above the lower transport. It does not replace the lower transport. That is why the earlier lower-family chapters still matter.

The chapter uses IPv4 code shapes because they are compact and familiar. The architectural idea is broader: lower family first, stream transport next, legacy or TLS connection handling above that, and protocol behavior in the context.

### Protocol contexts should stay TLS-independent when possible

A `SocketContext` should usually describe the application protocol. It should not become TLS-heavy unless TLS has protocol meaning. For many protocols, the conversation is the same after the secure connection is ready.

The context still needs to:

- react to `onConnected()`,
- read from the peer,
- send to the peer,
- maintain protocol state,
- respond to disconnects.

That means the same protocol endpoint may often work over legacy and TLS streams.

The application-side handle type, registered instance, connection-layer wrapper, and TLS configuration decide whether the connection is secure.

The context implements the conversation. A context can stay TLS-independent when the protocol conversation after connection readiness is the same.

#### When protocol logic should care about TLS

There are also honest cases where higher-level logic should care about TLS.

Examples include:

- protocols whose identity model depends on peer certificates,
- mTLS-style authorization,
- applications that audit TLS properties,
- applications that adapt behavior depending on secure versus insecure transport,
- systems that expose certificate or handshake details to higher layers,
- protocols that bind authorization to TLS peer identity,
- SNI-derived behavior that is part of application policy.

In those cases, TLS-specific meaning may rise into protocol logic. But it should rise deliberately. Do not make every ordinary context TLS-aware just because the transport is TLS.

### TLS diagnostics through the Chapter 18 lens

TLS makes diagnostics more important. A plain socket failure is already meaningful.

A TLS failure may involve several additional questions:

- Did the lower transport connection exist?
- Was the SSL object created?
- Did the TLS handshake start?
- Did the handshake succeed?
- Was certificate material present?
- Was the peer trusted?
- Did the client send the expected SNI?
- Did the server select the expected SNI certificate?
- Did initialization timeout?
- Did shutdown timeout?
- Was close-notify received or treated as EOF?

Chapter 18’s diagnostic map applies directly.

| Visibility source | TLS question |
|---|---|
| configuration visibility | Which certificate, key, CA, SNI, timeout, and trust settings were configured? |
| log visibility | Which handshake, shutdown, trust, or timeout events occurred? |
| connection visibility | Which concrete connection, peer, address, duration, and counters were involved? |
| protocol visibility | Did TLS meaning affect protocol authorization or behavior? |

Use configuration display to inspect TLS settings. Use ordinary logs for lifecycle events. Use `PLOG` or TLS-specific error reporting where system, OpenSSL, or library context matters.

Use `VLOG` for handshake, shutdown, certificate, and trust diagnostics that are too detailed for normal output. Use connection identity and counters to connect TLS events to a concrete peer relationship. TLS does not require a new diagnostic philosophy.

It makes the existing one more important.

### A useful teaching path: legacy first, TLS second

The clearest way to understand TLS in SNode.C is:

```text
legacy stream first
  -> then TLS stream
```

First understand the legacy application:

- application-side server/client handle,
- registered instance,
- instance configuration,
- factory,
- context,
- lower-family endpoint,
- connection lifecycle.

Then introduce TLS as a connection-layer upgrade. This lets the reader see what changed and what remained stable. It also avoids presenting TLS as a completely new application architecture.

TLS is easier to understand when the non-TLS shape is already clear because the architecture itself shows where the additional secure-connection work is inserted.

### A rule of thumb for TLS-capable applications

A useful rule is:

> Write the protocol endpoint as if secure and insecure transport are the same conversation whenever that is honestly true.

Then let:

- the application-side handle type,
- the registered instance and its configuration,
- the connection-layer wrapper,
- the `tls` section,
- and the diagnostics

carry the secure-transport differences. Only promote TLS details into protocol logic when the protocol semantics require it. This keeps application code cleaner.

It also keeps the architecture readable.

### TLS capability and deployment responsibility

TLS-capable components make secure connection handling possible; they do not by themselves complete a secure deployment. Certificate files, private-key permissions, trust anchors, SNI policy, and diagnostics still belong to the deployed role and its configuration.

That distinction will matter again in the deployment chapters. A binary may be linked with TLS support and still fail as a secure service if the surrounding filesystem, permissions, and trust material are wrong. TLS-capable linking is not the same as TLS deployment.

### What to remember

- TLS is a connection-layer specialization, not a second application architecture.
- The lower communication family and transport form remain present beneath TLS.
- TLS changes reader/writer behavior, SSL object setup, handshake, shutdown, close-notify handling, certificate/trust configuration, and diagnostics.
- The application-side handle and registered instance model remain recognizable; the TLS wrapper changes the connection-layer machinery.
- A `SocketContext` can often remain TLS-independent when the protocol conversation is the same after secure connection setup.
- TLS-specific meaning should enter protocol logic only when certificate, trust, SNI, or secure-transport properties are part of the protocol semantics.
- TLS configuration belongs in the `tls` section, not in endpoint identity, socket retry, or protocol-context code.
- `getSSL()` is TLS-specific access at the connection boundary.
- Chapter 20 continues with timeouts, retries, and failure modes.

### Closing perspective

Chapter 19 showed how secure connection handling fits into the same architecture. TLS is serious.

It introduces handshake behavior, shutdown behavior, certificate material, trust policy, SNI behavior, close-notify semantics, and new failure modes.

But it remains contained in the connection layer and its configuration unless higher protocol semantics deliberately make TLS properties meaningful.

That balance is the important architectural lesson.

```text
recognizable application shape
  -> TLS-aware connection handling
      -> secure protocol conversation
```

TLS has already shown that a connection may fail before readiness, during readiness, during shutdown, or while reporting peer trust.

The next chapter generalizes this view into timeouts, retries, and failure modes across the framework.
