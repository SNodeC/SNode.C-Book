## The Express-Like Framework

### From HTTP messages to application structure

Chapter 21 showed how SNode.C raises stream communication to HTTP request and response objects.

Chapter 22 moves one level higher.

The application is no longer organized only around a HTTP request-ready callback.

It is organized around:

- a web application,
- routers,
- routes,
- mounted routers,
- middleware chains,
- request and response facades,
- and explicit middleware continuation.

That is the central idea of this chapter:

> The Express-like layer does not replace HTTP; it organizes HTTP handling into application structure.

The lower stack remains visible:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response layer
              -> Express-like application layer
```

The Express-like layer is therefore not a different universe.

It is the application-organization layer above HTTP.

### The Express-like layer in the SNode.C stack

The stack now looks like this:

```text
runtime
  -> configured server instance
      -> lower communication family
          -> stream transport
              -> legacy or TLS connection handling
                  -> HTTP request / response
                      -> Express-like routing and middleware
```

Earlier chapters established the lower parts.

Chapter 21 introduced HTTP request and response semantics.

Chapter 22 now asks what happens when HTTP handling becomes an application structure.

The answer is:

```text
HTTP request ready
  -> Express controller
      -> root route
          -> router / middleware / application handler
```

This is the transition from protocol handling to web-application composition.

### HTTP layer and Express-like layer side by side

A compact comparison makes the new layer visible.

| Concern | HTTP layer | Express-like layer |
|---|---|---|
| application-facing unit | request / response | routed request / response flow |
| primary callback | request ready | route handler or middleware |
| structure | one HTTP protocol endpoint | application, routers, routes, middleware |
| flow control | HTTP lifecycle | `next()` and dispatcher chain |
| path meaning | HTTP target/path | mount path, route path, params, base/original URL |
| response surface | HTTP response | application-oriented response facade |
| reuse mechanism | HTTP server/client wrappers | routers and middleware |
| lower layers | still present | still present underneath HTTP |

The HTTP layer gives the application request and response objects.

The Express-like layer gives the application a way to organize what should happen with them.

### What “Express-like” means here

“Express-like” does not mean that SNode.C embeds Node.js or the JavaScript Express runtime.

It means that the C++ web-application layer uses a familiar application model:

- `WebApp`,
- `Router`,
- `.use()`,
- `.get()`, `.post()`, and other HTTP verb methods,
- middleware callbacks,
- `Next`,
- mounted routers,
- request and response facades,
- built-in middleware.

The layer is Express-like in its programming model.

It is still SNode.C in its runtime, connection, configuration, and lower-layer architecture.

This distinction matters because the familiar surface should not hide the underlying model.

A SNode.C Express-like application is still carried by:

- a configured server instance,
- a HTTP server layer,
- legacy or TLS connection handling,
- lower-family choices,
- diagnostics,
- timeout and failure behavior.

### WebApp, WebAppT, and the HTTP server underneath

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

This is the architectural center of the chapter.

| Type | Role |
|---|---|
| `Router` | route tree and middleware structure |
| `WebApp` | router-shaped application plus runtime-facing lifecycle |
| `ServerT` | concrete HTTP server type underneath |
| `WebAppT<ServerT>` | combined Express-like application and HTTP server |

The result is not a separate web runtime.

It is a web-application surface joined to a concrete HTTP server.

#### WebApp as router-shaped application

`WebApp` derives from `Router`.

That means the application itself can be treated as the root of a route structure.

It also exposes runtime-facing lifecycle operations such as:

- `init(...)`,
- `start(...)`,
- `stop()`,
- `tick(...)`,
- `free()`,
- `state()`.

This keeps the web-application layer connected to the same runtime story introduced earlier in the book.

A web application is not just a set of route functions.

It is a route structure that still runs inside the SNode.C event-driven runtime.

#### WebAppT as the bridge to a concrete HTTP server

`WebAppT<ServerT>` combines the Express-like layer with a concrete HTTP server type.

For example, an IPv4 legacy Express-like web app can be shaped as:

```cpp
using WebApp =
    WebAppT<web::http::legacy::in::Server>;
```

The same idea applies to other lower-family and connection-handling variants where provided.

The pattern is:

```text
Express-like WebAppT
  + concrete HTTP server
      -> runnable web application
```

This matches the design pattern from Chapter 21.

The HTTP layer remains underneath.

The Express-like layer organizes the application above it.

#### From HTTP request readiness to Express dispatch

The key bridge is the moment when HTTP request readiness enters the Express-like routing structure.

Conceptually:

```text
HTTP request ready
  -> Controller(req, res)
      -> rootRoute dispatch
          -> application callback / middleware / mounted router
```

This is where Chapter 21 becomes Chapter 22.

The HTTP layer has parsed the request and prepared a response object.

The Express-like layer now decides which application structure should handle that request.

That decision belongs above HTTP.

It depends on route paths, mounted routers, middleware, and routing policy.

### Router as the application composition unit

`Router` is the main composition unit of the Express-like layer.

It lets a web application be assembled from parts instead of being written as one large request callback.

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

The important point is not the length of the method list.

The important point is the structure it enables:

```text
application
  -> router
      -> route
      -> middleware
      -> mounted router
```

#### Routes, mounted routers, and middleware

A route is a point where request properties and application behavior meet.

A mounted router lets a larger application be built from smaller route structures.

Middleware lets common behavior be placed into the request flow without duplicating it in every handler.

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

At this layer, route matching is part of application correctness.

The router exposes policy controls such as:

| Policy | Question |
|---|---|
| strict routing | Are `/x` and `/x/` distinct? |
| case-insensitive routing | Should route matching ignore case? |
| merge params | Should mounted routers receive parent params? |

These policies belong here.

They are not socket concerns.

They are not generic HTTP parsing concerns.

They are web-application routing concerns.

`merge params` is a good example.

It decides how parameter information moves through nested router structures.

That is meaningful only once the application has routers and mount points.

### Application callbacks and middleware callbacks

The Express-like layer distinguishes two important callback shapes.

| Callback shape | Meaning |
|---|---|
| `(req, res)` | application handler; may produce a response |
| `(req, res, next)` | middleware; may continue the chain |

This distinction teaches the layer model clearly.

Not every function attached to a route has the same responsibility.

Some handlers answer.

Some middleware participates in a chain.

Some middleware may inspect, modify, authorize, log, or prepare state before passing control onward.

#### Application handlers

An application handler receives a request and a response.

Its typical responsibility is to produce an answer for a matched request.

Conceptually:

```text
matched route
  -> application handler
      -> response
```

This is the simplest Express-like callback shape.

#### Middleware handlers

A middleware handler receives a request, a response, and a `Next` object.

Its responsibility is not necessarily to finish the response.

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

This is why middleware is not just another name for a route handler.

#### `Next` and middleware flow

`Next` makes middleware continuation explicit.

A middleware can decide whether the request flow should continue.

The model is:

```text
middleware(req, res, next)
  -> does its work
      -> next()
          -> following middleware / router / handler
```

This makes flow control part of the application model.

The chain is visible to the user.

That is one of the main differences between a simple HTTP callback and an Express-like application framework.

### Dispatchers behind the API

The user-facing API is built on internal dispatcher roles.

A compact view is:

| Dispatcher | Role |
|---|---|
| `ApplicationDispatcher` | invokes application-style callbacks |
| `MiddlewareDispatcher` | handles middleware and `next()` flow |
| `RouterDispatcher` | enters mounted routers |

This internal structure mirrors the application model.

The framework does not pretend that all web actions are the same.

Application callbacks, middleware, and mounted routers have different meanings.

The dispatcher structure reflects those differences.

### Request and Response as application facades

Chapter 21 introduced HTTP request and response objects.

Chapter 22 raises them into Express-like application facades.

The facade does two things:

```text
keeps access to HTTP meaning
  + adds application-structure meaning
```

That is different from replacing the HTTP objects.

The Express-like layer wraps and enriches them.

#### Request facade

The Express-like `Request` adds routing and application context to the lower HTTP request.

| Request aspect | Examples |
|---|---|
| routing context | `baseUrl`, `path`, `file`, `params`, `param(...)` |
| original target | `originalUrl`, `originalPath` |
| HTTP metadata | method, URL, HTTP version, headers, trailer |
| parsed input | query values, cookies, body |

This is the request-side semantic lift.

The application can ask route-level questions, not only HTTP parsing questions.

For example:

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

This is the response-side semantic lift.

The application can express common web responses directly:

```text
send JSON
redirect
set a cookie
send a file
return a status
upgrade the connection
```

Those operations still produce HTTP behavior underneath.

The facade makes the application intent clearer.

#### Controlled access to lower HTTP capabilities

The facade raises the application API, but it does not hide all lower HTTP capabilities.

Advanced operations remain available when the application genuinely needs them.

Examples include:

- upgrade,
- fragment sending,
- explicit end control,
- socket-context access,
- lower header control.

This is a controlled escape hatch.

It keeps the application interface convenient without pretending that lower HTTP and connection realities no longer exist.

### Built-in middleware as reusable application behavior

The Express-like module also provides reusable middleware.

Examples include:

| Middleware | Application concern |
|---|---|
| `BasicAuthentication` | route-level authentication |
| `StaticMiddleware` | static file serving |
| `VHost` | virtual-host based routing |
| `VerboseRequest` | request visibility |
| `JsonMiddleware` | JSON request handling |

These belong above HTTP and below application-specific route logic.

They are reusable application behaviors.

That is middleware territory.

#### Authentication as middleware

Basic authentication is naturally middleware.

It can be attached where it is needed in the route structure.

It can participate in the same request flow as other middleware.

It does not have to be baked into the lower socket layer or into every route handler.

#### Static serving as middleware

Static file serving is also naturally middleware.

It is application behavior built on top of HTTP.

It may involve:

- a root directory,
- index handling,
- fall-through behavior,
- response headers,
- cookies,
- connection-state decisions after the response.

Those are web-serving concerns.

They belong at the Express-like layer.

#### JSON middleware

JSON middleware support belongs to the same group of reusable request-processing behavior.

It is part of the Express-like module when the required JSON dependency is available at build time.

The important architectural point is simple:

```text
common request-processing behavior
  -> reusable middleware
```

### Lower layers still matter

The Express-like layer changes application organization.

It does not remove lower-layer facts.

A web application still has:

- a lower communication family,
- legacy or TLS connection handling,
- HTTP parsing and response generation underneath,
- runtime lifecycle,
- configuration,
- diagnostics,
- timeouts,
- failure behavior.

This matters during operation.

A route handler may look simple, but the application can still fail because of:

- bind errors,
- TLS configuration,
- read/write timeouts,
- retry or reconnect policy,
- HTTP parsing errors,
- response streaming behavior,
- protocol upgrade behavior.

The Express-like layer is useful because it organizes application logic.

It is not a reason to forget the architecture beneath it.

### From Express-like applications to Server-Sent Events

Chapter 22 is the second step in Part VII.

Chapter 21 introduced the HTTP layer.

Chapter 22 showed how HTTP handling becomes application structure.

The next chapter moves to a specific HTTP-based real-time mechanism:

```text
Server-Sent Events
```

This is a natural next step.

The reader now understands:

```text
HTTP request / response
  -> Express-like application structure
      -> long-lived HTTP event streaming
```

Server-Sent Events will show how the web stack handles one-way event streaming while still using the same layered discipline.

### What to remember

Remember:

- The Express-like layer sits above HTTP.
- It organizes HTTP handling into routers, routes, middleware, and application callbacks.
- The Express-like layer does not replace HTTP; it structures HTTP use.
- `WebApp` is a router-shaped application surface.
- `WebAppT<ServerT>` combines the Express layer with a concrete HTTP server.
- HTTP request readiness is dispatched into the Express root route.
- `Router` provides route methods, mounted routers, middleware, and routing policy.
- Application callbacks and middleware callbacks have different responsibilities.
- `Next` controls middleware continuation.
- Express `Request` and `Response` are application-oriented facades over HTTP objects.
- Built-in middleware packages reusable web-application behavior.
- Lower runtime, configuration, diagnostics, TLS, timeout, and failure behavior still matter.
- Chapter 23 moves to Server-Sent Events.

### Closing perspective

Chapter 22 showed how HTTP handling becomes application structure.

The stack now reads:

```text
lower communication family
  -> stream transport
      -> legacy or TLS connection handling
          -> HTTP request / response
              -> Express-like routing and middleware
```

This is a higher-level application model, but it is still built on the same SNode.C foundations.

The next chapter turns to Server-Sent Events.

There, HTTP is used for long-lived one-way event streaming.
