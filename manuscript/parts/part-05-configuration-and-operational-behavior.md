# Configuration and Operational Behavior

Part IV separated protocol behavior from carrier selection. This part shows where many of those choices become visible in a real executable.

Configuration is treated as architecture, not as decoration: application-side handles, named roles, registered instances, generated command lines, logging, diagnostics, and runtime introspection all make operational behavior observable. With that surface established, Part VI can discuss secure and robust communication without hiding policy inside arbitrary callbacks.
