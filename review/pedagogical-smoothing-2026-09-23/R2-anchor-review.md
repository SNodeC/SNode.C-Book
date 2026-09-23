# R2 anchor review

Verified every framework source anchor against clean 07ca9a29. Exactly three
anchors in pre-split chapter 5 changed: EventLoop.cpp tick 224→244, reconfigure
323→343, and dispatch condition 215→224 with the prescribed pending-signal
condition. All other paths, lines and needles match and remain unchanged.
No anchor dropped; reviewed_tree_sha256 awaits the R2 build/runtime gate.
