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

The previous chapters separated runtime lifetimes from the layer choices beneath a context. Neither picture yet explains how two peers and a timer make progress in one process. To answer that, follow a single successful event-loop turn before reading the implementation. The question is practical: if one callback takes too long, which other work must wait?

Imagine that peer A has bytes ready, a connection retry timer is due, one application callback is already queued, and peer B has reached its read-timeout deadline. These are four reasons to do work, not four independent threads. The runtime must coordinate them while preserving the objects that each callback still uses. We will use this situation as a thought experiment; it describes responsibilities within a successful turn rather than promising an order among callbacks that happen to become ready together.

First comes the wait decision. The loop combines the caller's waiting bound with scheduled deadlines and descriptor observation. It should not sleep for a long interval when a timer already needs attention. Likewise, a ready descriptor gives it work without requiring an application-side blocking read loop. Waiting gathers evidence that progress is possible; it does not mean that a complete application message is available from peer A.

Next, active descriptor and timer work is published toward the appropriate receivers. Peer A's readiness can lead to receive processing; the due retry can lead to another attempt. Publication identifies work to dispatch. It does not give either participant exclusive use of the processor until its entire conversation succeeds. The retry still has its own eventual result, and peer A may still supply only part of a record.

Queued work then executes through the event queue. The already-queued application callback shares this scheduling domain with the work produced by readiness and deadlines. If it schedules another callback, that later work must not be treated as a recursive call at the scheduling expression. The deferred-work lab below makes the distinction observable: the first callback records its return before its deferred child can observe it as inactive.

The timeout check asks a different question from readiness: has peer B gone too long without the progress its policy requires? Peer A having data does not answer that question for B. A timeout can initiate closure or another protocol reaction, so it must run while the relevant receiver and connection state are still valid. Finally, cleanup releases expired or disabled resources after the work that still needs them. A decision to stop observing an object and destruction of that object are distinct events.

Now place a slow parser inside peer A's callback. While that callback is running, the loop cannot move ahead to the queued callback, the remaining timeout work or cleanup merely because those jobs belong to different peers. A due timer is a deadline to observe, not a preemptive execution slot. This explains the practical rule to do bounded work and return. The rule follows from the shared event loop, without requiring the reader to understand every receiver subclass first.

The useful prediction is therefore about dependencies rather than exact timestamps. After a long callback, unrelated work can be late. After a callback queues output, the peer may not yet have received it. After timeout processing requests cleanup, destruction may still have work to respect. A test should observe the effect needed by the application—such as a callback trace or a reply—rather than infer it from a successful iteration status alone.

With those questions established, the source map becomes easier to read. Locate where waiting is bounded, where work is published, where it executes and where resources are released. The same sequence will later explain why shutdown continues doing controlled work after ordinary running has ended. It also gives a concrete place to investigate application mistakes: a callback that never returns blocks more than its own connection.

The runtime is where the model becomes observable. Descriptors become ready, timers expire, queued work runs, callbacks fire, and connections advance without each application inventing its own event loop. The public control surface is `core::SNodeC`; `core::EventLoop` orchestrates the loop, and `core::EventMultiplexer` coordinates waiting and dispatch.

![The SNode.C event-processing core connects runtime control, descriptor readiness, timers, queued work, and protocol dispatch.](assets/figures/pdf/fig-03-event-runtime-picture.pdf){#fig:snodec-event-runtime width=88% latex-placement="tbp"}


Figure \ref{fig:snodec-event-runtime} is an orientation map, not a promise about every internal call order. Descriptor readiness, timers, queued work, timeout processing, signals, and cleanup meet in this runtime. The source excerpts make their relationship concrete.

\index{source-level reading}
\index{SNode.C!source reading}


The implementation follows the same structure. The excerpts below are abridged from `src/core/SNodeC.cpp`, `src/core/EventLoop.cpp`, and `src/core/EventMultiplexer.cpp`.

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

Use the thought experiment to read the following status vocabulary critically. A status describes the loop's control result; the application needs evidence that its own work occurred. In the deferred-work lab, that evidence is the ordered callback trace. In the echo program, it is received bytes. A timeout observation concerns elapsed inactivity for a particular participant. Mixing those three kinds of evidence would make a successful loop iteration appear to certify much more than the code actually observed.

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

Use `start()` to advance these examples. It bootstraps configuration and enters `RUNNING`. The internal `EventLoop::tick(...)` path reached through public `SNodeC::tick()` calls `_tick(...)` in `INITIALIZED`, but the internal multiplexer dispatch requires `RUNNING` with no pending stop signal, or `STOPPING`. Consequently, calling public `tick()` after `init()` is not equivalent to the startup path shown here. Read the internal tick sequence to understand coordination; do not infer an external-loop integration recipe from a successful return status.

The coarse runtime phases are `LOADED`, `INITIALIZED`, `RUNNING`, and `STOPPING`. They describe the framework lifecycle; a listen or connect flow can advance only when the runtime processes its work. `TickStatus` instead describes one iteration:

| Status | Interpretation |
|---|---|
| `SUCCESS` | Normal iteration result; observe a callback or byte exchange to establish application progress. |
| `INTERRUPTED` | Interruption remains explicit, including signal/control conditions. |
| `NOOBSERVER` | No observed participants remain for the runtime to advance. |
| `TRACE` | A named per-tick result, not a full tracing subsystem. |

A successful status alone is insufficient for the initialized public stepping path described above. The header names the possible results; the implementation shows when an iteration actually dispatches work.

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
`atNextTick` queues the callback for a later event-loop turn instead of running it immediately on the caller’s stack. Captured objects must remain valid until that callback executes.
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

The relevant public interface is this excerpt from `companion/examples/MiniGateway/MeasurementModel.h`; `Subscription` names the listener token returned by `subscribe()`:

```cpp
Measurement current() const;
Measurement accept(Measurement measurement);
Subscription subscribe(Listener listener);
void unsubscribe(Subscription subscription);
```

Read the four operations as observation, acceptance, subscription and explicit removal. The protocol that eventually supplies a measurement is absent from this interface, so it cannot become a second place that orders accepted state.

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
