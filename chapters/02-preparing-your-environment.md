## Preparing Your Environment

### Why the environment matters

Chapter 1 explained why SNode.C is worth studying.

Before we write and inspect code, we need a working environment.

That may sound like a purely practical step, but for this book it has an architectural meaning. SNode.C is not a single-header demonstration library. It is a real C++ framework with multiple layers, optional components, generated targets, example applications, and installable CMake package components.

If the environment is unclear, every later chapter becomes harder than necessary.

The goal of this chapter is therefore simple:

> Prepare a development setup that lets you build SNode.C, run examples, inspect the repository, and later compile small applications against the framework.

This chapter is not a full operating-system installation guide. It also does not try to cover every Linux distribution, every package manager, or every cross-compilation target.

Instead, it gives the reader a clean baseline.

The assumed path is a normal Linux development machine, preferably Debian-style for the concrete package examples. The concepts transfer to other distributions, but the package names and commands may need adjustment.

### Two source trees, two different purposes

During this book, it helps to keep two source trees mentally separate.

The first source tree is the **book repository**.

That is where the manuscript lives. It contains the Markdown files, the part files, the Pandoc build structure, and the book-specific project files.

The second source tree is the **SNode.C repository**.

That is where the framework lives. It contains the C++ implementation, the CMake build system, the core runtime, the network layers, protocol layers, and example applications.

A reader may have both trees side by side:

```text
projects/
  SNode.C-Book/
  snode.c/
```

This is a good habit.

Do not mix manuscript files into the framework repository.

Do not put experimental framework changes into the book repository.

The book explains the framework. The framework repository remains the source of truth for the code.

### What this environment must support

For the first part of the book, the environment must support five activities.

First, it must allow us to **clone and build SNode.C**.

Second, it must allow us to **run small server and client examples**.

Third, it must allow us to **inspect the generated build tree** without confusing it with the source tree.

Fourth, it must allow us to **compile small applications against installed SNode.C components**.

Fifth, it should make optional lower layers visible, especially Bluetooth RFCOMM and Bluetooth L2CAP when BlueZ development files are available.

This last point is important. Bluetooth does not have to be used immediately, but the environment should not hide it accidentally.

### Compiler and CMake expectations

SNode.C is a modern C++ framework.

The current build system expects CMake and a C++20-capable compiler. The top-level build requires CMake 3.18 or newer, and the `src` build configures the project as C++20.

The most important compiler expectations are:

- GCC 12.2 or newer,
- or Clang 13.0 or newer.

This is not an arbitrary preference.

SNode.C uses modern C++ internally. Building it with an older compiler is not a good way to learn the framework. If the compiler is too old, the reader will spend time fighting toolchain problems instead of understanding architecture.

A quick check is useful:

```sh
cmake --version
g++ --version
clang++ --version
```

It is fine if only one of GCC or Clang is used, as long as it satisfies the required version.

### Required and optional dependencies

The exact package names differ between Linux distributions, but the categories are stable.

For a Debian-style development system, the usual baseline tools are:

```sh
sudo apt update
sudo apt install git cmake make ninja-build g++ clang pkg-config
```

The framework also relies on development libraries.

For the core build path, install:

```sh
sudo apt install libssl-dev nlohmann-json3-dev
```

Useful optional dependencies are:

```sh
sudo apt install libbluetooth-dev libmagic-dev libmariadb-dev
```

These optional libraries matter because they unlock additional framework areas.

`libbluetooth-dev` is relevant for Bluetooth RFCOMM and Bluetooth L2CAP.

`libmagic-dev` is relevant where content or file-type detection is used.

`libmariadb-dev` is relevant for MariaDB database support.

Additional developer tools are helpful but not necessary for the first examples:

```sh
sudo apt install iwyu clang-format cmake-format doxygen
```

These tools support formatting, include analysis, and documentation generation. They are useful later, but they are not the central learning goal of the first chapters.

### Cloning the framework

Choose a directory where you keep source repositories.

For example:

```sh
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/SNodeC/snode.c.git
```

This creates:

```text
~/projects/snode.c/
```

The current SNode.C source repository uses `master` as the primary branch.

Check the branch with:

```sh
cd ~/projects/snode.c
git branch --show-current
```

If you already have a clone, update it before working through the book:

```sh
git pull
```

For normal reading, do not edit the framework repository immediately. First learn how it is organized and how it builds.

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

Using `cmake --build` is preferable in a book because it does not force the reader to care immediately whether the backend is Make or Ninja.

If you prefer Ninja explicitly, configure with:

```sh
cmake -S snode.c -B snode.c-build -G Ninja
cmake --build snode.c-build
```

The build can take some time. This is normal. The framework uses many templates and builds many components and examples.

### Installing the framework

For experimenting inside the source tree, installation is not always necessary.

For building separate applications against SNode.C using `find_package(snodec ...)`, installation is useful.

A local user installation avoids touching system directories:

```sh
cmake -S snode.c -B snode.c-build \
  -DCMAKE_INSTALL_PREFIX="$HOME/.local/snodec"

cmake --build snode.c-build -j$(nproc)
cmake --install snode.c-build
```

When using a custom prefix, later projects may need to know where to find the package:

```sh
export CMAKE_PREFIX_PATH="$HOME/.local/snodec:$CMAKE_PREFIX_PATH"
```

A system-wide installation is also possible:

```sh
sudo cmake --install snode.c-build
sudo ldconfig
```

Use a system-wide install only when you are comfortable with installing development libraries into the system prefix.

### Build options worth knowing early

The first chapters do not require many CMake options.

Still, two logging-related options are useful to know:

```text
SNODEC_DISABLE_LOGLEVEL_LOGGING
SNODEC_DISABLE_VERBOSE_LOGGING
```

These can disable logging categories at compile time.

For this book, logging is useful because it makes runtime behavior visible. Therefore, do not disable verbose or log-level logging while learning the first examples unless you have a specific reason.

The first examples benefit from seeing what happens.

### Finding built executables

Build trees differ slightly depending on generator and configuration. Rather than memorizing one exact path, learn how to search for built example executables.

From the build directory:

```sh
find . -type f -executable -name '*echo*'
```

or more generally:

```sh
find . -type f -executable | grep apps
```

This is often more robust than assuming one fixed path.

When later chapters refer to repository examples, the important point is not the exact build-tree location. The important point is that the source lives under the repository and the executable appears somewhere in the build tree.

### Running server and client programs

The basic pattern for server/client examples is always similar.

Open one terminal for the server.

Open another terminal for the client.

Start the server first.

Then start the client.

For the echo pair developed in Chapter 3, the server listens and the client initiates the first message. Once both sides reflect received data, the program intentionally creates visible ping-pong behavior.

That behavior is useful for teaching.

It proves that the runtime is active, the connection has been established, the context callbacks are executed, data is read, and data is written back.

To stop the example, interrupt one side with `Ctrl-C`.

### Do not hide runtime output too early

At the beginning, visible runtime output is your friend.

If an example logs that it is listening, connecting, connected, reading, writing, or disconnecting, that output is part of the learning process.

Later, logging can be configured more carefully. In the first chapters, however, do not silence the framework too aggressively.

A quiet program is not always a clean program. Sometimes it is only a program that has hidden the evidence you need for understanding.

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

A minimal playground structure might look like:

```text
snodec-playground/
  CMakeLists.txt
  EchoSocketContext.h
  EchoSocketContext.cpp
  echoserver.cpp
  echoclient.cpp
```

The CMake side of a separately built application will later use package components. For the first IPv4 legacy stream example, the relevant package component is:

```cmake
find_package(snodec COMPONENTS net-in-stream-legacy)
```

and executables link against:

```cmake
snodec::net-in-stream-legacy
```

This is enough for the first external echo-style experiments.

### Understanding components without memorizing all of them

SNode.C is componentized.

The component name tells you which part of the framework you are asking CMake to provide.

For example:

```text
net-in-stream-legacy
```

can be read as:

```text
network family: IPv4 / in
transport:      stream
connection:     legacy
```

Later you will see names for IPv6, Unix domain sockets, Bluetooth RFCOMM, Bluetooth L2CAP, TLS, HTTP, WebSocket, MQTT, and database support.

Do not try to memorize all component names now.

Instead, learn the shape of the naming:

```text
layer-family-transport-mode
```

or, for higher layers:

```text
protocol-role-transport
```

The names are not random. They encode architecture.

### Environment checklist

Before moving on, the reader should be able to answer these questions.

Can I clone the SNode.C repository?

Can I configure an out-of-tree build?

Can I compile the framework?

Can I find built example executables?

Can I run a server and a client in separate terminals?

Do I understand the difference between the source directory and the build directory?

Do I know whether optional Bluetooth development files are installed?

Do I know whether I am using a local install prefix or a system-wide install?

If the answer to these questions is yes, the environment is ready for the first program.

### Closing perspective

A good development environment is not only about making the compiler happy.

It shapes how the reader thinks.

If the source tree, build tree, install prefix, examples, and playground are clearly separated, the framework becomes easier to understand. If everything is mixed together, even simple questions become confusing.

The next chapter uses this prepared environment to build the first concrete program: an echo server and an echo client.

That example will be small.

But it will already expose the recurring shape of SNode.C applications.
