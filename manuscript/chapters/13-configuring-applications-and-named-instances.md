## Configuring Applications and Named Instances {#configuring-applications-and-named-instances}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace a named instance’s value through C++ defaults, file assignments and command-line overrides.
- **O2.** Diagnose a configuration error and distinguish parsed values from existing runtime activity.
- **O3.** Decide which communication roles need independent configuration and lifecycle control.
:::

### Configuration principles {#configuration-philosophy-in-snodec}

\index{configuration}
\index{configuration philosophy}
\index{instance!configuration}

Configuration is where architectural choices become adjustable by the operator. The context still implements the protocol and the factory creates contexts, but the application must choose its communication roles, endpoint values, connection variants and enablement.

Through a `SocketServer` or `SocketClient` handle, the application configures an instance. Giving the instance a name registers it in the configuration hierarchy. Each `listen(...)` or `connect(...)` call then starts an activation flow for that instance.

\index{configuration!architecture}
\index{instance!configuration}

Keep Chapter 4's runtime model beside this configuration story. The named instance supplies one shared settings tree; each explicit activation uses it. We will track `echoserver.local.port`: C++ supplies 8080, a deployment file selects 18091, and one command line selects 18092. The effective value is what startup consumes; a file assignment alone is neither a listening socket nor proof of successful activation.

### Three input paths, one configuration model

\index{configuration!C++ API}
\index{configuration!command line}
\index{configuration!file}

The C++ API supplies baseline defaults, a configuration file persists deployment choices, and the command line supplies run-specific overrides and inspection actions. All three feed the same hierarchy. The server/client handle exposes its configuration object directly.

For an IPv4 server, a minimal example may look like:

```cpp
EchoServer echoServer("echoserver");

echoServer.getConfig()->Local::setPort(8080);
```

In this case, the explicit `Local::` qualification is valid, but it is not required. The same server-side port can also be configured as:

```cpp
echoServer.getConfig()->setPort(8080);
```

`getConfig()` returns a pointer, hence `->`. This server configuration has no competing remote-port setter at this call site, so `Local::` is optional.

C++ code can provide baseline configuration. It can also express values that are genuinely programmatic: values derived from application structure, construction-time decisions, tests, or small teaching examples.

Convenience overloads such as:

```cpp
listen(8080, onStatus)
```

or:

```cpp
connect("localhost", 8080, onStatus)
```

fill the handle’s configuration before starting an activation. Source defaults remain useful for tests, small examples, and values determined by application structure.

Command-line configuration gives an already compiled application a way to be shaped at startup. That is especially important for named instances.

Constructing an endpoint handle with a name:

```cpp
EchoServer echoServer("echoserver");
```

creates a named instance in the command-line hierarchy: application, instance, section, and option.

A user can ask for help at different levels:

```sh
echoserver --help
echoserver echoserver --help
echoserver echoserver local --help
```

At each level, help reveals the next scope rather than requiring the user to guess a flat list of flags. Files persist that same structure.

Their key structure follows the same hierarchy:

```ini
instancename.sectionname.optionname = value
```

For example:

```ini
echoserver.local.port = 8080
uplink.remote.host = "localhost"
uplink.remote.port = 8080
```

Here `echoserver` is a named instance on the server side and `uplink` is a separate named instance on the client side in an application that creates both. A server does not acquire a client’s `remote` section merely because that key is written in a file. The file can configure the named instances the executable actually exposes.

\index{configuration!precedence}
\index{startup boundary}

Command-line values override configuration-file values, which override C++ defaults. Thus deployment can change a source default and a single invocation can override the deployment.

External configuration can address the named instances present in the hierarchy when parsing occurs. Startup parsing therefore sees the instances constructed before startup. An instance created later begins with the values supplied by application logic.

A deliberate runtime reparse can include named instances registered later. It changes configuration values, not existing activity; the section “Application and instance configuration” develops its lifecycle and failure consequences.

The current per-call flow model makes the configuration boundary particularly important. An endpoint exposes one shared configuration object. Each explicit activation receives its own controller, but that controller does not freeze a private copy of the endpoint settings. An address-taking `connect(...)` overload updates the endpoint's remote configuration before starting its flow. Use separate instances for destinations that need independent configuration; name them when operators need separate control; retaining two flow handles is not a substitute for that separation.

### Named instances as configuration addresses

The port key begins with `echoserver` because the entry point created that named instance. The executable name alone would not identify which listener to configure in an application with several inputs.

\index{named instances}
\index{configuration addresses}
\index{instance names}

An anonymous instance remains internal to application code; a named one becomes independently addressable through help, CLI overrides and file keys.

For example, an application may need to fetch data from a known remote resource as part of its own internal behavior. If that instance should not be configured, disabled, persisted, or inspected independently, an anonymous client is often the clearer choice.

Anonymous servers can also make sense, but the case is narrower.

They are reasonable for temporary local test servers, embedded loopback-only services, or helper servers whose endpoint is fixed by the surrounding program.

Externally operated servers usually benefit from named instances, because servers often need deployment-facing control over bind address, port, path, channel, enablement, and persistent configuration.

A name such as:

```cpp
EchoServer echoServer("echoserver");
```

gives the instance the external address `echoserver`. Choose names that remain useful in deployment files and operational procedures.

A named instance can remain in the application while being disabled for a deployment, test, or diagnostic run. Its configuration stays inspectable, but the instance is removed from the required startup path.

At activation, disablement lets the framework report an intentionally inactive instance. Setting that value later is not a command to close established peers or cancel every flow. Those actions have their own lifecycle controls; a runtime reparse does not merge them into one operation.

\index{configuration sections}
\index{section hierarchy}
\index{local section}
\index{remote section}
\index{tls section}

Sections group options by responsibility: endpoint identity, established-connection behavior, socket retry, server acceptance or TLS.

For the named server `echoserver` and the separate client `uplink`, examples include:

```text
echo local --port 8080
uplink remote --host localhost --port 8080
```

or in configuration-file form:

```ini
echoserver.local.port = 8080
uplink.remote.host = "localhost"
uplink.remote.port = 8080
```

\index{configuration!discovery}
\index{persistent options}
\index{generated configuration}

The detailed section catalogue below gives representative options and the differences between the server and client sides. Discovery, persistence and inspection all use these same scopes.

\index{listen()@\texttt{listen()}!parameterless}
\index{connect()@\texttt{connect()}!parameterless}
\index{parameterless activation}

A call such as:

```cpp
echoServer.listen(onStatus);
```

or:

```cpp
echoClient.connect(onStatus);
```

uses the endpoint values already supplied through code, a file or the command line.

For a server, being configured enough may mean that the local endpoint is known.

For a client, being configured enough may mean that the remote endpoint is known, and possibly also a local bind side.

For TLS instances, it may also mean that required TLS-related configuration is available. The exact requirements depend on the concrete server/client type.

\index{CLI11@\texttt{CLI11}}
\index{command-line parsing}

Missing required values lead back to the corresponding scope: a server’s `local` port, a client’s `remote` host, or a TLS setting. SNode.C uses CLI11 to implement parsing, grouping, help and persistent/nonpersistent option classification.

An external option is a promise to operators. Naming a role makes its endpoint and policy visible, but also makes those names part of configuration files, service definitions, and diagnostic procedures. Expose choices that deployments need to own; keep an internal helper’s construction detail in code when changing it independently would violate the application’s assumptions.

Startup-only configuration has a useful cost model: one validated process begins with one intended deployment shape. Runtime reconfiguration can avoid a full restart, but requires a policy for partial failure, existing connections, and future activation. The framework supplies the parsing operation. It cannot decide those application consequences from an option name.

The following section locates these choices in the hierarchy. The echo experiment then observes a port supplied in code, overridden by a file, and overridden for one invocation.

### Application and instance configuration {#application-and-instance-configuration-in-detail}

For our running value, 18092 belongs to the named listener’s local endpoint. A process-wide logging option belongs elsewhere in the tree. Keeping those scopes explicit lets an operator change diagnostics without confusing them with where the server listens.

\index{application configuration}
\index{instance configuration}
\index{configuration hierarchy}

\index{configuration hierarchy}
\index{application scope}
\index{instance scope}
\index{section scope}

Read the hierarchy from the outside inward: application-wide concerns, a named instance, a responsibility section, then an option. Figure \ref{fig:configuration-hierarchy} shows that hierarchy as one structural model. The named-instance level is where an instance receives an externally addressable identity and can be enabled or disabled without removing its endpoint handle from the application.

![A representative named-instance hierarchy: application, instance, section, and option. Options can also belong directly to application or instance scope; discovery can describe deeper or anonymous nodes.](assets/figures/pdf/fig-13-configuration-hierarchy.pdf){#fig:configuration-hierarchy width=90% latex-placement="tbp"}

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

These options form the operational envelope in which all instances operate.

They answer questions about the process as a program, not about a particular server port, peer address, Unix-domain path, Bluetooth channel, or TLS certificate used by one instance.

Instance scope belongs to one named instance. A server listens and accepts; a client connects. Their server/client side appears in help, and their endpoint sections reflect that difference.

It contains concerns such as:

- instance identity,
- server/client side identity,
- disabled state,
- configurability,
- and the set of sections that configure the instance.

The server/client object in application code is the handle. In the configuration model, a named instance has an externally addressable configuration identity created through that handle.

That distinction matters. The configuration system gives an instance an operational address instead of merely decorating a local C++ variable.

Section scope belongs to one aspect of one instance.

To locate an option, ask what it controls. A bind port belongs under `local`; a peer port under `remote`; an established connection’s timeout under `connection`. The detailed section descriptions below turn this placement rule into a map of the available responsibilities.

This is also a useful discovery exercise: start with a named instance’s help, choose the section that should own the value, and check its help before inventing an application-wide flag.

\index{application configuration}
\index{operational envelope}

\index{instance configuration}
\index{instance!configuration}
\index{required options}

Consider the operational name in this declaration:

```cpp
EchoServer echoServer("echoserver");
```

The string `"echoserver"` is an operational key. Renaming the C++ variable `echoServer` does not rename that key. Changing the string does: deployment files, overrides, and diagnostic procedures that address `echoserver` must then change together.

Treat such a rename as an application-interface change, even when the C++ program still compiles. The naming choice in the section “Configuration principles” becomes a compatibility decision once a script depends on it.

### Section configuration: scoped responsibilities

The next step in finding our port is `local`. It describes the server’s own listening endpoint, so putting 18092 in a client’s remote section would answer a different question. The section names preserve that distinction.

\index{section configuration}
\index{local section}
\index{remote section}
\index{connection section}
\index{socket section}
\index{server section}
\index{tls section}

| Section | Main meaning |
|---|---|
| `local` | local endpoint or bind side |
| `remote` | peer endpoint or connect side |
| `connection` | behavior of established connections |
| `socket` | socket-level behavior, retry, and reuse settings |
| `server` | listen and accept behavior |
| `tls` | TLS connection-layer configuration |

The available sections depend on the server/client side and layer combination. Use the relevant scope’s help to discover the actual options.

The `local` section describes the local endpoint of the instance.

For a server, it is usually the most important endpoint section because it describes where the server binds or listens.

For a client, it may describe an explicit local bind side if the application does not want to leave that side wildcarded.

The concrete fields depend on the network family.

| Network family | Typical local fields |
|---|---|
| IPv4 / IPv6 | host and port |
| Unix domain sockets | path |
| RFCOMM | Bluetooth address and channel |
| L2CAP | Bluetooth address and PSM |

For a client, `remote` supplies the peer endpoint: host and port, Unix-domain path, or Bluetooth address with channel/PSM.

An accepted server connection also has a remote peer address. That observation does not give the listening server a configurable `remote` section: the listener configures its local endpoint, while each accepted connection supplies the peer information.

The `connection` section describes behavior of established peer relationships.

Representative concerns include:

- read timeout,
- write timeout,
- read block size,
- write block size,
- termination timeout.

These apply after a connection exists; they do not choose where to bind or connect.

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

The section groups behavior that is closer to the socket and flow-control machinery than to the application protocol. A retry timeout, for example, is not part of an echo protocol. It belongs to the machinery that advances an activation flow.

The `server` section controls listening and acceptance:

- backlog,
- accepting behavior,
- accept-per-tick style limits where supported.

These settings shape listening and accepting, rather than an established connection.

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

Chapter 15 discusses TLS in depth. Here the important point is the section boundary.

### Three views of the same model

Follow the same local port through each notation below. The spelling changes from a C++ setter to a command path to a dotted file key, but these are three inputs to one option, not three independent settings to synchronize.

\index{configuration!C++ API}
\index{configuration!command line}
\index{configuration!file}

The C++ API uses section-qualified operations. Schematic examples are:

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

Use section qualification when the local/remote meaning needs to be explicit.

On the command line, the hierarchy becomes a path:

```sh
echoserver echoserver local --port 8080
```

This traverses the `echoserver` instance’s `local` section to set its `port`. Help follows the same path:

```sh
echoserver --help
echoserver echoserver --help
echoserver echoserver local --help
```

This mirrors the hierarchy: application help, then instance help, then section help, and finally option details.

The command line can also print command-line representations of the selected configuration. The `--command-line` option supports views such as `standard`, `required`, `active`, and `complete`.

Together with `--show-config` and `--write-config`, the command line becomes a way to inspect, reproduce, and persist the configuration of an application.

Missing required values are reported at the scope that owns them.

A schematic server-side session shows the idea. Here the executable is `echoserver` and the named instance is `echoserver`; the exact diagnostic wording depends on the target application:

```sh
$ echoserver
[RequiresError] echoserver requires echoserver

$ echoserver echoserver
[RequiresError] echoserver:echoserver requires local

$ echoserver echoserver local
[RequiresError] echoserver:echoserver:local requires --port

$ echoserver echoserver local --port
[ArgumentMismatch] --port: 1 required port:UINT in [0 - 65535] missing

$ echoserver echoserver local --port 8080
# The instance can now enter its listening path.
```

Chapter 14 explains the semantic records from the successful listening path.

A named instance on the client side follows the same idea, but the required section is usually `remote` rather than `local`. The CLI therefore teaches the structure while it reports the missing values.

Help and the command line describe the executable’s configuration surface. They do not open an interactive management channel into a running process. The current source provides a separate application decision: call `core::SNodeC::reconfigure()` from the event-loop thread while the runtime is `RUNNING`. `express::WebApp::reconfigure()` forwards the same operation.

The operation reparses the existing root hierarchy using the original arguments and the configuration file as it now exists. Original command-line values keep their precedence. Registered endpoint final validators run again, including for a replacement named configuration created after an earlier instance was destroyed and unregistered.

| Observation | Meaning |
|---|---|
| `true` | this runtime parse and validation succeeded |
| `false` before `RUNNING` or during shutdown | the lifecycle does not permit the operation |
| `false` from a file, value, or validation error | the parse failed; previously changed values are not automatically rolled back |
| changed endpoint values | future code can consume them; existing sockets are not restarted |
| changed logging or daemonization options | parsed values do not replace bootstrap side effects or frozen logging policy |

A successful reparse is therefore only one step in a live configuration change. The application still decides whether to end a flow, let a connection drain, construct a replacement role, or defer the new setting until a later activation. A deployment file alone cannot specify the correct lifetime transition. When configuration must change atomically, validating a replacement before a controlled process restart can be clearer than editing the live tree.

In a configuration file, the same hierarchy becomes a dotted key:

```ini
echoserver.local.port = 8080
uplink.remote.host = "localhost"
uplink.remote.port = 8080
```

Here `echoserver` names a server and `uplink` a separate client. Each dotted key must name a role and section that this executable actually creates.

### Observe precedence with the echo server

Use the Chapter 3 executable for a controlled experiment. Its instance is named `echoserver`, and its C++ listen call supplies the 8080 default used throughout this chapter. These inspection commands do not start a listening service:

```sh
cd ~/projects/snodec-playground-build
export SNODEC_CONFIG_EXERCISE=$(mktemp -d)
printf 'echoserver.local.port = 18091\n' > "$SNODEC_CONFIG_EXERCISE/echo.conf"

./echoserver --show-config
./echoserver --config-file "$SNODEC_CONFIG_EXERCISE/echo.conf" --show-config
./echoserver --config-file "$SNODEC_CONFIG_EXERCISE/echo.conf" --show-config \
  echoserver local --port=18092
```

Find the assignments for `echoserver.local.port` in each output. Commented assignments beginning with `#` show defaults; an uncommented assignment supplies the selected override. The effective values are 8080, 18091, and 18092. The display action exits with status 2 after printing; that inspection exit is not a failed bind. The last invocation leaves the file at 18091: overriding a value for a run does not save it. `--write-config` is a separate action with a filesystem effect.

Now inspect `./echoserver echoserverserver local --help`. The option belongs to the local endpoint even though three input paths can supply its value. If an unexpected value appears, inspect the selected configuration file and the full command line before changing the protocol context. That context does not choose the listening port.

The experiment observes startup parsing. To study a runtime reparse, use an application that deliberately calls `reconfigure()` while running, and separately observe the parsed value and the existing listener. The two need not change together.

\index{required values}
\index{progressive disclosure}
\index{parameterless activation}

The required-value walk above explains why these calls can omit addresses:

```cpp
echoServer.listen(onStatus);
```

or:

```cpp
echoClient.connect(onStatus);
```

The configured instance supplies the endpoint; the activation call starts the work. Help can be narrowed to the failing instance and section.

### Persistent and nonpersistent values

The file’s 18091 remains a deployment choice after a command selects 18092 for one run. Inspecting that effective value does not save it. Decide whether the port should survive another invocation before choosing a write action.

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

\index{shown configuration}
\index{generated configuration}

Files primarily describe durable choices. A CLI invocation can both override those choices and request an inspection action. `--show-config` reveals parsed values, generated configuration reveals their file form, and generated command lines show how to reproduce selected values.

### Structured discovery and snodec-control

Help located `echoserver.local.port`; structured discovery lets a tool locate that same option and inspect its metadata. A preview of 18092 still needs target validation and a successful listen before it demonstrates a running endpoint.

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

The root configuration now exposes semantic logging format and overrides by origin, boundary, component, and instance. A named communication instance also carries its connection resource policy, and HTTP/WebSocket instances add their protocol-specific limits.

Logging options belong at application scope; connection and protocol limits belong to their named instances.

Logging policy is established and frozen at bootstrap. A runtime reparse can change values visible in the configuration tree without replacing that effective policy. Runtime connections consume policy snapshots established from the configured tree. They do not reread a mutable deployment file for each received byte. Chapters 14, 16, 17 and 20 explain the meaning of the respective options; this chapter establishes where they belong and how they remain inspectable.

\index{configuration files}
\index{operational artifacts}

Configuration files should be readable by humans, stable enough for deployment, and close enough to the command-line hierarchy that users can move between both views without learning a second model.

The dotted-key structure helps:

```ini
echoserver.local.port = 8080
```

For multi-instance applications, this becomes especially useful:

```ini
public.local.port = 8080
admin.local.port = 9090
backend.remote.host = "127.0.0.1"
backend.remote.port = 1883
```

Each key says which instance it belongs to. That is the value of named instances. They make configuration files describe application structure, not just isolated values.

### Designing configuration for real applications

Return to the effective local port one final time: validation can reject an invalid value before listening, while a valid port can still fail to bind. Keep the parsed value, the activation result and the bytes later handled by a context separate.

\index{configuration design}
\index{deployment shape}

Endpoint values should live in `local` or `remote`, not in random application flags.

That makes address-family differences manageable. IPv4, IPv6, Unix-domain sockets, RFCOMM, and L2CAP all have different concrete endpoint fields, but the local/remote distinction remains stable.

This is the same design lesson as Chapters 7, 8 and 9, now expressed through configuration.

Configuration can select endpoints, timeouts, retry behavior, TLS settings, and activation shape. It should not become the protocol implementation.

The protocol still belongs in `SocketContext`.

The construction boundary still belongs in `SocketContextFactory`.

Configuration should expose variation; it should not replace application design.

One final distinction prevents a subtle configuration mistake. A named instance is the address in the configuration tree; a returned `FlowHandle` is control over one activation. Starting the endpoint twice does not create two separately configurable instance names. Likewise, `terminateFlow()` ends that activation's pending work and recovery decisions, while `setOnDestroy(...)` observes the eventual release and unregistration of the shared instance. Configuration identity, flow termination, and connection closure are three different observations.

::: {.snodec-remember title="What to remember"}
- The endpoint handle configures an instance whose settings are shared by its activation flows.
- The C++ API, configuration files, and command line feed one hierarchical configuration model.
- Named instances become addressable in that hierarchy; anonymous instances remain internal to application code.
- Sections such as `local`, `remote`, `connection`, `socket`, `server`, and `tls` scope options by responsibility.
- A runtime reparse changes configuration; it does not reactivate an endpoint or guarantee an atomic rollback after failure.
:::

::: {.snodec-exercise title="Exercises"}
Public answers, lab commands and expected observations are in `companion/exercises/ch13/README.md`.

1. **Review (O1).** A server accepts a remote peer. Does that give the listener a configurable `remote` section? Locate its bind port in all three input paths.
2. **Review (O2).** A runtime reparse returns `true` after changing a port and log level. Which effects remain unestablished? What additional risk does `false` introduce?
3. **Lab (O1, O2).** Build EchoPair and repeat the precedence experiment using a temporary file. Expect 8080, 18091 and the CLI override; verify that inspection leaves the file unchanged.
4. **Lab (O1, O2).** Follow application, instance and local help; supply port 70000. Expect rejection naming `--port`, and use local help to identify its owning scope before any listener starts.
5. **Design (O2, O3).** A gateway needs two independently configurable uplinks and an optional administrative listener. Choose names, disablement and a safe configuration-change policy. Explain why two flow handles alone cannot isolate destination settings.
:::
