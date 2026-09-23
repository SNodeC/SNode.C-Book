## The Express-Like Framework {#the-express-like-framework}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Trace a ready request through controller, mounted router and handler.
- **O2.** Diagnose continuation and short-circuit behavior from responses and handler visits.
- **O3.** Decide where shared routing, validation and resource policy belongs.
:::

\index{Express-like framework}
\index{web application framework}
\index{routing}

### From HTTP messages to application structure

HTTP messages are no longer handled only by an HTTP request-ready callback; the Express-like layer organizes them through routers, routes, middleware chains, request/response facades, and explicit continuation.

\index{Express-like framework!layered model}

HTTP provides message meaning; Express organizes application handling above it.

Follow one request through the complete local fixture before reading the class composition. The application mounts a router under `/api`. Both the application and router add middleware, and the router supplies a `/status` handler. The same fixture also provides a deliberately blocked path.

<!-- snodec-source: companion/exercises/ch18/dispatch.cpp -->
```cpp
// A synchronous test route tree: observations belong to one sequential request.
#include <express/legacy/in/WebApp.h>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    express::WebApp::init(argc, argv);
    const express::legacy::in::WebApp app("lab");
    const express::Router router;
    std::string trace;
    app.use([&](const auto& req, const auto&, express::Next& next) {
        trace = "app-before";
        std::cout << "APP " << req->originalUrl << std::endl;
        next();
    });
    app.use("/blocked", [](const auto&, const auto& res, express::Next&) {
        std::cout << "STOP" << std::endl;
        res->status(403).set("X-Trace", "app-before,stop").send("middleware stopped request");
    });
    app.get("/blocked", [](const auto&, const auto& res) {
        std::cout << "UNEXPECTED-HANDLER" << std::endl;
        res->send("unreachable");
    });
    router.use([&](const auto&, const auto&, express::Next& next) {
        trace += ",router-before";
        std::cout << "ROUTER" << std::endl;
        next();
    });
    router.get("/status", [&](const auto&, const auto& res) {
        trace += ",handler";
        std::cout << "HANDLER" << std::endl;
        res->set("X-Trace", trace).send(trace);
    });
    app.use("/api", router);
    app.listen([](const auto&, const auto&) {});
    return express::WebApp::start();
}
```

For `GET /api/status`, application middleware first records `app-before` and calls `next()`. The `/api` mount then selects the router, whose middleware appends `router-before` and continues. Its `/status` handler appends `handler` and sends the completed trace. The response body and `X-Trace` header therefore expose the path `app-before,router-before,handler`; status 200 alone would not establish that order.

For `GET /blocked`, application middleware still runs first. The next matching middleware sends 403 and deliberately does not continue. The subsequent `/blocked` handler is unreachable on that path. Returning from the middleware does not implicitly call `next()`. The fixture's `UNEXPECTED-HANDLER` output would reveal a violation even if another response looked plausible.

The shared trace variable is suitable for this bounded fixture's sequential requests and synchronous dispatch. It is not a template for storing unrelated requests' state in one global buffer. Keep that testing assumption separate from the reusable route tree: the routes are long-lived, while each request has its own dispatch and response.

A ready HTTP request enters a `Controller`, then the root route dispatches it through routers, middleware and handlers:

| Concern | HTTP layer | Express-like layer |
|---|---|---|
| application-facing unit | request / response | routed request / response flow |
| primary callback | request ready | route handler or middleware |
| structure | one HTTP protocol endpoint | application route tree |
| flow control | HTTP lifecycle | dispatcher chain and `next()` |
| path meaning | HTTP target/path | mount path, route path, params, base/original URL |
| response surface | HTTP response | application-oriented response facade |
| reuse mechanism | HTTP server/client wrappers | routers and middleware |
| lower layers | still present | still present underneath HTTP |

\index{Express-like framework!semantics}
\index{WebApp@\texttt{WebApp}}
\index{WebAppT@\texttt{WebAppT}}
\index{HTTP server}

“Express-like” names the C++ programming model, not an embedded Node.js or JavaScript Express runtime. Familiar routing and middleware still use SNode.C’s connection, configuration and event-driven runtime.

The core composition is visible in two steps.

First, `WebApp` is router-shaped:

```cpp
class WebApp : public Router {
    // runtime-facing lifecycle surface
};
```

Second, `WebAppT` joins that application shape with a concrete HTTP server type:

```cpp
template <typename ServerT>
class WebAppT
    : public WebApp
    , public ServerT {
    // bridge from HTTP request readiness to Express dispatch
};
```

This composition explains how HTTP request handling becomes Express-like application flow.

| Type | Role |
|---|---|
| `Router` | route tree and middleware structure |
| `WebApp` | router-shaped application plus runtime-facing lifecycle |
| `ServerT` | concrete HTTP server type underneath |
| `WebAppT<ServerT>` | combined Express-like application surface and HTTP server handle |

`WebApp` also exposes runtime-facing lifecycle operations such as:

- `init(...)`,
- `start(...)`,
- `stop()`,
- `tick(...)`,
- `free()`,
- `state()`,
- `reconfigure()` while the runtime is running, with the configuration boundaries from Chapter 13.

`WebAppT<ServerT>` is the joining point. It inherits the router-shaped `WebApp` surface and the concrete HTTP server type. When the HTTP server reports a ready request, `WebAppT` wraps that request/response pair in a `Controller` and dispatches it into the root route.

The concrete alias is not the main point; it is an example of the general pattern. An IPv4 legacy Express-like web application can be shaped as:

```cpp
using WebApp = WebAppT<web::http::legacy::in::Server>;
```

The SNode.C source also provides the corresponding convenience alias:

```cpp
express::legacy::in::WebApp
```

The same idea applies to other network-family and connection-handling variants where provided.

Follow the ready-request callback in `WebAppT` into its controller construction, then into root-route dispatch. This is the source trace behind the composition above. It separates the lifetime of one request’s dispatch from the longer lifetime of the application’s route tree.

The HTTP layer has parsed the request and prepared a response object. The Express-like layer now decides which application structure should handle that request. That decision belongs above HTTP because it depends on route paths, mounted routers, middleware, and routing policy.

The `Controller` is the dispatch-time object that carries the Express request/response facades through the route tree and tracks continuation state such as `next`, next route, and next router.

### Router as the application composition unit

\index{Router@\texttt{Router}}
\index{routes}
\index{mounted routers}
\index{middleware}

`Router` composes handlers, middleware and mounted routers. A route connects request properties to application behavior; a mounted router groups related paths, and middleware supplies shared behavior without copying it into every handler.

At this layer, route matching is part of application correctness. The router exposes policy controls such as:

| Policy | Question |
|---|---|
| strict routing | Are `/x` and `/x/` distinct? |
| case-insensitive routing | Should route matching ignore case? |
| merge params | Should mounted routers receive parent params? |

These policies belong to the router. They are not socket concerns and not generic HTTP parsing concerns. They are web-application routing concerns.

`merge params` is a good example. It decides how parameter information moves through nested router structures. That is meaningful only once the application has routers and mount points.

### Application callbacks and middleware callbacks

\index{application callbacks}
\index{middleware callbacks}
\index{Next@\texttt{Next}}

An application handler typically answers a matched request. Middleware may inspect, modify, authorize, log, parse or serve before deciding whether to answer or call `next()`. Returning from middleware does not itself continue the chain.

`Next` is the application-visible continuation object for the dispatcher chain, not a scheduler or thread handoff.

\index{dispatcher}
\index{routing dispatch}

The user-facing API is built on internal dispatcher roles.

The dispatchers encode the fact that application callbacks, middleware callbacks, and mounted routers have different control-flow meanings.

When a request stops advancing, inspect which dispatcher owns its continuation. A middleware return and a call to `next()` are different actions; neither is an instruction to move work to another thread.

### Request and Response as web-application facades

\index{Request@\texttt{Request}}
\index{Response@\texttt{Response}}
\index{facade}

The Express facades retain HTTP message access and add routing context and application-oriented operations.

The Express-like `Request` adds routing and application context to the lower HTTP request.

The Express-like `Response` adds application-oriented response operations to the lower HTTP response.

The facade raises the application API, but it does not hide all lower HTTP capabilities. Advanced operations remain available when the application genuinely needs them.

\index{middleware}
\index{static serving}
\index{virtual hosts}
\index{JSON middleware}
\index{authentication middleware}

These deliberate access points keep advanced HTTP and connection behavior available without making it every route’s responsibility.

The Express-like module also provides reusable middleware. Built-in middleware packages common request-processing behavior so it can be mounted once and reused across routes.

Static serving may involve root directories, index handling, fall-through behavior, headers, cookies, and connection-state decisions after the response. Those are practical application concerns, but they do not belong in the socket layer or in every route handler.

`VHost` belongs here because host-based dispatch is web-application routing behavior. `VerboseRequest` belongs here because request visibility is useful across routes but should not be duplicated inside every handler.

The Express module includes JSON middleware when the required `nlohmann_json` dependency is present; the build treats that dependency as required for this module. Architecturally, JSON middleware belongs to the same group of reusable request-processing behavior.

Bind/listen activation, TLS setup, HTTP parsing, timeout boundaries and shutdown still belong to the underlying runtime. Routing organizes the application work above those responsibilities.

::: {.snodec-note title="Routing API reference"}
| Need | Surface |
|---|---|
| Mount or match | `use`, `all`, `get`, `put`, `post`, `del`, `connect`, `options`, `trace`, `patch`, `head` |
| Answer or continue | `(req, res)` handler; `(req, res, next)` middleware with explicit continuation |
| Internal dispatch | `ApplicationDispatcher`, `MiddlewareDispatcher`, `RouterDispatcher` invoke those distinct participants |
| Inspect routed input | `baseUrl`, `path`, `file`, `params`, `param`, `originalUrl`, `originalPath`; HTTP metadata, query, cookies and body |
| Construct output | `status`, `set`, `append`, `type`, `cookie`, `clearCookie`, `send`, `json`, `end` |
| Specialized output | `sendFile`, `download`, `attachment`, `redirect`, `location`; upgrade, fragments and socket-context access |
| Reuse middleware | `BasicAuthentication`, `StaticMiddleware`, `VHost`, `VerboseRequest`, `JsonMiddleware` |
:::

### Observe continuation and a completed response

The public fixture in `companion/exercises/ch18/` provides both dispatch experiments below. Both observe loopback responses and handler visits. Corresponding optional framework tests can be selected with:

```sh
ctest --test-dir "$SNODEC_BUILD" --output-on-failure \
  -R '^InetExpressMiddleware(MountOrder|ShortCircuit)Test$'
```

Here `SNODEC_BUILD` is a configured and built framework test tree, as established in Chapter 29. These tests require local socket access. Their source files live in `tests/component/express`.

Read the companion `dispatch.cpp` mount-order path first; `InetExpressMiddlewareMountOrderTest.cpp` is its optional framework counterpart. Application middleware records `app-before` and calls `next()`. Router middleware appends `router-before` and calls `next()`. The router’s `/status` handler appends `handler`; the router is mounted at `/api`.

| Request | Expected observation |
|---|---|
| `GET /api/status` | status 200; response header and body contain `app-before,router-before,handler` |
| `GET /outside` | status 404; application middleware runs, but the mounted router and its handler do not |

The test counts those visits. A 200 response alone would not prove that middleware ran in the intended order.

The companion’s `/blocked` path demonstrates short-circuiting. Its optional framework counterpart is `InetExpressMiddlewareShortCircuitTest.cpp`. The middleware sends status 403, a diagnostic header, and `middleware stopped request`. It does not call `next()`. The following application handler would send 200, but its invocation count must remain zero. This is a deliberate response that ends dispatch, not an HTTP parsing error or a failed connection.

For a local experiment, work in a scratch copy of the test. Change the middleware to call `next()` without sending its 403 response, and predict the new response and counts before changing the assertions. Then restore the original. Do not leave both `send(...)` and unconditional continuation in place: that expresses two competing decisions about who answers the same request.

A flat request callback remains reasonable for one small endpoint. Mounted routers become useful when several endpoints share policy or path context. Their cost is less visible control flow: route order, mount paths, and explicit continuation become part of correctness. The paired response and invocation observations keep that cost visible.

\index{Express components}
\index{WebApp@\texttt{WebApp}!public surface}

::: {.snodec-note title="Build note"}
A file that directly uses the IPv4 legacy Express WebApp includes:

```cpp
#include <express/legacy/in/WebApp.h>
```

Code using the convenience server helpers includes:

```cpp
#include <express/legacy/in/Server.h>
```

The corresponding composed stream component is:

```text
http-server-express-legacy-in
```

It selects the Express layer together with the IPv4 legacy stream connection. The source-side and build-side names rhyme without being the same mechanism. Chapter 27 gives the source-derived matrix for the broader set of components and headers.
:::

Chapter 19 extends this routing model to a long-lived, one-way event response. Its observer lifetime needs more than the completed-response examples here.

::: {.snodec-remember title="What to remember"}
- `WebAppT<ServerT>` joins a root router and concrete HTTP server; request readiness starts controller dispatch.
- Mounted paths, route order and parameter policy affect which handler receives a request.
- Middleware may answer or continue explicitly; `next()` is not a thread handoff.
- Facades add routing context and common responses while keeping deliberate access to lower HTTP operations.
- Observe both the completed response and handler visits when checking dispatch or short-circuit behavior.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** How do `WebApp`, `WebAppT` and `Controller` connect the route tree to the runtime?
2. **Review (O2, O3).** Contrast returning from middleware, calling `next()` and sending a response. Why should a handler not send and then continue unconditionally?
3. **Lab (O1, O2).** Run the mount-order lab. Compare `/api/status` with `/outside`: expect ordered app/router/handler visits for 200, but only app middleware for 404.
4. **Lab (O2).** Run the short-circuit lab. Expect middleware’s 403 response and zero visits to the following handler.
5. **Design (O1, O3).** Place shared authentication, JSON handling and a mounted sensor API. Explain route order, parent parameters and which limits must act before middleware.

Public solutions and bounded lab commands: `companion/exercises/ch18/README.md`.
:::
