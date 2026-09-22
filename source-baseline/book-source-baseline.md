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

The current local HEAD is `37b3a1e16de436c818eed807ee8a962f7cbbf43b`, including the author's
committed C++20 build policy at the project root. The staged installed-consumer
test additionally sets its runtime library path to its temporary installation.
That two-line test-support change is included in the captured patch; the
reconstruction base remains unchanged. The manuscript and application sources
are unchanged by this repair. Current CI-repair evidence is recorded in
`review/ci-fix-2026-09-22/`; earlier editorial results retain their original
source identities.
