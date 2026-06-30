add_custom_target(
  proposal-package
  DEPENDS pdf proposal proposal-sample-pdf
  COMMAND
    "${CMAKE_COMMAND}"
    -D "SOURCE_DIR=${SNODEC_BOOK_ROOT}"
    -D "BUILD_DIR=${BOOK_BUILD_DIR}"
    -D "PACKAGE_DIR=${DIST_PACKAGE_DIR}"
    -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/MakeProposalPackage.cmake"
  WORKING_DIRECTORY "${SNODEC_BOOK_ROOT}"
  COMMENT "Creating full publisher/reviewer book proposal package"
  VERBATIM)

# Convenience alias for generators/users that prefer underscores in target names.
add_custom_target(proposal_package DEPENDS proposal-package)
