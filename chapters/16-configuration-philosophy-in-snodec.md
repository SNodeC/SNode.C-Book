## Configuration Philosophy in SNode.C

### From lower-family transfer to configured communication roles

Chapter 15 showed that protocol behavior can often remain stable while lower-family instance types and endpoint configuration change.

That makes configuration visible.

A protocol may remain in the same `SocketContext`.

A factory may remain small.

But the concrete application still has to decide:

- which instance exists,
- whether it is a server or a client,
- which lower family it uses,
- which local or remote endpoint it should use,
- whether TLS or legacy connection handling is selected,
- whether the instance is enabled,
- and which values can be changed without rebuilding the application.

This chapter turns to that model.

The central idea is:

> In SNode.C, configuration is one of the main ways an instance becomes a concrete communication role.

A `SocketServer` or `SocketClient` is not only a runtime object with a few options attached.

It is a configured role in the application.

Configuration gives that role its concrete shape.

### The central configuration idea

Configuration in SNode.C is not a separate afterthought beside the framework architecture.

It is part of the architecture.

The same instance that participates in the runtime, owns a role, creates connections, and uses contexts also has a configuration identity.

That identity can be shaped through several input paths, but those paths feed one configuration model.

#### A configured communication role

A configured communication role combines several things:

| Part | Meaning |
|---|---|
| instance identity | which role is being configured |
| role identity | server or client |
| lower-family shape | IPv4, IPv6, Unix domain sockets, RFCOMM, L2CAP, and connection variant |
| endpoint values | host, port, path, channel, PSM, or related local/remote values |
| section structure | scoped configuration areas such as `local`, `remote`, `connection`, `socket`, `server`, `tls` |
| operational state | enabled or disabled, persistent or run-specific options |
| activation | `listen(...)` or `connect(...)` using already supplied configuration |

This is why configuration belongs here in the book.

The previous chapters established the architectural roles.

This chapter explains how those roles become concrete enough to run.

#### One model, several entry paths

SNode.C has three main configuration input paths:

| Input path | Main use |
|---|---|
| C++ API | in-code defaults and programmatic shaping |
| command line | run-specific override, discovery, and operational control |
| configuration file | persistent instance behavior |

These are not three unrelated configuration worlds.

They are three ways to feed one underlying configuration model.

That matters because the same conceptual object can be shaped in code, overridden on the command line, and persisted in a file without changing its identity.

### Three input paths, one configuration model

The three input paths have different strengths.

They should be understood together.

#### Configuration through the C++ API

The C++ API is the most direct configuration path.

A server or client instance exposes its configuration object, and the application can set values on it directly.

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

The important point is that code can provide baseline configuration.

Convenience overloads such as:

```cpp
listen(8001, onStatus)
```

or:

```cpp
connect("localhost", 8001, onStatus)
```

also participate in this idea.

They are readable API calls, but conceptually they also fill configuration values before the instance is activated.

In-code configuration is therefore useful for:

- small teaching examples,
- reasonable defaults,
- programmatically selected values,
- tests and experiments,
- application-level decisions known at construction time.

It is not a second-class configuration path.

It is one native way to shape an instance.

#### Configuration through the command line

Command-line configuration gives an already compiled application a way to be shaped at startup.

That is especially important for named instances.

A named server instance such as:

```cpp
EchoServer echoServer("echo");
```

can appear as an addressable configuration role on the command line.

Under that instance, sections expose the available configuration scopes.

A typical hierarchy is:

```text
application
  -> instance
      -> section
          -> option
```

The command line is therefore not only a way to override values.

It is also a discovery surface.

A user can ask for help at different levels:

```shell
echoserver --help
echoserver echo --help
echoserver echo local --help
```

Each level reveals another part of the configuration model.

That makes the configuration space inspectable instead of hidden.

#### Configuration through configuration files

Configuration files persist the same model.

They do not introduce a second configuration language with a different worldview.

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

### Precedence and instance creation timing

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

This is a useful operational model.

The application can encode reasonable defaults.

The configuration file can store deployment choices.

The command line can override them for one run.

#### Instance creation timing

There is also an important timing boundary.

Command-line and configuration-file configuration apply to server and client instances that exist before the SNode.C event loop is started.

Instances created later at runtime cannot be retroactively addressed by the command line or by a configuration file that was already read.

Those later instances must be configured through the C++ API.

This distinction is important because it separates two cases:

```text
startup-known configured roles
  -> code, file, and command line can participate

runtime-created roles
  -> C++ API configuration is the available path
```

That is not a weakness.

It is the natural boundary between startup configuration and runtime object creation.

### Named instances as configuration addresses

One of the most important ideas in the configuration model is the difference between anonymous and named instances.

An anonymous instance exists as an object in code.

A named instance also becomes addressable by the configuration system.

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

#### A name is not only a label

A name such as:

```cpp
EchoServer echoServer("echo");
```

does more than make the C++ object easier to read.

It gives the instance an address in the configuration hierarchy.

That address can appear:

- in command-line help,
- in command-line overrides,
- in generated command lines,
- in shown configuration,
- and in configuration-file keys.

The name becomes part of the operational surface of the application.

That is why named instances are central for serious applications.

#### Disablement as instance-level configuration

A configured communication role may exist but be inactive.

SNode.C treats this as a first-class configuration idea.

A named instance can be disabled instead of being removed from the application.

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

This is cleaner than scattering ad hoc application flags across the program.

### Sections as structural scopes

Sections are not only headings in documentation.

They are structural scopes in the configuration hierarchy.

The common section names make this visible:

- `local`,
- `remote`,
- `connection`,
- `socket`,
- `server`,
- `tls`.

A section groups options that belong to a particular part of the communication role.

#### Section hierarchy

The shape is:

```text
application
  -> instance
      -> section
          -> option
```

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

The section model lets these differences remain structured without changing the larger configuration idea.

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

### Configuration as discovery and persistence

A good configuration system should not only accept values.

It should help users discover what can be configured.

SNode.C does this through command-line help, configuration display, command-line generation, and generated configuration files.

#### Help output as discovery

Because named instances and sections participate in the command-line hierarchy, help output can reveal the configuration model step by step.

At application level, help shows application-wide options and available instances.

At instance level, help shows instance-level options and sections.

At section level, help shows the options for that section.

This makes the configuration system self-describing.

The user does not have to guess the entire option universe at once.

#### Persistent and non-persistent options

Not every option should be written into a configuration file.

Some options describe lasting behavior.

Others describe one run.

SNode.C makes that distinction visible by separating persistent and non-persistent options.

The practical rule is:

```text
persistent options
  -> may be stored in configuration files

non-persistent options
  -> affect the current run only
```

This is useful because it prevents operational commands such as help, display, or one-time control actions from being confused with enduring instance configuration.

#### Generated and shown configuration

Generated configuration files are not only convenient output.

They show the configuration model in file form.

A generated file can contain:

- application-level options,
- instance-level options,
- section-level options,
- default values,
- values supplied in code,
- values overridden by file or command line,
- comments describing the available options.

That makes the file both editable and educational.

It is an inspectable artifact of the same hierarchy used by the command line and the C++ API.

### Parameterless `listen()` and `connect()`

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

> The instance should already know enough about its configured role to act.

The endpoint values may have been supplied by:

- C++ API calls,
- a configuration file,
- command-line arguments,
- or a combination of those according to the precedence rule.

The call itself does not need to repeat them.

#### Configured enough to act

For a server, being configured enough may mean that the local endpoint is known.

For a client, being configured enough may mean that the remote endpoint is known, and possibly also a local bind side.

For TLS instances, it may also mean that required TLS-related configuration is available.

The exact requirements depend on the concrete instance type.

The architectural idea is stable:

```text
configuration shapes the instance
activation uses the shaped instance
```

#### Missing configuration is reported structurally

When required configuration is missing, the error path should point back into the same hierarchy.

For example, a missing server port is not just a random failure.

It belongs to a particular instance and section:

```text
application
  -> instance
      -> local
          -> port
```

A missing client host or port likewise belongs to the remote section of a particular client instance.

This is why parameterless activation is a strong proof point.

It works only because the instance has a structured configuration identity.

### CLI11 as implementation foundation

SNode.C uses CLI11 as part of the implementation foundation for this unified model.

That matters, but it should stay in the background of the chapter.

The book does not need to turn into a CLI11 manual here.

The architectural point is:

```text
SNode.C exposes one hierarchical configuration model
through code, command line, and files.
```

CLI11 helps implement that model.

The important thing for the SNode.C reader is the resulting structure:

```text
application
  -> named instance
      -> section
          -> option
```

### Configuration as architectural leverage

Configuration is not only operational convenience.

It is architectural leverage.

Because configuration can shape an instance without rewriting protocol code, the same application structure can often be reused across deployments.

A protocol may remain in the context.

The factory may keep creating the same kind of endpoint.

The lower-family instance type and endpoint values may change.

Configuration is one of the places where that variation becomes explicit.

This connects directly back to Chapter 15.

Lower-family transfer is practical only if the changing parts have somewhere clear to live.

In SNode.C, configuration is one of those places.

### What to remember

Remember:

- Configuration is part of how an instance becomes a concrete communication role.
- SNode.C has three input paths into one configuration model: C++ API, command line, and configuration file.
- The precedence order is command line, then configuration file, then C++ API.
- Command-line and file configuration apply to startup-known instances; runtime-created instances are configured through the C++ API.
- Named instances become configuration addresses.
- Anonymous instances are useful for small demos and experiments.
- Sections are structural scopes, not only documentation categories.
- The hierarchy is application, instance, section, option.
- Persistent options can be written to configuration files.
- Non-persistent options describe the current run.
- Help output and shown/generated configuration make the model discoverable.
- Disablement means a configured role may exist but remain inactive.
- Parameterless `listen()` and `connect()` show that a configured instance can already know enough to act.
- Chapter 17 moves from this philosophy to concrete application, instance, and section configuration.

### Closing perspective

Part V begins with configuration because the previous chapters made configuration unavoidable.

A protocol endpoint can be stable.

A factory can remain small.

A lower-family instance can change.

Endpoint identity and deployment values still have to be supplied somewhere.

Chapter 16 introduced the model that gives those values a coherent place.

The result is:

```text
application
  -> named communication roles
      -> sections
          -> options
```

Those options can be supplied through code, command line, or files, with clear precedence and clear operational meaning.

The next chapter goes one level deeper.

It looks at application, instance, and section configuration in detail.
