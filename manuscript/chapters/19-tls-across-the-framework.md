## TLS Across the Framework

\index{TLS}
\index{secure communication}
\index{connection layer}


### From runtime visibility to secure connection handling

TLS is a connection-layer specialization with operational consequences. It does not introduce a second application model; it changes how a secure stream is established, verified, diagnosed, and shut down.

A TLS-enabled SNode.C application still has:

- server/client handles,
- registered runtime-visible server/client instances,
- configuration sections,
- factories,
- contexts,
- connection lifecycle,
- runtime diagnostics.

The connection handling between the lower transport and the application protocol changes.

That distinction matters. TLS is serious: it brings identity material, trust material, handshake behavior, shutdown behavior, close-notify semantics, timeout handling, and TLS-specific diagnostics. But those concerns have a place in the architecture. They belong to secure connection handling and its configuration. They should not be spread randomly through the protocol context merely because encryption is involved.

### TLS as a connection-layer specialization

\index{TLS!connection layer}
\index{connection-layer specialization}


The familiar layered reading path still applies: lower communication family, transport form, connection handling, and application protocol.

TLS belongs in the connection-handling position. It sits above the lower family and transport form. It sits below the application protocol.

That means:

```text
IPv4 stream
  -> legacy connection handling
      -> protocol context

IPv4 stream
  -> TLS connection handling
      -> protocol context
```

The lower family still exists, the registered server/client instance still exists, and the context still implements the protocol conversation. TLS adds secure connection handling between those parts; more generally, a `SocketContext` still sits above the lower family, stream transport, and the selected legacy-or-TLS connection layer.

Where a TLS wrapper exists for a lower family, this pattern applies. The chapter uses IPv4 examples because they are familiar, not because the architectural idea is IPv4-specific. The same connection-layer specialization can be expressed for other lower families where the corresponding TLS stream components are available.

Not every lower family has identical deployment meaning. IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP still have different endpoint identities and operating-system assumptions. The point is that TLS does not erase that lower-family identity. It specializes the stream connection handling above it.


Figure \ref{fig:tls-connection-layer-specialization} shows the intended mental model. TLS is not a different application protocol and not a different lower family. It specializes the stream connection form. The surrounding role, address family, and socket-context structure remain recognizable. The diagram focuses on that specialization point rather than enumerating every TLS-enabled class variant.

![TLS as a connection-layer specialization: the lower family, application protocol, and socket context shape remain stable, while the stream connection is specialized from legacy byte transport to TLS-secured byte transport.](assets/figures/pdf/fig-15-tls-connection-layer-specialization.pdf){#fig:tls-connection-layer-specialization width=90% latex-placement="tbp"}

### Legacy and TLS streams as neighboring connection variants

\index{legacy streams}
\index{TLS streams}
\index{connection variants}


A compact comparison makes the teaching point visible.

| Concern | Legacy stream | TLS stream |
|---|---|---|
| handle | selects a lower-family stream role | selects a lower-family TLS stream role |
| registered instance | same runtime-visible role model | same runtime-visible role model |
| lower family | IPv4, IPv6, Unix domain sockets, Bluetooth, etc. | still present beneath TLS |
| connection machinery | legacy reader/writer | TLS reader/writer |
| setup work | socket/connect/listen | socket/connect/listen plus SSL object setup and TLS handshake |
| shutdown work | socket shutdown/close | socket shutdown/close plus TLS shutdown and close-notify handling |
| configuration | `local` / `remote` / `socket` / `server` / `connection` | ordinary sections plus `tls` |
| context behavior | protocol endpoint | often unchanged after secure readiness |
| diagnostics | lifecycle, counters, errors | lifecycle, counters, errors plus TLS-specific handshake, trust, and shutdown diagnostics |

This table is the chapter in miniature: TLS adds real work without erasing the surrounding framework structure.

That is why TLS is easiest to understand after the legacy stream shape is already clear. The legacy stream shows the connection model without secure transport. The TLS stream then shows which parts are added by secure connection handling.

### The TLS wrapper shape in code

\index{TLS wrapper}
\index{TLS connection}


The code shape confirms the model. The TLS server is not a completely separate hand-built server type. It reuses the ordinary IPv4 stream server shell and changes the connection-layer pieces.

In simplified form, the shape is:

```cpp
using SocketServer =
    net::in::stream::SocketServer<core::socket::stream::tls::SocketAcceptor,
                                  net::in::stream::tls::config::ConfigSocketServer,
                                  SocketContextFactoryT,
                                  Args...>;
```

The client has the same idea:

```cpp
using SocketClient =
    net::in::stream::SocketClient<core::socket::stream::tls::SocketConnector,
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

This is the architectural payoff: the handle/instance model remains recognizable, the connection machinery changes, and the protocol endpoint can often remain stable.

### What TLS adds to the connection layer

\index{TLS!handshake}
\index{TLS!certificate handling}
\index{TLS!shutdown}


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

That is why the `tls` configuration section exists. The section gives secure connection handling its configuration; it is not decorative.

### What can remain stable above TLS

\index{TLS!protocol independence}
\index{SocketContext@\texttt{SocketContext}}


TLS often leaves the higher-level application structure recognizable.

The following parts can often remain stable:

- handle usage shape,
- registered instance naming,
- configuration hierarchy,
- factory pattern,
- context pattern,
- connection lifecycle vocabulary,
- protocol endpoint logic,
- use of `sendToPeer(...)`,
- use of `readFromPeer(...)`.

Therefore, TLS is teachable inside the same architecture. The reader does not need to learn a new framework model. The reader needs to understand where the secure connection layer fits.

The word *often* matters. TLS independence is a design result, not a universal law: it holds when the protocol conversation after secure connection readiness is the same. If the protocol uses peer certificates, secure-transport properties, or SNI-derived policy as part of its own semantics, then TLS meaning may deliberately rise into the protocol layer.

### The TLS connection object as the layer boundary

\index{TLS!layer boundary}
\index{getSSL()@\texttt{getSSL()}}


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

The TLS connection exposes access to the underlying `SSL*`, but that access should be understood carefully.

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

\index{TLS!configuration}
\index{tls section}
\index{SNI}


TLS configuration is added to the existing configuration model. It does not create a separate configuration universe.

For both IPv4 server and client roles, TLS configuration is layered onto the corresponding stream configuration.

Conceptually:

```text
family-specific stream configuration
  + TLS configuration
      -> TLS-enabled stream configuration
```

This matches the section model from Chapters 16 and 17.

A TLS-enabled instance still has the ordinary sections that describe endpoint identity, socket behavior, connection behavior, and server/client role behavior.

It additionally has a `tls` section for secure connection handling.

The instance-level configuration keeps several scopes visible: `local`, `remote`, `socket`, server/client-specific sections, `connection`, and `tls`.

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

SNI is therefore part of TLS identity selection during handshake, not just another string option.

#### Trust, expected identity, and SNI are separate decisions

The current source requires care at this point. `ssl_utils.cpp` enables peer verification when trust material or default trust paths are selected and accepting unknown certificates is disabled. With no selected trust source, its verification mode is zero. Selecting a TLS wrapper without a trust policy leaves peer authentication unresolved.

SNI is a second decision. `ssl_set_sni(...)` sets the name sent to the server; it does not configure the expected certificate identity. The example hostname-checking statements in `src/apps/echo/model/clients.h` are commented out. Reading those statements as active behavior would give the example a security property it does not currently have.

For a TLS client, choose the trust source and expected peer identity before the handshake. The existing `setOnConnect(...)` callback runs after the TLS configuration has created its `SSL_CTX`, but before the connector calls `startSSL(...)` for this connection. At this boundary, `getSSL()` is still null. Configure the shared client context's verification parameters before the new `SSL` object copies them. This is endpoint policy: clients that need different expected identities should use separate endpoint configurations. The following is an application-policy sketch for a DNS identity, to be attached to an already declared TLS client:

```cpp
client.getConfig()->setCaCert("local-ca.pem");
client.getConfig()->setCaCertAcceptUnknown(false);
client.setOnConnect([](auto* connection) {
    SSL_CTX* context = connection->getConfig()->getSslCtx();
    X509_VERIFY_PARAM* parameters = SSL_CTX_get0_param(context);
    X509_VERIFY_PARAM_set_hostflags(parameters, X509_CHECK_FLAG_NO_PARTIAL_WILDCARDS);
    if (X509_VERIFY_PARAM_set1_host(parameters, "sensor.example", 0) != 1) {
        connection->close();
    }
});
```

The sketch requires `<openssl/ssl.h>` and `<openssl/x509v3.h>`, a real trust file in place of `local-ca.pem`, and rejection of unknown certificates. `sensor.example` stands for the application's expected DNS identity; it is not a runnable public service. A literal IP identity needs the corresponding IP verification parameter, not a DNS-name substitution. This policy belongs before secure readiness, not in a protocol callback that runs after application data has already become possible.

Check the policy through three outcomes: the intended identity under the intended trust source succeeds, an untrusted issuer fails, and a trusted certificate for the wrong identity also fails. Those outcomes distinguish trust, identity, and encryption. They must be established for the deployment; compiling this callback alone does not establish them.

The edition includes a small verification fixture for this policy in `review/verification/refinement-probes`. From the book directory, with the Chapter 2 installation available, the local exercise is:

```sh
cmake -S review/verification/refinement-probes -B build/refinement-probes \
  -DCMAKE_PREFIX_PATH="$HOME/.local/snodec"
cmake --build build/refinement-probes
ctest --test-dir build/refinement-probes -R TlsTrustAndIdentity \
  --output-on-failure --no-tests=error
```

The fixture creates temporary self-signed test identities and uses an independent local TLS peer. It observes readiness for a trusted matching name, rejection of a trusted wrong name, and rejection of an untrusted matching name. It also checks that the early callback sees no connection `SSL*` yet. The identities are local test material and are removed afterward. Production certificate provisioning and application authorization remain deployment decisions.

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

Therefore, the lifecycle distinction between early connection creation and full readiness matters.

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

Failures and timeouts can occur during shutdown as well as during setup.

A TLS-enabled connection therefore has two important TLS-sensitive phases:

```text
startup
  -> handshake

shutdown
  -> TLS shutdown / close-notify
```

Both phases belong to the connection layer. Both phases are relevant for diagnostics.

Close-notify belongs to correct TLS connection shutdown rather than to the application message stream. A missing or unexpected close-notify can therefore be a connection-layer diagnostic fact even when the application protocol itself has already decided to close.

This is one reason TLS diagnostics belong together with connection lifecycle visibility.

### Graceful shutdown includes the TLS peer

\index{TLS!shutdown}
\index{close\_notify@\texttt{close\_notify}}

A TLS stream does not finish its lifecycle merely because the application stops producing plaintext. The TLS shutdown path has to preserve the protocol's `close_notify` exchange, readiness progress, and failure/timeout behavior.

During framework shutdown, the connection joins its existing bounded write-shutdown path. If a TLS shutdown helper is already active, the notification joins that operation rather than creating another helper or restarting it. Reader and writer subobjects may both encounter the notification, but the operation must remain idempotent.

Read observation can remain necessary while the connection waits for peer shutdown progress. Disabling it solely because the runtime entered `STOPPING` would prevent the cleanup from completing. A forced termination path still bounds a peer that never cooperates.

Handshake failure, established-stream shutdown, and an already active shutdown helper are different lifecycle situations. The TLS implementation coordinates their ownership; application contexts should not duplicate that state machine. The existing signal callback is still notified for signal-triggered shutdown, but returning `false` cannot veto framework transport cleanup.

These are concrete regression surfaces in the current test suite, including TLS result classification, helper ownership, state-machine behavior, and framework shutdown scenarios. They do not replace deployment checks for certificates, trust, names, or application authorization.

### TLS does not erase the lower family

A TLS connection is still carried over a lower family. The lower family does not disappear just because the connection is encrypted.

For a Unix-domain carrier, pathname permissions still determine who can reach the socket, while TLS peer verification answers a separate identity question. For a Bluetooth carrier, discovery, service endpoint selection, and any pairing required by the platform’s security policy still precede the secure conversation. An encrypted stream cannot repair a wrong PSM, an inaccessible pathname, or a missing route.

The IPv4 examples make the TLS boundary visible without adding those setup requirements. Transferring the protocol to another supported carrier preserves the trust and identity decisions while adding that carrier’s own reachability and operating-system checks.

### Protocol contexts should stay TLS-independent when possible

A `SocketContext` should usually describe the application protocol. It should not become TLS-heavy unless TLS has protocol meaning. For many protocols, the conversation is the same after the secure connection is ready.

The context still needs to:

- react to `onConnected()`,
- read from the peer,
- send to the peer,
- maintain protocol state,
- respond to disconnects.

That means the same protocol endpoint may often work over legacy and TLS streams.

The handle type, registered instance, connection-layer wrapper, and TLS configuration decide whether the connection is secure.

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

\index{TLS!diagnostics}


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

Use configuration display to inspect TLS settings. Use semantic lifecycle records to distinguish attempts, transport readiness, and protocol attachment. Preserve the explicit system or TLS error from the failing boundary rather than substituting an unrelated later `errno`.

Use scoped debug or trace policy for detailed handshake and shutdown investigation. Connection identity connects those records to a concrete peer episode. Certificate and trust diagnostics should remain useful without exposing private key material or unnecessary sensitive values. TLS uses the same semantic diagnostic model as the rest of the framework.

Correlate the failed TLS episode with its connection identity before interpreting later retry records as a second failure of the same handshake.

### A useful teaching path: legacy first, TLS second

The clearest way to understand TLS in SNode.C is still to read the legacy stream first, then the TLS stream.

Take the Chapter 15 transfer exercise and first establish its greeting, framing, and shutdown behavior over the legacy connection. When introducing TLS, retain those observations and add separate checks for trusted identity, mismatched identity, and handshake failure. A successful encrypted exchange alone does not distinguish those cases.

There is also a deployment choice. In-process TLS keeps the peer’s TLS connection and its policy at the application boundary, but makes that process responsible for certificate and key configuration. A terminating proxy can centralize that operation; the application then receives a different connection and needs an explicit trust policy for any forwarded identity. The protocol parser may remain reusable in both arrangements, while the authorization boundary changes.

### A rule of thumb for TLS-capable applications

A useful rule is:

::: {.snodec-rule title="Protocol continuity rule"}
Write the protocol endpoint as if secure and insecure transport are the same conversation whenever that is actually true.
:::

Then let:

- the handle type,
- the registered instance and its configuration,
- the connection-layer wrapper,
- the `tls` section,
- and the diagnostics

carry the secure-transport differences. Only promote TLS details into protocol logic when the protocol semantics require it. This keeps application code cleaner.

It also keeps the architecture readable.

### TLS capability and deployment responsibility

\index{TLS!deployment responsibility}


TLS-capable components make secure connection handling possible; they do not by themselves complete a secure deployment. Certificate files, private-key permissions, trust anchors, SNI policy, and diagnostics still belong to the deployed role and its configuration.

That distinction will matter again in the deployment chapters. A binary may be linked with TLS support and still fail as a secure service if the surrounding filesystem, permissions, and trust material are wrong. TLS-capable linking is not the same as TLS deployment.

::: {.snodec-remember title="What to remember"}
- TLS is a connection-layer specialization, not a second application architecture.
- The lower family and transport form remain present beneath TLS.
- TLS changes reader/writer behavior, SSL object setup, handshake, shutdown, close-notify handling, certificate/trust configuration, and diagnostics.
- The handle and registered instance model remain recognizable; the TLS wrapper changes the connection-layer machinery.
- A `SocketContext` can often remain TLS-independent when the protocol conversation is the same after secure connection setup.
- TLS-specific meaning should enter protocol logic only when certificate, trust, SNI, or secure-transport properties are part of the protocol semantics.
:::
