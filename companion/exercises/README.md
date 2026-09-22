# Public exercises and solutions

These are the public solutions for the five sample chapters. Each chapter has a
review answer, an observable lab, and a design discussion. Try the exercise before
reading its solution. `O1`–`O3` refer to the objectives printed at the chapter opening;
exercise 1 covers O1, exercise 2 covers O2, and exercise 3 covers O3.

Use the installed SNode.C environment prepared in Chapter 2. Add standalone Asio
headers (`libasio-dev` on Debian/Ubuntu) for the Chapter 1 comparison. No broker,
database, hardware, or framework source build is required by these labs.

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

Each chapter README gives a focused build target and test command. Chapter 1, 23,
and 35 labs build the canonical companion programs, then use Python's standard
library to make observations at their public socket/HTTP interfaces. Chapter 3
adds a client with a changed greeting while inheriting the existing reflection
behavior. Chapter 37 compiles the canonical `MeasurementModel.cpp` into a small
experiment. There is only one implementation of each reused algorithm.

The lab peers bind loopback and choose unused ports. Each process gets temporary
configuration, is stopped on success or failure, and has a bounded test duration.
Set `SNODEC_PREFIX` to the installation actually used to link the programs; the
Python harness uses it to find runtime libraries. A failed lab prints process
output, and CTest retains the test transcript in `build/labs/Testing/Temporary/`.
These checks require permission to open local sockets.
