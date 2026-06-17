# Repetition / shrink pass report

Scope: targeted part-by-part reduction of repeated explanatory prose, with priority on middle and late design/system chapters. Core terminology was preserved; local repetition and redundant restatement were reduced.

## Modified files

| File | Words before | Words after | Delta | Change |
|---|---:|---:|---:|---:|
| `chapters/16-configuration-philosophy-in-snodec.md` | 3387 | 3382 | -5 | -0.15% |
| `chapters/20-timeouts-retries-and-failure-modes.md` | 3832 | 3826 | -6 | -0.16% |
| `chapters/25-mqtt-support-in-snodec.md` | 2972 | 2967 | -5 | -0.17% |
| `chapters/26-mqtt-over-websocket.md` | 2698 | 2693 | -5 | -0.19% |
| `chapters/27-designing-iot-systems-with-multiple-protocols.md` | 3821 | 3393 | -428 | -11.20% |
| `chapters/28-database-support-and-application-state.md` | 3678 | 3663 | -15 | -0.41% |
| `chapters/29-learning-from-the-applications-in-src-apps.md` | 4166 | 4156 | -10 | -0.24% |
| `chapters/30-from-applications-to-systems.md` | 3071 | 2725 | -346 | -11.27% |
| `chapters/31-mqttsuite-as-a-reference-ecosystem.md` | 3303 | 2870 | -433 | -13.11% |
| `chapters/34-testing-debugging-and-benchmarking.md` | 6449 | 5743 | -706 | -10.95% |
| `chapters/35-architectural-judgment-choosing-the-right-layer-and-boundary.md` | 3507 | 3083 | -424 | -12.09% |
| `chapters/36-extending-the-framework-safely.md` | 3125 | 2739 | -386 | -12.35% |
| `chapters/38-extending-testing-and-deploying-minigateway.md` | 3223 | 3163 | -60 | -1.86% |

Changed chapter total: 47232 -> 44403 words (-2829 words, -5.99%).

The highest-priority dense chapters were reduced as follows:

- Chapter 27: -11.20%
- Chapter 30: -11.27%
- Chapter 31: -13.11%
- Chapter 34: -10.95%
- Chapter 35: -12.09%
- Chapter 36: -12.35%

## What was changed

- Removed repeated “boundary/role/meaning” restatements where the same point was made twice in adjacent paragraphs.
- Shortened repeated framing phrases such as “not merely”, “the important point”, and repeated chapter-purpose statements.
- Preserved the established SNode.C vocabulary and did not turn the pass into a global search/replace.
- Kept MiniGateway source listings and chapter structure intact; Chapter 38 prose was lightly tightened only where it repeated the base/extension idea.
- Corrected one existing duplicated fenced-code marker in Chapter 31 around the named instance list.

## Sanity checks

- All modified files have balanced triple-backtick fences.
- `book-files.txt` and part/chapter ordering were not changed in this pass.
- No source-code features or examples were added.
