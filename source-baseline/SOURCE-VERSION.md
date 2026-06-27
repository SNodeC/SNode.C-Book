# Target SNode.C Source Version

This manuscript targets one explicit, public SNode.C source baseline.

- Repository: `https://github.com/SNodeC/snode.c.git`
- Repository identifier: `SNodeC/snode.c`
- Source line: `master`
- Book release tag: `v1.0.2`
- Authoritative commit: `6e475262084ae2dab2daef8781ab9e4adb82d18e`
- Baseline recorded on: `2026-06-26`

The release tag is the human-facing checkout name used by readers and by verification scripts. The full commit SHA is the authoritative source pin. If the tag and the commit ever disagree, the commit SHA in this file wins for manuscript verification until this file is deliberately updated.

The manuscript, examples, component names, public include paths, and package descriptions should be read against this exact source baseline. Later repository changes may introduce, rename, or remove components, headers, examples, package components, or implementation details.

## Reader checkout

A reader who wants to build the framework version used by the book should check out the recorded release tag:

```sh
git clone https://github.com/SNodeC/snode.c.git
cd snode.c
git checkout v1.0.2
```

For verification work, also confirm the commit:

```sh
git rev-parse HEAD
```

The expected result is:

```text
6e475262084ae2dab2daef8781ab9e4adb82d18e
```

## Version-drift policy

This book does not describe arbitrary future states of the SNode.C repository. The public `master` branch may continue to move after publication. The examples and listings in this package are aligned with the baseline above. Newer SNode.C versions should be treated as newer software and checked against the book examples before the manuscript is updated.
