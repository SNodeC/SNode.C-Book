# Chapter 5 — solutions and discussion

## 2. Review (O2)

Read `net::rc::stream::tls::SocketServer<MyFactory>` as a Bluetooth RFCOMM stream
server with TLS connection handling and a factory creating per-peer contexts.
Its public header is `<net/rc/stream/tls/SocketServer.h>` and its corresponding
component is `net-rc-stream-tls`. Availability depends on the enabled framework
components and build dependencies. The type name does not supply Bluetooth
hardware, permissions, pairing, a selected channel, certificates, or trust policy.
It also does not specify the application protocol implemented by the factory's
contexts. Selecting this type alone does not demonstrate a radio or TLS exchange.

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

TODO(P3-apparatus)
