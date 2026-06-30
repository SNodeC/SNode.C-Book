# CI Behavioral Smoke Tests

This package includes a deliberately small runtime smoke-test layer in addition
to the companion-example compile checks. For the current package, this CI layer
is complete and has been confirmed in the public GitHub Actions workflow.

The smoke tests live in:

```text
ci/run-behavior-smoke-tests.sh
ci/run-behavior-smoke-tests.py
```

They are executed by `.github/workflows/companion-examples.yml` after the pinned
SNode.C release and the companion examples have been built. The workflow runs the
checks in the existing GCC/Clang compiler matrix. The checked status for this
package is: companion-example build verification complete; selected behavioral
smoke-test verification complete.

## Covered paths

The smoke tests cover selected showcase behavior only:

- start `sse-server`;
- request `/events` with `Accept: text/event-stream`;
- verify that the response is an SSE measurement event with `event:`, `id:`, and
  JSON `data:` fields;
- start `minigateway-extended`;
- verify `/health`;
- inject one measurement through `/tmp/minigateway-measurements.sock`;
- verify that `/status` exposes the accepted measurement with sequence `1`;
- verify that `/events` exposes the same accepted measurement as an SSE event.


## Runtime command lines

The smoke tests use explicit SNode.C command lines instead of guessing missing
subcommands from CLI errors. The selected command lines are:

```text
sse-server legacy local --port 8080
minigateway-extended mqtt-uplink remote --host 127.0.0.1 --port 1883
```

`SSE-Server` uses a parameterless `listen(...)`, so the smoke test supplies the
required `legacy local --port` configuration explicitly. The default port is `8080`,
matching `SSE-EventSource-Client`, which connects to `127.0.0.1:8080`. MiniGateway Extended
sets the HTTP listener port and Unix-domain socket path in the source, but its
MQTT client role still needs a configured remote endpoint for the parameterless
`connect(...)` path. The smoke test does not require a live MQTT broker; it
exercises the HTTP/SSE and Unix-domain input paths while the MQTT role remains
configured for retry/reconnect behavior.

## Deliberate limits

These checks are smoke tests, not a full integration-test suite. They do not run
an external MQTT broker, exercise OpenWrt packaging, perform load tests, run
long-lived service supervision checks, or claim broad third-party validation.
Their purpose is to close the most important gap between “the examples compile”
and “the showcase event-stream and Unix-domain input paths behave as described.”
For this package, that selected smoke-test layer is no longer an open item.
