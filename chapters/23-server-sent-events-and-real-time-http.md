## Server-Sent Events and Real-Time HTTP

### From request / response to event streams

Chapter 22 showed how HTTP handling becomes application structure through routing, middleware, and request/response facades.

Chapter 23 keeps the application inside the HTTP world, but changes the response shape.

One request opens a response stream that can remain open while the server sends event records over time.

That is the central idea of this chapter:

> Server-Sent Events keep the application inside HTTP while changing the response from a short message into a long-lived event stream.

SSE is useful because it is still HTTP.

It does not require a full bidirectional protocol when the application only needs server-to-client updates.

It sits between ordinary request/response HTTP and WebSocket:

```text
ordinary HTTP
  -> one request, one response

Server-Sent Events
  -> one request, one long-lived event response

WebSocket
  -> HTTP upgrade, then bidirectional messaging
```

This makes SSE a good bridge between the HTTP/Express chapters and the WebSocket chapter.

### SSE in the SNode.C web stack

The stack now looks like this:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response
              -> long-lived event-stream response
                  -> application MessageEvent handling
```

SSE does not bypass the lower architecture.

It still depends on:

- the runtime,
- a lower communication family,
- stream transport,
- legacy or TLS connection handling,
- HTTP client/server behavior,
- connection lifecycle,
- retry and reconnect policy,
- diagnostics.

The application-facing unit changes again.

Earlier chapters showed these semantic lifts:

```text
stream bytes
  -> HTTP Request / Response

HTTP request
  -> Express Request / Response facades

SSE lines
  -> MessageEvent
```

That is the main continuity.

SSE is another layer that gives the application a more meaningful unit of work.

### Ordinary HTTP, SSE, and WebSocket side by side

A compact comparison helps place SSE.

| Concern | Ordinary HTTP | Server-Sent Events | WebSocket |
|---|---|---|---|
| connection shape | request / response | request / long-lived response stream | upgraded bidirectional connection |
| direction | usually client request, server response | server to client events | both directions |
| protocol world | HTTP | HTTP | starts with HTTP upgrade, then WebSocket |
| application unit | response | event | message / frame |
| typical use | documents, APIs, files | notifications, dashboards, feeds | bidirectional interaction |
| complexity | lowest | moderate | higher |

SSE is not WebSocket with fewer features.

It is a different fit.

It is useful when the server should push events and the client does not need to send messages back over the same long-lived channel.

### SSE as long-lived HTTP

SSE begins as HTTP.

The client sends a HTTP request for an event-stream endpoint.

If the server accepts the request and responds with an event-stream response, the response remains open.

A useful model is:

```text
HTTP request
  -> HTTP response starts
      -> response remains open
          -> server sends event records over time
              -> client dispatches MessageEvent objects
```

The response is still a HTTP response.

The difference is that it is not immediately completed.

It becomes a long-lived stream of event records.

#### One request, one open response stream

Ordinary HTTP often looks like this:

```text
request
  -> response
      -> done
```

SSE changes the response phase:

```text
request
  -> response starts
      -> event
      -> event
      -> event
      -> ...
```

This makes SSE suitable for live updates without repeatedly polling the server.

The server can keep the response open and emit changes as they happen.

#### Server-to-client event direction

SSE is one-way by design.

The long-lived stream carries events from server to client.

That makes it useful for:

- dashboards,
- notifications,
- monitoring views,
- activity streams,
- state updates,
- incremental event feeds.

The client can still make ordinary HTTP requests elsewhere in the application.

SSE simply gives one endpoint a long-lived server-to-client update channel.

#### Why one-way is useful

One-way streaming keeps the model simpler than bidirectional messaging.

The application can use SSE when the main requirement is:

```text
server state changes
  -> client view updates
```

That is common in monitoring and dashboard applications.

If both sides need to send independent messages over the same long-lived channel, WebSocket becomes the more natural fit.

Chapter 24 will treat that case.

### Client-side EventSource and server-side SSE endpoints

It is useful to distinguish the two sides carefully.

On the client side, SNode.C provides an `EventSource` abstraction.

On the server side, SSE is expressed as long-lived HTTP response streaming from the web/HTTP application layer.

That means this chapter has two related views:

| Side | SNode.C view |
|---|---|
| client side | built-in `EventSource` tool on top of a HTTP client |
| server side | HTTP/Express endpoint that keeps a response open and writes event-stream data |

The inspected code strongly exposes the client-side facility.

The server-side pattern belongs naturally to HTTP or Express-like application code.

Do not confuse those two surfaces.

### The EventSource client abstraction

The client-side `EventSource` abstraction gives the application an event-stream model.

It provides:

| EventSource concept | Meaning |
|---|---|
| `ReadyState` | stream lifecycle: connecting, open, closed |
| `MessageEvent` | application-facing event object |
| `onMessage(...)` | default message listener |
| `addEventListener(...)` | custom event-type listener |
| `removeEventListeners(...)` | remove listeners for a type |
| `onOpen(...)` | stream open notification |
| `onError(...)` | stream error notification |
| `lastEventId()` | last event ID known to the client |
| `retry()` / `retry(...)` | current retry interval |
| `close()` | intentional shutdown |

This is the same design pattern the previous chapters prepared.

The lower stream and HTTP details still exist.

The application receives a higher-level event-stream surface.

#### ReadyState as lifecycle

SSE is not a one-shot request.

It has a lifecycle.

The ready-state model expresses that lifecycle:

| Ready state | Meaning |
|---|---|
| `CONNECTING` | the stream is not open yet or is reconnecting |
| `OPEN` | the event stream is active |
| `CLOSED` | the application has closed it or it will not reconnect |

This is a runtime concept, not only a browser-style convenience.

A long-lived stream needs a way to say whether it is connecting, open, or closed.

That state also matters for diagnostics and application decisions.

#### MessageEvent as application-facing unit

The `MessageEvent` object is the semantic lift from SSE wire fields to application meaning.

It contains:

| Field | Meaning |
|---|---|
| `type` | `"message"` or a custom event type |
| `data` | event payload |
| `lastEventId` | event ID associated with this event |
| `origin` | stream origin |

The application should not normally parse raw event-stream lines.

It should react to events.

Conceptually:

```text
raw SSE fields
  -> MessageEvent
      -> type, data, lastEventId, origin
```

This is the SSE equivalent of the earlier request/response lifts.

#### Message, custom event, open, and error listeners

The EventSource client has several listener surfaces:

| Listener | Meaning |
|---|---|
| `onMessage(...)` | receive default `"message"` events |
| `addEventListener(...)` | receive events with a named event type |
| `onOpen(...)` | observe successful stream opening |
| `onError(...)` | observe stream errors or interruptions |

This lets the application express event-stream behavior directly:

```text
stream opened
  -> start showing live state

message event arrived
  -> update application state

custom event arrived
  -> dispatch by event type

stream error occurred
  -> show degraded or reconnecting state
```

The lower HTTP receive loop remains underneath.

The application-facing model is event-based.

#### Close as intentional shutdown

`close()` is important because not every disconnect is a failure.

A user or application may intentionally stop the stream.

The client-side implementation marks the stream closed, disables reconnect/retry behavior, and shuts down the write side if a socket connection is present.

The conceptual distinction is:

```text
stream interrupted
  -> may reconnect

stream closed intentionally
  -> should not reconnect
```

That matches the retry/reconnect vocabulary from Chapter 20.

### SSE begins as an HTTP request

Even though the application eventually receives events, SSE starts as HTTP.

The client sends a request for the event-stream endpoint.

A simplified request shape is:

```text
GET /events HTTP/1.1
Accept: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

The exact path depends on the application.

The important point is that the client does not start with a new non-HTTP protocol.

It asks HTTP for an event stream.

#### Event-stream request setup

The client-side HTTP request for SSE sets HTTP/1.1 behavior and event-stream headers.

The key header is:

```text
Accept: text/event-stream
```

This tells the server that the client expects a server-sent event stream.

The request also uses:

```text
Cache-Control: no-cache
Connection: keep-alive
```

These settings match the long-lived streaming nature of the interaction.

#### Stream validation

The client should not treat every HTTP response as an event stream.

It validates that the response is actually a server-sent event stream.

The important check is:

```text
response Content-Type contains text/event-stream
```

If the response is not an event stream, the client closes the connection and reports an error.

This is important operational behavior.

It prevents a normal HTML page, redirect, error page, or unrelated response from being interpreted as SSE data.

### Parsing the event stream

Once the stream is open, the client receives bytes over time.

The parser turns those bytes into event records.

A useful model is:

```text
incoming stream bytes
  -> pending buffer
      -> lines
          -> fields
              -> accumulated event
                  -> dispatch on blank line
```

This is why SSE is more than “read text forever.”

The stream has field semantics.

The parser has to accumulate, interpret, and dispatch.

#### SSE fields

A compact field table is enough for this chapter.

| Field | Effect |
|---|---|
| `data` | append payload line |
| `event` | set custom event type |
| `id` | update event ID buffer if valid |
| `retry` | update retry timing |
| blank line | dispatch accumulated event |
| comment line | ignored |

Multiple `data:` lines belong to the same event until a blank line dispatches it.

The default event type is `"message"` when no custom `event:` field is present.

The `id:` field participates in continuity.

The `retry:` field participates in reconnection timing.

#### Dispatch on blank line

SSE dispatch is line-oriented.

The parser accumulates fields until it sees the event boundary.

The event boundary is a blank line.

At that point:

```text
accumulated data
  -> MessageEvent
      -> listeners
```

If there is no accumulated data, no message event needs to be delivered.

This keeps event dispatch tied to the SSE wire format.

#### Size guards and malformed streams

A long-lived stream must not allow unbounded pending data.

The implementation guards against overly large pending lines and overly large accumulated data.

If parsing fails, the stream can be closed.

This is part of making SSE operationally usable.

Long-lived inputs need limits.

### Retry and continuity

SSE interacts naturally with retry and reconnect behavior.

This should be read through the vocabulary of Chapter 20.

SSE has protocol-level retry information.

SNode.C maps that information into the underlying client reconnect/retry configuration.

That means the event-stream layer and the client role cooperate.

#### The `retry:` field

A server may send a `retry:` field.

The value is interpreted as a retry interval.

When accepted, it updates the EventSource retry value and the underlying client reconnect/retry timing.

Conceptually:

```text
retry: 5000
  -> EventSource retry interval becomes 5000 ms
      -> client reconnect/retry timing is updated
```

This is not a generic transport timeout.

It is SSE protocol information that influences recovery behavior.

#### Last-Event-ID

The `id:` field updates the client-side event ID buffer.

When an event is dispatched, the last event ID can be remembered.

On a later request, the client can send:

```text
Last-Event-ID: ...
```

if a last event ID is known.

This gives the server a continuity hint after reconnect.

The exact server behavior depends on the application, but the client-side mechanism is important.

It lets an event stream carry continuity information across interruptions.

### Express-like applications and SSE endpoints

Express-like applications are a natural place to expose SSE endpoints.

They already organize:

- routes,
- middleware,
- authentication,
- static assets,
- application APIs,
- response behavior.

An SSE endpoint can be one route in that application.

Server-side code can keep the HTTP response open and write event-stream records over time.

The built-in `EventSource` facility discussed in this chapter is the client-side counterpart.

The two sides meet at the HTTP/SSE boundary:

```text
server route
  -> emits text/event-stream response

client EventSource
  -> requests text/event-stream
      -> parses events
          -> dispatches MessageEvent objects
```

This is a useful pairing, but it is not the same abstraction on both sides.

### Lower layers and diagnostics still matter

SSE is a high-level event-stream behavior.

It still depends on lower-layer behavior.

The event stream can be affected by:

- DNS or address selection,
- lower-family endpoint configuration,
- legacy or TLS connection handling,
- HTTP response validation,
- read/write behavior,
- disconnects,
- retry and reconnect timing,
- intentional close,
- parser errors,
- server-side application behavior.

For SSE, the operator often needs to know:

- whether the HTTP connection was established,
- whether the SSE response opened,
- whether the stream entered `OPEN`,
- whether an error listener fired,
- whether reconnect is expected,
- which retry interval is active,
- which last event ID is known,
- whether the stream was closed intentionally.

This connects directly to the diagnostic model from Chapter 18 and the retry/reconnect model from Chapter 20.

SSE does not need a new operational philosophy.

It needs the existing one applied to a long-lived HTTP stream.

### Real-time-style HTTP

The chapter title says “real-time HTTP.”

In practice, SSE is best understood as real-time-style or live-update HTTP.

It is not a deterministic hard real-time mechanism.

It is a practical web mechanism for delivering events over a long-lived HTTP response.

That makes it useful for user interfaces and monitoring systems where updates should arrive as the server produces them.

Use cases include:

- sensor dashboards,
- status pages,
- notification feeds,
- build or deployment logs,
- monitoring views,
- application activity streams.

The timing behavior still depends on the network, server, client, buffering, and reconnect policy.

### What to remember

Remember:

- SSE is long-lived HTTP event streaming.
- SSE remains inside the HTTP world.
- One request opens a response stream that can carry many events.
- SSE is one-way from server to client.
- SNode.C provides a client-side `EventSource` abstraction.
- Server-side SSE is expressed as long-lived HTTP response streaming.
- `ReadyState` represents stream lifecycle.
- `MessageEvent` raises SSE fields into event objects.
- `data`, `event`, `id`, and `retry` fields have distinct meanings.
- A blank line dispatches an accumulated event.
- `retry` updates reconnect/retry timing.
- `Last-Event-ID` supports stream continuity.
- SSE begins as a HTTP request with `Accept: text/event-stream`.
- The client validates the event-stream response.
- Lower runtime, HTTP client behavior, connection lifecycle, diagnostics, and retry behavior still matter.
- Chapter 24 moves to WebSocket and bidirectional upgraded communication.

### Closing perspective

Chapter 23 showed how HTTP can remain open as a one-way event stream.

That gives SNode.C a real-time-style web mechanism without leaving the HTTP layer.

The path now looks like this:

```text
HTTP request / response
  -> Express-like application structure
      -> Server-Sent Events
          -> long-lived one-way event streaming
```

The next chapter turns to WebSocket.

There, HTTP upgrade leads to a bidirectional message-oriented connection.
