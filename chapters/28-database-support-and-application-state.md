## Database Support and Application State

### From protocol boundaries to persistence boundaries

Chapter 27 described IoT systems as collections of communication boundaries. Chapter 28 adds a different kind of boundary: persistence. Communication boundaries decide how information moves between active participants; persistence boundaries decide what information should remain after the immediate conversation is over.

A protocol boundary asks:

```text
How does information move between active participants?
```

A persistence boundary asks:

```text
What information should remain after the immediate conversation is over?
```

That second question changes the architecture of an application. The application now has to decide what belongs in memory, what belongs in durable storage, when database work should be started, how database results flow back into the event-driven application, what happens when the database is unavailable, and how persistence interacts with protocol roles such as HTTP, MQTT, WebSocket, SSE, and local-control interfaces.

A useful model is:

```text
protocol event
  -> application interpretation
      -> runtime state
          -> optional persistence boundary
              -> durable application state
```

Persistence is not automatically part of every request or every message. It is an application-state boundary that should be chosen deliberately.

Figure~\ref{fig:persistence-boundary} shows the boundary that should stay visible when database support enters an SNode.C application. The upper lane stays on the transient communication side: peer connections, protocol contexts, and application interpretation live in the runtime and give incoming events their application meaning. The lower lane stays on the durable-state side: once the application has decided that something should survive process lifetime, the work crosses the persistence boundary and becomes explicit persistence work.

![Persistence boundary in an SNode.C application: protocol contexts translate peer events into application meaning, application state decides what is worth keeping, and the database client belongs behind an explicit persistence boundary rather than inside transport or protocol mechanics.](figures/pdf/fig-17-persistence-boundary.pdf){#fig:persistence-boundary width=90% latex-placement="tbp"}

Figure~\ref{fig:persistence-boundary} therefore makes two decisions visible at the same time. First, protocol and transport activity do not automatically imply durable storage. Second, persistence begins with an application-state decision: what changed, what matters, and what is worth keeping. Only after that decision does the database client, its command API, and the durable store become part of the flow.

::: {.snodec-rule title="Persistence rule"}
Persist application facts, not raw transport accidents.
:::

### Persistence as an application-state boundary

A database connection should not be read as another transport protocol. An HTTP endpoint, MQTT session, WebSocket connection, Bluetooth link, or Unix-domain control socket is usually a communication boundary between active participants. A database connection is different. It is a persistence and query boundary: it stores state, retrieves state, changes state, and may become the durable memory of a larger system.

A compact comparison helps:

| Concern | Protocol boundary | Persistence boundary |
|---|---|---|
| main purpose | exchange information | store/retrieve durable information |
| lifetime | often connection, session, request, or message scoped | survives beyond runtime episodes |
| examples | HTTP, MQTT, WebSocket, Bluetooth | MariaDB database |
| failure mode | peer unreachable, protocol error, timeout | connection failure, query failure, transaction failure |
| application question | what did the peer say? | what should be remembered? |
| SNode.C concern | event-driven communication | event-integrated persistence work |

This distinction matters because database work should not be treated as random helper code hidden inside protocol callbacks. It belongs to the application-state architecture. A protocol callback may trigger a persistence decision, but the database boundary should still remain visible as its own architectural concern.

### What SNode.C currently supports

The database support in SNode.C has a concrete scope. The current concrete database module is MariaDB-focused. It should not be presented as a generic multi-backend ORM or database-independent abstraction.

The accurate statement is:

::: {.snodec-note title="MariaDB scope note"}
SNode.C currently provides a MariaDB integration layer shaped to work inside the same event-driven runtime discipline as the rest of the framework.
:::

This narrower statement keeps the chapter aligned with the implementation. It lets the chapter focus on what the code actually provides:

```text
MariaDB client object
  -> connection details
      -> event-integrated MariaDB connection
          -> command objects
              -> command sequences
                  -> callbacks for result and error handling
```

#### MariaDB-focused database module

The MariaDB module is added only when `libmariadb` is found by CMake; otherwise the `db-mariadb` target is not created. When it is available, the module builds the shared library:

```text
db-mariadb
```

and installs MariaDB-specific headers under the MariaDB database include path.

For ordinary application use, the public surface has a clear source side and build side. The source-side front door is the MariaDB client header:

```cpp
#include <database/mariadb/MariaDBClient.h>
```

The matching build-side component is:

```text
db-mariadb
```

That header is the source-facing entry to the normal MariaDB client abstraction. Application code should not include individual command headers merely to use the usual client API; those lower headers belong behind the public client surface unless the application directly names a lower command type. The component supplies the binary/library surface for the same MariaDB module.

The module contains the concrete pieces needed for MariaDB integration:

- `MariaDBClient`,
- `MariaDBClientASyncAPI`,
- `MariaDBClientSyncAPI`,
- `MariaDBConnection`,
- `MariaDBConnectionDetails`,
- `MariaDBCommand`,
- asynchronous and sync-style command variants,
- `MariaDBCommandSequence`,
- `MariaDBLibrary`,
- asynchronous commands,
- sync-style metadata commands.

The module structure presents this part of the framework as concrete MariaDB support integrated with the runtime. It is not a broad ORM layer. It is not a generic database-independent abstraction. It is event-integrated MariaDB support.

#### Test application as demonstration, not production model

The `testmariadb` application should be read as a demonstration and test program for the API shape and runtime integration, not as a production persistence architecture. A test application can be compact, direct, and repetitive because its purpose is to exercise and show the pieces.

That is useful. It can demonstrate database configuration, runtime initialization, construction of connection details, use of client objects, state-change reporting, command execution, result handling, metadata access, command sequencing, transaction flow, and scheduling patterns.

But a real application must make its own architectural decisions.

| Test app demonstrates | Production code should decide |
|---|---|
| API shape | ownership and lifetime of the database service |
| command chaining | domain-level persistence workflow |
| state callback | operational reporting policy |
| transactions | transaction policy |
| timers | scheduling policy |
| direct values | secure configuration and secret handling |

The test application shows how the pieces work. A real application must decide how persistence belongs to its own roles, configuration, security model, resource limits, and failure policy.

### Runtime state and database state

Runtime state and database state are not the same thing. Runtime state exists while the application is running. Database state survives beyond the current runtime episode.

A useful distinction is:

```text
runtime state
  -> live connections
  -> sessions
  -> timers
  -> pending work
  -> queues
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

The decision is not always obvious. Some information may exist in both places:

```text
database
  -> durable source of truth

runtime cache
  -> current fast-access representation
```

The application must decide how those representations are synchronized. A cache without a synchronization policy is not architecture; it is an assumption.

#### What belongs where?

A practical table helps:

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

This table is not a rulebook. It is a way to force the application to say which state is transient, which state is durable, and which state is cached. The database should not become a dumping ground for every transient detail. Runtime memory should not pretend to be durable when it is not. The persistence boundary should be explicit.

### `MariaDBClient` as the application-facing database object

The main application-facing object is `database::mariadb::MariaDBClient`. It combines the asynchronous command API and the sync-style metadata API, owns the internal connection object, stores the connection details, and reports connection state through a state-change callback.

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

This fits SNode.C’s runtime style. The application issues database operations and can also observe whether the database resource is connected, unavailable, or in an error state.

A database client is not the same kind of configured communication role as a socket server or client instance. It is an application-facing persistence object integrated with the runtime. It may belong to a role or service in the application, but it is not itself the same conceptual object as a registered runtime-visible socket instance.

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

The `connectionName` is especially useful for diagnostics. A named database connection is easier to understand in logs than an anonymous one.

The credential fields deserve care. A test program may place credentials close to the example to keep the demonstration compact. A real application needs an explicit policy for configuration, secret storage, deployment, and logging.

#### State-change callback

The state-change callback makes the database connection visible to the application. That matters because a database is a runtime participant. It may be connected, disconnected, unavailable, misconfigured, rejected by authentication, or failed during operation.

The callback gives the application a place to react:

```text
database connected
  -> enable persistence-dependent work

database unavailable
  -> report degraded state
      -> pause periodic writes
          -> keep protocol roles alive if possible
```

The exact policy belongs to the application. The framework exposes the state. The application decides what the state means operationally.

The state callback is database observability at the application boundary. It makes the persistence role visible instead of hiding database availability inside failed commands.

### A minimal MariaDB client example

The following listing is intentionally smaller than the repository's `testmariadb` application. It shows the shape of ordinary application use: configure connection details, construct the database client, observe connection state, submit SQL work, continue through callbacks, and then start the SNode.C runtime.

For the SQL statements below, assume a small table such as:

```sql
CREATE DATABASE snodec;

CREATE TABLE measurements (
    sensor VARCHAR(64) NOT NULL,
    value DOUBLE NOT NULL
);
```

This setup note is only there to make the example concrete. Chapter 28 is not a MariaDB administration chapter. A real deployment also needs a deliberate policy for database users, privileges, credentials, schema migration, backup, and secret handling.

```cpp
#include <core/SNodeC.h>
#include <database/mariadb/MariaDBClient.h>

#include <iostream>
#include <mysql.h>
#include <string>

int main(int argc, char* argv[]) {
    core::SNodeC::init(argc, argv);

    const database::mariadb::MariaDBConnectionDetails details = {
        .connectionName = "measurements-db",
        .hostname = "localhost",
        .username = "snodec",
        .password = "<password>",
        .database = "snodec",
        .port = 3306,
        .socket = "",
        .flags = 0,
    };

    database::mariadb::MariaDBClient db(details, [](const database::mariadb::MariaDBState& state) {
        if (state.error != 0) {
            std::cerr << "MariaDB state error " << state.error << ": "
                      << state.errorMessage << "\n";
        } else if (state.connected) {
            std::cout << "MariaDB connected\n";
        } else {
            std::cout << "MariaDB disconnected\n";
        }
    });

    db.exec(
          "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)",
          [&db]() {
              db.affectedRows(
                  [](my_ulonglong rows) {
                      std::cout << "insert affected rows: " << rows << "\n";
                  },
                  [](const std::string& error, unsigned int number) {
                      std::cerr << "affectedRows error " << number << ": "
                                << error << "\n";
                  });
          },
          [](const std::string& error, unsigned int number) {
              std::cerr << "insert error " << number << ": " << error << "\n";
          })
      .query(
          "SELECT sensor, value FROM measurements",
          [](const MYSQL_ROW row) {
              if (row != nullptr) {
                  std::cout << "measurement: " << row[0] << " = " << row[1] << "\n";
              } else {
                  std::cout << "measurement query complete\n";
              }
          },
          [](const std::string& error, unsigned int number) {
              std::cerr << "query error " << number << ": " << error << "\n";
          });

    return core::SNodeC::start();
}
```

The example deliberately keeps the database details local so that the API shape is visible. That is not a production credential policy. Production code should not hard-code database passwords in the source; it should read them from a controlled configuration or secret mechanism and should avoid logging secret material.

Nothing in this listing makes the database a transport peer. The database client is an application-owned persistence boundary. The SQL work is submitted before the runtime starts, but its progress and completion belong to the event-driven execution model. The row callback receives individual rows; a `nullptr` row marks the end of that result stream. For the database case, the companion source tree is `MariaDB-Minimal`.

The corresponding build-side dependency is the MariaDB component:

```cmake
target_link_libraries(myapp PRIVATE snodec::db-mariadb)
```

That target exists only in SNode.C builds where `libmariadb` was found. The source-side public header and the build-side component therefore form the usual pair:

```text
source side:
  <database/mariadb/MariaDBClient.h>

build side:
  snodec::db-mariadb
```

### Database work inside the event-driven runtime

The architectural heart of the MariaDB module is event-loop integration. Database work participates in the SNode.C event-driven runtime instead of simply calling SQL and blocking.

A useful model is:

```text
MariaDB socket descriptor
  -> SNode.C event receivers
      -> command continuation
          -> result callback or error callback
```

Internally, `MariaDBConnection` participates as a read, write, and exceptional-condition event receiver. The database descriptor becomes part of the same event-driven discipline as socket descriptors. It handles command execution, command continuation, command completion, read events, write events, exceptional-condition events, related timeouts, and connection state.

Conceptually:

```text
database command
  -> MariaDB nonblocking operation
      -> wait for descriptor readiness
          -> continue command
              -> complete, fail, or wait again
```

The application-facing API remains callback-shaped. The internal connection handles the event-driven continuation.

Event-integrated database work avoids blocking the application around ordinary command progress, but it does not make database latency disappear. A slow database is still slow. A saturated database is still saturated. The difference is that database progress can be coordinated with the same event-driven runtime discipline as the network layers.

#### `MariaDBConnection` and event receivers

The internal connection owns the active database interaction. It tracks the active command, queues command sequences, observes connection state, and reacts to read, write, and exceptional-condition readiness.

A compact source-shaped model is:

```text
start command
  -> wait for read/write readiness or completion
      -> commandContinue(...)
          -> commandCompleted()
```

This is the database equivalent of the earlier event-driven communication model. The specific resource is different. The runtime discipline remains familiar.

#### Command continuation

A database command may not complete immediately. It may need the underlying MariaDB socket to become readable or writable. The event loop tells the connection when progress is possible. Then the connection continues the current command.

A compact model is:

```text
start command
  -> command needs read/write readiness
      -> event loop wakes connection
          -> command continues
              -> command completes or waits again
```

The point is not the exact MariaDB C API detail. Database work is expressed as explicit continuation, not as an invisible blocking detour inside a protocol callback.

### Database work as commands and command sequences

The MariaDB layer represents database work explicitly. Database operations become command objects. Command objects can be grouped into command sequences. That gives database work structure inside the event-driven runtime.

A useful model is:

```text
command
  -> command sequence
      -> connection queue
          -> event-driven continuation
              -> success/error callback
```

This pattern is central to the database API. The application describes ordered database work. The connection drives that work through the event loop.

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

Each method uses success and error callbacks. The exact SQL is application-specific. The API shape is the important teaching point:

```text
database operation
  -> success callback
  -> error callback
```

The source uses the plural method names `startTransactions(...)` and `endTransactions(...)`; prose may speak about a transaction, but code-form sections should keep the actual names.

#### Sync-style metadata calls

The sync-style API exposes metadata calls such as:

| Method | Meaning |
|---|---|
| `affectedRows(...)` | report affected-row count |
| `fieldCount(...)` | report field count |

“Sync-style” here identifies metadata-style command surfaces; the application-facing flow still uses callbacks. A reader should not assume that sync-style metadata calls mean arbitrary blocking procedural database code inside an event-driven application.

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

The database receives SQL text in both cases. The application-facing API makes the intended use clearer.

#### Command sequences

A `MariaDBCommandSequence` allows database operations to be chained. The sequence itself is also an API surface: it inherits the asynchronous and sync-style API shapes so commands can be appended in order.

This matters because many database workflows are ordered. For example:

```text
delete old rows
  -> inspect affected rows
      -> insert new row
          -> inspect affected rows
              -> query current state
```

The command sequence expresses the order. The application does not need to write its own blocking loop. It describes the sequence and lets the database connection advance it through the event-driven runtime.

A command sequence is not the same thing as a transaction:

```text
command sequence
  -> ordered database work

transaction
  -> database consistency boundary represented through ordered commands
```

Both can appear together, but they are different ideas.

### Transactions as sequenced database work

Transactions are not outside the event model. They are represented as ordered database commands in the same command-sequence mechanism.

A useful model is:

```text
startTransactions
  -> exec / query
      -> commit or rollback
          -> endTransactions
```

The important point is not simply that transactions exist. Transaction flow remains visible and ordered. A transaction can succeed. It can fail. A rollback may be needed. An application may need to report degraded state, retry, compensate, or stop a workflow.

A transaction is not outside the event model; it is a policy and ordering boundary expressed through database commands and callbacks.

#### A compact transaction sequence

A command sequence keeps ordered database work visible. Transaction flow is not hidden behind a helper that silently blocks. The sequence shows when transaction mode begins, which work belongs to the transaction, when the commit is requested, and when transaction mode is left again.

```cpp
db.startTransactions(
      []() {
          // Transaction mode enabled.
      },
      [](const std::string& error, unsigned int number) {
          // Report transaction-start error.
      })
  .exec(
      "INSERT INTO measurements(sensor, value) VALUES ('humidity', 61.0)",
      []() {
          // Insert command accepted.
      },
      [](const std::string& error, unsigned int number) {
          // Report insert error.
      })
  .commit(
      []() {
          // Transaction committed.
      },
      [](const std::string& error, unsigned int number) {
          // Report commit error.
      })
  .endTransactions(
      []() {
          // Transaction mode disabled.
      },
      [](const std::string& error, unsigned int number) {
          // Report transaction-end error.
      });
```

The source uses the plural method names `startTransactions(...)` and `endTransactions(...)`; the listing keeps those exact names. A rollback path would use the same command-sequence shape with `rollback(...)` instead of, or before, a later `commit(...)`, depending on the application policy. The important architectural point is that transaction boundaries remain explicit and ordered.

### Timers and database work

Timers can trigger database work. The database commands then continue through the MariaDB event integration.

A simple model is:

```text
timer fires
  -> start database command sequence
      -> MariaDB event integration continues the work
          -> callback reports result or error
```

This is especially relevant for IoT systems. A service may periodically aggregate sensor values, clean old rows, reconcile database state with runtime state, refresh derived status, publish stored values, or check for pending commands.

The timer starts the work. The database layer does not become a blocking loop. It remains part of the same runtime world.

### Persistence service design

Database access should be designed as part of the application architecture. It should not automatically be scattered through every protocol callback. Sometimes direct access is acceptable. But in larger systems, a persistence service or application-level component is often clearer.

A useful shape is:

```text
protocol callback
  -> domain operation
      -> persistence service
          -> MariaDB command sequence
```

The protocol layer interprets protocol input. The domain layer decides what the input means. The persistence layer decides what must be stored, updated, read, or rolled back.

In the boundary language of Chapter 27, persistence may be its own role or service, especially when several protocol surfaces touch the same durable state.

#### Keep database logic out of low-level protocol callbacks

A protocol callback should usually interpret protocol input, not become the whole persistence layer. For example, an HTTP handler, MQTT callback, WebSocket message handler, or `SocketContext` method may receive an event. It should not automatically contain all SQL construction, transaction policy, retry policy, and error handling inline.

A cleaner design is often:

```text
HTTP / MQTT / WebSocket / local-control input
  -> validate and interpret
      -> call application service
          -> schedule persistence work
              -> report result/degraded state
```

This keeps protocol code readable. It also prevents database details from leaking into every communication boundary.

#### Database client ownership and lifetime

The lifetime of the database client should match the lifetime of the application role or service that owns persistence. The test application creates clients directly in `main()` because it is a compact demonstration. A structured application should decide ownership explicitly.

| Ownership | Fit |
|---|---|
| per request / per connection | rarely, only if isolated short work is intended |
| application or service scope | often the clearest default for persistence ownership |
| dedicated persistence component | good for multi-protocol systems |
| shared global | risky unless ownership and shutdown are explicit |

The design question is:

```text
What lifetime should this database connection or database service have relative to the roles that use it?
```

That affects shutdown, error handling, resource limits, and system clarity.

### Persistence, failure, and backpressure

Persistence changes failure thinking. A system may be partially healthy:

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

A database failure is not always an application failure. It may mean stop accepting certain operations, keep reading but stop writing, buffer with limits, drop non-critical values, show degraded status, retry later, or fail fast for administrative operations.

The MariaDB API exposes state and errors. The application must decide the policy.

Chapter 20’s vocabulary still applies: timeout, retry, shutdown, failure state, and degraded behavior must be decided at the boundary that owns the failing work.

#### Persistence can introduce backpressure

Database work can accumulate. This happens when incoming protocol activity is faster than database completion.

A useful model is:

```text
incoming protocol rate
  > database completion rate
      -> pending command sequences grow
```

This is a system-design problem. The application needs a policy.

| Policy | Meaning |
|---|---|
| reject | refuse new work when persistence is overloaded |
| buffer with limit | queue some work, then apply a limit |
| coalesce | merge repeated updates into one write |
| drop old values | keep only recent values |
| write latest state only | persist current state instead of every event |
| slow upstream producers | apply feedback if possible |
| report degraded state | make overload visible to operators |

Persistence is not free. A database boundary has throughput, latency, and failure behavior. A persistence queue without a limit is not a policy; it is delayed failure.

### Database state in multi-protocol IoT systems

In a multi-protocol IoT system, persistence is one boundary among several. A possible state flow is:

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

The correct order depends on the domain. Sometimes persistence follows communication; sometimes persistence authorizes or precedes communication.

persistence participates in the system flow. It should not be treated as an isolated afterthought.

A multi-protocol system may need to coordinate:

- current runtime state,
- persisted state,
- MQTT messages,
- HTTP requests,
- WebSocket sessions,
- SSE streams,
- local-control commands,
- database transactions.

That coordination is application architecture. The database module provides the event-integrated persistence tool. The application decides how durable state fits into the system.

::: {.snodec-remember title="What to remember"}
- Persistence is another system boundary.
- Persistence is where selected application information survives beyond one connection, message, request, or runtime episode.
- SNode.C currently provides MariaDB-focused database support through `db-mariadb`.
- Database state and runtime state are different.
- `MariaDBClient` is the application-facing database object.
- `MariaDBConnectionDetails` describes the database endpoint and credentials.
:::

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

That boundary changes application design. It introduces durable memory, query flow, transactions, database failure, and database backpressure into the same event-driven world as the protocol layers.

Chapter 28 introduced persistence as a boundary. Chapter 29 now turns to complete applications, where protocol roles, persistence choices, configuration, runtime lifecycle, and diagnostics meet in executable form.
