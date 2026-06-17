# Repetition / Shrink Pass 2 Report
This pass continues the repetition/shrink work after Pass 1. It was applied part-by-part across the manuscript rather than by global deletion of technical material.
## Scope
- Broader than Pass 1: all chapters were checked, with changes in most chapters.
- Priority remained repeated explanatory prose, oversized `What to remember` sections, and repetitive chapter-closing transitions.
- No source-code features, book-file order, examples, metadata, or part/chapter structure were changed.
## Result
- Chapter prose word count after Pass 1: 106,839
- Chapter prose word count after Pass 2: 103,104
- Delta: -3,735 words (-3.50%)

Combined with Pass 1, the book has now received a meaningful editorial compression while preserving the architecture-first teaching style.
## Main edit types
- Shortened repeated transition prose such as repeated chapter self-reference and rhetorical restatement.
- Compressed long `What to remember` lists so summaries remain useful but less repetitive.
- Shortened repeated `Closing perspective` sections where they restated the chapter too fully.
- Preserved core terminology such as instance, application-side handle, connection, context, factory, lower communication family, role, and boundary.
- Preserved code blocks and command examples.
## Changed chapters

| File | Before | After | Delta | Change |
|---|---:|---:|---:|---:|
| `chapters/01-why-snodec-exists.md` | 2,556 | 2,399 | -157 | -6.14% |
| `chapters/02-preparing-your-environment.md` | 2,103 | 2,032 | -71 | -3.38% |
| `chapters/03-your-first-working-program-the-echo-pair.md` | 2,007 | 1,936 | -71 | -3.54% |
| `chapters/04-reading-the-codebase-with-confidence.md` | 2,667 | 2,661 | -6 | -0.22% |
| `chapters/05-the-mental-model-of-snodec.md` | 3,274 | 3,132 | -142 | -4.34% |
| `chapters/06-core-runtime-and-event-processing.md` | 4,254 | 4,063 | -191 | -4.49% |
| `chapters/07-layers-in-practice-network-transport-connection-application.md` | 3,360 | 3,233 | -127 | -3.78% |
| `chapters/08-socket-addresses-and-address-semantics.md` | 2,355 | 2,293 | -62 | -2.63% |
| `chapters/09-servers-clients-and-connections.md` | 4,070 | 3,976 | -94 | -2.31% |
| `chapters/10-ipv4-and-ipv6-as-the-primary-teaching-path.md` | 2,693 | 2,631 | -62 | -2.30% |
| `chapters/11-unix-domain-sockets.md` | 2,510 | 2,484 | -26 | -1.04% |
| `chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md` | 2,037 | 1,979 | -58 | -2.85% |
| `chapters/13-writing-socketcontext-classes-well.md` | 3,140 | 3,020 | -120 | -3.82% |
| `chapters/14-writing-socketcontextfactory-classes-well.md` | 3,341 | 3,222 | -119 | -3.56% |
| `chapters/15-building-the-same-protocol-over-different-lower-layers.md` | 2,877 | 2,795 | -82 | -2.85% |
| `chapters/16-configuration-philosophy-in-snodec.md` | 2,921 | 2,839 | -82 | -2.81% |
| `chapters/17-application-and-instance-configuration-in-detail.md` | 3,550 | 3,426 | -124 | -3.49% |
| `chapters/18-logging-diagnostics-and-runtime-introspection.md` | 3,493 | 3,329 | -164 | -4.70% |
| `chapters/19-tls-across-the-framework.md` | 2,776 | 2,673 | -103 | -3.71% |
| `chapters/20-timeouts-retries-and-failure-modes.md` | 2,999 | 2,896 | -103 | -3.43% |
| `chapters/21-the-http-layer.md` | 2,270 | 2,229 | -41 | -1.81% |
| `chapters/22-the-express-like-framework.md` | 2,364 | 2,295 | -69 | -2.92% |
| `chapters/23-server-sent-events-and-real-time-http.md` | 2,438 | 2,377 | -61 | -2.50% |
| `chapters/24-websocket-and-protocol-upgrade.md` | 2,537 | 2,458 | -79 | -3.11% |
| `chapters/25-mqtt-support-in-snodec.md` | 2,427 | 2,314 | -113 | -4.66% |
| `chapters/26-mqtt-over-websocket.md` | 2,002 | 1,887 | -115 | -5.74% |
| `chapters/27-designing-iot-systems-with-multiple-protocols.md` | 2,722 | 2,632 | -90 | -3.31% |
| `chapters/28-database-support-and-application-state.md` | 2,849 | 2,733 | -116 | -4.07% |
| `chapters/29-learning-from-the-applications-in-src-apps.md` | 3,074 | 3,007 | -67 | -2.18% |
| `chapters/30-from-applications-to-systems.md` | 2,132 | 2,053 | -79 | -3.71% |
| `chapters/31-mqttsuite-as-a-reference-ecosystem.md` | 2,182 | 2,100 | -82 | -3.76% |
| `chapters/32-cmake-components-and-linking-strategy.md` | 3,784 | 3,617 | -167 | -4.41% |
| `chapters/33-deployment-on-linux-and-openwrt.md` | 3,290 | 3,181 | -109 | -3.31% |
| `chapters/34-testing-debugging-and-benchmarking.md` | 4,965 | 4,732 | -233 | -4.69% |
| `chapters/35-architectural-judgment-choosing-the-right-layer-and-boundary.md` | 2,706 | 2,541 | -165 | -6.10% |
| `chapters/36-extending-the-framework-safely.md` | 1,816 | 1,747 | -69 | -3.80% |
| `chapters/37-building-minigateway.md` | 1,562 | 1,503 | -59 | -3.78% |
| `chapters/38-extending-testing-and-deploying-minigateway.md` | 1,499 | 1,443 | -56 | -3.74% |
| `chapters/epilogue.md` | 1,237 | 1,236 | -1 | -0.08% |

## Sanity checks
- Balanced fenced code blocks: yes
- `book-files.txt` and `book-files-existing-only.txt` were not changed.
- Example source trees were not changed.
