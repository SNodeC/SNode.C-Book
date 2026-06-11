# Networking Foundations in SNode.C

This part walks through the lower communication families that make SNode.C concrete. IPv4, IPv6, Unix domain sockets, Bluetooth RFCOMM, and Bluetooth L2CAP are not treated as interchangeable address spellings. They are different boundary choices with different deployment assumptions.

The purpose is to make lower-family selection visible before higher protocol layers are added.
