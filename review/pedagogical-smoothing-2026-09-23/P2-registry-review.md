# P2 registry migration

Updated manuscript/book-files.txt, smoothing-structure.json and
smoothing-reference-register.json; ci/check-chapter-references.py and its six
regression tests; source-claims.json; all exercise directory, CMake target, CTest,
relative driver and public-answer paths; source markers; teaching/lifetime CI
paths; README.md, STRUCTURE.md, How to Read, affected Part openers; proposal
sample CMake paths, chapter/sample/Part tables, source metrics and pending page
extents; work-plan current Chapter ledger and this pass's chapter-ledger.md.

The reference registry retains existing topic targets and 374 historical
migration dispositions. Split references follow the topic they actually named.
The missing-anchor regression now removes the anchor from its new owner, Ch5;
its assertion is unchanged. The exact pre-split identity multiplicities (Ch4 and
Ch24 twice, every other chapter once) remain asserted.

Every registered framework anchor is preserved exactly (P2-source-preservation.json).
No framework manifest/digest changes. Split Ch4 assigns the concrete TLS type
anchor to Layers; runtime registration, flows and connection ownership stay in
Ch4. Split Ch24 assigns app build/echo policy to Ch25 and runtime/system
composition to Ch26. No anchor dropped or added.

The full read-only sweep includes ci, review, source-baseline, production,
packaging and companion. Historical review pass folders and completed dated
verification reports remain unchanged; source-claims.json is the live verification
registry. Current orchestration is run-checks.py; prior R and shutdown-run scripts
remain records of their original runs. No stale live chapter filenames found.
P1 terminology counts remain an immutable phase measurement; its allowlist paths
now follow the moved text.

P2 moves existing apparatus and tests only. TODO(P3-apparatus) marks missing
objectives/exercises/answers for Ch4, 5, 25 and 26. The 62 existing CTests retain
all assertion code and timeout values. The new layer/composition/system
observations are added during P3 with canonical implementations.

Gate verified: 32 chapters plus Appendix A, 33 source records, 37 marked complete listings, six reference-checker regressions, hygiene, companion build and 62/62 public labs pass. Fresh metrics: 100,916 tokens. No assertion or timeout changes.
