# Secure and Robust Communication

This part adds secure connection handling and communication-over-time behavior to the same layered model. TLS, timeout policy, retry, reconnect, shutdown, termination, and failure visibility are treated as architectural concerns, not as scattered implementation details.

The reader should keep one principle in mind: robustness belongs to the boundary that owns the behavior.
