# From Raw Connections to Application Protocols

The previous part showed that endpoint identity changes with the lower family. This part asks how application protocol meaning can remain recognizable anyway.

The focus is `SocketContext`, `SocketContextFactory`, and the transfer of one protocol shape across several lower layers. The lesson is not that carriers are irrelevant; it is that protocol behavior, context construction, carrier selection, and deployment policy become easier to reason about when each has a clear home. Part V then makes those choices visible through configuration and diagnostics.
