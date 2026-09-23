## Core Runtime and Event Processing {#core-runtime-and-event-processing}

\index{core runtime}
\index{event processing}
\index{event-driven runtime}


::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace deferred work from registration to dispatch and distinguish runtime phase from iteration status.
- **O2.** Diagnose how callback work delays descriptors, timers, timeouts, and cleanup in one event loop.
- **O3.** Implement shared measurement acceptance and remove an observer before its captured state dies.
:::

### The runtime picture and its source anchors

The runtime is where the model becomes observable. Descriptors become ready, timers expire, queued work runs, callbacks fire, and connections advance without each application inventing its own event loop. The public control surface is `core::SNodeC`; `core::EventLoop` orchestrates the loop, and `core::EventMultiplexer` coordinates waiting and dispatch.

![The SNode.C event-processing core connects runtime control, descriptor readiness, timers, queued work, and protocol dispatch.](assets/figures/pdf/fig-03-event-runtime-picture.pdf){#fig:snodec-event-runtime width=88% latex-placement="tbp"}


Figure \ref{fig:snodec-event-runtime} is an orientation map, not a promise about every internal call order. Descriptor readiness, timers, queued work, timeout processing, signals, and cleanup meet in this runtime. The source excerpts make their relationship concrete.

\index{source-level reading}
\index{SNode.C!source reading}


The implementation follows the same structure. The excerpts below are abridged from the pinned SNode.C `2.0.0` source in `src/core/SNodeC.cpp`, `src/core/EventLoop.cpp`, and `src/core/EventMultiplexer.cpp`.

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

### Public lifecycle and the stepping contract

\index{core::SNodeC@\texttt{core::SNodeC}}
\index{runtime facade}
\index{runtime phases}
\index{init()@\texttt{init()}}
\index{start()@\texttt{start()}}
\index{stop()@\texttt{stop()}}
\index{tick()@\texttt{tick()}}
\index{controlled stepping}
\index{runtime state}
\index{TickStatus@\texttt{TickStatus}}
\index{event loop!tick cycle}

The public facade provides `init(int argc, char* argv[])`, `start(const utils::Timeval& timeOut = {LONG_MAX, 0})`, `reconfigure()`, `stop()`, `tick(const utils::Timeval& timeOut = 0)`, `free()`, and `state()`. Runtime progress is explicit: initialize, register activation flows, then start processing. Constructing a server does not create an independent event loop.

For most applications, `start()` owns that progression until stopped, left without observed work, or given a terminating tick result. Its `timeOut` argument bounds a multiplexer wait within an iteration, not the application's total running time. The multiplexer takes the earlier of that bound and its next scheduled timeout, then can continue with another iteration. A service deadline needs its own timer or application policy.

In the source tree recorded for this edition, the public `EventLoop::tick(...)` path calls `_tick(...)` while the state is `INITIALIZED`, whereas `_tick(...)` dispatches the multiplexer only in `RUNNING` with no pending stop signal, or in `STOPPING`. That means an ordinary `init()` followed by public `tick()` must not be presented as an equivalent way to advance the examples. The working startup path used throughout this book is `start()`, which bootstraps configuration and enters `RUNNING`. Internal tick structure explains how the runtime progresses; it does not by itself establish a supported external-loop recipe.

The coarse runtime phases are `LOADED`, `INITIALIZED`, `RUNNING`, and `STOPPING`. They describe the framework lifecycle; a listen or connect flow can advance only when the runtime processes its work. `TickStatus` instead describes one iteration:

| Status | Interpretation |
|---|---|
| `SUCCESS` | Normal iteration result; observe a callback or byte exchange to establish application progress. |
| `INTERRUPTED` | Interruption remains explicit, including signal/control conditions. |
| `NOOBSERVER` | No observed participants remain for the runtime to advance. |
| `TRACE` | A named per-tick result, not a full tracing subsystem. |

A successful status alone is insufficient for the initialized public stepping path described above. Read header names as vocabulary and implementation cooperation as the contract.

The current source also makes configuration reapplication an explicit runtime operation. `reconfigure()` is called on the event-loop thread while the state is `RUNNING`; it returns whether reapplication succeeded. It does not repeat process startup or restart sockets, and failed parsing does not promise to roll back settings already changed. Chapter 13 distinguishes this operation from initial configuration and from an application's separate decision to reactivate an endpoint.

### One event domain and its ownership obligations

\index{core::EventLoop@\texttt{core::EventLoop}}
\index{event loop}

The application sees a compact facade; `core::EventLoop` is the singleton orchestrator behind it. It owns or exposes the multiplexer, tracks runtime state and tick count, and implements the lifecycle operations forwarded by `SNodeC`.

One event domain per process simplifies coordination and ownership, but creates shared scheduling pressure. A slow callback delays other roles even when their protocols are independent. Separate processes provide independent event domains and failure containment, at the cost of communication, deployment, and state coordination. Several roles in one loop suit short callbacks around a shared model; different resource or recovery policies can justify a process split. Chapter 26 returns to that choice.

The examples keep endpoint operations, flow control, and model updates on that event-loop thread. A shared pointer extends an object's lifetime; it does not make concurrent access to that object safe. Expensive computation and blocking external APIs need a deliberate handoff if they are moved elsewhere. Do not call connection or controller methods from a worker merely because that worker can hold a pointer. The current flow controllers retain the event-loop-thread usage contract, and a separate-thread integration needs an explicitly supported way to return work to that thread.

A callback is a runtime-owned execution point, not an ordinary helper invoked at a place chosen by the caller's current stack. Be explicit about capture lifetime, reentrancy assumptions, and the amount of work before return. The lifetime of a retained pointer and the thread allowed to use it are separate design decisions.

### From activation intent to deferred work

Chapter 4 separated the application-side handle from the runtime-visible instance.

That distinction becomes concrete in the stream server and client code. The local `SocketServer` or `SocketClient` object used in application code configures an instance. Each explicit `listen(...)` or `connect(...)` creates a controller for that call. Scheduled callbacks retain the controller together with the shared endpoint configuration and context. The current source therefore has one instance that can participate in several independent activation flows, rather than one endpoint-wide controller reused for every explicit call.

The application begins with local expressions such as:

```cpp
server.listen(...);
client.connect(...);
```

The public call reaches `realListen(...)` or `realConnect(...)`, which enters
`flowController.startFlow(...)` and schedules work through
`EventReceiver::atNextTick(...)`.

The scheduling boundary has a lifetime consequence. The server and client templates capture shared endpoint state in the work that will run later, so returning from the public call does not discard the configuration and factory needed by that flow. An application callback that captures a separate local object by reference needs its own lifetime argument; the framework's retained state does not make every capture safe.

\index{event delivery}
\index{runtime intent}

The scheduling API exposes that boundary directly:

```cpp
core::EventReceiver::atNextTick(...);
```

::: {.snodec-warning title="Deferred-work warning"}
Do not do this immediately on the caller's stack. Queue it for an event-loop turn.
:::

The implementation creates a temporary receiver, publishes its event, invokes the stored callback from `onEvent(...)`, and destroys the temporary receiver after execution. Deferral moves work into runtime progression; it does not make captured references safe automatically.

The queued-work lab records an empty trace immediately after registration. During `start()`, a callback records entry, schedules another callback, records return, and releases control. The nested callback must observe that the first is no longer active. Check those observations rather than using a successful return status as a substitute for dispatch.

### Events, receivers, and readiness

\index{EventReceiver@\texttt{EventReceiver}}
\index{Event@\texttt{Event}}

Two meanings of “event” meet in the loop. A scheduling event queues work such as `atNextTick(...)`; descriptor readiness or a timer deadline supplies a condition that the runtime notices and dispatches. Readable, writable, exceptional, timed-out, and signal-driven activity are not all next-tick callbacks, although their work enters the same runtime.

An `EventReceiver` has a name and implements `onEvent(const utils::Timeval& currentTime)`. Its associated `Event` is the queued and dispatched object connected to the multiplexer. Both expose `span()` and `relax()`: the receiver delegates them to its event. This separates who handles work from what is published for that receiver.

In `Event::span()`, a published flag prevents the same event from being inserted repeatedly while it is already queued. `relax()` removes a published event; dispatch clears that flag before calling the receiver. This is more precise than treating an event as an unbounded count of callback requests. Repeated publication of one already-published event is not a request for several independent invocations.

Read that rule beside `atNextTick(...)`: each call to that helper constructs a separate temporary receiver. Two helper calls therefore create two event objects, whereas calling `span()` twice on one already-published receiver addresses the same event. The distinction matters when reasoning about deferred work and cancellation.

This distinction prevents two common mistakes. Repeatedly publishing one receiver is not a way to count independent jobs, and queuing work is not proof that it ran. Observe the resulting callback effect, and keep data needed by that callback alive until execution or a supported cancellation path has finished.

### The multiplexer and one successful tick

\index{EventMultiplexer@\texttt{EventMultiplexer}}
\index{multiplexer}
\index{event queue}
\index{event loop!tick cycle}
\index{timeouts}
\index{event loop!cleanup}

`core::EventMultiplexer` combines descriptor observation, timer deadlines, queued work, timeout processing, signals, and resource cleanup. It is more than a wrapper around a readiness syscall. The backend can use `epoll`, `poll`, or `select` while preserving that coordinating responsibility.

Its three descriptor channels are `RD`, `WR`, and `EX`: readable, writable, and exceptional activity. Input processing, draining queued output, and error handling need different observations. Its timer publisher contributes deadlines; its embedded `EventQueue` supports insertion, removal, execution, and clearing with separate publish and execute queues.

Read a successful tick as a sequence of responsibilities:

1. Determine the wait from descriptor observation, timer deadlines, and the caller's bound.
2. Wait for readiness, due timers, or an interruption such as a signal.
3. Publish active work toward its receivers.
4. Execute queued events, including deferred activation and next-tick work.
5. Check descriptor timeouts and release expired or disabled resources.
6. Return the iteration's `TickStatus` to the event-loop control path.

This is a conceptual reading of `EventMultiplexer::tick()`, not a replacement for every branch. `start()` supplies the running state and repeats internal iterations; the public stepping restriction still applies. A long callback delays not only another read, but also the timeout checks and cleanup waiting for dispatch to return.

Application code should perform the immediate protocol work, preserve its invariants, and return. Descriptor readiness is an opportunity to make progress, not permission to occupy the loop until an entire application task completes. Bound the work or design an explicit handoff when one operation would delay unrelated roles.

### Observed descriptor populations

\index{descriptor events}
\index{descriptor publishers}
\index{descriptor receivers}
\index{event receivers}

A descriptor publisher manages observed receiver lists keyed by descriptor. It can enable, disable, suspend, and resume observation; publish active events; check timeouts; release disabled events; deliver signals; and disable the whole publisher. Descriptor handling therefore has a managed lifecycle beyond “call my function when this fd is ready.”

Enable/disable governs entering or leaving the observed population. Suspend/resume represents temporary inactivity while the receiver remains part of the runtime model. Backpressure, staged activity, retry delays, and temporary quiescence need that distinction: an existing receiver need not produce events at every moment.

The receiver derives from `EventReceiver`, tracks enablement and suspension, attaches to a descriptor, and has timeout and signal behavior. It implements reactions such as `dispatchEvent()`, `timeoutEvent()`, and `signalEvent(int)`. Publishers decide who is observed; receivers define what happens when that observation produces work.

| Runtime object | Main responsibility | Simple mental rule |
|---|---|---|
| `DescriptorEventPublisher` | Manages the observed population for a descriptor channel | Decides *who is being observed* |
| `DescriptorEventReceiver` | Defines behavior for one observed descriptor participant | Decides *what happens when observation produces work* |


Socket acceptors, connectors, readers, and writers specialize this pattern. Treat them as runtime participants with observation, timeout, and cleanup state, rather than anonymous callbacks. Disabling observation and destroying the participant are different lifecycle steps; coordinated cleanup must respect any work still using it.

### Timers and nonblocking callback work

\index{timers}
\index{event loop!timers}

`TimerEventPublisher` maintains a timer set, supports insertion and removal, computes the next timeout, publishes due events, and can stop its publisher. The `core::Timer` base is an ownership-oriented handle around a timer receiver, with `cancel()` and `restart()`. `core::timer::Timer` offers `intervalTimer(...)` and `singleshotTimer(...)` creation helpers.

Timers participate in the same loop as descriptors and queued work. The multiplexer combines their deadlines with descriptor observation, so retries and reconnects can be scheduled without sleeps, blocking loops, or a second scheduler. Chapter 4 introduced those as operational concerns of instances; the timer machinery supplies their time-based progression.

If a callback sleeps while waiting to retry, it also delays other connections, timers, queued events, timeout checks, and cleanup. Schedule the later action and return instead. This keeps the current protocol invariant intact while allowing unrelated roles to advance. A timer becoming due does not let its callback preempt a different callback that is still running.

The same rule applies to application-model updates. A short acceptance operation and bounded observer callbacks fit naturally in the event-loop thread. A synchronous observer that performs expensive work holds up the caller and therefore the rest of that runtime. Timer support cannot compensate for a blocking observer; callback duration is still an application responsibility.

### Coordinated shutdown

\index{shutdown}
\index{ShutdownContext@\texttt{ShutdownContext}}
\index{ShutdownReason@\texttt{ShutdownReason}}

Stopping the main run loop and destroying every descriptor immediately are not the same operation. Established streams can have queued output or a TLS shutdown exchange still in progress.

The runtime passes a `ShutdownContext` from the event loop through the multiplexer,
descriptor publisher and receiver to `SocketConnectionT` along its existing
ownership graph.

`ShutdownReason::Requested`, `ShutdownReason::Signal`, and `ShutdownReason::NoObserver` retain the reason shutdown began. For an established stream, these reasons join the same bounded write-shutdown path rather than selecting unrelated cleanup mechanisms.

A stream connection has reader and writer receiver subobjects. Both can encounter the framework notification, but the complete connection coordinates the operation once. Repeated delivery must join the existing shutdown rather than duplicate a signal callback, start a second transport shutdown, or destroy a helper that is still needed to finish.

`STOPPING` therefore still contains controlled work. Read observation can remain necessary for peer EOF or TLS `close_notify`, and timeout/termination behavior bounds a peer that does not cooperate. This is continuation of cleanup, not permission for an application to start unrelated new communication.

Signal-triggered shutdown still invokes the context's `onSignal(int)` callback. Its `bool` signature remains, but during coordinated framework shutdown the result cannot veto transport cleanup. A context should perform its protocol-specific response without assuming that returning `false` can keep the framework running.

The public application control surface remains `core::SNodeC`. That path explains internal coordination; it does not ask an installed consumer to include private `EventLoop` or multiplexer implementation headers. Chapters 15 and 16 connect the same shutdown model to TLS, timeouts, and output pressure.

### Part II checkpoint: one accepted state

The byte-transport checkpoint returned even an invalid measurement unchanged. We can now isolate the next responsibility: accepted state needs one owner, with observers whose lifetimes are explicit. The public solution compiles the canonical `MeasurementModel.cpp` directly; no HTTP, MQTT, or socket parser is needed to see this contract.

`accept(...)` takes a measurement by value, assigns the next local sequence, stores it, and invokes subscribed listeners synchronously. Two inputs carrying sequences 900 and 2 become accepted states 1 and 2. Remove the first observer between calls, then accept input numbered 1: the remaining observer sees accepted state 3, and `current()` agrees. The removed observer retains only its earlier observations. Unsubscribe the remaining listener before its captured storage leaves scope.

In a gateway, protocol callbacks will parse and validate input before calling this shared owner. This model experiment executes acceptance and observer removal; it does not demonstrate event-loop scheduling, transport teardown, or persistence. The other lab observes actual deferred callbacks. Together they connect state ownership with the runtime rule: keep operations bounded and retain their dependencies until callbacks finish.

::: {.snodec-remember title="What to remember"}
- Use `core::SNodeC::start()` for the runtime progression taught here; a public `tick()` status alone does not establish dispatch.
- One loop coordinates descriptors, timers, queued work, timeouts, and cleanup; blocking a callback delays them together.
- One published event and several separately queued callbacks have different execution counts.
- Shutdown can include bounded cleanup after the main running phase ends.
- Shared accepted state needs one owner; remove subscriptions before destroying captured observer state.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Distinguish `RUNNING` from `SUCCESS`. Why is an observed callback a stronger progress check than the latter status alone?
2. **Review (O2).** A receive callback sleeps before retrying. Trace which descriptor, timer, timeout, and cleanup work waits behind it, and explain why arming a timer elsewhere cannot preempt the sleep.
3. **Lab (O1, O2).** Build and run the queued-work solution. Expect no callback effect before `start()`, then trace 1,2,3: first callback entry and return, followed by its deferred child. Verify the child never observes the first callback active; explain why this says nothing about timing guarantees under load.
4. **Lab (O3).** Build and run the Part II model checkpoint. Expect input sequences 900,2,1 to become local order 1,2,3. Remove one observer after the second acceptance; expect it to retain only 1,2 while the other sees all three. Explain where gateway callbacks will call this model.
5. **Design (O1, O2, O3).** One measurement observer must perform slow persistence. Choose a process boundary or supported asynchronous handoff; justify callback lifetime, ordering, shutdown, and how completion returns without making the worker a second acceptance owner.

Public answers, commands, and expected observations: `companion/exercises/ch06/README.md`.
:::
