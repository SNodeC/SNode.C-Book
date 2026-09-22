# Networking Foundations in SNode.C

Part II established the runtime and layered vocabulary. This part puts that vocabulary under pressure by changing the lower communication family.

IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP are not interchangeable spellings for the same idea. Each carries its own endpoint identity, deployment assumptions, and operating-system reality. After this tour, Part IV can ask which parts of a protocol can remain stable when the carrier changes.

The Part III checkpoint chooses an endpoint for a local measurement producer by comparing the same byte exchange over loopback IP and a temporary Unix path. Bluetooth address exercises need no radio; the additional physical exchange is an equipped lab with explicit preparation.
