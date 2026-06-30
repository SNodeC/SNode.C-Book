## Application and Instance Configuration in Detail

\index{application configuration}
\index{instance configuration}
\index{configuration hierarchy}


### From configuration philosophy to configuration anatomy

Configuration shapes a communication role before it becomes a registered runtime instance.

This chapter looks at the practical anatomy of that model.

The core hierarchy is application, instance, section, and option.

The application is the executable-level operational shell. A named instance is the externally addressable configuration identity of one configured communication role inside that application. A section is one scoped part of that instance configuration.

An option is one concrete value inside such a scope.

This chapter follows that hierarchy from the outside inward. The goal is not to memorize every possible option. The goal is to understand where a value belongs, why it belongs there, and how the same structure appears in C++ code, on the command line, and in configuration files.

### The anatomy of the configuration hierarchy

\index{configuration hierarchy}
\index{application scope}
\index{instance scope}
\index{section scope}


The configuration model is easiest to read from the outside inward. Figure \ref{fig:configuration-hierarchy} shows that hierarchy as one structural model. The named-instance level is where a configured server/client role receives an externally addressable identity and can be enabled or disabled without removing the role from the application shape.

![The SNode.C configuration hierarchy: application scope contains named communication-role instances; each instance contains responsibility sections; each section owns concrete options.](assets/figures/pdf/fig-13-configuration-hierarchy.pdf){#fig:configuration-hierarchy width=90% latex-placement="tbp"}

The figure is a placement model. It shows where configuration meaning belongs: executable-wide concerns at application scope, externally addressable communication roles at instance scope, responsibility groups at section scope, and individual values at option scope. The concrete sections and options in real applications are narrower and more numerous than the diagram needs to show.

| Scope | Addressed by | Typical concerns |
|---|---|---|
| application | executable-level options | config file, logging, daemonization, help, generated command line |
| instance | named server/client communication role | disabled state, role identity, section collection |
| section | `local`, `remote`, `connection`, `socket`, `server`, `tls` | concrete endpoint or behavioral settings |
| option | individual setting | host, port, timeout, retry, backlog, certificate path |

This hierarchy organizes runtime responsibility; documentation follows from that structure.

It is the practical shape used by the framework. It appears in code, on the command line, and in configuration files.

#### Application scope

Application scope belongs to the executable as a whole.

It contains concerns that are not specific to one network endpoint. Examples include:

- selecting a configuration file,
- writing a configuration file,
- showing configuration,
- printing a generated command line,
- showing help and version information,
- logging level and log-file handling,
- daemonization,
- user and group selection for daemonized runs.

These options form the operational envelope in which all configured communication roles live.

They answer questions about the process as a program, not about a particular server port, peer address, Unix-domain path, Bluetooth channel, or TLS certificate used by one instance.

#### Instance scope

Instance scope belongs to one named server-side or client-side communication role.

It contains concerns such as:

- instance identity,
- server/client role identity,
- disabled state,
- configurability,
- and the set of sections that shape the role.

The server/client object in application code is the handle. In the configuration model, a named instance is the externally addressable configuration identity of the communication role that the handle configures and registers.

That distinction matters. The configuration system gives a communication role an operational address instead of merely decorating a local C++ variable.

#### Section scope

Section scope belongs to one aspect of one instance.

Common sections include:

- `local`,
- `remote`,
- `connection`,
- `socket`,
- `server`,
- `tls`.

A section groups options by responsibility.

The `local` section describes the local side.

The `remote` section describes the peer side.

The `connection` section describes established connection behavior.

The `socket` section describes socket-level behavior.

The `server` section describes server-role behavior.

The `tls` section describes TLS-related connection-layer behavior.

Sections are the boundaries between different kinds of responsibility inside one configured communication role. Help output reflects that boundary.

#### Same hierarchy in code, CLI, and files

The same hierarchy appears in three views:

| View | Example shape |
|---|---|
| C++ API | `instance.getConfig()->Local::setPort(8080)` |
| command line | `app instance section --option value` |
| configuration file | `instance.section.option = value` |

The syntax changes. The hierarchy remains the same.

That consistency is the main reason the detailed configuration model remains understandable. The C++ API gives the application direct programmatic control. The command line gives startup traversal and run-specific overrides. The configuration file gives a durable dotted-key representation of the same structure.

### Application configuration: the operational envelope

\index{application configuration}
\index{operational envelope}


Application configuration shapes the operational shell of the executable. It should not be confused with the configuration of one communication role.

Application-level options answer questions such as:

- Which configuration file should be read?
- Should a configuration file be written?
- Should the configuration be shown?
- Should a generated command line be printed?
- Should the application run as a daemon?
- Which log level should be used?
- Which log file should be used?
- Should the process run under a specific user or group?
- Should help or version information be displayed?

These are not address-family questions.

They do not say which port a server listens on or which peer a client connects to. They shape the executable as an operating program.

#### Operational shell of the executable

The application scope is above all instances. That boundary matters.

| Application-level concern | Why it belongs at application scope |
|---|---|
| configuration-file path | it controls how the executable reads or writes configuration |
| `--show-config` | it displays the model as parsed and configured |
| generated command line | it describes how to reproduce the selected configuration |
| logging | it affects the executable's operational visibility |
| daemonization | it affects process behavior |
| user/group selection | it affects process permissions |

These settings are shared by the application process. They are not owned by one server or client role.

#### Persistent and nonpersistent application options

Application options can be persistent or nonpersistent. Persistent options describe durable application shape and may be written into configuration files. Nonpersistent options inspect, generate, display, or control one run.

That distinction prevents operational commands from becoming durable configuration by accident. For example, a log level may be persistent. A request to show help, show configuration, print a command line, or write a configuration file is run-specific.

The distinction keeps the configuration file focused on lasting application behavior.

### Instance configuration: the configured communication role

\index{instance configuration}
\index{configured communication role}
\index{required options}


Instance configuration shapes one communication role.

A named instance is where the configuration model becomes concrete. It has an identity, a role, optional disabled state, and a collection of sections.

#### Named configurable communication roles

A named server handle such as:

```cpp
EchoServer echoServer("echo");
```

creates a communication role that can become addressable by the configuration system.

The name can appear:

- in command-line help,
- in command-line overrides,
- in generated command lines,
- in shown configuration,
- and in configuration-file keys.

Named instances matter for that reason.

They connect the handle to the operational surface of the application. The name is the address by which operators, scripts, configuration files, and diagnostic output can talk about that role.

#### Role identity: server or client

A configured role also has role identity. In the configuration model, that means an instance is constructed as a server role or a client role.

This text influences how the instance appears in help output and how its configuration is interpreted.

A server role is normally shaped around listening and accepting. A client role is normally shaped around connecting.

Both can share the same broad hierarchy, but their most important sections differ. For a server, `local` is usually central. For a client, `remote` is usually central.

#### Anonymous versus named instances

Chapter 16 distinguished anonymous and named instances.

Chapter 17 mostly concerns named instances, because named instances are addressable from the command line and from configuration files.

An anonymous instance may still be useful for an internal helper client or a temporary helper server. But once a communication role should be configured, disabled, persisted, inspected, or controlled from outside the source code, a named instance is usually the right model.

A useful distinction is:

| Anonymous instance | Named instance |
|---|---|
| application-internal role | externally addressable role |
| configured by code | configurable through the external hierarchy |
| not independently visible in CLI/file keys | visible in help, shown configuration, generated command lines, and files |
| useful for helper clients or small experiments | useful for operational communication roles |

This does not make anonymous instances inferior. It only means that they belong to a different design situation.

#### Disablement and requiredness

Disablement is a first-class instance state, not a loose Boolean label.

Disablement lets a configured role remain part of the application shape while being removed from the required startup path for a particular run. That matters for multi-instance programs.

An executable may contain several possible communication roles, while only some of them are active in a particular deployment. Configuration can then express that a role still exists, but is disabled for this run.

That is cleaner than removing the role from the application or inventing separate ad hoc flags.

It also keeps help output, configuration files, and generated command lines honest: the role still exists as part of the application design, but configuration decides whether it participates.

### Section configuration: scoped responsibilities

\index{section configuration}
\index{local section}
\index{remote section}
\index{connection section}
\index{socket section}
\index{server section}
\index{tls section}


Sections are the most important practical organizing device inside an instance. A section is a structural scope. It groups options that belong to one aspect of the communication role.

A compact overview is:

| Section | Main meaning |
|---|---|
| `local` | local endpoint or bind side |
| `remote` | peer endpoint or connect side |
| `connection` | behavior of established connections |
| `socket` | socket-level behavior, retry, and reuse settings |
| `server` | listen and accept behavior |
| `tls` | TLS connection-layer configuration |

Not every instance uses every section with the same importance.

Some sections appear only for particular role and layer combinations. The structure is shared, but the practical emphasis depends on the concrete instance.

The useful reading habit is:

```text
section name
  -> responsibility boundary
      -> representative options
```

This prevents the chapter from becoming a flat option catalogue.

#### The `local` section

The `local` section describes the local side of the communication role.

For a server, it is usually the most important endpoint section because it describes where the server binds or listens.

For a client, it may describe an explicit local bind side if the application does not want to leave that side wildcarded.

The concrete fields depend on the lower family.

| Lower family | Typical local fields |
|---|---|
| IPv4 / IPv6 | host and port |
| Unix domain sockets | path |
| RFCOMM | Bluetooth address and channel |
| L2CAP | Bluetooth address and PSM |

The idea is stable:

```text
local
  -> this side of the connection
```

The concrete option names depend on the lower family.

#### The `remote` section

The `remote` section describes the peer side.

For a client, it is usually central because it answers:

```text
Where should this client connect?
```

For example, an IPv4 client may need a remote host and port. A Unix-domain client may need a remote path. A Bluetooth client may need a Bluetooth address plus channel or PSM.

For a server, remote-side information may be less prominent in simple listen scenarios.

The durable distinction is:

```text
local side
  != remote side
```

That distinction remains useful across address families. The concrete fields change, but the conceptual boundary remains.

#### The `connection` section

The `connection` section describes behavior of established peer relationships.

Representative concerns include:

- read timeout,
- write timeout,
- read block size,
- write block size,
- termination timeout.

These are not endpoint identity values. They apply after a connection exists.

That makes the section boundary clear:

```text
connection
  -> behavior of the established connection
```

The `connection` section therefore belongs between the lower communication machinery and the protocol context. It does not decide where to bind or where to connect. It shapes how established peer relationships behave.

#### The `socket` section

The `socket` section describes socket-level behavior around creation, retry, and reuse.

Representative concerns include:

- address reuse,
- retry behavior,
- retry on fatal errors,
- retry timeout,
- retry attempts,
- exponential backoff,
- jitter,
- retry limit,
- role- or family-specific socket options.

The exact set depends on the concrete instance.

The section groups behavior that is closer to the socket and flow-control machinery than to the application protocol. A retry timeout, for example, is not part of an echo protocol. It belongs to the machinery that tries to establish or maintain a communication role.

#### The `server` section

The `server` section belongs to server-role behavior.

Representative concerns include:

- backlog,
- accepting behavior,
- accept-per-tick style limits where supported.

These settings are not generic connection options. They are about the listening and accepting side of a server role. That is why they belong in a server-specific section.

#### The `tls` section

The `tls` section belongs to TLS connection-layer configuration.

Representative examples include:

- certificate chain,
- certificate key,
- CA certificate or directory,
- cipher and option settings,
- SNI-related settings,
- TLS initialization or shutdown timeouts.

TLS is not a minor socket flag.

It is a connection-layer specialization. Grouping TLS configuration under `tls` keeps that concern separate from endpoint identity, socket retry behavior, and protocol behavior.

Chapter 19 discusses TLS in depth. Here the important point is the section boundary.

### Three views of the same model

\index{configuration!C++ API}
\index{configuration!command line}
\index{configuration!file}


Chapter 16 established that SNode.C has three input paths into one model.

Chapter 17 makes the practical consequence visible: the same hierarchy can be read in code, on the command line, and in configuration files.

#### C++ API view

In the C++ API, the hierarchy is visible through the configuration object and its section-qualified operations.

Schematic examples are:

```cpp
instance.getConfig()->Local::setPort(8080);
instance.getConfig()->Remote::setHost("localhost");
instance.getConfig()->Remote::setPort(8080);
```

`getConfig()` returns a pointer, so the examples use `->`. The section qualification is useful when local and remote meaning must remain visible.

In server-side cases, a shorter form may also be valid because there is no local/remote ambiguity at that call site:

```cpp
instance.getConfig()->setPort(8080);
```

The important habit is to think in sections even when the C++ syntax permits a shorter call. The shorter call may be readable in a small example, but the section-qualified call documents the architectural boundary.

#### Command-line view

On the command line, the hierarchy becomes a path:

```shell
echoserver echo local --port 8080
```

This can be read as:

```text
application: echoserver
instance:    echo
section:     local
option:      port
value:       8080
```

The command line is therefore a textual traversal of the configuration hierarchy rather than a flat collection of flags.

##### Command-line configuration as guided traversal

The command-line interface is also a guided configuration surface.

It can help the user discover the model step by step instead of requiring the full structure to be known in advance:

```shell
echoserver --help
echoserver echo --help
echoserver echo local --help
```

This mirrors the hierarchy: application help, then instance help, then section help, and finally option details.

The command line can also print command-line representations of the selected configuration. The `--command-line` option supports views such as `standard`, `required`, `active`, and `complete`.

Together with `--show-config` and `--write-config`, the command line becomes a way to inspect, reproduce, and persist the configuration of an application.

##### Guided errors for missing configuration

The same guided behavior appears when required configuration is missing.

A parameterless `listen()` or `connect()` can fail in a way that points the user back into the hierarchy: application, instance, section, and the required option inside that section.

A compact server-side session shows the idea. Here the executable is `echoserver` and the named server instance is `echo`:

```shell
$ echoserver
[RequiresError] echoserver requires echo

$ echoserver echo
[RequiresError] echoserver:echo requires local

$ echoserver echo local
[RequiresError] echoserver:echo:local requires --port

$ echoserver echo local --port
[ArgumentMismatch] --port: 1 required port:UINT in [0 - 65535] missing

$ echoserver echo local --port 8080
2026-06-06 18:04:05 0000000000001 echo: listening on '0.0.0.0:8080 (0.0.0.0)'
```

The exact timestamp and tick counter are run-specific. The direction matters: application, instance, section, option.

A named client instance follows the same idea, but the required section is usually `remote` rather than `local`. The CLI therefore teaches the structure while it reports the missing values.

##### Startup guidance, not arbitrary live reconfiguration

This command-line guidance belongs to startup and run configuration. It should not be confused with arbitrary post-start interactive reconfiguration of instances created later at runtime.

As Chapter 16 explained, command-line and file configuration apply to startup-known instances. Runtime-created roles must be shaped through the C++ API.

That boundary keeps the model clear: startup-known roles are guided by code, command-line arguments, and configuration files, while runtime-created roles must be configured by code.

The command line traverses the startup configuration model. It does not become a live management protocol for roles created later by application logic.

#### Configuration-file view

In a configuration file, the same hierarchy becomes a dotted key:

```ini
echo.local.port = 8080
echo.remote.host = "localhost"
echo.remote.port = 8080
```

The dotted key represents the same model: instance, section, option.

The syntax is different from the command line. The model is the same.

The file is therefore the persistent expression of the same hierarchy that the command line traverses and the C++ API configures directly, not a separate configuration universe.

### Required values and progressive disclosure

\index{required values}
\index{progressive disclosure}
\index{parameterless activation}


Parameterless `listen()` and `connect()` rely on configuration that is already present. If required configuration is missing, the error path can reveal the missing part of the hierarchy.

For a server, a missing port belongs to the `local` section of a specific configured instance.

For a client, missing peer information belongs to the `remote` section of that configured instance.

This is scoped error reporting.

It reinforces the structure of the configuration model. The error belongs to a scope that the user can inspect, instead of appearing as a generic failure.

#### Parameterless activation

A parameterless activation call such as:

```cpp
echoServer.listen(onStatus);
```

or:

```cpp
echoClient.connect(onStatus);
```

means that the communication role should already be configured enough to act.

The required values may have come from:

- C++ API defaults,
- a configuration file,
- command-line arguments,
- or the precedence model combining all three.

Therefore, parameterless activation is such a strong proof point for the configuration architecture. The call does not repeat the endpoint identity because the configured role already owns that identity.

#### Progressive disclosure as a teaching tool

Progressive disclosure is useful for operators, but it is also useful for readers.

It teaches the model in the order in which the model is structured. The same application/instance/section/option structure is therefore both an operator model and a reading model.

This is especially valuable in multi-instance programs. Instead of forcing every option into one flat help page, the hierarchy lets the user ask increasingly specific questions.

### Persistent and nonpersistent values

\index{persistent options}
\index{nonpersistent options}


Persistent options describe durable configuration. Nonpersistent options perform run-specific inspection or control. This distinction appears throughout the configuration model.

Persistent examples include values such as:

- endpoint host or port,
- Unix-domain path,
- Bluetooth channel or PSM,
- connection timeout,
- retry settings,
- TLS certificate paths,
- logging level or log-file path where configured as durable behavior.

Nonpersistent examples include:

- help,
- show configuration,
- generated command-line output,
- write-configuration action,
- version display,
- one-run control actions.

The important distinction is not whether an option is "important." Both kinds can be important. The distinction is whether the option describes lasting shape or performs an action for one run.

Configuration files should primarily describe durable shape. Command-line invocations can both supply durable values and trigger nonpersistent inspection actions.

### Generated and shown configuration

\index{shown configuration}
\index{generated configuration}


Generated configuration and shown configuration make the hierarchy inspectable.

A shown configuration helps answer:

```text
What did the application understand after code defaults, files, and command-line input were combined?
```

A generated configuration helps answer:

```text
What file form would represent this hierarchy?
```

A generated command line helps answer:

```text
What command-line form would reproduce the relevant option values?
```

These views are diagnostic tools. They make configuration visible instead of implicit.

That matters because configuration errors are often not bugs in protocol code. They are mismatches between intended deployment shape and actual configured values.

### Configuration files as operational artifacts

\index{configuration files}
\index{operational artifacts}


Configuration files are operational artifacts.

They should be readable by humans, stable enough for deployment, and close enough to the command-line hierarchy that users can move between both views without learning a second model.

The dotted-key structure helps:

```ini
echo.local.port = 8080
```

This can be read as:

```text
instance echo
  -> section local
      -> option port
```

For multi-instance applications, this becomes especially useful:

```ini
public.local.port = 8080
admin.local.port = 9090
backend.remote.host = "127.0.0.1"
backend.remote.port = 1883
```

Each key says which configured role it belongs to. That is the value of named instances. They make configuration files describe application structure, not just isolated values.

### Designing configuration for real applications

\index{configuration design}
\index{deployment shape}


The detailed model also suggests design habits.

#### Name externally operated roles

Externally operated server roles usually deserve names.

If a server binds a deployment-facing endpoint, accepts peers, uses TLS certificates, participates in logging, or may be disabled per deployment, it should normally be visible in the configuration hierarchy.

Helper clients may remain anonymous when they are intentionally internal to application logic.

The question is not:

```text
Can this role be named?
```

The better question is:

```text
Should this role be independently configured, inspected, persisted, or disabled?
```

If yes, naming it is usually the clearer design.

#### Keep endpoint options in endpoint sections

Endpoint values should live in `local` or `remote`, not in random application flags.

That makes address-family differences manageable. IPv4, IPv6, Unix-domain sockets, RFCOMM, and L2CAP all have different concrete endpoint fields, but the local/remote distinction remains stable.

This is the same design lesson as Chapters 08–12, now expressed through configuration.

#### Keep protocol behavior out of configuration

Configuration can select endpoints, timeouts, retry behavior, TLS settings, and activation shape. It should not become the protocol implementation.

The protocol still belongs in `SocketContext`.

The construction boundary still belongs in `SocketContextFactory`.

Configuration should expose variation; it should not replace application design.

#### Avoid hiding deployment shape in source-only defaults

C++ defaults are useful. They make examples small. They provide reasonable baselines. They help tests and embedded use cases.

But deployment-facing choices often deserve external visibility. Ports, paths, certificate files, log files, daemonization, and enablement are easier to operate when they are visible through the configuration hierarchy.

A good application can use both: source-level defaults for clarity and external configuration for deployment.

### What remains stable

Across all these details, the application/instance/section/option hierarchy remains the stable spine of configuration.

The application gives the operational envelope. The instance gives the configured communication role an address. The section gives one responsibility scope.

The option gives one value. The same structure appears in C++ API calls, command-line traversal, and configuration-file keys. Therefore, the configuration model scales from a small echo example to applications with several communication roles.

::: {.snodec-remember title="What to remember"}
- The configuration hierarchy is `application -> instance -> section -> option`.
- Application configuration describes the operational envelope of the executable.
- A named instance is an externally addressable configured communication role; an anonymous instance remains internal to application code.
- Sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls` group options by responsibility.
- The same hierarchy appears through the C++ API, command line, and configuration files.
- Disablement lets a role remain present while no longer blocking startup as a required participant.
:::
