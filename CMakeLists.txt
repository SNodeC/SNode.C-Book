cmake_minimum_required(VERSION 3.20)

project(snodec-book NONE)

set(PANDOC
    pandoc
    CACHE STRING "Pandoc executable")
set(PDF_ENGINE
    xelatex
    CACHE STRING "Pandoc PDF engine")
set(BUILD_DIR
    "${CMAKE_CURRENT_SOURCE_DIR}/build"
    CACHE PATH "Output directory")

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/book-files.txt" BOOK_FILES)
file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/book-files-existing-only.txt"
     EXISTING_FILES)

set(PANDOC_FROM "markdown+raw_tex+fenced_code_attributes")
set(PANDOC_CROSSREF_FILTER
    pandoc-crossref
    CACHE STRING "Pandoc cross-reference filter executable")

set(PANDOC_LISTINGS_FILTER
    "${CMAKE_CURRENT_SOURCE_DIR}/filters/snodec-listings.lua"
    CACHE STRING "Pandoc Lua filter for book-specific listings styles")

# Reconfigure automatically when one of the manuscript file lists changes.
# The Pandoc input list is read at configure time and baked into the build rules.
set_property(
  DIRECTORY
  APPEND
  PROPERTY CMAKE_CONFIGURE_DEPENDS
    "${CMAKE_CURRENT_SOURCE_DIR}/book-files.txt"
    "${CMAKE_CURRENT_SOURCE_DIR}/book-files-existing-only.txt")

# -----------------------------------------------------------------------------
# TikZ figure build
# -----------------------------------------------------------------------------
# Figure source files live in figures/src and are named fig-*.tex.
# They are compiled to PDF files in figures/pdf so Pandoc can include them from
# Markdown as ordinary image files.
set(FIGURE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/figures/src")
set(FIGURE_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/figures/pdf")
set(FIGURE_BUILD_ROOT "${BUILD_DIR}/figures")

file(GLOB FIGURE_SOURCES CONFIGURE_DEPENDS "${FIGURE_SOURCE_DIR}/fig-*.tex")
file(GLOB FIGURE_SUPPORT_FILES CONFIGURE_DEPENDS "${FIGURE_SOURCE_DIR}/*.tex")
if(FIGURE_SUPPORT_FILES AND FIGURE_SOURCES)
  list(REMOVE_ITEM FIGURE_SUPPORT_FILES ${FIGURE_SOURCES})
endif()

set(FIGURE_PDFS)
if(FIGURE_SOURCES)
  find_program(XELATEX_EXECUTABLE xelatex)
  if(NOT XELATEX_EXECUTABLE)
    message(FATAL_ERROR
      "xelatex was not found. It is required to build TikZ figures.")
  endif()

  foreach(FIGURE_SOURCE IN LISTS FIGURE_SOURCES)
    get_filename_component(FIGURE_NAME "${FIGURE_SOURCE}" NAME_WE)
    set(FIGURE_BUILD_DIR "${FIGURE_BUILD_ROOT}/${FIGURE_NAME}")
    set(FIGURE_PDF "${FIGURE_OUTPUT_DIR}/${FIGURE_NAME}.pdf")

    add_custom_command(
      OUTPUT "${FIGURE_PDF}"
      COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_BUILD_DIR}"
      COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_OUTPUT_DIR}"
      COMMAND
        "${XELATEX_EXECUTABLE}" -interaction=nonstopmode -halt-on-error
        -output-directory "${FIGURE_BUILD_DIR}" "${FIGURE_SOURCE}"
      COMMAND
        "${CMAKE_COMMAND}" -E copy_if_different
        "${FIGURE_BUILD_DIR}/${FIGURE_NAME}.pdf" "${FIGURE_PDF}"
      DEPENDS "${FIGURE_SOURCE}" ${FIGURE_SUPPORT_FILES}
      WORKING_DIRECTORY "${FIGURE_SOURCE_DIR}"
      COMMENT "Building TikZ figure ${FIGURE_NAME}"
      VERBATIM)

    list(APPEND FIGURE_PDFS "${FIGURE_PDF}")
  endforeach()

  add_custom_target(figures DEPENDS ${FIGURE_PDFS})
else()
  add_custom_target(
    figures
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_OUTPUT_DIR}"
    COMMENT "No TikZ figure sources found"
    VERBATIM)
endif()

add_custom_target(
  figures-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${FIGURE_BUILD_ROOT}"
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${FIGURE_OUTPUT_DIR}"
  VERBATIM)

function(make_pandoc_target target_name output_file)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BUILD_DIR}"
    COMMAND
      "${PANDOC}" ${ARGN} --lua-filter "${PANDOC_LISTINGS_FILTER}" --filter "${PANDOC_CROSSREF_FILTER}" --syntax-highlighting=idiomatic --from
      "${PANDOC_FROM}" --top-level-division=part -o
      "${BUILD_DIR}/${output_file}.tex"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    VERBATIM)
endfunction()

function(make_pandoc_pdf_target target_name output_file)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BUILD_DIR}"
    COMMAND "cp" "-fa" "${BUILD_DIR}/${output_file}.pdf"
            "${BUILD_DIR}/${output_file}-old.pdf" || echo ""
    COMMAND
      "${PANDOC}" ${ARGN} --lua-filter "${PANDOC_LISTINGS_FILTER}" --filter "${PANDOC_CROSSREF_FILTER}" --syntax-highlighting=idiomatic --from
      "${PANDOC_FROM}" --to pdf --top-level-division=part --pdf-engine
      "${PDF_ENGINE}" -o "${BUILD_DIR}/${output_file}-temp.pdf"
    COMMAND "rm" "-f" "${BUILD_DIR}/${output_file}.pdf" || echo ""
    COMMAND "mv" "${BUILD_DIR}/${output_file}-temp.pdf"
            "${BUILD_DIR}/${output_file}.pdf" || echo ""
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    VERBATIM)
endfunction()

make_pandoc_pdf_target(pdf "snodec-book" --metadata-file metadata.yaml
                       ${BOOK_FILES})

make_pandoc_pdf_target(pdf-existing "snodec-book-existing-only" --metadata-file
                       metadata.yaml ${EXISTING_FILES})

make_pandoc_target(tex "snodec-book" --metadata-file metadata.yaml
                   ${BOOK_FILES})

make_pandoc_target(tex-existing "snodec-book-existing-only" --metadata-file
                   metadata.yaml ${EXISTING_FILES})

make_pandoc_pdf_target(proposal "book-proposal-package" --metadata-file
                       metadata.yaml proposal/book-proposal-package.md)

# Main manuscript PDF targets require generated figure PDFs because the
# Markdown sources include figures/pdf/fig-*.pdf.
add_dependencies(pdf figures)
add_dependencies(pdf-existing figures)

add_custom_target(book ALL DEPENDS pdf)

add_custom_target(all-books DEPENDS pdf pdf-existing tex tex-existing proposal)


# -----------------------------------------------------------------------------
# Publisher/proposal package
# -----------------------------------------------------------------------------
# Create a clean proposal package containing only the files needed to review the
# book proposal.  The package is written to ./packages and named with a date/time
# stamp plus an incrementing two-digit version number, for example:
#
#   snodec-book-proposal-package-20260616-214530-v03.tar.gz
#
# The version number is computed at build time by scanning existing proposal
# packages in ./packages and taking the next free number.
set(PROPOSAL_PACKAGE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/packages")
set(PROPOSAL_PACKAGE_SCRIPT
    "${CMAKE_CURRENT_BINARY_DIR}/make-proposal-package.cmake")

file(WRITE "${PROPOSAL_PACKAGE_SCRIPT}" [==[
if(NOT DEFINED SOURCE_DIR)
  message(FATAL_ERROR "SOURCE_DIR is not set")
endif()

if(NOT DEFINED BUILD_DIR)
  message(FATAL_ERROR "BUILD_DIR is not set")
endif()

if(NOT DEFINED PACKAGE_DIR)
  message(FATAL_ERROR "PACKAGE_DIR is not set")
endif()

file(MAKE_DIRECTORY "${PACKAGE_DIR}")

file(GLOB EXISTING_PACKAGES
     "${PACKAGE_DIR}/snodec-book-proposal-package-*-v[0-9][0-9].tar.gz")

set(NEXT_VERSION 1)
foreach(PACKAGE_FILE IN LISTS EXISTING_PACKAGES)
  get_filename_component(PACKAGE_NAME "${PACKAGE_FILE}" NAME)
  if(PACKAGE_NAME MATCHES "-v([0-9][0-9])\\.tar\\.gz$")
    set(CURRENT_VERSION "${CMAKE_MATCH_1}")
    math(EXPR CANDIDATE_VERSION "${CURRENT_VERSION} + 1")
    if(CANDIDATE_VERSION GREATER NEXT_VERSION)
      set(NEXT_VERSION "${CANDIDATE_VERSION}")
    endif()
  endif()
endforeach()

if(NEXT_VERSION GREATER 99)
  message(FATAL_ERROR "Proposal package version would exceed v99")
endif()

string(TIMESTAMP PACKAGE_TIMESTAMP "%Y%m%d-%H%M%S")
if(NEXT_VERSION LESS 10)
  set(PACKAGE_VERSION "0${NEXT_VERSION}")
else()
  set(PACKAGE_VERSION "${NEXT_VERSION}")
endif()

set(PACKAGE_BASENAME
    "snodec-book-proposal-package-${PACKAGE_TIMESTAMP}-v${PACKAGE_VERSION}")
set(PACKAGE_PATH "${PACKAGE_DIR}/${PACKAGE_BASENAME}.tar.gz")

set(STAGING_DIR "${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_BASENAME}")
file(REMOVE_RECURSE "${STAGING_DIR}")
file(MAKE_DIRECTORY "${STAGING_DIR}")
file(MAKE_DIRECTORY "${STAGING_DIR}/proposal")

set(REQUIRED_PROPOSAL_FILES
    "proposal/book-proposal-package.md"
    "metadata.yaml")

foreach(REQUIRED_FILE IN LISTS REQUIRED_PROPOSAL_FILES)
  if(NOT EXISTS "${SOURCE_DIR}/${REQUIRED_FILE}")
    message(FATAL_ERROR "Required proposal package file missing: ${REQUIRED_FILE}")
  endif()
endforeach()

file(COPY "${SOURCE_DIR}/proposal/book-proposal-package.md"
     DESTINATION "${STAGING_DIR}/proposal")
file(COPY "${SOURCE_DIR}/metadata.yaml" DESTINATION "${STAGING_DIR}")

foreach(OPTIONAL_FILE IN ITEMS README.md STRUCTURE.md)
  if(EXISTS "${SOURCE_DIR}/${OPTIONAL_FILE}")
    file(COPY "${SOURCE_DIR}/${OPTIONAL_FILE}" DESTINATION "${STAGING_DIR}")
  endif()
endforeach()

if(EXISTS "${BUILD_DIR}/book-proposal-package.pdf")
  file(COPY "${BUILD_DIR}/book-proposal-package.pdf" DESTINATION "${STAGING_DIR}")
endif()

file(WRITE "${STAGING_DIR}/PACKAGE-CONTENTS.txt"
"SNode.C book proposal package\n\nThis archive contains only the publisher/reviewer-facing proposal files.\n\nIncluded when present:\n- proposal/book-proposal-package.md\n- book-proposal-package.pdf\n- metadata.yaml\n- README.md\n- STRUCTURE.md\n\nGenerated package: ${PACKAGE_BASENAME}.tar.gz\n")

execute_process(
  COMMAND "${CMAKE_COMMAND}" -E tar czf "${PACKAGE_PATH}" --format=gnutar .
  WORKING_DIRECTORY "${STAGING_DIR}"
  RESULT_VARIABLE TAR_RESULT)

if(NOT TAR_RESULT EQUAL 0)
  message(FATAL_ERROR "Failed to create proposal package: ${PACKAGE_PATH}")
endif()

file(REMOVE_RECURSE "${STAGING_DIR}")
message(STATUS "Created proposal package: ${PACKAGE_PATH}")
]==])

add_custom_target(
  proposal-package
  DEPENDS proposal
  COMMAND
    "${CMAKE_COMMAND}" -D "SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}" -D
    "BUILD_DIR=${BUILD_DIR}" -D "PACKAGE_DIR=${PROPOSAL_PACKAGE_DIR}" -P
    "${PROPOSAL_PACKAGE_SCRIPT}"
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  COMMENT "Creating publisher/reviewer proposal package"
  VERBATIM)

# Convenience alias for generators/users that prefer underscores in target names.
add_custom_target(proposal_package DEPENDS proposal-package)

add_custom_target(
  book-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${BUILD_DIR}"
  VERBATIM)
