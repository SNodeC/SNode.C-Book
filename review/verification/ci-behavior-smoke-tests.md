# CI Behavioral Smoke Tests

This package includes a deliberately small runtime smoke-test layer in addition
to the companion-example compile checks.

The smoke tests live in:

```text
ci/run-behavior-smoke-tests.sh
ci/run-behavior-smoke-tests.py
```

They are executed by `.github/workflows/companion-examples.yml` after the pinned
SNode.C release and the companion examples have been built. The workflow runs the
checks in the existing GCC/Clang compiler matrix.

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

## Deliberate limits

These checks are smoke tests, not a full integration-test suite. They do not run
an external MQTT broker, exercise OpenWrt packaging, perform load tests, run
long-lived service supervision checks, or claim broad third-party validation.
Their purpose is to close the most important gap between “the examples compile”
and “the showcase event-stream and Unix-domain input paths behave as described.”
