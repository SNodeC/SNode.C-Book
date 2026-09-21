#!/usr/bin/env python3
"""Apply the reviewed, remaining SNode.C 2.0 editorial changes once.

This is temporary migration tooling. It edits only the explicit book surfaces
below, never the framework checkout, and refuses an unexpected starting tree.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "0ac82c284b2682ddedb6f04d8affaeeb8d5c003d"
PIN = "1f0f728fc9b3b45174f2cd790d83b2f493e58af1"
OLD_PIN = "6e475262084ae2dab2daef8781ab9e4adb82d18e"
changes: dict[Path, str] = {}


def load(path: Path) -> str:
    return changes.get(path, path.read_text(encoding="utf-8"))


def chapter(number: int) -> Path:
    matches = list((ROOT / "manuscript/chapters").glob(f"{number:02}-*.md"))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Chapter {number}, got {matches}")
    return matches[0]


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"Expected one editorial anchor: {old[:100]!r}")
    return text.replace(old, new, 1)


def insert_before(number: int, heading: str, addition: str) -> None:
    path = chapter(number)
    changes[path] = replace_once(load(path), heading, addition.strip() + "\n\n" + heading)


def migrate_code(text: str) -> str:
    def block(match: re.Match[str]) -> str:
        body = match[2].replace("#include <log/Logger.h>", "#include <Log.h>")
        levels = {"TRACE": "trace", "DEBUG": "debug", "INFO": "info",
                  "WARNING": "warn", "ERROR": "error", "FATAL": "critical"}
        body = re.sub(r"\bPLOG\(ERROR\)",
                      "snode::log::application().systemError(snode::log::Level::Error, errnum)", body)
        body = re.sub(r"\bLOG\((TRACE|DEBUG|INFO|WARNING|ERROR|FATAL)\)",
                      lambda m: "snode::log::application()." + levels[m[1]] + "()", body)
        body = re.sub(r"\bVLOG\([0-9]+\)", "snode::log::application().trace()", body)
        return "```" + match[1] + "\n" + body + "\n```"
    return re.sub(r"```(cpp|cmake)\n(.*?)\n```", block, text, flags=re.S)


def sync_named_files(number: int, example: str, expected: int) -> None:
    path = chapter(number)
    text = load(path)
    edits = []
    for heading in re.finditer(r"^#### `([^`]+)`[ \t]*$", text, re.M):
        name = heading[1]
        if name != "CMakeLists.txt" and not name.endswith((".cpp", ".h")):
            continue
        source = ROOT / "companion/examples" / example / name
        if not source.is_file():
            raise RuntimeError(f"Missing source of truth: {source}")
        listing = re.search(r"```(cpp|cmake)\n(.*?)\n```", text[heading.end():], re.S)
        if not listing:
            raise RuntimeError(f"Missing listing after {name}")
        start = heading.end() + listing.start()
        end = heading.end() + listing.end()
        if re.search(r"^#{2,4} ", text[heading.end():start], re.M):
            raise RuntimeError(f"Listing crossed a section boundary after {name}")
        replacement = ("<!-- snodec-source: " + source.relative_to(ROOT).as_posix() +
                       " -->\n```" + listing[1] + "\n" +
                       source.read_text().rstrip("\n") + "\n```")
        edits.append((start, end, replacement))
    if len(edits) != expected:
        raise RuntimeError(f"Chapter {number}: expected {expected} complete listings, found {len(edits)}")
    for start, end, replacement in reversed(edits):
        text = text[:start] + replacement + text[end:]
    changes[path] = text


def sync_program(number: int, identifying_include: str, source_name: str) -> None:
    path = chapter(number)
    count = 0
    def listing(match: re.Match[str]) -> str:
        nonlocal count
        if identifying_include not in match[1] or "int main(" not in match[1]:
            return match[0]
        count += 1
        source = ROOT / source_name
        return ("<!-- snodec-source: " + source_name + " -->\n```cpp\n" +
                source.read_text().rstrip("\n") + "\n```")
    changes[path] = re.sub(r"```cpp\n(.*?)\n```", listing, load(path), flags=re.S)
    if count != 1:
        raise RuntimeError(f"Chapter {number}: expected one complete program, got {count}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-snapshot", action="store_true")
    args = parser.parse_args()
    if not args.local_snapshot:
        subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=True)
        subprocess.run(["git", "diff", "--exit-code", BASE, "--", "manuscript", "companion",
                        "review/proposal", "production/metadata"], cwd=ROOT, check=True)

    sync_named_files(35, "MiniGateway", 19)
    sync_named_files(36, "MiniGateway-Extended", 8)
    sync_program(23, "<web/http/legacy/in/EventSource.h>",
                 "companion/examples/SSE-EventSource-Client/main.cpp")
    sync_program(28, "<database/mariadb/MariaDBClient.h>",
                 "companion/examples/MariaDB-Minimal/main.cpp")
    for number in [23, 24, 25, 28, 29, 38]:
        path = chapter(number)
        changes[path] = migrate_code(load(path))

    insert_before(23, "### Retry and continuity", r'''
### Resource policy for an open event stream

\index{SSE!resource limits}
\index{SSE!backpressure}

An event stream passes through more than one resource boundary. The HTTP client validates the response headers under the shared parser policy from Chapter 21. Once a valid EventSource response switches to the raw event receiver, the HTTP body parser no longer accumulates that stream. Its `maximum-body-bytes` setting is therefore not a lifetime byte budget for SSE. Header limits still apply.

This exception is intentional. A successful event stream can remain open while it delivers an unbounded number of individually bounded events. The EventSource receiver's line and accumulated-event guards protect local parsing; they do not define how many events the application may retain, how much history it should replay, or how long an observer may remain attached.

The server has a different pressure boundary. Its response fragments pass through the connection's write queue. A finite `maximum-write-queue-bytes` and the queue watermarks belong to the connection configuration described in Chapter 20. They do not turn a callback-driven measurement publisher into a source that automatically pauses whenever a browser is slow. Automatic source suspension applies to attached `core::pipe::Source` objects; a publisher that invokes response methods directly still needs its own slow-observer policy.

For the compact example, the important distinction is between the accepted measurement and its delivery to one observer. A stalled observer must not become the owner of application state. A deployment can deliberately disconnect a slow observer, retain a bounded replay history, or reduce the update rate. Those are application choices around the framework's queue contract, not new SSE syntax.

A disconnect or queue-admission failure also does not prove that an event reached the peer. Event IDs provide a continuity mechanism when the application supplies a corresponding replay policy. They are not delivery acknowledgements. Tests should observe the emitted stream and the reconnect behavior separately from the model's decision to accept a measurement.
''')

    insert_before(24, "### Lower layers and diagnostics still matter", r'''
### Receiver limits belong to the selected connection

\index{WebSocket!receiver limits}
\index{WebSocket!close code 1009}
\index{ConfigWebSocket@\texttt{ConfigWebSocket}}

WebSocket preserves message boundaries above a stream, but preserving a boundary is not the same thing as allowing an unlimited message. SNode.C exposes receiver resource policy through the HTTP instance's `websocket` configuration section. The upgrade takes a snapshot of that policy for the receiver it creates.

| Option | Boundary it limits |
|---|---|
| `maximum-frame-bytes` | payload bytes in one frame, including control frames |
| `maximum-message-bytes` | accumulated data bytes across a fragmented message |
| `maximum-fragments` | data-frame count within one message |

The defaults are zero, meaning unlimited for these configurable resource limits. Protocol validity rules still apply; an unlimited resource setting does not make an invalid WebSocket frame valid. A finite frame bound alone is also insufficient to bound a message assembled from many smaller frames. The three settings protect different dimensions of the same receiver.

A receiver resource-limit violation uses close code `1009`, Message Too Big. The limit is enforced at the carrier boundary before the application can treat the rejected message as accepted subprotocol data. It does not replace application validation of message contents, authorization, or command semantics.

These settings belong to startup configuration, not to an undocumented runtime setter in the subprotocol. Nor do they introduce a corresponding sender-fragmentation policy: the current limits govern receiving. Chapter 20 covers the separate bounded-output contract below WebSocket, while Chapter 34 shows the receiver-validation and real-connection tests that protect these boundaries.
''')

    insert_before(28, "### Closing perspective", r'''
### Diagnostic identity and controlled persistence checks

\index{MariaDBClient@\texttt{MariaDBClient}!diagnostic identity}

The database boundary can now participate in semantic diagnostics as well as in the event loop. `MariaDBClient` accepts an optional instance-name argument after its connection details and state callback. That name gives the database connection a useful diagnostic identity; it does not create a socket server, an MQTT role, or a separate configuration hierarchy.

The compact program uses the public application logger for its own observations. Framework-owned database records and application decisions remain different evidence. A successful connection is not a successful transaction, and a queued command is not proof that durable state has changed. Preserve those distinctions when correlating database records with HTTP, SSE, or MQTT activity.

A persistence test also needs an explicitly controlled service environment. The framework's general CTest suite and an installed-consumer build do not establish that a particular database, schema, credential set, or transaction sequence works. Use isolated state, known input, and explicit cleanup for that check. The companion program is a small integration example, not a claim that every database deployment is covered by the framework test suite.
''')

    insert_before(29, "### Reading applications in `src/apps`", r'''
### Read applications beside consumer examples and tests

The current source tree gives an application reader three complementary views. `src/apps` shows how framework developers assemble applications inside the repository. `examples/echo` shows a standalone CMake consumer of an installed SNode.C package. `tests/` records selected behaviors and architectural restrictions as executable checks.

These views should not be collapsed. An in-tree application can use the repository's build context; an installed consumer must depend on exported targets and installed headers. A component test can use controlled peers or test-only access that does not belong in application code. Reading all three makes the distinction visible rather than relying on an example's directory name as proof of public API status.

A useful route is to read an application's entry point, inspect its include and link surfaces, and then locate the test boundary that would catch a regression in the behavior being studied. For a stream application, that may be a payload-reconstruction or disconnect-lifecycle test. For an HTTP application, it may be a parser, middleware, or installed-module check. Chapter 34 develops that test taxonomy in detail.

The repository also contains design notes under `docs/` and operational tooling under `src/tools/`. Those are useful companions to source reading, but a historical migration report should not override the current header or implementation. The current public logging entry point is `<Log.h>`; the source excerpts in this chapter use that surface rather than a removed macro interface.
''')

    path = chapter(32)
    text = load(path).replace(r"\texttt{v1.0.2}", r"\texttt{2.0.0}")
    text = replace_once(text, "- applies logging-related compile definitions,",
                        "- controls sanitizer instrumentation and application selection,")
    text = replace_once(text, "descends into `src`, and then includes packaging.",
                        "descends into `src`, conditionally registers the framework tests, and then includes packaging.")
    text = replace_once(text,
        "`--as-needed` discourages unnecessary linkage. `--no-undefined` requires shared libraries to declare the dependencies they need instead of relying on a final application link step to accidentally complete missing symbols.",
        "`--as-needed` discourages unnecessary linkage. In the ordinary, non-ASan build, `--no-undefined` requires shared libraries to declare the dependencies they need instead of relying on a final application link step to accidentally complete missing symbols. The ASan branch adds sanitizer instrumentation and omits that ordinary `--no-undefined` linker option; it is a separate build configuration, not the same binary with an extra runtime switch.")
    changes[path] = text
    insert_before(32, "### Exported package targets and external consumers", r'''
### Tests, tools, and installed-header discipline

\index{SNODEC_BUILD_TESTS@\texttt{SNODEC\_BUILD\_TESTS}}
\index{SNODEC_BUILD_APPS@\texttt{SNODEC\_BUILD\_APPS}}
\index{SNODEC_ENABLE_ASAN@\texttt{SNODEC\_ENABLE\_ASAN}}
\index{installed-consumer tests}

The top-level build now distinguishes framework tests from demonstration applications. `SNODEC_BUILD_TESTS` defaults to `OFF`; enabling it registers the CTest suite below `tests/`. `SNODEC_BUILD_APPS` defaults to `ON` and controls `src/apps`. Neither switch should be inferred from the presence of an executable left in an old build directory.

A framework verification build can make its intent explicit:

```sh
cmake -S snode.c -B snode.c-build-tests \
  -DCMAKE_BUILD_TYPE=Debug \
  -DSNODEC_BUILD_TESTS=ON -DSNODEC_BUILD_APPS=ON
cmake --build snode.c-build-tests --parallel 8
ctest --test-dir snode.c-build-tests --output-on-failure
```

The external `examples/echo` project has its own `BUILD_TESTING` switch. It is configured separately against an installation; it is not enabled merely by enabling the framework's tests. Likewise, `snodec-control` has its own test and optional Curses-interface settings. Build switches belong to the project that interprets them.

`SNODEC_ENABLE_ASAN` selects AddressSanitizer instrumentation for supported GCC and Clang builds. Use a separate build directory for that configuration and rebuild its libraries and consumers consistently. Chapter 34 explains the resulting evidence and its limits; a sanitizer build is not a substitute for testing the behavior the application promises.

Public-header discipline is also tested after installation. The staged installed-consumer check verifies selected consumer includes and checks that internal orchestration headers such as `core/EventLoop.h`, `core/EventMultiplexer.h`, `core/DescriptorEventPublisher.h`, and `core/TimerEventPublisher.h` have not become installed application dependencies. An application uses the public runtime entry point; a source-level explanation of the event loop does not make every implementation header a public API.

The logging surface illustrates another useful distinction. `<Log.h>` is the application-facing header, and `snodec::logger` is an exported target reached through the component graph. The list of supported `find_package(... COMPONENTS ...)` requests is not identical to the list of every exported dependency target. The logging-only companion requests the supported `core` component and links its loaded `snodec::logger` target; it does not invent a supported `logger` request.

The backend is private to that library. Its spdlog dependency does not require application chapters to include backend headers or configure an unrelated logger. Include-What-You-Use and installed-consumer checks support the same rule from different directions: include what the public abstraction actually promises, and do not depend on incidental transitive implementation includes.

Finally, source compatibility and binary compatibility are different contracts. SNode.C 2.0 changes installed class layouts and virtual interfaces. Rebuild applications, shared libraries, and dynamically loaded protocol modules against the selected 2.0 headers and libraries together. A successfully rebuilt application does not make an old 1.x plugin ABI-compatible.
''')

    path = chapter(33)
    changes[path] = replace_once(load(path), "increase verbose level if needed",
                                "enable a narrow semantic logging override if needed")
    insert_before(33, "### Reading a deployment", r'''
### Rebuild and inspect the installed system

\index{deployment!ABI compatibility}
\index{snodec-control@\texttt{snodec-control}}

A deployment of SNode.C 2.0 must use a coherent set of rebuilt C++ artifacts. Applications and runtime-loaded extensions compiled against 1.x must not be mixed with the new shared libraries. The source-level continuity of a role name or include path is not an ABI guarantee. Rebuild the application, its protocol modules, and the libraries that derive from affected public classes as one installation set.

Inspect that installed set in the environment in which it will run. The staged installed-consumer and external echo checks from Chapter 34 provide useful package evidence, but they do not exercise a particular service account, router image, certificate directory, or database installation. Those remain deployment checks.

`snodec-control` adds an operational view of a target application's configuration. It discovers the target's configuration output, can show or edit the resulting model, and can ask the target to write its canonical configuration. Its optional Curses interface changes the presentation, not the ownership of configuration. The target application still performs final validation.

This is also why configuration metadata and semantic logs serve different purposes. Metadata describes configurable structure and values; a log record describes an occurrence at runtime. Keep both with a reproducible service setup, but do not treat a configuration preview as proof that a listener started or that a request completed.
''')

    insert_before(38, "### Extending failure policy", r'''
#### Preserve semantic identity when adding diagnostics

The semantic logger now carries the origin, boundary, component, and optional runtime identity explicitly. A new application feature should use the public `<Log.h>` facade or an appropriate inherited context helper instead of rebuilding that identity inside every English message. Framework-owned helpers may be private; their names do not make them extension APIs.

Keep the event claim as precise as the control path. Queue admission is not delivery, a connection attempt is not an established session, and a context switch is not necessarily a peer disconnect. Chapter 18 explains how those distinctions survive text and JSON output. An extension should preserve them when it adds its own diagnostics.
''')
    insert_before(38, "### Avoiding framework pollution", r'''
#### Choose the existing regression layer

SNode.C now gives the extension author concrete places to protect that contract:

| Change | First regression surface to consider |
|---|---|
| local parser, value, or state transition | `tests/unit/` |
| composed connection, routing, or protocol behavior | `tests/component/` |
| an architectural restriction on source structure | `tests/policy/` |
| public headers, exports, or package assumptions | staged installed-consumer checks |
| a standalone application assembled from the installation | external-application checks |

The table selects a starting point, not a claim that one test layer is sufficient. A queue-policy change may need both a local admission-result test and a real slow-peer scenario. A new public header needs an installed-consumer check even when its in-tree unit test passes. A source-policy test can prevent a forbidden dependency or logging shortcut without proving the associated runtime behavior.

For output-producing extensions, use the result-returning queue API when the application needs to choose a recovery policy. `WouldExceedLimit` must not be interpreted as a partially accepted message, and `Queued` must not be interpreted as acknowledged delivery. The bounded-output and shutdown contracts from Chapter 20 should remain intact as the application grows.
''')

    proposal = ROOT / "review/proposal/book-proposal-package.md"
    text = load(proposal)
    text = text.replace("public release tag `v1.0.2`", "project version `2.0.0`")
    text = text.replace("release tag `v1.0.2`", "project version `2.0.0`")
    text = text.replace("SNode.C `v1.0.2`", "SNode.C `2.0.0`").replace(OLD_PIN, PIN)
    text = replace_once(text,
        "The reader-facing workflow is to check out the public tag. The full commit SHA remains the authoritative pin for reproducibility and review.",
        "Readers check out that exact commit. The project version identifies this source snapshot; the proposal does not assert that a matching release tag exists.")
    start = text.index("The package records author-confirmed local verification for the companion examples")
    end = text.index("\n\n", start)
    text = text[:start] + (
        "Verification for the migrated edition is tied to its exact book commit and the pinned framework source. The workflows build publication artifacts, compile the framework and companions with GCC and Clang, execute registered framework CTests and the external echo tests, and run selected book teaching and SSE/MiniGateway smoke checks. Run-specific outcomes belong in the accompanying verification report and workflow logs. Historical author-local confirmations are preserved with their original dates and source baseline; they are not silently transferred to the migrated sources. None of these checks is presented as independent adoption evidence or exhaustive deployment validation."
    ) + text[end:]
    text = text.replace("Package pins a public release tag and full commit SHA;", "Package pins a project version and full commit SHA;")
    text = text.replace("Verification includes author-confirmed local notes plus completed public CI workflows for package generation, companion-example compilation on GCC and Clang, and selected behavioral smoke tests.",
                        "Current evidence must identify the checked book commit, framework pin, compiler, and test scope; historical author-local confirmations remain separate.")
    changes[proposal] = text

    evidence = ROOT / "review/proposal/evidence-sheet.md"
    text = load(evidence).replace("public release tag `v1.0.2`", "project version `2.0.0`").replace(OLD_PIN, PIN)
    text = replace_once(text,
        "The first two documents record author-confirmed local verification against the public SNode.C source baseline. The CI smoke-test note records the completed public workflow checks for the selected runtime paths. These files are package evidence, not adoption evidence.",
        "The current notes define the migrated edition's verification scope and point to run-specific evidence. Earlier author-local confirmations are retained under `review/verification/history/` with their original baseline and dates. They are historical evidence, not new confirmations of changed source. None of these files is adoption evidence.")
    start = text.index("The public book repository contains completed GitHub Actions workflows")
    end = text.index("\n\n", start)
    text = text[:start] + (
        "The public book repository contains workflows for publication builds and companion verification. The publication workflow generates the proposal, sample-chapter, and full-book PDFs and the reviewer archive. The companion workflow reads the authoritative source pin, builds the framework with its CTest suite enabled, checks the installed external echo project, builds the book companions, and exercises selected teaching, SSE, and MiniGateway Extended behavior on GCC and Clang. Results must be attributed to the exact workflow run, not inferred from the presence of the workflow. A skipped test is not a passed behavioral check; a selected smoke test is not a complete protocol or deployment certification."
    ) + text[end:]
    changes[evidence] = text

    for path in (ROOT / "production/metadata").glob("*.yaml"):
        text = load(path)
        text = text.replace("Source,Sink,Logger,Config,", "Source,Sink,Logger,Level,Origin,Boundary,Identity,Scope,Settings,Message,QueueResult,ParserLimits,HttpServerPolicy,ConfigHttpParser,ConfigWebSocket,PeerCredentials,ShutdownContext,ShutdownReason,Config,")
        text = text.replace("{core,socket,stream,net,", "{snode,core,socket,stream,net,")
        changes[path] = text

    for path, text in changes.items():
        if "\b" in text:
            raise RuntimeError(f"Unexpected control character in {path}")
        path.write_text(text, encoding="utf-8")
    subprocess.run(["python3", "ci/check-source-alignment.py"], cwd=ROOT, check=True)
    subprocess.run(["bash", "ci/check-source-hygiene.sh"], cwd=ROOT, check=True)
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
    print("Completed remaining source alignment in", len(changes), "files")


if __name__ == "__main__":
    main()
