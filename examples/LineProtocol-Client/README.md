# LineProtocol-Client

This compact example is the runnable client counterpart to the line-command
`SocketContext` introduced in Chapter 13.

It connects to `localhost:8090` using the legacy IPv4 stream stack:

```text
net::in::stream::legacy::SocketClient<LineCommandClientContextFactory>
```

After the server sends `READY`, the client sends this short command sequence:

```text
PING
STATUS
UNKNOWN
QUIT
```

The expected response sequence before the final close is:

```text
READY
PONG
OK
ERR unknown command
```

Build the example against an installed SNode.C package:

```bash
cmake -S examples/LineProtocol-Client -B build/line-protocol-client \
    -Dsnodec_DIR=/path/to/snodec/lib/cmake/snodec
cmake --build build/line-protocol-client
```

Start `LineProtocol-Server` first, then run this client.
