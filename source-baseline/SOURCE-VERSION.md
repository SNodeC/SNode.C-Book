# Target SNode.C Source Version

This edition describes SNode.C project version **2.0.0**. Use `SNodeC/snode.c`
`master` HEAD, then compare its content with the edition manifest. The version
is the CMake project version, not a checkout tag.

- Repository: `SNodeC/snode.c`, default branch `master`
- Edition content: `framework-working-tree.json` (1,448 files)
- Baseline recorded: `2026-09-23`
- Observed commit provenance exists only in the content manifest.
- `framework-working-tree.patch` is empty; its digest remains checked.

## Reader checkout

Set `SNODEC_BOOK_SOURCE` to the absolute directory containing the book source
package. Clone default-branch HEAD; no patch is needed.

```sh
git clone --branch master https://github.com/SNodeC/snode.c.git
cd snode.c
git rev-parse HEAD
python3 "$SNODEC_BOOK_SOURCE/ci/check-source-alignment.py" --framework "$PWD"
```

The printed HEAD is evidence of what you inspected, not a checkout target.
The checker compares file contents and source anchors with the edition manifest.
If it reports “master has drifted from the edition manifest”, the named files
have changed, appeared or disappeared. Update the book from its `main` HEAD and
repeat the check against a fresh framework `master` clone. If drift remains,
report the named files to the book maintainers and pause the affected examples
until claims, manifest and tests have been reviewed together. Do not bypass the
check or select an older commit to conceal drift.

Follow Chapter 2 for build requirements. Keep source, build and install locations
separate; rebuild applications and dynamically loaded extensions against the
verified public headers and libraries.

## One checkout authority

`book-source-baseline.env` declares the repository, default branch and manifest.
The companion workflow checks out that branch, logs the observed HEAD and verifies
contents before building. `source-baseline-check` checks declarations, chapter
evidence and complete companion listings; `--framework` also checks the supplied
clone's source contents and anchors. Compilation and runtime tests are separate.

The manifest preserves earlier provenance; it does not direct a checkout.
Historical review records retain their original observations. MQTTSuite uses
`SNodeC/mqttsuite` master and the feed uses `SNodeC/OpenWRT` main; the external
anchor checker verifies their named source paths and symbols separately.
