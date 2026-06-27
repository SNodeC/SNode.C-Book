# Repository layout for the SNode.C book build.

get_filename_component(SNODEC_BOOK_ROOT "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)

set(MANUSCRIPT_DIR "${SNODEC_BOOK_ROOT}/manuscript")
set(PRODUCTION_DIR "${SNODEC_BOOK_ROOT}/production")
set(ASSETS_DIR "${SNODEC_BOOK_ROOT}/assets")
set(COMPANION_DIR "${SNODEC_BOOK_ROOT}/companion")
set(REVIEW_DIR "${SNODEC_BOOK_ROOT}/review")
set(BASELINE_DIR "${SNODEC_BOOK_ROOT}/source-baseline")
set(PACKAGING_DIR "${SNODEC_BOOK_ROOT}/packaging")
set(DIST_DIR "${SNODEC_BOOK_ROOT}/dist")
set(DIST_PDF_DIR "${DIST_DIR}/pdf")
set(DIST_PACKAGE_DIR "${DIST_DIR}/packages")

set(BOOK_BUILD_DIR
    "${CMAKE_BINARY_DIR}"
    CACHE PATH "Book build output directory")

# Backward-compatible alias for older local scripts that may still pass BUILD_DIR.
if(DEFINED BUILD_DIR AND NOT BUILD_DIR STREQUAL "")
  set(BOOK_BUILD_DIR "${BUILD_DIR}")
endif()

file(MAKE_DIRECTORY "${BOOK_BUILD_DIR}")
file(MAKE_DIRECTORY "${DIST_PDF_DIR}")
file(MAKE_DIRECTORY "${DIST_PACKAGE_DIR}")
