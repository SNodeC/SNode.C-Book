Follow-up 12: final polish. Close the open review items, then stop for the author's reading.

Store this message verbatim as
review/pedagogical-smoothing-2026-09-23/FOLLOWUP-12.md. It is an author
instruction. PROMPT.md, FOLLOWUP-01 and FOLLOWUP-11 remain the governing scope;
this follow-up adds only the items below. Record it in the work plan.

0. Starting point and rules
- Work on branch book/pedagogical-smoothing-2026-09-23 from tip 9b82ea4.
- The framework freeze is unchanged at 07ca9a29. Compare it with
  framework-freeze-R2.json at the start and at the end. Any change stops the run.
- The scope is exactly items P1–P9 below. Make no other manuscript changes, no
  companion changes and no structure changes.
- Refine, don't replace (PROMPT.md §1). Keep technical claims. Verify every
  changed technical statement against the frozen source and give header:line in
  the report.
- Budget:
  - The total stays at or below 115,000 tokens (hard limit); aim for 112,500 or
    less.
  - The per-chapter caps in smoothing-structure.json apply. A cap may be
    exceeded by at most 5%, with a waiver entry (PROMPT.md §4).
  - No chapter may drop below its floor.
- Make one commit per item, in the order below, then one evidence commit.

1. Items

P1. The old sense of "role" (register rows 1 and 16; dimensions L, C)
The glossary defines role as a design responsibility in a system. Replace every
remaining use in the older sense (a server or client side, a public type or
header, an instance, a status level) with the canonical term. Known occurrences,
with line numbers at 9b82ea4:
- ch05:35, 51, 62, 161, 209: "selects a role", "public role", "the role is a
  server", "role headers", "public role header"
- ch07:385 and ch12:194: "public role headers"
- ch17:29: the "context role" table row
- ch27:135: "source-facing public roles"
- ch08:345: "role-level status"
- ch26:249: "protocol role (MQTT or HTTP)"
- ch01:68, ch13:6, ch13:15: "communication roles". Keep these only where the
  sentence means a system-design role; otherwise rephrase.
Then grep the whole manuscript for "role" and review every hit in context.
Allowed uses are system-design roles: web role, MQTT uplink role, broker, bridge
and store roles, the MiniGateway roles, and "network role" in the Ch31 title.
List each kept use with a one-line justification in terminology-allowlist.md.

P2. Ch8 responsibility table (row 16; C)
The table at ch08:335 re-tabulates the taxonomy that Ch4 already tabulates.
Reduce it to the concerns Ch8 adds (retry and reconnect policy; local, bind and
remote endpoint views; status and callback layers), or turn it into prose. For
the rest, point to Ch4's figure and terminology box.

P3. Ch2 shortest path (row 5; G, S)
Replace the prose inside the "Shortest path to Chapter 3" box (ch02:18) with a
numbered list of the actual commands, one step per item:
  1. obtain the book package and the pinned framework commit;
  2. configure an out-of-tree build;
  3. build;
  4. install into one prefix;
  5. verify the installed package;
  6. build the external EchoPair;
  7. continue to Chapter 3.
Use exactly the commands and variable names the chapter uses later, so the two
never diverge. Keep one sentence after the list: resolve a failing step before
moving to the next.

P4. Ch13 running value (row 10; G, T)
The running value is echoserver's local port: 8080 as the default, 18091 from
the file, 18092 from the command line. It must reappear in every section after
"Configuration principles", including:
- "Section configuration: scoped responsibilities",
- "Persistent and nonpersistent values",
- "Designing configuration for real applications".
In each section, first show what the section's concept means for that one value,
then generalize. Add no other configuration examples.

P5. Ch21 MQTT fundamentals and diagram (row 8; D)
- In the first section, add a sequence diagram of the conversation the text
  traces: subscriber, broker and publisher, with CONNECT, CONNACK, SUBSCRIBE,
  SUBACK, PUBLISH, and the broker's PUBLISH to the subscriber. Use a TikZ figure
  in the existing figure pipeline if the figure build passes; otherwise use a
  `text` fenced diagram.
- Before the class tables, explain each of these briefly and precisely:
  - topic names versus topic filters, and the + and # wildcards;
  - QoS 0, 1 and 2, and what each acknowledgement covers;
  - retained messages;
  - keep-alive, with PINGREQ and PINGRESP;
  - clean versus persistent sessions.
- Identify the MQTT version the frozen source implements, and verify each
  statement against it (give file:line in the report). Do not describe features
  the implementation lacks; where it differs from the specification, say so.

P6. Ch18 remaining tables (row 7; T)
Move the type, lifecycle and method tables and lists into the existing "Routing
API reference" box. At most one table may stay outside the box: the comparison
between the HTTP layer and the Express-like layer.

P7. Ch23 worked case and abstraction (rows 19 and 29; X, T, L)
- Replace the worked case "Worked change: separate the device input from its
  observers" with a different multi-protocol decision. Sequence ownership is
  already taught in Ch1, Ch4, Ch30 and Ch32. Suggested: where to place the broker,
  and which QoS or acknowledgement a device path with intermittent connectivity
  needs. Keep the same shape: requirement, options, decision, consequence, test.
- In Ch23 and Ch26, rewrite every sentence that stacks three or more of these
  nouns so that it names a concrete actor (device, broker, gateway process, HTTP
  handler, database, operator): boundary, role, surface, policy, carrier, owner,
  ownership, observation, responsibility, contract.

P8. Verification register (row 32; X, L)
Count constructions with this case-insensitive regex:
  \b(does|do|did|can|cannot|could|will|would) ?(not|n't)? (by itself |alone |merely |yet )?(prove|establish|demonstrate|show)s?\b|\b(is|are) not (proof|evidence)\b|\bcannot (prove|establish|demonstrate)\b
The book-wide count rose from 46 at c7b76c1 to 61. Bring it back to at most 46
by removing redundant occurrences in text added since c7b76c1. Keep a
qualification only where it prevents a likely misreading. Where possible, state
the positive fact instead.

P9. Publisher proposal (outside the eight dimensions)
In review/proposal/book-proposal-package.md:
- Revision plan (line 114): describe the completed pedagogical revision in
  publisher language, as what changed for the reader:
  - a gentler opening;
  - two new chapters created by splitting;
  - protocol and build chapters that start from an example;
  - an expanded synthesis.
  No internal phase or gate names.
- Length row (line 118): remove the internal targets. State only the current
  extent and the author's ceiling of at most 115,000 words.
- Section density (line 119) and every other figure: take the values from
  ci/manuscript-metrics.py after this polish, and the page count from the
  rebuilt PDF.
- Grep review/proposal/ for other stale figures (tokens, pages, headings,
  chapter numbers) and for internal terms: "wish", "floor", "gate", "FOLLOWUP",
  "P0a", "P−1", \bP[0-7]\b, "107,338", "112,338".

2. Checks
Add review/pedagogical-smoothing-2026-09-23/check-polish.py, asserting:
1. None of these phrases remains outside terminology-allowlist.md: "public
   role", "role header", "role file", "the role is a", "selects a role",
   "role-level", "context role", "protocol role", "server role", "client role",
   "communication role".
2. Outside Ch4, no table names five or more of: handle, instance, flow,
   connection, context, factory.
3. Ch2's shortest-path box contains a numbered list of at least 6 items, and
   each item contains a command.
4. Every level-3 section of Ch13 after the first mentions "echoserver" together
   with one of: 8080, 18091, 18092, local.port.
5. Ch21's first section contains the sequence diagram before the first class
   table. The chapter explains topic filters, the + and # wildcards, QoS 0, 1
   and 2, retained messages, keep-alive and session persistence.
6. Ch18 has at most one table outside the "Routing API reference" box.
7. Ch23's worked-case section does not contain "sequence number",
   "sequence owner" or "sequence authority". Ch23 and Ch26 contain no sentence
   with three or more of P7's nouns, except allowlisted ones.
8. The book-wide count of P8's regex is at most 46.
9. The proposal contains none of P9's internal terms, and its figures match the
   metrics and the PDF.

Then run:
- check-smoothing.py
- ci/manuscript-metrics.py
- ci/check-chapter-references.py
- ci/check-source-alignment.py --framework <frozen tree>
- ci/check-source-hygiene.sh
- ci/build-book-package.sh (for the PDF)
Labs are not required, because no companion file changes. If one does change,
run all labs.

3. Report
Write POLISH-REPORT.md, containing:
- The status matrix: all 32 register rows × 8 dimensions, with ● met, ◐ partly
  met, ○ open. Give file:line evidence for every cell that moved from ◐ or ○.
- Tokens before and after, in total and for each chapter touched, against
  112,338 and 115,000.
- The PDF page count and path.
- The check results, the framework-freeze comparison, and the commit SHA for
  each item.
Do not mark a cell ● without evidence. If an item cannot be completed within
this scope, leave it at ◐ and explain why.

4. Operational
Push the work branch when done. Do not merge. Final message, short:
- commit SHAs for P1–P9;
- check results;
- tokens and page count;
- the matrix totals per dimension;
- any cell that is not ●, and why;
- the PDF path.