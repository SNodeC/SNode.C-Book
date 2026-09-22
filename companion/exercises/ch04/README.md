# Chapter 4 — solutions and discussion

## 1. Review (O1)

The local endpoint handle configures the role and registers activation. Shared
endpoint state and runtime callbacks retain what active work needs after a local
wrapper leaves scope. An explicit listen operation has its own flow; an accepted
connection is a separate peer relationship and can survive termination of that
listener. Its current context belongs to that connection, not to the local
variable or the listening operation's stack frame. Retaining a flow handle permits
control of that operation; dropping it is not cancellation.

This does not keep an arbitrary reference capture alive. If a factory passes an
application model to each context, the application must retain that model through
the last use. The independent-peer lab below tests peer isolation, not cancellation
of the listening flow; those are different observations.

## 2. Review (O2)

Read `net::rc::stream::tls::SocketServer<MyFactory>` as a Bluetooth RFCOMM stream
server with TLS connection handling and a factory creating per-peer contexts.
Its public header is `<net/rc/stream/tls/SocketServer.h>` and its corresponding
component is `net-rc-stream-tls`. Availability depends on the enabled framework
components and build dependencies. The type name does not supply Bluetooth
hardware, permissions, pairing, a selected channel, certificates, or trust policy.
It also does not specify the application protocol implemented by the factory's
contexts. Selecting this type alone does not demonstrate a radio or TLS exchange.

## 3. Lab (O3)

Use the common configuration in [the exercise guide](../README.md), then:

```sh
cmake --build build/labs --target ch04-lab
ctest --test-dir build/labs -R '^exercise-ch04-model-instances$' --output-on-failure -V
```

This reuses `companion/exercises/ch30/model-instances.cpp` as a focused early
experiment; no later chapter is a prerequisite. It compiles the canonical
`companion/examples/MiniGateway/MeasurementModel.cpp` and uses the public
`accept(...)` and `current()` interface. Two references representing input paths
share one model. Their accepted sequences must be 1 and 2, and `current()` must
report 2. Two separate model objects instead each assign 1 to their first input.
Expect one PASS line comparing shared and separate ownership.

A minimal mental walkthrough is enough before opening the source: constructing
a model creates its own current measurement; `accept` replaces an input sequence
with the next locally accepted sequence. References do not create another model.
The exercise checks object ownership, not network delivery, persistence, or
interprocess order. A model constructed for each context would partition accepted
state by peer, even though every context used the same class definition.

## 4. Lab (O1)

```sh
ctest --test-dir build/labs -R '^exercise-ch04-independent-peers$' --output-on-failure -V
```

The existing bounded peer script is reused with the canonical EchoPair server.
One connection sends ten bytes, `other` followed by NUL followed by `peer`, while
another peer remains idle. The active connection must receive the same bytes.
After the idle peer closes, the first sends `still here` and must receive that
unchanged. Expect one PASS line covering both exchanges. The harness uses a fresh
loopback port and stops the server after the observations.

The result distinguishes per-connection behavior from the endpoint that accepted
both peers. It does not stop the listening flow or destroy the application model,
so neither of those operations is established by this run. It also does not say
that stream reads preserve the boundaries of the peer's writes.

## 5. Design (O1, O2, O3)

Use separate configured endpoints for the IP and local Unix input. Select the Unix
public role header/type and matching `net-un-stream-legacy` component where the
non-TLS variant meets the local policy. Give the Unix endpoint a socket identity
and permissions appropriate to its deployment; an IP address/port is not a path.

Keep partial-record buffers in each input's context. A factory supplies the
appropriate context for each accepted peer and gives it access to the one shared
application model. Parse and validate before accepting a measurement. The model
assigns ordering across both inputs; neither context keeps a competing global
sequence. Output observers consume already accepted state.

Construct the model so it survives all contexts and observers that reference it.
Remove each observer subscription before its captured response or other state is
destroyed. Shutting down one listening flow should have an explicit policy for
already accepted peers, rather than relying on local wrapper destruction. Compare
the resulting address, lifecycle, and protocol obligations separately.
