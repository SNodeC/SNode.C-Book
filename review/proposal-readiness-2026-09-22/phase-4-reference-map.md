# Phase 4 reference migration register

Status: awaiting author approval. This register is a normative appendix to RESTRUCTURE-PLAN.md; it records current locations, not edits.

Chapter references include singular/plural forms, multiline lists, ranges, uppercase running heads, and literals inside printed listings. Chapter 4 moves mainly to Appendix A; its introductory teaching remains in new Chapter 4. Foundation ranges exclude the optional appendix. References between merged chapters become section references. Full source context is in phase-4-reference-inventory.json.

| ID | Current source:line | Current reference | Intended destination | Required treatment |
| --- | --- | --- | --- | --- |
| R001 | `README.md:40` | Chapters 35 and 36 | Chapter 28, Chapter 29 | renumber to listed destinations; retain target meaning |
| R002 | `README.md:60` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R003 | `README.md:60` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R004 | `README.md:66` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R005 | `README.md:66` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R006 | `STRUCTURE.md:134` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R007 | `STRUCTURE.md:134` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R008 | `STRUCTURE.md:167` | Chapter 1 | Chapter 1 | retain number; recheck semantic target |
| R009 | `STRUCTURE.md:167` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R010 | `STRUCTURE.md:167` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R011 | `STRUCTURE.md:167` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R012 | `STRUCTURE.md:167` | Chapter 37 | Chapter 30 | renumber to listed destinations; retain target meaning |
| R013 | `STRUCTURE.md:172` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R014 | `STRUCTURE.md:172` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R015 | `STRUCTURE.md:176` | Chapters 3 and 18 | Chapter 3, Chapter 13 | renumber to listed destinations; retain target meaning |
| R016 | `ci/check-source-hygiene.sh:63` | Chapter 10 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R017 | `ci/manuscript-metrics.py:19` | Chapter 29 | policy guard retained | preserve this legacy forbidden-phrase guard; it is policy, not a reader cross-reference |
| R018 | `ci/run-teaching-smoke-tests.py:2` | Chapter 3 and 18 | Chapter 3, Chapter 13 | renumber to listed destinations; retain target meaning |
| R019 | `ci/run-teaching-smoke-tests.py:83` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R020 | `ci/run-teaching-smoke-tests.py:110` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R021 | `ci/run-teaching-smoke-tests.py:131` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R022 | `companion/examples/Comparison-AsioEcho/README.md:3` | Chapter 1 | Chapter 1 | retain number; recheck semantic target |
| R023 | `companion/examples/Comparison-AsioEcho/README.md:21` | Chapter 1 | Chapter 1 | retain number; recheck semantic target |
| R024 | `companion/examples/EchoPair/README.md:3` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R025 | `companion/examples/HttpUpgrade-Client/README.md:3` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R026 | `companion/examples/HttpUpgrade-Server/README.md:3` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R027 | `companion/examples/LineProtocol-Client/README.md:4` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R028 | `companion/examples/LineProtocol-Server/README.md:4` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R029 | `companion/examples/MQTT-ClientRole/README.md:3` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R030 | `companion/examples/MariaDB-Minimal/README.md:3` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R031 | `companion/examples/MiniGateway-Extended/README.md:3` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R032 | `companion/examples/MiniGateway-Extended/README.md:27` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R033 | `companion/examples/MiniGateway/README.md:3` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R034 | `companion/examples/MiniGateway/README.md:30` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R035 | `companion/examples/README.md:10` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R036 | `companion/examples/README.md:11` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R037 | `companion/examples/README.md:60` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R038 | `companion/examples/README.md:78` | Chapters 35 and 36 | Chapter 28, Chapter 29 | renumber to listed destinations; retain target meaning |
| R039 | `companion/examples/SSE-EventSource-Client/README.md:3` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R040 | `companion/examples/SSE-Server/README.md:3` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R041 | `companion/examples/SemanticLogging/README.md:3` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R042 | `companion/examples/WebSocket-Echo-ClientSubprotocol/README.md:3` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R043 | `companion/examples/WebSocket-Echo-ServerSubprotocol/README.md:3` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R044 | `companion/exercises/README.md:8` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R045 | `companion/exercises/README.md:9` | Chapter 1 | Chapter 1 | retain number; recheck semantic target |
| R046 | `companion/exercises/README.md:24` | Chapter 1, 23, and 35 | Chapter 1, Chapter 18, Chapter 28 | renumber to listed destinations; retain target meaning |
| R047 | `companion/exercises/README.md:26` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R048 | `companion/exercises/README.md:28` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R049 | `companion/exercises/README.md:28` | Chapter 37 | Chapter 30 | renumber to listed destinations; retain target meaning |
| R050 | `companion/exercises/ch01/README.md:1` | Chapter 1 | Chapter 1 | retain number; recheck semantic target |
| R051 | `companion/exercises/ch01/README.md:23` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R052 | `companion/exercises/ch01/README.md:31` | Chapter 1 | Chapter 1 | retain number; recheck semantic target |
| R053 | `companion/exercises/ch01/README.md:47` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R054 | `companion/exercises/ch03/README.md:1` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R055 | `companion/exercises/ch23/README.md:1` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R056 | `companion/exercises/ch35/README.md:1` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R057 | `companion/exercises/ch37/README.md:1` | Chapter 37 | Chapter 30 | renumber to listed destinations; retain target meaning |
| R058 | `companion/exercises/ch37/README.md:30` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R059 | `manuscript/backmatter/further-reading.md:14` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R060 | `manuscript/backmatter/further-reading.md:32` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R061 | `manuscript/backmatter/further-reading.md:61` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R062 | `manuscript/backmatter/further-reading.md:63` | Chapter 12 | Chapter 8 | renumber to listed destinations; retain target meaning |
| R063 | `manuscript/chapters/01-why-snodec-exists.md:59` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R064 | `manuscript/chapters/01-why-snodec-exists.md:126` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R065 | `manuscript/chapters/01-why-snodec-exists.md:126` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R066 | `manuscript/chapters/01-why-snodec-exists.md:174` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R067 | `manuscript/chapters/01-why-snodec-exists.md:174` | Chapter 5 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R068 | `manuscript/chapters/01-why-snodec-exists.md:192` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R069 | `manuscript/chapters/01-why-snodec-exists.md:193` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R070 | `manuscript/chapters/02-preparing-your-environment.md:257` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R071 | `manuscript/chapters/02-preparing-your-environment.md:288` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R072 | `manuscript/chapters/02-preparing-your-environment.md:339` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R073 | `manuscript/chapters/02-preparing-your-environment.md:355` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R074 | `manuscript/chapters/02-preparing-your-environment.md:387` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R075 | `manuscript/chapters/02-preparing-your-environment.md:449` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R076 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:41` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R077 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:44` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R078 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:73` | Chapter 5 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R079 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:246` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R080 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:328` | Chapters 9 and 20 | Chapter 7, Chapter 15 | renumber to listed destinations; retain target meaning |
| R081 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:395` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R082 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:457` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R083 | `manuscript/chapters/03-your-first-working-program-the-echo-pair.md:466` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R084 | `manuscript/chapters/04-reading-the-codebase-with-confidence.md:500` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R085 | `manuscript/chapters/04-reading-the-codebase-with-confidence.md:572` | Chapter 5 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R086 | `manuscript/chapters/05-the-mental-model-of-snodec.md:10` | Chapter 4 | Chapter 4 (source-reading introduction) | rewrite as within-chapter introduction; do not assume Appendix A was read |
| R087 | `manuscript/chapters/05-the-mental-model-of-snodec.md:268` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R088 | `manuscript/chapters/05-the-mental-model-of-snodec.md:393` | Chapter 4 | Chapter 4 (source-reading introduction) | rewrite as within-chapter introduction; do not assume Appendix A was read |
| R089 | `manuscript/chapters/05-the-mental-model-of-snodec.md:589` | Chapter 6 | Chapter 5 | renumber to listed destinations; retain target meaning |
| R090 | `manuscript/chapters/05-the-mental-model-of-snodec.md:589` | Chapter 7 | Chapter 4 | replace self-reference with named section/earlier discussion; retain other destinations |
| R091 | `manuscript/chapters/06-core-runtime-and-event-processing.md:119` | Chapters 16 and 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R092 | `manuscript/chapters/06-core-runtime-and-event-processing.md:185` | Chapter 30 | Chapter 24 | renumber to listed destinations; retain target meaning |
| R093 | `manuscript/chapters/06-core-runtime-and-event-processing.md:243` | Chapter 5 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R094 | `manuscript/chapters/06-core-runtime-and-event-processing.md:514` | Chapter 5 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R095 | `manuscript/chapters/06-core-runtime-and-event-processing.md:589` | Chapters 19 and 20 | Chapter 14, Chapter 15 | renumber to listed destinations; retain target meaning |
| R096 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:3` | CHAPTER 7 | Chapter 4 | replace self-reference with named section/earlier discussion; retain other destinations |
| R097 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:3` | CHAPTER 7 | Chapter 4 | replace self-reference with named section/earlier discussion; retain other destinations |
| R098 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:44` | Chapter 6 | Chapter 5 | renumber to listed destinations; retain target meaning |
| R099 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:88` | Chapters 5 and 6 | Chapter 4, Chapter 5 | replace self-reference with named section/earlier discussion; retain other destinations |
| R100 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:194` | Chapter 8 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R101 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:297` | Chapter 19 | Chapter 14 | renumber to listed destinations; retain target meaning |
| R102 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:353` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R103 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:447` | Chapter 19 | Chapter 14 | renumber to listed destinations; retain target meaning |
| R104 | `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:447` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R105 | `manuscript/chapters/08-socket-addresses-and-address-semantics.md:59` | Chapter 7 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R106 | `manuscript/chapters/08-socket-addresses-and-address-semantics.md:101` | Chapter 7 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R107 | `manuscript/chapters/08-socket-addresses-and-address-semantics.md:219` | Chapter 11 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R108 | `manuscript/chapters/08-socket-addresses-and-address-semantics.md:403` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R109 | `manuscript/chapters/09-servers-clients-and-connections.md:10` | Chapter 8 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R110 | `manuscript/chapters/09-servers-clients-and-connections.md:225` | Chapter 8 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R111 | `manuscript/chapters/09-servers-clients-and-connections.md:373` | Chapter 8 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R112 | `manuscript/chapters/09-servers-clients-and-connections.md:397` | Chapter 8 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R113 | `manuscript/chapters/09-servers-clients-and-connections.md:437` | Chapter 6 | Chapter 5 | renumber to listed destinations; retain target meaning |
| R114 | `manuscript/chapters/09-servers-clients-and-connections.md:554` | Chapter 9 | Chapter 7 | replace self-reference with named section/earlier discussion; retain other destinations |
| R115 | `manuscript/chapters/09-servers-clients-and-connections.md:582` | Chapter 19 | Chapter 14 | renumber to listed destinations; retain target meaning |
| R116 | `manuscript/chapters/09-servers-clients-and-connections.md:616` | Chapter 9 | Chapter 7 | replace self-reference with named section/earlier discussion; retain other destinations |
| R117 | `manuscript/chapters/09-servers-clients-and-connections.md:628` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R118 | `manuscript/chapters/09-servers-clients-and-connections.md:628` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R119 | `manuscript/chapters/09-servers-clients-and-connections.md:655` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R120 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:90` | Chapter 7 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R121 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:100` | Chapter 8 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R122 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:117` | Chapter 8 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R123 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:125` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R124 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:174` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R125 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:237` | Chapter 8 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R126 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:256` | Chapter 8 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R127 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:256` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R128 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:258` | Chapter 8 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R129 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:258` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R130 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:258` | Chapter 10 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R131 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:379` | Chapters 8 and 9 | Chapter 6, Chapter 7 | replace self-reference with named section/earlier discussion; retain other destinations |
| R132 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:379` | Chapter 8 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R133 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:379` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R134 | `manuscript/chapters/10-ipv4-and-ipv6-as-the-first-concrete-network-families.md:425` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R135 | `manuscript/chapters/11-unix-domain-sockets.md:50` | Chapter 10 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R136 | `manuscript/chapters/11-unix-domain-sockets.md:198` | Chapter 10 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R137 | `manuscript/chapters/11-unix-domain-sockets.md:251` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R138 | `manuscript/chapters/11-unix-domain-sockets.md:298` | Chapter 7 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R139 | `manuscript/chapters/11-unix-domain-sockets.md:409` | Chapters 8--12 | Chapter 6, Chapter 7, Chapter 8 | replace self-reference with named section/earlier discussion; retain other destinations |
| R140 | `manuscript/chapters/11-unix-domain-sockets.md:424` | Chapter 11 | Chapter 6 | replace self-reference with named section/earlier discussion; retain other destinations |
| R141 | `manuscript/chapters/11-unix-domain-sockets.md:424` | Chapter 12 | Chapter 8 | renumber to listed destinations; retain target meaning |
| R142 | `manuscript/chapters/11-unix-domain-sockets.md:456` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R143 | `manuscript/chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md:129` | Chapter 8 | Chapter 6 | renumber to listed destinations; retain target meaning |
| R144 | `manuscript/chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md:267` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R145 | `manuscript/chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md:346` | Chapter 7 | Chapter 4 | renumber to listed destinations; retain target meaning |
| R146 | `manuscript/chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md:366` | Chapter 15 | Chapter 11 | renumber to listed destinations; retain target meaning |
| R147 | `manuscript/chapters/12-bluetooth-in-snodec-rfcomm-and-l2cap.md:421` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R148 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:210` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R149 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:321` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R150 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:371` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R151 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:377` | Chapter 6 | Chapter 5 | renumber to listed destinations; retain target meaning |
| R152 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:459` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R153 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:570` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R154 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:634` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R155 | `manuscript/chapters/13-writing-socketcontext-classes-well.md:638` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R156 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:130` | Chapters 9, 13, and 14 | Chapter 7, Chapter 9, Chapter 10 | replace self-reference with named section/earlier discussion; retain other destinations |
| R157 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:130` | Chapter 9 | Chapter 7 | renumber to listed destinations; retain target meaning |
| R158 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:130` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R159 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:161` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R160 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:226` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R161 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:226` | Chapter 14 | Chapter 10 | replace self-reference with named section/earlier discussion; retain other destinations |
| R162 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:333` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R163 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:585` | Chapter 15 | Chapter 11 | renumber to listed destinations; retain target meaning |
| R164 | `manuscript/chapters/14-writing-socketcontextfactory-classes-well.md:587` | Chapter 15 | Chapter 11 | renumber to listed destinations; retain target meaning |
| R165 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:35` | Chapters 13 and 14 | Chapter 9, Chapter 10 | renumber to listed destinations; retain target meaning |
| R166 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:111` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R167 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:143` | Chapters 13 and 14 | Chapter 9, Chapter 10 | renumber to listed destinations; retain target meaning |
| R168 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:198` | Chapters 8 through 12 | Chapter 6, Chapter 7, Chapter 8 | renumber to listed destinations; retain target meaning |
| R169 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:297` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R170 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:297` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R171 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:341` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R172 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:369` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R173 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:421` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R174 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:480` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R175 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:488` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R176 | `manuscript/chapters/15-building-the-same-protocol-over-different-lower-layers.md:604` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R177 | `manuscript/chapters/16-configuration-philosophy-in-snodec.md:48` | Chapter 15 | Chapter 11 | renumber to listed destinations; retain target meaning |
| R178 | `manuscript/chapters/16-configuration-philosophy-in-snodec.md:250` | Chapter 17 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R179 | `manuscript/chapters/16-configuration-philosophy-in-snodec.md:393` | Chapters 8–12 | Chapter 6, Chapter 7, Chapter 8 | renumber to listed destinations; retain target meaning |
| R180 | `manuscript/chapters/16-configuration-philosophy-in-snodec.md:423` | Chapter 17 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R181 | `manuscript/chapters/16-configuration-philosophy-in-snodec.md:425` | Chapter 16 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R182 | `manuscript/chapters/16-configuration-philosophy-in-snodec.md:548` | Chapter 17 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R183 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:174` | Chapter 16 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R184 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:188` | Chapter 16 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R185 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:190` | Chapter 17 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R186 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:376` | Chapter 19 | Chapter 14 | renumber to listed destinations; retain target meaning |
| R187 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:385` | Chapter 16 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R188 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:387` | Chapter 17 | Chapter 12 | replace self-reference with named section/earlier discussion; retain other destinations |
| R189 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:474` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R190 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:514` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R191 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:687` | Chapters 18, 20, 21, and 24 | Chapter 13, Chapter 15, Chapter 16, Chapter 19 | renumber to listed destinations; retain target meaning |
| R192 | `manuscript/chapters/17-application-and-instance-configuration-in-detail.md:760` | Chapters 08–12 | Chapter 6, Chapter 7, Chapter 8 | renumber to listed destinations; retain target meaning |
| R193 | `manuscript/chapters/18-logging-diagnostics-and-runtime-introspection.md:29` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R194 | `manuscript/chapters/18-logging-diagnostics-and-runtime-introspection.md:308` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R195 | `manuscript/chapters/18-logging-diagnostics-and-runtime-introspection.md:400` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R196 | `manuscript/chapters/19-tls-across-the-framework.md:119` | Chapter 14 | Chapter 10 | renumber to listed destinations; retain target meaning |
| R197 | `manuscript/chapters/19-tls-across-the-framework.md:120` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R198 | `manuscript/chapters/19-tls-across-the-framework.md:240` | Chapters 16 and 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R199 | `manuscript/chapters/19-tls-across-the-framework.md:314` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R200 | `manuscript/chapters/19-tls-across-the-framework.md:454` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R201 | `manuscript/chapters/19-tls-across-the-framework.md:475` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R202 | `manuscript/chapters/19-tls-across-the-framework.md:494` | Chapter 15 | Chapter 11 | renumber to listed destinations; retain target meaning |
| R203 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:235` | Chapter 19 | Chapter 14 | renumber to listed destinations; retain target meaning |
| R204 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:235` | Chapter 20 | Chapter 15 | replace self-reference with named section/earlier discussion; retain other destinations |
| R205 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:578` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R206 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:587` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R207 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:614` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R208 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:622` | Chapter 13 | Chapter 9 | renumber to listed destinations; retain target meaning |
| R209 | `manuscript/chapters/20-timeouts-retries-and-failure-modes.md:658` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R210 | `manuscript/chapters/21-the-http-layer.md:37` | Chapter 21 | Chapter 16 | replace self-reference with named section/earlier discussion; retain other destinations |
| R211 | `manuscript/chapters/21-the-http-layer.md:160` | Chapters 13 and 14 | Chapter 9, Chapter 10 | renumber to listed destinations; retain target meaning |
| R212 | `manuscript/chapters/21-the-http-layer.md:242` | Chapters 16 and 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R213 | `manuscript/chapters/21-the-http-layer.md:460` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R214 | `manuscript/chapters/21-the-http-layer.md:478` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R215 | `manuscript/chapters/21-the-http-layer.md:478` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R216 | `manuscript/chapters/21-the-http-layer.md:501` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R217 | `manuscript/chapters/21-the-http-layer.md:507` | Chapter 21 | Chapter 16 | replace self-reference with named section/earlier discussion; retain other destinations |
| R218 | `manuscript/chapters/21-the-http-layer.md:513` | Chapter 21 | Chapter 16 | replace self-reference with named section/earlier discussion; retain other destinations |
| R219 | `manuscript/chapters/21-the-http-layer.md:513` | Chapter 22 | Chapter 17 | renumber to listed destinations; retain target meaning |
| R220 | `manuscript/chapters/21-the-http-layer.md:543` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R221 | `manuscript/chapters/22-the-express-like-framework.md:123` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R222 | `manuscript/chapters/22-the-express-like-framework.md:153` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R223 | `manuscript/chapters/22-the-express-like-framework.md:338` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R224 | `manuscript/chapters/22-the-express-like-framework.md:338` | Chapter 22 | Chapter 17 | replace self-reference with named section/earlier discussion; retain other destinations |
| R225 | `manuscript/chapters/22-the-express-like-framework.md:474` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R226 | `manuscript/chapters/22-the-express-like-framework.md:493` | Chapter 22 | Chapter 17 | replace self-reference with named section/earlier discussion; retain other destinations |
| R227 | `manuscript/chapters/22-the-express-like-framework.md:493` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R228 | `manuscript/chapters/22-the-express-like-framework.md:493` | Chapter 22 | Chapter 17 | replace self-reference with named section/earlier discussion; retain other destinations |
| R229 | `manuscript/chapters/22-the-express-like-framework.md:509` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R230 | `manuscript/chapters/22-the-express-like-framework.md:544` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R231 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:44` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R232 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:359` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R233 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:363` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R234 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:376` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R235 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:410` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R236 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:410` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R237 | `manuscript/chapters/23-server-sent-events-and-real-time-http.md:431` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R238 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:61` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R239 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:77` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R240 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:308` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R241 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:377` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R242 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:611` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R243 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:611` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R244 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:635` | Chapter 24 | Chapter 19 | replace self-reference with named section/earlier discussion; retain other destinations |
| R245 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:643` | Chapter 26 | Chapter 21 | renumber to listed destinations; retain target meaning |
| R246 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:650` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R247 | `manuscript/chapters/24-websocket-and-protocol-upgrade.md:668` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R248 | `manuscript/chapters/25-mqtt-support-in-snodec.md:32` | Chapter 25 | Chapter 20 | replace self-reference with named section/earlier discussion; retain other destinations |
| R249 | `manuscript/chapters/25-mqtt-support-in-snodec.md:32` | Chapter 26 | Chapter 21 | renumber to listed destinations; retain target meaning |
| R250 | `manuscript/chapters/25-mqtt-support-in-snodec.md:61` | Chapter 26 | Chapter 21 | renumber to listed destinations; retain target meaning |
| R251 | `manuscript/chapters/25-mqtt-support-in-snodec.md:69` | Chapter 26 | Chapter 21 | renumber to listed destinations; retain target meaning |
| R252 | `manuscript/chapters/25-mqtt-support-in-snodec.md:221` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R253 | `manuscript/chapters/25-mqtt-support-in-snodec.md:221` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R254 | `manuscript/chapters/25-mqtt-support-in-snodec.md:298` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R255 | `manuscript/chapters/25-mqtt-support-in-snodec.md:428` | Chapter 31 | Chapter 24 | renumber to listed destinations; retain target meaning |
| R256 | `manuscript/chapters/25-mqtt-support-in-snodec.md:436` | Chapter 25 | Chapter 20 | replace self-reference with named section/earlier discussion; retain other destinations |
| R257 | `manuscript/chapters/25-mqtt-support-in-snodec.md:436` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R258 | `manuscript/chapters/25-mqtt-support-in-snodec.md:444` | Chapter 26 | Chapter 21 | renumber to listed destinations; retain target meaning |
| R259 | `manuscript/chapters/25-mqtt-support-in-snodec.md:446` | Chapter 25 | Chapter 20 | replace self-reference with named section/earlier discussion; retain other destinations |
| R260 | `manuscript/chapters/25-mqtt-support-in-snodec.md:460` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R261 | `manuscript/chapters/25-mqtt-support-in-snodec.md:512` | Chapter 27 | Chapter 22 | renumber to listed destinations; retain target meaning |
| R262 | `manuscript/chapters/25-mqtt-support-in-snodec.md:512` | Chapter 25 | Chapter 20 | replace self-reference with named section/earlier discussion; retain other destinations |
| R263 | `manuscript/chapters/26-mqtt-over-websocket.md:32` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R264 | `manuscript/chapters/26-mqtt-over-websocket.md:32` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R265 | `manuscript/chapters/26-mqtt-over-websocket.md:60` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R266 | `manuscript/chapters/26-mqtt-over-websocket.md:60` | Chapter 26 | Chapter 21 | replace self-reference with named section/earlier discussion; retain other destinations |
| R267 | `manuscript/chapters/26-mqtt-over-websocket.md:266` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R268 | `manuscript/chapters/26-mqtt-over-websocket.md:285` | Chapter 6 | Chapter 5 | renumber to listed destinations; retain target meaning |
| R269 | `manuscript/chapters/26-mqtt-over-websocket.md:287` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R270 | `manuscript/chapters/26-mqtt-over-websocket.md:312` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R271 | `manuscript/chapters/26-mqtt-over-websocket.md:431` | Chapter 26 | Chapter 21 | replace self-reference with named section/earlier discussion; retain other destinations |
| R272 | `manuscript/chapters/26-mqtt-over-websocket.md:439` | Chapter 27 | Chapter 22 | renumber to listed destinations; retain target meaning |
| R273 | `manuscript/chapters/26-mqtt-over-websocket.md:493` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R274 | `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:260` | Chapter 26 | Chapter 21 | renumber to listed destinations; retain target meaning |
| R275 | `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:314` | Chapter 16 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R276 | `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:314` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R277 | `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:330` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R278 | `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:383` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R279 | `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:432` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R280 | `manuscript/chapters/28-database-support-and-application-state.md:252` | Chapter 28 | Chapter 23 | replace self-reference with named section/earlier discussion; retain other destinations |
| R281 | `manuscript/chapters/28-database-support-and-application-state.md:563` | Chapter 27 | Chapter 22 | renumber to listed destinations; retain target meaning |
| R282 | `manuscript/chapters/28-database-support-and-application-state.md:610` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R283 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:375` | Chapter 16 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R284 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:375` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R285 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:375` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R286 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:426` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R287 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:494` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R288 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:494` | Chapter 29 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R289 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:511` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R290 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:526` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R291 | `manuscript/chapters/29-learning-from-the-applications-in-src-apps.md:534` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R292 | `manuscript/chapters/30-from-applications-to-systems.md:34` | Chapter 29 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R293 | `manuscript/chapters/30-from-applications-to-systems.md:37` | Chapter 30 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R294 | `manuscript/chapters/30-from-applications-to-systems.md:40` | Chapter 31 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R295 | `manuscript/chapters/30-from-applications-to-systems.md:106` | Chapter 31 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R296 | `manuscript/chapters/30-from-applications-to-systems.md:199` | Chapter 27 | Chapter 22 | renumber to listed destinations; retain target meaning |
| R297 | `manuscript/chapters/30-from-applications-to-systems.md:271` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R298 | `manuscript/chapters/30-from-applications-to-systems.md:297` | Chapters 16 and 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R299 | `manuscript/chapters/30-from-applications-to-systems.md:391` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R300 | `manuscript/chapters/30-from-applications-to-systems.md:391` | Chapter 30 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R301 | `manuscript/chapters/30-from-applications-to-systems.md:399` | Chapter 29 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R302 | `manuscript/chapters/30-from-applications-to-systems.md:417` | Chapter 15 | Chapter 11 | renumber to listed destinations; retain target meaning |
| R303 | `manuscript/chapters/30-from-applications-to-systems.md:467` | Chapter 29 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R304 | `manuscript/chapters/31-mqttsuite-as-a-reference-ecosystem.md:12` | Chapter 30 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R305 | `manuscript/chapters/31-mqttsuite-as-a-reference-ecosystem.md:88` | Chapter 29 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R306 | `manuscript/chapters/31-mqttsuite-as-a-reference-ecosystem.md:150` | Chapter 30 | Chapter 24 | replace self-reference with named section/earlier discussion; retain other destinations |
| R307 | `manuscript/chapters/31-mqttsuite-as-a-reference-ecosystem.md:284` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R308 | `manuscript/chapters/31-mqttsuite-as-a-reference-ecosystem.md:399` | Chapter 25 | Chapter 20 | renumber to listed destinations; retain target meaning |
| R309 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:589` | Chapter 21 | Chapter 16 | renumber to listed destinations; retain target meaning |
| R310 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:589` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R311 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:589` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R312 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:599` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R313 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:652` | Chapter 24 | Chapter 19 | renumber to listed destinations; retain target meaning |
| R314 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:728` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R315 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:761` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R316 | `manuscript/chapters/32-cmake-components-and-linking-strategy.md:919` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R317 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:71` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R318 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:135` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R319 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:143` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R320 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:169` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R321 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:311` | Chapter 3 | Chapter 3 | retain number; recheck semantic target |
| R322 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:425` | Chapter 28 | Chapter 23 | renumber to listed destinations; retain target meaning |
| R323 | `manuscript/chapters/33-deployment-on-linux-and-openwrt.md:684` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R324 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:51` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R325 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:141` | Chapters 18 and 21 | Chapter 13, Chapter 16 | renumber to listed destinations; retain target meaning |
| R326 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:149` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R327 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:157` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R328 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:184` | Chapters 10, 11, and 15 | Chapter 6, Chapter 11 | renumber to listed destinations; retain target meaning |
| R329 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:206` | Chapter 17 | Chapter 12 | renumber to listed destinations; retain target meaning |
| R330 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:249` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R331 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:355` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R332 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:355` | Chapter 34 | Chapter 27 | replace self-reference with named section/earlier discussion; retain other destinations |
| R333 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:393` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R334 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:401` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R335 | `manuscript/chapters/34-testing-debugging-and-benchmarking.md:531` | Chapter 33 | Chapter 26 | renumber to listed destinations; retain target meaning |
| R336 | `manuscript/chapters/35-building-minigateway.md:53` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R337 | `manuscript/chapters/35-building-minigateway.md:191` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R338 | `manuscript/chapters/35-building-minigateway.md:212` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R339 | `manuscript/chapters/35-building-minigateway.md:422` | Chapter 23 | Chapter 18 | renumber to listed destinations; retain target meaning |
| R340 | `manuscript/chapters/35-building-minigateway.md:1229` | Chapter 35 | Chapter 28 | renumber printed README together with canonical companion README; preserve exact source-marker agreement |
| R341 | `manuscript/chapters/35-building-minigateway.md:1256` | Chapter 35 | Chapter 28 | renumber printed README together with canonical companion README; preserve exact source-marker agreement |
| R342 | `manuscript/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md:3` | CHAPTER 37 | Chapter 30 | replace self-reference with named section/earlier discussion; retain other destinations |
| R343 | `manuscript/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md:3` | CHAPTER 37 | Chapter 30 | replace self-reference with named section/earlier discussion; retain other destinations |
| R344 | `manuscript/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md:144` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R345 | `manuscript/chapters/38-extending-the-framework-safely.md:367` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R346 | `manuscript/chapters/38-extending-the-framework-safely.md:432` | Chapter 18 | Chapter 13 | renumber to listed destinations; retain target meaning |
| R347 | `manuscript/chapters/38-extending-the-framework-safely.md:470` | Chapter 34 | Chapter 27 | renumber to listed destinations; retain target meaning |
| R348 | `manuscript/chapters/38-extending-the-framework-safely.md:502` | Chapter 20 | Chapter 15 | renumber to listed destinations; retain target meaning |
| R349 | `manuscript/chapters/38-extending-the-framework-safely.md:547` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R350 | `manuscript/frontmatter/conventions.md:11` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R351 | `manuscript/frontmatter/conventions.md:19` | Chapters 5, 9, and 20 | Chapter 4, Chapter 7, Chapter 15 | renumber to listed destinations; retain target meaning |
| R352 | `manuscript/frontmatter/how-to-read-this-book.md:13` | Chapter 32 | Chapter 25 | renumber to listed destinations; retain target meaning |
| R353 | `manuscript/frontmatter/how-to-read-this-book.md:23` | Chapters 1--7 | Chapter 1, Chapter 2, Chapter 3, Chapter 4, Chapter 5 | foundation becomes Chapters 1–5; Appendix A is optional and excluded |
| R354 | `manuscript/frontmatter/how-to-read-this-book.md:23` | Chapters 8--20 | Chapter 6, Chapter 7, Chapter 8, Chapter 9, Chapter 10, Chapter 11, Chapter 12, Chapter 13, Chapter 14, Chapter 15 | renumber to listed destinations; retain target meaning |
| R355 | `manuscript/frontmatter/how-to-read-this-book.md:24` | Chapters 21--28 | Chapter 16, Chapter 17, Chapter 18, Chapter 19, Chapter 20, Chapter 21, Chapter 22, Chapter 23 | renumber to listed destinations; retain target meaning |
| R356 | `manuscript/frontmatter/how-to-read-this-book.md:24` | Chapters 35--36 | Chapter 28, Chapter 29 | renumber to listed destinations; retain target meaning |
| R357 | `manuscript/frontmatter/how-to-read-this-book.md:24` | Chapters 30, 32--34, and 37 | Chapter 24, Chapter 25, Chapter 26, Chapter 27, Chapter 30 | renumber to listed destinations; retain target meaning |
| R358 | `manuscript/frontmatter/how-to-read-this-book.md:25` | Chapter 4 | Appendix A | renumber to listed destinations; retain target meaning |
| R359 | `manuscript/frontmatter/how-to-read-this-book.md:25` | Chapters 5--20 | Chapter 4, Chapter 5, Chapter 6, Chapter 7, Chapter 8, Chapter 9, Chapter 10, Chapter 11, Chapter 12, Chapter 13, Chapter 14, Chapter 15 | renumber to listed destinations; retain target meaning |
| R360 | `manuscript/frontmatter/how-to-read-this-book.md:25` | Chapters 29, 32, 34, and 38 | Chapter 24, Chapter 25, Chapter 27, Appendix A | renumber to listed destinations; retain target meaning |
| R361 | `manuscript/frontmatter/how-to-read-this-book.md:27` | Chapters 27, 30, and 37 | Chapter 22, Chapter 24, Chapter 30 | renumber to listed destinations; retain target meaning |
| R362 | `manuscript/frontmatter/preface.md:27` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R363 | `manuscript/frontmatter/preface.md:31` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |
| R364 | `manuscript/parts/part-11-building-a-minigateway-application.md:7` | Chapter 35 | Chapter 28 | renumber to listed destinations; retain target meaning |
| R365 | `manuscript/parts/part-11-building-a-minigateway-application.md:7` | Chapter 36 | Chapter 29 | renumber to listed destinations; retain target meaning |
| R366 | `manuscript/parts/part-12-designing-with-snodec.md:5` | Chapter 37 | Chapter 30 | renumber to listed destinations; retain target meaning |
| R367 | `manuscript/parts/part-12-designing-with-snodec.md:5` | Chapter 38 | Appendix A | renumber to listed destinations; retain target meaning |
| R368 | `review/proposal/book-proposal-package.md:32` | Chapters 35–36 | Chapter 28, Chapter 29 | renumber to listed destinations; retain target meaning |
| R369 | `review/proposal/book-proposal-package.md:34` | Chapters 1–7 | Chapter 1, Chapter 2, Chapter 3, Chapter 4, Chapter 5 | foundation becomes Chapters 1–5; Appendix A is optional and excluded |
| R370 | `review/proposal/book-proposal-package.md:34` | Chapters 16–18 and 20–23, then 25, 32, and 35 | Chapter 12, Chapter 13, Chapter 15, Chapter 16, Chapter 17, Chapter 18, Chapter 20, Chapter 25, Chapter 28 | renumber to listed destinations; retain target meaning |
| R371 | `review/proposal/book-proposal-package.md:116` | Chapters 1, 3, 23, 35, and 37 | Chapter 1, Chapter 3, Chapter 18, Chapter 28, Chapter 30 | renumber to listed destinations; retain target meaning |
| R372 | `review/proposal/book-proposal-package.md:129` | Chapters 35–36 | Chapter 28, Chapter 29 | renumber to listed destinations; retain target meaning |
| R373 | `review/proposal/evidence-sheet.md:18` | Chapters 1, 3, 23, 35, and 37 | Chapter 1, Chapter 3, Chapter 18, Chapter 28, Chapter 30 | renumber to listed destinations; retain target meaning |
| R374 | `review/proposal/sample-chapters.md:11` | Chapter 2 | Chapter 2 | retain number; recheck semantic target |

## Manual running-head and section-number overrides

Recompute chapter/section labels after movement and condensation; retain semantic anchor IDs.

| Source:line | Current override | Destination |
| --- | --- | --- |
| `manuscript/chapters/04-reading-the-codebase-with-confidence.md:358` | `\SNodeCNextSectionMark{4.13. SOURCE PATHS, PUBLIC INCLUDES, COMPONENTS}` | A |
| `manuscript/chapters/06-core-runtime-and-event-processing.md:455` | `\SNodeCNextSectionMark{6.14. DESCRIPTOR EVENT RECEIVERS}` | 5 |
| `manuscript/chapters/07-layers-in-practice-network-transport-connection-application.md:3` | `\markboth{CHAPTER 7. LAYERS IN PRACTICE}{CHAPTER 7. LAYERS IN PRACTICE}` | 4 |
| `manuscript/chapters/27-designing-iot-systems-with-multiple-protocols.md:161` | `\SNodeCNextSectionMark{27.6. TELEMETRY, CONTROL, OBSERVATION, ADMINISTRATION}` | 22 |
| `manuscript/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md:3` | `\markboth{CHAPTER 37. ARCHITECTURAL JUDGMENT}{CHAPTER 37. ARCHITECTURAL JUDGMENT}` | 30 |

## Part references

Parts I–X retain their numbers. Old Parts XI and XII become Part XI; rewrite the contributor-appendix transition. The epilogue stays unnumbered. Ranges and combined expressions also need review.

| Source:line | Current expression |
| --- | --- |
| `manuscript/chapters/04-reading-the-codebase-with-confidence.md:572` | Part I |
| `manuscript/chapters/11-unix-domain-sockets.md:19` | Part III |
| `manuscript/chapters/16-configuration-philosophy-in-snodec.md:18` | Part IV |
| `manuscript/chapters/16-configuration-philosophy-in-snodec.md:18` | Part V |
| `manuscript/chapters/22-the-express-like-framework.md:493` | Part VII |
| `manuscript/chapters/32-cmake-components-and-linking-strategy.md:9` | Part X |
| `manuscript/chapters/32-cmake-components-and-linking-strategy.md:13` | Part IX |
| `manuscript/chapters/32-cmake-components-and-linking-strategy.md:13` | Part X |
| `manuscript/frontmatter/how-to-read-this-book.md:5` | Parts I and II |
| `manuscript/frontmatter/how-to-read-this-book.md:7` | Parts III and IV |
| `manuscript/frontmatter/how-to-read-this-book.md:9` | Parts V and VI |
| `manuscript/frontmatter/how-to-read-this-book.md:11` | Parts VII and VIII |
| `manuscript/frontmatter/how-to-read-this-book.md:13` | Parts IX and X |
| `manuscript/frontmatter/how-to-read-this-book.md:15` | Parts XI and XII |
| `manuscript/parts/part-01-getting-oriented.md:5` | Part II |
| `manuscript/parts/part-02-the-snodec-architecture.md:5` | Part III |
| `manuscript/parts/part-03-networking-foundations-in-snodec.md:3` | Part II |
| `manuscript/parts/part-03-networking-foundations-in-snodec.md:5` | Part IV |
| `manuscript/parts/part-04-from-raw-connections-to-application-protocols.md:5` | Part V |
| `manuscript/parts/part-05-configuration-and-operational-behavior.md:3` | Part IV |
| `manuscript/parts/part-05-configuration-and-operational-behavior.md:5` | Part VI |
| `manuscript/parts/part-06-secure-and-robust-communication.md:3` | Part V |
| `manuscript/parts/part-06-secure-and-robust-communication.md:5` | Part VII |
| `manuscript/parts/part-07-web-protocols-and-web-applications.md:3` | Part VI |
| `manuscript/parts/part-07-web-protocols-and-web-applications.md:5` | Part VIII |
| `manuscript/parts/part-08-iot-and-message-oriented-systems.md:5` | Part IX |
| `manuscript/parts/part-09-persistence-and-full-systems.md:3` | Part VIII |
| `manuscript/parts/part-09-persistence-and-full-systems.md:5` | Part X |
| `manuscript/parts/part-10-building-porting-and-maintaining.md:3` | Part IX |
| `manuscript/parts/part-10-building-porting-and-maintaining.md:5` | Part XI |
