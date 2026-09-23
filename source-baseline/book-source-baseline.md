# Book Source Baseline

Current source: SNode.C 2.0.0, public commit
`07ca9a2936ee72582df7d159cb06666fe23e30f8`. Readers check out this commit without a patch.

`book-source-baseline.env` is the machine-readable authority; `SOURCE-VERSION.md`
documents the checkout. The manifest records the 1,448 file contents of the clean
author tree. The retained patch file is empty and its digest is still verified.
This pin identifies a source snapshot, not a newly created release tag.

The re-baseline includes asynchronous logging and semantic rendering on its
worker, along with the compiler's `-fno-gnu-unique` policy. Claim review and new
build/runtime evidence are recorded in `review/pedagogical-smoothing-2026-09-23/`.
Earlier verification remains historical and is not relabeled as evidence for
this source.
