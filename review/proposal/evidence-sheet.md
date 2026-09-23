```{=latex}
\clearpage
```

# Evidence sheet

Checked **23 September 2026 (Europe/Vienna)**. This sheet separates public corroboration, author-supplied facts, and observations of the supplied book package. None establishes a sales forecast or institutional endorsement.

## Public corroboration

- **Current appointment.** The [Interactive Media faculty page](https://fh-ooe.at/en/degree-programs/interactive-media-master/team) lists Volker Christian as a professor of multimedia programming at FH Upper Austria's School of Informatics, Communications and Media in Hagenberg. The author supplies his teaching in the Media Technology and Design and Interactive Media programmes; preferred printed title and department wording remain to be confirmed.
- **Earlier relevant practice.** The [2001 Futurelab biographies](https://webarchive.ars.electronica.art/en/archives/festival_archive/festival_catalogs/festival_artikel.asp%3FiProjectID=12338.html) corroborate theoretical-physics study at Graz, the 1997–1999 assistantship, and a Futurelab deputy role beginning in 1999. The [1999 TeleZone catalogue](https://webarchive.ars.electronica.art/en/archives/festival_archive/festival_catalogs/festival_artikel.asp%3FiProjectID=8362.html) credits Christian among the programmers. These sources support selected facts, not the full chronology or all projects in his career.
- **Repositories.** Direct GitHub REST API collection on 23 September 2026, 00:58–00:59 Europe/Vienna (22 September, 22:58–22:59 UTC) returned **6,318 / 1,156** reachable `master` commits, **11 / 2** stars, **27 / 6** forks, and **0 / 2** watching subscribers for [SNode.C](https://github.com/SNodeC/snode.c) / [MQTTSuite](https://github.com/SNodeC/mqttsuite), respectively. Their oldest returned commits have no parents and dates 13 April 2020 / 25 September 2022. The release endpoints list **3 / 2** published releases; the proposal links their release histories.
- **Counting limits.** Commit pagination used a captured branch head for each repository. Contributor and release endpoints were fully paginated. Contributors returned **4 User + 1 Bot accounts / 3 User accounts**, excluding anonymous identities by default. Account counts are not independently verified human counts. GitHub interest figures do not measure deployments, readers, downloads, or purchasers.

## Author-supplied evidence and its limits

The teaching portfolio establishes responsibility for the book's prerequisite chain: programming and algorithms, applied C++, POSIX I/O and sockets, distributed systems, and sensor-based IoT. Electronics and signal-processing teaching connect the software path to physical measurements. This supports the author's ability to explain intermediate steps; no enrolment total or course adoption of the book is claimed.

The author reports continuous maintenance of SNode.C since its creation in April 2020, its origin in live online teaching during the first COVID lockdown, later MQTT/MQTTSuite development, and student projects over several cohorts. The collected root-commit date corroborates the start of the repository history; it does not independently verify each teaching event. The author also states that the framework and book examples are written by hand, with limited AI assistance since mid-2025.

The reported Hartbeespoort Dam application connects water-quality sensors and GPS through ESP32 devices, LoRaWAN/The Things Network, MQTTSuite/MQTTStore, and a WebSocket/WSS dashboard. This is an author-reported research application beyond his own projects. Permission to identify the research institution and collaborator, and independently checkable operational evidence, remain outstanding; no ecological effectiveness claim is made.

## Evidence in the supplied book package

- **Manuscript:** 32 numbered chapters in 11 Parts, Appendix A, closing essay and reference material; **110,177 whitespace tokens**, of which 102,339 are prose and 7,838 occur in fences; **326 pages in the rebuilt reading PDF; publisher pagination pending**.
- **Teaching apparatus:** 99 objectives and 165 mapped exercises across 32 chapters and Appendix A. Each has two review questions, two labs and one design problem, public solutions, and a recap of at most five bullets. All 11 Parts have runnable checkpoints; the epilogue is a closing essay.
- **Samples:** Chapters **1, 3, 19, 30 and 32**, using the same teaching pattern. The smoothing pass adds explanations and worked traces where each sample needs them. The sample guide identifies the skill and observable outcome each demonstrates.
- **Build/run evidence:** the companion examples and lab dependencies compiled, including the standalone Asio comparison, and **66/66 local lab cases passed on 23 September 2026 against public 07ca9a29**. The fresh framework build passed 185/185 tests, and all teaching, behavior and lifetime smoke suites passed. The manuscript, proposal and sample PDFs build; complete printed listings match their companion sources.
- **Observation limits:** local tests include broker delivery and database persistence across a client restart. They do not certify Bluetooth hardware, OpenWrt deployment, the author's field application, or a new hosted build. Public lab instructions state dependencies, expected outcomes, and the scope of each observation.
- Manuscript baseline: project version `2.0.0`, public commit `07ca9a29`, with contents recorded by the edition manifest; no patch required

## Items still required from the author

- **[AUTHOR TO SUPPLY]** Preferred printed title and department wording; exact Graz institute name and Futurelab/JKU appointment dates if a fuller biography is needed.
- **[AUTHOR TO SUPPLY]** Dated public talks, workshops, articles or posts, and supervised SNode.C theses; permission to cite the summer-2026 lecture deck publicly.
- **[AUTHOR TO SUPPLY]** Permission to name the research institution and collaborator, with checkable application evidence; student-project counts and years, approximate annual student numbers, and confirmation of the founding semester.
- **[AUTHOR TO SUPPLY]** Any independent readership evidence or reviewer quotations cleared for use.
- **[AUTHOR TO SUPPLY]** Weeks to final manuscript after acceptance and hours per week available for revision.

The available evidence supports assessment of the teaching method, technical content, author expertise, and inspectable examples. The unresolved items limit the market case and prevent a delivery commitment.
