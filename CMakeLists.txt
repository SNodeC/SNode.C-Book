cmake_minimum_required(VERSION 3.20)

project(SNodeCBook NONE)

option(SNODEC_BOOK_BUILD_PDFS
       "Configure book/proposal PDF and publisher-package targets" ON)

option(SNODEC_BOOK_BUILD_COMPANION_EXAMPLES
       "Configure companion C++ examples; requires an installed SNode.C CMake package"
       OFF)

if(SNODEC_BOOK_BUILD_PDFS)
  include("${CMAKE_CURRENT_SOURCE_DIR}/production/cmake/SNodeCBookPaths.cmake")
  include("${CMAKE_CURRENT_SOURCE_DIR}/production/cmake/SNodeCBookTools.cmake")
  include("${CMAKE_CURRENT_SOURCE_DIR}/production/cmake/SNodeCPandocBook.cmake")

  add_subdirectory(production)
  add_subdirectory(assets)
  add_subdirectory(manuscript)
  add_subdirectory(review)
  add_subdirectory(packaging)
  add_subdirectory(source-baseline)

  add_custom_target(all-books DEPENDS pdf tex proposal proposal-sample-pdf)

  add_custom_target(
    book-clean
    COMMAND "${CMAKE_COMMAND}" -E rm -rf "${BOOK_BUILD_DIR}"
    VERBATIM)
endif()

if(SNODEC_BOOK_BUILD_COMPANION_EXAMPLES)
  enable_language(CXX)
  add_subdirectory(companion)
endif()

if(NOT SNODEC_BOOK_BUILD_PDFS AND NOT SNODEC_BOOK_BUILD_COMPANION_EXAMPLES)
  message(WARNING
    "Both SNODEC_BOOK_BUILD_PDFS and SNODEC_BOOK_BUILD_COMPANION_EXAMPLES are OFF; no main targets will be configured.")
endif()
