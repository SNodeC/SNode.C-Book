# Chapter 1 comparison evidence

Checked 2026-09-22. These are feature and ownership claims, not performance or
adoption measurements. The Chapter 1 comparison is 514 whitespace words, including
the table, below the 1,200-word limit (`phase-2-exit-checks.json`).

- SNode.C platform: read-only inspection of
  `/home/voc/projects/snodec/snode.c/README.md:599`–608 documents Linux development,
  Debian builds, x86-64/Arm, and OpenWrt. Chapter 1 states the supported path plainly
  and makes no native Windows/macOS promise. No platform build was executed here.
- One runtime loop per process: `src/core/EventLoop.cpp:125`–128 returns a static
  `EventLoop`; `src/core/SNodeC.cpp:61` delegates startup to it. The runtime API
  supplies this process loop, so blocking its callback delays other connections.
- Asio platform/header-only claim: [official build documentation](https://think-async.com/Asio/asio-1.30.2/doc/asio/using.html),
  sections Supported Platforms and Optional separate compilation. No third-party
  benchmark or unsupported compatibility claim is used.
- Asio execution ownership: [official io_context reference](https://think-async.com/Asio/asio-1.30.2/doc/asio/reference/io_context.html),
  sections Thread Safety, Synchronous and asynchronous operations, and Stopping.
  Application-owned contexts and threads calling `run()` contrast with the
  SNode.C process runtime. The new example intentionally uses one thread.
- Ecosystem wording: the [project's public organization](https://github.com/SNodeC)
  foregrounds MQTTSuite and framework-related applications. “Small ecosystem” and
  planning for source reading are qualitative editorial assessments of the
  available project material, not measured adoption, popularity, or market share.
  No repository counts, stars, deployment numbers, or endorsements are asserted.
- Ownership and buffering in the comparison: `Comparison-AsioEcho/main.cpp:14`
  gives each session its socket/buffer; shared handler captures keep it alive;
  `async_write` completion gates the next read. The printed EchoPair receive
  callback and factory supply the other side of the table. All new comparison
  code is original companion code; no external tutorial listing was copied.
- Execution: `phase-2-asio-standalone.log` builds Asio without SNode.C; the normal
  companion build registers it alongside EchoPair. `phase-2-labs.log`, exercise-ch01,
  records byte equality for both implementations. This establishes the exercised
  byte-reflection behavior, not latency, throughput, security, or deployment fitness.
