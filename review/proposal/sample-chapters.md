```{=latex}
\clearpage
```

# Selected sample chapters

Read these samples in the order below. Chapter numbers refer to the complete manuscript; the sample PDF's section numbers are only navigation within this combined document. Chapters between the samples supply prerequisites, so the five selections demonstrate stages of the learning path rather than a replacement course.

| Current chapter | What it demonstrates | What the reader can check |
|---|---|---|
| 1. Why SNode.C Exists | A connected case for layered programming, a fair Asio comparison with paired source excerpts, and explicit framework costs | Trace buffer ownership before building; the two echo labs follow Chapter 2's environment setup |
| 3. Your First Working Program: The Echo Pair | Complete first-program listings and the minimum handle/factory/context vocabulary | Change a greeting, preserve binary reflection, and distinguish an occupied endpoint from protocol failure |
| 19. Server-Sent Events and Real-Time HTTP | A long-lived response, subscriber ownership, and the distinction between reconnect and replay | Compare accepted state with events and observe independent stream lifetimes |
| 30. Building MiniGateway | Source assembly around one shared model, with complete listings and HTTP/SSE/MQTT roles | Observe local state without a broker and reject invalid measurements before acceptance |
| 32. Architectural Judgment: Choosing the Right Layer and Boundary | Decision tables applied to ownership, lifetime, and operational requirements | Compare shared and separate model instances; run the integrated HTTP/Unix/SSE checkpoint, then justify a privileged collector's process boundary |

Each sample opens with three observable objectives and closes with a recap and five mapped exercises: two review questions, two labs, and one design problem. Public conceptual answers, lab commands with expected outcomes, and design discussions accompany the source under `companion/exercises/`. Try the exercises before consulting their solutions. The four newly split chapters follow the same teaching pattern. The epilogue is a closing essay.

```{=latex}
\AddToHook{cmd/subsection/before}{\clearpage}
\AddToHook{cmd/subsubsection/before}{\Needspace{6\baselineskip}}
\tcbset{snodecboxbase/.append style={unbreakable}}
```
