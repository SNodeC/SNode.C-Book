# CMake listings highlighting infrastructure

This is an infrastructure-only update for the Markdown -> Pandoc -> XeLaTeX book build.

## What it changes

- Adds a custom `SNodeCCMake` listings language in `metadata.yaml`.
- Changes `snodec-cmake` from a plain-text style to a real CMake highlighting style.
- Updates `filters/snodec-listings.lua` so fenced blocks such as:

```markdown
```cmake
cmake_minimum_required(VERSION 3.20)
project(example CXX)
add_executable(example main.cpp)
target_link_libraries(example PRIVATE snodec::core)
```
```

are mapped to `style=snodec-cmake` without requiring chapter changes.

## Files changed

- `metadata.yaml`
- `filters/snodec-listings.lua`

No chapter Markdown files need to be changed as long as CMake snippets already use the `cmake` fence class.
