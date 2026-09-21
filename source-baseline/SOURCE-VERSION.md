# Target SNode.C Source Version

This edition targets the SNode.C **2.0.0 source snapshot** below. The version is
the CMake project version of that snapshot; it is not a claim that a `v2.0.0`
release tag exists.

- Repository: `SNodeC/snode.c`
- Source line observed: `master`
- Project version: `2.0.0`
- Authoritative commit: `1f0f728fc9b3b45174f2cd790d83b2f493e58af1`
- Baseline recorded: `2026-09-21`

## Reader checkout

```sh
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout --detach 1f0f728fc9b3b45174f2cd790d83b2f493e58af1
git rev-parse HEAD
```

The final command must print the authoritative commit above. Follow the build
requirements in Chapter 2; applications and dynamically loaded extensions must
be rebuilt against the 2.0 public headers and libraries.

## One checkout authority

`book-source-baseline.env` is the machine-readable authority. The companion
workflow reads its repository and ref, and the build script verifies the checked
out commit before building. `source-baseline-check` checks the book's declarations
and marked companion listings; it is not a substitute for compiling the source.

Later `master` commits are different snapshots. Update this pin, reader-facing
claims, printed listings, and verification evidence together rather than silently
testing a moving branch. Historical 1.x author verification remains recorded under
`review/verification/history/`; it does not certify this migrated source tree.
