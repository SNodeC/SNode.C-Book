# Follow-up 14 — companion CI record

The GitHub connector returned the hosted job logs that gh could not download
in Follow-up 13. CMake compiler-identification lines establish the versions.

| Run / book commit | GCC 13.3.0 | Clang 18.1.3 |
|---|---|---|
| 36002150169 / f19a658 | framework 185/185, external echo 4/4, labs 65/66; job failure | framework 185/185, external echo 4/4, labs 66/66; job success |
| 36002653903 / d4ff44d | framework 185/185, external echo 4/4, labs 66/66; job success | framework 185/185, external echo 4/4, labs 66/66; job success |

The first GCC failure is exercise-ch07-ip-families: asynchronous diagnostic
text interleaves with the IDENTITY line, causing int(port_text) to raise
ValueError. It is not a loader failure or a framework compile failure. The
unchanged companion code passed the subsequent run. This historical failure
is retained as an observation, not silently treated as fixed by a later pass.
No assertion, timeout, parser, diagnostic setting or test logic is changed.

The shared Linux inherited-RPATH policy from f19a658 resolves the reported
loader problem in both hosted compiler jobs. Hosted Clang 18.1.3 compiles the
frozen framework, so the conditional instruction to pin a failing hosted
compiler does not apply. No workflow or companion build change is needed.
Local Clang 21.1.8 remains a framework compatibility follow-up outside this
branch: ConfigActions.cpp:296, -Werror,-Wnrvo.

Local reproduction uses an isolated Ubuntu 24.04 root filesystem under the
book build directory, installed with the workflow's development dependencies,
GCC and distribution Clang. Both compilers receive separate workspaces, homes,
build trees and installation prefixes. The fresh public clone is mounted
read-only; the author's tree is not mounted. The workflow build script, bare
CTest command, and smoke/lifetime commands run without test changes or caller
LD_LIBRARY_PATH. Full local results and the new pushed hosted run will be
recorded in FOLLOWUP-14-REPORT.md after completion; they are pending at this
item commit. Prior success is not substituted for those required runs.
