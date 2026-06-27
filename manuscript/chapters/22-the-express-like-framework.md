## The Express-Like Framework

\index{Express-like framework}
\index{web application framework}
\index{routing}


### From HTTP messages to application structure

Chapter 21 showed how SNode.C raises stream communication to HTTP request and response objects. Chapter 22 moves one level higher: HTTP messages are no longer handled only by an HTTP request-ready callback, but by a web-application structure made of routers, routes, middleware chains, request/response facades, and explicit continuation.

That is the central idea of this chapter:

::: {.snodec-rule title="Express-layer rule"}
The Express-like layer does not replace HTTP; it organizes HTTP handling into application structure.
:::

The lower stack remains visible:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response layer
              -> Express-like application layer
```

The Express-like layer is therefore not a different universe. It is the application-organization layer above HTTP. HTTP gives message meaning; the Express-like layer gives application structure.

Part VII now moves in steps. Chapter 21 introduced HTTP messages. Chapter 22 shows how those messages become routed application flow. Chapter 23 will keep that web-application structure, but change the temporal shape of a handler: instead of answering once, a route may keep an HTTP response open and emit events over time.

### The Express-like layer in the layered SNode.C model

\index{Express-like framework!layered model}


The stack now reads:

```text
runtime
  -> registered server instance
      -> lower communication family
          -> stream transport
              -> legacy or TLS connection handling
                  -> HTTP request / response
                      -> Express-like routing and middleware
```

The visible `WebAppT<ServerT>` object in application code is the application-side handle. Through that handle, the application configures a server-side communication role and registers a runtime-visible server instance. The Express-like layer does not change that model; it changes what happens when a ready HTTP request reaches application code.

Earlier chapters established the lower parts. Chapter 21 introduced HTTP request and response semantics. Chapter 22 now asks what happens when HTTP handling becomes application structure. The answer is:

```text
HTTP request ready
  -> Controller(req, res)
      -> root route dispatch
          -> router / middleware / application handler
```

This is the transition from protocol handling to web-application composition.

### HTTP messages and Express-like application flow side by side

A compact comparison makes the new layer visible.

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

The HTTP layer gives the application request and response objects. The Express-like layer gives the application a way to organize what should happen with them.

### What “Express-like” means here

\index{Express-like framework!semantics}


“Express-like” does not mean that SNode.C embeds Node.js or the JavaScript Express runtime. It means that the C++ web-application layer uses a familiar application model:

- `WebApp`,
- `Router`,
- `.use()`,
- `.get()`, `.post()`, and other HTTP verb methods,
- middleware callbacks,
- `Next`,
- mounted routers,
- request and response facades,
- built-in middleware.

The layer is Express-like in its programming model. It is still SNode.C in its runtime, connection, configuration, diagnostics, and lower-layer architecture.

This distinction matters because the familiar surface should not hide the underlying model. A SNode.C Express-like application is still carried by an application-side web-app/server handle, a registered server instance, an HTTP server layer, legacy or TLS connection handling, lower-family choices, configuration, diagnostics, timing, and failure behavior.

### WebApp, WebAppT, and the HTTP server below

\index{WebApp@\texttt{WebApp}}
\index{WebAppT@\texttt{WebAppT}}
\index{HTTP server}


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

The result is not a separate web runtime. It is a web-application surface joined to a concrete HTTP server.

#### WebApp as router-shaped application

`WebApp` derives from `Router`. Because `WebApp` is router-shaped, the application root is not a separate routing concept. The application itself is the root router, and `WebAppT` makes that root router runnable by combining it with a concrete HTTP server.

`WebApp` also exposes runtime-facing lifecycle operations such as:

- `init(...)`,
- `start(...)`,
- `stop()`,
- `tick(...)`,
- `free()`,
- `state()`.

This keeps the web-application layer connected to the same event-driven runtime story introduced earlier in the book. A web application is a route structure that still runs inside the SNode.C runtime, not a loose set of route functions.

#### WebAppT as the bridge to a concrete HTTP server

`WebAppT<ServerT>` is the joining point. It inherits the router-shaped `WebApp` surface and the concrete HTTP server type. When the HTTP server reports a ready request, `WebAppT` wraps that request/response pair in a `Controller` and dispatches it into the root route.

The concrete alias is not the main point; it is an example of the general pattern. An IPv4 legacy Express-like web application can be shaped as:

```cpp
using WebApp =
    WebAppT<web::http::legacy::in::Server>;
```

The SNode.C source also provides the corresponding convenience alias:

```cpp
express::legacy::in::WebApp
```

The same idea applies to other lower-family and connection-handling variants where provided.

The pattern is:

```text
Express-like WebAppT
  + concrete HTTP server
      -> runnable web application
```

This matches the design pattern from Chapter 21. The HTTP layer remains underneath; the Express-like layer organizes application behavior above it.

#### From HTTP request readiness to Express dispatch

The key bridge is the moment when HTTP request readiness enters the Express-like routing structure.

Conceptually:

```text
HTTP request ready
  -> Controller(req, res)
      -> root route dispatch
          -> application callback / middleware / mounted router
```

The HTTP layer has parsed the request and prepared a response object. The Express-like layer now decides which application structure should handle that request. That decision belongs above HTTP because it depends on route paths, mounted routers, middleware, and routing policy.

The `Controller` is the dispatch-time object that carries the Express request/response facades through the route tree and tracks continuation state such as `next`, next route, and next router.

### Router as the application composition unit

\index{Router@\texttt{Router}}
\index{routes}
\index{mounted routers}
\index{middleware}


`Router` is the main composition unit of the Express-like layer. It lets a web application be assembled from parts instead of being written as one large request callback.

A router can contribute:

- route handlers,
- middleware,
- mounted routers,
- method-specific behavior,
- routing policy.

The routing surface includes familiar methods such as:

- `.use()`,
- `.all()`,
- `.get()`,
- `.put()`,
- `.post()`,
- `.del()`,
- `.connect()`,
- `.options()`,
- `.trace()`,
- `.patch()`,
- `.head()`.

The method list matters because each method attaches structure to the route tree. The point is not that there are many methods; it is that routing, middleware, and mounted routers become composable:

```text
application
  -> router
      -> route
      -> middleware
      -> mounted router
```

#### Routes, mounted routers, and middleware

A route is a point where request properties and application behavior meet. A mounted router lets a larger application be built from smaller route structures. Middleware lets common behavior be placed into the request flow without duplicating it in every handler.

Together, these ideas move the application from:

```text
one request callback
```

to:

```text
structured request processing
```

That is the main application-level gain of the Express-like layer.

#### Routing policy

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


The Express-like layer distinguishes two important callback shapes.

| Callback shape | Meaning |
|---|---|
| `(req, res)` | application handler; may produce a response |
| `(req, res, next)` | middleware participant; may continue the chain |

This distinction teaches the layer model clearly. Not every function attached to a route has the same responsibility. Some handlers answer. Some middleware participates in a chain. Some middleware may inspect, modify, authorize, log, or prepare state before passing control onward.

#### Application handlers

An application handler receives a request and a response. Its typical responsibility is to produce an answer for a matched request.

Conceptually:

```text
matched route
  -> application handler
      -> response
```

This is the simplest Express-like callback shape.

#### Middleware handlers

A middleware handler receives a request, a response, and a `Next` object. Its responsibility is not necessarily to finish the response.

It may:

- inspect the request,
- add application state,
- enforce authentication,
- log or trace,
- parse or prepare input,
- serve content,
- pass control to the next component.

Conceptually:

```text
middleware
  -> maybe handle
  -> maybe modify state
  -> maybe call next()
```

Therefore, middleware should not be read as another name for a route handler.

#### `Next` and middleware flow

`Next` makes middleware continuation explicit. A middleware can decide whether the request flow should continue.

The model is:

```text
middleware(req, res, next)
  -> does its work
      -> next()
          -> following middleware / router / handler
```

`Next` is not a scheduler and not a thread handoff. It is the application-visible continuation object for the dispatcher chain.

This makes flow control part of the application model. The chain is visible to the user. That is one of the main differences between a simple HTTP callback and an Express-like application framework.

### Dispatchers behind the API

\index{dispatcher}
\index{routing dispatch}


The user-facing API is built on internal dispatcher roles.

A compact view is:

| Dispatcher | Role |
|---|---|
| `ApplicationDispatcher` | invokes application-style callbacks |
| `MiddlewareDispatcher` | handles middleware and `next()` flow |
| `RouterDispatcher` | enters mounted routers |

The dispatchers encode the fact that application callbacks, middleware callbacks, and mounted routers have different control-flow meanings.

This internal structure mirrors the application model. The framework does not pretend that all web actions are the same. The dispatcher structure reflects those differences.

### Request and Response as web-application facades

\index{Request@\texttt{Request}}
\index{Response@\texttt{Response}}
\index{facade}


Chapter 21 introduced HTTP request and response objects. Chapter 22 raises them into Express-like application facades.

The facade does two things:

```text
keeps access to HTTP meaning
  + adds application-structure meaning
```

That is different from replacing the HTTP objects. The Express-like layer wraps and enriches them:

```text
HTTP objects
  -> protocol message meaning

Express facades
  -> web-application meaning
```

#### Request facade

The Express-like `Request` adds routing and application context to the lower HTTP request.

| Request aspect | Examples |
|---|---|
| routing context | `baseUrl`, `path`, `file`, `params`, `param(...)` |
| original target | `originalUrl`, `originalPath` |
| HTTP metadata | method, URL, HTTP version, headers, trailer |
| parsed input | query values, cookies, body |

This is the request-side semantic lift. The application can ask route-level questions, not only HTTP parsing questions:

```text
Which route parameter was matched?
What was the original URL?
Which mounted base path led here?
Which cookie or query value is present?
```

Those are web-application questions.

#### Response facade

The Express-like `Response` adds application-oriented response operations to the lower HTTP response.

| Response aspect | Examples |
|---|---|
| status and headers | `status`, `set`, `append`, `type` |
| cookies | `cookie`, `clearCookie` |
| body output | `send`, `json`, `end` |
| files | `sendFile`, `download`, `attachment` |
| redirects | `redirect`, `location` |
| advanced HTTP | `upgrade`, fragments, socket-context access |

This is the response-side semantic lift. The application can express common web responses directly:

```text
send JSON
redirect
set a cookie
send a file
return a status
upgrade the connection
```

Those operations still produce HTTP behavior underneath. The facade makes the application intent clearer.

#### Controlled access to lower HTTP capabilities

The facade raises the application API, but it does not hide all lower HTTP capabilities. Advanced operations remain available when the application genuinely needs them.

Examples include:

- upgrade,
- fragment sending,
- explicit end control,
- socket-context access,
- lower header control.

The facade is not a wall. It is a raised application surface with deliberate access points back to lower HTTP capabilities when the application genuinely needs them. This keeps the application interface convenient without pretending that lower HTTP and connection realities no longer exist.

### Built-in middleware as reusable application behavior

\index{middleware}
\index{static serving}
\index{virtual hosts}
\index{JSON middleware}
\index{authentication middleware}


The Express-like module also provides reusable middleware. Built-in middleware packages common request-processing behavior so it can be mounted once and reused across routes.

Examples include:

| Middleware | Application concern |
|---|---|
| `BasicAuthentication` | route-level authentication |
| `StaticMiddleware` | static file serving |
| `VHost` | virtual-host based routing |
| `VerboseRequest` | request visibility |
| `JsonMiddleware` | JSON request handling |

These belong above HTTP and below application-specific route logic. They are reusable application behaviors. That is middleware territory.

#### Authentication, static serving, virtual hosts, request visibility, and JSON handling

Basic authentication, static serving, virtual-host routing, verbose request reporting, and JSON handling are examples of reusable application behavior. They can be attached through middleware instead of being baked into the lower socket layer, the HTTP parser, or every individual route handler.

Static serving may involve root directories, index handling, fall-through behavior, headers, cookies, and connection-state decisions after the response. Those are practical application concerns, but they do not belong in the socket layer or in every route handler.

`VHost` belongs here because host-based dispatch is web-application routing behavior. `VerboseRequest` belongs here because request visibility is useful across routes but should not be duplicated inside every handler.

The Express module includes JSON middleware when the required `nlohmann_json` dependency is present; the build treats that dependency as required for this module. Architecturally, JSON middleware belongs to the same group of reusable request-processing behavior.

The architectural point is:

```text
common request-processing behavior
  -> reusable middleware
```

### Lower layers still matter

The Express-like layer changes application organization. It does not remove the lower stack. A route handler may look high-level, but bind/listen activation, TLS setup, HTTP parsing, response streaming, upgrade behavior, timeout boundaries, diagnostics, and shutdown still belong to the same layered runtime model.

That is the useful distinction: Express organizes web application logic; it does not hide the architecture beneath it.

### From Express-like routing to Server-Sent Events

Chapter 22 is the second step in Part VII. Chapter 21 introduced the HTTP layer. Chapter 22 showed how HTTP handling becomes application structure.

The next chapter moves to a specific HTTP-based real-time mechanism:

```text
Server-Sent Events
```

This is a natural next step. The reader now understands:

```text
HTTP request / response
  -> Express-like application structure
      -> long-lived HTTP event streaming
```

Chapter 23 then asks what happens when a route is not a short request/response exchange, but a long-lived one-way event stream. Server-Sent Events will show how the web stack handles that shape while still using the same layered discipline.

::: {.snodec-remember title="What to remember"}
- The Express-like layer sits above HTTP and organizes HTTP handling into web-application structure.
- `WebApp` is a router-shaped application surface.
- `WebAppT<ServerT>` combines that application surface with a concrete HTTP server type.
- HTTP request readiness enters the Express layer through a controller and the root route.
- `Router` composes routes, middleware, mounted routers, method-specific handlers, and routing policy.
- Application callbacks and middleware callbacks have different responsibilities.
:::

### Express public surface: WebApp header and carrier component

\index{Express components}
\index{WebApp@\texttt{WebApp}!public surface}


A file that directly uses the IPv4 legacy Express WebApp includes:

```cpp
#include <express/legacy/in/WebApp.h>
```

Code using the convenience server helpers includes:

```cpp
#include <express/legacy/in/Server.h>
```

The corresponding carrier component is:

```text
http-server-express-legacy-in
```

It selects the Express layer together with the IPv4 legacy stream carrier. The source-side and build-side names rhyme without being the same mechanism. Chapter 32 gives the source-derived matrix for the broader set of components and headers.

### Closing perspective

Chapter 21 raised stream communication to HTTP messages. Chapter 22 raised HTTP messages into application structure.

Chapter 23 keeps that structure but changes the temporal shape of a handler: instead of answering once, a route may keep an HTTP response open and emit events over time. There, HTTP is used for long-lived one-way event streaming.

