## Bluetooth in SNode.C: RFCOMM and L2CAP {#bluetooth-in-snodec-rfcomm-and-l2cap}

::: {.snodec-objectives title="Learning objectives"}
- **O1.** Construct and inspect Bluetooth device identities with distinct channel and PSM selectors.
- **O2.** Diagnose which build, controller, pairing, service, or protocol stage prevents a Bluetooth exchange.
- **O3.** Choose a local measurement network family using observed endpoint identities and cleanup behavior.
:::

\index{Bluetooth}
\index{RFCOMM}
\index{L2CAP}

### Device identity and service selectors

Bluetooth is local in a different sense from Unix-domain sockets: the peer is nearby, device-specific, and mediated by the platform Bluetooth stack.

Bluetooth uses device identity plus a family-specific service selector: an RFCOMM channel or an L2CAP PSM.

After IPv4, IPv6, and Unix domain sockets, Bluetooth is the final network-family variation before the focus moves upward to application protocol contexts.

The first task is to identify which service the peer actually offers. A device address alone is not enough, and changing `rc` to `l2` in a type name does not translate an RFCOMM service into an L2CAP service. Once the matching endpoint is available, the existing factory/context model supplies protocol behavior over it.

\index{Bluetooth!service selectors}
\index{RFCOMM!channel}
\index{L2CAP!PSM}

SNode.C represents Bluetooth through two distinct network families:

| Aspect | RFCOMM | L2CAP |
|---|---|---|
| Namespace | `net::rc` | `net::l2` |
| Address class | `net::rc::SocketAddress` | `net::l2::SocketAddress` |
| Endpoint identity | Bluetooth address + channel | Bluetooth address + PSM |
| Service selector | channel | PSM |
| Server side | `SocketServer` | `SocketServer` |
| Client side | `SocketClient` | `SocketClient` |
| Context/factory model | stable | stable |
| Runtime model | stable | stable |

\index{RFCOMM}
\index{Bluetooth!RFCOMM}
\index{net::rc::SocketAddress@\texttt{net::rc::SocketAddress}}

RFCOMM endpoint identity is built from a Bluetooth device address plus an RFCOMM channel. A typical pair is `10:3D:1C:AC:BA:9C` with channel `16`. The channel is the RFCOMM service selector; it should not be treated as a generic "Bluetooth port" in the IP sense. SNode.C keeps that vocabulary visible in the API through `setBtAddress(...)` and `setChannel(...)`.

\index{L2CAP}
\index{Bluetooth!L2CAP}
\index{net::l2::SocketAddress@\texttt{net::l2::SocketAddress}}

L2CAP endpoint identity is built from a Bluetooth device address plus an L2CAP PSM. A typical pair is `10:3D:1C:AC:BA:9C` with PSM `0x1001`. The PSM is the L2CAP service selector, not the same concept as an RFCOMM channel. SNode.C keeps that vocabulary visible in the API through `setBtAddress(...)` and `setPsm(...)`: the shared Bluetooth-address part makes RFCOMM and L2CAP look related, while the service-selector part keeps them distinct.

Channel and PSM are not interchangeable. Separate address classes and setters preserve the distinction even when the surrounding application uses the same factory/context model.

\index{Bluetooth address}
\index{net::rc::SocketAddress@\texttt{net::rc::SocketAddress}}
\index{net::l2::SocketAddress@\texttt{net::l2::SocketAddress}}

The address classes make the RFCOMM/L2CAP distinction concrete: their setters, getters, constructors, and string rendering expose the two pieces of endpoint identity for each family.

The RFCOMM address class is:

```cpp
net::rc::SocketAddress
```

Construction may supply a device address, channel, both, or an existing socket address. Initialization and `getBtAddress()` / `getChannel()` expose those fields; `toString()` renders them.

A compact code anchor is:

```cpp
net::rc::SocketAddress address("10:3D:1C:AC:BA:9C", 16);
```

The L2CAP address class is:

```cpp
net::l2::SocketAddress
```

Its construction, initialization, Bluetooth-address access, and string rendering follow the RFCOMM shape above. The family-specific operations use a PSM: construction from a PSM or Bluetooth address plus PSM, construction from an existing L2CAP socket address, and `setPsm(...)` / `getPsm()`.

A compact code anchor is:

```cpp
net::l2::SocketAddress address("10:3D:1C:AC:BA:9C", 0x1001);
```

As in Chapter 7, distinguish initial configuration from a usable endpoint. `getBtAddress()` starts empty; explicit `00:00:00:00:00:00` denotes a wildcard device address. Select a real peer before connecting.

The service selector starts at zero:

| Family | Initial configuration |
|---|---|
| RFCOMM | empty configured device, channel `0` |
| L2CAP | empty configured device, PSM `0` |

### Configuring local and remote Bluetooth addresses

\index{Bluetooth!server/client use}
\index{listen()@\texttt{listen()}}
\index{connect()@\texttt{connect()}}

The stream Bluetooth wrappers follow the SNode.C pattern already seen for IPv4, IPv6, and Unix domain sockets. The convenience calls configure the handle and then enter the usual registration path.

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

For a server, the supplied address/channel configures the local endpoint; a backlog configures pending acceptance.

A simple RFCOMM client may look like this:

```cpp
using RcClient = net::rc::stream::legacy::SocketClient<MyFactory>;

RcClient client("echo-rc-client");
client.connect("10:3D:1C:AC:BA:9C", 16, onStatus);
```

For a client, address/channel selects the remote peer. Optional bind arguments refine the local Bluetooth address, the local channel, or both.

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

The L2CAP listener uses the same local-address/backlog pattern, with a PSM instead of a channel.

A simple L2CAP client may look like this:

```cpp
using L2Client = net::l2::stream::legacy::SocketClient<MyFactory>;

L2Client client("echo-l2-client");
client.connect("10:3D:1C:AC:BA:9C", 0x1001, onStatus);
```

The L2CAP client selects a remote address/PSM and can specify a local address, PSM, or both. As Chapter 8 established, changing the family does not erase local/remote direction.

### Prepare an equipped Bluetooth exchange

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

Pairing is therefore a platform and service requirement, not an unconditional requirement imposed by these SNode.C socket wrappers. SNode.C uses the prepared Bluetooth stack as a network family; it does not replace controller setup, discovery, pairing, or authorization. Once those prerequisites are satisfied and the peer service is running, the ordinary listen/connect path can establish the application connection. The addressing choices are the ones already explained above.

### Reusable protocol, explicit operating assumptions

A `SocketContext` implementing a stream protocol does not need to become fundamentally RFCOMM-specific or L2CAP-specific just because it is carried over:

```cpp
net::rc::stream::legacy
```

or:

```cpp
net::l2::stream::legacy
```

Byte parsing and response selection may remain unchanged. Timing and trust assumptions still need review: a protocol tested on a local IP loopback connection has not established that its deadlines or peer-selection policy suit the chosen Bluetooth service. Keep the parser reusable where possible, while making those deployment policies explicit through the endpoint and application configuration.

Chapter 5 introduced `legacy` and `tls` as connection-layer variants: `legacy` is the non-TLS stream connection variant, while `tls` adds TLS connection handling. RFCOMM and L2CAP can participate in that stream connection-layer pattern when the corresponding Bluetooth and TLS components are available. The point here is architectural, not cryptographic: Bluetooth support does not sit outside the connection-layer model, and the same separation still applies to network family, transport form, connection handling, and application context.

\index{Bluetooth!deployment}
\index{permissions}

Bluetooth is device-near, radio-based communication, so it changes the operational setting.

Build availability and operating hardware are separate observations. If the installed SNode.C package does not contain the requested Bluetooth component, attaching an adapter will not supply the missing library. Conversely, a successfully built Bluetooth example can still run on a host with no usable controller. Check component discovery when building the consumer and controller state when preparing to run it; pairing does not repair a missing build dependency.

A Bluetooth connection can fail before the application context receives a byte. Use the preparation sequence above to distinguish an unavailable controller, an unprepared device relationship, denied service access, and a peer service that has not been started. Rewriting the parser does not repair any of those conditions.

Conversely, successful pairing alone says nothing about the application's messages. Once the connection is ready, the context is responsible for the same framing and protocol behavior taught in the neighboring chapters. The distinction lets a reader inspect a sample program in two stages: what the platform must provide before activation, and what the context does after activation.

The preparation guide establishes what must be ready before a Bluetooth example can run. The selected adapter, peer service, and operating-system policy determine the actual connection outcome. Chapter 12 develops protocol transfer with IPv4 and Unix-domain sockets, where the reader can observe that behavior without Bluetooth hardware.

A device-near application may combine Bluetooth input, Unix-domain local helpers, IP networking, and HTTP or MQTT above them. Keep the input family distinct from both its protocol and the application’s accepted measurement state.

### Public components and the Part III checkpoint

\index{net::rc::stream::legacy@\texttt{net::rc::stream::legacy}}
\index{net::l2::stream::legacy@\texttt{net::l2::stream::legacy}}

Bluetooth stream types follow the same source/build rule, but only when the required Bluetooth development support is present. RFCOMM uses the `rc` family fragment:

```cpp
#include <net/rc/stream/legacy/SocketServer.h>
#include <net/rc/stream/legacy/SocketClient.h>
```

with the corresponding component:

`net-rc-stream-legacy`.

L2CAP uses the `l2` fragment:

```cpp
#include <net/l2/stream/legacy/SocketServer.h>
#include <net/l2/stream/legacy/SocketClient.h>
```

with the corresponding component:

`net-l2-stream-legacy`.

The local lesson is the conditional family surface. Chapter 27 gives the broader include/component matrix.

The Part III checkpoint compares two usable local producer endpoints before requiring radio equipment. Its thin drivers link the same EchoPair context and factory over IPv4 and Unix-domain streams. Send the same measurement-shaped bytes, then compare the actual peer and service identities. The Unix fixture owns a private directory: the server removes its socket path, the producer removes its own, and an unrelated file remains intact. Choosing a network family changes those responsibilities without yet adding parsing or acceptance to the measurement model.

::: {.snodec-remember title="What to remember"}
- A Bluetooth device address needs the service selector of the chosen family: RFCOMM channel or L2CAP PSM.
- Building a component, powering a controller, pairing, starting a service, and receiving bytes are separate observations.
- Local and remote direction remains explicit even when both endpoints use Bluetooth identities.
- Reusable byte handling does not transfer timing, security, or deployment assumptions automatically.
- Use actual endpoint and cleanup observations to choose a network family; echoed bytes have not yet become accepted measurements.
:::

::: {.snodec-exercise title="Exercises"}
1. **Review (O1).** Explain why a discovered device address plus RFCOMM channel 16 cannot be reused as an L2CAP endpoint merely by changing the namespace.
2. **Review (O2).** The Bluetooth consumer builds and the peer is paired, but no application bytes arrive. Give an ordered diagnosis that distinguishes controller availability, service readiness, authorization, and protocol behavior.
3. **Lab (O1).** Build and run the hardware-independent selector solution. Expect default device/selector values, then the same device with channel 16 and PSM 4097 (`0x1001`). Explain why these observations do not demonstrate radio reachability. An optional equipped exchange is described with the public solution.
4. **Lab (O3).** Run the Part III checkpoint: exchange the same measurement bytes over IPv4 loopback and a temporary Unix path. Expect exact replies, distinct actual identities, and owned-path cleanup. Choose the local producer endpoint from those observations; explain why reflection is not measurement acceptance.
5. **Design (O2, O3).** A nearby sensor supplies only an advertised BLE service, while a local helper supplies a pathname stream. Decide what additional evidence or adapter is needed before choosing an RFCOMM/L2CAP input. Keep transport choice separate from measurement validation and acceptance.

Public answers, commands, and observations: `companion/exercises/ch09/README.md`.
:::
