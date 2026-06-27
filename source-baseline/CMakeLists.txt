add_custom_target(
  source-baseline-check
  COMMAND "${CMAKE_COMMAND}" -E echo
          "SNode.C source baseline is recorded in ${BASELINE_DIR}/SOURCE-VERSION.md"
  VERBATIM)
