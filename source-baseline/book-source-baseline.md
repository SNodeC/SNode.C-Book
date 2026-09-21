# Book Source Baseline

Current source: SNode.C 2.0.0, base commit `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`
plus the current source changes captured in `framework-working-tree.patch`.

The machine-readable authority is `book-source-baseline.env`; the reader checkout
and scope are documented in `SOURCE-VERSION.md`. The file manifest records the
contents of the actual local source tree, including uncommitted changes. This is a reproducible source snapshot,
not a newly created release tag.

The migration updates semantic logging, the test architecture, resource policy,
shutdown, configuration discovery, installed-consumer guidance, and affected
companion listings. Compilation and behavioral evidence must identify both the
book revision and this framework working-tree digest. The base commit alone is
insufficient to identify the refined edition. Historical author confirmations remain
historical and are not relabeled as new automated or independent verification.

The combined editorial pass refreshed this snapshot after the author committed
per-call flow controllers and checked runtime reconfiguration, then included the
author's subsequent uncommitted binary-logging changes. The final local HEAD
is `2e52b6b7337f21812932eb1e097fb3c27c8228a9`; the reconstruction base remains unchanged.
Current test results and their limits are recorded in `review/editorial/`.
