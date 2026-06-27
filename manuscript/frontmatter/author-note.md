## Author and Framework Note {.unnumbered}

This is a first-party book. The author is the creator and maintainer of SNode.C and writes from inside the design of the framework.

That position has advantages and limits. The advantage is direct architectural knowledge: the book can explain why the framework separates runtime roles, connections, contexts, factories, protocol layers, configuration, diagnostics, and deployment concerns in the way it does. It can also connect public examples to implementation choices that are not obvious from an API reference alone.

The limit is that this book is not an independent review of SNode.C against every alternative C++ networking library. It does not try to rank frameworks or claim that one design is best for every project. It explains the design SNode.C uses, the kinds of systems that design supports, and the tradeoffs a reader should understand when adopting or extending it.

The book therefore asks to be judged on two levels: as a practical guide to SNode.C, and as a worked study of layered, event-driven network architecture in modern C++.
