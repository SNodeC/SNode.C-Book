## Bluetooth in SNode.C: RFCOMM and L2CAP

### From path identity to Bluetooth endpoint identity

Chapter 11 replaced host-plus-port identity with Unix-domain path identity.

This chapter changes endpoint identity again.

Bluetooth RFCOMM and L2CAP are neither host-plus-port families nor path-based local IPC families. They use Bluetooth device identity together with a family-specific service selector:

```text
RFCOMM:
Bluetooth address + channel

L2CAP:
Bluetooth address + PSM
```

The larger SNode.C model remains recognizable:

- a server or client instance,
- a socket-context factory,
- a socket context,
- a concrete connection,
- runtime integration,
- status callbacks,
- connection lifecycle callbacks,
- and the same broad stream-based communication story.

The lower communication family changes.

The endpoint identity changes.

The application architecture does not need to be reinvented.

### Two Bluetooth endpoint families

SNode.C represents Bluetooth through two distinct lower communication families:

| Aspect | RFCOMM | L2CAP |
|---|---|---|
| Namespace | `net::rc` | `net::l2` |
| Address class | `net::rc::SocketAddress` | `net::l2::SocketAddress` |
| Endpoint identity | Bluetooth address + channel | Bluetooth address + PSM |
| Service selector | channel | PSM |
| Server role | `SocketServer` | `SocketServer` |
| Client role | `SocketClient` | `SocketClient` |
| Context/factory model | same | same |
| Runtime model | same | same |

This table contains the main distinction of the chapter.

RFCOMM and L2CAP are both Bluetooth families, but they are not the same endpoint model.

#### RFCOMM: Bluetooth address plus channel

RFCOMM endpoint identity is built from:

```text
Bluetooth device address
  + RFCOMM channel
```

A typical address-like pair may therefore look like:

```text
10:3D:1C:AC:BA:9C
channel 16
```

The channel is the RFCOMM service selector. It should not be treated as a generic "Bluetooth port" in the IP sense.

In SNode.C this distinction appears directly in the API:

```cpp
setBtAddress(...)
setChannel(...)
```

That naming is important because it keeps RFCOMM vocabulary visible in code.

#### L2CAP: Bluetooth address plus PSM

L2CAP endpoint identity is built from:

```text
Bluetooth device address
  + L2CAP PSM
```

A typical address-like pair may therefore look like:

```text
10:3D:1C:AC:BA:9C
PSM 0x1001
```

The PSM is the L2CAP service selector. It is not the same concept as an RFCOMM channel.

In SNode.C this distinction appears directly in the API:

```cpp
setBtAddress(...)
setPsm(...)
```

The shared Bluetooth-address part makes RFCOMM and L2CAP look related.

The service-selector part keeps them distinct.

#### Channel and PSM are not interchangeable

The most important conceptual mistake would be to collapse RFCOMM and L2CAP into one vague "Bluetooth socket" idea.

They belong in the same chapter because they are both Bluetooth-related lower communication families.

They must still remain conceptually separate:

```text
RFCOMM channel != L2CAP PSM
```

SNode.C preserves this separation in three places:

- separate namespaces: `net::rc` and `net::l2`,
- separate address classes,
- separate family-specific setters and getters.

This prevents the convenience of a shared framework pattern from hiding the real endpoint semantics.

### Bluetooth address classes

The address classes make the RFCOMM/L2CAP distinction concrete.

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

Default construction follows the same general address-model idea introduced in Chapter 8.

For Bluetooth address families, the wildcard Bluetooth address is represented as:

```text
00:00:00:00:00:00
```

The service selector starts at zero:

| Family | Default / wildcard shape |
|---|---|
| RFCOMM | `00:00:00:00:00:00`, channel `0` |
| L2CAP | `00:00:00:00:00:00`, PSM `0` |

This does not make RFCOMM and L2CAP the same family.

It means the same broad default/wildcard idea exists in both Bluetooth address models, while the service selector remains family-specific.

### Server and client use

The stream Bluetooth wrappers follow the same SNode.C pattern already seen for IPv4, IPv6, and Unix domain sockets.

The convenience calls set family-specific configuration and then delegate to the configured `listen(onStatus)` or `connect(onStatus)` path.

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

The server still registers a listening role.

The endpoint identity is now RFCOMM-specific.

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

The remote side is the peer Bluetooth address plus RFCOMM channel.

The optional local side can refine the local Bluetooth address, the local channel, or both.

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

The structure mirrors RFCOMM.

The service selector changes.

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

Again, the structure mirrors RFCOMM.

The endpoint semantics differ.

### Local and remote Bluetooth identity

Bluetooth endpoint identity may be less familiar than IP host-plus-port identity, so the local/remote distinction is worth making explicit.

For a Bluetooth server, the configured local endpoint may be:

```text
local Bluetooth address + channel
```

or:

```text
local Bluetooth address + PSM
```

depending on the family.

For a Bluetooth client, the configured remote endpoint is the peer service:

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

depending on the overload and family.

This continues Chapter 9’s connection model.

A lower-family identity change does not remove communication roles. There is still a local side, a remote side, a bound identity, and a peer identity.

### What remains stable

Bluetooth changes endpoint semantics, but it does not require a different SNode.C application architecture.

#### Server/client/connection/context model

The same core roles remain:

| Role | Meaning with Bluetooth stream families |
|---|---|
| `SocketServer` | listens using RFCOMM or L2CAP endpoint identity |
| `SocketClient` | connects to an RFCOMM or L2CAP peer endpoint |
| `SocketConnection` | represents one concrete peer relationship |
| `SocketContextFactory` | creates a context for a connection |
| `SocketContext` | implements application protocol behavior |

The server is still the outer listening role.

The client is still the outer connecting role.

The connection is still the concrete peer relationship.

The context is still the protocol endpoint attached to that connection.

#### Context and protocol logic

A `SocketContext` implementing a stream protocol does not need to become fundamentally RFCOMM-specific or L2CAP-specific just because it is carried over:

```cpp
net::rc::stream::legacy
```

or:

```cpp
net::l2::stream::legacy
```

What changes is the lower communication family.

What often remains stable is:

- how the protocol reacts to connection establishment,
- how it reads data,
- how it sends data,
- how it handles disconnection,
- how it thinks in terms of one connection and one context.

The context may inspect Bluetooth addresses for logging or diagnostics, but the application protocol logic can remain separated from the lower-family details.

#### Legacy and TLS

Chapter 7 introduced `legacy` and `tls` as connection-layer variants.

In the SNode.C component model, RFCOMM and L2CAP can participate in the same legacy/TLS connection-layer pattern when the corresponding components are available.

The point here is architectural, not cryptographic.

Bluetooth support does not sit outside the connection-layer model. The same separation still applies:

```text
network family
  -> transport form
      -> connection handling
          -> application context
```

### What changes operationally

Bluetooth is device-near, radio-based communication.

That changes the operational setting.

#### Platform reality

Bluetooth support depends on platform Bluetooth support.

On Linux, that usually means BlueZ and the corresponding development files must be available when building the Bluetooth-enabled components.

The build structure treats Bluetooth support as conditional rather than pretending that every target platform always has the necessary Bluetooth stack.

That is normal for system-level Bluetooth support.

SNode.C exposes RFCOMM and L2CAP as lower communication families, while still respecting the platform dependency.

#### Device-near and IoT systems

Bluetooth matters especially in device-near systems.

A system may combine several communication worlds:

- Bluetooth for local radio-based device communication,
- Unix domain sockets for local process-to-process communication,
- IPv4 or IPv6 for network communication,
- TLS for connection-layer security where appropriate,
- HTTP, WebSocket, MQTT, or other protocols above the lower layers.

SNode.C’s value is that these worlds can be understood through one layered model instead of as unrelated programming domains.

This is especially useful in IoT and embedded systems, where local device communication and network communication often coexist.

### What to remember

Remember:

- Bluetooth in SNode.C is represented by two lower communication families: RFCOMM and L2CAP.
- `net::rc` is RFCOMM.
- `net::l2` is L2CAP.
- RFCOMM endpoint identity is Bluetooth address plus channel.
- L2CAP endpoint identity is Bluetooth address plus PSM.
- Channel and PSM are not interchangeable.
- Both families use Bluetooth address identity, but their service selectors differ.
- Default Bluetooth address construction uses the wildcard Bluetooth address `00:00:00:00:00:00`.
- RFCOMM defaults its channel to `0`.
- L2CAP defaults its PSM to `0`.
- The server/client/connection/context model remains stable.
- Local and remote identities still matter.
- Bluetooth support depends on platform Bluetooth support and build availability.
- The lower-family tour is now complete.

### Closing perspective

Chapter 10 covered host-plus-port endpoint identity through IPv4 and IPv6.

Chapter 11 replaced that with Unix-domain path identity.

This chapter replaced it again with Bluetooth-specific endpoint identities:

- Bluetooth address plus RFCOMM channel,
- Bluetooth address plus L2CAP PSM.

Across all of these changes, the same broad SNode.C role model remained stable.

The lower-family tour is now complete.

The next part can move upward again, beginning with how to write `SocketContext` classes well.
