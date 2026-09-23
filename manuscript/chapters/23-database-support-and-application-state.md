## Database Support and Application State {#database-support-and-application-state}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Distinguish transient acceptance, queued database work and committed state.
- **O2.** Observe command ordering, SQL failure and read-back after client restart.
- **O3.** Choose persistence ownership, transaction decisions and bounded overload policy.
:::

\index{database support}
\index{application state}
\index{persistence}

### From protocol boundaries to persistence boundaries

Persistence answers a question that protocols alone cannot answer: which information should survive after a connection, request, message, or process has ended?

A protocol boundary asks how information moves; persistence asks what remains afterward. The application must choose memory or durable storage, when to start database work, how results return to its event-driven roles, and what happens when storage is unavailable. A protocol event receives domain meaning before it causes an optional persistence decision.

Figure \ref{fig:persistence-boundary} separates transient connections, contexts and application interpretation from explicitly chosen durable work. Queues and client memory remain on the transient side; crossing into database work does not make submission a commit. The MariaDB client, connection and command API implement that work after the application decides what matters.

![Persistence boundary in an SNode.C application: protocol contexts translate peer events into application meaning, application state decides what is worth keeping, and the database client submits explicit persistence work. Queued work and client memory are still transient; the diagram does not equate submission with a durable commit.](assets/figures/pdf/fig-17-persistence-boundary.pdf){#fig:persistence-boundary width=90% latex-placement="tbp"}

::: {.snodec-rule title="Persistence rule"}
Persist application facts, not raw transport accidents.
:::

\index{persistence boundary}
\index{application-state boundary}

A database client still communicates through a protocol and transport. Its role in this application is persistence and query, rather than the device or observer conversation. It stores state, retrieves state, changes state, and may become the durable memory of a larger system. Read the distinction by application purpose: HTTP, MQTT, WebSocket, Bluetooth, and Unix-domain sockets can carry conversations whose accepted facts the persistence role later records.

A compact comparison helps:

| Concern | Protocol boundary | Persistence boundary |
|---|---|---|
| main purpose | exchange information | store/retrieve durable information |
| lifetime | often connection, session, request, or message scoped | survives beyond runtime episodes |
| examples | HTTP, MQTT, WebSocket, Bluetooth | MariaDB database |
| failure mode | peer unreachable, protocol error, timeout | connection failure, query failure, transaction failure |
| application question | what did the peer say? | what should be remembered? |
| SNode.C concern | event-driven communication | event-integrated persistence work |

A protocol callback may trigger a persistence decision, but database work belongs to the application-state architecture, with its own lifetime and failure policy.

### The MariaDB module and its public client

The current concrete database module is MariaDB-focused, not a generic multi-backend ORM. It integrates a client, connection details, queued commands and result/error callbacks into the event-driven runtime. CMake creates `db-mariadb` only when `libmariadb` is found and installs its MariaDB-specific headers.

\index{MariaDB}
\index{database module}

Ordinary application use begins with the public client header:

```cpp
#include <database/mariadb/MariaDBClient.h>
```

The matching component is `db-mariadb`. Include lower command headers only when directly naming a lower command type; ordinary use goes through the public client.

The module provides these public types and operations:

- `MariaDBClient` with asynchronous and sync-style APIs;
- `MariaDBConnection` and its `MariaDBConnectionDetails`;
- command variants and `MariaDBCommandSequence`;
- `MariaDBLibrary`.

These types let the reader trace ownership from the public client to a connection and its queued commands. Keep that trace concrete when moving from the small listing to a larger persistence service.

The repository's `testmariadb` demonstrates configuration, runtime setup, client construction, state callbacks, commands, metadata, sequences, transactions and timers. Its compact API exercise is not a production persistence architecture.

| Test app demonstrates | Production code should decide |
|---|---|
| API shape | ownership and lifetime of the database service |
| command chaining | domain-level persistence workflow |
| state callback | operational reporting policy |
| transactions | transaction policy |
| timers | scheduling policy |
| direct values | secure configuration and secret handling |

### Runtime state and database state

\index{runtime state}
\index{database state}

Runtime state includes connections, timers, pending work and caches. Database state records selected facts that should survive the current process, such as measurement history, users, audit records and durable configuration.

The decision is not always obvious. Some information may exist in both places: the database as durable source of truth, and a runtime cache as the current fast-access representation. The application must decide how those representations are synchronized. A cache without a synchronization policy is not architecture; it is an assumption.

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

This table forces the application to say which state is transient, durable, or cached; it is not a rulebook. The database should not become a dumping ground for every transient detail. Runtime memory should not pretend to be durable when it is not. The persistence boundary should be explicit.

\index{MariaDBClient@\texttt{MariaDBClient}}
\index{MariaDBConnectionDetails@\texttt{MariaDBConnectionDetails}}
\index{database client}

The main application-facing object is `database::mariadb::MariaDBClient`. It combines the asynchronous command API and the sync-style metadata API, owns the internal connection object, stores the connection details, and reports connection state through a state-change callback.

The state callback receives an error number, error message and connected flag.

A database client is an application-facing persistence object integrated with the runtime, distinct from a socket instance. It may belong to a role or service in the application, but it is not itself the same conceptual object as a socket instance.

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

The state callback exposes connected, disconnected, unavailable, misconfigured, authentication-rejected or failed operation states. The application chooses what follows: enable persistence-dependent work, pause periodic writes, report degradation or keep other protocol roles alive. Database availability should not be hidden inside individual failed commands.

### A minimal MariaDB client example

\index{MariaDB!minimal client example}

The following listing is intentionally smaller than the repository's `testmariadb` application. It shows the shape of ordinary application use: configure connection details, construct the database client, observe connection state, submit SQL work, continue through callbacks, and then start the SNode.C runtime.

For the SQL statements below, assume a small table such as:

```sql
CREATE DATABASE snodec;
USE snodec;

CREATE TABLE measurements (
    sensor VARCHAR(64) NOT NULL,
    value DOUBLE NOT NULL
);
```

A deployment also needs deliberate users, privileges, credentials, schema migration, backup and secret handling.

<!-- snodec-source: companion/examples/MariaDB-Minimal/main.cpp -->
```cpp
#include <core/SNodeC.h>
#include <database/mariadb/MariaDBClient.h>
#include <Log.h>

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
            snode::log::application().error() << "MariaDB state error " << state.error << ": "
                       << state.errorMessage;
        } else if (state.connected) {
            snode::log::application().trace() << "MariaDB connected";
        } else {
            snode::log::application().trace() << "MariaDB disconnected";
        }
    });

    db.exec(
          "INSERT INTO measurements(sensor, value) VALUES ('temperature', 23.5)",
          [&db]() {
              db.affectedRows(
                  [](my_ulonglong rows) {
                      snode::log::application().trace() << "insert affected rows: " << rows;
                  },
                  [](const std::string& error, unsigned int number) {
                      snode::log::application().error() << "affectedRows error " << number << ": "
                                 << error;
                  });
          },
          [](const std::string& error, unsigned int number) {
              snode::log::application().error() << "insert error " << number << ": " << error;
          })
      .query(
          "SELECT sensor, value FROM measurements",
          [](const MYSQL_ROW row) {
              if (row != nullptr) {
                  snode::log::application().trace() << "measurement: " << row[0] << " = " << row[1];
              } else {
                  snode::log::application().trace() << "measurement query complete";
              }
          },
          [](const std::string& error, unsigned int number) {
              snode::log::application().error() << "query error " << number << ": " << error;
          });

    return core::SNodeC::start();
}
```

The example deliberately keeps the database details local so that the API shape is visible. That is not a production credential policy. Production code should not hard-code database passwords in the source; it should read them from a controlled configuration or secret mechanism and should avoid logging secret material.

The database is a communicating peer, but the application uses this client as its persistence boundary. The SQL work is submitted before the runtime starts, but its progress and completion belong to the event-driven execution model. The row callback receives individual rows; a `nullptr` row marks the end of that result stream. For the database case, the companion source tree is `MariaDB-Minimal`.

The corresponding build-side dependency is the MariaDB component:

```cmake
target_link_libraries(myapp PRIVATE snodec::db-mariadb)
```

That target exists only when `libmariadb` was found. It pairs with the public client header used above.

### Database work inside the event-driven runtime

\index{MariaDBConnection@\texttt{MariaDBConnection}}
\index{event-driven database access}

`MariaDBConnection` participates as a read, write and exceptional-condition event receiver. It owns the active database interaction, tracks the active command, queues sequences and handles readiness, timeouts and connection state.

A command starts a MariaDB nonblocking operation. If it needs descriptor readiness, the event loop wakes the connection to continue it; it then completes, fails or waits again. Application callbacks receive the result or error. The application does not need its own blocking progress loop.

Event integration leaves other callbacks runnable while ordinary command progress waits, but it does not remove database latency or saturation. Pending sequences still need an application policy.

Database operations become explicit command objects and ordered sequences.

\index{database commands}
\index{command sequences}
\index{query()@\texttt{query()}}
\index{exec()@\texttt{exec()}}

The asynchronous API exposes the main database operations:

| Method | Meaning |
|---|---|
| `query(...)` | execute SQL that produces rows |
| `exec(...)` | execute SQL action without row iteration as the main result |
| `startTransactions(...)` | enter transaction mode |
| `endTransactions(...)` | leave transaction mode |
| `commit(...)` | commit current transaction work |
| `rollback(...)` | roll back current transaction work |

Each method uses success and error callbacks. The exact SQL is application-specific; the important teaching point is that every database operation has an explicit success path and an explicit error path.

The plural names `startTransactions(...)` and `endTransactions(...)` select transaction mode; they do not make a command sequence an automatic all-or-nothing operation.

The sync-style API exposes metadata calls such as:

| Method | Meaning |
|---|---|
| `affectedRows(...)` | report affected-row count |
| `fieldCount(...)` | report field count |

“Sync-style” here identifies metadata-style command surfaces; the application-facing flow still uses callbacks. These calls read state that the MariaDB client library already has after a completed command or result step. They do not stand for arbitrary blocking SQL work inside an event-driven application.

`exec(...)` covers action statements such as insert, update, delete and schema modification. `query(...)` selects row iteration. Both send SQL text; the API makes the intended result handling explicit.

### Command sequences and callback ordering

A `MariaDBCommandSequence` allows database operations to be chained. The sequence itself is also an API surface: it inherits the asynchronous and sync-style API shapes so commands can be appended in order.

Many database workflows are ordered. For example:

```text
delete old rows
  -> inspect affected rows
      -> insert new row
          -> inspect affected rows
              -> query current state
```

The command sequence expresses the order. The application does not need to write its own blocking loop. It describes the sequence and lets the database connection advance it through the event-driven runtime.

A command sequence is not the same thing as a transaction. A command sequence expresses ordered database work. A transaction is a database consistency boundary represented through ordered commands.

Both can appear together, but they are different ideas.

The call shape is important. A chained call appends to the command sequence returned by the previous operation:

```cpp
db.exec(...).query(...);
```

Here the `query(...)` belongs to the same sequence as the preceding `exec(...)`. It is not a second immediate operation on the client object.

Starting async work from inside a callback has different meaning:

```cpp
db.exec(
    ...,
    [&db]() {
        db.exec(...);
    },
    ...);
```

The inner `exec(...)` creates a new command sequence and queues it on the same connection. It does not splice itself into the current sequence, and it does not jump ahead of commands already chained onto that sequence.

Metadata calls such as `affectedRows(...)` are the narrow exception to this “queue more SQL work” rule. They are synchronous metadata reads of the just-completed command state. Used inside an `exec(...)` success callback, `affectedRows(...)` observes the completed command before the connection advances to the next queued SQL command.

A compact mental model is that a chained call appends to the current returned sequence, an async call created inside a callback creates a new queued sequence, and a metadata call inside a callback reads already available command/result state immediately.

Sequence order also has a failure boundary. A success callback means that particular database operation succeeded; it does not mean all later chained operations will succeed. Likewise, accepting a measurement into an in-memory model does not make it durable merely because an asynchronous database command was queued. Decide where the application reports durable acceptance, and make the transaction's success or failure observable there. A reconnect policy can restore a database connection, but it cannot by itself decide whether replaying an interrupted application operation would duplicate a write.

### Transactions as sequenced database work

\index{transactions}
\index{commit@\texttt{commit}}
\index{rollback@\texttt{rollback}}

Transactions use the same ordered command mechanism but add a database consistency boundary. The application must choose whether to commit, roll back, retry, compensate or stop after an error.

The following success-path illustration shows transaction mode, queued work, commit and departure from transaction mode. Its comment-only error callbacks do not implement recovery.

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

The source uses the plural method names `startTransactions(...)` and `endTransactions(...)`; the listing keeps those exact names. The current queue advances after a command-level SQL error as well as after success while the connection remains usable. Consequently, the chained `commit(...)` above is already queued even if the insert later fails. The sequence does not automatically branch to rollback.

Queuing `db.rollback(...)` from that insert’s error callback would create a new sequence behind the remaining commands; it would not jump ahead of this prequeued commit. A production workflow that must choose commit or rollback should enqueue the dependent operation only after observing the required outcome and should prevent unrelated work from interleaving on that connection. The transaction sketch teaches API order, not that complete failure policy.

Timers can start database sequences for periodic aggregation, row cleanup, reconciliation, derived status, stored-value publication or pending-command checks. The event loop continues the work; its callbacks report completion or failure. A new timer tick must account for earlier work still pending.

### Persistence service design

\index{persistence service design}
\index{database client ownership}

A protocol callback interprets input; a domain operation decides what it means; a persistence service owns durable work. Direct access can be acceptable for a small example, but larger applications should avoid repeating SQL, transaction and retry policy across HTTP, MQTT, WebSocket and local-control callbacks.

In the boundary language of Chapter 22, a persistence service is especially useful when several protocol surfaces touch the same durable state. Validate and interpret input first, then schedule persistence and report success, failure or degraded state.

The lifetime of the database client should match the lifetime of the application role or service that owns persistence. The test application creates clients directly in `main()` because it is a compact demonstration. A structured application should decide ownership explicitly.

| Ownership | Fit |
|---|---|
| per request / per connection | rarely, only if isolated short work is intended |
| application or service scope | often the clearest default for persistence ownership |
| dedicated persistence component | good for multi-protocol systems |
| shared global | risky unless ownership and shutdown are explicit |

Choose the connection or service lifetime relative to its callers; that choice affects shutdown, errors and resource limits.

### Persistence, failure, and backpressure

\index{persistence!backpressure}
\index{database failure}

Persistence changes failure thinking. A system may be partially healthy:

| Situation | Likely design question |
|---|---|
| HTTP route is healthy, but the database is unavailable | Should the application report degraded behavior? |
| MQTT is connected, but an insert fails | Should the application buffer, drop, retry, or report an error? |
| A timer fires while the previous sequence is still pending | What scheduling or backpressure policy applies? |

A database failure is not always an application failure. It may mean stop accepting certain operations, keep reading but stop writing, buffer with limits, drop non-critical values, show degraded status, retry later, or fail fast for administrative operations.

The MariaDB API exposes state and errors. The application must decide the policy.

Chapter 15’s vocabulary still applies: timeout, retry, shutdown, failure state, and degraded behavior must be decided at the boundary that owns the failing work.

When incoming protocol activity is faster than database completion, pending command sequences accumulate. Event integration keeps other callbacks runnable; it does not bound that queue for the application.

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

Ordering follows the domain contract. A sensor update may arrive over MQTT, update application state, be inserted into the database, then appear on SSE. An operator HTTP command may instead require validation and a committed transaction before publishing an MQTT command and updating WebSocket status. Persistence can follow, authorize or precede communication; choose which outcome each observer may truthfully report.

### Observe acceptance and durability separately

For a controlled integration exercise, use an isolated database and the companion `MariaDB-Minimal` schema. Record the table’s row count before running the program, then observe the insert callback and query rows. Query the table from a separate database client after the program ends. The independent query is the durable-state observation; the connected callback alone is not.

Run a failure case in the same isolated environment by using a nonexistent table name in a scratch copy of the insert. Record the error callback and whether the following query still runs. That distinguishes command failure from connection failure and makes the queue behavior above visible. Restore the scratch statement before testing a deliberate transaction and rollback.

A useful transaction exercise inserts a uniquely identified test row, deliberately fails the next statement, and verifies the chosen rollback policy from another connection. Do not infer rollback from an error log. The expected row count must agree with the declared policy. Keep setup and cleanup confined to the dedicated test schema; the printed measurement example does not supply general migration or retry machinery.

This exercise requires a running MariaDB service, suitable credentials, and a controlled schema.

\index{MariaDBClient@\texttt{MariaDBClient}!diagnostic identity}

The database boundary can now participate in semantic diagnostics as well as in the event loop. `MariaDBClient` accepts an optional instance-name argument after its connection details and state callback. That name gives the database connection a useful diagnostic identity; it does not create a socket server, an MQTT role, or a separate configuration hierarchy.

The compact program uses the public application logger for its own observations. Framework-owned database records and application decisions remain different evidence. A successful connection is not a successful transaction, and a queued command is not proof that durable state has changed. Preserve those distinctions when correlating database records with HTTP, SSE, or MQTT activity.

Use isolated state, known input, and explicit cleanup when testing a particular database, schema, credential set, or transaction sequence.

::: {.snodec-remember title="What to remember"}
- Database state outlives the client; connection and submission alone establish no commit.
- Chained operations share a sequence; new asynchronous calls inside callbacks join the queue later.
- Metadata callbacks read completed command state; they do not submit arbitrary blocking SQL.
- A command error can leave later commands queued, so commit/rollback decisions require explicit control.
- Persistence ownership, shutdown, backpressure and replay policy belong to the application.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Classify a connection, pending sequence, cached measurement and committed row. Which can survive the client process?
2. **Review (O2, O3).** Why can rollback queued inside an error callback fail to precede an already chained commit? Contrast an immediate metadata read.
3. **Lab (O1, O2).** Run the equipped durability lab. Expect one affected row, independent read-back after client shutdown and the same row after a read-only client restart.
4. **Lab (O2, O3).** Run the equipped SQL-error lab. Expect missing-table error 1146, completion of the following query and zero rows from an independent observer.
5. **Design (O1, O3).** Define durable acceptance for a measurement service. Choose transaction ownership, an overload limit and how to resolve an uncertain write after disconnection.

Public solutions and bounded lab commands: `companion/exercises/ch23/README.md`.
:::
