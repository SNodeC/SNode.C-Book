# From Raw Connections to Application Protocols

This part moves from configured lower-family connections to protocol behavior. It focuses on writing `SocketContext` and `SocketContextFactory` classes well and then shows how the same protocol idea can remain recognizable over different lower layers.

The central lesson is that protocol meaning should live at the layer that can honestly own it.
