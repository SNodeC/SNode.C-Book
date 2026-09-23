# P4/P5 API and gate evidence

Framework remains frozen at 07ca9a29. Inspected declarations: src/net/config/ConfigPhysicalSocket.h:83 setRetry, :86 setRetryOnFatal, :89 setRetryTimeout, :92 setRetryTries (0 unlimited), :95 setRetryBase, :98 setRetryLimit, :101 setRetryJitter; src/net/config/ConfigPhysicalSocketClient.h:70 setReconnect, :73 setReconnectTime; src/core/socket/Socket.h:73 getConfig.

The exact new setter sequence compiles in an isolated copy of the canonical EchoPair client against the new R2 installation (P4-retry-api-build.log). No canonical C++ or driver source was edited. The unchanged ch16 recovery tests run the corresponding CLI policy and distinguish initial-attempt retry from post-connection recovery. Added retry-on-fatal=false and retry-limit=1 spellings match the configuration declarations, and are explicit defaults/cap in the teaching example; no test policy was changed.

The configured TLS box uses existing ch15/tls.py server flags --cert and --cert-key and its Python ssl.create_default_context(cafile=...) / wrap_socket(server_hostname=...) operations. It does not add a C++ API or teach new TLS internals. Existing trust/identity and secure echo tests pass. MQTT-over-WebSocket trace retains the adapter implementation and existing binary/text tests; the IoT decision preserves one model authority. Eight focused labs pass across ch15, ch16, ch22 and ch23; full exit suites remain P7 work.

P4 source metrics and P5 source metrics are separate fresh measurements. The P4 projection was below 113,500, so optional rows 30 and 31 were implemented. P4/P5 alter manuscript/support documentation only: no application, test, driver or timeout changes. The API probe is ignored build support, not a new companion implementation.

Source provenance is confined to the Ch2 sidebar and source-baseline documentation. Preface retains one version/commit sentence to satisfy source alignment. Operational SDK source selection refers back to Ch2 without repeating pin reconstruction mechanics.
