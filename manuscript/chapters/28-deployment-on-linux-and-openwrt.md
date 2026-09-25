## Deployment on Linux and OpenWrt {#deployment-on-linux-and-openwrt}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Distinguish a linked application from a complete installed runtime environment.
- **O2.** Observe installed echo behavior, process restart and configuration-error recovery.
- **O3.** Choose service ownership, resources and target-specific deployment checks.
:::

\index{deployment}
\index{Linux deployment}
\index{OpenWrt}

### Deployment as installed architecture

Deployment is where build decisions meet the operating system. Linking produces a binary; running a service requires its libraries, modules, configuration, supervision, writable state and application resources to exist with the correct ownership.

\index{installed architecture}
\index{filesystem layout}
A small experimental program may run from the build tree with a manually adjusted environment. A serious deployment needs a reproducible filesystem shape. Figure \ref{fig:build-install-package-deployment-surface} shows the path from a build component to an installed runtime surface.

::: {.snodec-warning title="Install-tree warning"}
Do not confuse build-tree success with install-tree success. A running role also needs its installed libraries, modules, configuration, service shape, and writable runtime state.
:::

![The build-to-deployment path in which component choices become installed packages, service definition, configuration, and runtime state.](assets/figures/pdf/fig-11-build-install-package-deployment-surface.pdf){#fig:build-install-package-deployment-surface width=90% latex-placement="tbp"}

The figure goes beyond compilation: a component acquires an install location and package dependency metadata, then joins a service definition, configuration and writable state.

General-purpose Linux workstations, servers, virtual machines and Debian-like SBCs provide the first rehearsal: build, install, package, configure and supervise. Even here the executable may need protocol extensions, TLS material, database access or web assets.

Chapter 27's component boundaries remain useful after installation. An IPv4 stream tool need not carry HTTP, MQTT or MariaDB; a web administrator may need Express but no MQTT; a bridge selects client and stream support, while a store adds persistence.

Runtime packages supply libraries, modules, configuration and service files. Development packages also supply public headers and exported targets. Check the complete role: external libraries, readable configuration, writable log/pid directories, TLS keys and trust, database connectivity and web assets can all be required beyond the executable.

### Packages and installed component surfaces

\index{deployment!packages}
\index{CPack@\texttt{CPack}}
\index{package dependencies}
\index{runtime-loaded modules}

The top-level build includes packaging after `src`. Its CPack configuration enables Debian packages, shared-library dependency and metadata generation, component dependencies and installation, and one package per component group.

CPack turns install rules into packages. It does not decide supervision, certificate material, database schema, site configuration, OpenWrt feed layout, repository signing or update policy.

Package dependencies should follow component dependencies, and development packages should install the public headers that correspond to the components they expose. That is exactly what the SNode.C packaging configuration expresses.

Examples include:

| Package or component group | Declared dependency |
|---|---|
| `utils` | `logger` |
| `core` | `mux-${IO_Multiplexer}`, `utils` |
| WebSocket server/client packages | shared WebSocket layer and the corresponding HTTP side |
| `net-in-stream-tls` | `net-in-stream`, `core-socket-stream-tls` |

The metadata carries the component graph to the package manager. `mux-epoll`, `mux-poll` and `mux-select` are separate packages; `core` requires its selected default and `utils`. Additional multiplexers can be installed deliberately for process-local overrides such as `LD_PRELOAD`, without changing the application's event model.

\index{multiplexer packages}
\index{runtime overrides}

Ordinary dependencies must be found by the platform loader. HTTP upgrade and WebSocket subprotocol modules add runtime selection: the application can start successfully while a later upgrade fails because its module is missing or misplaced. Install these libraries where SNode.C expects them or where configuration selects them.

### RPATH as deployment policy

\index{RPATH@\texttt{RPATH}}
\index{deployment policy}

Build-tree lookup paths are not installed lookup paths. System linker configuration may locate ordinary libraries, while nested protocol-extension layouts can require install RPATH and explicit directories.

A deployment should answer:

- will the platform loader find ordinary shared libraries?
- will SNode.C find runtime-loaded upgrade or subprotocol modules?
- does the installed path match what the build encoded?
- does cross-compilation staging avoid leaking build-host paths into target binaries?

RPATH can preserve intended lookup paths for installed components, but deployment still has to ensure that the files, permissions, and package dependencies are actually present on the target. The last question becomes especially important for OpenWrt and other cross-compiled environments.

For the private Linux installation below, also inspect transitive library lookup. An executable’s `DT_RUNPATH` applies only to its direct dependencies. The companion lifecycle lab uses `-DCMAKE_EXE_LINKER_FLAGS=-Wl,--disable-new-dtags` to select inherited `DT_RPATH` for its private prefix. The shared companion build selects that same inherited lookup policy for all Linux exercise targets. A maintained package instead needs a coherent loader policy for the complete installed dependency graph.

### Runtime state and service operation

\index{runtime state}
\index{service operation}
\index{daemonization}
\index{service managers}
\index{pid files}

SNode.C's configuration model creates real deployment expectations. When run with effective root privileges, the current configuration startup code uses system-level directories:

```text
/etc/snode.c
/var/log/snode.c
/var/run/snode.c
```

In non-root mode, the current code chooses a user base from `XDG_CONFIG_HOME`, `HOME`, or the passwd home directory and constructs SNode.C-specific configuration, log, and pid paths below that base:

```text
<user-base>/.config/snode.c
<user-base>/.local/log/snode.c
<user-base>/.local/run/snode.c
```

These locations distinguish ordinary-user development from root-mode operation; service identity determines which paths must be prepared.

When root-mode directory creation is needed, SNode.C expects a management group. The default group name is compiled from `GROUP_NAME`, whose current build default is `snodec`. During root-mode directory creation, the code looks up that group and uses it for group ownership. If the group is missing, directory setup is treated as a configuration/runtime setup error.

Prepare that group, directory ownership and permissions, and service-user membership where appropriate. Avoid world-writable runtime directories. A failure to read configuration or create a log/pid file is a deployment failure before it is a protocol problem.

The configuration shell exposes `--daemonize`, `--user-name`, `--group-name`, `--kill`, `--log-file` and `--enforce-log-file`. These let applications manage background execution, identity and files; they do not replace host supervision.

A Linux service manager can own restart, logging, dependencies and process lifetime. OpenWrt normally uses `procd`. Run in the foreground beneath a foreground-process supervisor rather than daemonizing out of its control.

During development and debugging, foreground execution is usually the clearest mode. It keeps process output, configuration experiments, and failure behavior visible before the role is hidden behind a service manager.

A typical development rhythm is to run in the foreground, inspect help and effective configuration, enable a narrow semantic logging override if needed, write a configuration file, and move the role into a managed service.

Generated configuration records the deployed role map: enabled instances, endpoints, TLS, retries/timeouts, application logging/daemon options and state directories. Keep it as a reproducible deployment artifact.

Logs and pid files are mutable runtime state. Decide where they live, who can read and write them, how logs rotate and whether the supervisor needs the pid file or it is only an application convenience.

### A worked Linux service: the installed echo server

Use the Chapter 3 echo server for a small service rehearsal. It needs no broker, database, web assets, or protocol module, so the exercise isolates installation, configuration, supervision, and shutdown. The example uses a systemd user manager and a private loopback port. The user manager must be available in the login session; this does not configure a system-wide service or boot-time user lingering.

Assume `SNODEC_BOOK_SOURCE` names the book checkout and that the selected framework has been installed at `$HOME/.local/snodec`, with libraries in `lib`. If your installation uses another library directory, substitute that actual directory in the RPATH below. Build and install the book's consumer into its own prefix:

```sh
cmake -S "$SNODEC_BOOK_SOURCE/companion/examples/EchoPair" \
  -B "$HOME/projects/snodec-service-echo-build" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="$HOME/.local/snodec" \
  -DCMAKE_INSTALL_PREFIX="$HOME/.local/snodec-book" \
  -DCMAKE_INSTALL_RPATH="$HOME/.local/snodec/lib"
cmake --build "$HOME/projects/snodec-service-echo-build" --parallel 4
cmake --install "$HOME/projects/snodec-service-echo-build"
mkdir -p "$HOME/.config/snodec-book" "$HOME/.config/systemd/user"
```

Save this as `$HOME/.config/snodec-book/echo.conf`:

```ini
daemonize=false
log-level=4
log-format=json
echoserver.local.host=127.0.0.1
echoserver.local.port=18093
```

First run the installed executable in the foreground:

```sh
"$HOME/.local/snodec-book/bin/echoserver" \
  --config-file "$HOME/.config/snodec-book/echo.conf"
```

From another terminal, use an independent peer. It sends one payload and accumulates the reflected bytes without assuming one receive call returns the whole payload:

```sh
python3 - <<'PY'
import socket
payload = b"service rehearsal\n"
with socket.create_connection(("127.0.0.1", 18093), timeout=2) as peer:
    peer.sendall(payload)
    received = bytearray()
    while len(received) < len(payload):
        chunk = peer.recv(len(payload) - len(received))
        if not chunk:
            raise RuntimeError("connection ended before the echo was complete")
        received.extend(chunk)
    assert received == payload
print("installed echo exchange passed")
PY
```

Stop the foreground server with Ctrl-C before starting the managed instance. Save the following user unit as `$HOME/.config/systemd/user/snodec-book-echo.service`:

```ini
[Unit]
Description=SNode.C book echo rehearsal

[Service]
Type=exec
ExecStart=%h/.local/snodec-book/bin/echoserver --config-file=%h/.config/snodec-book/echo.conf
WorkingDirectory=%h
UnsetEnvironment=XDG_CONFIG_HOME
Restart=on-failure
RestartSec=2s
TimeoutStopSec=10s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

`Type=exec` supervises the foreground process; the application must not daemonize underneath it. `%h` resolves to the user’s home directory. Clearing `XDG_CONFIG_HOME` here makes the framework’s current non-root base-directory calculation use `HOME`, as described earlier. The explicit configuration-file path remains unchanged. The unit uses the journal rather than requiring a separate application log file. Consult the installed `systemd.service(5)` and `systemd.exec(5)` manuals for the host’s supported settings; the upstream [service-unit documentation](https://github.com/systemd/systemd/blob/main/man/systemd.service.xml) describes the process and restart model.

Validate, start, and inspect it:

```sh
systemd-analyze --user verify "$HOME/.config/systemd/user/snodec-book-echo.service"
systemctl --user daemon-reload
systemctl --user start snodec-book-echo.service
systemctl --user status snodec-book-echo.service --no-pager
journalctl --user -u snodec-book-echo.service -n 30 --no-pager
```

Repeat the Python peer check. Then use `systemctl --user restart snodec-book-echo.service` and repeat it again. Finally stop it with `systemctl --user stop snodec-book-echo.service`; a new peer connection should fail. Inspect the journal for normal shutdown and confirm that the service is inactive. A process reported as active and a completed echo are separate observations.

For a controlled failure case, stop this rehearsal service and temporarily put a nonnumeric value in its port assignment. Starting it should expose a configuration error; `Restart=on-failure` may make repeated attempts subject to the manager’s start limits. Stop it, restore the valid port, run `systemctl --user reset-failed snodec-book-echo.service`, and repeat the successful check. This tests operational recovery from a configuration mistake without changing the protocol implementation.

Remove the rehearsal unit and its dedicated configuration when finished, then run `systemctl --user daemon-reload`. A production system service would additionally select a service account and managed writable directories. The user-unit exercise establishes the supervision sequence without claiming that those production choices have been made.

### Deployment-specific resources

\index{TLS certificates}
\index{database dependencies}
\index{web assets}

TLS needs certificate chains, private keys, CA files/directories, renewal policy, ownership, permissions and any SNI configuration. Linking a TLS component supplies none of that deployment policy.

Chapter 24's persistence boundary requires a client-library package plus a database endpoint, credentials, schema, permissions and an unavailable-database policy. Record both the package dependency and the persistent-state contract; MQTTStore and history services depend on both.

Applications can also install web assets, as the MQTTSuite broker does below its web directory. Executables, libraries, assets, configuration, service definitions and runtime directories have different update and ownership rules; one anonymous copy step hides those distinctions.

### Embedded Linux and OpenWrt

\index{embedded Linux}
\index{OpenWrt!deployment}
\index{OpenWrt SDK}

Embedded targets make storage, memory, library count, startup time, log volume, writable flash and optional dependencies more expensive. Package only the protocol families, modules and applications the target uses.

OpenWrt adds embedded, cross-compiled and package-managed constraints to Linux. Typical systems use BusyBox, musl, `procd` and overlay filesystems. The matching SDK supplies the target CPU, C library, ABI, compiler/linker and library environment; a desktop binary is not a substitute.

The flow is SDK, package recipe, cross-compiled package, feed/image, package-manager installation, service and runtime configuration. Commands and package formats depend on the selected release. Let that release's build system produce its package format instead of treating an extension as a stable interface.

Recipes should preserve useful component boundaries: core and multiplexer, network families, TLS, HTTP/Express, WebSocket, MQTT, MariaDB and selected applications may be split separately. This is packaging policy, not a claim that the repository ships that feed layout. Declare TLS, JSON, database and Bluetooth dependencies explicitly; where JSON is built into a component, ensure the SDK supplies it reproducibly.

A feed identifies available packages/versions, dependencies and target architectures for installation or image builds. Repository metadata, signing and update trust belong to distribution; a correctly compiled package alone cannot establish them.

A `procd` service declares the command, configuration, user/group, restart policy and prerequisites. Keep the application in its intended supervision model even if it also supports self-daemonization.

\index{OpenWrt!deployment flow}
\index{feeds}
\index{package recipes}
\index{procd@\texttt{procd}}
\index{OpenWrt!service integration}

### A worked OpenWrt path: verify the package before the device

The first practical step is to inspect the recipe at the [SNode.C OpenWrt feed’s main HEAD](https://github.com/SNodeC/OpenWRT/tree/main), before cross-compiling. In `net/snode.c/Makefile`, check `PKG_VERSION`, compare `PKG_SOURCE_VERSION` with the framework’s `master` HEAD, inspect the logger download and its hash, and compare the module list with current CMake targets. A package version alone does not establish that the selected source matches the book’s manifest.

The recipe already describes the 2.0 package layout, supplies a checked spdlog download and lists the valid `net-un-phy` component. Source selection still needs attention: the recipe selects a tag rather than `master`. Verify these properties again at HEAD before using an SDK; the steps below rehearse a build and deployment, not a claim that a particular device has passed them.

On a disposable target or test image, record the release, target and available space before choosing its matching SDK:

```sh
cat /etc/openwrt_release
uname -m
df -h /overlay
```

Select the SDK for that release and target, including its C library and toolchain. In the extracted SDK, inspect `feeds.conf.default`, update the configured feeds, and install their recipe links:

```sh
./scripts/feeds update -a
./scripts/feeds install -a
```

Add the SNode.C recipe through a local feed under your control. Review the following points before selecting it in `make menuconfig`:

| Recipe surface | Required evidence for the current source |
|---|---|
| Source selection | The feed currently selects a framework tag rather than `master`; compare its prepared contents with the Chapter 2 manifest and use reviewed master contents for this rehearsal |
| Version and library names | The recipe declares 2.0 and derives the SONAME major; verify the staged filenames from the SDK build |
| Component graph | Met by the inspected recipe: the module graph includes the valid `net-un-phy` target; recheck selected modules against current CMake targets |
| Logger dependency | Met by the inspected recipe: a hashed spdlog download supplies FetchContent with networking disabled; verify the download in the SDK build |
| Optional features | The recipe exposes feature selections; choose TLS, Bluetooth, database support and applications deliberately, then verify the staged result |
| Consumer application | The book echo consumer is cross-compiled against the staged target installation and installed as `/usr/bin/echoserver` |
| Runtime ownership | The configured management group and configuration directories exist on the target |

Use the framework source prepared in Chapter 2 for the SDK package. Compare the prepared files with that input before accepting the build. Do not point the consumer’s `snodec_DIR` at the desktop installation: that would mix host and target artifacts.

After the reviewed recipe and echo package are selected, expand the SDK configuration and build the framework recipe with verbose output:

```sh
make defconfig
make package/snode.c/compile V=s
```

The second command assumes the recipe retains the `snode.c` directory name used by the inspected feed. Build the echo application through its own registered recipe target. Record the SDK archive identity, feed revision, recipe changes, `.config`, prepared source revision and build log together. Before copying packages to the test device, inspect their file lists and dependency metadata with the selected release's package tools. Check the target executable's architecture and its required shared-library names with the SDK's inspection tools. Those observations should identify target artifacts, not host binaries or build-directory paths.

Install the resulting framework components and echo package using that release's package manager, then run `/usr/bin/echoserver --help` on the device. A loader failure belongs to packaging; do not work around it by copying arbitrary desktop libraries. For the first rehearsal, keep the listener on device loopback. Save `/etc/snode.c/book-echo.conf` with the same five settings used in the Linux exercise above, including port `18093` and `daemonize=false`.

A minimal foreground-service definition in `/etc/init.d/book-echo` is:

```sh
#!/bin/sh /etc/rc.common
START=95
STOP=10
USE_PROCD=1

start_service() {
    procd_open_instance
    procd_set_param command /usr/bin/echoserver --config-file /etc/snode.c/book-echo.conf
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_set_param respawn 3600 5 5
    procd_close_instance
}
```

This is a rehearsal service using the device's existing account and group setup, not a complete privilege-isolation policy. Package the script and configuration through install rules when turning the rehearsal into a maintained package. The command keeps the application in the foreground so `procd` owns process supervision. The respawn parameters bound repeated short-lived failures; inspect the selected release's `procd` behavior when choosing production values.

On the test device, make the script executable and exercise its lifecycle:

```sh
chmod 0755 /etc/init.d/book-echo
/etc/init.d/book-echo start
logread -e book-echo
/etc/init.d/book-echo restart
/etc/init.d/book-echo stop
```

Between start, restart and stop, test the listener from the development host through an SSH loopback tunnel, for example `ssh -N -L 18094:127.0.0.1:18093 root@TEST_DEVICE`, substituting the test device's actual address. Run the Linux exercise's independent Python peer against local port `18094`. Expect the exact echo after start and restart, then a failed exchange after stop. This avoids making a teaching listener reachable from the router's external interfaces. The SSH client and server must permit forwarding; if they do not, use an available target-side peer and record that substitution.

Finally, repeat the invalid-port experiment from the Linux exercise, inspect the service failure, restore the configuration, and verify a fresh successful exchange. Enable boot startup only after these checks on the disposable target, then test one reboot. Installation, successful start, restart, controlled failure, recovery and boot behavior are separate observations. Run this rehearsal only when the matching SDK, ported recipe, and target are available.

### Rebuild and inspect the installed system

\index{deployment!ABI compatibility}
\index{snodec-control@\texttt{snodec-control}}

A deployment of SNode.C 2.0 must use a coherent set of rebuilt C++ artifacts. Applications and runtime-loaded extensions compiled against 1.x must not be mixed with the new shared libraries. The source-level continuity of a public type name or include path is not an ABI guarantee. Rebuild the application, its protocol modules, and the libraries that derive from affected public classes as one installation set.

Inspect that installed set in the environment in which it will run. The staged installed-consumer and external echo checks from Chapter 29 provide useful package evidence, but they do not exercise a particular service account, router image, certificate directory, or database installation. Those remain deployment checks.

`snodec-control` adds an operational view of a target application's configuration. It discovers the target's configuration output, can show or edit the resulting model, and can ask the target to write its canonical configuration. Its optional Curses interface changes the presentation, not the ownership of configuration. The target application still performs final validation.

This is also why configuration metadata and semantic logs serve different purposes. Metadata describes configurable structure and values; a log record describes an occurrence at runtime. Keep both with a reproducible service setup, but do not treat a configuration preview as proof that a listener started or that a request completed.

### Reading a deployment

\index{deployment reading workflow}

::: {.snodec-checklist title="Practical deployment checklist"}
A SNode.C deployment can be read with a checklist. It is not a command sequence; it is a way to keep deployment architectural.

1. Which executable or service role is being deployed?
2. Which SNode.C components does it require?
3. Which package components provide those libraries?
4. Which runtime-loaded modules must be installed?
5. Which external libraries are required?
6. Which configuration file describes the role?
7. Which paths are read-only, and which must be writable at runtime?
8. Which user and group run the process?
9. Which directories hold configuration, logs, and pid files?
10. Which TLS or database resources are required?
11. Which service manager owns lifecycle and restart policy?
12. Which package manager installs or updates the service?
13. Which repository or feed provides the packages?
14. Which trust model protects package updates?
:::

A deployment rehearsal should preserve the application's actual operating conditions. Run the installed executable under the intended service account, with its real configuration path and working directory, before putting a supervisor around it. Verify that named instance sections resolve as intended, the Unix-domain directory is writable where required, TLS material is readable where required, and the installed protocol modules can be found. Then stop the process normally and observe its cleanup before testing restart. A build-tree run under the developer's account leaves all of those deployment boundaries untested.

For MiniGateway, keep liveness and readiness distinct. `/health` demonstrates a responsive HTTP role. It does not query broker acceptance, database durability, or the freshness of measurements. A supervisor can use a liveness observation without pretending it establishes those wider application guarantees.

The next chapter turns those deployment observations into tests that distinguish package failures, wrong endpoints and application behavior.

::: {.snodec-remember title="What to remember"}
- Installed libraries, runtime-selected modules, configuration and writable state must all fit the deployed role.
- Package dependencies carry component choices; they do not supply service or update policy.
- Foreground execution makes configuration and shutdown observable before supervision.
- Service restart, completed protocol work and application readiness are separate observations.
- OpenWrt requires the matching SDK, explicit recipe dependencies and target-runtime checks.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1, O3).** An installed executable starts but its WebSocket upgrade fails. Which library, module-path, package and permission observations would separate the possible causes?
2. **Review (O2, O3).** Why should a foreground-process supervisor own restart? Distinguish active status, successful echo, liveness and application readiness.
3. **Lab (O1, O2).** Run the private-installation lifecycle lab. Build and install EchoPair, exchange exact bytes, restart it with a new process identity, repeat the exchange and observe refusal after shutdown.
4. **Lab (O2, O3).** Run the invalid-configuration lab. A nonnumeric port must stop startup; restore the port and observe a successful installed exchange. Explain which service-manager checks the local process lab leaves open.
5. **Design (O1, O3).** Plan the OpenWrt rehearsal for a chosen disposable target. Identify SDK/recipe prerequisites, library and asset packages, writable state, supervision, update trust and the observations required before enabling boot startup.

Public solutions and bounded lab commands: `companion/exercises/ch28/README.md`.
:::
