## Server-Sent Events and Real-Time HTTP {#server-sent-events-and-real-time-http}

\index{Server-Sent Events}
\index{SSE}
\index{EventSource@\texttt{EventSource}}
\index{real-time HTTP}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Explain how an open HTTP response becomes typed events and how its subscriber is released.
- **O2.** Build the SSE example and compare an accepted measurement with the event received by an observer.
- **O3.** Decide a recovery and slow-observer policy without confusing event IDs with delivery acknowledgements.
:::

### From request / response to event streams

Routing, middleware, and request/response facades stay inside the HTTP world, but Server-Sent Events change the temporal shape of one response: a route may start a response stream and keep it open while the server sends event-stream records over time.

Here, “real-time” means live-update HTTP. It does not mean deterministic latency, hard real-time scheduling, or a replacement for the lower timing and failure model introduced earlier. SSE is a practical web mechanism for delivering server-side updates as they become available.

SSE fits server-to-client updates that do not require a bidirectional messaging protocol.


\index{SSE!layered model}
\index{event streams}


SSE keeps the same lower stack and HTTP request/response foundation, but the response becomes a long-lived event stream that produces `MessageEvent` objects.

The new lifetime matters operationally: a request that remains open keeps a response and its connection resources alive. Retry can establish a replacement stream, but it cannot by itself replay the events missed during the interruption.


A compact comparison helps place SSE without turning this chapter into a protocol reference.

| Concern | Ordinary HTTP | Server-Sent Events | WebSocket |
|---|---|---|---|
| connection shape | request / response | request / long-lived response stream | upgraded bidirectional connection |
| direction | usually client request, server response | server-to-client events | both directions |
| protocol world | HTTP | HTTP | starts with HTTP upgrade, then WebSocket |
| application unit | response | event | message / frame |
| typical use | documents, APIs, files | notifications, dashboards, feeds | bidirectional interaction |
| application obligation | complete each response | bound observer state and decide replay | define message semantics and both directions of flow |

SSE is a different fit from WebSocket, not a weaker version of it. It fits cases where the server should push events and the client does not need to send messages back over the same long-lived channel. If both sides need to send independent messages over one long-lived channel, WebSocket becomes the more natural fit. Chapter 19 treats that case.


\index{SSE!long-lived HTTP}
\index{HTTP streaming}


SSE begins with one HTTP request and keeps its response open. The client can still send ordinary requests to other endpoints; this observation stream carries only server-to-client records. On the client, a validated `text/event-stream` response installs the event receiver. On the server, an HTTP or Express route formats the records without ending the response.

### The server route and its observer lifetime

\index{EventSource@\texttt{EventSource}}
\index{streaming endpoints}


| Side | SNode.C view |
|---|---|
| client side | built-in `EventSource` abstraction on top of an HTTP client |
| server side | HTTP/Express endpoint that keeps a response open and writes event-stream records |

SNode.C exposes the client-side `EventSource` facility explicitly. Server-side SSE is a route or HTTP handler that keeps the response open and writes data in event-stream format, not a different server abstraction or a symmetric server-side `EventSource` abstraction.


A server-side event-stream record may contain fields such as:

```text
event: status
id: 42
data: {"state":"online"}

```

The blank line ends the accumulated event record. In SNode.C response streaming, each `sendFragment(...)` call emits one response fragment with line termination; SSE field fragments should therefore be passed without embedded `\n` or `\r\n`. Emit the blank event boundary as a separate empty fragment.


A server-side SSE endpoint is still an ordinary HTTP route. The teaching route chooses a narrow request contract: it checks for an exact `Accept: text/event-stream` value before switching into long-lived streaming behavior. A general endpoint may use a broader content-negotiation policy; the restriction here belongs to this example.

The following complete companion example uses an application-owned measurement source. The publisher keeps the current value and a list of listeners. Subscribing returns the position of one listener; unsubscribing removes that listener. The route connects those two operations to the lifetime of its HTTP response:

<!-- snodec-source: companion/examples/SSE-Server/main.cpp -->
```cpp
#include <core/socket/State.h>
#include <express/legacy/in/WebApp.h>
#include <nlohmann/json.hpp>
#include <Log.h>
#include <web/http/http_utils.h>
#include <web/http/server/SocketContext.h>

#include <cstdint>
#include <functional>
#include <list>
#include <memory>
#include <string>
#include <utility>

using WebApp = express::legacy::in::WebApp;
using Request = WebApp::Request;
using Response = WebApp::Response;
using SocketAddress = WebApp::SocketAddress;

struct Measurement {
    std::uint64_t sequence = 0;
    std::string sensor;
    double value = 0.0;

    nlohmann::json toJson() const {
        return {
            {"sequence", sequence},
            {"sensor", sensor},
            {"value", value},
        };
    }
};

class MeasurementPublisher {
public:
    using Listener = std::function<void(const Measurement&)>;
    using Subscription = std::list<Listener>::iterator;
    Measurement current() const {
        return last;
    }

    Subscription subscribe(Listener listener) {
        return listeners.insert(listeners.end(), std::move(listener));
    }

    void unsubscribe(Subscription subscription) {
        listeners.erase(subscription);
    }

    Measurement publish(std::string sensor, double value) {
        last = Measurement{last.sequence + 1, std::move(sensor), value};
        for (const auto& listener : listeners) {
            listener(last);
        }
        return last;
    }

private:
    Measurement last{1, "temperature", 23.5};
    std::list<Listener> listeners;
};

static bool acceptsEventStream(const std::shared_ptr<Request>& req) {
    return web::http::ciEquals(req->get("Accept"), "text/event-stream");
}

static void sendMeasurement(const std::shared_ptr<Response>& res,
                            const Measurement& measurement) {
    res->sendFragment("event: measurement");
    res->sendFragment("id: " + std::to_string(measurement.sequence));
    res->sendFragment("data: " + measurement.toJson().dump());
    res->sendFragment("");
}

int main(int argc, char* argv[]) {
    express::WebApp::init(argc, argv);

    MeasurementPublisher measurements;
    const WebApp app("legacy");

    app.get("/events", [&measurements](const std::shared_ptr<Request>& req,
                                        const std::shared_ptr<Response>& res) {
        if (acceptsEventStream(req)) {
            res->set("Content-Type", "text/event-stream")
               .set("Cache-Control", "no-cache")
               .set("Connection", "keep-alive")
               .sendHeader();

            if (const Measurement current = measurements.current(); current.sequence > 0) {
                sendMeasurement(res, current);
            }

            const auto subscription = measurements.subscribe([res](const Measurement& measurement) {
                sendMeasurement(res, measurement);
            });
            res->getSocketContext()->setOnDisconnected([&measurements, subscription] {
                measurements.unsubscribe(subscription);
            });
        } else {
            res->status(406).send("SSE requires Accept: text/event-stream");
        }
    });

    app.post("/simulate", [&measurements](const std::shared_ptr<Request>&,
                                          const std::shared_ptr<Response>& res) {
        const Measurement measurement = measurements.publish("temperature", 24.0);

        res->set("Content-Type", "application/json")
           .send(measurement.toJson().dump());
    });

    app.listen([](const SocketAddress& socketAddress,
                  const core::socket::State&) {
        snode::log::application().trace() << "SSE server listening on " << socketAddress.toString();
    });

    return express::WebApp::start();
}
```

The `Measurement` type and the `measurements` publisher are application code, not special SSE machinery. The SNode.C-specific shape is the HTTP route and response handling. The small `acceptsEventStream(...)` helper keeps request validation visible, and `sendMeasurement(...)` centralizes the event-stream record shape. The teaching route deliberately accepts only an `Accept` field whose entire value equals `text/event-stream`, ignoring case. It rejects other values with an ordinary HTTP response. This is a restricted example contract, not a general media-range negotiation algorithm: wildcard values, lists, and parameters such as `q=0` do not enter the streaming path. Notice that the SSE field strings themselves do not contain line endings; the empty fragment marks the blank line between events.

After `sendHeader()`, the route writes records without ending the response. It stays open until application shutdown or a detected disconnect.

The subscription is a `std::list` iterator, a handle to exactly one stored callback. Inserting or removing another listener does not invalidate it. The publisher and the connection callbacks run on the event-loop thread, and the publisher in `main()` lives until that loop has stopped. These are the lifetime assumptions of this small example; it is not a thread-safe observer library.

The ownership path is short. The publisher holds the listener, and the listener's shared pointer keeps the response facade alive while events may be sent. The existing HTTP socket context receives a disconnect callback through `setOnDisconnected(...)`. That callback removes the subscription exactly once and releases the listener's response reference. It captures the subscription handle and the publisher, not another owning response pointer. No new measurement is needed to make cleanup happen.

The framework disconnects the underlying response before invoking these registered context callbacks. Removal therefore belongs to connection teardown, including a locally detected connection error. It does not mean that the server instantly knows about a peer that disappears without a detectable transport event. The ordinary connection timeout policy still matters. The example's listeners only send a measurement; they do not mutate the listener list during publication.

### The EventSource client

The corresponding client side enters through the concrete EventSource wrapper for the selected HTTP client stack. A compact IPv4 legacy client looks like this:

<!-- snodec-source: companion/examples/SSE-EventSource-Client/main.cpp -->
```cpp
#include <core/SNodeC.h>
#include <net/in/SocketAddress.h>
#include <web/http/legacy/in/EventSource.h>
#include <Log.h>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const net::in::SocketAddress address{"127.0.0.1", 8080};

    auto events = web::http::legacy::in::EventSource("http", address, "/events");

    events->onOpen([] {
        snode::log::application().trace() << "SSE stream opened";
    });

    events->onMessage([](const web::http::client::tools::EventSource::MessageEvent& event) {
        snode::log::application().trace() << "message: " << event.data;
    });

    events->addEventListener(
        "measurement",
        [](const web::http::client::tools::EventSource::MessageEvent& event) {
            snode::log::application().trace() << "measurement: " << event.data;
        });

    events->onError([] {
        snode::log::application().error() << "SSE stream error";
    });

    return core::SNodeC::start();
}
```

The server-side route produces event-stream syntax. The client-side `EventSource` parses that stream, applies retry and continuity rules, and dispatches ordinary `MessageEvent` callbacks. `readyState()`, `retry()`, `lastEventId()`, and `close()` remain the client-side controls for observing and steering that stream lifecycle. The matching companion programs are `SSE-Server` and `SSE-EventSource-Client`.


\index{EventSource@\texttt{EventSource}!client abstraction}
\index{ReadyState@\texttt{ReadyState}}
\index{MessageEvent@\texttt{MessageEvent}}


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


SSE is not a one-shot request. It has a lifecycle, and the client-side `EventSource` ready-state model expresses that lifecycle:

| Ready state | Meaning |
|---|---|
| `CONNECTING` | the stream is not open yet or is reconnecting |
| `OPEN` | the event stream is active |
| `CLOSED` | the application has closed it or it will not reconnect |


The `MessageEvent` object is the semantic lift from SSE wire fields to application meaning. It contains exactly the kind of information the application normally needs:

| Field | Meaning |
|---|---|
| `type` | `"message"` or a custom event type |
| `data` | event payload |
| `lastEventId` | event ID associated with this event |
| `origin` | stream origin |

Applications normally react to `MessageEvent`, rather than parsing raw event-stream lines themselves.


Named events go to listeners registered for that type; only events of type `"message"` go to `onMessage(...)`. The example's `measurement` listener therefore receives its updates.


`close()` marks the client `CLOSED`, disables retry/reconnect, and shuts down the connection's write side when present. Intentional shutdown must remain distinguishable from a recoverable interruption.

### Request validation and event parsing

\index{SSE!HTTP request setup}
\index{event-stream validation}


Even though the application eventually receives events, SSE starts as HTTP. The client sends a request for the event-stream endpoint.

A simplified request shape is:

```text
GET /events HTTP/1.1
Accept: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```


The client should not treat every HTTP response as an event stream. It validates that the response is actually a server-sent event stream.

The client checks that the response Content-Type contains `text/event-stream`. Failed validation closes the socket context and invokes the error callback instead of interpreting an unrelated page as events.


\index{SSE!parsing}
\index{event stream fields}
\index{blank-line dispatch}


The parser accumulates incoming bytes into lines, interprets fields, and dispatches on a blank line.


| Field | Effect |
|---|---|
| `data` | append value plus newline to the accumulated payload |
| `event` | set custom event type |
| `id` | update the ID buffer if the value contains no NUL byte |
| `retry` | update retry timing if the value is numeric |
| blank line | dispatch accumulated event |
| comment line | ignored |

Multiple `data:` lines belong to the same event until a blank line dispatches it. The default event type is `"message"` when no custom `event:` field is present. The `id:` field participates in continuity. The `retry:` field participates in reconnection timing.


Before dispatch, the trailing newline added by `data:` accumulation is removed. If there is no accumulated data, no message event needs to be delivered. This keeps event dispatch tied to the SSE wire format.


A long-lived stream must not allow unbounded pending data. The implementation applies finite limits to pending lines and accumulated data, so a malformed or hostile long-lived stream cannot grow parser state without bound. If parsing fails, the stream can be closed.


### Resource policy for an open event stream

\index{SSE!resource limits}
\index{SSE!backpressure}

An event stream passes through more than one resource boundary. The HTTP client validates the response headers under the shared parser policy from Chapter 16. Once a valid EventSource response switches to the raw event receiver, the HTTP body parser no longer accumulates that stream. Its `maximum-body-bytes` setting is therefore not a lifetime byte budget for SSE. Header limits still apply.

This exception is intentional. A successful event stream can remain open while it delivers an unbounded number of individually bounded events. The EventSource receiver's line and accumulated-event guards protect local parsing; they do not define how many events the application may retain, how much history it should replay, or how long an observer may remain attached.

The server has a different pressure boundary. Its response fragments pass through the connection's write queue. A finite `maximum-write-queue-bytes` and the queue watermarks belong to the connection configuration described in Chapter 15. They do not turn a callback-driven measurement publisher into a source that automatically pauses whenever a browser is slow. Automatic source suspension applies to attached `core::pipe::Source` objects; a publisher that invokes response methods directly still needs its own slow-observer policy.

For the compact example, the important distinction is between the accepted measurement and its delivery to one observer. A stalled observer must not become the owner of application state. A deployment can deliberately disconnect a slow observer, retain a bounded replay history, or reduce the update rate. Those are application choices around the framework's queue contract, not new SSE syntax.

After a disconnect or queue-admission failure, event delivery remains uncertain. Event IDs provide a continuity mechanism when the application supplies a corresponding replay policy. They are not delivery acknowledgements. Tests should observe the emitted stream and the reconnect behavior separately from the model's decision to accept a measurement.

### Retry and continuity

\index{SSE!retry}
\index{retry field}
\index{Last-Event-ID}


SSE retry information updates the underlying client reconnect/retry configuration introduced in Chapter 15.


A server may send a `retry:` field. The value is interpreted as a retry interval. When accepted, it updates the EventSource retry value and the underlying client reconnect/retry timing.

`retry:` carries event-stream protocol information that updates the client-side recovery interval; it is not a generic transport timeout. The SSE value is expressed in milliseconds; the underlying client configuration receives the corresponding seconds value.


The `id:` field updates the client-side event ID buffer. When an event is dispatched, the last event ID can be remembered.

When a new request starts and a last event ID is known, the client sets:

```text
Last-Event-ID: ...
```

on the request. This gives the server a continuity hint after reconnect. The exact server behavior depends on the application, but the client-side mechanism is important: it lets an event stream carry continuity information across interruptions.


On interruption, a stream that is not `CLOSED` returns to `CONNECTING`, clears parsing buffers, reports the error, and reapplies recovery timing. Intentional close leaves it `CLOSED` with retry and reconnect disabled.

### Routes, diagnostics, and local observation

\index{SSE!Express routes}
\index{streaming endpoints}


An SSE endpoint shares the application’s routing and authorization boundary with its other HTTP endpoints. Decide access before sending the event-stream header. Once the stream has begun, the route cannot answer a later application error by starting an unrelated ordinary JSON response on that same response object.

For a dashboard, SSE plus ordinary POST requests can be a clearer division than a bidirectional channel: one path observes accepted state, another requests a change. WebSocket becomes useful when both directions need an ongoing message conversation. The decision depends on interaction and recovery requirements, not on a ranking of protocol sophistication.


SSE is high-level event-stream behavior, but it is still a long-lived HTTP response over a lower connection. Operationally, the relevant evidence is layered: connection establishment, response validation, transition to `OPEN`, parser errors, retry interval, last event ID, disconnects, and intentional close.

That connects directly to the diagnostic model from Chapter 13 and the configuration/timing model from Chapter 15. SSE does not need a new operational philosophy; it applies the existing one to a long-lived HTTP stream.


A live dashboard should distinguish a quiet source from a broken observation channel. A source can be quiet while the transport is healthy, and a newly opened stream may have no replay of missed measurements. Expose the last accepted measurement and stream state separately when that distinction matters to the reader of the dashboard.

For this example, reconnect observes the current measurement when one exists. It does not replay an event history from `Last-Event-ID`. To add replay, the application would need a bounded history and a policy for an ID older than that history; sending IDs alone does not provide either.

Subscriber lifetime is tied to the HTTP connection through the explicit unsubscribe path shown above. During a quiet period, closing an observer still removes its callback when the runtime handles the disconnect. Repeated connections therefore do not accumulate obsolete response owners until a later measurement. The remaining application choices concern live observers: how many to admit, how to deal with a slow peer, and whether to retain event history.

Start `sse-server legacy local --host=127.0.0.1 --port=8080`. Keep `curl -N -H 'Accept: text/event-stream' http://localhost:8080/events` open and send `curl -X POST http://localhost:8080/simulate` from another terminal. The JSON response and next event describe the same accepted measurement. Repeat the stream request with `Accept: text/event-stream;q=0`: this example returns 406. Disconnect during a quiet period and trace the context callback to `unsubscribe(...)`; cleanup does not require another measurement.


\index{EventSource@\texttt{EventSource}!public surface}


Client-side EventSource code includes the EventSource abstraction it names. For the IPv4 legacy wrapper, that front door is:

```cpp
#include <web/http/legacy/in/EventSource.h>
```

Server-side SSE remains an HTTP or Express route that validates the request and streams `text/event-stream` response fragments. Chapter 25 summarizes the broader component/header mapping.

::: {.snodec-remember title="What to remember"}
- One HTTP response can carry many server-to-client events; a blank line ends a record.
- The server route writes fields; the EventSource client dispatches typed `MessageEvent` objects.
- An observer subscription must end when its response disconnects, including during idle periods.
- Parser limits, write-queue limits, and retained application history govern different resources.
- Retry can reconnect; replay requires an application history and gap policy.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Trace the response reference from subscription to disconnect. Why must cleanup work when no new measurement arrives?
2. **Review (O1).** What ends an SSE record, and how do its event type, ID, and data reach the client?
3. **Lab (O2).** Build and run the SSE solution. Open an observer, call `/simulate` twice, and compare each event ID and JSON payload with its POST response. Reconnect with an older `Last-Event-ID`: expect only the current measurement, not a replay. Also verify the example rejects `text/event-stream;q=0`.
4. **Lab (O2).** Build the server and run the observers lab. Connect two streams, simulate once, then close one and simulate again. Expect identical first events and a second event on the remaining stream.
5. **Design (O3).** Choose a slow-observer and replay policy for a dashboard that may disconnect for ten minutes. State bounds, the response to an expired ID, and what the UI shows while disconnected.

Public solutions and lab commands: `companion/exercises/ch18/README.md`.
:::
