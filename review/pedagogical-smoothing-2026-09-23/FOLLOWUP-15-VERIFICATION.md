# Follow-up 15 — verify-first ledger

Evidence below was inspected before the corresponding edit. Repository HEADs are in heads-followup-15-start.json; paths under build/followup-15 are fresh default-branch clones. Existence is not execution.

| Item | Finding at entry / HEAD evidence | Decision |
|---|---|---|
| A1 | source-baseline/book-source-baseline.env:5–6; ci/check-source-alignment.py:35–60 require a SHA and reader declarations repeat it; .github/workflows/companion-examples.yml:43 uses that value. Fresh snode.c master is content-identical to the edition manifest. | Reproduced; change checkout authority to master and retain digest/anchor checks. Chapter evidence already references framework_manifest (source-claims.json:3); no chapter SHA requirement exists separately, so retain that correct relation. |
| A2 | preface.md:36 and ch02:19,155,163,173–186 contain the pinned-checkout instructions. | Reproduced; replace with master clone/update and actionable content-drift guidance, retaining separate source/build/install areas. |
| A3 | OpenWRT/net/snode.c/Makefile:4 version 2.0.0; :10 selects OpenWRT; :70–80 hashed spdlog 1.17.0 download; :109–111 disconnected FetchContent; :347 net-un-phy. snode.c/src/net/un/phy/CMakeLists.txt:46–49 defines the valid SHARED target. ch28:255–257 instead describes 1.0.1 and an obsolete component. | Reproduced; correct the live feed description and re-rate every table row. Device/SDK rehearsal remains unexecuted deployment guidance. The feed's tag selection is reported outside this repository, not used as a checkout target. |
| A4 | mqttsuite/mqttbridge/lib/Mqtt.cpp:119–120 forwards to broker.getBridge().publish; mqttstore/lib/Mqtt.cpp:138–149 calls storage.store; MariaDbStorage.cpp:94–108 submits raw exec then calls storeProjections outside either callback; :300 defines the projection operation. | Verified; make the independent submission order explicit and guard external paths/symbols at master/main HEAD. |
