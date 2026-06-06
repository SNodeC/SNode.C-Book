## Application and Instance Configuration in Detail

### From configuration philosophy to configuration anatomy

Chapter 16 introduced configuration as one of the main ways an instance becomes a concrete communication role.

This chapter looks at the practical structure of that model.

The core hierarchy is:

```text
application
  -> instance
      -> section
          -> option
```

The application is the executable-level operational shell.

An instance is one configured communication role inside that application.

A section is one scoped part of that instance configuration.

An option is one concrete value inside such a scope.

This chapter follows that hierarchy.

### The configuration hierarchy

The configuration model is easiest to read from the outside inward.

| Scope | Addressed by | Typical concerns |
|---|---|---|
| application | executable-level options | config file, logging, daemonization, help, generated command line |
| instance | named server/client instance | disabled state, role identity, section collection |
| section | `local`, `remote`, `connection`, `socket`, `server`, `tls` | concrete endpoint or behavioral settings |
| option | individual setting | host, port, timeout, retry, backlog, certificate path |

This hierarchy is not only a way to organize documentation.

It is the practical shape used by the framework.

It appears in code, on the command line, and in configuration files.

#### Application scope

Application scope belongs to the executable as a whole.

It contains concerns that are not specific to one network endpoint.

Examples include:

- selecting a configuration file,
- writing a configuration file,
- showing current configuration,
- printing a generated command line,
- showing help and version information,
- logging level and log-file handling,
- daemonization,
- user and group selection for daemonized runs.

These options form the operational envelope in which all configured communication roles live.

#### Instance scope

Instance scope belongs to one named server or client instance.

It contains concerns such as:

- instance identity,
- server/client role identity,
- disabled state,
- configurability,
- and the set of sections that shape the role.

An instance is therefore not just a C++ object with some fields.

In the configuration model, a named instance is an addressable communication role.

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

#### Same hierarchy in code, CLI, and files

The same hierarchy appears in three views:

| View | Example shape |
|---|---|
| C++ API | `instance.getConfig()->Local::setPort(8080)` |
| command line | `app instance section --option value` |
| configuration file | `instance.section.option = value` |

The syntax changes.

The hierarchy remains the same.

That consistency is the main reason the detailed configuration model remains understandable.

### Application configuration

Application configuration shapes the operational shell of the executable.

It should not be confused with the configuration of one communication role.

Application-level options answer questions such as:

- Which configuration file should be read?
- Should a configuration file be written?
- Should the current configuration be shown?
- Should a generated command line be printed?
- Should the application run as a daemon?
- Which log level should be used?
- Which log file should be used?
- Should the process run under a specific user or group?
- Should help or version information be displayed?

These are not address-family questions.

They do not say which port a server listens on or which peer a client connects to.

They shape the executable as an operating program.

#### Operational shell of the executable

The application scope is above all instances.

That boundary matters.

For example:

| Application-level concern | Why it belongs at application scope |
|---|---|
| configuration-file path | it controls how the executable reads or writes configuration |
| `--show-config` | it displays the current model |
| generated command line | it describes how to reproduce the current configuration |
| logging | it affects the executable's operational visibility |
| daemonization | it affects process behavior |
| user/group selection | it affects process permissions |

These settings are shared by the application process.

They are not owned by one server or client role.

#### Persistent and non-persistent application options

Application options can be persistent or non-persistent.

Persistent options may be written into configuration files.

Non-persistent options affect the current run only.

That distinction prevents operational commands from becoming durable configuration by accident.

For example, a log level may be persistent.

A request to show help or write a configuration file is normally run-specific.

The distinction keeps the configuration file focused on lasting application behavior.

### Instance configuration

Instance configuration shapes one communication role.

A named instance is where the configuration model becomes concrete.

It has an identity, a role, optional disabled state, and a collection of sections.

#### Named configurable communication roles

A named instance such as:

```cpp
EchoServer echoServer("echo");
```

becomes addressable by the configuration system.

The name can appear:

- in command-line help,
- in command-line overrides,
- in generated command lines,
- in shown configuration,
- and in configuration-file keys.

That is why named instances matter.

They connect the C++ object to the operational surface of the application.

#### Role identity: server or client

An instance also has role identity.

In the configuration model, that means an instance is constructed as a server role or a client role.

This is not merely descriptive text.

It influences how the instance appears in help output and how its configuration is interpreted.

A server role is normally shaped around listening and accepting.

A client role is normally shaped around connecting.

Both can share the same broad hierarchy, but their most important sections differ.

For a server, `local` is usually central.

For a client, `remote` is usually central.

#### Anonymous versus named instances

Chapter 16 distinguished anonymous and named instances.

Chapter 17 mostly concerns named instances, because named instances are addressable from the command line and from configuration files.

An anonymous instance may still be useful for an internal helper client or a temporary helper server.

But once a communication role should be configured, disabled, persisted, inspected, or controlled from outside the source code, a named instance is usually the right model.

#### Disablement and requiredness

Disablement is a first-class instance state.

It is not only a Boolean label.

In SNode.C, disabling an instance also affects requiredness: an inactive role can remain present without blocking startup because required options for that disabled instance can be forced to become unrequired.

That is important for multi-instance programs.

An executable may contain several possible communication roles, while only some of them are active in a particular deployment.

The configuration can then express:

```text
this role exists
  -> but it is currently disabled
```

That is cleaner than removing the role from the application or inventing separate ad hoc flags.

### Section configuration

Sections are the most important practical organizing device inside an instance.

A section is a structural scope.

It groups options that belong to one aspect of the communication role.

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

Some sections appear only for particular role and layer combinations.

The structure is shared, but the practical emphasis depends on the concrete instance.

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

For example, an IPv4 client may need a remote host and port.

A Unix-domain client may need a remote path.

A Bluetooth client may need a Bluetooth address plus channel or PSM.

For a server, remote-side information may be less prominent in simple listen scenarios.

The important conceptual distinction still holds:

```text
local side
  != remote side
```

That distinction remains useful across address families.

#### The `connection` section

The `connection` section describes behavior of established peer relationships.

Typical concerns include:

- read timeout,
- write timeout,
- read block size,
- write block size,
- termination timeout.

These are not endpoint identity values.

They apply after a connection exists.

That makes the section boundary clear:

```text
connection
  -> behavior of the established connection
```

#### The `socket` section

The `socket` section describes socket-level behavior around creation, retry, and reuse.

Typical concerns include:

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

The section groups behavior that is closer to the socket and flow-control machinery than to the application protocol.

#### The `server` section

The `server` section belongs to server-role behavior.

Typical concerns include:

- backlog,
- accepting behavior,
- accept-per-tick style limits where supported.

These settings are not generic connection options.

They are about the listening and accepting side of a server role.

That is why they belong in a server-specific section.

#### The `tls` section

The `tls` section belongs to TLS connection-layer configuration.

Typical examples include:

- certificate chain,
- certificate key,
- CA certificate or directory,
- cipher and option settings,
- SNI-related settings,
- TLS initialization or shutdown timeouts.

TLS is not a minor socket flag.

It is a connection-layer specialization.

Grouping TLS configuration under `tls` keeps that concern separate from endpoint identity, socket retry behavior, and application protocol behavior.

Chapter 19 discusses TLS in depth.

Here the important point is the section boundary.

### Three views of the same model

Chapter 16 established that SNode.C has three input paths into one model.

Chapter 17 makes the practical consequence visible.

The same hierarchy can be read in code, on the command line, and in configuration files.

#### C++ API view

In the C++ API, the hierarchy is visible through the configuration object and its section-qualified operations.

Schematic examples are:

```cpp
instance.getConfig()->Local::setPort(8080);
instance.getConfig()->Remote::setHost("localhost");
instance.getConfig()->Remote::setPort(8080);
```

`getConfig()` returns a pointer, so the examples use `->`.

The section qualification is useful when local and remote meaning must remain visible.

In server-side cases, a shorter form is also valid because there is no local/remote ambiguity:

```cpp
instance.getConfig()->setPort(8080);
```

The important habit is to think in sections even when the C++ syntax permits a shorter call.

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

The command line is therefore not just a flat collection of flags.

It is a textual traversal of the configuration hierarchy.

#### Command-line configuration as guided traversal

The command-line interface is also a guided configuration surface.

It can help the user discover the model step by step instead of requiring the full structure to be known in advance:

```shell
echoserver --help
echoserver echo --help
echoserver echo local --help
```

This mirrors the hierarchy:

```text
application help
  -> instance help
      -> section help
          -> option details
```

The command line can also print command-line representations of the current configuration.

The `--command-line` option supports views such as `standard`, `required`, `full`, and `default`.

Together with `--show-config` and `--write-config`, this makes the command line more than a parser: it becomes a way to inspect, reproduce, and persist the configuration of an application.

#### Guided errors for missing configuration

The same guided behavior appears when required configuration is missing.

A parameterless `listen()` or `connect()` can fail in a way that points the user back into the hierarchy:

```text
application
  -> instance
      -> section
          -> required option
```

A compact server-side session shows the idea.

Here the executable is `echoserver` and the named server instance is `echo`:

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

The exact timestamp and tick counter are run-specific.

The important point is the direction.

The CLI leads from application, to instance, to section, to option.

A named client instance follows the same idea, but the required section is usually `remote` rather than `local`.

The CLI therefore teaches the structure while it reports the missing values.

#### Startup guidance, not arbitrary live reconfiguration

This command-line guidance belongs to startup and run configuration.

It should not be confused with arbitrary post-start interactive reconfiguration of instances created later at runtime.

As Chapter 16 explained, command-line and file configuration apply to startup-known instances. Runtime-created instances must be shaped through the C++ API.

That boundary keeps the model clear:

```text
startup-known roles
  -> guided by code, command line, and configuration files

runtime-created roles
  -> configured by code
```

#### Configuration-file view

In a configuration file, the same hierarchy becomes a dotted key:

```ini
echo.local.port = 8080
echo.remote.host = "localhost"
echo.remote.port = 8080
```

The dotted key is the file representation of:

```text
instance
  -> section
      -> option
```

The syntax is different from the command line.

The model is the same.

### Required values and progressive disclosure

Parameterless `listen()` and `connect()` rely on configuration that is already present.

If required configuration is missing, the error path can reveal the missing part of the hierarchy.

For a server, a missing port can be understood as:

```text
application
  -> instance
      -> local
          -> port
```

For a client, missing peer information can be understood as:

```text
application
  -> instance
      -> remote
          -> host / port
```

This is more than error reporting.

It reinforces the structure of the configuration model.

#### Parameterless activation

A parameterless call such as:

```cpp
echoServer.listen(onStatus);
```

or:

```cpp
echoClient.connect(onStatus);
```

means that the instance should already have the required values.

Those values may come from:

- C++ API defaults,
- a configuration file,
- command-line arguments,
- or a combination of those according to the precedence rule.

Activation then uses the shaped instance.

It does not need to repeat the endpoint values at the call site.

#### Missing configuration points back into the hierarchy

When a required value is absent, the missing value is not arbitrary.

It belongs to a scope.

A missing server port belongs to the `local` section of a server instance.

A missing client host belongs to the `remote` section of a client instance.

A missing TLS certificate belongs to the `tls` section of a TLS instance.

That makes error reporting easier to understand.

It also makes the configuration model easier to learn by use.

### Persistence and generated configuration

Configuration is also about durable operational state.

Persistent options can be written to configuration files.

Non-persistent options affect the current run only.

#### Application-level and instance-level persistence

Persistence can apply at different levels.

Application-level persistent options describe lasting executable behavior, such as logging choices.

Instance-level persistent options describe lasting role behavior, such as whether a named instance is disabled.

Section-level persistent options describe lasting details of that role, such as endpoint values or retry settings.

The hierarchy remains:

```text
application
  -> instance
      -> section
          -> option
```

Persistence does not create a new model.

It stores the same model.

#### Commented defaults as inspection

Generated configuration output can show defaults and configured values.

Default values may appear commented.

That is useful because it lets the operator see:

- which options exist,
- which values are defaults,
- which values have been supplied,
- which values could be made explicit.

A generated configuration file is therefore not only a file to edit.

It is also a readable map of the current configuration space.

### Multi-instance applications

The detailed configuration model becomes especially valuable when one executable contains more than one communication role.

Each named instance can have:

- its own name,
- its own server/client role identity,
- its own disabled state,
- its own sections,
- its own endpoint values,
- its own socket behavior,
- and its own TLS or non-TLS configuration where applicable.

This lets one process host several roles without collapsing the configuration into an unstructured list of flags.

A multi-instance application can therefore be read as:

```text
application
  -> instance A
      -> sections for A

  -> instance B
      -> sections for B

  -> instance C
      -> sections for C
```

#### Switching between instances on the command line

On the command line, switching between instances is done by naming the next instance.

All section names and options following an instance name belong to that instance until another instance name is encountered.

For example:

```shell
myapp instance1 local --port 8001 socket --retry true \
      instance2 local --port 8002 socket --retry false
```

This configures `instance1` first, then switches to `instance2`.

Within one instance, a later section name changes the active section for that same instance.

The structure is still:

```text
application
  -> instance
      -> section
          -> option
```

Only the active instance and active section change as the command line is read from left to right.

### Reading a configuration

A good reading order is simple.

Do not start by scanning values randomly.

Read from the outside inward.

Ask:

1. What are the application-wide operational settings?
2. Which named instances exist?
3. Which instances are enabled or disabled?
4. For each enabled instance, which sections shape the role?
5. Which concrete options inside those sections differ from defaults?

This reading order mirrors the architecture.

It helps separate process-level concerns from communication-role concerns.

It also helps distinguish endpoint identity, socket behavior, connection behavior, and security configuration.

### What to remember

Remember:

- Application configuration shapes the executable's operational shell.
- Instance configuration shapes one named communication role.
- Section configuration shapes one aspect of that role.
- The hierarchy is application, instance, section, option.
- Named instances are addressable in command-line and configuration-file views.
- Disablement is a first-class instance state and affects requiredness.
- `local` and `remote` preserve endpoint-side semantics.
- `connection`, `socket`, `server`, and `tls` describe different behavioral scopes.
- The C++ API, command line, and configuration file are three views of the same hierarchy.
- The command line can guide users through application, instance, section, and option scopes.
- `--command-line`, `--show-config`, and `--write-config` make configuration inspectable, reproducible, and persistent.
- Required-configuration errors point back into the same hierarchy.
- Generated configuration can serve as an inspectable map of available options.
- Multi-instance applications stay readable because each named role has its own sections.
- On the command line, naming another instance switches the following sections and options to that instance.
- Chapter 18 turns from configured structure to runtime visibility.

### Closing perspective

Chapter 16 explained why configuration is architectural in SNode.C.

Chapter 17 showed the working anatomy of that configuration model.

The central structure is:

```text
application
  -> instance
      -> section
          -> option
```

The application scope describes the executable's operational shell.

The instance scope describes one communication role.

The section scope describes one part of that role.

The option scope contains the concrete value.

With that structure in place, configuration is no longer a flat list of flags.

It is a readable description of how the application and its communication roles are shaped.

The next chapter turns to runtime visibility.

Once roles are configured and activated, the next question is how to observe them, diagnose them, and understand what they are doing while the application runs.
