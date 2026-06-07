## Database Support and Application State

### From protocol boundaries to persistence boundaries

Chapter 27 described IoT systems as collections of communication boundaries.

Chapter 28 adds another kind of boundary:

```text
the persistence boundary
```

Persistence is where selected application information survives beyond one connection, message, request, or runtime episode.

A protocol boundary asks:

```text
How does information move between active participants?
```

A persistence boundary asks:

```text
What information should remain after the immediate conversation is over?
```

That changes the architecture of an application.

The application now has to decide:

- what belongs in memory,
- what belongs in durable storage,
- when database work should be started,
- how database results flow back into the event-driven application,
- what happens when the database is unavailable,
- and how persistence interacts with protocol roles such as HTTP, MQTT, WebSocket, SSE, and local-control interfaces.

A useful model is:

```text
protocol event
  -> application interpretation
      -> runtime state
          -> optional persistence boundary
              -> durable application state
```

Persistence is not automatically part of every request or every message.

It is a boundary that should be chosen deliberately.

### Persistence as an application-state boundary

A database is not just another transport protocol.

A HTTP endpoint, MQTT session, WebSocket connection, Bluetooth link, or Unix-domain control socket is usually a communication boundary between active participants.

A database connection is different.

It is a persistence and query boundary.

It stores state, retrieves state, changes state, and may become the durable memory of a larger system.

A compact comparison helps:

| Concern | Protocol boundary | Persistence boundary |
|---|---|---|
| main purpose | exchange information | store/retrieve durable information |
| lifetime | often connection, session, request, or message scoped | survives beyond runtime episodes |
| examples | HTTP, MQTT, WebSocket, Bluetooth | MariaDB database |
| failure mode | peer unreachable, protocol error, timeout | connection failure, query failure, transaction failure |
| application question | what did the peer say? | what should be remembered? |
| SNode.C concern | event-driven communication | event-integrated database work |

This distinction matters because database work should not be treated as random helper code hidden inside protocol callbacks.

It belongs to the application-state architecture.

### What SNode.C currently supports

The database support in SNode.C has a concrete scope.

The current concrete database module is MariaDB-focused.

It is not presented here as a generic multi-backend persistence abstraction.

The accurate statement is:

> SNode.C currently provides a MariaDB integration layer shaped to work inside the same event-driven runtime discipline as the rest of the framework.

This narrower statement keeps the chapter aligned with the implementation.

It lets the chapter focus on what the code actually provides:

```text
MariaDB client object
  -> connection details
      -> event-integrated MariaDB connection
          -> command objects
              -> command sequences
                  -> callbacks for result and error handling
```

#### MariaDB-focused database module

The MariaDB module is built only when the MariaDB client library is available.

The module builds the shared library:

```text
db-mariadb
```

and installs MariaDB-specific headers under the MariaDB database include path.

The module contains:

- `MariaDBClient`,
- asynchronous and sync-style API surfaces,
- `MariaDBConnection`,
- `MariaDBConnectionDetails`,
- command classes,
- command sequences,
- connection/library support,
- asynchronous commands,
- sync-style metadata commands.

The module structure presents this part of the framework as concrete MariaDB support integrated with the runtime.

It is concrete database support for MariaDB, integrated into SNode.C’s runtime style.

It is not a broad ORM layer.

It is not a generic database-independent abstraction.

#### Test application as demonstration, not production model

The current `testmariadb` application is best read as a demonstration and test program.

It shows the API shape and runtime integration.

It demonstrates:

- adding database-related configuration,
- initializing the SNode.C runtime,
- constructing connection details,
- creating MariaDB client objects,
- observing database state changes,
- executing statements,
- querying rows,
- chaining command sequences,
- reading metadata,
- using transactions,
- scheduling repeated database activity.

That is useful.

But the example should not be copied as production persistence architecture without thought.

A useful distinction is:

| Test app demonstrates | Production code should decide |
|---|---|
| API shape | ownership and lifetime of the database service |
| command chaining | domain-level persistence workflow |
| state callback | operational reporting policy |
| transactions | transaction policy |
| timers | scheduling policy |
| hard-coded values | secure configuration and secret handling |

The test application shows how the pieces work.

A real application must decide how persistence belongs to its own roles, configuration, security model, and failure policy.

### Application state and database state

Application state and database state are not the same thing.

Runtime state exists while the application is running.

Database state survives beyond the current runtime episode.

A useful distinction is:

```text
runtime state
  -> live connections
  -> sessions
  -> timers
  -> pending work
  -> caches
  -> current protocol relationships

database state
  -> persisted facts
  -> measurement history
  -> users
  -> audit records
  -> durable configuration
  -> long-lived application data
```

The decision is not always obvious.

Some information may exist in both places:

```text
database
  -> durable source of truth

runtime cache
  -> current fast-access representation
```

The application must decide how those representations are synchronized.

#### What belongs where?

A practical table helps.

| Information | Usually runtime state | Usually database state |
|---|---:|---:|
| active socket connection | yes | no |
| current WebSocket session | yes | no |
| active timer | yes | no |
| pending command sequence | yes | no |
| MQTT subscription relationship | often yes | sometimes metadata |
| last known device state | cache maybe | often yes |
| sensor measurement history | no | yes |
| audit log | no | yes |
| durable configuration | maybe loaded into memory | often source of truth |
| currently displayed dashboard state | yes | maybe derived from stored data |

The database should not become a dumping ground for every transient detail.

Runtime memory should not pretend to be durable when it is not.

The persistence boundary should be explicit.

### `MariaDBClient` as the application-facing database object

The main application-facing object is `database::mariadb::MariaDBClient`.

It is constructed from:

```text
MariaDBConnectionDetails
  + state-change callback
```

and exposes:

```text
async command API
  + sync-style metadata API
```

A useful model is:

```text
MariaDBConnectionDetails
  + onStateChanged callback
      -> MariaDBClient
          -> async commands
          -> sync-style metadata calls
          -> event-integrated connection
```

The state-change callback receives a state object containing:

- error number,
- error message,
- connected flag.

This fits SNode.C’s runtime style.

The application does not only issue database operations.

It can also observe whether the database resource is connected, unavailable, or in an error state.

#### `MariaDBConnectionDetails`

`MariaDBConnectionDetails` describes the database endpoint and credentials.

| Field | Meaning |
|---|---|
| `connectionName` | diagnostic / operational name |
| `hostname` | database host |
| `username` | database user |
| `password` | database password |
| `database` | selected database |
| `port` | TCP port, if used |
| `socket` | local socket path, if used |
| `flags` | MariaDB client flags |

The `connectionName` is especially useful for diagnostics.

A named database connection is easier to understand in logs than an anonymous one.

The credential fields also deserve care.

A test application may use direct values to make the example compact.

A real application should decide how credentials are configured, protected, and deployed.

#### State-change callback

The state-change callback makes the database connection visible to the application.

That matters because a database is a runtime participant.

It may be:

- connected,
- disconnected,
- unavailable,
- misconfigured,
- rejected by authentication,
- failed during operation.

The callback gives the application a place to react.

For example:

```text
database connected
  -> enable persistence-dependent work

database unavailable
  -> report degraded state
      -> pause periodic writes
          -> keep protocol roles alive if possible
```

The exact policy belongs to the application.

The framework exposes the state.

The application decides what the state means operationally.

### Database work inside the event-driven runtime

The architectural heart of the MariaDB module is event-loop integration.

Database work is not only “call SQL and block.”

The MariaDB connection participates in the SNode.C event-driven runtime.

A useful model is:

```text
MariaDB socket descriptor
  -> SNode.C event receivers
      -> command continuation
          -> result callback or error callback
```

The internal `MariaDBConnection` privately participates in read, write, and exceptional-condition event receiving.

This makes the database layer part of the same event-driven architecture as the network layers.

It shows how database work can fit into the same event-driven discipline as network work.

#### `MariaDBConnection` and event receivers

The internal connection owns the active database interaction.

It handles:

- command execution,
- command continuation,
- command completion,
- read events,
- write events,
- exceptional-condition events,
- related timeouts,
- connection state.

Conceptually:

```text
database command
  -> MariaDB nonblocking operation
      -> wait for descriptor readiness
          -> continue command
              -> complete, fail, or wait again
```

The application-facing API remains callback-based.

The internal connection handles the event-driven continuation.

#### Command continuation

A database command may not complete immediately.

It may need the underlying MariaDB socket to become readable or writable.

The event loop tells the connection when progress is possible.

Then the connection continues the current command.

A compact model is:

```text
start command
  -> command needs read/write readiness
      -> event loop wakes connection
          -> command continues
              -> command completes or waits again
```

This is the database equivalent of the earlier event-driven communication model.

The specific resource is different.

The runtime discipline remains familiar.

### Database operations as commands

The MariaDB layer represents database work explicitly.

Database operations become command objects.

Command objects can be grouped into command sequences.

That gives database work structure inside the event-driven runtime.

A useful model is:

```text
command
  -> command sequence
      -> connection queue
          -> event-driven continuation
              -> success/error callback
```

This pattern is central to the database API.

The application describes ordered database work.

The connection drives that work through the event loop.

#### Async API: query, exec, transactions, commit, rollback

The asynchronous API exposes the main database operations:

| Method | Meaning |
|---|---|
| `query(...)` | execute SQL that produces rows |
| `exec(...)` | execute SQL action without row iteration as the main result |
| `startTransactions(...)` | enter transaction mode |
| `endTransactions(...)` | leave transaction mode |
| `commit(...)` | commit current transaction work |
| `rollback(...)` | roll back current transaction work |

Each method uses success and error callbacks.

The exact SQL is application-specific.

The API shape is the important teaching point:

```text
database operation
  -> success callback
  -> error callback
```

#### Sync-style metadata calls

The sync-style API exposes metadata calls such as:

| Method | Meaning |
|---|---|
| `affectedRows(...)` | report affected-row count |
| `fieldCount(...)` | report field count |

The naming distinguishes command type.

The application-facing style is still callback-oriented.

So a reader should not assume that “sync API” means arbitrary blocking procedural code in the middle of an event-driven application.

The metadata calls still fit the command/callback style.

#### `query(...)` versus `exec(...)`

The difference between `query(...)` and `exec(...)` is an application intention.

| Method | Use when |
|---|---|
| `exec(...)` | the SQL statement performs an action and row iteration is not the main result |
| `query(...)` | the SQL statement produces rows the application wants to inspect |

Examples:

```text
exec
  -> insert
  -> update
  -> delete
  -> schema modification

query
  -> select rows
  -> inspect result records
```

The database receives SQL text in both cases.

The application-facing API makes the intended use clearer.

#### Command sequences

A `MariaDBCommandSequence` allows database operations to be chained.

This matters because many database workflows are ordered.

For example:

```text
delete old rows
  -> inspect affected rows
      -> insert new row
          -> inspect affected rows
              -> query current state
```

The command sequence expresses the order.

The application does not need to write its own blocking loop.

It describes the sequence and lets the database connection advance it through the event-driven runtime.

### Transactions as sequenced database work

Transactions are not outside the event model.

They are represented as ordered database commands in the same command-sequence mechanism.

A useful model is:

```text
startTransactions
  -> exec / query
      -> commit or rollback
          -> endTransactions
```

The important point is not only that transactions exist.

The important point is that transaction flow remains visible and ordered.

A transaction can succeed.

It can fail.

A rollback may be needed.

An application may need to report degraded state, retry, compensate, or stop a workflow.

The command sequence keeps those decisions tied to explicit callbacks and errors.

### Timers and database work

Timers can trigger database work.

The database commands then continue through the MariaDB event integration.

A simple model is:

```text
timer fires
  -> start database command sequence
      -> MariaDB event integration continues the work
          -> callback reports result or error
```

This is especially relevant for IoT systems.

A service may periodically:

- aggregate sensor values,
- clean old rows,
- reconcile database state with runtime state,
- refresh derived status,
- publish stored values,
- check for pending commands.

The timer starts the work.

The database layer does not become a blocking loop.

It remains part of the same runtime world.

### Persistence service design

Database access should be designed as part of the application architecture.

It should not automatically be scattered through every protocol callback.

Sometimes direct access is acceptable.

But in larger systems, a persistence service or application-level component is often clearer.

A useful shape is:

```text
protocol callback
  -> domain operation
      -> persistence service
          -> MariaDB command sequence
```

The protocol layer interprets protocol input.

The domain layer decides what the input means.

The persistence layer decides what must be stored, updated, read, or rolled back.

This separation becomes important when several protocol roles touch the same durable state.

#### Keep database logic out of low-level protocol callbacks

A protocol callback should usually interpret protocol input, not become the whole persistence layer.

For example, a HTTP handler, MQTT callback, WebSocket message handler, or `SocketContext` method may receive an event.

It should not automatically contain all SQL construction, transaction policy, retry policy, and error handling inline.

A cleaner design is often:

```text
HTTP / MQTT / WebSocket / local-control input
  -> validate and interpret
      -> call application service
          -> schedule persistence work
              -> report result/degraded state
```

This keeps protocol code readable.

It also prevents database details from leaking into every communication boundary.

#### Database client ownership and lifetime

The lifetime of the database client should match the lifetime of the application role that owns persistence.

The test application creates clients directly in `main()` because it is a compact demonstration.

A structured application should decide ownership explicitly.

| Ownership | Fit |
|---|---|
| per request / per connection | rarely, only if isolated short work is intended |
| application or service scope | common for a persistence role |
| dedicated persistence component | good for multi-protocol systems |
| shared global | risky unless ownership and shutdown are explicit |

The design question is:

```text
What lifetime should this database connection or database service have relative to the roles that use it?
```

That is not only a coding detail.

It affects shutdown, error handling, resource limits, and system clarity.

### Persistence, failure, and backpressure

Persistence changes failure thinking.

A system may be partially healthy.

For example:

```text
HTTP route healthy
  + database unavailable
      -> degraded application behavior

MQTT connected
  + insert fails
      -> buffering, dropping, retry, or error policy needed

timer fires
  + previous sequence still pending
      -> scheduling/backpressure policy needed
```

A database failure is not always an application failure.

It may mean:

- stop accepting certain operations,
- keep reading but stop writing,
- buffer with limits,
- drop non-critical values,
- show degraded status,
- retry later,
- fail fast for administrative operations.

The MariaDB API exposes state and errors.

The application must decide the policy.

#### Persistence can introduce backpressure

Database work can accumulate.

This happens when incoming protocol activity is faster than database completion.

A useful model is:

```text
incoming protocol rate
  > database completion rate
      -> pending command sequences grow
```

This is a system-design problem.

The application needs a policy.

Possible policies include:

| Policy | Meaning |
|---|---|
| reject | refuse new work when persistence is overloaded |
| buffer with limit | queue some work, then apply a limit |
| coalesce | merge repeated updates into one write |
| drop old values | keep only recent values |
| write latest state only | persist current state instead of every event |
| slow upstream producers | apply feedback if possible |
| report degraded state | make overload visible to operators |

This connects to the earlier discussion of backpressure.

Persistence is not free.

A database boundary has throughput, latency, and failure behavior.

The application must not ignore that.

### Database state in multi-protocol IoT systems

In a multi-protocol IoT system, persistence is one boundary among several.

A possible state flow is:

```text
sensor update
  -> MQTT publish
      -> application state update
          -> database insert
              -> SSE dashboard update
```

Another system may use a different order:

```text
HTTP command
  -> validate operator request
      -> database transaction
          -> MQTT command publish
              -> WebSocket status update
```

The order depends on the system.

The important point is that persistence participates in the system flow.

It should not be treated as an isolated afterthought.

A multi-protocol system may need to coordinate:

- current runtime state,
- persisted state,
- MQTT messages,
- HTTP requests,
- WebSocket sessions,
- SSE streams,
- local-control commands,
- database transactions.

That coordination is application architecture.

The database module provides the event-integrated persistence tool.

The application decides how durable state fits into the system.

### What to remember

Remember:

- Persistence is another system boundary.
- Persistence is where selected application information survives beyond one connection, message, request, or runtime episode.
- SNode.C currently provides MariaDB-focused database support.
- Database state and runtime state are different.
- `MariaDBClient` is the application-facing database object.
- `MariaDBConnectionDetails` describes the database endpoint and credentials.
- The state-change callback exposes database availability and errors.
- `MariaDBConnection` participates in the event-driven runtime.
- Database operations are represented as commands and command sequences.
- `query(...)` and `exec(...)` express different intentions.
- Sync-style metadata calls still use callback-shaped application flow.
- Transactions are sequenced database work.
- Timers can trigger database work.
- Protocol callbacks should not automatically contain persistence logic.
- Database service ownership and lifetime are application design decisions.
- Database failures create degraded modes across protocol roles.
- Persistence can introduce backpressure.
- Chapter 29 moves from the database module to applications in `src/apps`.

### Closing perspective

Chapter 28 introduced persistence as an application-state boundary.

The path now looks like this:

```text
protocol event
  -> application meaning
      -> runtime state
          -> persistence boundary
              -> durable state
```

That boundary changes application design.

It introduces durable memory, query flow, transactions, database failure, and database backpressure into the same event-driven world as the protocol layers.

Chapter 29 now turns to the example applications in `src/apps`.

There, protocol roles, configuration, runtime behavior, and application structure can be studied together.
