## Configuration Philosophy in SNode.C

\index{configuration}
\index{configuration philosophy}
\index{configured communication role}


### From lower-family transfer to configured communication roles

Configuration is where many architectural choices become visible to the executable and to the operator.

The protocol behavior may remain in the same `SocketContext`. The context creation policy may remain in the same `SocketContextFactory`.

But the concrete application still has to decide which server-side or client-side role exists, which lower family it uses, which endpoint identity it receives, whether it uses legacy or TLS connection handling, whether it is enabled, and which values belong in source code, a configuration file, or a run-specific command line.

That is the subject of this chapter.

Part IV separated protocol behavior, context construction, lower-family selection, and endpoint identity. Part V asks how these choices become visible, adjustable, persistent, and operable.

In SNode.C, configuration makes a communication role concrete: it gives the role endpoint values, operational switches, instance identity, and activation-time shape.

Through a `SocketServer` or `SocketClient` handle, the application configures a server-side or client-side communication role. Constructing a named endpoint registers its configuration instance. Each `listen(...)` or `connect(...)` call then starts an activation flow for that configured role.

Configuration therefore gives the role its operational shape instead of decorating an otherwise complete object.

### Configuration as part of the architecture

\index{configuration!architecture}
\index{configured communication role}


In SNode.C, configuration belongs to the framework architecture rather than standing beside it as an afterthought.

A communication role has several aspects:

```text
application-side handle
  -> shared endpoint configuration
      -> named instance registered in the configuration hierarchy
          -> explicit activation flow
              -> connections with factory-created contexts
```

The context implements the protocol behavior. The factory creates the context. The lower-family server or client type selects the communication family.

Configuration gives the role its concrete endpoint values, operational switches, and persistent identity.

That is why this chapter belongs immediately after Chapter 15. Lower-family transfer is practical only when the changing parts have somewhere clear to live; in SNode.C, configuration provides that place.

#### A configured communication role

A configured communication role combines several things:

| Part | Meaning |
|---|---|
| instance identity | which role is being configured |
| role identity | server-side or client-side behavior |
| lower-family shape | IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP, and connection variant |
| endpoint values | host, port, path, channel, PSM, or related local/remote values |
| section structure | scoped areas such as `local`, `remote`, `connection`, `socket`, `server`, and `tls` |
| operational state | enabled or disabled, persistent or run-specific options |
| activation | `listen(...)` or `connect(...)` using supplied configuration |

This is a different view from “an object with some options.”

A configured role is the architectural place where the application says:

```text
this role exists
this is how it is named
this is how it is addressed
this is how it participates
this is how it can be operated
```

The previous chapters established the runtime and protocol roles. This chapter explains how those roles become concrete enough to run in an application.

#### One model, several entry paths

SNode.C has three main configuration input paths:

| Input path | Main use |
|---|---|
| C++ API | baseline defaults and programmatic shaping |
| configuration file | persistent operational configuration |
| command line | run-specific override, discovery, and control |

These are not three unrelated configuration worlds. They are three ways to feed one underlying configuration model. The C++ API gives the application a baseline.

The configuration file gives deployment a durable expression. The command line gives a run-specific control surface.

That matters because the same conceptual role can be shaped in code, persisted in a file, and overridden for one invocation without changing its identity.

### Three input paths, one configuration model

\index{configuration!C++ API}
\index{configuration!command line}
\index{configuration!file}


The three input paths have different strengths. They should be understood together.

#### Configuration through the C++ API

The C++ API is the most direct configuration path.

The server/client handle exposes its configuration object, and the application can set values on it directly.

For an IPv4 server, a minimal example may look like:

```cpp
EchoServer echoServer;

echoServer.getConfig()->Local::setPort(8001);
```

In this case, the explicit `Local::` qualification is valid, but it is not required. The same server-side port can also be configured as:

```cpp
echoServer.getConfig()->setPort(8001);
```

`getConfig()` returns a pointer to the configuration object, so the examples use `->`.

The `Local::` qualification is optional here because this IPv4 server configuration does not expose two competing `setPort(...)` meanings at this call site. There is no local-versus-remote ambiguity for the server-side port in this example.

C++ code can provide baseline configuration. It can also express values that are genuinely programmatic: values derived from application structure, construction-time decisions, tests, or small teaching examples.

Convenience overloads such as:

```cpp
listen(8001, onStatus)
```

or:

```cpp
connect("localhost", 8001, onStatus)
```

participate in the same idea.

They are readable API calls. Conceptually, they also fill configuration values on the handle before the role enters the activation path.

In-code configuration is therefore useful for:

- small teaching examples,
- reasonable defaults,
- programmatically selected values,
- tests and experiments,
- application-level decisions known at construction time.

It is one native way to shape a communication role, not a second-class configuration path.

#### Configuration through the command line

Command-line configuration gives an already compiled application a way to be shaped at startup. That is especially important for named instances.

A named server instance such as:

```cpp
EchoServer echoServer("echo");
```

can appear as an addressable communication role on the command line. Under that instance, sections expose the available configuration scopes.

A typical hierarchy is application, instance, section, and option.

The command line is therefore a discovery surface as well as a way to override values.

A user can ask for help at different levels:

```sh
echoserver --help
echoserver echo --help
echoserver echo local --help
```

Each level reveals another part of the configuration model.

Applications that expose more than one communication role benefit from this hierarchy: instead of hiding all options behind a flat list, it shows how options belong to roles and sections.

#### Configuration through configuration files

Configuration files persist the same model. They do not introduce a second configuration language with a different worldview.

Their key structure follows the same hierarchy:

```ini
instancename.sectionname.optionname = value
```

For example:

```ini
echo.local.port = 8080
uplink.remote.host = "localhost"
uplink.remote.port = 8080
```

Here `echo` is a named server and `uplink` is a separate named client in an application that creates both. A server does not acquire a client’s `remote` section merely because that key is written in a file. The file can configure the roles the executable actually exposes.

The configuration file is therefore both:

- an operational artifact,
- and an inspectable map of the configured application.

It is operational because it can be used by a deployed application. It is inspectable because it shows the same structure that the command line and the C++ API feed.

### Precedence and the startup boundary

\index{configuration!precedence}
\index{startup boundary}


The precedence rule is part of the configuration philosophy.

The order is:

```text
command line
  > configuration file
      > C++ API
```

That means:

| Source | Typical role |
|---|---|
| C++ API | baseline defaults or programmatic intent |
| configuration file | persistent operational configuration |
| command line | run-specific override |

This is the practical operational model. The application can encode reasonable defaults. The configuration file can store deployment choices.

The command line can override them for one run.

The order is important because it lets an application be useful out of the box, adaptable in deployment, and still controllable at startup.

#### Instance creation timing

There is also an important timing boundary.

External configuration can address the named roles present in the hierarchy when parsing occurs. Startup parsing therefore sees the roles constructed before startup. A role created later begins with the values supplied by application logic.

The current framework also supports a deliberate runtime reparse through `core::SNodeC::reconfigure()`. While the event loop is `RUNNING`, application code on the event-loop thread can ask the existing parser to read the current configuration file again, with the original command-line arguments still taking precedence. A named role that is now registered can participate in that parse. Merely editing the file or constructing a role does not trigger this operation.

The distinction is between changing configuration values and changing live activity. Reconfiguration does not restart listeners, reconnect peers, or replace the policy already captured by an established connection. It also leaves bootstrap logging and daemonization in place. The application must decide which subsequent activation should use the new values and how existing activity should finish.

A failed reparse returns `false`; it is not a transaction that rolls back every value already changed. Chapter 17 develops the operational consequences. For a service whose configuration must change atomically, validating a replacement before a controlled process restart may be a clearer policy than editing the live tree.

The current per-call flow model makes the configuration boundary particularly important. An endpoint exposes one shared configuration object. Each explicit activation receives its own controller, but that controller does not freeze a private copy of the endpoint settings. An address-taking `connect(...)` overload updates the endpoint's remote configuration before starting its flow. Use separate named endpoints for destinations that need independent configuration; retaining two flow handles is not a substitute for that separation.

### Named instances as configuration addresses

\index{named instances}
\index{configuration addresses}
\index{instance names}


One of the most important ideas in the configuration model is the difference between anonymous and named instances. An anonymous instance exists as a configured role in application code. A named instance also becomes addressable by the external configuration hierarchy.

That is the key distinction.

#### Anonymous and named instances

A useful rule of thumb is:

| Anonymous instance | Named instance |
|---|---|
| internal helper clients | externally operated communication roles |
| temporary or embedded helper servers | independently configurable server roles |
| no external configuration address needed | persistent or inspectable behavior |
| tiny demos | operational applications |
| one-off experiments | command-line and file control |
| simplest code | multi-instance applications |

Anonymous instances are useful for communication roles that are intentionally internal to the program and should not become independently addressable through the external configuration model.

This is especially common for helper clients.

For example, an application may need to fetch data from a known remote resource as part of its own internal behavior. If that communication role should not be configured, disabled, persisted, or inspected independently, an anonymous client is often the clearer choice.

Anonymous servers can also make sense, but the case is narrower.

They are reasonable for temporary local test servers, embedded loopback-only services, or helper servers whose endpoint is fixed by the surrounding program.

Externally operated server roles are usually better expressed as named instances, because servers often need deployment-facing control over bind address, port, path, channel, enablement, and persistent configuration.

In other words:

```text
anonymous
  -> application-internal role

named
  -> externally addressable configured role
```

A named instance is attached to the external configuration hierarchy. An anonymous instance remains application-internal and does not appear as an independently addressable command-line/config-file subcommand.

#### Why names matter

A name such as:

```cpp
EchoServer echoServer("echo");
```

gives the configured role an address in the configuration hierarchy, with the readable C++ name as its source-level anchor.

That address can appear:

- in command-line help,
- in command-line overrides,
- in generated command lines,
- in shown configuration,
- and in configuration-file keys.

The name becomes part of the operational surface of the application. That is why named instances are central for serious applications: the name is a stable handle for operation.

#### Disablement as instance-level configuration

A configured communication role may exist but be inactive. SNode.C treats this as an instance-level configuration idea. A named instance can be disabled instead of being removed from the application.

That is useful for:

- multi-instance programs,
- optional carriers,
- staged deployment,
- development and testing,
- field diagnostics,
- temporarily disabling a communication role without rebuilding.

The important idea is:

```text
configured role exists
  -> configuration may decide whether it participates
```

Disablement belongs to the configured role. It lets the role remain part of the application shape while configuration decides whether it participates in a run.

At activation, disablement lets the framework report an intentionally inactive role. Setting that value later is not a command to close established peers or cancel every flow. Those actions have their own lifecycle controls; a runtime reparse does not merge them into one operation.

### Sections as structural scopes

\index{configuration sections}
\index{section hierarchy}
\index{local section}
\index{remote section}
\index{tls section}


Sections are structural scopes in the configuration hierarchy. A section is the boundary between different kinds of responsibility inside a communication role.

The common section names make this visible:

- `local`,
- `remote`,
- `connection`,
- `socket`,
- `server`,
- `tls`.

A section groups options that belong to a particular part of the role.

#### Section hierarchy

The same application/instance/section/option hierarchy applies here; only the concrete section and option change.

For the named server `echo` and the separate client `uplink`, examples include:

```text
echo local --port 8080
uplink remote --host localhost --port 8080
```

or in configuration-file form:

```ini
echo.local.port = 8080
uplink.remote.host = "localhost"
uplink.remote.port = 8080
```

The command-line hierarchy and the configuration-file hierarchy express the same structure.

The main point is that the hierarchy is the visible form of the configured communication role, not an accidental CLI shape.

#### Local and remote sections

The `local` and `remote` sections are especially important because they connect directly to the address semantics from Chapters 8–12.

For a server, local configuration usually describes the endpoint to bind or listen on.

For a client, remote configuration usually describes the peer endpoint to connect to, while local configuration may describe an explicit bind side.

The exact fields depend on the lower family:

| Family | Typical endpoint fields |
|---|---|
| IPv4 / IPv6 | host and port |
| Unix domain sockets | path |
| RFCOMM | Bluetooth address and channel |
| L2CAP | Bluetooth address and PSM |

The section model lets these differences remain structured without changing the larger configuration idea. The family changes the endpoint fields. The hierarchy remains recognizable.

#### Connection, socket, server, and TLS sections

Other sections describe other parts of the communication role.

For example:

| Section | Typical scope |
|---|---|
| `connection` | established connection behavior, timeouts, read/write behavior |
| `socket` | socket-level behavior such as retry or reuse options |
| `server` | server-specific behavior |
| `tls` | TLS-related connection-layer configuration |

Chapter 17 can go into these details more concretely.

For Chapter 16, the important point is the structure:

```text
sections are scopes
not loose option groups
```

This keeps configuration readable. A timeout, an address, a TLS certificate path, and a server backlog do not all live in one flat pile. They belong to different scopes of the same configured role.

### Configuration as discovery, persistence, and inspection

\index{configuration!discovery}
\index{persistent options}
\index{generated configuration}


A good configuration system should not only accept values. It should help users discover what can be configured, inspect the active shape, and persist durable choices. SNode.C does this through command-line help, configuration display, command-line generation, and generated configuration files.

#### Help output as discovery

Because named instances and sections participate in the command-line hierarchy, help output can reveal the configuration model step by step.

At application level, help shows application-wide options and available instances. At instance level, help shows instance-level options and sections. At section level, help shows the options for that section.

This makes the configuration system self-describing. The user does not have to guess the entire option universe at once. The hierarchy itself teaches the shape of the application.

#### Persistent and nonpersistent options

Not every option should be written into a configuration file. Some options describe lasting behavior. Others describe one run.

SNode.C makes that distinction visible by separating persistent and nonpersistent options.

The practical rule is simple: persistent options may be stored in configuration files, while nonpersistent options affect inspection, generation, help, or the current run only.

Persistent options describe the desired shape of an application or instance. Nonpersistent options trigger inspection, generation, display, help, or one-run control actions.

This prevents operational commands such as help, display, command-line generation, or write-config from being confused with enduring instance configuration.

#### Generated and shown configuration

Generated configuration files show the configuration model in file form.

A generated file can contain:

- application-level options,
- instance-level options,
- section-level options,
- default values,
- values supplied in code,
- values overridden by file or command line,
- comments describing the available options.

Shown configuration and generated command lines serve a similar purpose from different angles. They make the active or possible configuration visible. That makes the file both editable and educational.

It is an inspectable artifact of the same hierarchy used by the command line and the C++ API.

### Parameterless `listen()` and `connect()`

\index{listen()@\texttt{listen()}!parameterless}
\index{connect()@\texttt{connect()}!parameterless}
\index{parameterless activation}


Parameterless activation is one of the clearest expressions of the configuration philosophy.

A call such as:

```cpp
echoServer.listen(onStatus);
```

or:

```cpp
echoClient.connect(onStatus);
```

means:

> The role should already know enough about its configured shape to act.

The endpoint values may have been supplied by:

- C++ API calls,
- a configuration file,
- command-line arguments,
- or a combination of those according to the precedence rule.

The call itself does not need to repeat them.

#### Configured enough to act

For a server, being configured enough may mean that the local endpoint is known.

For a client, being configured enough may mean that the remote endpoint is known, and possibly also a local bind side.

For TLS instances, it may also mean that required TLS-related configuration is available. The exact requirements depend on the concrete server/client type.

The architectural idea is stable:

```text
configuration shapes the role
activation uses the shaped role
```

This is the bridge between configuration and runtime behavior.

A configured role has already been prepared for activation. The parameterless call is readable precisely because the role has already been shaped.

#### Missing configuration is reported structurally

When required configuration is missing, the error path should point back into the same hierarchy. For example, a missing server port belongs to the configured server role that required it.

For a server-side role, the hierarchy commonly narrows to the `local` section and then to a concrete option such as `port`.

A missing client host or port likewise belongs to the remote section of a particular client instance. Therefore, parameterless activation is a strong proof point. It works only because the role has a structured configuration identity.

### Configuration can describe itself to another program

The configuration model now has a machine-readable description carried inside its ordinary INI-compatible output. Structured `#@` comment records describe the document, nodes, groups, and options while leaving the real configuration assignments as INI text.

That is an extension of the existing configuration surface, not a parallel JSON configuration system. Existing files without metadata remain valid. The metadata is available when description/comment output is enabled, as with `--show-config`.

The distinction is useful operationally. A tool can discover the application/instance/section tree without guessing structure from a flat list of dotted keys, while the target application remains responsible for validation and canonical configuration output. Chapter 17 shows how `snodec-control` uses that separation.

### CLI11 as implementation foundation

\index{CLI11@\texttt{CLI11}}
\index{command-line parsing}


SNode.C uses CLI11 as part of the implementation foundation for this unified model. That matters, but it should stay in the background of the chapter. The book does not need to become a CLI11 manual here.

The architectural point is:

```text
SNode.C exposes one hierarchical configuration model
through code, command line, and files.
```

CLI11 helps implement that model.

For the SNode.C reader, the important point is that command-line form moves from the application to a named instance, then to a section, and finally to a concrete option.

That is the model the application author and operator see.

The implementation foundation matters because it makes help output, configuration files, option grouping, command-line generation, and persistent/nonpersistent classification possible. But the conceptual model remains the SNode.C configuration hierarchy.

### Choosing what operators can change

An external option is a promise to operators. Naming a role makes its endpoint and policy visible, but also makes those names part of configuration files, service definitions, and diagnostic procedures. Expose choices that deployments need to own; keep an internal helper’s construction detail in code when changing it independently would violate the application’s assumptions.

Startup-only configuration has a useful cost model: one validated process begins with one intended deployment shape. Runtime reconfiguration can avoid a full restart, but requires a policy for partial failure, existing connections, and future activation. The framework supplies the parsing operation. It cannot decide those application consequences from an option name.

The next chapter makes the distinction observable. We will inspect the same port supplied in code, overridden by a file, and overridden again for one invocation before discussing what a runtime reparse does with that hierarchy.

::: {.snodec-remember title="What to remember"}
- Configuration is part of the SNode.C architecture, not an afterthought beside it.
- The handle configures a server-side or client-side communication role; the registered instance carries that configured role into the runtime.
- The C++ API, configuration files, and command line feed one hierarchical configuration model.
- Named instances become addressable in that hierarchy; anonymous instances remain internal to application code.
- Sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls` scope options by responsibility.
- Parameterless `listen(onStatus)` and `connect(onStatus)` are useful because the role can already be configured before activation.
:::
