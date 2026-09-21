find_package(Python3 3.9 REQUIRED COMPONENTS Interpreter)

add_custom_target(
  source-baseline-check
  COMMAND "${Python3_EXECUTABLE}" "${SNODEC_BOOK_ROOT}/ci/check-source-alignment.py"
  WORKING_DIRECTORY "${SNODEC_BOOK_ROOT}"
  COMMENT "Checking the source snapshot and marked complete companion listings"
  VERBATIM)
