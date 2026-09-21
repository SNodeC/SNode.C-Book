# Local PDF box-warning audit — 21 September 2026

The local clean build succeeded and regenerated `dist/pdf/snodec-book.pdf` from the current Markdown manuscript. The final PDF has **490 physical pages**, comprising 22 pages before Arabic page 1 and Arabic pages 1–468.

**The final book pass contains 25 box warnings at 23 rendered pages: 2 overfull horizontal boxes, 12 underfull horizontal boxes, 11 underfull vertical boxes, and no overfull vertical boxes.** All 18 figure PDFs and the two-page figure contact sheet were rebuilt and their 19 logs contain zero box warnings.

The two overfull lines are real margin intrusions. The underfull horizontal boxes are uneven word spacing. The vertical warnings arise from page filling around fixed-height material, particularly listings; a badness of 10000 does not by itself mean clipping or missing text. The affected pages were inspected as rendered images, not judged from warning counts alone.

The recommended remedies preserve every word and every code listing. This audit applied **no fixes to manuscript or production sources**. The delivered `dist` PDF is the ordinary rebuild with the warnings listed below. Separate disposable proofs tested proposed remedies; they did not replace that PDF.

## Build and counting method

```sh
cmake -S . -B build/pdf-box-audit-2026-09-21 -G Ninja
cmake --build build/pdf-box-audit-2026-09-21 --target pdf --clean-first --parallel 4
```

- Book revision: `fcbe51a`; working tree clean at build start.
- Toolchain: Pandoc 3.10.1, XeTeX 0.999998 / TeX Live 2026 (Debian), the configured pandoc-crossref and MakeIndex.
- The standard target generated LaTeX, ran XeLaTeX once, MakeIndex, then XeLaTeX twice. The final log has no unresolved-reference or rerun-required warning.
- The console contains **75 box-warning emissions**, because the same 25 warnings recur in each of the three book passes. There are no additional first-pass-only box warnings. Counting all passes as 75 separate defects would be wrong.
- Final book log: `review/pdf-box-audit-2026-09-21/snodec-book.log`. Complete build console: `build-console.txt`. Figure-log paths, hashes and zero-warning results: `figure-log-summary.json`.
- Every affected page was rendered at 110 dpi and visually inspected. This is a complete **box-warning** audit, not a visual inspection of all 490 pages or publication certification.
- Page references below are **printed Arabic page / physical PDF page**. Generated TeX locations refer to `build/pdf-box-audit-2026-09-21/snodec-book.tex`. The JSON inventory also retains the final log line and exact diagnostic.
- B02 is a notable mapping correction: TeX measures the callout before shipout 74, but the warning's text actually appears on printed page **75**. Rendered content, not merely the next page number in the log, determines the reported location.

## Overfull horizontal boxes — fix first

| ID | Page / PDF | Excess | Source and location | Proposed fix |
|---|---:|---:|---|---|
| B09 | 186 / 208 | 28.43593pt | [Ch. 17:579](/home/voc/projects/snodec/publications/book/manuscript/chapters/17-application-and-instance-configuration-in-detail.md:579) — 17.8, Progressive disclosure as a teaching tool | Permit a discretionary break after each slash in application/instance/section/option. |
| B15 | 367 / 389 | 7.64592pt | [Ch. 32:751](/home/voc/projects/snodec/publications/book/manuscript/chapters/32-cmake-components-and-linking-strategy.md:751) — 32.7, opening build-switch paragraph | Insert a paragraph break after the existing sentence ending “demonstration applications.” Start the next paragraph with SNODEC_BUILD_TESTS. |

B09 protrudes about **10.00 mm** into the right margin; B15 protrudes about **2.69 mm**. Both are clearly visible. The proposed fixes eliminated the respective warnings in paragraph proofs using the book's own preamble, font sizes and line measure.

## Underfull horizontal boxes — all 12

Badness is TeX's line-spacing diagnostic, not a measurement in points or a probability. B06–B08 are three different lines in one paragraph, not duplicate log emissions.

| ID | Page / PDF | Badness | Source and location | Proposed fix |
|---|---:|---:|---|---|
| B02 | 75 / 97 | 1215 | [Ch. 07:563](/home/voc/projects/snodec/publications/book/manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:563) — 7.11, What to remember, application-layer bullet | Use ragged-right text for the recap bullet/list within the existing remember-box style. Keep identifiers and all prose intact. |
| B04 | 120 / 142 | 1005 | [Ch. 12:158](/home/voc/projects/snodec/publications/book/manuscript/chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md:158) — 12.3, default/wildcard paragraph | Permit a discretionary break after the slash in default/wildcard. |
| B05 | 139 / 161 | 2875 | [Ch. 13:645](/home/voc/projects/snodec/publications/book/manuscript/chapters/13-writing-socketcontext-classes-well.md:645) — 13.12, What to remember, first bullet | Use ragged-right text for the recap bullet/list within the existing remember-box style. Keep identifiers and all prose intact. |
| B06 | 163 / 185 | 1960 | [Part V:5](/home/voc/projects/snodec/publications/book/manuscript/parts/part-05-configuration-and-operational-behavior.md:5) — Part V opening, line beginning Configuration is treated | Use ragged-right part-introduction setting with both existing insets retained; one shared correction resolves B06–B08. |
| B07 | 163 / 185 | 3907 | [Part V:5](/home/voc/projects/snodec/publications/book/manuscript/parts/part-05-configuration-and-operational-behavior.md:5) — Part V opening, line beginning application-side handles | Use ragged-right part-introduction setting with both existing insets retained; one shared correction resolves B06–B08. |
| B08 | 163 / 185 | 1142 | [Part V:5](/home/voc/projects/snodec/publications/book/manuscript/parts/part-05-configuration-and-operational-behavior.md:5) — Part V opening, line beginning generated command lines | Use ragged-right part-introduction setting with both existing insets retained; one shared correction resolves B06–B08. |
| B10 | 193 / 215 | 2884 | [Ch. 18:153](/home/voc/projects/snodec/publications/book/manuscript/chapters/18-logging-diagnostics-and-runtime-introspection.md:153) — 18.5, Connection and context scopes, opening paragraph | Insert a paragraph break after the existing sentence ending “by reference.” Leave both sentences intact. |
| B11 | 224 / 246 | 1406 | [Ch. 20:674](/home/voc/projects/snodec/publications/book/manuscript/chapters/20-timeouts-retries-and-failure-modes.md:674) — 20.13, opening boundary rule | Permit breaks after the slashes in retry/reconnect and connection/context. |
| B14 | 298 / 320 | 1237 | [Ch. 27:207](/home/voc/projects/snodec/publications/book/manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:207) — 27.7, MQTT integration-spine paragraph | Permit a break after the slash in publish/subscribe. |
| B19 | 389 / 411 | 1675 | [Ch. 34:137](/home/voc/projects/snodec/publications/book/manuscript/chapters/34-testing-debugging-and-benchmarking.md:137) — 34.4, Parser and formatter contracts | Insert a paragraph break after “HttpMessageParserTest checks message parsing.” Keep the preceding sentence with it and start the next paragraph with “Despite their RawWire names”. |
| B20 | 392 / 414 | 1888 | [Ch. 34:256](/home/voc/projects/snodec/publications/book/manuscript/chapters/34-testing-debugging-and-benchmarking.md:256) — 34.7, The external echo test layer | Insert a paragraph break after the first sentence, ending “installed SNode.C package.” Start the next paragraph with “It has its own CTest setup”. |
| B25 | 433 / 455 | 3919 | [Ch. 36:624](/home/voc/projects/snodec/publications/book/manuscript/chapters/36-extending-minigateway-with-a-new-network-role.md:624) — 36.11, What to remember, Unix-socket bullet | Use ragged-right text for the recap bullet/list within the existing remember-box style. Keep identifiers and all prose intact. |

The slash-break proposals retain justified body text and insert no printed hyphen. For example, the TeX presentation of B09 can allow breaks at these existing separators:

```tex
application/\allowbreak{}instance/\allowbreak{}section/\allowbreak{}option
```

Apply this to the identified ordinary-prose compounds, not indiscriminately to source listings, identifiers, commands or paths. The four paragraph-break proposals add only a blank line at an existing sentence boundary; no sentence is shortened or rewritten.

For B02/B05/B25, a coherent recap-list alignment policy belongs in the existing `snodecrememberbox` definition in `production/latex/snodec-callouts.tex`. The proof tested the affected bullets at their actual box/list width. Extending that policy to all recap boxes requires a complete rebuild and visual review of those boxes.

For B06–B08, adjust the existing part-introduction group in `production/metadata/metadata.yaml`. The tested setting preserves the current inset and adds stretch only on the right:

```tex
\leftskip=0.13\textwidth
\rightskip=0.13\textwidth plus 1fil
```

A bare `\raggedright` would reset the inset; do not use it there without restoring the intended geometry. The tested proof retained the 12-point italic text. Applying the shared part-opening policy requires inspecting all part pages afterward.

## Underfull vertical boxes — all 11

The common cause is the book class's equal-height page setting combined with fixed-height figures, tables and listings. My preferred production choice for this technical manuscript is **ragged-bottom main matter**: retain natural internal spacing and let unused depth remain at the foot. This is a real layout decision, not raising warning thresholds or hiding diagnostics.

A separate full-book proof changed only the generated copy to add `\raggedbottom`. It eliminated **all 11** underfull vertical boxes and retained **490 pages**. All 14 original horizontal warnings remained, demonstrating that the two classes of issue need separate treatment. The proof log is preserved as `vertical-proof.log`; the ordinary `dist` PDF was not replaced.

| ID | Page / PDF | Badness | Source and page contents | Page-specific assessment and proposed treatment |
|---|---:|---:|---|---|
| B01 | 5 / 27 | 2591 | [Ch. 01:115](/home/voc/projects/snodec/publications/book/manuscript/chapters/01-why-snodec-exists.md:115) — 1.6, Figure 1.1 and layer questions | Figure, fixed-height sketches, quote and callout leave insufficient stretch for equal-height page setting. The extra gaps between blocks are visible; nothing is clipped. Apply ragged-bottom setting; preserve the content. |
| B03 | 107 / 129 | 1484 | [Ch. 10:407](/home/voc/projects/snodec/publications/book/manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:407) — 10.6, IPv4/IPv6 comparison table and recap | The table and recap occupy most of the page; equal-height setting spreads gaps around the heading/table. All rows and bullets remain readable. Apply ragged-bottom setting; preserve the content. |
| B12 | 247 / 269 | 1496 | [Ch. 23:9](/home/voc/projects/snodec/publications/book/manuscript/chapters/23-server-sent-events-and-real-time-http.md:9) — 23.1, SSE chapter opening | A two-line chapter title, callout and two fixed-height sketches leave limited page flexibility; their surrounding gaps stretch. Apply ragged-bottom setting; preserve the content. |
| B13 | 251 / 273 | 10000 | [Ch. 23:173](/home/voc/projects/snodec/publications/book/manuscript/chapters/23-server-sent-events-and-real-time-http.md:173) — 23.6, complete SSE-Server main.cpp listing | A full page of a continuing listing has almost no stretchable material. Badness 10000 here is not evidence of lost code; the printed lines fit. Apply ragged-bottom setting; preserve the content. |
| B16 | 378 / 400 | 2393 | [Ch. 33:363](/home/voc/projects/snodec/publications/book/manuscript/chapters/33-deployment-on-linux-and-openwrt.md:363) — 33.4, Linux user-service rehearsal | Several listings and their explanations leave little flexible page material; spaces around the listings are stretched. Apply ragged-bottom setting; preserve the content. |
| B17 | 379 / 401 | 1097 | [Ch. 33:402](/home/voc/projects/snodec/publications/book/manuscript/chapters/33-deployment-on-linux-and-openwrt.md:402) — 33.5, Deployment-specific resources | Subheadings, lists and the short state-deployment sketch constrain page fill. The warning is mild and no content crosses a boundary. Apply ragged-bottom setting; preserve the content. |
| B18 | 388 / 410 | 10000 | [Ch. 34:95](/home/voc/projects/snodec/publications/book/manuscript/chapters/34-testing-debugging-and-benchmarking.md:95) — 34.3, test-layer table continuation and Figure 34.1 | The large top float, table continuation and two closing paragraphs cause visibly enlarged gaps. Separately, the figure interrupts the table between its unit and component rows. Apply ragged-bottom setting; preserve the content. |
| B21 | 405 / 427 | 1895 | [Ch. 35:226](/home/voc/projects/snodec/publications/book/manuscript/chapters/35-building-minigateway.md:226) — 35.5-35.6, CMakeLists.txt ending and Stage 2 opening | The fixed-height listing ends above a heading and two paragraphs; equal-height setting expands the available gaps. Apply ragged-bottom setting; preserve the content. |
| B22 | 413 / 435 | 10000 | [Ch. 35:703](/home/voc/projects/snodec/publications/book/manuscript/chapters/35-building-minigateway.md:703) — 35.10, MiniGatewayWeb.cpp listing ending | A listing-only page has insufficient stretch. Its content fits, with white space at the foot. Automatic wraps inside strings and types also merit a separate readability pass. Apply ragged-bottom setting; preserve the content. |
| B23 | 416 / 438 | 10000 | [Ch. 35:883](/home/voc/projects/snodec/publications/book/manuscript/chapters/35-building-minigateway.md:883) — 35.11, MiniGatewayMqtt.cpp listing continuation | The listing has essentially fixed line heights and cannot fill the remaining page depth through ordinary paragraph glue. Nothing is clipped. Apply ragged-bottom setting; preserve the content. |
| B24 | 430 / 452 | 10000 | [Ch. 36:378](/home/voc/projects/snodec/publications/book/manuscript/chapters/36-extending-minigateway-with-a-new-network-role.md:378) — 36.5, MeasurementUnixSocketContext.cpp continuation | Another continuing code page with fixed line heights. The extreme badness is about page fill, not horizontal overflow or missing source. Apply ragged-bottom setting; preserve the content. |

If equal bottom alignment is an essential design requirement, the alternative is individual page composition: adjust float placement or block spacing and, where necessary, move an intact block to a following page. That is more fragile under future manuscript edits. I would not reduce figure/code fonts or delete explanations simply to fill these pages. In particular, the code-only pages B13/B22/B23/B24 are already readable and should retain their source-aligned listings.

B18 also exposes a separate composition issue: Figure 34.1 floats above the continuation of a table whose first row is on page 387. Ragged-bottom setting removes the exaggerated gaps, but **does not reunite the table or fix that reading order**. In a later layout pass, prevent this figure from floating ahead of its declaration; a local trial of `latex-placement="bp"` instead of `"tbp"` would remove its top-of-page eligibility. Then review pages 387–389 together and, if needed, keep this short table together. This placement proposal has not been tested in the integrated book.

## What was tested, and what remains a proposal

1. **Original build:** complete clean figure and book generation, including index and final reference passes. All final-pass box warnings inventoried and all 23 actual warning pages inspected.
2. **Horizontal proofs:** the book's preamble and exact affected text were reused at native widths. Each baseline warning was reproduced. Discretionary slash breaks, the four specified paragraph breaks, ragged-right recap bullets, and the inset-preserving part-introduction setting removed all corresponding warnings in those isolated cases. The selected proof renderings were inspected. No word or code changes are needed.
3. **Vertical proof:** one full-book diagnostic pass with ragged-bottom setting, using copied auxiliary files, removed all 11 vertical warnings and still produced 490 pages. Representative figure/table and code pages were inspected. It was not a fresh publication/index-release build. The diagnostic applied ragged-bottom setting globally; it also changes index-column spacing. For implementation, scope the main-matter choice deliberately and restore the intended index setting. Raw text extraction retains identical non-whitespace text on every physical page; layout extraction differs in row interleaving on two index pages.
4. **Not done:** no combined, source-level implementation of all remedies and no integrated proof after combining them. Horizontal reflow and shared style changes can shift page breaks, index references or floats. Therefore the current finding is “each proposed remedy has diagnostic support,” not “a final warning-free book has been produced.”
5. **Scope:** no manuscript wording, complete listing, companion implementation, framework source, or production configuration was edited. The current framework was not rebuilt or revalidated during this typography audit. OpenWrt and publication completion remain deferred; broader runtime validation remains omitted as agreed.

The paragraph-probe sources, logs and structured results are retained in this review directory. They also record unsuccessful experiments: adjusting `\looseness`, reducing hyphen penalties, or substituting individual words did not reliably cure the problem. Those failed alternatives are not recommended.

## Other observations outside the box counts

These do not change the 25-warning total, but should be considered before publication:

- The final log reports that the requested bold Latin Modern Mono shape is unavailable and substitutes its regular shape. Explicitly map a suitable installed bold mono face or choose a complete matching family before final production; that font decision will require a fresh box audit because it changes metrics. This audit did not change fonts.
- `tocloft` reports that `\@starttoc` was already redefined. Resolve ownership/load-order compatibility for the contents setup and review the contents pages; do not hide the warning. The precise compatibility patch remains to be investigated.
- Pandoc's generated `\captionsetup[table]` is unused in this book build. This is configuration noise rather than visible overflow; remove or condition that setup at the template level if pursuing a fully clean production log.
- The affected page 193 also has a period stranded after the inline `System` identifier, and several long listings wrap inside strings or types. These are examples of visible typography issues that can escape box diagnostics. They merit a separate inline-code and listing-wrap review while preserving exact code contents.

## Recommended implementation order

1. Allow slash breaks in the four identified prose paragraphs and add the four paragraph breaks. Preserve all words and source-listing markers.
2. Apply a consistent recap-list alignment policy and inset-preserving part-introduction alignment in the existing production definitions.
3. Adopt ragged-bottom main matter, if this page-design choice is accepted. Address Figure 34.1's table interruption as an additional local composition correction.
4. Run the complete ordinary build again, including MakeIndex and all final passes. Re-inventory every box warning and recheck affected/shifted pages, contents, index and all part openings. Do not assume isolated proof success guarantees the combined result.

No implementation or publication closure is claimed by this report.
