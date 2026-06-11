## Bluetooth in SNode.C: RFCOMM and L2CAP

### From path identity to Bluetooth endpoint identity

Chapter 11 replaced host-plus-port endpoint identity with Unix-domain path identity. This chapter changes endpoint identity again.

Bluetooth RFCOMM and L2CAP are neither host-plus-port families nor path-based local IPC families. They use Bluetooth device identity together with a family-specific service selector:

```text
RFCOMM:
Bluetooth address + channel

L2CAP:
Bluetooth address + PSM
```

After IPv4, IPv6, and Unix domain sockets, Bluetooth is the final lower-family variation in this part of the book before the focus moves upward to application protocol contexts.

The larger SNode.C model remains recognizable:

- an application-side `SocketServer` or `SocketClient` handle,
- a registered server-side or client-side instance,
- a concrete `SocketConnection`,
- a socket-context factory,
- a per-connection socket context,
- runtime integration,
- status callbacks,
- connection lifecycle callbacks,
- and the same broad stream-based server/client/connection model.

The lower communication family changes. The endpoint identity changes. The application architecture does not need to be reinvented.

### Two Bluetooth families, two service selectors

SNode.C represents Bluetooth through two distinct lower communication families:

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

This table contains the main distinction of the chapter.

RFCOMM and L2CAP share the idea of Bluetooth device identity. They differ in the service selector that identifies the communication endpoint within that Bluetooth family.

That difference is not cosmetic. An RFCOMM channel is not an L2CAP PSM, and a PSM is not an RFCOMM channel.

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

The shared Bluetooth-address part makes RFCOMM and L2CAP look related. The service-selector part keeps them distinct.

#### Channel and PSM are not interchangeable

The most important conceptual mistake would be to collapse RFCOMM and L2CAP into one vague "Bluetooth socket" idea. They belong in the same chapter because they are both Bluetooth-related lower communication families.

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

Their surface is not arbitrary. The setters, getters, constructors, and string rendering expose the two pieces of endpoint identity for each family.

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

In the SNode.C address model used here, default Bluetooth construction belongs to the same wildcard or deferred-endpoint pattern as the earlier families: wildcard Bluetooth address plus a zero service selector.

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

It means the broad default/wildcard idea exists in both Bluetooth address models, while the service selector remains family-specific.

### Server and client use with Bluetooth endpoints

The stream Bluetooth wrappers follow the SNode.C pattern already seen for IPv4, IPv6, and Unix domain sockets. The convenience calls configure the application-side handle and then enter the usual registration path.

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

The structure mirrors RFCOMM. The service selector changes.

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

Again, the structure mirrors RFCOMM. The endpoint semantics differ.

### Local and remote Bluetooth identity

Bluetooth endpoint identity may be less familiar than IP host-plus-port identity, so the local/remote distinction is worth making explicit.

Changing the endpoint family does not erase direction.

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

### Pairing before SNode.C communication

Bluetooth endpoint identity is not the whole operational story.

Before two devices can communicate through SNode.C over RFCOMM or L2CAP, the devices must already be paired using the operating-system Bluetooth tools or user interface.

SNode.C uses the Bluetooth stack as a lower communication family. It does not replace Bluetooth discovery, pairing, trust management, or adapter setup.

That separation is important:

```text
Bluetooth setup:
pairing, trust, adapter state, permissions

SNode.C communication:
configured endpoint identity, listen/connect registration, connection handling, context behavior
```

If pairing is missing, a SNode.C client may use the correct Bluetooth address and service selector and still fail at the platform Bluetooth layer.

This is not a different SNode.C architecture problem. It is an operational precondition of Bluetooth communication between devices.

### What remains stable

Bluetooth changes endpoint semantics, but it does not require a different SNode.C application architecture.

#### Server/client/connection/context model

The stable core roles remain:

| Role | Meaning with Bluetooth stream families |
|---|---|
| Application-side handle | the visible `SocketServer` or `SocketClient` object used to configure and register the role |
| Registered instance | the runtime-visible server-side or client-side communication role |
| `SocketConnection` | one concrete peer relationship |
| `SocketContextFactory` | creates a context for a connection |
| `SocketContext` | implements application protocol behavior |

The server is still the listening role. The client is still the connecting role. The connection is still the concrete peer relationship.

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

`legacy` is the non-TLS stream connection variant.

`tls` adds TLS connection handling.

RFCOMM and L2CAP can participate in that stream connection-layer pattern when the corresponding Bluetooth and TLS components are available.

The point here is architectural, not cryptographic.

Bluetooth support does not sit outside the connection-layer model. The same separation still applies:

```text
network family
  -> transport form
      -> connection handling
          -> application context
```

### What changes operationally

Bluetooth is device-near, radio-based communication. That changes the operational setting.

#### Platform and build reality

Bluetooth support depends on platform Bluetooth support.

On Linux, that usually means BlueZ and the corresponding development files must be available when building the Bluetooth-enabled components.

The framework can model RFCOMM and L2CAP as lower communication families, but the build can only provide those components where the platform Bluetooth stack and development files are available.

That is normal for system-level Bluetooth support. SNode.C exposes RFCOMM and L2CAP as lower communication families, while still respecting the platform dependency.

#### Pairing, permissions, and adapter state

Bluetooth also has operational state outside the application process.

Before SNode.C can establish a Bluetooth connection between two devices, the devices must be paired by hand or by the surrounding system administration process. Depending on the platform setup, they may also need to be trusted, visible to the relevant adapter, and permitted by the local Bluetooth service policy.

That means Bluetooth failures should not be diagnosed only as SNode.C configuration failures.

The application may have selected the right family, address, and service selector while the platform still refuses the connection because pairing, adapter state, permissions, or service availability are not in the expected state.

For SNode.C code, the practical rule is:

```text
First make Bluetooth communication possible at the operating-system level.
Then let SNode.C use that endpoint identity through its normal listen/connect model.
```

This keeps framework concerns and Bluetooth administration concerns separate.

#### Device-near and IoT systems

Bluetooth matters especially in device-near systems.

A system may combine several communication worlds:

- Bluetooth for local radio-based device communication,
- Unix domain sockets for local process-to-process communication,
- IPv4 or IPv6 for network communication,
- TLS for connection-layer security where appropriate,
- HTTP, WebSocket, MQTT, or other protocols above the lower layers.

SNode.C's value is that these worlds can be understood through one layered model instead of as unrelated programming domains.

This is especially useful in IoT and embedded systems, where local device communication and network communication often coexist.

### What to remember

- Bluetooth support in this part is represented by two lower communication families: RFCOMM in `net::rc` and L2CAP in `net::l2`.
- RFCOMM endpoint identity is Bluetooth address plus channel; L2CAP endpoint identity is Bluetooth address plus PSM.
- Channel and PSM are not interchangeable service selectors.
- The application-side handle, registered instance, connection, factory, context, callbacks, and runtime model remain structurally familiar.
- Bluetooth convenience calls configure the application-side handle and then enter the usual registration path.
- The Bluetooth wildcard or deferred endpoint shape is the wildcard Bluetooth address plus service selector `0`.
- Devices must be paired at the operating-system Bluetooth level before SNode.C can use RFCOMM or L2CAP between them.
- Bluetooth support depends on platform Bluetooth support and build availability.

### Closing perspective

Chapter 10 covered host-plus-port endpoint identity through IPv4 and IPv6. Chapter 11 replaced that with Unix-domain path identity.

This chapter replaced it again with Bluetooth-specific endpoint identities:

- Bluetooth address plus RFCOMM channel,
- Bluetooth address plus L2CAP PSM.

That completes the lower-family tour of this part of the book.

The next part can now move upward. The question becomes less "Which endpoint family carries the connection?" and more "How should protocol behavior be written inside a `SocketContext`, and how should factories create those contexts?"
