# Chapter 25 — solutions and discussion

## 1. Review (O1)

In-tree targets use local names; installed consumers resolve exported `snodec::`
targets and installed public headers. Source includes identify directly named C++
abstractions. The link line selects components such as the protocol/application
layer and concrete carrier. Their targets propagate the deeper dependency graph.
Copying every internal dependency into an application's link list makes the
application responsible for implementation details it does not own.

## 3. Lab (O1)

Use [the common configuration](../README.md), then inspect the public route fixture
at `../ch18/CMakeLists.txt` and `../ch18/dispatch.cpp`. Its single imported Express
carrier component supplies the public protocol and concrete carrier; initialization,
middleware/routes, listener activation and runtime start form its composition root.
Find the handlers that append `app-before`, `router-before` and `handler`.

```sh
cmake --build build/labs --target ch25-lab
ctest --test-dir build/labs -R '^exercise-ch25-composition$' --output-on-failure -V
```

This reuses the earlier public HTTP framing observer unchanged. A request missing
its final blank line produces neither a response nor an application marker during
200 ms. Completing it produces HTTP 200 and the expected handler order. Relate the
observation to the build/entry-point trace: the application registers behavior,
while the installed parser admits the completed request. This is a local reading
and execution exercise; it does not execute every program in `src/apps`.


TODO(P3-apparatus)
