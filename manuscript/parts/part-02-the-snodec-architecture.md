# The SNode.C Architecture

The first part made SNode.C observable through a working program and a readable source tree. This part turns those observations into the framework's core model.

The chapters that follow separate two questions: what keeps an operation alive, and what advances it? The answers distinguish endpoint configuration, activation flows, connections, contexts, and the shared event runtime. Layer choices then show which of those responsibilities changes when a carrier or connection variant changes. Part III applies that distinction to concrete endpoint families.
