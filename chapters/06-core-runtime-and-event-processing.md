## Core Runtime and Event Processing
### Why this chapter matters

In Chapter 5 we built a mental model of SNode.C around instances, connections, contexts, factories, and layers.

That model is necessary, but it still leaves an important question open.

**How does the framework actually keep everything moving?**

A server can register an intention to listen. A client can register an intention to connect. A context can define reactions such as `onConnected()` and `onReceivedFromPeer()`. A timer can be armed. A descriptor can become readable. A timeout can expire.

Something has to coordinate all of that.

That “something” is the runtime core.

This chapter explains the runtime without getting lost in implementation noise. We will stay close to the current repository structure, but we will describe it in a teaching-oriented way: as a small number of cooperating runtime concepts.

The key insight is this:

> SNode.C does not treat event processing as a hidden implementation detail. It gives it a clear architecture.

That architecture has several visible pieces:

- `core::SNodeC` as the public runtime control surface,
- `core::EventLoop` as the singleton orchestrator,
- `core::EventMultiplexer` as the waiting and dispatch backbone,
- descriptor event publishers and receivers for file-descriptor activity,
- timer publishers and timer handles for scheduled activity,
- and a lightweight event queue for deferred execution.     

Once those pieces are placed correctly in the reader’s mind, the framework’s behavior stops feeling magical.

### The public runtime surface: `core::SNodeC`

The first runtime-facing type most users encounter is `core::SNodeC`.

In the current codebase, its public surface is intentionally small:

- `init(int argc, char* argv[])`
- `start(const utils::Timeval& timeOut = {LONG_MAX, 0})`
- `stop()`
- `tick(const utils::Timeval& timeOut = 0)`
- `free()`
- `state()` 

This small public surface already teaches several important things.

#### The runtime has explicit phases

The existence of `init`, `start`, `stop`, `free`, and `state` tells us that the framework runtime is not just a side effect of object construction.

It has lifecycle.

That is a design strength. It reduces ambiguity for applications and gives the reader a stable mental timeline.

#### Event-loop control is intentionally centralized

The existence of `start()` and `tick()` tells us that SNode.C treats the event loop as a central framework capability rather than as a behavior buried inside one particular server or client type.

That means sockets, timers, retries, and protocol contexts all live inside one runtime story.

#### `tick()` reveals something subtle but important

The presence of `tick(...)` is especially interesting.

It means SNode.C is not limited to one usage pattern only. It can run in the classical “start the event loop and let it own the thread” mode, but it also exposes a per-iteration stepping model. This makes the runtime more understandable and potentially more embeddable than a pure black-box loop would be.  

That is not just convenient. It is architecturally revealing.

A framework that offers `tick()` is telling you: the event loop is real, structured, and inspectable.

### The hidden public secret: `core::EventLoop`

Although most application code touches `core::SNodeC`, the current repository makes clear that the actual loop orchestrator is `core::EventLoop`.

Its header tells us several key facts:

- it is a singleton (`instance()`),
- it owns or exposes an `EventMultiplexer`,
- it tracks a tick counter,
- it tracks runtime state,
- and it is the actual home of `init`, `tick`, `start`, `stop`, and `free`, with `SNodeC` acting as the public façade. 

This is an excellent example of a good teaching design in a systems framework.

The application sees a compact, stable façade. The runtime internals still have a concrete orchestrator object.

That separation keeps everyday use simple without flattening the underlying architecture.

#### Why a singleton event loop makes sense here

The singleton model is a tradeoff.

On the positive side, it gives the framework one primary event domain per process. That simplifies ownership, global coordination, and runtime reasoning. The repository’s own runtime notes describe this as centralized lifecycle management and explicitly call out that the singleton loop simplifies global ownership, though at the cost of flexibility for multi-reactor scenarios. 

For teaching purposes, this is helpful.

It means the reader does not need to imagine several unrelated event loops competing inside the same application. There is one runtime story.

On the other hand, it also means the framework is not optimized around multiple independent reactor domains inside one process. That is a real tradeoff, and it is better to understand it early.

### Runtime state is coarse on purpose

The current `core::State` enum is small:

- `LOADED`
- `INITIALIZED`
- `RUNNING`
- `STOPPING` 

At first glance, this may seem too simple. But for teaching and operational reasoning, it is almost ideal.

It gives the framework a coarse-grained phase language without turning ordinary users into internal state-machine archaeologists.

A reader can now think in a clean timeline:

1. the framework is loaded,
2. it is initialized,
3. it is running,
4. it is stopping.

That is enough to reason about many important behaviors.

For example, in the current `SocketServer` and `SocketClient` templates, real listen/connect work is only scheduled forward if the framework state is appropriate. In Chapter 5 we already saw that these operations integrate with runtime state rather than behaving like isolated library calls. This chapter sharpens that picture: the event loop state is not background decoration; it is part of the control logic.   

### Tick-by-tick execution and `TickStatus`

If `State` describes coarse lifecycle phases, then `TickStatus` describes the result of a single event-loop iteration.

In the current codebase, `TickStatus` contains:

- `SUCCESS`
- `INTERRUPTED`
- `NOOBSERVER`
- `TRACE` 

This enum is more informative than it may first appear.

#### Why `SUCCESS` is obvious but still useful

`SUCCESS` simply means the iteration completed normally.

In a tick-driven or embedded integration scenario, this allows the caller to distinguish ordinary progress from exceptional control outcomes.

#### Why `INTERRUPTED` matters

An event loop can be interrupted by signals or other control conditions. Exposing this as a separate status keeps such cases explicit.

That is better than silently collapsing them into generic success or failure.

#### Why `NOOBSERVER` is architecturally interesting

`NOOBSERVER` is a very revealing name.

It suggests that SNode.C thinks in terms of *observed runtime entities* — descriptor receivers, timers, and other event sources — and that a loop iteration can recognize the absence of anything meaningful left to observe.

That is a strong hint about the event model: the runtime is not just looping blindly; it is managing a population of observed event receivers.

#### Why `TRACE` hints at diagnosability

Even without over-interpreting it, `TRACE` suggests that the loop design keeps room for richer per-tick visibility or instrumentation.

The important teaching point is not the exact internal usage. The important point is that per-tick semantics are explicit enough to be named.

### From runtime intent to event delivery

To really understand event processing, we need to distinguish between two different meanings of “event” in SNode.C.

The first is a **runtime scheduling event**. The second is a **descriptor or timer readiness event**.

These are related, but not identical.

#### Scheduling events

The `core::EventReceiver` API makes one important mechanism directly visible: `atNextTick(const std::function<void(void)>&)`. 

This is the framework’s way of saying:

> Do not do this immediately on the caller’s stack. Queue it for the next event-loop turn.

That is exactly what the current `SocketServer` and `SocketClient` templates do when they begin the real listen/connect workflow.  

This small design decision has a large conceptual effect.

It means the framework consistently moves operational work into the runtime domain instead of letting arbitrary user call stacks become the event loop.

That produces cleaner phase boundaries and more predictable sequencing.

#### Readiness events

A descriptor may become readable, writable, exceptional, or timed out. A timer may expire. A signal may arrive.

These are not “next tick callbacks” in the same sense. They are external or scheduled conditions that the runtime notices and then dispatches.

So the mental model should be:

- `atNextTick(...)` is how framework or user code can enqueue work into the loop,
- descriptor and timer mechanisms are how the loop notices the outside world.

### `EventReceiver` and `Event`: the small but important abstraction pair

The current `EventReceiver` and `Event` headers are compact, but together they reveal a lot about the runtime’s shape.

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

- the **receiver** is the runtime-facing behavior endpoint,
- the **event** is the thing that becomes queued and dispatched for that receiver.

That is a very elegant split.

It means SNode.C can talk about *who handles work* and *what gets published into the loop* as related but distinct concepts.

#### What `span()` and `relax()` suggest

Both `EventReceiver` and `Event` expose `span()` and `relax()`-style operations. The names may feel unusual at first, but conceptually they fit the framework well.

They suggest activation and deactivation of observation or publication rather than a procedural “do this now” model.

This is consistent with the whole architecture: runtime entities are observed, enabled, disabled, suspended, resumed, and dispatched. The framework vocabulary is intentionally lifecycle-oriented.

### The multiplexer is the waiting and coordination backbone

At the center of event processing sits `core::EventMultiplexer`.

Its header is one of the richest runtime descriptions in the current codebase. It tells us that the multiplexer:

- owns access to three descriptor event publisher channels (`RD`, `WR`, `EX`),
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

This is an extraordinary amount of runtime design information in one place.

A good teaching summary is this:

> The multiplexer is not only a thin wrapper around `epoll`, `poll`, or `select`. It is the runtime hub that combines descriptor readiness, timer progression, queued framework events, timeout processing, and cleanup into one coordinated tick.

That is a much richer mental picture than “the multiplexer waits for file descriptors.”

#### Why there are three descriptor channels

The enum inside `EventMultiplexer` defines three descriptor categories:

- `RD`
- `WR`
- `EX` 

That immediately maps to readable, writable, and exceptional descriptor activity.

So the runtime does not treat all descriptor activity as one undifferentiated stream. It keeps distinct observation channels for the major categories of interest.

#### The event queue inside the multiplexer matters a lot

The embedded `EventQueue` inside `EventMultiplexer` is especially revealing.

It has insert/remove/execute/clear operations and maintains separate execute and publish queues. Even without needing every implementation detail, the architecture tells us that queued event work is a first-class part of a loop tick, not an ad-hoc side mechanism. 

This helps explain why `atNextTick(...)` can be such a clean primitive.

There is already a place in the loop structure for queued runtime work.

### Descriptor event publishers: observed file descriptors as managed populations

The current `DescriptorEventPublisher` header is also highly informative.

A descriptor event publisher can:

- `enable(...)`
- `disable(...)`
- `suspend(...)`
- `resume(...)`
- `spanActiveEvents()`
- `checkTimedOutEvents(...)`
- `releaseDisabledEvents(...)`
- `signal(...)`
- `disable()` the whole publisher 

It also maintains maps of observed receiver lists keyed by descriptor.

This is a strong clue about the internal runtime philosophy.

SNode.C does not think of descriptor handling as “the loop calls my callback when `fd` is ready.”

Instead, it thinks in terms of **managed observed populations**:

- receivers can become observed,
- temporarily suspended,
- resumed,
- timed out,
- disabled,
- or released.

This is a more operationally mature model than a naïve reactor sketch.

#### Why suspend/resume is different from enable/disable

Even without implementation detail, the distinction between suspend/resume and enable/disable is conceptually valuable.

- **enable/disable** suggests entering or leaving the observed population,
- **suspend/resume** suggests remaining conceptually present while temporarily inactive.

That is exactly the kind of distinction that becomes important in real systems where backpressure, staged activity, retry delays, or temporary quiescence must be represented cleanly.

### Descriptor event receivers: behavior attached to observed descriptors

If publishers manage descriptor-facing populations, then receivers express the behavior of one observed descriptor participant.

The current `DescriptorEventReceiver` header confirms this. A receiver:

- derives from `EventReceiver`,
- knows whether it is enabled or suspended,
- can be enabled on a file descriptor,
- can be disabled, suspended, resumed,
- can have timeout behavior,
- and must implement runtime reactions such as `dispatchEvent()`, `timeoutEvent()`, and `signalEvent(int)`. 

This tells us how the descriptor side of the runtime really fits together.

A descriptor receiver is not “just a callback object.”

It is a runtime participant with:

- observation state,
- timeout state,
- signal behavior,
- and dispatch behavior.

That is why the framework can support such a wide range of connection and socket workflows while still feeling regular.

The same basic runtime pattern is reused with different specialized receivers.

### Timers are not bolted on — they are part of the same event story

A good runtime design treats timers as first-class event sources.

SNode.C does exactly that.

The current `TimerEventPublisher` maintains a timer set, supports insertion and removal, can compute the next timeout, can span active events, and can stop the timer publisher itself. 

The current `core::Timer` base class is a small ownership-oriented handle around a timer event receiver, offering `cancel()` and `restart()`. On top of that, `core::timer::Timer` provides concrete creation helpers such as:

- `intervalTimer(...)`
- `singleshotTimer(...)`  

This means the timer story fits beautifully into the broader runtime story.

A timer is not a foreign utility living outside the event loop.

It is part of the loop’s own scheduled event fabric.

That has several benefits.

#### Timers share the same central loop worldview

A timeout does not require a second runtime model.

It is simply another kind of event source participating in the same tick progression.

#### Retry and reconnect features fit naturally

In Chapter 5 we already saw that `SocketServer` and `SocketClient` integrate retry and reconnect behavior. That becomes much easier to understand now: these features are natural because the runtime already has timer-driven scheduling built into its core.    

### One tick, conceptually

With the main pieces now placed, we can describe one conceptual event-loop iteration.

This is not a line-by-line implementation trace. It is the teaching model that best fits the current structure.

#### The loop begins a tick

The event loop begins one iteration and has a timeout budget.

#### The multiplexer determines what to wait for

The multiplexer considers descriptor activity and timer deadlines, computes the next relevant timeout, and prepares to monitor the registered descriptor sources.  

#### External readiness or timer expiration occurs

Descriptors become readable, writable, exceptional, or timed out; timers become due; signals may arrive.

#### Active events are spanned

The multiplexer spans active events and publishes them toward the relevant receivers.  

#### The event queue is executed

Queued work — including next-tick callbacks and other internal runtime events — is executed.  

#### Timeouts and cleanup are checked

The loop checks for timed-out observed entities and releases expired or disabled resources.  

#### The tick returns a status

The loop reports a `TickStatus`, and the next iteration can begin. 

That is the conceptual heartbeat of SNode.C.

### Why `listen(...)` and `connect(...)` are intentionally indirect

By now, one of the framework’s earlier design choices should feel much more natural.

In the current `SocketServer` and `SocketClient` templates, the public `listen(...)` and `connect(...)` entry points do not immediately perform all operational work. Instead, they schedule their real work through `EventReceiver::atNextTick(...)` and let the runtime proceed from there.   

Why is that such a good idea?

Because it preserves a clean boundary between:

- the user’s current call stack,
- and the framework’s event-processing domain.

This reduces hidden reentrancy surprises and keeps communication lifecycle transitions inside the same runtime world that will later handle reads, writes, timeouts, retries, reconnects, and disconnects.

In other words, the indirection is not unnecessary complexity.

It is architectural hygiene.

### Why the runtime is teachable

Some event-driven systems are hard to teach because the control flow is too dispersed.

SNode.C is easier to teach because its runtime core has a small set of well-defined moving parts:

- one event loop,
- one multiplexer backbone,
- observed descriptor receivers,
- timer receivers,
- a queue for deferred work,
- explicit runtime states,
- explicit per-tick statuses.      

That does not mean the implementation is trivial. It is not.

But it does mean the conceptual structure is stable and nameable.

That is exactly what a good teaching book needs.

### Practical advice for readers using the runtime

At this point, it is helpful to translate the architecture into a few practical habits.

#### Call `init(...)` early

Because the runtime is a real framework phase, initialization should not be treated as optional decoration.

It prepares the environment in which instances, configuration, and event-driven behavior will make sense. 

#### Think of `start()` as entering the runtime world

When you call `core::SNodeC::start()`, you are not merely “waiting.”

You are giving control to the central event-processing machinery. That is where the runtime story truly begins. 

#### Use `tick()` when you need integration, not because you fear the loop

The existence of `tick()` is a strength, but it should be used for a reason: embeddability, controlled stepping, or hybrid runtime coordination. It is not primarily a sign that `start()` is insufficient.  

#### Do not confuse framework-managed events with manual control flow

If a connection callback, a context method, or a timer callback is invoked, that is runtime-driven behavior. Resist the temptation to explain everything as if the program were still following one linear call chain from `main()`.

That mindset breaks down quickly in event-driven systems.

#### Treat timers and retries as part of the same runtime fabric

A retry delay is not outside the loop. A reconnect wait is not outside the loop. A singleshot timer is not outside the loop.

They are all expressions of the same event-processing model.    

### Common misunderstandings about the runtime

It helps to name a few misunderstandings explicitly.

#### Misunderstanding 1: “The event loop is just the socket waiting mechanism.”

Corrected view: the event loop includes descriptor monitoring, timer processing, queued events, timeout checks, and cleanup — not only descriptor waiting. 

#### Misunderstanding 2: “Timers are a separate utility facility.”

Corrected view: timers are first-class event sources inside the same runtime architecture.  

#### Misunderstanding 3: “Calling `listen(...)` or `connect(...)` means the work happens directly there.”

Corrected view: these methods register and schedule work into the event-driven runtime.   

#### Misunderstanding 4: “A callback-based framework must be opaque.”

Corrected view: SNode.C keeps the runtime measurable through explicit states, tick results, connection metrics, publisher/receiver abstractions, and named runtime phases.    

#### Misunderstanding 5: “Event-driven means there is no structure, only callbacks.”

Corrected view: in SNode.C, callback behavior lives inside a strong architecture: façade, event loop, multiplexer, publishers, receivers, timers, and queued event dispatch.

### Closing perspective

A good runtime chapter should leave the reader with less fear of the event loop, not more.

SNode.C’s runtime becomes understandable once you see that it is made of a few cooperating layers of responsibility.

- `core::SNodeC` is the public control surface.
- `core::EventLoop` is the singleton orchestrator.
- `core::EventMultiplexer` is the waiting and coordination backbone.
- descriptor publishers and receivers handle observed file-descriptor activity.
- timer publishers and timer handles manage scheduled activity.
- `EventReceiver` and `Event` connect behavior to queued dispatch.
- `State` and `TickStatus` make lifecycle and per-iteration outcomes explicit.       

This is the runtime heart of the framework.

And once the runtime heart is understood, the next chapter becomes much easier.

We can finally examine the framework’s layered structure — network family, transport, connection, and application — not as an abstract taxonomy, but as something already carried by a concrete event-driven runtime.
