# Target SNode.C Source Version

This edition targets SNode.C project version **2.0.0** at public commit
`8b8da56e0349191d4658ca8f820a490539eccd4d`. The version is the CMake project version,
not a claim that a matching release tag exists.

- Repository: `SNodeC/snode.c`
- Source authority: the pinned public commit, checked against the clean author tree
- Exact tree digest: `f00e7f9c16854d70c3d2122272458c581bacd108882ed13004c7d6d2173348ee`
- Exact file contents: `framework-working-tree.json` (1,447 files)
- Baseline recorded: `2026-09-23`
- `framework-working-tree.patch` is empty; its digest remains checked.

## Reader checkout

Set `SNODEC_BOOK_SOURCE` to the absolute directory containing the book source
package. Check out the public commit; no patch is needed.

```sh
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout --detach 8b8da56e0349191d4658ca8f820a490539eccd4d
git rev-parse HEAD
python3 "$SNODEC_BOOK_SOURCE/ci/check-source-alignment.py" --framework "$PWD"
```

`git rev-parse HEAD` must print the pin above. The checker verifies the recorded
file contents. Follow Chapter 2 for build requirements; rebuild applications and
dynamically loaded extensions against the 2.0 public headers and libraries.

## One checkout authority

`book-source-baseline.env` is the machine-readable authority. The companion
workflow reads its repository and ref and verifies source contents before building.
`source-baseline-check` checks the declarations, chapter evidence and marked
companion listings; compilation and runtime tests provide separate evidence.

The manifest records the original author-tree location for provenance, but
verification does not require that location. Update declarations, reader claims
and verification evidence together when changing the pin. Historical review
records retain their original source identities.
