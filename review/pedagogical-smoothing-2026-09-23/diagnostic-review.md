# P7 diagnostic review

All 33 before/after records, identifier spellings, first-400-word identifiers, abstract-noun passages, context terms, fenced-token changes and three tail blocks are in smoothing-diagnostics.json. Before is c7b76c1; the two splits use the approved headings, so their original apparatus stays in the corresponding original half. Counts are diagnostics, not asserted quality targets.

The identifier proxy counts unique monospace C++-like spellings per 1,000 prose tokens. It does not infer whether a reader has previously encountered an API. First-400 counts and exact spellings expose that limitation. Raw cluster detection retains tables, index entries and captions so no hit is silently discarded.

| Unit | Identifier density before → after | Clusters before → after | Review of the change |
|---|---|---|---|
| 1 | 5.52 → 3.94 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 2 | 4.91 → 4.55 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 3 | 12.22 → 12.08 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 4 | 8.36 → 6.54 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 5 | 9.49 → 6.51 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 6 | 21.42 → 17.25 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 7 | 7.14 → 7.08 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 8 | 15.5 → 14.22 | 1 → 1 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 9 | 10.48 → 10.47 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 10 | 13.08 → 13.08 | 0 → 0 | Small normalization/denominator movement; reference mechanism and actors preserved. |
| 11 | 4.39 → 4.41 | 1 → 0 | Small normalization/denominator movement; reference mechanism and actors preserved. |
| 12 | 7.75 → 7.67 | 1 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 13 | 8.06 → 7.38 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 14 | 19.73 → 21.11 | 1 → 1 | Shorter repetitive prose raises the ratio around an unchanged explicit logging reference table; the constructed logger is shown first. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 15 | 9.83 → 9.19 | 1 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 16 | 5.36 → 5.74 | 0 → 0 | The required setter/CLI example names its public APIs; compilation and source declarations are recorded in P4-P5-api-review.md. |
| 17 | 11.15 → 11.12 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 18 | 26.2 → 32.11 | 0 → 0 | The requested complete dispatch and request trace name middleware APIs; the concrete request precedes the consolidated inventory. |
| 19 | 9.63 → 9.5 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 20 | 6.29 → 6.29 | 0 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 21 | 18.28 → 11.32 | 1 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 22 | 10.85 → 8.83 | 4 → 3 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 23 | 0.0 → 0.0 | 12 → 13 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: the diagram names devices, local services and the gateway; configuration names MQTT/HTTP instances; retry contrasts an MQTT integration client with local administration. Table/index hits are inventories, not sentences. The added HTTP/MQTT decision supplies the concrete adapter consequence. |
| 24 | 5.61 → 5.56 | 2 → 2 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 25 | 13.64 → 10.73 | 1 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 26 | 4.87 → 4.53 | 10 → 8 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: the application process, named admin/ingest roles, SSE route and MQTTBroker/Integrator/Bridge give the actors. The consumer/security checklist is an explicit design checklist. |
| 27 | 14.95 → 14.01 | 3 → 0 | Concrete examples supply the extra prose; density is stable or lower. |
| 28 | 6.1 → 6.12 | 1 → 1 | Small normalization/denominator movement; reference mechanism and actors preserved. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 29 | 9.35 → 8.88 | 2 → 2 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 30 | 10.89 → 7.3 | 2 → 2 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: SocketStateReporter is the concrete diagnostic owner; other hits are index entries. |
| 31 | 4.12 → 4.72 | 2 → 2 | The three requested source excerpts have surrounding explanation; removal of the long listing changes the prose denominator. Cluster passages were read in context: hits are explicit reference tables, captions or named API responsibilities, with prose context supplying the concrete objects. |
| 32 | 2.63 → 1.44 | 5 → 5 | Concrete examples supply the extra prose; density is stable or lower. Cluster passages were read in context: tables enumerate concrete input paths and model ownership; the concluding sentence names Unix, web and MQTT actors. |
| A | 10.69 → 11.28 | 2 → 2 | Relocated descriptor source reading introduces the relevant public/internal names in the optional appendix. Cluster passages were read in context: the extension input and configuration option are the subjects; the latter intentionally classifies configuration responsibilities. |

The three tail blocks were compared with the seam pass; Build-note chapters close in the required order. No diagnostic threshold was used to delete code or inflate prose. No material identifier increase is left without the pedagogical reasons above.
