# Target SNode.C Source Version

This edition targets SNode.C project version **2.0.0** at public commit
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. The version is the CMake project version,
not a claim that a matching release tag exists.

- Repository: `SNodeC/snode.c`
- Source authority: the pinned public commit, checked against the clean author tree
- Exact tree digest: `2face99fc58fb1ec5374c35d88e6fcd9c7a7d56b52ea44cb00e49eb4825b9a2b`
- Exact file contents: `framework-working-tree.json` (1,448 files)
- Baseline recorded: `2026-09-23`
- `framework-working-tree.patch` is empty; its digest remains checked.

## Reader checkout

Set `SNODEC_BOOK_SOURCE` to the absolute directory containing the book source
package. Check out the public commit; no patch is needed.

```sh
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout --detach 07ca9a2936ee72582df7d159cb06666fe23e30f8
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
