# From Raw Connections to Application Protocols

The previous part showed that endpoint identity changes with the network family. This part asks how application protocol meaning can remain recognizable anyway.

The focus is `SocketContext`, `SocketContextFactory`, and the transfer of one protocol shape across several lower layers. The lesson is not that network families are irrelevant; it is that protocol behavior, context construction, network-family selection, and deployment policy become easier to reason about when each has a clear home. Part V then makes those choices visible through configuration and diagnostics.

The Part IV checkpoint keeps the line parser and factory fixed while transferring fragmented and coalesced commands between IPv4 and a private Unix path. Compare reconstructed replies and distinguish an unreachable endpoint from an invalid command. These framing rules prepare the measurement input; domain validation and acceptance remain separate.
