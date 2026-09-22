## Deployment on Linux and OpenWrt

\index{deployment}
\index{Linux deployment}
\index{OpenWrt}


### Why deployment belongs after CMake

Deployment is where build decisions meet the operating system.

The subject is deployment, but the real topic is still architectural visibility. Deployment is where SNode.C's build choices enter the filesystem. Shared libraries, component packages, executable applications, exported CMake package files, runtime-loaded protocol modules, configuration directories, log directories, pid directories, service definitions, and package-manager metadata are not unrelated operational leftovers. They are the installed form of the architecture.

The distinction is simple:

```text
linking:
  the binary can be produced

deployment:
  the complete runtime environment exists
```

That distinction matters for SNode.C because the framework is used to build long-running communication roles: HTTP applications, MQTT tools, WebSocket upgrade handlers, database-connected services, IoT-facing components, and full systems such as MQTTSuite. Once those applications leave the build tree, the important questions are no longer only compiler and linker questions:

```text
Where are the libraries installed?
Where are runtime-loaded modules installed?
Which packages are required?
Which user or group owns runtime state?
Where do configuration, logs, and pid files live?
How is the service supervised?
Which TLS, database, or web-asset resources belong to the deployment?
What changes on embedded Linux or OpenWrt?
```

These questions are not afterthoughts. They decide whether the built architecture can actually run.

### Deployment as installed architecture

\index{installed architecture}
\index{filesystem layout}


#### Architecture entering the filesystem

Deployment is architecture entering the filesystem. When SNode.C is installed, the framework's internal boundaries become visible as libraries, executables, exported package files, runtime-loaded modules, configuration directories, service definitions, package metadata, and managed runtime state.

A small experimental program may run from the build tree with a manually adjusted environment. A serious deployment needs a reproducible filesystem shape. Figure \ref{fig:build-install-package-deployment-surface} shows the path from a build component to an installed runtime surface.

::: {.snodec-warning title="Install-tree warning"}
Do not confuse build-tree success with install-tree success. A running role also needs its installed libraries, modules, configuration, service shape, and writable runtime state.
:::

![The build-to-deployment path in which component choices become installed packages, service definition, configuration, and runtime state.](assets/figures/pdf/fig-11-build-install-package-deployment-surface.pdf){#fig:build-install-package-deployment-surface width=90% latex-placement="tbp"}

Figure \ref{fig:build-install-package-deployment-surface} is intentionally not only a build pipeline. Each step preserves architectural information. A CMake target expresses a component boundary. An install component gives that boundary a filesystem location. A package component adds dependency metadata. The deployed runtime surface then has to contain everything the running role needs: libraries, executables, runtime-loaded modules, configuration, service definition, writable state, and deployment-specific resources.

The installed system should still reveal what was built. If the build selected HTTP, Express, MQTT, WebSocket, TLS, MariaDB support, or a particular network family, deployment should not hide those choices behind one opaque pile of files.

#### General-purpose Linux as the first deployment target

The first deployment target is general-purpose Linux: development workstations, servers, virtual machines, single-board computers running Debian-like distributions, and Linux-based lab systems. This environment is easiest to understand because it is close to the development system:

CMake build, CMake install, CPack component package, package-manager installation, filesystem layout, service definition, and runtime configuration/state.

Even there, SNode.C has a richer deployment story than a single executable. The framework installs component libraries, exported package configuration, runtime-sensitive protocol-extension layouts, and applications that may need logs, pid files, TLS material, database access, web assets, and service supervision.

#### Component meaning should survive installation

Chapter 32 treated SNode.C components as architectural surfaces. Deployment should preserve that meaning. A Linux package set does not have to collapse everything into one enormous install unit.

For example, a small IPv4 stream tool does not need HTTP, WebSocket, MQTT, and MariaDB libraries. A web administration application may need HTTP and Express but not MQTT. An MQTT bridge may need MQTT client support and selected transport components. A database-backed store may need MariaDB support while a pure broker may not.

This is where component packaging becomes practical. A deployment is easier to reason about when installed packages still reflect the same component boundaries that existed in the build.

For runtime packages, this mostly means the right libraries, configuration, service files, and runtime-loadable modules. For development packages, it also means that public headers and exported CMake targets preserve the same component boundaries for external consumers.

#### Deployment as runtime shape

Copying one executable is rarely the whole deployment. A SNode.C application may need:

- shared libraries,
- runtime-loaded upgrade or subprotocol modules,
- external library dependencies,
- configuration files,
- a writable log directory,
- a writable pid directory,
- TLS certificates and private keys,
- database connectivity,
- application-specific files such as web assets,
- and a service definition.

The binary is only one part of the deployed system. Deployment proves that all the other pieces are present, placed correctly, owned correctly, and visible to the runtime.

### Packages and installed component surfaces

\index{deployment!packages}
\index{CPack@\texttt{CPack}}
\index{package dependencies}
\index{runtime-loaded modules}


#### CPack as the ordinary Linux packaging bridge

SNode.C's top-level build enters `src` and then includes the project packaging configuration. Packaging is therefore part of the project build story, not an unrelated external script.

The packaging configuration enables Debian package generation, shared-library dependency generation, shared-library metadata generation, component dependency handling, component installation, and one package per component group. That matters because it lets the component model survive into deployable packages.

A useful deployment path is: SNode.C component target, install component, CPack component package, package dependency metadata, and target installation.

The component model is therefore not only useful while compiling from source. It can become visible to the target system's package manager.

#### What CPack solves, and what it does not solve

CPack can package installed components and express package dependencies. It can help generate binary packages from install rules and component metadata.

It does not create a complete deployment policy. It does not decide service supervision, certificate material, database schema, site-specific configuration, OpenWrt feed layout, repository signing policy, or operational update policy.

CPack provides the packaging bridge. It does not replace system design.

#### Package dependencies follow component dependencies

Package dependencies should follow component dependencies, and development packages should install the public headers that correspond to the components they expose. That is exactly what the SNode.C packaging configuration expresses.

Examples include:

| Package or component group | Declared dependency |
|---|---|
| `utils` | `logger` |
| `core` | `mux-${IO_Multiplexer}`, `utils` |
| WebSocket server/client packages | shared WebSocket layer and the corresponding HTTP side |
| `net-in-stream-tls` | `net-in-stream`, `core-socket-stream-tls` |

This mirrors the component graph from Chapter 32. A package manager should not have to rediscover the architecture from filenames. The package metadata should already carry the dependency story.

#### Multiplexer packages and runtime overrides

\index{multiplexer packages}
\index{runtime overrides}


Chapter 32 introduced the multiplexer choice. Deployment makes that choice visible.

SNode.C has package components for the multiplexer libraries:

```text
mux-epoll
mux-poll
mux-select
```

The `core` package depends on the selected default multiplexer component:

`core` with the selected `mux-${IO_Multiplexer}` component and `utils`.

That is the ordinary deployment path. A deployment may still install additional multiplexer libraries deliberately if process-local override techniques such as `LD_PRELOAD` are part of the operational or diagnostic strategy. That gives two deployment modes:

normal package dependency, where the selected default multiplexer is installed with `core`; and explicit operational override, where an additional multiplexer library is available for process-local override.

Both mechanisms remain deployment decisions. They do not change the application-facing event-driven model.

#### Installed paths and runtime-loaded modules

Some libraries are ordinary link-time dependencies. Others participate in runtime protocol composition. HTTP upgrade support, WebSocket upgrade handling, WebSocket subprotocol support, and MQTT-over-WebSocket composition make installation paths operationally important.

For ordinary linked libraries, the platform loader must find the dependency. For upgrade and subprotocol composition, SNode.C must also find the libraries that participate in runtime protocol composition. A dynamically loaded or path-sensitive module must therefore be installed where the runtime expects it, or where configuration tells the runtime to find it.

Chapter 32 identified the build-side properties that make such runtime composition visible. In deployment, those choices stop being abstract build details. They become the difference between:

application starts, the runtime protocol extension is found, and WebSocket or MQTT-over-WebSocket works.

and:

application starts, runtime protocol extension is missing, and the upgrade path fails.

A missing WebSocket upgrade or subprotocol module may look like an application failure, but it can be a deployment-path failure.

#### RPATH as deployment policy

\index{RPATH@\texttt{RPATH}}
\index{deployment policy}


RPATH is often treated as a linker detail. For SNode.C it can also be part of deployment policy.

In a build tree, library locations are usually convenient and known. In an installed system, the runtime loader must still find the libraries. For ordinary system libraries, the platform linker configuration may be enough. For nested SNode.C protocol-extension layouts, install RPATH and well-defined library directories can be part of the runtime contract.

A deployment should answer:

- will the platform loader find ordinary shared libraries?
- will SNode.C find runtime-loaded upgrade or subprotocol modules?
- does the installed path match what the build encoded?
- does cross-compilation staging avoid leaking build-host paths into target binaries?

RPATH can preserve intended lookup paths for installed components, but deployment still has to ensure that the files, permissions, and package dependencies are actually present on the target. The last question becomes especially important for OpenWrt and other cross-compiled environments.

### Runtime state and service operation

\index{runtime state}
\index{service operation}
\index{daemonization}
\index{service managers}
\index{pid files}


#### Configuration directories

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

This distinction is useful. The same application can run in development as a normal user and in deployment as a system service, without pretending that those are the same mode. The directories are part of the operational shell of the application.

#### The `snodec` group and ownership model

When root-mode directory creation is needed, SNode.C expects a management group. The default group name is compiled from `GROUP_NAME`, whose current build default is `snodec`. During root-mode directory creation, the code looks up that group and uses it for group ownership. If the group is missing, directory setup is treated as a configuration/runtime setup error.

A deployment package or installation procedure therefore has to prepare the runtime ownership model. That usually means:

- create the configured group if it does not exist,
- set directory ownership and permissions correctly,
- add service users where appropriate,
- avoid world-writable runtime directories,
- and make sure the application can create or read its configuration, log, and pid files.

This supports operational reliability and security hygiene. A service that cannot create its pid file or log file because deployment forgot directory ownership will fail in a way that looks unrelated to HTTP, MQTT, WebSocket, or database code.

#### Daemonization and service managers

SNode.C applications expose daemonization-related options through the configuration shell. The root configuration includes options such as:

```text
--daemonize
--user-name
--group-name
--kill
--log-file
--enforce-log-file
```

An application can run in foreground mode or daemon mode, write pid files, and switch user or group privileges, but those capabilities do not remove the need for a host service manager.

On general-purpose Linux, a long-running service is often better supervised by systemd or the local service manager. That service manager can own restart policy, logging integration, dependencies, user identity, and lifecycle. On OpenWrt, a continuously running packaged SNode.C application should normally be integrated with the platform service supervision model, commonly `procd`.

The deployment question is therefore not only:

```text
Can the program daemonize itself?
```

It is also:

```text
Which operating-system service model should supervise this role?
```

SNode.C gives applications an operational shell. Deployment integrates that shell with the host service model.

#### Foreground mode during development

During development and debugging, foreground execution is usually the clearest mode. It keeps process output, configuration experiments, and failure behavior visible before the role is hidden behind a service manager.

A typical development rhythm is to run in the foreground, inspect help and effective configuration, enable a narrow semantic logging override if needed, write a configuration file, and move the role into a managed service.

Deployment begins with understanding the effective configuration, not with hiding the process in the background.

#### Generated configuration as deployment artifact

SNode.C's ability to show and write configuration is especially important in deployment. A generated configuration file is a reproducible description of the deployed role shape.

It can record:

- which configured roles exist,
- which registered instances are enabled,
- which local and remote addresses are used,
- which TLS settings are active,
- which retry and timeout policies matter,
- which application-level options shape logging or daemon behavior,
- and which runtime-state directories are used.

This is particularly valuable for multi-role systems. A SNode.C configuration file can become a readable map of the deployed role constellation. That is much clearer than a shell script full of opaque command-line fragments.

#### Logs and pid files as managed state

Logs and pid files are runtime state. They are not source files, and they are not static configuration. A deployment answers:

- where are logs written?
- who can read them?
- are they rotated by the operating system?
- where is the pid file written?
- does the service user have permission to write it?
- does the init system rely on it, or is it only a SNode.C convenience?

A pid file and a log file are not architectural features, but unmanaged pid and log locations can break an otherwise correct deployment. A network framework can be technically correct and still fail operationally if runtime state is unmanaged.

#### A worked Linux service: the installed echo server

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


#### TLS certificate material

TLS deployment is not finished when an application links against TLS-capable components. A TLS deployment also installs and protects certificate material:

- certificate chains,
- private keys,
- CA files or CA directories,
- renewal policy,
- file ownership,
- file permissions,
- and SNI-related configuration where needed.

A TLS-capable binary is not yet a secure deployment. The certificate and trust material must be deployed correctly too.

#### Database dependencies and persistent state

Chapter 28 treated persistence as an application-state boundary. Deployment turns that boundary into library dependencies, credentials, schema assumptions, database reachability, and failure policy.

An application may need the MariaDB client library on the target. It may also need access to a database server, socket path or network endpoint, database name, user, password source, schema, and permissions. Database deployment is therefore both:

```text
package dependency deployment
  + persistent-state deployment
```

A good deployment makes the database contract visible:

- which package provides the client library,
- which configuration values identify the database endpoint,
- which schema is expected,
- which credentials are required,
- and what happens when the database is unavailable.

This becomes especially important for MQTTStore, IoT history, monitoring, or other persistence-facing applications.

#### Web assets and application-specific files

Some applications deploy more than binaries and shared libraries. For example, the MQTTSuite broker build installs browser assets for its web interface below a MQTTSuite web directory.

That is a concrete reminder that application deployment may include:

- executables,
- SNode.C libraries,
- web assets,
- configuration files,
- service definitions,
- and runtime directories.

Those files belong to different parts of the filesystem and have different update and ownership expectations. A deployment that treats all of them as one anonymous copy step loses useful structure.

### Embedded Linux and OpenWrt

\index{embedded Linux}
\index{OpenWrt!deployment}
\index{OpenWrt SDK}


#### Embedded Linux changes the deployment priorities

General-purpose Linux teaches the basic model. Embedded Linux does not change the architecture, but it changes the cost of every dependency.

On smaller targets, deployment becomes more sensitive to:

- storage size,
- memory use,
- library count,
- package granularity,
- startup time,
- log volume,
- writable flash use,
- cross-compilation correctness,
- and external dependency selection.

Therefore, SNode.C's componentized design matters. A constrained target does not need to carry protocol families, database support, example applications, or dynamic modules it never uses. On embedded systems, linking and packaging discipline become resource discipline.

#### OpenWrt is Linux under embedded constraints

OpenWrt is Linux, but it is not ordinary server deployment. It targets routers and embedded network devices, and it commonly appears with BusyBox, musl, `procd`, overlay filesystems, cross-compilation workflows, and package-manager-based system assembly rather than a full desktop/server distribution model.

A compact mental model is SNode.C Linux deployment under embedded, cross-compiled, package-managed constraints.

That is the heart of the OpenWrt part of the chapter.

#### The OpenWrt SDK as packaging environment

For application packages, the OpenWrt SDK is usually the right starting point. A binary copied from a desktop build tree is usually the wrong deployment artifact for OpenWrt.

The target may differ in:

- CPU architecture,
- C library,
- ABI,
- compiler version,
- linker behavior,
- available libraries,
- filesystem layout,
- package manager,
- and default security expectations.

The SDK provides a target-specific cross-compilation environment. That is the right environment for C++ applications with shared libraries, optional dependencies, and package metadata.

#### OpenWrt deployment flow

\index{OpenWrt!deployment flow}
\index{feeds}
\index{package recipes}


A compact OpenWrt deployment flow runs through the OpenWrt SDK, package recipe, cross-compiled package, feed or image build, package-manager installation, `procd` service definition, and SNode.C configuration/runtime state.

The exact commands depend on the OpenWrt release and build setup. The architectural flow remains stable.

#### Package recipes should preserve component meaning

An OpenWrt package recipe should not flatten SNode.C blindly. It should preserve the smallest useful deployable surface.

A feed may choose to split packages along component lines such as:

- core runtime libraries,
- selected multiplexer libraries,
- network-family components,
- TLS stream support,
- HTTP support,
- Express support,
- WebSocket support,
- MQTT support,
- MariaDB support,
- selected applications,
- selected MQTTSuite executables.

The exact split is a packaging policy decision, not a statement that the SNode.C repository already ships this particular OpenWrt feed layout. The principle is stable:

small target, small package surface, explicit dependencies, and reproducible image.

This is how an embedded target stays understandable.

#### OpenWrt dependencies must be explicit

OpenWrt packages declare dependencies explicitly. A package that needs TLS depends on the selected TLS library packages. An MQTT or HTTP component that needs JSON support depends on the JSON package if it is dynamically provided, or ensures it is built appropriately. A MariaDB-backed tool depends on the MariaDB client library. A Bluetooth component depends on Bluetooth stack support where applicable.

This is image reproducibility and build correctness. An OpenWrt image is assembled from many small packages. Hidden dependencies make the final image fragile and difficult to reproduce.

#### Package-manager format is release-specific

OpenWrt package-manager tooling and package formats are release-specific. The durable lesson is not a filename extension.

A package recipe should express the software correctly and let the OpenWrt build system produce the package format used by the selected release. That keeps the deployment lesson stable even when the package-manager workflow changes.

#### Feeds are distribution boundaries

An OpenWrt feed is a distribution boundary expressed through package recipes.

A feed tells downstream systems:

- which packages exist,
- which versions are available,
- which dependencies they require,
- which target architectures are supported,
- and which packages can be installed or built into an image.

A compact view is: package recipes, package dependencies, target-architecture builds, and repository metadata.

A clear feed layout makes the system easier to build, install, update, and reproduce.

#### Repository signing and update trust

Once packages are distributed through an OpenWrt package repository, signing becomes part of deployment trust. The target device must be able to trust repository metadata and package source according to the package manager used by that OpenWrt release.

This is especially important for routers and network infrastructure devices. A technically correct package is still not a complete deployment story if the repository cannot be trusted or updated cleanly.

#### `procd` service integration

\index{procd@\texttt{procd}}
\index{OpenWrt!service integration}


On OpenWrt, `procd` is the normal service supervision layer. A continuously running SNode.C application packaged for OpenWrt should therefore be described as a `procd`-managed service.

That service definition is where deployment expresses:

- how the process starts,
- which configuration file is used,
- which user or group is used,
- whether the service restarts,
- and which dependencies must be available before startup.

The application may still support daemonization, but on OpenWrt the deployed role should fit the platform service model.

#### A worked OpenWrt path: verify the package before the device

The first practical step is to identify the recipe's source, not to start cross-compiling. The separately maintained [SNode.C OpenWrt feed](https://github.com/SNodeC/OpenWRT) is useful packaging source, but its `net/snode.c/Makefile` at commit `c9378fe95f7c015752c748fc4ab012b585d294d1` still declares `PKG_VERSION:=1.0.1` and downloads the framework's `OpenWRT` branch. It does not select this book's current 2.0 source. Its module list also contains the old `net-un-phy` component. Installing that recipe unchanged would answer a different compatibility question.

This gives the walkthrough a real prerequisite: a recipe port for the selected 2.0 contents and the exact target SDK. The steps below explain the build and deployment rehearsal once that prerequisite is satisfied. They are not evidence that the old feed already builds 2.0.

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
| Source selection | The archive or checkout matches the book's framework manifest, including any author changes beyond the reconstruction base |
| Version and library names | Package version, SONAME major and installed filenames match the 2.0 build |
| Component graph | Selected module recipes follow current targets; obsolete targets are removed rather than satisfied by old libraries |
| Logger dependency | The current spdlog build dependency is supplied reproducibly by the SDK recipe; an undeclared configure-time download is not a package dependency policy |
| Optional features | TLS, Bluetooth, database support and applications are selected deliberately rather than through the feed's broad `full` or `apps` package |
| Consumer application | The book echo consumer is cross-compiled against the staged target installation and installed as `/usr/bin/echoserver` |
| Runtime ownership | The configured management group and configuration directories exist on the target |

Keep the source check literal. `git archive HEAD` captures committed files only; it is insufficient if the author tree has uncommitted changes. The book's manifest and reconstruction patch identify the reviewed contents. Compare the SDK's prepared source files against that manifest before accepting the build. Likewise, do not point the consumer's `snodec_DIR` at the desktop installation: that would mix host and target artifacts.

After the ported recipe and echo package are selected, expand the SDK configuration and build the framework recipe with verbose output:

```sh
make defconfig
make package/snode.c/compile V=s
```

The second command assumes the recipe retains the `snode.c` directory name used by the inspected feed. Build the echo application through its own registered recipe target. Record the SDK archive identity, feed revision, recipe changes, `.config`, prepared source identity and build log together. Before copying packages to the test device, inspect their file lists and dependency metadata with the selected release's package tools. Check the target executable's architecture and its required shared-library names with the SDK's inspection tools. Those observations should identify target artifacts, not host binaries or build-directory paths.

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

A deployment of SNode.C 2.0 must use a coherent set of rebuilt C++ artifacts. Applications and runtime-loaded extensions compiled against 1.x must not be mixed with the new shared libraries. The source-level continuity of a role name or include path is not an ABI guarantee. Rebuild the application, its protocol modules, and the libraries that derive from affected public classes as one installation set.

Inspect that installed set in the environment in which it will run. The staged installed-consumer and external echo checks from Chapter 34 provide useful package evidence, but they do not exercise a particular service account, router image, certificate directory, or database installation. Those remain deployment checks.

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

A shorter mental grouping is: artifact, dependencies, configuration, runtime state, service manager, package source, and trust/update model.

#### What deployment should not hide

A deployment should not hide:

- missing runtime-loaded modules,
- implicit package dependencies,
- writable directories with unclear ownership,
- certificate placement,
- private-key permissions,
- database schema assumptions,
- service supervision policy,
- package-manager format assumptions,
- repository trust assumptions,
- or platform-specific differences between general-purpose Linux and OpenWrt.

When these details are hidden, failures appear later as unrelated runtime problems. When they are explicit, deployment becomes another readable part of the system.

A deployment rehearsal should preserve the application's actual operating conditions. Run the installed executable under the intended service account, with its real configuration path and working directory, before putting a supervisor around it. Verify that named endpoint sections resolve as intended, the Unix-domain directory is writable where required, TLS material is readable where required, and the installed protocol modules can be found. Then stop the process normally and observe its cleanup before testing restart. A build-tree run under the developer's account leaves all of those deployment boundaries untested.

For MiniGateway, keep liveness and readiness distinct. `/health` demonstrates a responsive HTTP role. It does not query broker acceptance, database durability, or the freshness of measurements. A supervisor can use a liveness observation without pretending it establishes those wider application guarantees.

::: {.snodec-remember title="What to remember"}
- Deployment is architecture entering the filesystem.
- Linking proves that the binary can be built; deployment proves that the runtime environment exists.
- SNode.C's component model and public include hierarchy should survive installation and packaging.
- CPack connects install components to ordinary Linux packages, but it does not replace service, certificate, database, repository, or update policy.
- Package dependencies should follow component dependencies.
- Runtime-loaded upgrade and subprotocol modules make installation paths and RPATH part of deployment.
:::
