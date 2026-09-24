#!/usr/bin/env bash
set -euo pipefail
ROOT=$(pwd)
compiler=$1
if [[ "$compiler" == gcc ]]; then cxx=g++; else cxx=clang++; fi
exec bwrap --unshare-user --uid 1000 --gid 1000 \
 --ro-bind "$ROOT/build/followup-14/ubuntu-root" / \
 --bind "$ROOT/build/followup-14/$compiler-workspace" /workspace \
 --bind "$ROOT/build/followup-14/$compiler-workspace/home" /home/runner \
 --ro-bind "$ROOT/build/followup-14-public-07ca9a29" /workspace/external/snode.c \
 --ro-bind "$ROOT/build/followup-14/run-local.sh" /run-local.sh \
 --dev /dev --proc /proc --tmpfs /tmp --chdir /workspace \
 --setenv HOME /home/runner --setenv USER runner --setenv LOGNAME runner \
 --setenv PATH /usr/bin:/bin --unsetenv LD_LIBRARY_PATH \
 --setenv CC "$compiler" --setenv CXX "$cxx" /bin/bash /run-local.sh
