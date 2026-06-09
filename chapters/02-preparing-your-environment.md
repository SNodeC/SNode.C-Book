## Preparing Your Environment

### Why the environment matters

Chapter 1 introduced SNode.C as a framework whose teaching value comes from visible structure: event-driven runtime behavior, explicit layers, named roles, and reusable application boundaries.

Before we can study that structure in code, the development environment must make it visible.

That may sound like a purely practical concern. It is not. For this book, the environment is part of the learning model. SNode.C is not a single-file demonstration library. It is a real C++ framework with a core runtime, network-family components, stream transports, legacy and TLS connection variants, higher protocol layers, example applications, generated CMake targets, installable package components, and optional support for technologies such as Bluetooth and MariaDB.

If the source tree, build tree, install prefix, and external playground are mixed together, the architecture becomes harder to see. If they are kept separate, the structure of the framework becomes much easier to inspect.

The goal of this chapter is therefore simple:

> Prepare a development setup that lets you build SNode.C, run examples, inspect the repository, and later compile small applications against installed SNode.C components.

This is not a general Linux installation guide. It does not try to cover every distribution, every package manager, every editor, or every cross-compilation target. The concrete commands assume a normal Linux development machine, with Debian-style package names where package installation is shown. The ideas transfer to other systems, but package names and installation commands may need adjustment.

### Three trees, three different purposes

During the book it helps to keep three locations mentally separate.

The first is the **book repository**.

That is where the manuscript lives. It contains the Markdown chapter files, part files, Pandoc build configuration, LaTeX-related metadata, and other book-specific project files.

The second is the **SNode.C framework repository**.

That is where the framework implementation lives. It contains the C++ source code, the CMake build system, the core runtime, network layers, protocol layers, database support, and example applications.

The third is a small **playground project**.

That is where you can later write small external applications that consume an installed SNode.C package without modifying the framework repository itself.

A useful layout is:

```text
projects/
  SNode.C-Book/
  snode.c/
  snodec-playground/
```

A separate build directory belongs beside these source trees, not inside them:

```text
projects/
  SNode.C-Book/
  snode.c/
  snode.c-build/
  snodec-playground/
```

This separation is not only tidy. It protects the reader from confusing generated files with source files, manuscript files with framework files, and local experiments with upstream examples.

The book explains the framework. The framework repository remains the source of truth for the implementation. The playground is where you can test your understanding.

### What the environment must support

For the first part of the book, the environment must support five activities.

First, it must allow us to **clone and build SNode.C**.

Second, it must allow us to **run small server and client examples**.

Third, it must allow us to **inspect the source tree and build tree separately**.

Fourth, it must allow us to **install the framework into a known prefix**.

Fifth, it must allow us to **compile small external programs against installed SNode.C components**.

Optional technologies should also be visible when available. Bluetooth RFCOMM and Bluetooth L2CAP require the appropriate BlueZ development files. MariaDB support requires MariaDB development files. These optional areas do not have to be used immediately, but the environment should not hide them accidentally.

### Compiler and CMake expectations

SNode.C is a modern C++ framework.

The build expects CMake and a C++20-capable compiler. A recent GCC or Clang installation is therefore the right baseline. On a Debian-style system, GCC 12 or newer and Clang 13 or newer are reasonable minimum expectations for the commands shown in this book.

Check the available tools first:

```sh
cmake --version
g++ --version
clang++ --version
```

Only one compiler is needed for normal work. It is useful to have both GCC and Clang installed, but the first examples do not depend on using both.

The important point is not compiler variety. The important point is avoiding old-toolchain problems. If the compiler is too old, the reader will spend time debugging the environment instead of learning the framework.

### Required and optional packages

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

`libbluetooth-dev` is relevant for Bluetooth RFCOMM and Bluetooth L2CAP.

`libmagic-dev` is relevant where file-type or content-type detection is used.

`libmariadb-dev` is relevant for MariaDB support.

Additional developer tools are useful later, especially during maintenance and review:

```sh
sudo apt install iwyu clang-format cmake-format doxygen
```

These tools are not required for the first echo example. They are mentioned here because SNode.C is a framework, and framework work eventually benefits from include checking, formatting, and documentation generation.

### Cloning the framework

Choose a directory where you keep source repositories:

```sh
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/SNodeC/snode.c.git
```

This creates:

```text
~/projects/snode.c/
```

The SNode.C framework repository uses `master` as its primary branch. Check the active branch with:

```sh
cd ~/projects/snode.c
git branch --show-current
```

If you already have a clone, update it before working through the examples:

```sh
git pull
```

For normal reading, do not edit the framework repository immediately. First learn where examples are located, how the build is organized, and which parts of the framework are source code, generated build output, or installation artifacts.

### Use an out-of-tree build

A build directory should be separate from the source directory.

This keeps generated files away from the code you want to read.

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

Using `cmake --build` is deliberate. It does not force the reader to care immediately whether the generator is Make, Ninja, or something else.

If you prefer Ninja explicitly, configure with:

```sh
cmake -S snode.c -B snode.c-build -G Ninja
cmake --build snode.c-build -j$(nproc)
```

The build can take some time. That is normal. SNode.C contains many components and example applications.

### Installing the framework

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

A system-wide installation is also possible:

```sh
sudo cmake --install snode.c-build
sudo ldconfig
```

Use a system-wide install only when you are comfortable installing development libraries into the system prefix.

For the book, a local prefix is often the safer teaching setup. It makes it clear which installation belongs to the experiments and avoids accidental interaction with other system packages.

### Build options worth knowing early

The first chapters do not require many CMake options.

Still, two logging-related options are useful to recognize early:

```text
SNODEC_DISABLE_LOGLEVEL_LOGGING
SNODEC_DISABLE_VERBOSE_LOGGING
```

These options can disable logging categories at compile time.

Do not disable logging while working through the first examples unless you have a specific reason. Early in the book, visible runtime output is useful. It helps connect the code you write with the runtime behavior you observe.

Later chapters will treat logging and configuration more carefully. At this stage, the important rule is simple:

> Do not make the first examples silent before you understand what they are doing.

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

The basic pattern for server/client examples is simple.

Open one terminal for the server.

Open another terminal for the client.

Start the server first.

Then start the client.

The echo pair in Chapter 3 uses this pattern. The server listens. The client connects and initiates the first message. Once both sides reflect received data, the program intentionally creates visible ping-pong behavior.

That behavior is useful for teaching. It proves that the runtime is active, the connection has been established, callbacks are executed, data is read, and data is written back.

To stop the example, interrupt one side with:

```text
Ctrl-C
```

The first time you run such an example, pay attention to the output. You are not only checking that the program works. You are learning how the framework makes runtime behavior visible.

### Do not hide runtime output too early

At the beginning, visible runtime output is your friend.

If an example logs that it is listening, connecting, connected, reading, writing, or disconnecting, that output is part of the learning process.

Later, logging can be configured more carefully. In the first chapters, however, do not silence the framework too aggressively.

A quiet program is not automatically a clean program. Sometimes it is only a program that has hidden the evidence you need for understanding.

### Preparing a separate playground project

Besides building the framework repository itself, it is useful to have a small external playground project.

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

### Components as installed architecture

When an external application consumes SNode.C, it asks CMake for package components.

For the first IPv4 legacy stream example, the relevant component is:

```cmake
find_package(snodec COMPONENTS net-in-stream-legacy)
```

The executable then links against the corresponding imported target:

```cmake
target_link_libraries(echoserver PRIVATE snodec::net-in-stream-legacy)
```

and similarly for the client.

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

Do not try to memorize all names at this stage. Learn the shape instead. SNode.C component names are a compact form of architectural information.

### Source tree, build tree, install tree

Before moving on, keep three locations distinct:

```text
source tree
  the files you read and edit

build tree
  generated files and compiled binaries

install tree
  headers, libraries, CMake package files, and installed executables
```

For example:

```text
~/projects/snode.c/
~/projects/snode.c-build/
~/.local/snodec/
```

This distinction will appear again throughout the book. It matters for CMake, for debugging, for deployment, and for understanding why an external playground project is different from an in-tree example.

### Environment checklist

Before moving on, you should be able to answer these questions.

Can I clone the SNode.C repository?

Can I configure an out-of-tree build?

Can I compile the framework?

Can I find built example executables?

Can I run a server and a client in separate terminals?

Do I understand the difference between the source directory, build directory, and install prefix?

Do I know whether optional Bluetooth development files are installed?

Do I know whether optional MariaDB development files are installed?

Do I know whether I am using a local install prefix or a system-wide install?

Do I have a separate playground directory for later external experiments?

If the answer to these questions is yes, the environment is ready for the first program.

### Closing perspective

A good development environment is not only about making the compiler happy.

It shapes how the reader thinks.

If the source tree, build tree, install prefix, examples, and playground are clearly separated, the framework becomes easier to understand. If everything is mixed together, even simple questions become confusing.

Chapter 1 introduced the architectural reason for studying SNode.C. This chapter prepared the practical ground on which that architecture can be inspected.

The next chapter uses this environment to build the first concrete program: an echo server and an echo client.

The example will be small.

But it will already expose the recurring shape of SNode.C applications.
