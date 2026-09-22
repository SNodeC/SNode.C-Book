# The SNode.C Architecture

The first part made SNode.C observable through a working echo program. This part turns those observations into the framework's core model.

The chapters that follow separate two questions: what keeps an operation alive, and what advances it? The answers distinguish endpoint configuration, activation flows, connections, contexts, and the shared event runtime. Layer choices then show which of those responsibilities changes when a carrier or connection variant changes. Part III applies that distinction to concrete endpoint families.

The Part II checkpoint in Chapter 5 gives accepted measurements one owner: two inputs share an order, and removing one observer leaves the other active. A separate queued-work lab makes callback deferral observable before later Parts combine model and transport.
