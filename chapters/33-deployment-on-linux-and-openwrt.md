## Deployment on Linux and OpenWrt
### Why deployment deserves its own chapter

A framework book can easily make deployment feel like an afterthought.

That would be a mistake here.

SNode.C is not only a collection of headers and libraries.

It is a framework for building long-running communication roles, protocol stacks, MQTT tools, HTTP applications, WebSocket upgrade handlers, database-connected services, and IoT-facing applications.

Once such programs leave the developer’s build tree, several questions immediately become real:

- where are the shared libraries installed?
- where are runtime-loaded protocol modules installed?
- where do configuration files live?
- where do logs and pid files live?
- which user and group should own runtime state?
- which package contains which component?
- which dependencies are required on the target?
- what changes when the target is not a desktop Linux machine but OpenWrt?

Those questions are not merely operational details.

They are the deployment form of the architecture the book has been teaching all along.

That is why this chapter follows the CMake and component chapter directly.

Chapter 32 explained how SNode.C is built and componentized.

This chapter explains how that componentized framework becomes an installed system.

### Deployment is architecture entering the filesystem

A useful first sentence is this:

> Deployment is architecture entering the filesystem.

That may sound dramatic, but it is accurate.

When SNode.C is installed, the framework’s architectural decisions become visible as:

- shared libraries,
- component packages,
- executable applications,
- exported CMake package files,
- runtime-loaded upgrade modules,
- configuration directories,
- log directories,
- pid directories,
- service definitions,
- and package-manager metadata.

This is why deployment should not be discussed only as “copy the executable and run it.”

That may work for a tiny experiment.

It is not enough for serious SNode.C systems.

### The first deployment target is ordinary Linux

The first deployment target is ordinary Linux.

This includes development workstations, servers, virtual machines, SBCs running Debian-like distributions, and Linux-based lab systems.

On this kind of target, the deployment story is usually familiar:

- build with CMake,
- install into a prefix,
- generate or install packages,
- run services directly or through a service manager,
- keep configuration under system or user configuration directories,
- keep logs and pid files under appropriate runtime locations.

This is the easiest deployment environment to understand because it is close to the build environment.

But even here, SNode.C has a richer story than a single binary.

### Linux deployment should preserve component meaning

Chapter 32 argued that SNode.C’s components are architectural.

Deployment should preserve that.

A Linux package set should not blindly collapse everything into one enormous install unit if the application does not need that.

For example:

- a small IPv4 stream tool should not need HTTP, WebSocket, MQTT, and MariaDB libraries,
- a web administration application may need HTTP and Express but not MQTT,
- a MQTT bridge may need MQTT client support and TLS but not the full application examples,
- a database-backed store may need MariaDB support while a pure broker may not.

This is where component packaging becomes practical.

A deployment is easier to reason about when installed packages still reflect the same component boundaries that existed in the build.

### CPack is the ordinary Linux packaging bridge

The current SNode.C build already contains CPack configuration.

That matters because CPack is the bridge from CMake targets and install components to ordinary binary packages.

The build enables Debian-style package generation, shared-library dependency generation, component dependency handling, and one-package-per-component grouping.

This is an important design decision.

It means SNode.C’s component model is not only useful while building from source.

It can also become visible in deployable packages.

For Linux distributions using Debian-style packaging, this creates a natural path:

- build the framework,
- install components into a package staging area,
- generate packages,
- install only the component set the target needs.

That is much better than pretending every target machine needs the whole framework surface.

### Package dependencies should follow target dependencies

The CPack configuration declares dependencies among install components.

That is exactly what deployment needs.

For example, a high-level component should not be installable in a way that forgets its lower layers.

A WebSocket server component depends on the WebSocket base and HTTP server support.

A MQTT client depends on the MQTT core.

A network-family TLS component depends on the lower network-family stream layer and the TLS stream layer.

This mirrors the framework’s conceptual dependency graph.

That is good.

A package manager should not have to rediscover the architecture from filenames.

The package metadata should already carry the dependency story.

### Dynamic loading makes installation paths part of runtime behavior

Some SNode.C components are not merely linked and forgotten.

HTTP upgrade support, WebSocket subprotocol support, and MQTT-over-WebSocket composition bring runtime-loaded or path-sensitive libraries into the picture.

That means installation paths matter.

A dynamically loaded library must be placed where the runtime expects it or where configuration tells the runtime to find it.

This is why Chapter 32 spent time on RPATH, library output directories, and upgrade-library install locations.

In deployment, those choices stop being abstract build details.

They become the difference between:

- a working WebSocket or MQTT-over-WebSocket stack,
- and an application that builds correctly but fails to load its runtime protocol extension.

### RPATH is a deployment decision, not only a linker detail

RPATH deserves a second mention because it is often misunderstood.

In small examples, a developer may run directly from the build tree, where library locations are convenient and obvious.

In an installed system, that convenience disappears.

The runtime loader must be able to find the shared libraries.

For ordinary system libraries, the platform linker configuration may be enough.

For nested SNode.C protocol-extension layouts, install RPATH and well-defined library directories become more important.

A good deployment should answer these questions explicitly:

- will the library be found by the platform loader?
- will runtime-loaded upgrade or subprotocol modules be found by the framework?
- does the installed path still match what the build encoded?
- does cross-compilation staging accidentally leak build-host paths into target binaries?

The last question becomes especially important on OpenWrt.

### Configuration directories are part of deployment

SNode.C’s configuration model is not theoretical.

It creates real deployment expectations.

When run as root, the framework uses system-level directories such as:

```text
/etc/snode.c
/var/log/snode.c
/var/run/snode.c
```

When run as an ordinary user, it uses user-level locations under the user’s home or XDG configuration area.

This is a very useful deployment behavior.

It means the same application can run in development as an ordinary user and in production as a system service without pretending those are the same mode.

The directories themselves become part of the application’s operational shell.

### The `snodec` group is an operational hint

The current configuration startup code expects the system group `snodec` when it creates system-level configuration, log, and pid directories as root.

That is an important deployment hint.

A package or installation procedure should not merely copy files.

It should also prepare the expected runtime ownership model.

That usually means:

- create the group if it does not exist,
- set directory ownership and permissions correctly,
- add service users where appropriate,
- avoid world-writable runtime directories,
- and make sure the application can create or read its configuration and log files.

This is not only security hygiene.

It is also operational reliability.

A service that cannot create its pid file or log file because deployment forgot directory ownership will fail in ways that look unrelated to the protocol code.

### Daemonization is supported, but service managers still matter

SNode.C applications expose daemonization-related options through the application configuration shell.

That means a program can run in a foreground or background mode, write pid files, and switch user or group privileges.

This is useful.

But a modern Linux deployment should still think carefully about the service manager.

On a systemd-based Linux distribution, it may often be cleaner to let systemd manage foreground services, restart policy, logging integration, dependencies, and user identity.

On smaller systems or embedded targets, a different init system may be used.

The important lesson is this:

SNode.C gives applications an operational shell, but deployment should still integrate with the host operating system’s service model honestly.

Do not use daemonization as an excuse to avoid proper service definition.

### Foreground mode is often best during development

During development and debugging, foreground execution is usually the best mode.

It keeps logs visible, makes crashes obvious, and makes configuration experiments easy.

A typical development rhythm is:

- run in the foreground,
- inspect help and effective configuration,
- increase verbose level when needed,
- write a configuration file once the shape is correct,
- only then move the same role into a managed service.

This is exactly the rhythm the earlier configuration chapters prepared.

Deployment begins with understanding the effective configuration, not with hiding the process in the background.

### Generated configuration is a deployment artifact

SNode.C’s ability to show and write configuration is especially important in deployment.

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

That is much better than a shell script full of opaque command-line fragments.

### Logs and pid files should be treated as managed state

Logs and pid files are not application source.

They are runtime state.

That means deployment should handle them differently from binaries and configuration.

A good deployment answers:

- where are logs written?
- who can read them?
- are they rotated by the system?
- where is the pid file written?
- does the service user have permission to write it?
- does the init system rely on it, or is it only a SNode.C convenience?

These questions are mundane but important.

A technically elegant network framework still fails operationally if runtime state is not managed.

### TLS deployment is certificate deployment

TLS is not finished when the program links against the TLS component.

A TLS deployment must also install and protect certificate material.

That includes questions such as:

- where is the certificate chain stored?
- where is the private key stored?
- which user can read the private key?
- how are CA files or directories managed?
- how are certificate renewals handled?
- how are SNI-related configurations expressed?

This is where deployment and security meet directly.

The TLS chapter explained the connection-layer model.

This chapter adds the operational point:

A TLS-capable binary is not yet a secure deployment.

The certificate and trust material must be deployed correctly too.

### Database deployment is dependency and state deployment

MariaDB support brings another deployment dimension.

The application may require the MariaDB client library on the target.

It may also require access to a MariaDB server, socket path, database, user, password source, schema, and permissions.

That means database deployment is both:

- package dependency deployment,
- and persistent-state deployment.

A good SNode.C deployment should not hide database setup inside an application start script.

It should describe it clearly:

- which package provides the client library,
- which configuration values identify the database endpoint,
- which schema is expected,
- which credentials are required,
- and what happens when the database is unavailable.

This becomes especially important in MQTT store or IoT history applications.

### Embedded Linux changes the deployment priorities

Ordinary Linux deployment teaches the general model.

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

This is why SNode.C’s componentized design matters so much.

A constrained target should not carry unnecessary protocol families, database support, example apps, or dynamic modules that it never uses.

On embedded systems, linking and packaging discipline become resource discipline.

### OpenWrt is Linux, but it is not ordinary Linux deployment

OpenWrt is Linux, but it should not be treated like a generic server distribution.

It has a different build and deployment culture.

It targets routers and embedded network devices.

It uses a cross-compilation build system and package feeds.

It has constrained storage and memory assumptions.

It commonly uses BusyBox, musl, procd, overlay filesystems, and package-manager workflows rather than the full desktop/server distribution model.

Therefore, the right mental model is:

> OpenWrt deployment is SNode.C Linux deployment under embedded, cross-compiled, package-managed constraints.

That sentence is the heart of the OpenWrt part of the chapter.

### The OpenWrt SDK is usually the right packaging environment

For application packages, the OpenWrt SDK is usually the right starting point.

A developer should not normally copy a binary built on a desktop Linux machine onto an OpenWrt router and hope it works.

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

The SDK gives the developer a target-specific cross-compilation environment.

That is exactly what a C++ framework with shared libraries and optional dependencies needs.

### OpenWrt package recipes should reflect SNode.C components

A good OpenWrt package recipe should not flatten SNode.C blindly.

It should reflect the component story from Chapter 32.

For example, an OpenWrt feed may provide separate packages for:

- core runtime libraries,
- network-family components,
- TLS stream support,
- HTTP support,
- Express support,
- WebSocket support,
- MQTT support,
- selected applications,
- selected MQTTSuite executables.

The exact split is a packaging policy decision.

But the principle is stable:

OpenWrt packaging should preserve the smallest useful deployable surface.

That is how the target stays small and understandable.

### OpenWrt dependencies must be explicit

OpenWrt packages should declare dependencies honestly.

A package that needs TLS should depend on the chosen TLS library packages.

A MQTT component that needs JSON support should depend on the JSON package if it is dynamically provided or ensure it is built appropriately.

A MariaDB-backed tool should depend on the MariaDB client library.

A Bluetooth component should depend on Bluetooth stack support where applicable.

This is not only a build correctness issue.

It is also a maintenance issue.

An OpenWrt image is often assembled from many small packages.

If dependencies are hidden, the final image becomes fragile and hard to reproduce.

### The OpenWrt package manager transition should be handled deliberately

OpenWrt package workflows have historically been associated with `.ipk` packages and `opkg`.

Newer OpenWrt releases have moved toward APK-based package management.

For this book, the important lesson is not to freeze the chapter around one filename extension.

The better lesson is:

> write OpenWrt packaging so that the package recipe expresses the software correctly, then let the release-specific OpenWrt build system produce the package format used by that release.

That matters because the package format and repository-signing workflow are release-specific operational details.

A good SNode.C deployment chapter should teach durable architecture, not only today’s command syntax.

### OpenWrt feeds are distribution boundaries

An OpenWrt feed is more than a directory of package recipes.

It is a distribution boundary.

When SNode.C or MQTTSuite packages are placed into a feed, the feed becomes the place where downstream systems learn:

- which packages exist,
- which versions are available,
- which dependencies they require,
- which target architectures are supported,
- and which packages can be installed or built into an image.

This is why feed organization matters.

A sloppy feed layout makes deployment sloppy.

A clear feed layout makes the system easier to build, install, and update.

### Repository signing is part of deployment trust

Once packages are distributed through an OpenWrt package repository, signing becomes part of the deployment story.

It is not enough to build packages.

The target device must be able to trust the repository metadata and package source according to the package manager used by that OpenWrt release.

This is especially important for routers and network infrastructure devices.

A SNode.C deployment on OpenWrt may be technically correct and still operationally unacceptable if the package repository cannot be trusted or updated cleanly.

The book should therefore treat signing and trust as deployment concerns, not as optional polish.

### Cross-compilation path leakage is a real risk

Cross-compilation introduces a risk that ordinary Linux builds rarely expose:

build-host or staging paths can accidentally leak into installed target artifacts.

This is especially relevant for RPATH, CMake package files, pkg-config data, and install-tree metadata.

On OpenWrt, the build uses staging directories and target root directories during packaging.

Those paths are useful during the build.

They must not become required paths on the running router.

A good deployment should inspect binaries and package metadata for accidental references to build-host locations.

This is one of the most important OpenWrt-specific lessons for a CMake-based C++ framework.

### RPATH on OpenWrt should be minimal and intentional

On ordinary Linux, RPATH can be useful for non-standard install prefixes.

On OpenWrt, RPATH should be handled with extra care.

The target filesystem is small, the library paths are usually conventional, and the package manager owns the installation layout.

An RPATH that points into a staging directory is wrong.

An unnecessary RPATH may be undesirable.

A runtime-loaded protocol module path, by contrast, may still need to be explicit and well-defined.

So the rule is not “always remove RPATH.”

The rule is:

> remove accidental build paths; preserve only target-meaningful runtime lookup behavior.

That distinction matters.

### Runtime-loaded modules need package-aware installation

If a SNode.C application depends on WebSocket upgrade support or MQTT-over-WebSocket subprotocol modules, OpenWrt packaging must install those modules in the correct target path.

It is not enough to install the main executable.

The package must include:

- the shared libraries needed by the executable,
- the protocol-extension or subprotocol libraries needed at runtime,
- and any configuration defaults required to find them.

This is a common embedded deployment trap.

A developer tests successfully in the build tree, then packages only the visible executable, and the target fails because a dynamic module is missing.

A good package recipe should prevent that.

### OpenWrt service integration belongs to procd

On OpenWrt, long-running services are normally integrated through init scripts managed by procd.

That means a SNode.C service package should usually include an init script or equivalent service integration.

The service definition should answer:

- what executable starts?
- which configuration file is used?
- which user or group should run the process?
- should the service restart automatically?
- which network conditions should be waited for?
- where are logs expected to go?
- how is shutdown handled?

This is the OpenWrt analogue of the service-manager discussion for ordinary Linux.

Again, the key point is the same:

copying the binary is not deployment.

A service must be integrated into the target operating environment.

### OpenWrt configuration and SNode.C configuration should not be confused

OpenWrt has its own configuration culture and UCI system.

SNode.C has its own CLI11-based hierarchical configuration model.

Those two worlds can be connected, but they should not be confused.

A simple package may use SNode.C’s native configuration file under `/etc/snode.c` directly.

A more OpenWrt-native package may expose selected settings through UCI and generate or pass SNode.C configuration from those values.

Both approaches can be valid.

The important design question is:

> Who is the intended operator, and which configuration surface should they use?

For development and framework-centered deployments, native SNode.C configuration may be best.

For router users and LuCI-oriented administration, UCI integration may eventually be more appropriate.

### Log volume matters on OpenWrt

Log volume matters much more on OpenWrt than on a desktop or server.

Flash storage is limited.

Persistent writes should be minimized.

The system log may be memory-backed or rotated differently from a desktop system.

Verbose protocol logging that is useful during debugging may be inappropriate in production.

This means OpenWrt deployments should choose logging policy carefully:

- quiet or low-verbosity defaults,
- temporary higher verbosity during debugging,
- system log integration where appropriate,
- avoidance of uncontrolled file growth,
- and careful use of persistent log files.

A good IoT deployment is observable, but not write-amplifying.

### TLS and certificates are harder on small routers

TLS deployment on OpenWrt has all the concerns of ordinary Linux, plus embedded constraints.

Private keys must be protected.

CA bundles may be smaller or packaged differently.

Certificate renewal may be harder.

Time synchronization may matter because TLS validation depends on correct time.

Storage for certificates may be limited.

This does not mean TLS should be avoided.

It means TLS deployment should be designed deliberately.

A secure transport layer requires a secure operational environment around it.

### MQTT and OpenWrt fit naturally, but should still be scoped

MQTT and OpenWrt are a natural pair for many systems.

Routers and embedded gateways often sit exactly where MQTT bridges, integrators, or stores are useful.

But natural fit is not the same as unlimited fit.

A router target should run only the MQTT roles it actually needs.

For example:

- a small gateway may only need an MQTT client bridge,
- a lab router may host a small broker,
- a richer edge device may run broker plus HTTP administration,
- a storage-heavy service may belong on a server instead of a tiny router.

This is the same architectural judgment as before, now applied to resource-constrained deployment.

### MQTTSuite deployment should be role-based

MQTTSuite is especially useful on OpenWrt-like targets because it already consists of focused tools.

That makes role-based deployment natural.

A target may install only:

- `mqttcli` for testing,
- `mqttbridge` for broker-to-broker forwarding,
- `mqttintegrator` for mapping and transformation,
- `mqttbroker` for local broker service,
- `mqttstore` only when database persistence is actually available and appropriate.

This is much healthier than treating the suite as one inseparable blob.

The package split should follow the application split.

That is how the ecosystem remains usable on constrained systems.

### Image-based deployment versus post-install deployment

OpenWrt offers two broad deployment styles.

One style is to build packages and install them onto an existing device.

Another style is to include the packages directly in a custom firmware image.

Both can be valid.

Post-install deployment is useful during development and testing.

Image-based deployment is often better for repeatable field deployment because the firmware image already contains the exact role set, dependencies, and default configuration expected for the device.

A good SNode.C/OpenWrt workflow often moves from the first style to the second:

- develop packages,
- test installation on a device,
- stabilize configuration,
- then build a repeatable image.

### The deployment checklist for ordinary Linux

For ordinary Linux, a practical deployment checklist looks like this:

1. choose the smallest honest component set,
2. build or install the required packages,
3. verify shared-library resolution,
4. verify runtime-loaded module paths if upgrades or subprotocols are used,
5. create required users and groups,
6. ensure `/etc/snode.c`, `/var/log/snode.c`, and `/var/run/snode.c` or their equivalents exist with correct permissions,
7. generate and inspect configuration,
8. place TLS and database credentials safely,
9. define the service manager unit or init script,
10. run once in foreground with useful verbosity before enabling automatic startup.

This checklist is deliberately practical.

It is how architecture becomes a reliable deployment.

### The deployment checklist for OpenWrt

For OpenWrt, the checklist changes:

1. choose the exact OpenWrt release, target, and SDK,
2. decide which SNode.C and application components are needed,
3. write or update package recipes in a feed,
4. declare dependencies explicitly,
5. build with the target SDK or buildroot,
6. inspect package contents for unnecessary files and missing runtime-loaded modules,
7. check for staging-directory path leakage,
8. verify service integration through procd,
9. decide whether configuration is native SNode.C, UCI-integrated, or both,
10. install packages or build a firmware image,
11. test on the actual target hardware under realistic memory, storage, and network conditions.

This checklist is intentionally different from the ordinary Linux one.

OpenWrt is Linux, but it is a different deployment culture.

### Common deployment mistakes

Several deployment mistakes occur repeatedly in systems like this.

#### Mistake 1: Installing the executable but not the runtime-loaded modules

A program may start but fail when a WebSocket upgrade or subprotocol is needed.

#### Mistake 2: Linking against everything

This wastes space and makes dependencies harder to reason about, especially on OpenWrt.

#### Mistake 3: Letting build paths leak into target binaries

This is especially dangerous in cross-compilation and staging environments.

#### Mistake 4: Treating TLS as only a build option

TLS deployment also requires certificate, key, trust, and time-management decisions.

#### Mistake 5: Using verbose logs as a production default on embedded flash

This may damage observability by creating storage pressure and unnecessary writes.

#### Mistake 6: Confusing SNode.C configuration with OpenWrt UCI

They can cooperate, but they are not the same system.

### Deployment testing should happen on the real target

A package that builds successfully is not necessarily a good deployment.

A service that runs on a development machine is not necessarily valid on an embedded target.

Final deployment testing should happen on the real target class.

For OpenWrt, that means testing on the actual device or a close hardware equivalent.

Important checks include:

- startup and shutdown,
- service restart behavior,
- memory footprint,
- missing shared libraries,
- missing dynamic modules,
- config-file permissions,
- log behavior,
- TLS certificate access,
- network availability timing,
- and upgrade/reinstall behavior.

This is the difference between a build success and a deployable system.

### Deployment is also documentation

A good deployment teaches the next maintainer how the system is intended to work.

That means package names, service names, configuration names, and instance names should be chosen carefully.

For example:

- `in-mqtt`,
- `in-mqtts`,
- `un-mqtt`,
- `in-http`,
- `in-https`,
- `bridge-client`,
- `admin-http`,
- `local-control`.

Names like these make the role constellation visible.

A poor deployment hides the architecture behind generic names.

A good deployment preserves meaning.

### The chapter’s main lesson

The main lesson of this chapter is simple:

> SNode.C deployment should preserve the architecture that SNode.C development created.

If the framework is componentized, the packages should respect components.

If applications are role-based, services and configuration should preserve roles.

If protocol upgrades need runtime-loaded modules, deployment must install those modules deliberately.

If the target is OpenWrt, package recipes, dependencies, service integration, and storage policy must reflect embedded constraints.

Deployment is not where architecture disappears.

Deployment is where architecture becomes operational.

### Common misunderstandings about deployment

#### Misunderstanding 1: “Deployment means copying the binary.”

Corrected view: deployment includes libraries, runtime-loaded modules, configuration, logs, pid files, service integration, dependency metadata, and package trust.

#### Misunderstanding 2: “Linux deployment and OpenWrt deployment are basically the same.”

Corrected view: OpenWrt is Linux, but it has a cross-compiled, package-feed, embedded-device deployment culture.

#### Misunderstanding 3: “The package format is the main OpenWrt issue.”

Corrected view: package format matters, but the deeper issues are target-specific build recipes, dependencies, service integration, repository trust, and resource constraints.

#### Misunderstanding 4: “Runtime-loaded modules are development details.”

Corrected view: they are deployment artifacts and must be installed where the runtime can find them.

#### Misunderstanding 5: “Configuration belongs entirely to the application.”

Corrected view: configuration is part of deployment because it describes which roles exist and how they operate on the target.

### A good one-paragraph summary of the chapter

Deployment in SNode.C is the process of preserving framework architecture in an installed system. On ordinary Linux, that means using component packages, shared-library dependencies, configuration directories, service management, TLS material, and runtime-loaded module paths correctly. On OpenWrt, the same concerns become more constrained and more explicit: packages are built through the target SDK or buildroot, dependencies must be minimal and honest, service integration belongs to the embedded init system, logging and storage policy must respect flash limits, and package feeds or images become the reproducible deployment boundary.

That is the heart of the chapter.

### Closing perspective

This chapter completes the transition from build structure to deployed system.

Chapter 32 showed that the CMake and component model is an architectural map.

This chapter showed that deployment should preserve that map rather than flatten it.

That is especially important for SNode.C because the framework often builds systems composed of several roles and several protocol layers.

A deployment that hides those roles becomes hard to operate.

A deployment that preserves those roles becomes readable, maintainable, and reproducible.

That is exactly what ordinary Linux and OpenWrt deployments should aim for.

The next chapter can now turn to the final maintenance foundation:

how to test, debug, and benchmark SNode.C systems once they are built and deployed.
