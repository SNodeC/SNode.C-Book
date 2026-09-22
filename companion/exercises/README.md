# Public exercises and solutions

These are the public solutions for Parts I–VI and the later sample chapters. Each chapter has two
review answers, two observable labs, and a design discussion. Try the exercise before
reading its solution. `O1`–`O3` refer to the objectives printed at the chapter opening;
each exercise and solution identifies its objective explicitly.

Use the installed SNode.C environment prepared in Chapter 2. Add standalone Asio
headers (`libasio-dev` on Debian/Ubuntu) for the Chapter 1 comparison. The mandatory labs need no broker, database, radio hardware, or framework source build. The Bluetooth selector lab needs installed Bluetooth components and development support; its optional physical RFCOMM extension is an equipped lab. IPv6 loopback must be available for the IP-family comparison.

From the book repository root:

```sh
export SNODEC_PREFIX="$HOME/.local/snodec"
cmake -S . -B build/labs \
  -DSNODEC_BOOK_BUILD_PDFS=OFF \
  -DSNODEC_BOOK_BUILD_COMPANION_EXAMPLES=ON \
  -DCMAKE_PREFIX_PATH="$SNODEC_PREFIX"
cmake --build build/labs --parallel 2
ctest --test-dir build/labs --output-on-failure
```

Each chapter README gives a focused build target and test command. Chapters 1, 18 and 28 labs build the canonical companion programs, then use Python's standard
library to make observations at their public socket/HTTP interfaces. The environment labs build EchoPair as an independent installed-package consumer
and diagnose an intentionally missing component in a temporary copy. Chapter 3
adds a client with a changed greeting while inheriting the existing reflection
behavior, then checks independent measurement peers for the Part I checkpoint. Chapter 28 also isolates JSON validation before acceptance; Chapter 30 compiles
the canonical `MeasurementModel.cpp` into two ownership experiments. There is only one implementation of each reused algorithm.

The architecture labs reuse the existing measurement-model experiments and EchoPair
peer harness; the runtime lab separately checks deferred callbacks through the installed
public API. The Part II checkpoint needs no transport or external service.

Part III compiles thin family drivers around the same EchoPair context and factory,
checks IP and Unix identities/cleanup, and constructs Bluetooth service selectors
without opening a radio socket.

Part IV reuses the canonical line protocol to compare framing, fresh parser state,
construction refusal and IPv4/Unix transfer through bounded independent peers.

Part V reuses EchoPair and SemanticLogging for isolated configuration inspection,
scoped errors and a reproducible runtime/logging checkpoint.

Part VI adds the OpenSSL command-line tool, installed TLS components and Python's
standard-library TLS support. Temporary certificates exercise trust and expected
identity; EchoPair supplies secure echo and controlled retry/reconnect observations.
The fixtures generate and remove their own private keys and need no external CA.

The lab peers bind loopback and choose unused ports. Each process gets temporary
configuration, is stopped on success or failure, and has a bounded test duration.
Set `SNODEC_PREFIX` to the installation actually used to link the programs; the
Python harness uses it to find runtime libraries. A failed lab prints process
output, and CTest retains the test transcript in `build/labs/Testing/Temporary/`.
These checks require permission to open local sockets.
