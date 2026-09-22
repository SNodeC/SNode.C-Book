## Core Runtime and Event Processing

\index{core runtime}
\index{event processing}
\index{event-driven runtime}


### Why this chapter matters

The runtime is where the model becomes observable. Descriptors become ready, timers expire, queued work runs, callbacks fire, and connection objects advance without each application inventing its own event loop.

That model is necessary, but it still leaves an important question open.

**How does the framework actually keep everything moving?**

A server can register an intention to listen. A client can register an intention to connect. A context can define reactions such as `onConnected()` and `onReceivedFromPeer()`. A timer can be armed. A descriptor can become readable. A timeout can expire. Something has to coordinate all of that.

That “something” is the runtime core. This chapter therefore moves from application shape to runtime machinery. It stays close to the SNode.C source structure, but it describes that structure in a teaching-oriented way: as a small number of cooperating runtime concepts.

The key insight is this:

> SNode.C does not treat event processing as a hidden implementation detail. It gives it a clear architecture.

That architecture has several visible pieces:

- `core::SNodeC` as the public runtime control surface,
- `core::EventLoop` as the singleton orchestrator,
- `core::EventMultiplexer` as the waiting and dispatch backbone,
- descriptor event publishers and receivers for file-descriptor activity,
- timer publishers and timer handles for scheduled activity,
- and an event queue for deferred execution.

Once those pieces are placed correctly in the reader's mind, the framework's behavior stops feeling magical. Registered instances are not advanced by scattered blocking calls. They are advanced by a coordinated event-processing core.

### The runtime picture in one diagram

Before looking at the individual parts, it helps to place the event-processing core in one visual model. As shown in Figure \ref{fig:snodec-event-runtime}, the public runtime surface leads into the event loop and multiplexer, which coordinate descriptor readiness, timers, queued work, and dispatch.

![The SNode.C event-processing core connects runtime control, descriptor readiness, timers, queued work, and protocol dispatch.](assets/figures/pdf/fig-03-event-runtime-picture.pdf){#fig:snodec-event-runtime width=88% latex-placement="tbp"}

The figure is an orientation map. It places the major runtime ideas in relation to each other while leaving implementation order, call paths, and lower-level scheduling details to the source code.

The application normally talks to `core::SNodeC`. `core::SNodeC` forwards runtime control to the event loop. The event loop delegates low-level waiting and dispatch coordination to the multiplexer. The multiplexer brings together descriptor readiness, timers, queued events, timeout processing, signals, and cleanup.

That is the backbone of the chapter.

### A short source-level reading

\index{source-level reading}
\index{SNode.C!source reading}


The implementation follows the same structure. The excerpts below are abridged from the pinned SNode.C `2.0.0` source in `src/core/SNodeC.cpp`, `src/core/EventLoop.cpp`, and `src/core/EventMultiplexer.cpp`. They are not a second model of the runtime; they are source anchors for the model used in this chapter.

First, the public facade really is a facade. `core::SNodeC` forwards runtime control to `core::EventLoop`:

```cpp
int SNodeC::start(const utils::Timeval& timeOut) {
    return EventLoop::start(timeOut);
}

TickStatus SNodeC::tick(const utils::Timeval& timeOut) {
    return EventLoop::tick(timeOut);
}

State SNodeC::state() {
    return EventLoop::getEventLoopState();
}
```

Second, `EventLoop::start(...)` bootstraps configuration, enters the running state, and then advances the runtime through repeated calls to `_tick(...)` while the loop remains active:

```cpp
if (utils::Config::bootstrap()) {
    eventLoopState = State::RUNNING;

    do {
        tickStatus = EventLoop::instance()._tick(timeOut);
    } while ((tickStatus == TickStatus::SUCCESS || tickStatus == TickStatus::INTERRUPTED) &&
             eventLoopState == State::RUNNING);
}
```

Third, a multiplexer tick has the expected coordination shape: wait, publish active work, execute queued work, check timeouts, and release expired resources:

```cpp
const TickStatus tickStatus = waitForEvents(...);

if (tickStatus == TickStatus::SUCCESS) {
    spanActiveEvents(...);
    executeEventQueue(...);
    checkTimedOutEvents(...);
    releaseExpiredResources(...);
}
```

Those excerpts are deliberately small. They show that the diagram's main path is not only a teaching abstraction: facade, event loop, multiplexer, descriptor readiness, timers, queued work, timeout handling, and cleanup are visible as source-level responsibilities.

### The public runtime surface: `core::SNodeC`

\index{core::SNodeC@\texttt{core::SNodeC}}
\index{runtime facade}


The first runtime-facing type most users encounter is `core::SNodeC`.

Its public surface is small:

- `init(int argc, char* argv[])`
- `start(const utils::Timeval& timeOut = {LONG_MAX, 0})`
- `reconfigure()`
- `stop()`
- `tick(const utils::Timeval& timeOut = 0)`
- `free()`
- `state()`

This compact interface already teaches several important things.

The current source also makes configuration reapplication an explicit runtime operation. `reconfigure()` is called on the event-loop thread while the state is `RUNNING`; it returns whether reapplication succeeded. It does not repeat process startup or restart sockets, and failed parsing does not promise to roll back settings already changed. Chapters 16 and 17 distinguish this operation from initial configuration and from an application's separate decision to reactivate an endpoint.

#### The runtime has explicit phases

\index{runtime phases}
\index{init()@\texttt{init()}}
\index{start()@\texttt{start()}}
\index{stop()@\texttt{stop()}}


The existence of `init`, `start`, `stop`, `free`, and `state` tells us that the framework runtime has an explicit lifecycle instead of being a side effect of object construction.

That is a design strength. It reduces ambiguity for applications and gives the reader a stable mental timeline. A typical application does not simply create a server and hope that background machinery appears. It initializes the framework, registers communication roles, and then starts the runtime.

#### Event-loop control is centralized

The existence of `start()` and `tick()` tells us that SNode.C treats the event loop as a central framework capability rather than as behavior buried inside one particular server or client type.

That means sockets, timers, retries, reconnects, and protocol contexts participate in one runtime. A `SocketServer` is not an independent miniature event loop. A `SocketClient` is not an independent miniature event loop. Both register work that is advanced by shared runtime machinery.

#### `start()` is the normal ownership mode

For most applications, `core::SNodeC::start()` is the normal mode. It means:

> Let the SNode.C runtime run the event loop until it is stopped, has no remaining observed work, or encounters a terminating tick result.

That is the style already used in the echo pair. It is the natural mode when SNode.C is the central network runtime of the process.

The `timeOut` argument limits a multiplexer wait within an iteration. It is not a total running-time budget for the application. The multiplexer takes the earlier of that bound and its next scheduled timeout, then the loop can continue with another iteration. A service deadline therefore needs its own application or timer policy; passing a short wait bound does not make the service stop after that interval.

#### `tick()` and the current stepping contract

\index{tick()@\texttt{tick()}}
\index{controlled stepping}


The public surface also declares `tick(...)`. Its name suggests controlled stepping, which is useful when reasoning about individual event-loop iterations, testing, or embedding a reactor in another outer loop. The source contract must be checked before treating that declaration as a working alternative to `start()`.

In the source tree recorded for this edition, the public `EventLoop::tick(...)` path calls `_tick(...)` while the state is `INITIALIZED`, whereas `_tick(...)` dispatches the multiplexer only in `RUNNING` or `STOPPING`. That means an ordinary `init()` followed by public `tick()` must not be presented as an equivalent way to advance the examples. The working startup path used throughout this book is `start()`, which bootstraps configuration and enters `RUNNING`. Internal tick structure explains how the runtime progresses; it does not by itself establish a supported external-loop recipe.

### The orchestrator behind the facade: `core::EventLoop`

\index{core::EventLoop@\texttt{core::EventLoop}}
\index{event loop}


Although most application code touches `core::SNodeC`, the actual loop orchestrator is `core::EventLoop`.

Its interface exposes several key facts:

- it is a singleton through `instance()`,
- it owns or exposes an `EventMultiplexer`,
- it tracks a tick counter,
- it tracks runtime state,
- and it is the actual home of `init`, `tick`, `start`, `stop`, and `free`, with `SNodeC` acting as the public facade.

This is a useful separation in a systems framework. The application sees a compact facade. The runtime internals still have a concrete orchestrator object.

That separation keeps everyday use simple without flattening the underlying architecture.

#### Why a singleton event loop makes sense here

The singleton event loop is a tradeoff.

On the positive side, it gives the framework one primary event domain per process. That simplifies ownership, coordination, and runtime reasoning. For the applications emphasized in this book, that is helpful: the reader does not need to imagine several unrelated event loops competing inside the same process. There is one central runtime story.

The tradeoff is shared scheduling pressure. A slow callback delays other roles in the same process, even if their protocols are otherwise independent. Separate processes provide independent event domains and failure containment, at the cost of communication, deployment, and state coordination between them. Several roles in one loop are attractive when their callbacks stay short and they benefit from a shared model; process separation becomes more attractive when they need different resource or recovery policies. Chapter 30 returns to that system-level choice.

The examples keep endpoint operations, flow control, and model updates on that event-loop thread. A shared pointer extends an object's lifetime; it does not make concurrent access to that object safe. Expensive computation and blocking external APIs need a deliberate handoff if they are moved elsewhere. Do not call connection or controller methods from a worker merely because that worker can hold a pointer. The current flow controllers retain the event-loop-thread usage contract, and a separate-thread integration needs an explicitly supported way to return work to that thread.

### Runtime state is coarse on purpose

\index{runtime state}


The `core::State` enum is small:

- `LOADED`
- `INITIALIZED`
- `RUNNING`
- `STOPPING`

At first glance, this may seem too simple. For operational reasoning, it is useful precisely because it is coarse. It gives the framework a phase language without turning ordinary users into internal state-machine archaeologists.

A reader can think in a clean timeline:

1. the framework is loaded,
2. it is initialized,
3. it is running,
4. it is stopping.

That is enough to reason about many important behaviors. Server and client flows are not isolated library calls. They integrate with runtime state. A listen or connect flow can only move forward meaningfully when the runtime is in a phase where such work can be processed.

### Tick-by-tick execution and `TickStatus`

\index{TickStatus@\texttt{TickStatus}}
\index{event loop!tick cycle}


If `State` describes coarse lifecycle phases, `TickStatus` describes the result of a single event-loop iteration.

`TickStatus` defines:

- `SUCCESS`
- `INTERRUPTED`
- `NOOBSERVER`
- `TRACE`

This enum is more informative than it may first appear.

`SUCCESS` is the normal iteration result. It does not, by itself, prove that a callback ran or a descriptor was dispatched. In particular, the public stepping limitation described above means that an initialized loop can return this result without advancing the multiplexer.

`INTERRUPTED` matters because an event loop can be interrupted by signals or other control conditions. Exposing this as a separate status keeps interruption explicit instead of silently collapsing it into generic success or failure.

`NOOBSERVER` is architecturally revealing. It says that the event-loop iteration can recognize the absence of observed runtime participants. Descriptor receivers, timers, and queued work form a population of things the runtime can observe or advance. The runtime therefore manages a set of event participants rather than looping blindly.

`TRACE` is part of the per-tick vocabulary, but it should not be mistaken for a full tracing subsystem. The important point for this chapter is narrower: per-tick outcomes are explicit enough to be named and propagated.

That is a useful rule for reading the core runtime:

> Header names reveal design vocabulary, but the architectural meaning should be taken from how the pieces cooperate.

### From handles to runtime-visible instances

Chapter 5 separated the application-side handle from the runtime-visible instance.

That distinction becomes concrete in the stream server and client code. The local `SocketServer` or `SocketClient` object used in application code names and configures a communication role. Each explicit `listen(...)` or `connect(...)` creates a controller for that call. Scheduled callbacks retain the controller together with the shared endpoint configuration and context. The current source therefore has one configured endpoint that can participate in several independent activation flows, rather than one endpoint-wide controller reused for every explicit call.

The application begins with local expressions such as:

```cpp
server.listen(...);
client.connect(...);
```

But the runtime story does not stop on that stack frame. The public call enters the real listen/connect path, that path uses the flow controller, and the flow controller schedules the actual work for an event-loop turn.

For stream servers and clients, the practical path is:

```text
listen(...) / connect(...)
  -> realListen(...) / realConnect(...)
      -> flowController.startFlow(...)
          -> EventReceiver::atNextTick(...)
```

The scheduling boundary has a lifetime consequence. The server and client templates capture shared endpoint state in the work that will run later, so returning from the public call does not discard the configuration and factory needed by that flow. An application callback that captures a separate local object by reference needs its own lifetime argument; the framework's retained state does not make every capture safe.

### From runtime intent to event delivery

\index{event delivery}
\index{runtime intent}


To understand event processing, we need to distinguish between two different meanings of “event” in SNode.C:

- a **runtime scheduling event**,
- and a **descriptor or timer readiness event**.

These are related, but not identical.

#### Scheduling events

The `core::EventReceiver` API makes one important mechanism directly visible:

```cpp
core::EventReceiver::atNextTick(...);
```

This is the framework's way of saying:

::: {.snodec-warning title="Deferred-work warning"}
Do not do this immediately on the caller's stack. Queue it for an event-loop turn.
:::

The implementation creates a temporary event receiver, spans it into the event system, invokes the stored callback from `onEvent(...)`, and destroys the temporary receiver after execution. The exact caller path depends on the surrounding flow, but the architectural meaning is stable: operational work can be moved into the runtime domain instead of being executed immediately by arbitrary user call stacks.

That produces cleaner phase boundaries and more predictable sequencing.

#### Readiness events

A descriptor may become readable, writable, exceptional, or timed out. A timer may expire. A signal may arrive. These are not “next-tick callbacks” in the same sense. They are external or scheduled conditions that the runtime notices and then dispatches.

So the mental model should be:

- `atNextTick(...)` is how framework or user code can enqueue work into the loop;
- descriptor and timer mechanisms are how the loop notices the outside world and scheduled time.

Both meet in the same runtime, but they enter it through different doors.

### `EventReceiver` and `Event`: the small but important abstraction pair

\index{EventReceiver@\texttt{EventReceiver}}
\index{Event@\texttt{Event}}


The `EventReceiver` and `Event` headers are compact, but together they reveal a lot about the runtime's shape.

An `EventReceiver`:

- has a name,
- exposes `onEvent(const utils::Timeval& currentTime)`,
- can `span()` and `relax()`,
- and supports `atNextTick(...)`.

An `Event`:

- is associated with an `EventReceiver`,
- has a name,
- can `span()` and `relax()`,
- can be `dispatch(...)`,
- and is connected to the `EventMultiplexer`.

The cleanest way to think about this pair is:

- the **receiver** is the runtime-facing behavior endpoint;
- the **event** is the thing that becomes queued and dispatched for that receiver.

That is a useful split. It means SNode.C can talk about *who handles work* and *what gets published into the loop* as related but distinct concepts.

#### What `span()` and `relax()` do

`EventReceiver` delegates these operations to its event. In `Event::span()`, a published flag prevents the same event from being inserted repeatedly while it is already queued. `relax()` removes a published event; dispatch clears that flag before calling the receiver. This is more precise than treating an event as an unbounded count of callback requests. Repeated publication of one already-published event is not a request for several independent invocations.

Read that rule beside `atNextTick(...)`: each call to that helper constructs a separate temporary receiver. Two helper calls therefore create two event objects, whereas calling `span()` twice on one already-published receiver addresses the same event. The distinction matters when reasoning about deferred work and cancellation.

### The multiplexer is the coordination backbone

\index{EventMultiplexer@\texttt{EventMultiplexer}}
\index{multiplexer}
\index{event queue}


At the center of event processing sits `core::EventMultiplexer`. This is the most important internal runtime concept in this chapter.

A good teaching summary is:

> One tick is the multiplexer coordinating descriptor readiness, timers, queued events, timeout processing, signals, and cleanup.

The multiplexer is the runtime hub that combines several kinds of progress into one coordinated event-loop iteration, rather than a thin wrapper around `epoll`, `poll`, or `select`.

Its structure shows that it:

- owns access to three descriptor event publisher channels,
- owns a timer event publisher,
- maintains an internal event queue,
- supports spanning and relaxing events,
- can receive signals and termination requests,
- computes timeouts,
- waits for events,
- spans active events,
- executes the event queue,
- checks timed-out events,
- and releases expired resources.

That is a richer mental picture than “the multiplexer waits for file descriptors.”

#### Why there are three descriptor channels

The multiplexer distinguishes three descriptor categories:

- `RD`
- `WR`
- `EX`

These correspond to readable, writable, and exceptional descriptor activity. The runtime does not treat all descriptor activity as one undifferentiated stream. It keeps distinct observation channels for the major categories of interest.

That matters for network systems because read readiness, write readiness, and exceptional conditions often mean different things. A readable socket may allow protocol input processing. A writable socket may allow queued output to drain. An exceptional condition may require error handling or shutdown.

Keeping these channels distinct makes the runtime more expressive.

#### The event queue inside the multiplexer matters

The embedded `EventQueue` inside `EventMultiplexer` is especially revealing. It has operations for insertion, removal, execution, and clearing. It also uses separate publish and execute queues.

The architecture tells us that queued event work is a first-class part of a loop tick, not an ad-hoc side mechanism. This helps explain why `atNextTick(...)` can be such a clean primitive: there is a defined place in the loop structure for queued runtime work.

#### Multiplexer implementations are replaceable at the lower level

The conceptual role of the multiplexer is stable, but the concrete waiting mechanism can vary. The source tree separates lower-level multiplexer backends for mechanisms such as `epoll`, `poll`, and `select`.

For the reader, the goal is not to memorize a backend first, but to understand the architectural contract:

> The multiplexer is the place where observed descriptors, timers, queued work, timeout processing, signals, and cleanup meet.

That contract is what later socket and protocol layers rely on.

### Observed event sources

Once the multiplexer is understood as the coordination backbone, the next question is:

> What exactly does it observe?

For this chapter, the two most important groups are descriptor event sources and timer event sources.

Descriptor event sources connect the runtime to file descriptors. Timer event sources connect the runtime to scheduled time. Both are managed as runtime participants, not as unrelated utilities.

### Descriptor event publishers: managing observed descriptor populations

\index{descriptor events}
\index{descriptor publishers}


A descriptor event publisher manages a population of observed descriptor receivers.

It can:

- `enable(...)`
- `disable(...)`
- `suspend(...)`
- `resume(...)`
- `spanActiveEvents()`
- `checkTimedOutEvents(...)`
- `releaseDisabledEvents(...)`
- `signal(...)`
- disable the whole publisher

It also maintains maps of observed receiver lists keyed by descriptor.

This is a strong clue about the internal runtime philosophy. SNode.C does not think of descriptor handling merely as:

> The loop calls my callback when `fd` is ready.

Instead, it thinks in terms of **managed observed populations**.

Receivers can become observed, temporarily suspended, resumed, timed out, disabled, or released. This is a more operationally mature model than a naive reactor sketch.

#### Why suspend/resume is different from enable/disable

Even without walking through every implementation detail, the distinction between suspend/resume and enable/disable is conceptually valuable.

- **enable/disable** suggests entering or leaving the observed population;
- **suspend/resume** suggests remaining conceptually present while temporarily inactive.

That distinction becomes important in real systems where backpressure, staged activity, retry delays, or temporary quiescence must be represented cleanly. A receiver may still exist as part of the runtime model even when it is not meant to produce events for a while.

\SNodeCNextSectionMark{6.14. DESCRIPTOR EVENT RECEIVERS}

### Descriptor event receivers: behavior attached to observed descriptors

\index{descriptor receivers}
\index{event receivers}


If publishers manage descriptor-facing populations, receivers express the behavior of one observed descriptor participant.

A descriptor receiver:

- derives from `EventReceiver`,
- knows whether it is enabled or suspended,
- can be enabled on a file descriptor,
- can be disabled, suspended, and resumed,
- can have timeout behavior,
- and must implement runtime reactions such as `dispatchEvent()`, `timeoutEvent()`, and `signalEvent(int)`.

This tells us how the descriptor side of the runtime fits together.

A descriptor receiver is not “just a callback object.” It is a runtime participant with observation state, timeout state, signal behavior, and dispatch behavior. That is why the framework can support a wide range of connection and socket workflows while still feeling regular. The same basic runtime pattern is reused with different specialized receivers.

#### Publisher and receiver side by side

A small table helps to keep the distinction clear.

| Runtime object | Main responsibility | Simple mental rule |
|---|---|---|
| `DescriptorEventPublisher` | Manages the observed population for a descriptor channel | Decides *who is being observed* |
| `DescriptorEventReceiver` | Defines behavior for one observed descriptor participant | Decides *what happens when observation produces work* |

This distinction will matter again when socket acceptors, connectors, readers, and writers enter the picture. They are specialized runtime participants managed by the event system, not anonymous callbacks attached to file descriptors.

### Timers are not bolted on

\index{timers}
\index{event loop!timers}


A good runtime design treats timers as first-class event sources. SNode.C does exactly that.

The `TimerEventPublisher` maintains a timer set, supports insertion and removal, computes the next timeout, spans active events, and can stop the timer publisher itself.

The `core::Timer` base class is a small ownership-oriented handle around a timer event receiver. It offers operations such as `cancel()` and `restart()`. On top of that, `core::timer::Timer` provides concrete creation helpers such as:

- `intervalTimer(...)`
- `singleshotTimer(...)`

This means the timer story fits naturally into the broader runtime story. A timer participates in the loop's own scheduled event fabric rather than living as a foreign utility outside the event loop.

#### Timers share the same central loop worldview

A timeout fits the same runtime model: another kind of event source participating in the same tick progression.

The multiplexer computes timeout information together with descriptor observation and queued event work. That is why time-based behavior can be integrated without inventing a second scheduler beside the event loop.

#### Retry and reconnect features fit naturally

Chapter 5 introduced retry and reconnect behavior as operational concerns of configured instances. In the stream flow-controller path, that now becomes concrete. Retry and reconnect need time, and the runtime already has first-class timer support.

Therefore retries and reconnects do not need to be improvised as sleeps, blocking loops, or external threads. They can be represented as scheduled runtime work that belongs to the same event-loop world as descriptor activity and callbacks.

This is the architectural reason why retry, reconnect, and timeout behavior feel like part of SNode.C rather than add-ons.

### One tick, conceptually

\index{event loop!tick cycle}
\index{timeouts}
\index{event loop!cleanup}


With the main pieces now placed, we can describe one conceptual event-loop iteration. This is not a line-by-line implementation trace. It is the teaching model that best fits the implementation structure.

Read the following sequence against `EventMultiplexer::tick()`. Its successful path publishes active work, executes the queue, checks descriptor timeouts, and releases expired resources. This order explains why a long callback can delay more than the next read: timeout processing and cleanup also wait for control to return.

#### The loop begins a tick

The event loop begins one internal iteration with a bound on its wait. In the examples, `start()` supplies the running state and repeats these iterations. This description concerns that internal cycle; the public `tick()` declaration does not remove the state restriction described earlier.

#### The multiplexer determines what to wait for

The multiplexer considers descriptor activity and timer deadlines. It computes the next relevant timeout and prepares to monitor the registered descriptor sources. This is where descriptor observation and timer observation meet.

#### External readiness or timer expiration occurs

Descriptors may become readable, writable, exceptional, or timed out. Timers may become due. Signals may arrive. The runtime now has work to publish or dispatch.

#### Active events are spanned

The multiplexer spans active events and publishes them toward the relevant receivers. The concept is stable: observed runtime participants that are ready for work are brought into the event-processing path.

#### The event queue is executed

Queued work, including next-tick callbacks and other internal runtime events, is executed. This is where scheduled framework work can run outside the original caller's stack.

It is also the reason `listen(...)` and `connect(...)` can register intent rather than doing the whole operation immediately.

#### Timeouts and cleanup are checked

The loop checks for timed-out observed entities and releases expired or disabled resources. Event-driven systems must not only react to positive readiness. They must also notice inactivity, timeout, cancellation, disablement, and cleanup.

#### The tick returns a status

The loop iteration returns a `TickStatus`.

For normal `start()` usage, this status is part of the runtime's internal loop control. Tests must observe the intended callback or data exchange as well as the return value; a status alone is not evidence that application work progressed.

### Coordinated shutdown is part of the runtime model

\index{shutdown}
\index{ShutdownContext@\texttt{ShutdownContext}}
\index{ShutdownReason@\texttt{ShutdownReason}}

Stopping the main run loop and destroying every descriptor immediately are not the same operation. Established streams can have queued output or a TLS shutdown exchange still in progress.

The current runtime carries a `ShutdownContext` through its existing ownership graph:

```text
EventLoop
  -> EventMultiplexer
      -> DescriptorEventPublisher
          -> DescriptorEventReceiver
              -> SocketConnectionT
```

`ShutdownReason::Requested`, `ShutdownReason::Signal`, and `ShutdownReason::NoObserver` retain the reason shutdown began. For an established stream, these reasons join the same bounded write-shutdown path rather than selecting unrelated cleanup mechanisms.

A stream connection has reader and writer receiver subobjects. Both can encounter the framework notification, but the complete connection coordinates the operation once. Repeated delivery must join the existing shutdown rather than duplicate a signal callback, start a second transport shutdown, or destroy a helper that is still needed to finish.

`STOPPING` therefore still contains controlled work. Read observation can remain necessary for peer EOF or TLS `close_notify`, and timeout/termination behavior bounds a peer that does not cooperate. This is continuation of cleanup, not permission for an application to start unrelated new communication.

Signal-triggered shutdown still invokes the context's `onSignal(int)` callback. Its `bool` signature remains, but during coordinated framework shutdown the result cannot veto transport cleanup. A context should perform its protocol-specific response without assuming that returning `false` can keep the framework running.

The public application control surface remains `core::SNodeC`. The graph above explains internal coordination; it does not ask an installed consumer to include private `EventLoop` or multiplexer implementation headers. Chapters 19 and 20 connect the same shutdown model to TLS, timeouts, and output pressure.

### What application authors should learn from this

This chapter has looked under the visible application API. The purpose is not to turn every application writer into a maintainer of the runtime core. The purpose is to develop the right instincts.

#### Do not block inside callbacks

Callbacks run inside the runtime's event-processing world. If a callback blocks for a long time, it prevents the runtime from processing other descriptors, timers, queued events, retries, reconnects, timeout checks, and cleanup work.

A callback should do the immediate protocol work it is responsible for, preserve its invariants, and then return control to the event loop. Long-running work must be designed carefully.

#### Treat callbacks as runtime-owned execution points

A callback is a runtime-owned execution point, not an ordinary helper function called by your own code at a predictable place on your own stack.

That means callback code should be clear about ownership, reentrancy assumptions, and the amount of work it performs before returning.

#### Use timers instead of manual sleeps

If you need to delay work, retry later, or run periodic activity, the runtime timer model is the natural place.

A manual sleep inside a callback is almost always the wrong instinct. It stops the event loop from doing the work it exists to do.

#### Remember that `listen(...)` and `connect(...)` register intent

The endpoint configuration exists before the public call creates its activation flow. The flow-controller/shared-context path and the event loop advance the actual work.

This wording marks the difference between reading SNode.C as a blocking socket wrapper and reading it as an event-driven runtime.

#### Understand where descriptor activity, timers, and queued work meet

Descriptor readiness, timer expiration, and next-tick scheduling are different sources of activity. But they meet in the same event-loop architecture.

The `EventMultiplexer` is the central place where they are coordinated. That is the core runtime picture to carry forward.

#### Distinguish internal ticks from public stepping

Most applications should simply call `core::SNodeC::start()`.

Use `start()` for the application recipes in this edition. An embedding design needs a separately established stepping contract and a test that observes actual event delivery. The current public `tick()` path does not supply that contract merely by returning a named status.

### Stable concepts versus implementation details

This chapter has intentionally stayed close to the SNode.C headers because SNode.C is a systems framework, and systems frameworks should not be taught as vague abstractions only.

Function bodies, event receiver types, and multiplexer backends may change. The architectural concepts are more durable:

- public runtime control through `core::SNodeC`,
- event-loop orchestration through `core::EventLoop`,
- multiplexing through `core::EventMultiplexer`,
- descriptor event publishers and receivers,
- timer event publishing,
- queued runtime work,
- timeout processing,
- cleanup,
- and per-tick progress.

Two stable distinctions matter especially for the rest of the book.

The first is the distinction between a handle and an instance. The server/client object is the application-side handle. The registered instance is advanced by shared runtime and flow-controller machinery.

The second is the distinction between an instance and a connection. The instance is the long-lived communication role. A connection is a concrete peer relationship that appears through runtime progress.

Those are the ideas the reader should carry forward.

As a source-reading exercise, start at the echo server's `listen(...)` call and follow the scheduled callback to the first acceptor work. Mark the point where the caller's stack stops advancing the operation. Then inspect `EventMultiplexer::tick()` and locate the work that would be delayed by a blocking receive callback. The expected result is a control-flow explanation, not just another list of classes: deferred activation reaches a shared dispatcher, and application work must return before that dispatcher can continue its other responsibilities.

::: {.snodec-remember title="What to remember"}
- `core::SNodeC` is the public runtime facade; `core::EventLoop` is the central event-loop orchestrator behind it.
- `core::EventMultiplexer` coordinates descriptor readiness, timers, queued work, timeout checks, signals, and cleanup.
- `listen(...)` and `connect(...)` do not perform the whole operation on the caller's stack; they enter the flow-controller path and schedule runtime work.
- Server/client handles register runtime roles; shared state and flow-controller machinery advance those roles after registration.
- Descriptor receivers and timer receivers are managed runtime participants with enable/disable, suspend/resume, timeout, and cleanup behavior.
- Application callbacks should return control to the event loop rather than blocking the runtime.
:::
