# MariaDB-Minimal

Compact MariaDB client example used by Chapter 28.

The example is intended to compile as a SNode.C consumer application. Running it
requires a reachable MariaDB server and a schema such as the one shown in the
chapter.

Build with an installed SNode.C package:

```bash
cmake -S . -B build -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build
```
