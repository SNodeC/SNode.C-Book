## Database Support and Application State
### Why database support belongs after the IoT chapter

The previous chapter brought the protocol chapters together into multi-protocol IoT system design.

That was the right place to talk about boundaries:

- device-facing boundaries,
- local-control boundaries,
- MQTT integration boundaries,
- human-facing HTTP and WebSocket boundaries,
- and real-time observation boundaries.

But a real system usually needs one more kind of boundary.

It needs a place where information survives beyond one connection, one message, or one runtime episode.

That is the persistence boundary.

This chapter introduces that boundary through the database support that exists in the current SNode.C repository.

The important teaching point is not that every SNode.C application must use a database.

The important point is that persistence changes the architecture of an application.

Once state is stored outside the immediate protocol conversation, the developer must think about:

- what belongs in memory,
- what belongs in the database,
- when database operations should be scheduled,
- how query results flow back into the event-driven application,
- and how database failure should be observed.

That is why database support belongs here, after the protocol and IoT chapters but before the later chapters on full applications and systems.

### What the current repository actually supports

The current repository should be read carefully here.

The database part of SNode.C is not presented as a broad abstract database layer with many interchangeable backends.

In the live source tree, the concrete database module is MariaDB-focused.

The build structure descends into `src/database/mariadb`, checks for `libmariadb`, and only builds the `db-mariadb` library when that dependency is available.

The corresponding application example under `src/apps/database` is likewise conditional: it builds a `testmariadb` executable only when `LIBMARIADB_FOUND` is true, and links that executable against `db-mariadb`.

This matters for the book.

We should not overstate the module as a generic persistence framework.

The accurate statement is narrower and stronger:

> SNode.C currently provides a MariaDB integration layer that is shaped to work inside the same event-driven runtime discipline as the rest of the framework.

That is the correct teaching starting point.

### Persistence is not another transport protocol

A database is easy to misuse conceptually in a networking framework.

A beginner might think of it as just another endpoint:

- connect,
- send query text,
- receive rows.

That description is not completely wrong, but it is too shallow.

A database boundary has a different role from the network protocol boundaries discussed earlier.

A HTTP endpoint, a WebSocket session, or a MQTT connection is usually a communication boundary between active peers.

A database connection is usually a persistence and query boundary.

It stores application state, retrieves state, modifies state transactionally, and can become the durable memory of a larger system.

This means database code should not be treated as random helper code hidden inside request handlers.

It should be treated as part of the application-state architecture.

### The live database app is a test and teaching example, not a polished product application

The current `testmariadb` application is best read as a test and demonstration program.

It shows how the MariaDB API is used, but it is not meant to be copied blindly into a production service.

That distinction is important.

The example demonstrates:

- adding a small custom configuration subcommand for database host selection,
- initializing the SNode.C runtime,
- constructing a `MariaDBConnectionDetails` object,
- creating `MariaDBClient` objects,
- reacting to database connection state changes,
- executing commands,
- querying rows,
- chaining command sequences,
- reading affected-row and field-count metadata,
- starting and ending transactions,
- committing and rolling back,
- and scheduling repeated database activity through framework timers.

That is a lot of useful information.

But the application also contains hard-coded database user, password, database name, table name, and setup comments.

A teaching book should present that honestly.

The example is valuable because it shows the API shape and runtime integration. It is not a security or configuration model to imitate unchanged.

### The first visible pattern: database configuration can use the same config system

The live database app begins by defining a small `ConfigDb` class derived from `utils::SubCommand`.

That class adds a `--db-host` option, marks it configurable, makes it required, and then provides a `setHost(...)` helper that sets a default and clears the required flag.

This is a small piece of code, but it is architecturally meaningful.

It shows that database-related configuration does not need to live outside the SNode.C application shell.

It can be attached to the same configuration hierarchy used by the rest of the framework.

That is exactly the right instinct.

A database host is not a random global variable. It is part of the application’s operational configuration.

The example uses only a small database-host option, but the pattern generalizes naturally.

A more serious application would likely make additional values configurable:

- database name,
- username,
- password source,
- port,
- socket path,
- flags,
- connection name,
- and possibly TLS or credential-store details depending on deployment.

The important lesson is not the exact option set.

The important lesson is that database configuration belongs in the same operational vocabulary as the rest of the application.

### Runtime initialization still comes before database activity

The example adds its custom database configuration subcommand before calling `core::SNodeC::init(argc, argv)`.

That ordering is important.

The application first shapes the configuration tree, then lets the framework initialize with that configuration surface available.

After initialization, it reads the configured database host and uses it to construct the database connection details.

This fits the configuration chapters well.

A SNode.C application should not treat configuration parsing and runtime startup as unrelated phases.

The database example confirms that even non-socket resources can participate in the same application-level initialization story.

### `MariaDBConnectionDetails` is the concrete database endpoint description

The current MariaDB API uses a `MariaDBConnectionDetails` structure to describe the database endpoint and credentials.

It contains:

- a connection name,
- hostname,
- username,
- password,
- database name,
- port,
- socket path,
- and flags.

This structure plays a role similar to endpoint configuration, but at the database boundary rather than at a network-protocol boundary.

It tells the MariaDB client enough to establish and identify the database connection.

The presence of a `connectionName` is especially important for diagnostics.

As with named SNode.C instances, a named database connection is much easier to understand in logs than an anonymous one.

This is a small but important example of operational clarity carrying into the persistence layer.

### `MariaDBClient` is the application-facing database object

The live API centers ordinary use around `database::mariadb::MariaDBClient`.

A client is constructed from:

- `MariaDBConnectionDetails`,
- and an `onStateChanged` callback.

That callback receives a `MariaDBState` containing:

- an error number,
- an error message,
- and a connected flag.

This is a good fit for the rest of SNode.C.

The application does not only fire queries and hope.

It can observe whether the database connection succeeds, fails, or vanishes.

That matters because a database connection is a runtime participant. It can be unavailable, disconnected, or in an error state just like other external resources.

### The database connection is created lazily

One subtle live-code detail is especially useful for teaching.

The `MariaDBClient` does not immediately construct its internal `MariaDBConnection` in the constructor.

Instead, the internal connection object is created when the first asynchronous or synchronous command is executed.

This is an important design detail.

It means the public client object can exist as an application-facing handle before the database connection is actually created and registered with the runtime machinery.

This fits event-driven design well.

Resources become active when work is requested, and the connection object then enters the runtime event-processing world.

### The MariaDB connection is integrated with the SNode.C event loop

The most important internal fact in the live database implementation is this:

`MariaDBConnection` participates in the SNode.C event loop.

It derives privately from read, write, and exceptional-condition event receivers.

During connection setup, it obtains the MariaDB socket descriptor and registers that descriptor with the SNode.C event loop. It then suspends or resumes read, write, and exceptional-condition observation depending on what the MariaDB nonblocking API currently needs.

This is the architectural heart of the database module.

The database client is not merely blocking the application while queries run.

Instead, it is wired into the same descriptor-event model used elsewhere in the framework.

That is why database support belongs in this book.

It is not only about SQL. It is about making database work fit into the same event-driven runtime discipline as network work.

### MariaDB commands are represented explicitly

The live database implementation does not treat database operations as anonymous lambdas floating around in the runtime.

It represents operations as command objects.

There are asynchronous command types for actions such as:

- connect,
- query,
- exec,
- fetch row,
- free result,
- auto-commit,
- commit,
- rollback.

There are also synchronous-style command types for metadata operations such as:

- affected rows,
- field count,
- use result.

This command structure matters.

It lets the MariaDB connection keep track of the current operation, continue it when the descriptor becomes ready, report errors through the command’s error callback, and move to the next operation in a sequence.

In other words, the command abstraction is how database work becomes event-loop work.

### The asynchronous API is callback-based

The live `MariaDBClientASyncAPI` exposes the most important application-facing database operations:

- `query(...)`,
- `exec(...)`,
- `startTransactions(...)`,
- `endTransactions(...)`,
- `commit(...)`,
- `rollback(...)`.

Each operation takes success and error callbacks in the style expected by the command.

For `query(...)`, the success callback receives a `MYSQL_ROW`.

The example uses an important convention: the row callback is called with non-null rows while results are available, and with `nullptr` after all results have been fetched.

This is a very useful teaching point.

A row callback in this API is not simply “one callback when the query is done.”

It is part of result iteration.

A good user of the API should therefore treat `row == nullptr` as the end-of-result signal for that query callback.

### `exec(...)` and `query(...)` express two different intentions

The live app demonstrates both `exec(...)` and `query(...)`.

That distinction is worth making explicit.

Use `exec(...)` when the SQL statement is about action:

- delete,
- insert,
- update,
- schema modification,
- or any statement where result rows are not the main purpose.

Use `query(...)` when the SQL statement produces rows that the application wants to inspect.

The underlying database may treat both as SQL text, but the application-facing API distinguishes the intention clearly.

That helps keep calling code readable.

### Command sequences make database flow readable

One of the most distinctive parts of the live API is `MariaDBCommandSequence`.

The asynchronous methods return a reference that allows further operations to be chained.

The `testmariadb` example uses this extensively:

- delete rows,
- inspect affected rows,
- insert a row,
- inspect affected rows,
- run a select,
- run another select,
- and later build transaction sequences.

This is one of the most important usage patterns in the chapter.

The chain expresses ordering.

It says: this database work should happen as a sequence, not as unrelated independent commands.

That fits the event-driven runtime very well.

The application can describe a logical series of database operations without writing its own blocking loop.

### Metadata calls are still callback-based

The synchronous API name can be slightly misleading to a new reader.

The `MariaDBClientSyncAPI` exposes methods such as:

- `affectedRows(...)`,
- `fieldCount(...)`.

But these are still callback-shaped from the application’s point of view.

The success callback receives the requested metadata, and the error callback receives the error string and error number.

The example uses `affectedRows(...)` after delete and insert statements, and `fieldCount(...)` after selected query activity.

The teaching lesson is this:

Do not assume that “sync API” means ordinary blocking procedural style in the middle of your application logic.

The MariaDB layer keeps a callback-oriented surface that fits the rest of SNode.C’s event-driven style.

### Transactions are command sequences too

The live app demonstrates transaction control through the same chainable command style.

It calls:

- `startTransactions(...)`,
- `exec(...)`,
- `rollback(...)`,
- another `exec(...)`,
- `commit(...)`,
- `query(...)`,
- and `endTransactions(...)`.

This is one of the most valuable parts of the example.

It shows that transactions are not separate magical blocks outside the event model.

They are expressed as database commands in a sequence.

That makes transaction flow visible and ordered.

It also keeps transaction success and failure inside the same callback/error-callback pattern as other database operations.

### Timers and database work can cooperate

The live database app also uses `core::timer::Timer::intervalTimer(...)` to schedule repeated database work.

This is another important architectural connection.

Database activity is not isolated from the rest of SNode.C’s runtime.

Timers can initiate periodic queries or transaction sequences, and those database operations then continue through the event-driven MariaDB connection machinery.

This is especially relevant for IoT systems.

A service may periodically:

- aggregate sensor values,
- clean old rows,
- poll a status table,
- publish derived state,
- or reconcile database state with MQTT or HTTP-facing state.

The live example is deliberately noisy and test-like, but it demonstrates the real architectural possibility: timers and database commands can live in the same runtime world.

### Database state and application state are not the same thing

This is one of the most important design lessons in the chapter.

A database stores durable state.

An application still has runtime state.

Those two should not be confused.

Runtime state includes things like:

- live connections,
- current WebSocket sessions,
- active timers,
- MQTT subscriptions,
- in-memory caches,
- pending command sequences.

Database state includes things like:

- persisted users,
- persisted device records,
- measurement history,
- configuration records,
- audit logs,
- durable application facts.

A good SNode.C application should decide carefully which state belongs where.

The database should not become a dumping ground for every transient detail, and in-memory state should not pretend to be durable when it is not.

### Persistence changes failure thinking

Once a database is introduced, failure behavior becomes richer.

A HTTP route may be reachable while the database is unavailable.

A MQTT client may be connected while insert operations fail.

A timer may keep firing while an earlier database sequence is still pending.

A transaction may fail after some application-level event has already occurred.

This means the developer must think carefully about database failure as part of the larger system topology.

The live API helps by making state changes and command errors visible through callbacks.

But the architecture still belongs to the application designer.

The framework can report the error. The application must decide the policy.

### Keep database operations out of low-level protocol contexts when possible

A practical design rule belongs here.

Do not reflexively put database access directly inside every low-level protocol callback.

Sometimes it is appropriate.

But often a cleaner design is to separate:

- protocol parsing,
- application command interpretation,
- persistence service logic,
- and database execution.

For example, a `SocketContext` or HTTP handler might validate and interpret an incoming request, then hand a domain-level operation to a persistence component that owns the MariaDB client and its command sequencing.

That separation keeps protocol code readable and prevents database details from leaking into every communication boundary.

This is especially important in multi-protocol IoT systems where MQTT, HTTP, WebSocket, and local-control roles may all touch the same durable state.

### The database client should usually be owned at application or service scope

The live example creates `MariaDBClient` objects directly in `main()` because it is a compact test application.

In a more structured application, a database client will often belong to a service object or application-level component.

That component can then be shared carefully with the protocol roles that need persistence.

This is usually better than each connection creating its own database client without a clear reason.

The design question should be:

> What lifetime should this database connection or database service have relative to the application roles that use it?

That is a system-design question, not merely a coding detail.

### Be careful with SQL construction

The live app uses fixed SQL strings because it is a test program.

A teaching book should explicitly warn readers not to generalize that into unsafe dynamic SQL construction.

When user input, device payloads, or network messages influence database operations, the application must handle SQL construction safely.

That usually means using proper escaping or prepared-statement patterns where available, and not concatenating untrusted input directly into SQL strings.

The current chapter does not need to turn into a SQL-security textbook.

But it should make one rule unmistakable:

network-facing data and SQL text must not be casually mixed.

This is especially important because SNode.C applications are often precisely the applications that sit between network protocols and persistent state.

### Build and deployment implications

The MariaDB support is optional at build time.

The database library is built only when `libmariadb` is found. The test application is built only under the same condition.

This should shape how the reader thinks about deployment.

Database support is not just a header include.

It depends on:

- the MariaDB client development libraries at build time,
- the MariaDB client library at runtime,
- and a reachable MariaDB server or socket endpoint at operation time.

That is another reason the chapter belongs in the persistence and full-systems part of the book.

Database support is both code and deployment.

### A practical reading of `testmariadb`

The best way to read the live database app is not linearly as one perfect application.

It is better to read it as a catalogue of API behaviors:

- how to add a database-related config option,
- how to construct connection details,
- how to create a client with a state callback,
- how to run `exec(...)`,
- how to run `query(...)`,
- how to process rows and end-of-result,
- how to chain commands,
- how to ask for affected rows and field count,
- how to express transactions,
- how to use timers to initiate repeated database work.

That is the right teaching interpretation.

The example is not a finished persistence architecture.

It is a living source-code demonstration of the current MariaDB API surface.

### Common misunderstandings about database support in SNode.C

It helps to clear away a few misunderstandings explicitly.

#### Misunderstanding 1: “SNode.C has a generic database abstraction for many backends.”

Corrected view: the current repository’s concrete database support is MariaDB-focused and builds through `db-mariadb` when `libmariadb` is available.

#### Misunderstanding 2: “Database operations are outside the event-driven runtime story.”

Corrected view: the MariaDB connection registers the MariaDB socket descriptor with SNode.C event receivers and continues commands according to read, write, exceptional, and timeout readiness.

#### Misunderstanding 3: “A query callback only means the query is finished.”

Corrected view: the row callback receives rows as they are fetched, and the example treats `nullptr` as the end-of-result signal.

#### Misunderstanding 4: “Command chaining is just syntactic style.”

Corrected view: command sequences express ordered database work in a way that fits the event-driven runtime.

#### Misunderstanding 5: “The test app is a production-ready persistence architecture.”

Corrected view: it is a useful API demonstration and stress-style example, but real applications should externalize credentials, shape configuration carefully, and separate protocol handling from persistence policy.

### A good one-paragraph summary of the chapter

Database support in the current SNode.C repository is centered on a MariaDB integration layer that fits into the framework’s event-driven architecture. Applications use `MariaDBConnectionDetails` to describe the database boundary, create `MariaDBClient` objects with state callbacks, issue asynchronous `query`, `exec`, transaction, commit, and rollback commands, and compose ordered database work through `MariaDBCommandSequence`. Internally, the MariaDB connection participates in the SNode.C event loop through descriptor event receivers, which makes persistence work part of the same runtime discipline as the network-facing parts of the framework.

That is the heart of the chapter.

### Closing perspective

This chapter adds an important missing piece to the system story.

The earlier chapters taught how SNode.C applications communicate.

This chapter shows how they can also remember.

That does not mean every SNode.C application needs a database.

But it does mean that when persistence enters the design, it should be treated with the same architectural care as any other boundary.

The database layer has configuration, connection details, state callbacks, command sequencing, error reporting, and event-loop integration.

Those are not incidental details.

They are the shape of persistence inside an event-driven communication framework.

With that in place, the next chapter can study the application tree with a better eye.

The reader is now ready to look at the concrete applications in `src/apps` not only as executables, but as examples of how framework pieces, configuration, protocol layers, and now stateful services can become real programs.
