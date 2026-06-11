## Epilogue — What to Take Away from SNode.C {.unnumbered}

SNode.C is not primarily a shortcut for opening sockets.

It is a way of keeping network-system architecture visible while the application grows from simple connections to protocols, protocols to roles, roles to applications, and applications to deployable systems.

That visibility is the real subject of this book.

### Layers are not decoration {.unnumbered}

The word layered can be used lazily. In SNode.C, it is meant operationally.

Lower communication families, stream transport, TLS or legacy connection handling, protocol layers, application roles, configuration, diagnostics, build targets, packages, and deployment shape all have their own responsibilities.

The important lesson is not that every layer must be visible to every programmer at every moment. The lesson is that the architecture remains understandable because the layers have not been erased prematurely.

```text
lower family
  -> transport and connection handling
      -> protocol meaning
          -> application role
              -> system boundary
```

A reader who understands this stack can move between IPv4, IPv6, Unix domain sockets, Bluetooth, HTTP, WebSocket, MQTT, persistence, and deployment without treating each subject as a separate world.

### Boundaries are design decisions {.unnumbered}

Many mistakes in network applications are not caused by the wrong syntax. They are caused by the wrong boundary.

A protocol concern is placed in a transport layer. A deployment concern is hidden in a parser. A domain rule is buried in a socket callback. A persistence policy is smuggled into an HTTP route. A retry policy becomes invisible because it is treated as a low-level accident.

SNode.C gives the programmer many possible places where behavior can live. That is powerful, but it also requires judgment.

The central question returns again and again:

```text
Which boundary honestly owns this concern?
```

That question is useful before writing code, while debugging code, while designing configuration, while packaging the application, and while deciding whether a system should remain one executable or become several cooperating services.

### Roles and instances need precise language {.unnumbered}

The book deliberately distinguishes system-design roles, application-side server or client handles, configured communication roles, registered runtime-visible instances, connections, contexts, factories, middleware, subprotocols, and application services.

That precision may feel demanding at first. It is worth the effort.

When the vocabulary is clear, a system can be discussed by developers, operators, teachers, and students using the same names.

```text
configured role name
  -> appears in configuration
  -> appears in logs
  -> appears in diagnostics
  -> appears in operational discussion
```

This is not merely terminology. It is how a running system becomes understandable.

### Protocols carry meaning, not only bytes {.unnumbered}

The book started with simple communication and gradually moved upward: custom stream protocols, HTTP, Express-like routing, SSE, WebSocket, MQTT, MQTT-over-WebSocket, and multi-protocol IoT systems.

The recurring lesson is that bytes become useful only when a layer gives them meaning.

```text
raw data
  -> parsed protocol
      -> session or request meaning
          -> application state
              -> system behavior
```

This is why protocol code should not be treated as accidental glue. It is where communication becomes part of an application.

### Build and deployment are part of architecture {.unnumbered}

A network framework does not end at the source tree.

The build target says what the application selects. The exported package says what external consumers can depend on. The install component says what files need to exist. The package dependency says what the target system must provide. The runtime path says where loaded modules and services can be found. The configuration file says what role shape is deployed.

That is why this book treated CMake, packaging, deployment, testing, and debugging as architectural surfaces rather than as afterthoughts.

```text
source component
  -> build target
      -> installed component
          -> package dependency
              -> deployed role
                  -> observable runtime behavior
```

A system that is clear only in the source tree is not yet fully clear.

### The guided project is not the end of the idea {.unnumbered}

MiniGateway was deliberately small. It did not try to become a product. It showed how the pieces can be assembled while preserving the vocabulary of the book.

That is the transferable lesson.

A real application may use different lower families, different protocols, more roles, stronger persistence, stronger authentication, different deployment targets, or a larger ecosystem such as MQTTSuite. The architectural questions remain the same.

```text
What is the domain state?
Which roles expose it?
Which protocols serve which boundaries?
Which configuration makes the deployment reproducible?
Which diagnostics make failure understandable?
Which tests protect the real boundaries?
```

When those questions remain answerable, the application can grow without becoming opaque.

### Where to go next {.unnumbered}

A reader who finishes this book should not merely know that SNode.C has servers, clients, contexts, HTTP, WebSocket, MQTT, configuration, and CMake components.

The reader should know how to think with them.

Useful next steps are:

```text
build a small application with one clear role
add one second protocol surface deliberately
make configuration reproduce the role shape
add diagnostics before the system becomes hard to debug
test one boundary at a time
only then generalize or split the system
```

SNode.C rewards this discipline because its architecture makes the boundaries explicit. It does not force good design automatically, but it gives good design places to live.

### Closing perspective {.unnumbered}

The promise of SNode.C is not that networking becomes trivial.

Networking is not trivial. Protocols, timing, failures, deployment, security, diagnostics, and system evolution remain real engineering problems.

The promise is different:

```text
network systems can remain understandable
when their layers and boundaries remain visible
```

That is the book's central lesson.

If the reader carries one idea forward, it should be this:

```text
Do not hide meaning too early.
Place behavior where the right boundary can own it.
Keep that boundary visible in code, configuration, diagnostics, build, deployment, and tests.
```

That is how SNode.C should be used.
And that is how layered network applications in modern C++ can stay clear as they grow.
