# Terminology allowlist — P1

Every remaining carrier use is listed below, including capitalization, plurals
and preserved anchor IDs. Chapter numbers here are pre-split; P2 updates paths.
No carrier use outside these locations is permitted.

| Location | Use | Reason |
|---|---|---|
| manuscript/frontmatter/conventions.md:37 | `/ **Carrier** / In the MQTT chapters only, the` | Canonical glossary entry |
| manuscript/chapters/14-tls-across-the-framework.md:193 | `and protocol decisions {#carrier-and-protocol-decisions}` | Preserved heading ID |
| manuscript/chapters/20-mqtt-support-in-snodec.md:4 | `ckets, session state and carrier contexts divide responsibilities.` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:6 | `- **O3.** Choose carrier and delivery evidence for a broker` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:19 | `Chapter 21 develops that carrier choice.` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:36 | ` protocol object and the carrier underneath /` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:45 | `### `Mqtt` and its carriers` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:53 | `nt, it is connected to a carrier through `MqttContext` and either a` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:96 | ` protocol object and the carrier underneath /` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:99 | `ocol object to whichever carrier is used underneath, letting it rea` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:211 | `o a stream or to another carrier. The MQTT role itself shows the pr` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:231 | `/ carrier established / connection identity ` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:246 | `The WebSocket carrier substitutes a subprotocol role for` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:246 | `e remains the same; keep carrier selection separate from session an` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:284 | `to a native or WebSocket carrier.` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/20-mqtt-support-in-snodec.md:292 | ` control packet from its carrier through the deserializer to its MQ` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:11 | `\index{WebSocket!MQTT carrier}` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:25 | `n diagnostic cost of the carrier composition, and the reason to kee` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:30 | `frames. The point is the carrier contrast, not a split in MQTT sema` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:32 | `antics but use different carrier paths.](assets/figures/pdf/fig-07-` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:36 | `/ carrier / stream connection / WebSocket co` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:43 | `astructure requires that carrier, but adds upgrade configuration, s` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:63 | `le supplies the upgraded carrier surface. `MqttContext` supplies th` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:72 | `urface. MQTT sees either carrier through `MqttContext`, rather than` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:74 | `et is a message-oriented carrier. MQTT is a byte-oriented packet pr` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:110 | `ed bidirectional message carrier, framing, binary payload delivery,` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:156 | ` selecting the WebSocket carrier. The MQTT role remains an MQTT rol` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:168 | `apter, and the WebSocket carrier. The corresponding server-side com` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:210 | `he adapter while keeping carrier roles explicit.` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/21-mqtt-over-websocket.md:219 | `treating text as a valid carrier choice.` | MQTT native-stream versus WebSocket comparison |
| manuscript/chapters/22-designing-iot-systems-with-multiple-protocols.md:133 | ` boundary {#choosing-the-carrier-at-each-boundary}` | Preserved heading ID |

## Context-dependent survivors

All remaining uses mean system-design responsibilities:

- manuscript/chapters/01-why-snodec-exists.md:54: SNode.C is not trying to replace every C++ networking approach. It is most useful when an application needs explicit communication roles, layered protocol structure, runtime-visible configuration, diagnostics, and several transport or protocol surfaces within one architectural model.
- manuscript/chapters/12-configuring-applications-and-named-instances.md:6: - **O3.** Decide which communication roles need independent configuration and lifecycle control.
- manuscript/chapters/12-configuring-applications-and-named-instances.md:15: Configuration is where architectural choices become adjustable by the operator. The context still implements the protocol and the factory creates contexts, but the application must choose its communication roles, endpoint values, connection variants and enablement.
- manuscript/chapters/24-snodec-in-larger-systems.md:315: The role `database-state` is intentionally different from `admin-http` or `mqtt-ingest`. It is not the same kind of communication role as a socket server or client. It names the persistence boundary that owns durable application state.
- manuscript/chapters/28-building-minigateway.md:14: ### One model, several communication roles
- manuscript/chapters/28-building-minigateway.md:1235: - an MQTT client role for measurement input and output;
- manuscript/chapters/29-extending-minigateway-with-a-new-network-role.md:30: The new concern is local measurement injection through a Unix-domain stream socket. That concern belongs to a new socket-server role. It does not belong in the HTTP route code, the SSE response path, or the MQTT client context.

No server-instance or client-instance forms remain. Exact `Role` API names and
role enum values retain their spelling; these name protocol-side choices in code.
Stable heading IDs, figure IDs and historical filenames containing lower-family
wording remain resolvable and are not renamed for a vocabulary count.
