## Server-Sent Events and Real-Time HTTP

### From request / response to event streams

Chapter 22 showed how HTTP handling becomes application structure through routing, middleware, and request/response facades. Chapter 23 keeps that structure inside the HTTP world, but changes the temporal shape of one response: a route may start a response stream and keep it open while the server sends event-stream records over time.

That is the central idea of this chapter:

> Server-Sent Events keep the application inside HTTP while changing the response from a short message into a long-lived event stream.

Here, “real-time” means live-update HTTP. It does not mean deterministic latency, hard real-time scheduling, or a replacement for the lower timing and failure model introduced earlier. SSE is a practical web mechanism for delivering server-side updates as they become available.

SSE is useful because it is still HTTP. It does not require a full bidirectional protocol when the application only needs server-to-client updates, and it fits naturally between ordinary request/response HTTP and WebSocket:

```text
ordinary HTTP
  -> one request, one response

Server-Sent Events
  -> one request, one long-lived event response

WebSocket
  -> HTTP upgrade, then bidirectional messaging
```

This makes SSE a good bridge inside Part VII:

```text
Chapter 21: HTTP messages
Chapter 22: Express-like application structure
Chapter 23: long-lived one-way HTTP event streams
Chapter 24: HTTP upgrade to bidirectional WebSocket communication
```

### SSE in the layered SNode.C web stack

The stack now looks like this:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response
              -> long-lived event-stream response
                  -> MessageEvent handling
```

SSE does not bypass the lower architecture. It still depends on the runtime, a lower communication family, stream transport, legacy or TLS connection handling, HTTP client/server behavior, connection lifecycle, retry and reconnect policy, and diagnostics.

The application-facing unit changes again. Earlier chapters showed a sequence of semantic lifts:

```text
stream bytes
  -> HTTP Request / Response

HTTP request / response
  -> Express Request / Response facades

SSE event-stream fields
  -> MessageEvent
```

That is the main continuity. SSE remains HTTP, but the application no longer reacts to one completed response only. It reacts to event objects produced from a long-lived response stream.

### Ordinary HTTP, SSE, and WebSocket side by side

A compact comparison helps place SSE without turning this chapter into a protocol reference.

| Concern | Ordinary HTTP | Server-Sent Events | WebSocket |
|---|---|---|---|
| connection shape | request / response | request / long-lived response stream | upgraded bidirectional connection |
| direction | usually client request, server response | server-to-client events | both directions |
| protocol world | HTTP | HTTP | starts with HTTP upgrade, then WebSocket |
| application unit | response | event | message / frame |
| typical use | documents, APIs, files | notifications, dashboards, feeds | bidirectional interaction |
| complexity | lowest | moderate | higher |

SSE is not WebSocket with fewer features. It is a different fit. It is useful when the server should push events and the client does not need to send messages back over the same long-lived channel. If both sides need to send independent messages over one long-lived channel, WebSocket becomes the more natural fit. Chapter 24 treats that case.

### SSE as long-lived HTTP

SSE begins as HTTP. The client sends an HTTP request for an event-stream endpoint. If the server accepts the request and responds with an event-stream response, the response remains open.

A useful model is:

```text
HTTP request
  -> HTTP response starts
      -> response remains open
          -> server sends event-stream records over time
              -> client dispatches MessageEvent objects
```

The response is still an HTTP response. The difference is that it is not immediately completed. It becomes a long-lived stream of event records.

On the client side, the long-lived response is represented by an HTTP request that installs an SSE event receiver after the response has been validated as `text/event-stream`. On the server side, SSE is an HTTP or Express route that chooses to keep the response open and format outgoing data as event-stream records.

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

This makes SSE suitable for live updates without repeatedly polling the server. The server can keep the response open and emit changes as they happen.

#### Server-to-client event direction

SSE is one-way by design. The long-lived stream carries events from server to client. That makes it useful for dashboards, notifications, monitoring views, activity streams, state updates, and incremental event feeds.

The client can still make ordinary HTTP requests elsewhere in the application. The SSE stream itself is simply the endpoint that carries a long-lived server-to-client update channel.

#### Why one-way is useful

One-way streaming keeps the model simpler than bidirectional messaging. The application can use SSE when the main requirement is:

```text
server state changes
  -> client view updates
```

That pattern is common in monitoring and dashboard applications. The application still has to think about reconnect, retry, timeouts, and diagnostics, but it does not need the full protocol shape of a bidirectional upgraded connection.

### Client-side EventSource and server-side streaming endpoints

It is important to distinguish the two sides carefully.

| Side | SNode.C view |
|---|---|
| client side | built-in `EventSource` abstraction on top of an HTTP client |
| server side | HTTP/Express endpoint that keeps a response open and writes event-stream records |

The inspected source strongly exposes the client-side `EventSource` facility. Server-side SSE is not a different server instance type and not a symmetric server-side `EventSource` abstraction. It is a route or HTTP handler that keeps the response open and writes data in event-stream format.

Conceptually:

```text
server route
  -> emits text/event-stream response

client EventSource
  -> requests text/event-stream
      -> parses events
          -> dispatches MessageEvent objects
```

The two sides meet at the HTTP/SSE boundary, but they are not the same API surface.

A server-side event-stream record may contain fields such as:

```text
event: status
id: 42
data: {"state":"online"}

```

The blank line ends the accumulated event record. This is enough server-side format detail for this chapter. The central architectural point is that the server writes event-stream records over an HTTP response that remains open.

### The EventSource client abstraction

The client-side `EventSource` abstraction gives the application an event-stream model while the lower stream and HTTP details remain underneath. The application sees a higher-level surface:

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

This follows the pattern prepared by the previous chapters. The lower client handle, configured client-side communication role, registered runtime-visible client instance, connection, HTTP request, and parser still exist. `EventSource` is the application-side abstraction that exposes the event-stream behavior.

#### ReadyState as client-side lifecycle

SSE is not a one-shot request. It has a lifecycle, and the client-side `EventSource` ready-state model expresses that lifecycle:

| Ready state | Meaning |
|---|---|
| `CONNECTING` | the stream is not open yet or is reconnecting |
| `OPEN` | the event stream is active |
| `CLOSED` | the application has closed it or it will not reconnect |

This is a runtime concept, not only a browser-style convenience. A long-lived stream needs a way to say whether it is connecting, open, or closed. That state also matters for diagnostics and application decisions.

#### MessageEvent as application-facing unit

The `MessageEvent` object is the semantic lift from SSE wire fields to application meaning. It contains exactly the kind of information the application normally needs:

| Field | Meaning |
|---|---|
| `type` | `"message"` or a custom event type |
| `data` | event payload |
| `lastEventId` | event ID associated with this event |
| `origin` | stream origin |

The application should not normally parse raw event-stream lines. It should react to events:

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

Custom event listeners receive events by type. The default `onMessage` listeners receive events whose type is `"message"`.

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

The lower HTTP receive loop remains underneath, but the application-facing model is event-based.

#### Close as intentional shutdown

`close()` is important because not every disconnect is a failure. A user or application may intentionally stop the stream.

In SNode.C’s EventSource client, `close()` marks the EventSource as `CLOSED`, disables reconnect and retry on the underlying client configuration, and shuts down the write side if a socket connection is present. The conceptual distinction is:

```text
stream interrupted while not CLOSED
  -> may reconnect

stream closed intentionally
  -> should not reconnect
```

That matches the retry/reconnect vocabulary from Chapter 20.

### SSE starts as an HTTP request

Even though the application eventually receives events, SSE starts as HTTP. The client sends a request for the event-stream endpoint.

A simplified request shape is:

```text
GET /events HTTP/1.1
Accept: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

The exact path depends on the application. The important point is that the client does not start with a new non-HTTP protocol. It asks HTTP for an event stream.

#### Event-stream request setup

The client-side HTTP request for SSE uses HTTP/1.1 behavior and event-stream headers. The key header is:

```text
Accept: text/event-stream
```

This tells the server that the client expects a server-sent event stream. The request also uses:

```text
Cache-Control: no-cache
Connection: keep-alive
```

These settings match the long-lived streaming nature of the interaction.

#### Stream validation

The client should not treat every HTTP response as an event stream. It validates that the response is actually a server-sent event stream.

The important check is:

```text
response Content-Type contains text/event-stream
```

The request still carries `Accept: text/event-stream`. If validation fails, the socket context is closed and the error callback is invoked. This prevents a normal HTML page, redirect, error page, or unrelated response from being interpreted as SSE data.

### Parsing the event stream

Once the stream is open, the client receives bytes over time. The parser turns those bytes into event records:

```text
incoming stream bytes
  -> pending buffer
      -> lines
          -> fields
              -> accumulated event
                  -> dispatch on blank line
```

SSE is therefore more than “read text forever.” The stream has field semantics. The parser accumulates, interprets, and dispatches.

#### SSE fields

A compact field table is enough for this chapter.

| Field | Effect |
|---|---|
| `data` | append value plus newline to the accumulated payload |
| `event` | set custom event type |
| `id` | update the ID buffer if the value contains no NUL byte |
| `retry` | update retry timing if the value is numeric |
| blank line | dispatch accumulated event |
| comment line | ignored |

Multiple `data:` lines belong to the same event until a blank line dispatches it. The default event type is `"message"` when no custom `event:` field is present. The `id:` field participates in continuity. The `retry:` field participates in reconnection timing.

#### Dispatch on blank line

SSE dispatch is line-oriented. The parser accumulates fields until it sees the event boundary. The event boundary is a blank line.

At that point:

```text
accumulated data
  -> MessageEvent
      -> listeners
```

Before dispatch, the trailing newline added by `data:` accumulation is removed. If there is no accumulated data, no message event needs to be delivered. This keeps event dispatch tied to the SSE wire format.

#### Size guards and malformed streams

A long-lived stream must not allow unbounded pending data. The implementation applies finite limits to pending lines and accumulated data, so a malformed or hostile long-lived stream cannot grow parser state without bound. If parsing fails, the stream can be closed.

That is part of making SSE operationally usable. Long-lived inputs need limits.

### Retry and continuity

SSE interacts naturally with retry and reconnect behavior. This should be read through the vocabulary of Chapter 20.

SSE has protocol-level retry information. SNode.C maps that information into the underlying client reconnect/retry configuration. That means the event-stream layer and the client role cooperate.

#### The `retry:` field

A server may send a `retry:` field. The value is interpreted as a retry interval. When accepted, it updates the EventSource retry value and the underlying client reconnect/retry timing.

Conceptually:

```text
retry: 5000
  -> EventSource retry interval becomes 5000 ms
      -> client reconnect/retry timing is updated
```

`retry:` is not a generic transport timeout. It is event-stream protocol information that updates the client-side recovery interval. The SSE value is expressed in milliseconds; the underlying client configuration receives the corresponding seconds value.

#### Last-Event-ID

The `id:` field updates the client-side event ID buffer. When an event is dispatched, the last event ID can be remembered.

When a new request starts and a last event ID is known, the client sets:

```text
Last-Event-ID: ...
```

on the request. This gives the server a continuity hint after reconnect. The exact server behavior depends on the application, but the client-side mechanism is important: it lets an event stream carry continuity information across interruptions.

#### Interruption versus intentional close

An interruption while the stream is not `CLOSED` is handled differently from an intentional close. Conceptually:

```text
interrupted while not CLOSED
  -> error notification
  -> ready state returns to CONNECTING
  -> parsing buffers are cleared
  -> retry/reconnect timing is reapplied

closed intentionally
  -> ready state becomes CLOSED
  -> retry/reconnect is disabled
```

This is where Chapter 20’s retry/reconnect distinction becomes visible at the SSE layer.

### Express-like routes and SSE endpoints

Express-like applications are a natural place to expose SSE endpoints. They already organize routes, middleware, authentication, static assets, application APIs, and response behavior.

An SSE endpoint can be one route in that application. Server-side code can keep the HTTP response open and write event-stream records over time. The built-in `EventSource` facility discussed in this chapter is the client-side counterpart.

The two sides meet at the HTTP/SSE boundary:

```text
server route
  -> emits text/event-stream response

client EventSource
  -> requests text/event-stream
      -> parses events
          -> dispatches MessageEvent objects
```

This pairing is useful, but it is not the same abstraction on both sides. The server route produces event-stream syntax; the client `EventSource` interprets it as events.

### Lower layers and diagnostics still matter

SSE is a high-level event-stream behavior, but it still depends on lower-layer behavior. The event stream can be affected by DNS or address selection, lower-family endpoint configuration, legacy or TLS connection handling, HTTP response validation, read/write behavior, disconnects, retry and reconnect timing, intentional close, parser errors, and server-side application behavior.

For SSE, the operator often needs to know:

- whether the HTTP connection was established,
- whether the SSE response opened,
- whether the stream entered `OPEN`,
- whether an error listener fired,
- whether reconnect is expected,
- which retry interval is active,
- which last event ID is known,
- whether the stream was closed intentionally.

This connects directly to the diagnostic model from Chapter 18 and the retry/reconnect model from Chapter 20:

```text
Chapter 18
  -> logs, connection identity, counters, visible configuration

Chapter 20
  -> reconnect, retry, timeout, intentional close

Chapter 23
  -> ready state, response validation, parser errors, last event ID, retry interval
```

SSE does not need a new operational philosophy. It needs the existing one applied to a long-lived HTTP stream.

### Real-time-style HTTP

The chapter title says “real-time HTTP.” The word “real-time” here means live-update behavior over HTTP. It does not mean deterministic latency or hard real-time scheduling.

SSE is a practical web mechanism for delivering events over a long-lived HTTP response. That makes it useful for user interfaces and monitoring systems where updates should arrive as the server produces them.

Use cases include:

- sensor dashboards,
- status pages,
- notification feeds,
- build or deployment logs,
- monitoring views,
- application activity streams.

The timing behavior still depends on the network, server, client, buffering, and reconnect policy.

### What to remember

- Server-Sent Events keep the application inside HTTP while turning one response into a long-lived event stream.
- SSE is one-way: the long-lived stream carries events from server to client.
- SNode.C provides a client-side `EventSource` abstraction on top of an HTTP client.
- Server-side SSE is an HTTP or Express route that keeps a response open and writes event-stream records.
- `ReadyState` describes the client-side stream lifecycle: connecting, open, or closed.
- `MessageEvent` raises SSE fields into an application-facing event object.
- `data`, `event`, `id`, and `retry` fields have distinct meanings; a blank line dispatches the accumulated event.
- `retry:` updates client recovery timing; `Last-Event-ID` supports continuity across reconnects.
- `close()` is intentional shutdown and disables retry/reconnect behavior.
- Lower HTTP, connection lifecycle, diagnostics, retry/reconnect, and TLS behavior remain relevant.
- Chapter 24 moves to WebSocket and bidirectional upgraded communication.

### Closing perspective

Chapter 21 raised stream communication to HTTP messages. Chapter 22 organized HTTP messages into application structure. Chapter 23 kept that structure inside HTTP but stretched one response over time.

The path now looks like this:

```text
HTTP request / response
  -> Express-like application structure
      -> Server-Sent Events
          -> long-lived one-way event streaming
```

The next chapter turns to WebSocket. There, HTTP is used to negotiate an upgrade, after which WebSocket provides a bidirectional message-oriented connection.
