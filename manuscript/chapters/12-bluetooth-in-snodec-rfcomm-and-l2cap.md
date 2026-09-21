## Bluetooth in SNode.C: RFCOMM and L2CAP

\index{Bluetooth}
\index{RFCOMM}
\index{L2CAP}


### From path identity to Bluetooth endpoint identity

Bluetooth is local in a different sense from Unix-domain sockets: the peer is nearby, device-specific, and mediated by the platform Bluetooth stack.

Bluetooth RFCOMM and L2CAP are neither host-plus-port families nor path-based local IPC families. They use Bluetooth device identity together with a family-specific service selector:

```text
RFCOMM:
Bluetooth address + channel

L2CAP:
Bluetooth address + PSM
```

After IPv4, IPv6, and Unix domain sockets, Bluetooth is the final lower-family variation before the focus moves upward to application protocol contexts.

The first task is to identify which service the peer actually offers. A device address alone is not enough, and changing `rc` to `l2` in a type name does not translate an RFCOMM service into an L2CAP service. Once the matching endpoint is available, the existing factory/context model supplies protocol behavior over it.

### Two Bluetooth families, two service selectors

\index{Bluetooth!service selectors}
\index{RFCOMM!channel}
\index{L2CAP!PSM}


SNode.C represents Bluetooth through two distinct lower families:

| Aspect | RFCOMM | L2CAP |
|---|---|---|
| Namespace | `net::rc` | `net::l2` |
| Address class | `net::rc::SocketAddress` | `net::l2::SocketAddress` |
| Endpoint identity | Bluetooth address + channel | Bluetooth address + PSM |
| Service selector | channel | PSM |
| Server role | `SocketServer` | `SocketServer` |
| Client role | `SocketClient` | `SocketClient` |
| Context/factory model | stable | stable |
| Runtime model | stable | stable |

This table contains the main distinction of the chapter: RFCOMM and L2CAP share Bluetooth device identity, but they use different service selectors. An RFCOMM channel is not an L2CAP PSM, and a PSM is not an RFCOMM channel.

#### RFCOMM: Bluetooth address plus channel

\index{RFCOMM}
\index{Bluetooth!RFCOMM}
\index{net::rc::SocketAddress@\texttt{net::rc::SocketAddress}}


RFCOMM endpoint identity is built from a Bluetooth device address plus an RFCOMM channel. A typical pair is `10:3D:1C:AC:BA:9C` with channel `16`. The channel is the RFCOMM service selector; it should not be treated as a generic "Bluetooth port" in the IP sense. SNode.C keeps that vocabulary visible in the API through `setBtAddress(...)` and `setChannel(...)`.

#### L2CAP: Bluetooth address plus PSM

\index{L2CAP}
\index{Bluetooth!L2CAP}
\index{net::l2::SocketAddress@\texttt{net::l2::SocketAddress}}


L2CAP endpoint identity is built from a Bluetooth device address plus an L2CAP PSM. A typical pair is `10:3D:1C:AC:BA:9C` with PSM `0x1001`. The PSM is the L2CAP service selector, not the same concept as an RFCOMM channel. SNode.C keeps that vocabulary visible in the API through `setBtAddress(...)` and `setPsm(...)`: the shared Bluetooth-address part makes RFCOMM and L2CAP look related, while the service-selector part keeps them distinct.

#### Channel and PSM are not interchangeable

The most important conceptual mistake would be to collapse RFCOMM and L2CAP into one vague "Bluetooth socket" idea. They belong in the same chapter because they are both Bluetooth-related lower families, but their service selectors are not interchangeable: `RFCOMM channel != L2CAP PSM`. SNode.C preserves that separation through separate namespaces (`net::rc` and `net::l2`), separate address classes, and separate family-specific setters and getters, so the convenience of a shared framework pattern does not hide the real endpoint semantics.

### Bluetooth address classes

\index{Bluetooth address}
\index{net::rc::SocketAddress@\texttt{net::rc::SocketAddress}}
\index{net::l2::SocketAddress@\texttt{net::l2::SocketAddress}}


The address classes make the RFCOMM/L2CAP distinction concrete: their setters, getters, constructors, and string rendering expose the two pieces of endpoint identity for each family.

#### `net::rc::SocketAddress`

The RFCOMM address class is:

```cpp
net::rc::SocketAddress
```

Its conceptual surface includes:

- default construction,
- construction from a Bluetooth address,
- construction from a channel,
- construction from Bluetooth address plus channel,
- construction from an existing RFCOMM socket address,
- initialization,
- `setBtAddress(...)` and `getBtAddress()`,
- `setChannel(...)` and `getChannel()`,
- and string rendering.

This mirrors the endpoint identity:

```text
Bluetooth address + channel
```

A compact code anchor is:

```cpp
net::rc::SocketAddress address("10:3D:1C:AC:BA:9C", 16);
```

#### `net::l2::SocketAddress`

The L2CAP address class is:

```cpp
net::l2::SocketAddress
```

Its conceptual surface includes:

- default construction,
- construction from a Bluetooth address,
- construction from a PSM,
- construction from Bluetooth address plus PSM,
- construction from an existing L2CAP socket address,
- initialization,
- `setBtAddress(...)` and `getBtAddress()`,
- `setPsm(...)` and `getPsm()`,
- and string rendering.

This mirrors the endpoint identity:

```text
Bluetooth address + PSM
```

A compact code anchor is:

```cpp
net::l2::SocketAddress address("10:3D:1C:AC:BA:9C", 0x1001);
```

#### Default construction and wildcard Bluetooth address

Default construction follows the same general address-model idea introduced in Chapter 8. In the SNode.C address model used here, default Bluetooth construction belongs to the same wildcard or deferred-endpoint pattern as the earlier families: wildcard Bluetooth address plus a zero service selector. For Bluetooth address families, the wildcard Bluetooth address is represented as:

```text
00:00:00:00:00:00
```

The service selector starts at zero:

| Family | Default / wildcard shape |
|---|---|
| RFCOMM | `00:00:00:00:00:00`, channel `0` |
| L2CAP | `00:00:00:00:00:00`, PSM `0` |

This does not make RFCOMM and L2CAP the same family; it only means that the broad default/\allowbreak{}wildcard idea exists in both Bluetooth address models while the service selector remains family-specific.

### Server and client use with Bluetooth endpoints

\index{Bluetooth!server/client use}
\index{listen()@\texttt{listen()}}
\index{connect()@\texttt{connect()}}


The stream Bluetooth wrappers follow the SNode.C pattern already seen for IPv4, IPv6, and Unix domain sockets. The convenience calls configure the handle and then enter the usual registration path.

The difference is the configured endpoint identity:

```text
RFCOMM:
Bluetooth address + channel

L2CAP:
Bluetooth address + PSM
```

#### RFCOMM server-side `listen(...)`

A simple RFCOMM server may look like this:

```cpp
using RcServer = net::rc::stream::legacy::SocketServer<MyFactory>;

RcServer server("echo-rc");
server.listen(16, 5, onStatus);
```

or with an explicit local Bluetooth address:

```cpp
server.listen("10:3D:1C:AC:BA:9C", 16, 5, onStatus);
```

The server-side convenience overloads are channel-centered:

| Surface call | Configuration effect |
|---|---|
| `listen(channel, ...)` | `Local::setChannel(channel)` |
| `listen(channel, backlog, ...)` | `Local::setChannel(channel)` + backlog |
| `listen(btAddress, channel, ...)` | `Local::setBtAddress(btAddress)->setChannel(channel)` |
| `listen(btAddress, channel, backlog, ...)` | `Local::setBtAddress(btAddress)->setChannel(channel)` + backlog |

The server still registers a listening instance. The endpoint identity is now RFCOMM-specific.

#### RFCOMM client-side `connect(...)`

A simple RFCOMM client may look like this:

```cpp
using RcClient = net::rc::stream::legacy::SocketClient<MyFactory>;

RcClient client("echo-rc-client");
client.connect("10:3D:1C:AC:BA:9C", 16, onStatus);
```

The client-side convenience overloads are also channel-centered:

| Surface call | Configuration effect |
|---|---|
| `connect(btAddress, channel, ...)` | `Remote::setBtAddress(btAddress)->setChannel(channel)` |
| `connect(btAddress, channel, bindBtAddress, ...)` | remote address/channel + `Local::setBtAddress(bindBtAddress)` |
| `connect(btAddress, channel, bindChannel, ...)` | remote address/channel + `Local::setChannel(bindChannel)` |
| `connect(btAddress, channel, bindBtAddress, bindChannel, ...)` | remote address/channel + `Local::setBtAddress(bindBtAddress)->setChannel(bindChannel)` |

The remote side is the peer Bluetooth address plus RFCOMM channel. The optional local side can refine the local Bluetooth address, the local channel, or both.

#### L2CAP server-side `listen(...)`

A simple L2CAP server may look like this:

```cpp
using L2Server = net::l2::stream::legacy::SocketServer<MyFactory>;

L2Server server("echo-l2");
server.listen(0x1001, 5, onStatus);
```

or with an explicit local Bluetooth address:

```cpp
server.listen("10:3D:1C:AC:BA:9C", 0x1001, 5, onStatus);
```

The server-side convenience overloads are PSM-centered:

| Surface call | Configuration effect |
|---|---|
| `listen(psm, ...)` | `Local::setPsm(psm)` |
| `listen(psm, backlog, ...)` | `Local::setPsm(psm)` + backlog |
| `listen(btAddress, psm, ...)` | `Local::setBtAddress(btAddress)->setPsm(psm)` |
| `listen(btAddress, psm, backlog, ...)` | `Local::setBtAddress(btAddress)->setPsm(psm)` + backlog |

The structure mirrors RFCOMM, while the service selector changes.

#### L2CAP client-side `connect(...)`

A simple L2CAP client may look like this:

```cpp
using L2Client = net::l2::stream::legacy::SocketClient<MyFactory>;

L2Client client("echo-l2-client");
client.connect("10:3D:1C:AC:BA:9C", 0x1001, onStatus);
```

The client-side convenience overloads are PSM-centered:

| Surface call | Configuration effect |
|---|---|
| `connect(btAddress, psm, ...)` | `Remote::setBtAddress(btAddress)->setPsm(psm)` |
| `connect(btAddress, psm, bindBtAddress, ...)` | remote address/PSM + `Local::setBtAddress(bindBtAddress)` |
| `connect(btAddress, psm, bindPsm, ...)` | remote address/PSM + `Local::setPsm(bindPsm)` |
| `connect(btAddress, psm, bindBtAddress, bindPsm, ...)` | remote address/PSM + `Local::setBtAddress(bindBtAddress)->setPsm(bindPsm)` |

Again, the structure mirrors RFCOMM, while the endpoint semantics differ.

### Local and remote Bluetooth identity

Bluetooth endpoint identity may be less familiar than IP host-plus-port identity, so the local/remote distinction is worth making explicit: changing the endpoint family does not erase direction.

A server still has a local listening identity:

```text
local Bluetooth address + channel
```

or:

```text
local Bluetooth address + PSM
```

depending on the family.

A client still has a remote peer identity:

```text
remote Bluetooth address + channel
```

or:

```text
remote Bluetooth address + PSM
```

The client may also refine its local side:

```text
local Bluetooth address
local channel
local PSM
```

depending on the overload and family. This continues Chapter 9's connection model. There is still a local side, a remote side, a bound identity, and a peer identity.

### Establish the Bluetooth service before connecting

\index{Bluetooth!pairing}
\index{adapter state}


Before running a Bluetooth example, prepare two compatible endpoints. Each needs working Bluetooth hardware: an integrated controller or a supported USB adapter, its driver and firmware, and an enabled radio. For the classic RFCOMM and L2CAP stream examples here, choose peers and adapters that support the required Bluetooth Classic service. A device advertised only as a Bluetooth Low Energy sensor does not thereby provide one of these stream endpoints.

On Linux, the operating system must expose the controller and the required Bluetooth socket support. BlueZ supplies the usual administration tools and daemon; its development files allow the corresponding SNode.C components to be built. Successful compilation establishes that build dependency, not that an adapter is present or that a remote application is listening.

The preparation order is practical:

1. Check that the intended controller is visible, powered, and not disabled by the system's radio-blocking policy. If several controllers are present, select the one the application will use.
2. Put the peer into its discovery and pairing mode when setting up a new relationship. Both devices must be within working radio range, and the peer must actually support the intended service.
3. When the service or local security policy requires pairing, complete it with the operating-system tools or Bluetooth settings interface. Respond to the authentication request on the participating devices and inspect the resulting paired state.
4. Check the service's authorization and trust policy, then start the matching peer application. Pairing establishes a device relationship; it does not start the SNode.C server or create its application service.

A short Linux administration session can make these stages visible. Start `bluetoothctl`, then inspect the controller and discover the peer:

```text
list
show
power on
agent on
default-agent
scan on
```

Use the peer identifier reported by the tool in place of `PEER` below. Inspect it first; when pairing is required and it is not already paired, issue the pairing command and follow the prompts:

```text
info PEER
pair PEER
info PEER
scan off
```

These are interactive `bluetoothctl` commands, not SNode.C options. An existing valid pairing need not be recreated. BlueZ versions may also establish trust or connect available profiles as part of `pair`; inspect the resulting state and the local policy instead of treating a generic “connected” indication as proof that the book's application service is ready. The BlueZ `bluetoothctl` manual and Device API documentation describe those platform operations.

Pairing is therefore a platform and service requirement, not an unconditional requirement imposed by these SNode.C socket wrappers. SNode.C uses the prepared Bluetooth stack as a lower family; it does not replace controller setup, discovery, pairing, or authorization. Once those prerequisites are satisfied and the peer service is running, the ordinary listen/connect path can establish the application connection. The addressing choices are the ones already explained above.

### What remains stable

Bluetooth changes endpoint semantics, but it does not require a different SNode.C application architecture.

#### Server/client/connection/context model

The stable core roles remain:

| Role | Meaning with Bluetooth stream families |
|---|---|
| Application-side handle | the `SocketServer`/`SocketClient` handle used to configure and register the role |
| Registered instance | the runtime-visible server-side or client-side communication role |
| `SocketConnection` | one concrete peer relationship |
| `SocketContextFactory` | creates a context for a connection |
| `SocketContext` | implements protocol behavior |

The server is still the listening role, the client is still the connecting role, the connection is still the concrete peer relationship, and the context is still the protocol endpoint attached to that connection.

#### Context and protocol logic

A `SocketContext` implementing a stream protocol does not need to become fundamentally RFCOMM-specific or L2CAP-specific just because it is carried over:

```cpp
net::rc::stream::legacy
```

or:

```cpp
net::l2::stream::legacy
```

Byte parsing and response selection may remain unchanged. Timing and trust assumptions still need review: a protocol tested on a local IP loopback connection has not established that its deadlines or peer-selection policy suit the chosen Bluetooth service. Keep the parser reusable where possible, while making those deployment policies explicit through the endpoint and application configuration.

#### Legacy and TLS

Chapter 7 introduced `legacy` and `tls` as connection-layer variants: `legacy` is the non-TLS stream connection variant, while `tls` adds TLS connection handling. RFCOMM and L2CAP can participate in that stream connection-layer pattern when the corresponding Bluetooth and TLS components are available. The point here is architectural, not cryptographic: Bluetooth support does not sit outside the connection-layer model, and the same separation still applies to network family, transport form, connection handling, and application context.

### What changes operationally

\index{Bluetooth!deployment}
\index{permissions}


Bluetooth is device-near, radio-based communication, so it changes the operational setting.

#### Platform and build reality

Build availability and operating hardware are separate observations. If the installed SNode.C package does not contain the requested Bluetooth component, attaching an adapter will not supply the missing library. Conversely, a successfully built Bluetooth example can still run on a host with no usable controller. Check component discovery when building the consumer and controller state when preparing to run it; pairing does not repair a missing build dependency.

#### Diagnose preparation before protocol behavior

A Bluetooth connection can fail before the application context receives a byte. Use the preparation sequence above to distinguish an unavailable controller, an unprepared device relationship, denied service access, and a peer service that has not been started. Rewriting the parser does not repair any of those conditions.

Conversely, successful pairing alone says nothing about the application's messages. Once the connection is ready, the context is responsible for the same framing and protocol behavior taught in the neighboring chapters. The distinction lets a reader inspect a sample program in two stages: what the platform must provide before activation, and what the context does after activation.

The preparation guide establishes what must be ready before a Bluetooth example can run. The selected adapter, peer service, and operating-system policy determine the actual connection outcome. Chapter 15 develops protocol transfer with IPv4 and Unix-domain sockets, where the reader can observe that behavior without Bluetooth hardware.

#### Device-near and IoT systems

Bluetooth matters especially in device-near systems, where one application may combine several communication worlds:

- Bluetooth for local radio-based device communication,
- Unix domain sockets for local process-to-process communication,
- IPv4 or IPv6 for network communication,
- TLS for connection-layer security where appropriate,
- HTTP, WebSocket, MQTT, or other protocols above the lower layers.

SNode.C's value is that these worlds can be understood through one layered model instead of as unrelated programming domains. That is especially useful in IoT and embedded systems, where local device communication and network communication often coexist.

::: {.snodec-remember title="What to remember"}
- Bluetooth support in this part is represented by two lower families: RFCOMM in `net::rc` and L2CAP in `net::l2`.
- RFCOMM endpoint identity is Bluetooth address plus channel; L2CAP endpoint identity is Bluetooth address plus PSM.
- Channel and PSM are not interchangeable service selectors.
- Prepare compatible hardware, an enabled controller, the peer service, and any required pairing/authorization before diagnosing application protocol behavior.
- Bluetooth convenience calls configure the handle and then enter the usual registration path.
- The Bluetooth wildcard or deferred endpoint shape is the wildcard Bluetooth address plus service selector `0`.
:::

### Public surface of Bluetooth stream roles

\index{net::rc::stream::legacy@\texttt{net::rc::stream::legacy}}
\index{net::l2::stream::legacy@\texttt{net::l2::stream::legacy}}


Bluetooth stream roles follow the same source/build rule, but only when the required Bluetooth development support is present. RFCOMM uses the `rc` family fragment:

```cpp
#include <net/rc/stream/legacy/SocketServer.h>
#include <net/rc/stream/legacy/SocketClient.h>
```

with the corresponding component:

```text
net-rc-stream-legacy
```

L2CAP uses the `l2` fragment:

```cpp
#include <net/l2/stream/legacy/SocketServer.h>
#include <net/l2/stream/legacy/SocketClient.h>
```

with the corresponding component:

```text
net-l2-stream-legacy
```

The local lesson is the conditional family surface. Chapter 32 gives the broader include/component matrix.

### Closing perspective

Host-plus-port, path-based, and Bluetooth endpoint identities show the same architectural question from three lower-family angles. The lower-family tour has done its job once endpoint identity can be separated from protocol behavior.

