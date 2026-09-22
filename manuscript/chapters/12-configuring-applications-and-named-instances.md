## Configuring Applications and Named Instances {#configuring-applications-and-named-instances}

### Configuration principles {#configuration-philosophy-in-snodec}

\index{configuration}
\index{configuration philosophy}
\index{configured communication role}


#### From lower-family transfer to configured communication roles

Configuration is where many architectural choices become visible to the executable and to the operator.

The protocol behavior may remain in the same `SocketContext`. The context creation policy may remain in the same `SocketContextFactory`.

But the concrete application still has to decide which server-side or client-side role exists, which lower family it uses, which endpoint identity it receives, whether it uses legacy or TLS connection handling, whether it is enabled, and which values belong in source code, a configuration file, or a run-specific command line.

That is the subject of this chapter.

Part IV separated protocol behavior, context construction, lower-family selection, and endpoint identity. Part V asks how these choices become visible, adjustable, persistent, and operable.

In SNode.C, configuration makes a communication role concrete: it gives the role endpoint values, operational switches, instance identity, and activation-time shape.

Through a `SocketServer` or `SocketClient` handle, the application configures a server-side or client-side communication role. Constructing a named endpoint registers its configuration instance. Each `listen(...)` or `connect(...)` call then starts an activation flow for that configured role.

Configuration therefore gives the role its operational shape instead of decorating an otherwise complete object.

#### Configuration as part of the architecture

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

That is why this chapter belongs immediately after Chapter 11. Lower-family transfer is practical only when the changing parts have somewhere clear to live; in SNode.C, configuration provides that place.

##### A configured communication role

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

##### One model, several entry paths

SNode.C has three main configuration input paths:

| Input path | Main use |
|---|---|
| C++ API | baseline defaults and programmatic shaping |
| configuration file | persistent operational configuration |
| command line | run-specific override, discovery, and control |

These are not three unrelated configuration worlds. They are three ways to feed one underlying configuration model. The C++ API gives the application a baseline.

The configuration file gives deployment a durable expression. The command line gives a run-specific control surface.

That matters because the same conceptual role can be shaped in code, persisted in a file, and overridden for one invocation without changing its identity.

#### Three input paths, one configuration model

\index{configuration!C++ API}
\index{configuration!command line}
\index{configuration!file}


The three input paths have different strengths. They should be understood together.

##### Configuration through the C++ API

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

##### Configuration through the command line

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

##### Configuration through configuration files

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

#### Precedence and the startup boundary

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

##### Instance creation timing

There is also an important timing boundary.

External configuration can address the named roles present in the hierarchy when parsing occurs. Startup parsing therefore sees the roles constructed before startup. A role created later begins with the values supplied by application logic.

The current framework also supports a deliberate runtime reparse through `core::SNodeC::reconfigure()`. While the event loop is `RUNNING`, application code on the event-loop thread can ask the existing parser to read the current configuration file again, with the original command-line arguments still taking precedence. A named role that is now registered can participate in that parse. Merely editing the file or constructing a role does not trigger this operation.

The distinction is between changing configuration values and changing live activity. Reconfiguration does not restart listeners, reconnect peers, or replace the policy already captured by an established connection. It also leaves bootstrap logging and daemonization in place. The application must decide which subsequent activation should use the new values and how existing activity should finish.

A failed reparse returns `false`; it is not a transaction that rolls back every value already changed. The section “Application and instance configuration” develops the operational consequences. For a service whose configuration must change atomically, validating a replacement before a controlled process restart may be a clearer policy than editing the live tree.

The current per-call flow model makes the configuration boundary particularly important. An endpoint exposes one shared configuration object. Each explicit activation receives its own controller, but that controller does not freeze a private copy of the endpoint settings. An address-taking `connect(...)` overload updates the endpoint's remote configuration before starting its flow. Use separate named endpoints for destinations that need independent configuration; retaining two flow handles is not a substitute for that separation.

#### Named instances as configuration addresses

\index{named instances}
\index{configuration addresses}
\index{instance names}


One of the most important ideas in the configuration model is the difference between anonymous and named instances. An anonymous instance exists as a configured role in application code. A named instance also becomes addressable by the external configuration hierarchy.

That is the key distinction.

##### Anonymous and named instances

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

##### Why names matter

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

##### Disablement as instance-level configuration

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

#### Sections as structural scopes

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

##### Section hierarchy

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

##### Local and remote sections

The `local` and `remote` sections are especially important because they connect directly to the address semantics from Chapters 6–8.

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

##### Connection, socket, server, and TLS sections

Other sections describe other parts of the communication role.

For example:

| Section | Typical scope |
|---|---|
| `connection` | established connection behavior, timeouts, read/write behavior |
| `socket` | socket-level behavior such as retry or reuse options |
| `server` | server-specific behavior |
| `tls` | TLS-related connection-layer configuration |

The section “Application and instance configuration” develops these details concretely.

For the section “Configuration principles”, the important point is the structure:

```text
sections are scopes
not loose option groups
```

This keeps configuration readable. A timeout, an address, a TLS certificate path, and a server backlog do not all live in one flat pile. They belong to different scopes of the same configured role.

#### Configuration as discovery, persistence, and inspection

\index{configuration!discovery}
\index{persistent options}
\index{generated configuration}


A good configuration system should not only accept values. It should help users discover what can be configured, inspect the active shape, and persist durable choices. SNode.C does this through command-line help, configuration display, command-line generation, and generated configuration files.

##### Help output as discovery

Because named instances and sections participate in the command-line hierarchy, help output can reveal the configuration model step by step.

At application level, help shows application-wide options and available instances. At instance level, help shows instance-level options and sections. At section level, help shows the options for that section.

This makes the configuration system self-describing. The user does not have to guess the entire option universe at once. The hierarchy itself teaches the shape of the application.

##### Persistent and nonpersistent options

Not every option should be written into a configuration file. Some options describe lasting behavior. Others describe one run.

SNode.C makes that distinction visible by separating persistent and nonpersistent options.

The practical rule is simple: persistent options may be stored in configuration files, while nonpersistent options affect inspection, generation, help, or the current run only.

Persistent options describe the desired shape of an application or instance. Nonpersistent options trigger inspection, generation, display, help, or one-run control actions.

This prevents operational commands such as help, display, command-line generation, or write-config from being confused with enduring instance configuration.

##### Generated and shown configuration

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

#### Parameterless `listen()` and `connect()`

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

##### Configured enough to act

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

##### Missing configuration is reported structurally

When required configuration is missing, the error path should point back into the same hierarchy. For example, a missing server port belongs to the configured server role that required it.

For a server-side role, the hierarchy commonly narrows to the `local` section and then to a concrete option such as `port`.

A missing client host or port likewise belongs to the remote section of a particular client instance. Therefore, parameterless activation is a strong proof point. It works only because the role has a structured configuration identity.

#### Configuration can describe itself to another program

The configuration model now has a machine-readable description carried inside its ordinary INI-compatible output. Structured `#@` comment records describe the document, nodes, groups, and options while leaving the real configuration assignments as INI text.

That is an extension of the existing configuration surface, not a parallel JSON configuration system. Existing files without metadata remain valid. The metadata is available when description/comment output is enabled, as with `--show-config`.

The distinction is useful operationally. A tool can discover the application/instance/section tree without guessing structure from a flat list of dotted keys, while the target application remains responsible for validation and canonical configuration output. The section “Application and instance configuration” shows how `snodec-control` uses that separation.

#### CLI11 as implementation foundation

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

#### Choosing what operators can change

An external option is a promise to operators. Naming a role makes its endpoint and policy visible, but also makes those names part of configuration files, service definitions, and diagnostic procedures. Expose choices that deployments need to own; keep an internal helper’s construction detail in code when changing it independently would violate the application’s assumptions.

Startup-only configuration has a useful cost model: one validated process begins with one intended deployment shape. Runtime reconfiguration can avoid a full restart, but requires a policy for partial failure, existing connections, and future activation. The framework supplies the parsing operation. It cannot decide those application consequences from an option name.

The following section makes the distinction observable. We will inspect the same port supplied in code, overridden by a file, and overridden again for one invocation before discussing what a runtime reparse does with that hierarchy.

### Application and instance configuration {#application-and-instance-configuration-in-detail}

\index{application configuration}
\index{instance configuration}
\index{configuration hierarchy}


#### From configuration philosophy to configuration anatomy

Constructing a named endpoint registers its configuration instance. The values in that hierarchy then shape each activation of the communication role.

This chapter looks at the practical anatomy of that model.

The core hierarchy is application, instance, section, and option.

The application is the executable-level operational shell. A named instance is the externally addressable configuration identity of one configured communication role inside that application. A section is one scoped part of that instance configuration.

An option is one concrete value inside such a scope.

This chapter follows that hierarchy from the outside inward. The important skill is not memorizing every possible option, but understanding where a value belongs, why it belongs there, and how the same structure appears in C++ code, on the command line, and in configuration files.

#### The anatomy of the configuration hierarchy

\index{configuration hierarchy}
\index{application scope}
\index{instance scope}
\index{section scope}


The configuration model is easiest to read from the outside inward. Figure \ref{fig:configuration-hierarchy} shows that hierarchy as one structural model. The named-instance level is where a configured server/client role receives an externally addressable identity and can be enabled or disabled without removing the role from the application shape.

![A representative named-endpoint hierarchy: application, instance, section, and option. Options can also belong directly to application or instance scope; discovery can describe deeper or anonymous nodes.](assets/figures/pdf/fig-13-configuration-hierarchy.pdf){#fig:configuration-hierarchy width=90% latex-placement="tbp"}

The figure is a placement model. It shows where configuration meaning belongs: executable-wide concerns at application scope, externally addressable communication roles at instance scope, responsibility groups at section scope, and individual values at option scope. The concrete sections and options in real applications are narrower and more numerous than the diagram needs to show.

| Scope | Addressed by | Typical concerns |
|---|---|---|
| application | executable-level options | config file, logging, daemonization, help, generated command line |
| instance | named server/client communication role | disabled state, role identity, section collection |
| section | `local`, `remote`, `connection`, `socket`, `server`, `tls` | concrete endpoint or behavioral settings |
| option | individual setting | host, port, timeout, retry, backlog, certificate path |

This hierarchy organizes runtime responsibility; documentation follows from that structure.

It is the practical shape used by the framework. It appears in code, on the command line, and in configuration files.

##### Application scope

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

##### Instance scope

Instance scope belongs to one named server-side or client-side communication role.

It contains concerns such as:

- instance identity,
- server/client role identity,
- disabled state,
- configurability,
- and the set of sections that shape the role.

The server/client object in application code is the handle. In the configuration model, a named instance is the externally addressable configuration identity of the communication role that the handle configures and registers.

That distinction matters. The configuration system gives a communication role an operational address instead of merely decorating a local C++ variable.

##### Section scope

Section scope belongs to one aspect of one instance.

To locate an option, ask what it controls. A bind port belongs under `local`; a peer port under `remote`; an established connection’s timeout under `connection`. The detailed section descriptions below turn this placement rule into a map of the available responsibilities.

This is also a useful discovery exercise: start with a named instance’s help, choose the section that should own the value, and check its help before inventing an application-wide flag.

##### Same hierarchy in code, CLI, and files

The same hierarchy appears in three views:

| View | Example shape |
|---|---|
| C++ API | `instance.getConfig()->Local::setPort(8080)` |
| command line | `app instance section --option value` |
| configuration file | `instance.section.option = value` |

The syntax changes. The hierarchy remains the same.

That consistency is the main reason the detailed configuration model remains understandable. The C++ API gives the application direct programmatic control. The command line gives startup traversal and run-specific overrides. The configuration file gives a durable dotted-key representation of the same structure.

#### Application configuration: the operational envelope

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

##### Operational shell of the executable

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

##### Persistent and nonpersistent application options

Application options can be persistent or nonpersistent. Persistent options describe durable application shape and may be written into configuration files. Nonpersistent options inspect, generate, display, or control one run.

That distinction prevents operational commands from becoming durable configuration by accident. For example, a log level may be persistent. A request to show help, show configuration, print a command line, or write a configuration file is run-specific.

The distinction keeps the configuration file focused on lasting application behavior.

#### Instance configuration: the configured communication role

\index{instance configuration}
\index{configured communication role}
\index{required options}


Instance configuration shapes one communication role.

A named instance is where the configuration model becomes concrete. It has an identity, a role, optional disabled state, and a collection of sections.

##### Named configurable communication roles

A named server handle such as:

```cpp
EchoServer echoServer("echo");
```

creates a communication role that can become addressable by the configuration system.

The string `"echo"` is an operational key. Renaming the C++ variable `echoServer` does not rename that key. Changing the string does: deployment files, overrides, and diagnostic procedures that address `echo` must then change together.

Treat such a rename as an application-interface change, even when the C++ program still compiles. The section “Configuration principles”’s naming choice becomes a compatibility decision once another person or script depends on it.

##### Role identity: server or client

A configured role also has role identity. In the configuration model, that means an instance is constructed as a server role or a client role.

This text influences how the instance appears in help output and how its configuration is interpreted.

A server role is normally shaped around listening and accepting. A client role is normally shaped around connecting.

Both can share the same broad hierarchy, but their most important sections differ. For a server, `local` is usually central. For a client, `remote` is usually central.

##### Anonymous versus named instances

The section “Configuration principles” distinguished anonymous and named instances.

The section “Application and instance configuration” mostly concerns named instances, because named instances are addressable from the command line and from configuration files.

An anonymous instance may still be useful for an internal helper client or a temporary helper server. But once a communication role should be configured, disabled, persisted, inspected, or controlled from outside the source code, a named instance is usually the right model.

A useful distinction is:

| Anonymous instance | Named instance |
|---|---|
| application-internal role | externally addressable role |
| configured by code | configurable through the external hierarchy |
| not independently visible in CLI/file keys | visible in help, shown configuration, generated command lines, and files |
| useful for helper clients or small experiments | useful for operational communication roles |

This does not make anonymous instances inferior. It only means that they belong to a different design situation.

##### Disablement and requiredness

Disablement is a first-class instance state, not a loose Boolean label.

Disablement lets a configured role remain part of the application shape while being removed from the required startup path for a particular run. That matters for multi-instance programs.

An executable may contain several possible communication roles, while only some of them are active in a particular deployment. Configuration can then express that a role still exists, but is disabled for this run.

That is cleaner than removing the role from the application or inventing separate ad hoc flags.

It also keeps help output, configuration files, and generated command lines honest: the role still exists as part of the application design, but configuration decides whether it participates.

#### Section configuration: scoped responsibilities

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

##### The `local` section

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

##### The `remote` section

The `remote` section describes the peer side.

For a client, it is usually central because it answers:

```text
Where should this client connect?
```

For example, an IPv4 client may need a remote host and port. A Unix-domain client may need a remote path. A Bluetooth client may need a Bluetooth address plus channel or PSM.

An accepted server connection also has a remote peer address. That observation does not give the listening server a configurable `remote` section: the listener configures its local endpoint, while each accepted connection supplies the peer information.

The durable distinction is:

```text
local side
  != remote side
```

That distinction remains useful across address families. The concrete fields change, but the conceptual boundary remains.

##### The `connection` section

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

##### The `socket` section

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

##### The `server` section

The `server` section belongs to server-role behavior.

Representative concerns include:

- backlog,
- accepting behavior,
- accept-per-tick style limits where supported.

These settings are not generic connection options. They are about the listening and accepting side of a server role. That is why they belong in a server-specific section.

##### The `tls` section

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

Chapter 14 discusses TLS in depth. Here the important point is the section boundary.

#### Three views of the same model

\index{configuration!C++ API}
\index{configuration!command line}
\index{configuration!file}


The section “Configuration principles” established that SNode.C has three input paths into one model.

The section “Application and instance configuration” makes the practical consequence visible: the same hierarchy can be read in code, on the command line, and in configuration files.

##### C++ API view

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

##### Command-line view

On the command line, the hierarchy becomes a path:

```sh
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

###### Command-line configuration as guided traversal

The command-line interface is also a guided configuration surface.

It can help the user discover the model step by step instead of requiring the full structure to be known in advance:

```sh
echoserver --help
echoserver echo --help
echoserver echo local --help
```

This mirrors the hierarchy: application help, then instance help, then section help, and finally option details.

The command line can also print command-line representations of the selected configuration. The `--command-line` option supports views such as `standard`, `required`, `active`, and `complete`.

Together with `--show-config` and `--write-config`, the command line becomes a way to inspect, reproduce, and persist the configuration of an application.

###### Guided errors for missing configuration

The same guided behavior appears when required configuration is missing.

A parameterless `listen()` or `connect()` can fail in a way that points the user back into the hierarchy: application, instance, section, and the required option inside that section.

A schematic server-side session shows the idea. Here the executable is `echoserver` and the named server instance is `echo`; the exact diagnostic wording depends on the target application:

```sh
$ echoserver
[RequiresError] echoserver requires echo

$ echoserver echo
[RequiresError] echoserver:echo requires local

$ echoserver echo local
[RequiresError] echoserver:echo:local requires --port

$ echoserver echo local --port
[ArgumentMismatch] --port: 1 required port:UINT in [0 - 65535] missing

$ echoserver echo local --port 8080
# The configured role can now enter its listening path.
```

The successful path now uses the semantic logging surface explained in Chapter 13. The direction matters here: application, instance, section, option.

A named client instance follows the same idea, but the required section is usually `remote` rather than `local`. The CLI therefore teaches the structure while it reports the missing values.

###### Startup discovery and explicit runtime reconfiguration

Help and the command line describe the executable’s configuration surface. They do not open an interactive management channel into a running process. The current source provides a separate application decision: call `core::SNodeC::reconfigure()` from the event-loop thread while the runtime is `RUNNING`. `express::WebApp::reconfigure()` forwards the same operation.

The operation reparses the existing root hierarchy using the original arguments and the configuration file as it now exists. Original command-line values keep their precedence. Registered endpoint final validators run again, including for a replacement named configuration created after an earlier instance was destroyed and unregistered.

| Observation | Meaning |
|---|---|
| `true` | this runtime parse and validation succeeded |
| `false` before `RUNNING` or during shutdown | the lifecycle does not permit the operation |
| `false` from a file, value, or validation error | the parse failed; previously changed values are not automatically rolled back |
| changed endpoint values | future code can consume them; existing sockets are not restarted |
| changed logging or daemonization options | parsed values do not replace bootstrap side effects or frozen logging policy |

A successful reparse is therefore only one step in a live configuration change. The application still decides whether to end a flow, let a connection drain, construct a replacement role, or defer the new setting until a later activation. A deployment file alone cannot specify the correct lifetime transition.

The framework’s `SNodeCReconfigureTest` exercises repeated parses, file changes, retained command-line precedence, recreated named configuration, final validators, failure and recovery, and frozen bootstrap behavior. It provides a source-level counterpart to these boundaries; it does not imply that every application implements a live administration interface.

##### Configuration-file view

In a configuration file, the same hierarchy becomes a dotted key:

```ini
echo.local.port = 8080
uplink.remote.host = "localhost"
uplink.remote.port = 8080
```

Here `echo` names a server and `uplink` a separate client. Each dotted key must name a role and section that this executable actually creates.

The syntax is different from the command line. The model is the same.

The file is therefore the persistent expression of the same hierarchy that the command line traverses and the C++ API configures directly, not a separate configuration universe.

#### Observe precedence with the echo server

Use the Chapter 3 executable for a controlled experiment. Its instance is named `echoserver`, rather than the schematic `echo` used above, and its C++ listen call supplies port 8080. These inspection commands do not start a listening service:

```sh
cd ~/projects/snodec-playground-build
export SNODEC_CONFIG_EXERCISE=$(mktemp -d)
printf 'echoserver.local.port = 18091\n' > "$SNODEC_CONFIG_EXERCISE/echo.conf"

./echoserver --show-config
./echoserver --config-file "$SNODEC_CONFIG_EXERCISE/echo.conf" --show-config
./echoserver --config-file "$SNODEC_CONFIG_EXERCISE/echo.conf" --show-config \
  echoserver local --port=18092
```

Find the assignments for `echoserver.local.port` in each output. Commented assignments beginning with `#` show defaults; an uncommented assignment supplies the selected override. The effective values are 8080, 18091, and 18092. In this source version the display action exits with status 2 after printing; that inspection exit is not a failed bind. The last invocation leaves the file at 18091: overriding a value for a run does not save it. `--write-config` is a separate action with a filesystem effect.

Now inspect `./echoserver echoserver local --help`. The option belongs to the local endpoint even though three input paths can supply its value. If an unexpected value appears, inspect the selected configuration file and the full command line before changing the protocol context. That context does not choose the listening port.

The experiment observes startup parsing. To study a runtime reparse, use an application that deliberately calls `reconfigure()` while running, and separately observe the parsed value and the existing listener. The two need not change together.

#### Required values and progressive disclosure

\index{required values}
\index{progressive disclosure}
\index{parameterless activation}


Parameterless `listen()` and `connect()` rely on configuration that is already present. If required configuration is missing, the error path can reveal the missing part of the hierarchy.

For a server, a missing port belongs to the `local` section of a specific configured instance.

For a client, missing peer information belongs to the `remote` section of that configured instance.

This is scoped error reporting.

It reinforces the structure of the configuration model. The error belongs to a scope that the user can inspect, instead of appearing as a generic failure.

##### Parameterless activation

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

##### Progressive disclosure as a teaching tool

Progressive disclosure is useful for operators, but it is also useful for readers.

It teaches the model in the order in which the model is structured. The same application/\allowbreak{}instance/\allowbreak{}section/\allowbreak{}option structure is therefore both an operator model and a reading model.

This is especially valuable in multi-instance programs. Instead of forcing every option into one flat help page, the hierarchy lets the user ask increasingly specific questions.

#### Persistent and nonpersistent values

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

#### Generated and shown configuration

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

#### Structured discovery and snodec-control

\index{snodec-control@\texttt{snodec-control}}
\index{configuration!comment metadata}

`--show-config` can include structured comment metadata under the `#@` prefix. The schema describes a document, tree nodes, option groups, and individual options. Node paths represent the actual hierarchy, including anonymous or nested subcommands; they are not limited to one fixed application/instance/section depth.

The underlying file is still INI-compatible text. JSON-shaped metadata appears only inside comments, and changing an active option still means changing its ordinary configuration assignment. Metadata is omitted when description/comment output is disabled.

The values also require careful reading. Current effective values, configured values, and C++ defaults are different observations. The metadata does not claim a complete historical registration-default record or a complete decomposition of every validator. A tool must respect those limits instead of interpreting every missing constraint as permission.

The `snodec-control` tool lives under `src/tools/snodec-control`. It discovers a target's configuration, can inspect or edit the discovered model, and can delegate saving and execution back to the target:

```sh
snodec-control --target ./minigateway --print-summary
snodec-control --target ./minigateway --list-options
snodec-control --target ./minigateway \
  --set mqtt-uplink.remote.host=127.0.0.1 \
  --set mqtt-uplink.remote.port=1883 \
  --check-required --print-run-command
```

The last command is a preview, not a connection attempt. Use the discovered option names for the actual application. A bare name is convenient only when it is unambiguous; full keys preserve the named role and section.

`--materialize` writes a tool-produced editable configuration. `--save-config` asks the target to write its canonical configuration. `--check-required` is a local preflight check, not a replacement for the target's final validation. `--run` starts the target with the selected configuration; it does not turn the tool into an in-process runtime control API.

An optional Curses interface is available with `--ui` when built with that support. The noninteractive operations remain useful without it. The tool's own build/test choices are separate from the framework test switch; its README documents `SNODEC_CONTROL_BUILD_TUI` and `SNODEC_CONTROL_BUILD_TESTS`.

#### Logging policy and resource policy in the same tree

The root configuration now exposes semantic logging format and overrides by origin, boundary, component, and instance. A named communication instance also carries its connection resource policy, and HTTP/WebSocket instances add their protocol-specific limits.

These options extend the existing tree rather than creating a second setter system:

```text
application
  -> logging policy
  -> named instance
      -> connection queue policy
      -> http/parser policy
      -> websocket receiver policy
```

Logging policy is established and frozen at bootstrap. A runtime reparse can change values visible in the configuration tree without replacing that effective policy. Runtime connections consume policy snapshots established from the configured tree. They do not reread a mutable deployment file for each received byte. Chapters 13, 15, 16 and 19 explain the meaning of the respective options; this chapter establishes where they belong and how they remain inspectable.

#### Configuration files as operational artifacts

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

#### Designing configuration for real applications

\index{configuration design}
\index{deployment shape}


The detailed model also suggests design habits.

##### Name externally operated roles

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

##### Keep endpoint options in endpoint sections

Endpoint values should live in `local` or `remote`, not in random application flags.

That makes address-family differences manageable. IPv4, IPv6, Unix-domain sockets, RFCOMM, and L2CAP all have different concrete endpoint fields, but the local/remote distinction remains stable.

This is the same design lesson as Chapters 6–8, now expressed through configuration.

##### Keep protocol behavior out of configuration

Configuration can select endpoints, timeouts, retry behavior, TLS settings, and activation shape. It should not become the protocol implementation.

The protocol still belongs in `SocketContext`.

The construction boundary still belongs in `SocketContextFactory`.

Configuration should expose variation; it should not replace application design.

##### Avoid hiding deployment shape in source-only defaults

C++ defaults are useful. They make examples small. They provide reasonable baselines. They help tests and embedded use cases.

But deployment-facing choices often deserve external visibility. Ports, paths, certificate files, log files, daemonization, and enablement are easier to operate when they are visible through the configuration hierarchy.

A good application can use both: source-level defaults for clarity and external configuration for deployment.

One final distinction prevents a subtle configuration mistake. A named endpoint is the address in the configuration tree; a returned `FlowHandle` is control over one activation. Starting the endpoint twice does not create two separately configurable instance names. Likewise, `terminateFlow()` ends that activation's pending work and recovery decisions, while `setOnDestroy(...)` observes the eventual release and unregistration of the shared configuration instance. Configuration identity, flow termination, and connection closure are three different observations.

#### What remains stable

Across all these details, the application/instance/section/option hierarchy remains the stable spine of configuration.

The application gives the operational envelope. The instance gives the configured communication role an address. The section gives one responsibility scope.

The option gives one value. The same structure appears in C++ API calls, command-line traversal, and configuration-file keys. Therefore, the configuration model scales from a small echo example to applications with several communication roles.

::: {.snodec-remember title="What to remember"}
- The handle configures a server-side or client-side communication role; the registered instance carries that configured role into the runtime.
- The C++ API, configuration files, and command line feed one hierarchical configuration model.
- Named instances become addressable in that hierarchy; anonymous instances remain internal to application code.
- Sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls` scope options by responsibility.
- A runtime reparse changes configuration; it does not reactivate an endpoint or guarantee an atomic rollback after failure.
:::
