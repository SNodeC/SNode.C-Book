## Deployment on Linux and OpenWrt

### Why deployment belongs after CMake

Chapter 32 showed how SNode.C becomes a set of component targets, package components, exported targets, and runtime-sensitive library paths.

Chapter 33 follows those build decisions into the installed system.

Deployment is where the architecture enters the filesystem:

- shared libraries,
- component packages,
- executable applications,
- exported CMake package files,
- runtime-loaded protocol modules,
- configuration directories,
- log directories,
- pid directories,
- service definitions,
- and package-manager metadata.

Linking proves that the binary can be built.

Deployment proves that the complete runtime environment exists.

That distinction matters for SNode.C because the framework is not only a collection of headers and libraries. It is used to build long-running communication roles: HTTP applications, MQTT tools, WebSocket upgrade handlers, database-connected services, IoT-facing components, and full systems such as MQTTSuite.

Once such applications leave the build tree, the questions become operational:

```text
Where are the libraries installed?
Where are runtime-loaded modules installed?
Which packages are required?
Which user or group owns runtime state?
Where do configuration, logs, and pid files live?
How is the service supervised?
What changes on embedded Linux or OpenWrt?
```

These are not afterthoughts.

They are the installed form of the architecture.

### Deployment as installed architecture

#### Deployment is architecture entering the filesystem

Deployment is architecture entering the filesystem.

When SNode.C is installed, the framework's internal boundaries become visible as files, directories, packages, and service definitions.

A small experimental program may run from the build tree with a manually adjusted environment.

A serious deployment needs more than that.

It needs a reproducible filesystem shape:

```text
build target
  -> install component
      -> package
          -> installed files
              -> service definition
                  -> runtime configuration
                      -> runtime state
```

The installed system should still reveal what was built.

If the build selected HTTP, Express, MQTT, WebSocket, TLS, MariaDB support, or a particular network family, deployment should not hide those choices behind one opaque pile of files.

#### General-purpose Linux as the first deployment target

The first deployment target is general-purpose Linux.

That includes development workstations, servers, virtual machines, SBCs running Debian-like distributions, and Linux-based lab systems.

On this kind of target, the deployment story is familiar:

```text
CMake build
  -> CMake install
      -> CPack component package
          -> package manager installation
              -> filesystem layout
                  -> service definition
                      -> runtime configuration and state
```

This environment is easiest to understand because it is close to the development system.

But SNode.C still has a richer deployment story than a single executable.

The framework installs component libraries, exported package configuration, runtime-sensitive protocol layouts, and applications that may need logs, pid files, TLS material, database access, and service supervision.

#### Component meaning should survive installation

Chapter 32 treated SNode.C components as architectural surfaces.

Deployment should preserve that meaning.

A Linux package set does not have to collapse everything into one enormous install unit.

For example:

- a small IPv4 stream tool does not need HTTP, WebSocket, MQTT, and MariaDB libraries,
- a web administration application may need HTTP and Express but not MQTT,
- an MQTT bridge may need MQTT client support and selected transport components,
- a database-backed store may need MariaDB support while a pure broker may not.

This is where component packaging becomes practical.

A deployment is easier to reason about when installed packages still reflect the same component boundaries that existed in the build.

#### Deployment is not only copying binaries

Copying one executable is rarely the whole deployment.

A SNode.C application may need:

- shared libraries,
- protocol upgrade modules,
- WebSocket subprotocol modules,
- external library dependencies,
- configuration files,
- a writable log directory,
- a writable pid directory,
- TLS certificates and private keys,
- database connectivity,
- and a service definition.

The binary is only one part of the deployed system.

### Packages and installed component surfaces

#### CPack as the ordinary Linux packaging bridge

SNode.C's top-level build enters `src` and then includes the project packaging configuration.

That makes packaging part of the project build story, not an unrelated external script.

The packaging file enables Debian-style package generation, shared-library dependency generation, shared-library metadata generation, component dependency handling, component installation, and one package per component group.

This matters because it lets the component model survive into deployable packages.

A useful deployment path is:

```text
SNode.C component target
  -> install component
      -> CPack component package
          -> package dependency metadata
              -> target installation
```

The component model is therefore not only useful while compiling from source.

It can become visible to the target system's package manager.

#### What CPack solves, and what it does not solve

CPack can package installed components and express package dependencies.

It can help generate binary packages from the install rules and component metadata.

It does not solve everything about deployment.

It does not create:

- service supervision policy,
- certificate material,
- database schema,
- site-specific configuration,
- OpenWrt feed layout,
- repository signing policy,
- operational update policy.

Those concerns remain deployment work.

CPack provides the packaging bridge.

It does not replace system design.

#### Package dependencies follow component dependencies

Package dependencies should follow component dependencies.

That is exactly what the SNode.C packaging configuration expresses.

Examples include:

```text
utils
  -> logger

core
  -> mux-${IO_Multiplexer}
  -> utils

websocket-server
  -> websocket
  -> http-server

websocket-client
  -> websocket
  -> http-client

net-in-stream-tls
  -> net-in-stream
  -> core-socket-stream-tls
```

This mirrors the component graph from Chapter 32.

A package manager should not have to rediscover the architecture from filenames.

The package metadata should already carry the dependency story.

#### Multiplexer packages and runtime overrides

Chapter 32 introduced the multiplexer choice.

Deployment makes that choice visible.

SNode.C has package components for the multiplexer libraries:

```text
mux-epoll
mux-poll
mux-select
```

The `core` package depends on the selected default multiplexer component:

```text
core
  -> mux-${IO_Multiplexer}
  -> utils
```

That is the ordinary deployment path.

A deployment may still install additional multiplexer libraries deliberately if process-local `LD_PRELOAD` overrides are part of the operational strategy.

That gives two deployment modes:

```text
normal package dependency
  -> default multiplexer installed with core

explicit operational override
  -> additional multiplexer library available for LD_PRELOAD
```

The important point is that both mechanisms remain deployment decisions.

They do not change the application-facing event-driven model.

#### Installed paths and runtime-loaded modules

Some libraries are ordinary link-time dependencies.

Others are part of runtime protocol composition.

HTTP upgrade support, WebSocket upgrade handling, WebSocket subprotocol support, and MQTT-over-WebSocket composition make installation paths operationally important.

A dynamically loaded or path-sensitive module must be installed where the runtime expects it, or where configuration tells the runtime to find it.

This is why Chapter 32 discussed output directories, install directories, RPATH, and upgrade-library locations.

In deployment, those choices stop being abstract build details.

They become the difference between:

```text
application starts
  -> runtime protocol extension is found
      -> WebSocket or MQTT-over-WebSocket works
```

and:

```text
application starts
  -> runtime protocol extension is missing
      -> upgrade path fails
```

#### RPATH as deployment policy

RPATH is often treated as a linker detail.

For SNode.C it is also deployment policy.

In a build tree, library locations are usually convenient and known.

In an installed system, the runtime loader must still find the libraries.

For ordinary system libraries, the platform linker configuration may be enough.

For nested SNode.C protocol-extension layouts, install RPATH and well-defined library directories can be part of the runtime contract.

A deployment should answer:

- will the platform loader find ordinary shared libraries?
- will SNode.C find runtime-loaded upgrade or subprotocol modules?
- does the installed path match what the build encoded?
- does cross-compilation staging avoid leaking build-host paths into target binaries?

The last question becomes especially important for OpenWrt and other cross-compiled environments.

### Runtime state and service operation

#### Configuration directories

SNode.C's configuration model creates real deployment expectations.

When run with effective root privileges, the current configuration startup code uses system-level directories:

```text
/etc/snode.c
/var/log/snode.c
/var/run/snode.c
```

When run as an ordinary user, it uses user-local locations:

```text
$XDG_CONFIG_HOME/.config/snode.c
$XDG_CONFIG_HOME/.local/log/snode.c
$XDG_CONFIG_HOME/.local/run/snode.c
```

or corresponding locations below the user's home directory when the environment does not provide `XDG_CONFIG_HOME`.

This distinction is useful.

The same application can run in development as a normal user and in deployment as a system service, without pretending that those are the same mode.

The directories are part of the operational shell of the application.

#### The `snodec` group and ownership model

When root-mode directory creation is needed, SNode.C expects a system group named `snodec`.

The startup code creates the configuration, log, and pid directories with group-oriented permissions and assigns group ownership to the `snodec` group when running as root.

A deployment package or installation procedure therefore has to prepare the runtime ownership model.

That usually means:

- create the `snodec` group if it does not exist,
- set directory ownership and permissions correctly,
- add service users where appropriate,
- avoid world-writable runtime directories,
- and make sure the application can create or read its configuration, log, and pid files.

This is not only security hygiene.

It is operational reliability.

A service that cannot create its pid file or log file because deployment forgot directory ownership will fail in a way that looks unrelated to HTTP, MQTT, WebSocket, or database code.

#### Daemonization and service managers

SNode.C applications expose daemonization-related options through the configuration shell.

An application can run in foreground mode or daemon mode, write pid files, and switch user or group privileges.

That is useful.

It does not remove the need for a host service manager.

On general-purpose Linux, a long-running service is often better supervised by systemd or the local service manager. That service manager can own restart policy, logging integration, dependencies, user identity, and lifecycle.

On OpenWrt, the corresponding service supervision layer is normally `procd`.

The deployment question is therefore not only:

```text
Can the program daemonize itself?
```

It is also:

```text
Which operating-system service model should supervise this role?
```

SNode.C gives applications an operational shell.

Deployment integrates that shell with the host service model.

#### Foreground mode during development

During development and debugging, foreground execution is usually the clearest mode.

It keeps logs visible, makes crashes obvious, and makes configuration experiments easy.

A typical development rhythm is:

```text
run in the foreground
  -> inspect help and effective configuration
      -> increase verbose level if needed
          -> write a configuration file
              -> move the role into a managed service
```

This follows naturally from the configuration model.

Deployment begins with understanding the effective configuration, not with hiding the process in the background.

#### Generated configuration as deployment artifact

SNode.C's ability to show and write configuration is especially important in deployment.

A generated configuration file is not only convenient.

It is a deployment artifact.

It records:

- which instances exist,
- which instances are enabled,
- which local and remote addresses are used,
- which TLS settings are active,
- which retry and timeout policies matter,
- and which application-level options shape logging or daemon behavior.

This is particularly valuable for multi-role systems.

A SNode.C configuration file can become a readable map of the deployed role constellation.

That is much clearer than a shell script full of opaque command-line fragments.

#### Logs and pid files as managed state

Logs and pid files are runtime state.

They are not source files, and they are not static configuration.

A deployment answers:

- where are logs written?
- who can read them?
- are they rotated by the operating system?
- where is the pid file written?
- does the service user have permission to write it?
- does the init system rely on it, or is it only a SNode.C convenience?

These questions are mundane but important.

A network framework can be technically correct and still fail operationally if runtime state is unmanaged.

### Deployment-specific resources

#### TLS certificate material

TLS deployment is not finished when an application links against TLS-capable components.

A TLS deployment also installs and protects certificate material.

That includes:

- certificate chains,
- private keys,
- CA files or CA directories,
- renewal policy,
- file ownership,
- file permissions,
- and SNI-related configuration where needed.

A TLS-capable binary is not yet a secure deployment.

The certificate and trust material must be deployed correctly too.

#### Database dependencies and persistent state

MariaDB support adds another deployment dimension.

An application may need the MariaDB client library on the target. It may also need access to a database server, socket path or network endpoint, database name, user, password source, schema, and permissions.

Database deployment is therefore both:

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

Some applications deploy more than binaries and shared libraries.

For example, the MQTTSuite broker build installs browser assets for its web interface below a MQTTSuite web directory.

That is a concrete reminder that application deployment may include:

- executables,
- SNode.C libraries,
- web assets,
- configuration files,
- service definitions,
- and runtime directories.

Those files belong to different parts of the filesystem and have different update and ownership expectations.

A deployment that treats all of them as one anonymous copy step loses useful structure.

### Embedded Linux and OpenWrt

#### Embedded Linux changes the deployment priorities

General-purpose Linux teaches the basic model.

Embedded Linux changes the priorities.

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

This is why SNode.C's componentized design matters.

A constrained target does not need to carry protocol families, database support, example applications, or dynamic modules it never uses.

On embedded systems, linking and packaging discipline become resource discipline.

#### OpenWrt is Linux under embedded constraints

OpenWrt is Linux, but it is not ordinary server deployment.

It targets routers and embedded network devices.

It uses a cross-compilation build system and package feeds.

It commonly appears with BusyBox, musl, `procd`, overlay filesystems, and package-manager workflows rather than a full desktop/server distribution model.

A compact mental model is:

```text
OpenWrt deployment
  -> SNode.C Linux deployment
      -> under embedded, cross-compiled, package-managed constraints
```

That is the heart of the OpenWrt part of the chapter.

#### The OpenWrt SDK as packaging environment

For application packages, the OpenWrt SDK is usually the right starting point.

A binary copied from a desktop build tree is usually the wrong deployment artifact for OpenWrt.

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

The SDK provides a target-specific cross-compilation environment.

That is the right environment for C++ applications with shared libraries, optional dependencies, and package metadata.

#### OpenWrt deployment flow

A compact OpenWrt deployment flow looks like this:

```text
OpenWrt SDK
  -> package recipe
      -> cross-compiled package
          -> feed or image build
              -> package manager installation
                  -> procd service definition
                      -> SNode.C configuration and runtime state
```

The exact commands depend on the OpenWrt release and build setup.

The architectural flow remains stable.

#### Package recipes should preserve component meaning

An OpenWrt package recipe should not flatten SNode.C blindly.

It should preserve the smallest useful deployable surface.

For example, a feed may provide packages for:

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

The exact split is a packaging policy decision.

The principle is stable:

```text
small target
  -> small package surface
      -> explicit dependencies
          -> reproducible image
```

This is how an embedded target stays understandable.

#### OpenWrt dependencies must be explicit

OpenWrt packages declare dependencies explicitly.

A package that needs TLS depends on the selected TLS library packages.

An MQTT or HTTP component that needs JSON support depends on the JSON package if it is dynamically provided, or ensures it is built appropriately.

A MariaDB-backed tool depends on the MariaDB client library.

A Bluetooth component depends on Bluetooth stack support where applicable.

This is not only build correctness.

It is image reproducibility.

An OpenWrt image is assembled from many small packages. Hidden dependencies make the final image fragile and difficult to reproduce.

#### Package-manager format is release-specific

OpenWrt package-manager tooling and package formats are release-specific.

The durable lesson is not a filename extension.

A package recipe should express the software correctly and let the OpenWrt build system produce the package format used by the selected release.

That keeps the deployment lesson stable even when the package-manager workflow changes.

#### Feeds are distribution boundaries

An OpenWrt feed is more than a directory of package recipes.

It is a distribution boundary.

A feed tells downstream systems:

- which packages exist,
- which versions are available,
- which dependencies they require,
- which target architectures are supported,
- and which packages can be installed or built into an image.

A compact view is:

```text
feed
  -> package recipes
      -> package dependencies
          -> target architecture builds
              -> repository metadata
```

A clear feed layout makes the system easier to build, install, update, and reproduce.

#### Repository signing and update trust

Once packages are distributed through an OpenWrt package repository, signing becomes part of deployment trust.

The target device must be able to trust repository metadata and package source according to the package manager used by that OpenWrt release.

This is especially important for routers and network infrastructure devices.

A technically correct package is still not a complete deployment story if the repository cannot be trusted or updated cleanly.

#### `procd` service integration

On OpenWrt, `procd` is the normal service supervision layer.

A SNode.C application packaged for OpenWrt should therefore be described as a `procd`-managed service when it is meant to run continuously.

That service definition is where deployment expresses:

- how the process starts,
- which configuration file is used,
- which user or group is used,
- whether the service restarts,
- and which dependencies must be available before startup.

The application may still support daemonization.

But on OpenWrt, the deployed role should fit the platform service model.

### Reading a deployment

#### Practical deployment checklist

A SNode.C deployment can be read with a checklist:

1. Which executable or service role is being deployed?
2. Which SNode.C components does it require?
3. Which package components provide those libraries?
4. Which runtime-loaded modules must be installed?
5. Which external libraries are required?
6. Which configuration file describes the role?
7. Which user and group run the process?
8. Which directories hold configuration, logs, and pid files?
9. Which TLS or database resources are required?
10. Which service manager owns lifecycle and restart policy?
11. Which package manager installs or updates the service?
12. Which repository or feed provides the packages?
13. Which trust model protects package updates?

This checklist is not a command sequence.

It is a way to keep deployment architectural.

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

When these details are hidden, failures appear later as unrelated runtime problems.

When they are explicit, deployment becomes another readable part of the system.

### What to remember

- Deployment is architecture entering the filesystem.
- Linking proves that the binary can be built; deployment proves that the runtime environment exists.
- SNode.C's component model should survive installation and packaging.
- CPack connects install components to ordinary Linux packages, but it does not replace service, certificate, database, or repository policy.
- Package dependencies should follow component dependencies.
- Runtime-loaded upgrade and subprotocol modules make installation paths and RPATH part of deployment.
- Root-mode SNode.C deployments use system-level configuration, log, and pid directories and expect the `snodec` group for directory ownership.
- Generated configuration files are deployment artifacts.
- Logs and pid files are managed runtime state.
- TLS deployment includes certificate and trust material.
- Database deployment includes both package dependencies and persistent-state assumptions.
- OpenWrt deployment is Linux deployment under embedded, cross-compiled, package-managed constraints.
- OpenWrt packages should preserve the smallest useful SNode.C component surface.
- Continuous OpenWrt services should fit the `procd` service model.
- Package repositories and feeds are part of deployment trust.

### Closing perspective

Chapter 33 moved from build artifacts to deployed systems.

The same architecture that appears in SNode.C targets and packages also appears in installed libraries, runtime module paths, configuration directories, service definitions, and package repositories.

That is why deployment belongs in Part X.

The next chapter turns to testing, debugging, and benchmarking. Once a system can be built and deployed, the next question is how to verify, inspect, and measure it without losing the architectural clarity that made the build and deployment understandable in the first place.
