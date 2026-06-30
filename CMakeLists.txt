cmake_minimum_required(VERSION 3.20)

project(SNodeCBook NONE)

include("${CMAKE_CURRENT_SOURCE_DIR}/production/cmake/SNodeCBookPaths.cmake")
include("${CMAKE_CURRENT_SOURCE_DIR}/production/cmake/SNodeCBookTools.cmake")
include("${CMAKE_CURRENT_SOURCE_DIR}/production/cmake/SNodeCPandocBook.cmake")

option(SNODEC_BOOK_BUILD_COMPANION_EXAMPLES
       "Configure companion C++ examples as part of the book build" OFF)

add_subdirectory(production)
add_subdirectory(assets)
add_subdirectory(manuscript)
add_subdirectory(review)
add_subdirectory(packaging)
add_subdirectory(source-baseline)

if(SNODEC_BOOK_BUILD_COMPANION_EXAMPLES)
  add_subdirectory(companion)
endif()

add_custom_target(all-books DEPENDS pdf tex proposal proposal-sample-pdf)

add_custom_target(
  book-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${BOOK_BUILD_DIR}"
  VERBATIM)
