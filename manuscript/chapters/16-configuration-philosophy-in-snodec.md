## Configuration Philosophy in SNode.C

\index{configuration}
\index{configuration philosophy}
\index{configured communication role}


### From lower-family transfer to configured communication roles

Configuration becomes visible as soon as a protocol is carried over different lower families.

The protocol behavior may remain in the same `SocketContext`. The context creation policy may remain in the same `SocketContextFactory`.

But the concrete application still has to decide which server-side or client-side role exists, which lower family it uses, which endpoint identity it receives, whether it uses legacy or TLS connection handling, whether it is enabled, and which values belong in source code, a configuration file, or a run-specific command line.

That is the subject of this chapter.

Part IV separated protocol behavior, context construction, lower-family selection, and endpoint identity. Part V asks how these choices become visible, adjustable, persistent, and operable.

The central idea is:

::: {.snodec-rule title="Configuration rule"}
In SNode.C, configuration is one of the main ways a communication role becomes concrete.
:::

The `SocketServer`/`SocketClient` handle is the handle. Through that handle, the application configures a server-side or client-side communication role. When `listen(...)` or `connect(...)` registers that role, the configured instance enters the runtime.

Configuration is therefore not decoration around an otherwise complete object. It is one of the places where the role receives its operational shape.

### Configuration as part of the architecture

\index{configuration!architecture}
\index{configured communication role}


Configuration in SNode.C is not a separate afterthought beside the framework architecture. It is part of the architecture.

A communication role has several aspects:

```text
application-side handle
  -> configuration surface
      -> registered server/client instance
          -> concrete connections
              -> factories and contexts
```

The context implements the protocol behavior. The factory creates the context. The lower-family server or client type selects the communication family.

Configuration gives the role its concrete endpoint values, operational switches, and persistent identity.

That is why this chapter belongs immediately after Chapter 15. Lower-family transfer is practical only when the changing parts have somewhere clear to live. In SNode.C, configuration is one of those places.

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

The previous chapters established the runtime and protocol roles. It explains how those roles become concrete enough to run in an application.

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

It is not a second-class configuration path. It is one native way to shape a communication role.

#### Configuration through the command line

Command-line configuration gives an already compiled application a way to be shaped at startup. That is especially important for named instances.

A named server instance such as:

```cpp
EchoServer echoServer("echo");
```

can appear as an addressable communication role on the command line. Under that instance, sections expose the available configuration scopes.

A typical hierarchy is application, instance, section, and option.

The command line is therefore not only a way to override values. It is a discovery surface.

A user can ask for help at different levels:

```shell
echoserver --help
echoserver echo --help
echoserver echo local --help
```

Each level reveals another part of the configuration model.

This is important for applications that expose more than one communication role. Instead of hiding all options behind a flat list, the configuration hierarchy shows how options belong to roles and sections.

#### Configuration through configuration files

Configuration files persist the same model. They do not introduce a second configuration language with a different worldview.

Their key structure follows the same hierarchy:

```ini
instancename.sectionname.optionname = value
```

For example:

```ini
echo.local.port = 8080
echo.remote.host = "localhost"
echo.remote.port = 8080
```

This is the file form of the same application/instance/section/option structure exposed by the command line.

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

External configuration can only address roles that are present in the configuration hierarchy when the application parses its startup configuration. A role created later by application logic must be configured by application logic.

This separates two cases:

```text
startup-known configured roles
  -> C++ API, configuration file, and command line can participate

runtime-created roles
  -> C++ API configuration is the available path
```

That is not a weakness. It is the natural boundary between startup configuration and runtime object creation.

The command line and configuration file are external startup inputs. They can shape what has been made addressable before startup parsing completes. They cannot retroactively reach into a role that did not yet exist in that hierarchy.

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

This is cleaner than scattering ad hoc application flags across the program.

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

For a named instance `echo`, examples include:

```text
echo local --port 8080
echo remote --host localhost --port 8080
```

or in configuration-file form:

```ini
echo.local.port = 8080
echo.remote.host = "localhost"
echo.remote.port = 8080
```

The command-line hierarchy and the configuration-file hierarchy express the same structure.

That is the main point: the hierarchy is not an accidental CLI shape. It is the visible form of the configured communication role.

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

### Configuration as architectural leverage

Configuration gives the architecture operational leverage.

Because configuration can shape a role without rewriting protocol code, the same application structure can often be reused across deployments.

A protocol may remain in the context. The factory may keep creating the same kind of endpoint. The lower-family handle type, registered instance, endpoint identity, TLS/legacy selection, and deployment values may change.

Configuration is one of the places where that variation becomes explicit. This connects directly back to Chapter 15. Lower-family transfer is practical only if the changing parts have somewhere clear to live.

In SNode.C, configuration is one of those places.

::: {.snodec-remember title="What to remember"}
- Configuration is part of the SNode.C architecture, not an afterthought beside it.
- The handle configures a server-side or client-side communication role; the registered instance carries that configured role into the runtime.
- The C++ API, configuration files, and command line feed one hierarchical configuration model.
- Named instances become addressable in that hierarchy; anonymous instances remain internal to application code.
- Sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls` scope options by responsibility.
- Parameterless `listen(onStatus)` and `connect(onStatus)` are useful because the role can already be configured before activation.
:::

### Closing perspective

Configuration makes protocol behavior, context creation, lower-family choice, and endpoint identity visible to applications and operators.

The practical structure is application configuration, instance configuration, sections, and the concrete options that expose the model.

