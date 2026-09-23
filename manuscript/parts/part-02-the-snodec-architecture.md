# The SNode.C Architecture

The first part made SNode.C observable through a working echo program. This part turns those observations into the framework's core model.

The runtime mental model, layers in practice, and event processing now each have a chapter. They separate what keeps an operation alive, what can vary beneath a protocol, and what advances the work. The answers distinguish endpoint configuration, activation flows, connections, contexts, and the shared event runtime. Layer choices then show which of those responsibilities changes when a network family or connection variant changes. Part III applies that distinction to concrete endpoint families.

The Part II checkpoint in Chapter 6 gives accepted measurements one owner: two inputs share an order, and removing one observer leaves the other active. A separate queued-work lab makes callback deferral observable before later Parts combine model and transport.
