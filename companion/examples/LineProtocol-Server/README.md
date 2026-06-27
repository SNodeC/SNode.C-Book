# LineProtocol-Server

This compact example is the runnable server counterpart to the line-command
`SocketContext` introduced in Chapter 13.

It listens on IPv4 TCP port `8090` using the legacy stream stack:

```text
net::in::stream::legacy::SocketServer<LineCommandServerContextFactory>
```

For each connection, the server sends a greeting line:

```text
READY
```

It then accepts the following line commands:

```text
PING    -> PONG
STATUS  -> OK
QUIT    -> close the connection
other   -> ERR unknown command
```

Build the example against an installed SNode.C package:

```bash
cmake -S companion/examples/LineProtocol-Server -B build/line-protocol-server \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build/line-protocol-server
```

Run the server before starting `LineProtocol-Client`.
