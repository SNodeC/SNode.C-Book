# IoT and Message-Oriented Systems

The web chapters ended with upgraded and long-lived communication. This part introduces MQTT and then places it beside WebSocket and HTTP as one surface in larger IoT designs.

Native MQTT, MQTT over WebSocket, and multi-protocol systems are treated as choices about who talks to whom, through which surface, and for what purpose. Part IX then adds durable application state and reads complete applications as systems rather than isolated protocol examples.

The checkpoint observes a publication at an independent broker subscriber, then checks that local gateway state remains observable when MQTT is unavailable. Keep session, subscription, delivery and application acceptance separate as these roles join the running project.
