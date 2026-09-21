# CI Behavioral Smoke Tests

The book uses two deliberately separate runtime check groups. Results belong to
the exact book commit and pinned framework commit in each workflow run.

## Teaching examples

`ci/run-teaching-smoke-tests.py` checks the Chapter 18 public logging example by
parsing its actual JSON records. It also checks the Chapter 3 echo server and
client against controlled Python socket peers. Received data is accumulated;
tests do not equate a TCP read with an application message.

## Integrated showcase

`ci/run-behavior-smoke-tests.py` and its shell entry point retain the selected SSE
and MiniGateway Extended checks: health, one Unix-domain measurement, resulting
HTTP state, and the same measurement in an SSE event. The source commands remain:

```text
sse-server legacy local --port 8080
minigateway-extended mqtt-uplink remote --host 127.0.0.1 --port 1883
```

The MQTT role is configured for its normal retry behavior; no live broker is
required by this test. Passing does not prove MQTT delivery.

## Framework tests and limits

The build script separately enables the framework's registered CTest suite.
That suite is distinct from these book application checks. Test discovery,
results, and skip conditions are retained in the workflow output and uploaded
logs. Bluetooth hardware, full MQTT topologies, MariaDB service integration,
OpenWrt packages, load tests, and long-running supervision are not certified by
these selected checks. The historical pre-migration status record is retained
under `history/ci-behavior-smoke-tests.md`.
