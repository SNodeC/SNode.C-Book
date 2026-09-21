## Preparing Your Environment

\index{build environment}
\index{development environment}
\index{source checkout}


### Why the environment matters

Before the architecture can become interesting, the toolchain must be boring. The examples in this book should build, run, and fail in understandable ways, so the first practical task is to keep the source tree, build tree, install prefix, and later playground project separate.

This is more than tidiness. SNode.C is a real C++ framework with a core runtime, network-family components, stream transports, legacy and TLS connection variants, higher protocol layers, example applications, generated CMake targets, installable package components, and optional support for technologies such as Bluetooth and MariaDB.

For example, successfully rebuilding a framework library does not refresh a different copy already installed in a local prefix. An external application can still compile against that older installation. Keeping the locations explicit makes that failure understandable.

The goal of this chapter is therefore simple:

> Prepare a development setup that lets you build SNode.C, run examples, inspect the framework source tree, and later compile small applications against installed SNode.C public headers and installed SNode.C components.

This is not a general Linux installation guide. It does not try to cover every distribution, every package manager, every editor, or every cross-compilation target. The concrete commands assume a normal Linux development machine, with Debian-style package names where package installation is shown. The ideas transfer to other systems, but package names and installation commands may need adjustment.

### Working areas, different purposes

During the book it helps to keep four locations mentally separate:

| Area | Purpose |
|---|---|
| **SNode.C source tree** | framework implementation, C++ source, CMake build system, core runtime, network layers, protocol layers, database support, and example applications |
| **build tree** | generated build files, intermediate object files, and compiled binaries; disposable and kept outside the source tree |
| **install prefix** | installed headers, libraries, CMake package files, and possibly installed executables; useful for self-contained learning |
| **playground project** | small external applications that consume an installed SNode.C package without modifying the framework source tree |

A useful layout is:

```text
projects/
  snode.c/
  snode.c-build/
  snodec-playground/
```

A local install prefix can live outside these source and build directories:

```text
~/.local/snodec/
```

The framework source tree remains the source of truth for the implementation. The build tree is disposable. The install prefix is what external projects consume. The playground is where you can test your understanding.

### What the environment must support

For the first part of the book, the environment must support five activities: **clone and build SNode.C**, **run small server and client examples**, **inspect the framework source tree and build tree separately**, **install the framework into a known prefix**, and **compile small external programs against installed SNode.C public headers and installed SNode.C components**.

Optional technologies should also be visible when available. Bluetooth RFCOMM and Bluetooth L2CAP require the appropriate BlueZ development files. MariaDB support requires MariaDB development files. These optional areas do not have to be used immediately, but the environment should not hide them accidentally.

### Compiler and CMake expectations

\index{compiler requirements}
\index{CMake@\texttt{CMake}}
\index{C++20@C++20}


SNode.C is a modern C++ framework.

The build system expects CMake and a C++20-capable compiler. The top-level build requires CMake 3.18 or newer, and the `src` build configures the project as C++20.

The most important compiler expectations are:

- GCC 12.2 or newer,
- or Clang 13.0 or newer.

This is not an arbitrary preference. SNode.C uses modern C++ internally. Building it with an older compiler is not a good way to learn the framework: the reader will spend time fighting toolchain problems instead of understanding architecture.

A quick check is useful:

```sh
cmake --version
g++ --version
clang++ --version
```

It is fine if only one of GCC or Clang is used, as long as it satisfies the required version.

### Required and optional packages

\index{build environment!dependencies}
\index{build environment!optional dependencies}
\index{build environment!packages}


Package names differ across distributions. On a Debian-style development system, the baseline tools are usually:

```sh
sudo apt update
sudo apt install git cmake make ninja-build g++ clang pkg-config
```

The core framework path also needs development libraries. A useful baseline is:

```sh
sudo apt install libssl-dev nlohmann-json3-dev
```

Optional libraries unlock additional framework areas:

```sh
sudo apt install libbluetooth-dev libmagic-dev libmariadb-dev
```

`libbluetooth-dev` is relevant for Bluetooth RFCOMM and Bluetooth L2CAP. `libmagic-dev` is relevant where file-type or content-type detection is used.

`libmariadb-dev` is relevant for MariaDB support.

Additional developer tools are useful later, especially during maintenance and review:

```sh
sudo apt install iwyu clang-format cmake-format doxygen
```

These tools are not required for the first echo example. They are mentioned here because SNode.C is a framework, and framework work eventually benefits from include checking, formatting, and documentation generation.

### Cloning the framework

\index{SNode.C!cloning}
\index{git checkout@\texttt{git checkout}}


First obtain this edition's electronic source package from the [SNode.C Book repository](https://github.com/SNodeC/SNode.C-Book) or its edition download. The commands below assume that the package is available at `~/projects/SNode.C-Book`. Point the shell variable at the actual location if yours differs:

```sh
export SNODEC_BOOK_SOURCE="$HOME/projects/SNode.C-Book"
```

This directory contains the manuscript, companion examples, and source-baseline record. It is separate from the framework source. The recorded framework tree includes current changes beyond its base commit, so checking out that commit is the first step, not the complete reconstruction.

Choose a directory where you keep source repositories:

```sh
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout --detach 1f0f728fc9b3b45174f2cd790d83b2f493e58af1
git apply "$SNODEC_BOOK_SOURCE/source-baseline/framework-working-tree.patch"
python3 "$SNODEC_BOOK_SOURCE/ci/check-source-alignment.py" --framework "$PWD"
```

The checked-out framework source now lives in:

```text
~/projects/snode.c/
```

The book baseline is SNode.C\textsubscript{\texttt{2.0.0}}. The full commit is the base checkout target; `2.0.0` is the project version recorded by the source. The patch captures the current source-tree changes, and the checker compares the reconstructed file contents with the edition's manifest. Comparing `git rev-parse HEAD` alone would miss those changes.

The SNode.C repository uses `master` as its moving development line. Do not build the examples against an arbitrary newer checkout unless you deliberately want to check the book against a newer framework state. If you already have a clean clone, fetch the source and select the base explicitly, then apply the edition patch once:

```sh
cd ~/projects/snode.c
git fetch origin
git checkout --detach 1f0f728fc9b3b45174f2cd790d83b2f493e58af1
git apply "$SNODEC_BOOK_SOURCE/source-baseline/framework-working-tree.patch"
python3 "$SNODEC_BOOK_SOURCE/ci/check-source-alignment.py" --framework "$PWD"
```

Use a separate clone if the existing checkout contains your own work. An already reconstructed checkout only needs verification; applying the same patch twice is not an update procedure. For normal reading, first learn where examples are located, how the build is organized, and which parts are source code, generated build output, or installation artifacts.

### Use an out-of-tree build

\index{out-of-tree build}
\index{build tree}


A build directory should be separate from the source directory. This keeps generated files away from the code you want to read.

A simple layout is:

```text
~/projects/
  snode.c/
  snode.c-build/
```

Configure the build:

```sh
cd ~/projects
cmake -S snode.c -B snode.c-build
```

Then build:

```sh
cmake --build snode.c-build -j$(nproc)
```

Using `cmake --build` keeps the generator choice out of the foreground; the reader does not need to care immediately whether the generator is Make, Ninja, or something else.

If you prefer Ninja explicitly, select it in a separate build directory:

```sh
cmake -S snode.c -B snode.c-ninja -G Ninja
cmake --build snode.c-ninja -j$(nproc)
```

The build can take some time. That is normal. The framework uses many templates and builds many components and examples.

### Installing the framework

\index{installation}
\index{install tree}


For experimenting inside the framework build tree, installation is not always necessary.

For compiling separate applications against SNode.C with `find_package(snodec ...)`, installation is useful. It turns the framework from “source tree plus build tree” into a package that another CMake project can consume.

A local user installation avoids touching system directories:

```sh
cmake -S snode.c -B snode.c-build \
  -DCMAKE_INSTALL_PREFIX="$HOME/.local/snodec"

cmake --build snode.c-build -j$(nproc)
cmake --install snode.c-build
```

When using a custom prefix, later projects may need to know where to find the installed package:

```sh
export CMAKE_PREFIX_PATH="$HOME/.local/snodec:$CMAKE_PREFIX_PATH"
```

A system-wide installation is also possible. Configure that destination explicitly in its own build directory; running an install command with `sudo` does not change a previously selected local prefix:

```sh
cmake -S snode.c -B snode.c-system -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build snode.c-system -j$(nproc)
sudo cmake --install snode.c-system
sudo ldconfig
```

Use a system-wide install only when you are comfortable installing development libraries into the system prefix.

For the book, a local prefix is often the safer teaching setup. It makes it clear which installation belongs to the experiments and avoids accidental interaction with other system packages.

### Build options worth knowing early

\index{build options}
\index{CMake@\texttt{CMake}!options}


The first chapters do not require many CMake options.

Build selection and runtime diagnostic policy are different choices. The build selects applications, tests, and optional instrumentation. A normal SNode.C application selects its semantic logging policy through the root configuration, for example with `--log-level=5`.

Keep useful lifecycle output enabled while working through the first examples. Chapter 18 explains the semantic logging API and its scoped thresholds; raising diagnostic detail does not require rebuilding the framework with an old macro-logging switch.

::: {.snodec-warning title="Early diagnostic warning"}
Do not make the first examples silent before you understand what they are doing.
:::

### Selecting application, test, and diagnostic builds

\index{SNODEC_BUILD_APPS@\texttt{SNODEC\_BUILD\_APPS}}
\index{SNODEC_BUILD_TESTS@\texttt{SNODEC\_BUILD\_TESTS}}
\index{SNODEC_ENABLE_ASAN@\texttt{SNODEC\_ENABLE\_ASAN}}

The framework distinguishes three build choices that should not be confused with protocol configuration:

| Option | Default | Purpose |
|---|---|---|
| `SNODEC_BUILD_APPS` | `ON` | build the in-tree application and demonstration targets |
| `SNODEC_BUILD_TESTS` | `OFF` | register and build the framework's CTest suite |
| `SNODEC_ENABLE_ASAN` | `OFF` | instrument a GCC/Clang build with AddressSanitizer |

A first development build can include the tests explicitly:

```sh
cmake -S snode.c -B snode.c-tests \
  -DCMAKE_BUILD_TYPE=Debug \
  -DSNODEC_BUILD_APPS=ON \
  -DSNODEC_BUILD_TESTS=ON
cmake --build snode.c-tests --parallel 8
ctest --test-dir snode.c-tests --output-on-failure
```

Keep an instrumented build in a separate directory. Turning on AddressSanitizer is a compiler/linker choice, not a runtime logging level. Chapter 34 explains the test categories and how to interpret passes, failures, and skipped tests.

The logger backend is fetched as an implementation dependency during configuration. An offline build therefore needs the relevant dependency sources or CMake fetch cache already available. Application code still includes `<Log.h>` rather than depending directly on the backend's headers.

The source snapshot used by this edition declares version `2.0.0`. It starts a new C++ API/ABI epoch: rebuild applications and dynamically loaded extensions against the same headers and libraries. Keeping an older binary beside a newer installation is not the same as rebuilding that application successfully.

### Finding built executables

Build-tree layouts differ depending on generator, configuration, and installation choices. Rather than memorizing one exact executable path, learn how to inspect the build tree.

From the build directory, search for echo-related executables:

```sh
cd ~/projects/snode.c-build
find . -type f -executable -name '*echo*'
```

Or search more generally for application executables:

```sh
find . -type f -executable | grep apps
```

This is often more robust than assuming one fixed path.

When later chapters refer to example applications, the important distinction is:

```text
source file location
  -> where the example is implemented

build-tree executable location
  -> where the configured build placed the binary

installed executable location
  -> where installation placed the binary, if it was installed
```

Do not confuse these three. Many build problems become easier to diagnose once this distinction is clear.

### Running server and client programs

\index{server program}
\index{client program}
\index{runtime output}


The basic pattern for server/client examples is simple. Open one terminal for the server. Open another terminal for the client.

Start the server first. Then start the client.

The echo pair in Chapter 3 uses this pattern. The server listens. The client connects and initiates the first message. Once both sides reflect received data, the program intentionally creates visible ping-pong behavior.

That behavior is useful for teaching. It proves that the runtime is active, the connection has been established, callbacks are executed, data is read, and data is written back.

To stop the example, interrupt one side with:

```text
Ctrl-C
```

The first time you run such an example, pay attention to the output. You are not simply checking that the program works. You are learning how the framework makes runtime behavior visible.

### Do not hide runtime output too early

Use the first run to distinguish three observations: the listener reports readiness, the client establishes a connection, and the contexts exchange bytes. A build success proves none of those runtime facts. If only the first observation appears, inspect the client's destination and diagnostics before changing the echo context.

Keep `--log-level=5` for the short teaching run so payload diagnostics are visible, then stop the pair. Later, Chapter 18 separates framework and application scopes so diagnostic volume can be reduced deliberately. The useful habit is to retain evidence of the boundary under investigation, rather than treating either silence or maximum verbosity as a permanent policy.

### Preparing a separate playground project

\index{playground project}
\index{external consumer project}


Besides building the framework source tree itself, it is useful to have a small external playground project.

For example:

```text
~/projects/
  snode.c/
  snode.c-build/
  snodec-playground/
```

The playground is where you can later put small experiments without modifying the framework source tree.

A minimal playground for the first echo-style experiments might eventually contain:

```text
snodec-playground/
  CMakeLists.txt
  EchoSocketContext.h
  EchoSocketContext.cpp
  echoserver.cpp
  echoclient.cpp
```

Do not worry yet about writing all of this. Chapter 3 introduces the first concrete program. The point here is only to prepare a place where an external application can live.

### Components and public headers as installed architecture

\index{components}
\index{public headers}
\index{installed architecture}


When an external application consumes SNode.C, it asks CMake for package components. The same application also includes public SNode.C headers. These two selections belong together: the component selection describes the binary/link surface, while the include selection describes the C++ source surface.

For the first IPv4 legacy stream example, the relevant component is:

```cmake
find_package(snodec COMPONENTS net-in-stream-legacy)
```

The executable then links against the corresponding imported target:

```cmake
target_link_libraries(echoserver PRIVATE snodec::net-in-stream-legacy)
```

The matching public include path has the same structure, expressed with directories rather than CMake component dashes:

```cpp
#include <net/in/stream/legacy/SocketServer.h>
#include <net/in/stream/legacy/SocketClient.h>
```

The application does not include the lower core socket headers merely because the concrete server and client are built from lower socket machinery. It includes the highest public header for the abstraction it directly names. Likewise, the build links the highest component that represents the direct framework surface used by the target.

The actual echo pair has separate server and client targets, but both follow the same public-header/component pairing.

The component name is not arbitrary. It encodes a path through the architecture:

```text
net-in-stream-legacy
```

can be read as:

```text
layer area:     net
network family: in       (IPv4)
transport:      stream
connection:     legacy   (non-TLS stream connection variant)
```

The term `legacy` is important. In this naming context it denotes the non-TLS stream connection variant. It does not, by itself, mean that the component is obsolete or deprecated.

Later chapters will introduce additional component names for IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS variants, HTTP, WebSocket, MQTT, and database support.

Do not try to memorize all names at this stage. Learn the shape instead. SNode.C component names and public include paths are compact forms of architectural information. The dashes in a component name and the slashes in an include path often describe the same stack from different technical viewpoints.

### Check which installation the playground consumes

\index{source tree}
\index{build tree}
\index{install tree}


After configuring the playground in Chapter 3, inspect its `CMakeCache.txt` for `snodec_DIR`. That entry identifies the package configuration CMake actually found. Compare its prefix with the installation you intended to use. The expected result is the package under `~/.local/snodec`, if you followed the local installation above.

This check becomes useful when a source change appears to have no effect. First rebuild and reinstall the framework into the selected prefix, then rebuild the consumer. If you intend to switch installations, use a fresh consumer build directory or explicitly correct its cached package location. Changing the source checkout alone does not change an already selected installed package.

::: {.snodec-checklist title="Environment checklist"}
Before moving on, you should be able to answer these questions.

- Can I clone the SNode.C repository?
- Can I configure an out-of-tree build?
- Can I compile the framework?
- Can I find built example executables?
- Can I run a server and a client in separate terminals?
- Do I understand the difference between the source directory, build directory, and install prefix?
- Do I know whether optional Bluetooth development files are installed?
- Do I know whether optional MariaDB development files are installed?
- Do I know whether I am using a local install prefix or a system-wide install?
- Do I have a separate playground project for later external experiments?

If the answer to these questions is yes, the environment is ready for the first program.
:::

::: {.snodec-remember title="What to remember"}
- Keep the source tree, build tree, install tree, and playground project separate; each has a different purpose.
- Use an out-of-tree build so generated files and compiled binaries do not obscure the source tree.
- A local install prefix makes external examples predictable because headers, libraries, and CMake package files live in one known place.
- Component names such as `net-in-stream-legacy` encode architectural position; public include paths such as `<net/in/stream/legacy/SocketServer.h>` encode the corresponding C++ source-facing entry point; `legacy` means the non-TLS stream connection variant.
- Runtime output is part of the learning process. Do not silence diagnostics before the first examples are understood.
- The environment is ready when the framework builds, example programs can be found and run, and an external playground project can consume the installed package.
:::
