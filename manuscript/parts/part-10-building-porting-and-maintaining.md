# Building, Porting, and Maintaining

Part IX moved from durable state to complete applications and then to cooperating processes. This part asks how those systems remain trustworthy after they leave the source tree.

CMake components, public headers, install surfaces, package dependencies, Linux/OpenWrt deployment, testing, debugging, and benchmarking are treated as part of the same architectural story. Part XI then uses the accumulated material to build MiniGateway as a complete guided system.

The checkpoint rebuilds EchoPair as an external consumer, installs it privately, separates a wrong endpoint from a build failure, and records a bounded latency measurement. Keep the installation, operating conditions and limits with each result.
