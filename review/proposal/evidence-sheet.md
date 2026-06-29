```{=latex}
\clearpage
```

# Evidence Sheet: SNode.C Book Proposal

## Purpose of this sheet

This sheet separates three kinds of evidence:

1. public evidence that can be checked from repositories or public documentation;
2. author-confirmed professional context;
3. adoption or market evidence that is not yet claimed.

It is deliberately conservative. The proposal should not invent users, downloads, commercial deployments, course adoptions, or independent validation that has not been documented.

## Public project evidence

### SNode.C repository

- Public repository: [SNodeC/snode.c](https://github.com/SNodeC/snode.c)
- Repository visibility: public
- Default branch: `master`
- Manuscript baseline: public release tag `v1.0.2`, commit `6e475262084ae2dab2daef8781ab9e4adb82d18e`
- The repository README describes SNode.C as a lightweight, highly extensible, event-driven, layer-based C++ framework for network applications.
- The README states that development began during the first Corona lockdown in Austria in summer semester 2020 as part of the course *Network and Distributed Systems* in the master's program *Interactive Media* at FH Upper Austria, Campus Hagenberg.
- The README names MQTTSuite as the SNode.C reference project.

### MQTTSuite repository

- Public repository: [SNodeC/mqttsuite](https://github.com/SNodeC/mqttsuite)
- Repository visibility: public
- Default branch: `master`
- The README describes MQTTSuite as a lightweight MQTT 3.1.1 integration system composed of focused applications.
- The listed application roles include MQTTBroker, MQTTIntegrator, MQTTBridge, MQTTCli, and MQTTStore.
- The README states that MQTTSuite is powered by SNode.C.

### Related public repositories

The SNodeC GitHub organization also contains related public repositories that support the ecosystem and book context, including:

- `SNodeC/SNode.C-Book`
- `SNodeC/MiniGateway`
- `SNodeC/IOTApplicationDesigner`
- `SNodeC/INJA-Templatebuilder`
- `SNodeC/CLI11`

These repositories demonstrate an ecosystem around the framework and book, but they should not be presented as external adoption evidence unless independent use is documented.

## Applied-system evidence

### MQTTSuite as reference ecosystem

MQTTSuite gives the book a concrete applied context beyond the framework itself. It shows SNode.C used for MQTT-facing applications, including broker, integration, bridge, CLI, and persistence roles. This supports the book's claim that SNode.C is not only a small teaching abstraction but also a basis for multi-application protocol systems.

### MiniGateway as guided capstone

The book package contains two MiniGateway source trees:

```text
companion/examples/MiniGateway
companion/examples/MiniGateway-Extended
```

They support Chapters 37 and 38 and demonstrate a small SNode.C application that combines HTTP status routes, SSE observation, MQTT publication, application-owned state, and an added Unix-domain input boundary in MiniGateway Extended.

MiniGateway is evidence of pedagogical completeness and architectural applicability inside the manuscript package. It is not presented as external market adoption.

### Companion examples

The package also contains companion source trees for selected protocol and persistence examples, including HTTP upgrade, SSE, WebSocket echo subprotocol examples, MQTT client role, and MariaDB. These examples support the reader promise and reduce the risk that the manuscript is only prose without buildable companion material.

## Teaching-context evidence

The SNode.C README publicly ties the framework's origin to a teaching context: the *Network and Distributed Systems* course in the master's program *Interactive Media* at FH Upper Austria, Campus Hagenberg.

This supports the book's educational positioning, but it should not be overstated as independent course adoption of the finished book unless such adoption is documented separately.

## Educational and interdisciplinary technical use cases

The manuscript explicitly supports educational and interdisciplinary technical use cases, including networked measurement, environmental monitoring, field sensing, lab instrumentation, gateway-style integration systems, and technical data-collection projects. These are presented as architectural use cases for readers who need to understand, build, teach, specify, adapt, or supervise such systems, not as claims of external adoption.

## Author-confirmed professional context

The following background items are author-confirmed and relevant to credibility, but should be treated as author-supplied CV context unless independent public sources are attached later:

- studies in theoretical physics in Graz;
- work at Ars Electronica Futurelab;
- four years as university assistant at Johannes Kepler University Linz in the Pervasive Computing group;
- work with ORF Kunstradio;
- participation around documenta X in Kassel;
- many projects connected to Ars Electronica Futurelab and media technology.

This background supports the author's technical and media-technology authority, but the proposal should distinguish it from repository-based evidence.

## Verification evidence inside the package

The package includes verification notes for the examples and MiniGateway source trees:

```text
review/verification/examples-aggregate-build-verification.md
review/verification/minigateway-step8-author-verification.md
source-baseline/book-source-baseline.md
source-baseline/book-source-baseline.env
```

These documents record author-confirmed local verification against the public SNode.C source baseline. They are useful package evidence, but they are not independent CI evidence.

## What is not yet claimed

The current proposal does not claim:

- commercial deployments;
- external customers;
- download statistics;
- package-manager install counts;
- GitHub stars/forks as market proof;
- third-party dependent projects;
- independent course adoption of the finished book;
- independent CI verification of all companion examples.

This restraint is intentional. Unsupported adoption claims would weaken the proposal.

## Evidence gaps to close for a stronger acquisition case

A broader professional-trade acquisition case would be stronger with:

- documented public release/download statistics;
- list of known users or organizations, if any can be named;
- dependent repositories or downstream projects;
- course-use statement or syllabus reference;
- independent reviewer quotes;
- CI badge or reproducible build workflow for companion examples;
- public package/deployment evidence for Linux or OpenWrt if available;
- a concise statement of why readers who do not yet use SNode.C should care.

## Current evidence verdict

The evidence currently supports a specialist, project-authoritative, course-friendly, or community technical-book case. It does not yet support an exaggerated mass-market claim. The proposal should therefore sell the book on depth, completeness, architecture, source alignment, examples, transparency, and the applied MQTTSuite ecosystem.
