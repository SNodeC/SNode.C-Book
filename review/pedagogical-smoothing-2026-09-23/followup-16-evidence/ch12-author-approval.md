# Author approval during Follow-up 16

Question: Approve this Ch12 CMake correction: replace `"8090,"` with `"\"/tmp/line-transfer.sock\","` without matching leading spaces? This keeps the generated lab’s behavior unchanged and fixes the build after formatting. Approval is needed because FOLLOWUP-16 §0 forbids changing strings; no assertion, timeout or C++ behavior would change.

Author answer: **Approve the Ch12 generator correction**.

The exact reviewed diff is preserved in ch12-author-approved.patch. The generated
C++ equivalence check is recorded in ch12-generator-verification.json.
