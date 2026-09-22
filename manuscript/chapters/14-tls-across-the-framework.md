## TLS Across the Framework {#tls-across-the-framework}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain which responsibilities TLS changes and which remain with the carrier and protocol.
- **O2.** Distinguish trust, expected peer identity and SNI when diagnosing a secure connection.
- **O3.** Decide where to apply handshake, shutdown and deployment policy.
:::

\index{TLS}
\index{secure communication}
\index{connection layer}

TLS is a connection-layer specialization with operational consequences. It does not introduce a second application model; it changes how a secure stream is established, verified, diagnosed, and shut down.

Identity, trust, handshake timing and close-notify belong to secure connection handling and its configuration. They should not spread through the protocol context merely because encryption is involved.

### TLS as a connection-layer specialization

\index{TLS!connection layer}
\index{connection-layer specialization}

TLS sits above the lower family and stream transport and below the application protocol. The registered instance still owns the role, and its factory still creates the protocol context.

Where a TLS wrapper exists for a lower family, this pattern applies. The chapter uses IPv4 examples because they are familiar, not because the architectural idea is IPv4-specific. The same connection-layer specialization can be expressed for other lower families where the corresponding TLS stream components are available.

Not every lower family has identical deployment meaning. IPv4, IPv6, Unix domain sockets, RFCOMM, and L2CAP still have different endpoint identities and operating-system assumptions. The point is that TLS does not erase that lower-family identity. It specializes the stream connection handling above it.

Figure \ref{fig:tls-connection-layer-specialization} locates this specialization without enumerating every TLS-enabled class variant.

![TLS as a connection-layer specialization: the lower family, application protocol, and socket context shape remain stable, while the stream connection is specialized from legacy byte transport to TLS-secured byte transport.](assets/figures/pdf/fig-15-tls-connection-layer-specialization.pdf){#fig:tls-connection-layer-specialization width=90% latex-placement="tbp"}

\index{legacy streams}
\index{TLS streams}
\index{connection variants}

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
| `SocketContextFactoryT` | the factory construction pattern from Chapter 10 |
| context type | the per-connection protocol endpoint from Chapter 9 |

The application still selects a concrete server/client handle type. That type registers a server-side or client-side instance as before. The TLS specialization changes the acceptor or connector, the reader/writer behavior, and the configuration type used beneath that handle.

\index{TLS!handshake}
\index{TLS!certificate handling}
\index{TLS!shutdown}
\index{TLS!protocol independence}
\index{SocketContext@\texttt{SocketContext}}

A context can often remain unchanged. TLS independence is a design result, not a universal law: it holds when the protocol conversation after secure connection readiness is the same. If the protocol uses peer certificates, secure-transport properties, or SNI-derived policy as part of its own semantics, then TLS meaning may deliberately rise into the protocol layer.

\index{TLS!layer boundary}
\index{getSSL()@\texttt{getSSL()}}

The TLS connection remains a stream `SocketConnection`, with TLS-aware readers/writers and access to its underlying `SSL*` through `getSSL()`. Use that access for certificate inspection, auditing, peer identity checks or TLS diagnostics when those properties matter to the application. It is not the ordinary protocol interface and should not make every context TLS-dependent.

### TLS configuration and the `tls` section

\index{TLS!configuration}
\index{tls section}
\index{SNI}

The `tls` section extends the instance hierarchy from Chapter 12. Endpoint identity remains in `local`/`remote`, retry and socket behavior in `socket`, and listen behavior in server-specific configuration. Secure setup and shutdown have their own settings:

| Responsibility | Representative settings |
|---|---|
| certificate identity | certificate chain, private key, key password |
| trust material | CA certificate, CA directory, default CA directory use |
| trust policy | accepting or rejecting unknown certificates |
| protocol/cipher policy | cipher list and SSL/TLS options |
| timing | initialization timeout and shutdown timeout |
| shutdown behavior | close-notify / EOF handling |
| SNI behavior | client-side SNI and server-side SNI certificate selection |

SNI appears on both sides of the TLS relationship, but with different meanings.

On the client side, SNI is a name sent during TLS setup so the peer can select an appropriate TLS identity.

On the server side, SNI is used to select certificate material for the requested name. A server-side configuration may also require SNI instead of silently falling back to a master certificate.

SNI selects identity material during handshake; selecting the expected peer identity for verification is a separate decision.

### Trust, expected identity, and SNI are separate decisions

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

TLS inserts SSL object creation, configuration and handshake between transport connection establishment and secure readiness. Only after that does the protocol context attach and begin work.

| Boundary | Meaning |
|---|---|
| `onConnect` | connection object exists and TLS setup can begin |
| TLS handshake | secure connection setup is in progress |
| `onConnected` | connection is ready for protocol work |
| context `onConnected()` | protocol endpoint can begin its conversation |

A handshake can fail after transport establishment. Shutdown likewise adds close-notify work before the underlying socket closes; setup and shutdown can each fail or time out. A missing or unexpected close-notify is a connection-layer diagnostic, even when the application has decided to close.

### Graceful shutdown includes the TLS peer

\index{TLS!shutdown}
\index{close\_notify@\texttt{close\_notify}}

A TLS stream does not finish its lifecycle merely because the application stops producing plaintext. The TLS shutdown path has to preserve the protocol's `close_notify` exchange, readiness progress, and failure/timeout behavior.

During framework shutdown, the connection joins its existing bounded write-shutdown path. If a TLS shutdown helper is already active, the notification joins that operation rather than creating another helper or restarting it. Reader and writer subobjects may both encounter the notification, but the operation must remain idempotent.

Read observation can remain necessary while the connection waits for peer shutdown progress. Disabling it solely because the runtime entered `STOPPING` would prevent the cleanup from completing. A forced termination path still bounds a peer that never cooperates.

Handshake failure, established-stream shutdown, and an already active shutdown helper are different lifecycle situations. The TLS implementation coordinates their ownership; application contexts should not duplicate that state machine. The existing signal callback is still notified for signal-triggered shutdown, but returning `false` cannot veto framework transport cleanup.

These lifecycle cases require separate observations; none replaces deployment checks for trust, names or application authorization.

### Carrier and protocol decisions

For a Unix-domain carrier, pathname permissions still determine who can reach the socket, while TLS peer verification answers a separate identity question. For a Bluetooth carrier, discovery, service endpoint selection, and any pairing required by the platform’s security policy still precede the secure conversation. An encrypted stream cannot repair a wrong PSM, an inaccessible pathname, or a missing route.

The IPv4 examples make the TLS boundary visible without adding those setup requirements. Transferring the protocol to another supported carrier preserves the trust and identity decisions while adding that carrier’s own reachability and operating-system checks.

A context can retain its readiness, read/send and state-handling logic when the secure and insecure conversations agree. TLS details enter protocol logic deliberately when they have application meaning.

Examples include:

- protocols whose identity model depends on peer certificates,
- mTLS-style authorization,
- applications that audit TLS properties,
- applications that adapt behavior depending on secure versus insecure transport,
- systems that expose certificate or handshake details to higher layers,
- protocols that bind authorization to TLS peer identity,
- SNI-derived behavior that is part of application policy.

### TLS diagnostics through the Chapter 13 lens

\index{TLS!diagnostics}

Locate a TLS failure along its lifecycle: transport establishment, SSL object creation, handshake, certificate/trust/name checks, readiness or shutdown. Check whether initialization or shutdown timed out and how close-notify or EOF was classified. Chapter 13’s diagnostic map applies:

| Visibility source | TLS question |
|---|---|
| configuration visibility | Which certificate, key, CA, SNI, timeout, and trust settings were configured? |
| log visibility | Which handshake, shutdown, trust, or timeout events occurred? |
| connection visibility | Which concrete connection, peer, address, duration, and counters were involved? |
| protocol visibility | Did TLS meaning affect protocol authorization or behavior? |

Use configuration display to inspect TLS settings. Use semantic lifecycle records to distinguish attempts, transport readiness, and protocol attachment. Preserve the explicit system or TLS error from the failing boundary rather than substituting an unrelated later `errno`.

Use scoped debug or trace policy for detailed handshake and shutdown investigation. Connection identity connects those records to a concrete peer episode. Certificate and trust diagnostics should remain useful without exposing private key material or unnecessary sensitive values. TLS uses the same semantic diagnostic model as the rest of the framework.

Correlate the failed TLS episode with its connection identity before interpreting later retry records as a second failure of the same handshake.

Take the Chapter 11 transfer exercise and first establish its greeting, framing, and shutdown behavior over the legacy connection. When introducing TLS, retain those observations and add separate checks for trusted identity, mismatched identity, and handshake failure. A successful encrypted exchange alone does not distinguish those cases.

There is also a deployment choice. In-process TLS keeps the peer’s TLS connection and its policy at the application boundary, but makes that process responsible for certificate and key configuration. A terminating proxy can centralize that operation; the application then receives a different connection and needs an explicit trust policy for any forwarded identity. The protocol parser may remain reusable in both arrangements, while the authorization boundary changes.

::: {.snodec-rule title="Protocol continuity rule"}
Write the protocol endpoint as if secure and insecure transport are the same conversation whenever that is actually true.
:::

Let the selected handle, registered instance, TLS wrapper and configuration carry the secure-transport differences unless they change protocol semantics.

\index{TLS!deployment responsibility}

TLS-capable components make secure connection handling possible; they do not by themselves complete a secure deployment. Certificate files, private-key permissions, trust anchors, SNI policy, and diagnostics still belong to the deployed role and its configuration.

That distinction will matter again in the deployment chapters. A binary may be linked with TLS support and still fail as a secure service if the surrounding filesystem, permissions, and trust material are wrong. TLS-capable linking is not the same as TLS deployment.

::: {.snodec-remember title="What to remember"}
- TLS adds secure setup, verification and shutdown between the carrier and protocol.
- The handle, registered instance and factory retain their responsibilities when the stream wrapper changes.
- Trust, expected identity and SNI require separate decisions before secure readiness.
- A context can remain TLS-independent when secure and insecure transports carry the same conversation.
- Use certificate or TLS properties in protocol logic when they affect application semantics.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Which parts of EchoPair remain unchanged when its stream wrapper becomes TLS, and which responsibilities change?
2. **Review (O2, O3).** Why can a trusted certificate still identify the wrong peer? Explain why SNI and an early `onConnect()` callback do not establish authenticated readiness.
3. **Lab (O2, O3).** Run the public trust-and-identity fixture. Predict and observe trusted/matching success, trusted/wrong-name rejection and untrusted/matching-name rejection; record whether SSL exists in the early callback.
4. **Lab (O1, O3).** Build the TLS EchoPair wrapper and run the independent TLS peer. Expect the binary payload unchanged and reciprocal close-notify during shutdown.
5. **Design (O1, O2, O3).** Choose TLS in the service or termination at a proxy for a gateway. State the trusted hop, expected identity, certificate ownership and shutdown limits; explain what authorization still requires.

Public solutions and bounded lab commands: `companion/exercises/ch14/README.md`.
:::
