# MiniGateway Verification: Current and Historical Scope

The complete sources for Chapters 35 and 36 are `companion/examples/MiniGateway`
and `companion/examples/MiniGateway-Extended`. Their marked printed listings are
checked against those files. The current framework pin is recorded in
`source-baseline/SOURCE-VERSION.md`.

The author's earlier local build/run confirmation, including MQTT input/output,
is retained unchanged in `history/minigateway-step8-author-verification.md`. It
is a genuine historical author confirmation, not a claim that the migrated
2.0.0 source has been independently retested on the author's machine.

Current automated behavior checks exercise MiniGateway Extended's health route,
Unix-domain measurement input, resulting HTTP state, and SSE observation. They
configure the MQTT endpoint but do not launch a broker. Therefore, even a passing
current CI run does not newly verify MQTT broker exchange, database behavior,
OpenWrt deployment, long-running service operation, or overload policy.

See `examples-aggregate-build-verification.md` and the exact GitHub Actions run
for current build and selected runtime evidence. Broader author/reviewer checks
can be added with their real environment, book commit, source pin, and results.
