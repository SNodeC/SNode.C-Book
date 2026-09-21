# Target SNode.C Source Version

This edition targets the current SNode.C **2.0.0 working-tree snapshot** below. The version is
the CMake project version of that snapshot; it is not a claim that a `v2.0.0`
release tag exists.

- Repository: `SNodeC/snode.c`
- Authority: current local source contents, including uncommitted changes
- Project version: `2.0.0`
- Base commit: `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`
- Author-tree HEAD at final capture: `bb63e8a87aeda88123e8c0d72cb6d298908a9fe6` (C++20 build policy moved from `src/` to the project root)
- Exact tree digest: `f676e6cbeabbd8a14a0e2c64a254f688790c6a2e59a6b37daea28ea4f69a4df6`
- Changes from the reconstruction base: `framework-working-tree.patch`
- Exact file contents: `framework-working-tree.json`
- Baseline recorded: `2026-09-22`

## Reader checkout

Set `SNODEC_BOOK_SOURCE` to the absolute directory containing this edition's
book source package. The base commit alone does not contain the current per-call
flow API, checked runtime reconfiguration, or scoped binary logging described in this refinement. Apply the supplied patch and verify the
complete source contents before building.

```sh
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout --detach 1f0f728fc9b3b45174f2cd790d83b2f493e58af1
git apply "$SNODEC_BOOK_SOURCE/source-baseline/framework-working-tree.patch"
git rev-parse HEAD
python3 "$SNODEC_BOOK_SOURCE/ci/check-source-alignment.py" --framework "$PWD"
```

`git rev-parse HEAD` must print the base commit above; the checker must also
confirm every recorded working-tree file. Follow the build
requirements in Chapter 2; applications and dynamically loaded extensions must
be rebuilt against the 2.0 public headers and libraries.

## One checkout authority

`book-source-baseline.env` is the machine-readable authority. The companion
workflow reads its repository and ref, applies the captured patch, and the build
script verifies the source contents before building. `source-baseline-check` checks the book's declarations,
the 38-chapter evidence map, and marked companion listings; it is not a substitute for compiling the source.

The current local tree, including its uncommitted changes, was the authority for
this refinement. Its original location is recorded in the manifest for provenance;
verification does not require that location. The captured patch makes the same
contents reproducible without modifying or committing the author's framework tree.

A later commit with identical file contents does not change the verified source contents. Later file changes are different snapshots. Update this record, reader-facing
claims, printed listings, and verification evidence together rather than silently
testing a moving branch. Historical 1.x author verification remains recorded under
`review/verification/history/`; it does not certify this migrated source tree.
