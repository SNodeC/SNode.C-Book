cmake_minimum_required(VERSION 3.20)

project(snodec-book NONE)

set(PANDOC
    pandoc
    CACHE STRING "Pandoc executable")
set(PDF_ENGINE
    xelatex
    CACHE STRING "Pandoc PDF engine")
set(MAKEINDEX
    makeindex
    CACHE STRING "MakeIndex executable")
set(BUILD_DIR
    "${CMAKE_CURRENT_SOURCE_DIR}/build"
    CACHE PATH "Output directory")

file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/book-files.txt" BOOK_FILES)

set(PANDOC_FROM "markdown+raw_tex+fenced_code_attributes")
set(PANDOC_CROSSREF_FILTER
    pandoc-crossref
    CACHE STRING "Pandoc cross-reference filter executable")

set(PANDOC_CALLOUT_FILTER
    "${CMAKE_CURRENT_SOURCE_DIR}/filters/snodec-callouts.lua"
    CACHE STRING "Pandoc Lua filter for SNode.C semantic callouts")

set(PANDOC_LISTINGS_FILTER
    "${CMAKE_CURRENT_SOURCE_DIR}/filters/snodec-listings.lua"
    CACHE STRING "Pandoc Lua filter for book-specific listings styles")

# Reconfigure automatically when one of the manuscript file lists changes. The
# Pandoc input list is read at configure time and baked into the build rules.
set_property(
  DIRECTORY
  APPEND
  PROPERTY CMAKE_CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/book-files.txt")

# -----------------------------------------------------------------------------
# Figure build
# -----------------------------------------------------------------------------
# Figure-specific build rules live in figures/CMakeLists.txt.  The subdirectory
# creates the `figures`, `figures-contact-sheet`, and `figures-clean` targets.
add_subdirectory(figures)

function(make_pandoc_target target_name output_file)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BUILD_DIR}"
    COMMAND
      "${PANDOC}" ${ARGN} --lua-filter "${PANDOC_LISTINGS_FILTER}" --lua-filter
      "${PANDOC_CALLOUT_FILTER}" --filter "${PANDOC_CROSSREF_FILTER}"
      --syntax-highlighting=idiomatic --from "${PANDOC_FROM}"
      --top-level-division=part --standalone -o "${BUILD_DIR}/${output_file}.tex"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    VERBATIM)
endfunction()

function(make_pandoc_pdf_target target_name output_file)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BUILD_DIR}"
    COMMAND
      "${PANDOC}" ${ARGN} --lua-filter "${PANDOC_LISTINGS_FILTER}" --lua-filter
      "${PANDOC_CALLOUT_FILTER}" --filter "${PANDOC_CROSSREF_FILTER}"
      --syntax-highlighting=idiomatic --from "${PANDOC_FROM}"
      --top-level-division=part --standalone -o "${BUILD_DIR}/${output_file}.tex"
    COMMAND "${CMAKE_COMMAND}" -E rm -f "${BUILD_DIR}/${output_file}.idx"
            "${BUILD_DIR}/${output_file}.ind" "${BUILD_DIR}/${output_file}.ilg"
    COMMAND "${PDF_ENGINE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${BUILD_DIR}" "${BUILD_DIR}/${output_file}.tex"
    COMMAND "${CMAKE_COMMAND}" -E chdir "${BUILD_DIR}" "${MAKEINDEX}"
            "${output_file}.idx"
    COMMAND "${PDF_ENGINE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${BUILD_DIR}" "${BUILD_DIR}/${output_file}.tex"
    COMMAND "${PDF_ENGINE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${BUILD_DIR}" "${BUILD_DIR}/${output_file}.tex"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    VERBATIM)
endfunction()

make_pandoc_pdf_target(pdf "snodec-book" --metadata-file metadata.yaml
                       ${BOOK_FILES})

make_pandoc_target(tex "snodec-book" --metadata-file metadata.yaml
                   ${BOOK_FILES})

make_pandoc_pdf_target(proposal "book-proposal-package" --metadata-file
                       metadata.yaml proposal/book-proposal-package.md)

# Main manuscript PDF targets require generated figure PDFs because the Markdown
# sources include figures/pdf/fig-*.pdf.
add_dependencies(pdf figures)

add_custom_target(book ALL DEPENDS pdf)

add_custom_target(all-books DEPENDS pdf tex proposal)

# -----------------------------------------------------------------------------
# Publisher/proposal package
# -----------------------------------------------------------------------------
# Create a clean publisher/reviewer package for the full book proposal.  The
# package contains the generated proposal PDF, the generated full manuscript
# PDF, the exact SNode.C source-version pin, and the source files required to
# inspect or rebuild the proposal/manuscript without carrying local build artefacts, IDE state, VCS
# metadata, or workbench reports into the archive.
#
# The package is written to ./packages and named with a date/time stamp plus an
# incrementing two-digit version number, for example:
#
# snodec-book-proposal-package-20260616-214530-v03.tar.gz
#
# The version number is computed at build time by scanning existing proposal
# packages in ./packages and taking the next free number.
set(PROPOSAL_PACKAGE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/packages")
set(PROPOSAL_PACKAGE_SCRIPT
    "${CMAKE_CURRENT_BINARY_DIR}/make-proposal-package.cmake")

file(
  WRITE "${PROPOSAL_PACKAGE_SCRIPT}"
  [==[
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
file(MAKE_DIRECTORY "${STAGING_DIR}/pdf")

set(REQUIRED_SOURCE_FILES
    "metadata.yaml"
    "book-files.txt"
    "SOURCE-VERSION.md"
    "CMakeLists.txt"
    "figures/CMakeLists.txt"
    "proposal/book-proposal-package.md")

set(REQUIRED_SOURCE_DIRS
    "frontmatter"
    "chapters"
    "parts"
    "backmatter"
    "proposal"
    "figures/src"
    "figures/pdf"
    "filters"
    "latex"
    "examples")

set(REQUIRED_BUILD_FILES
    "snodec-book.pdf"
    "book-proposal-package.pdf")

foreach(REQUIRED_FILE IN LISTS REQUIRED_SOURCE_FILES)
  if(NOT EXISTS "${SOURCE_DIR}/${REQUIRED_FILE}")
    message(FATAL_ERROR
      "Required publisher package source file missing: ${REQUIRED_FILE}")
  endif()
endforeach()

foreach(REQUIRED_DIR IN LISTS REQUIRED_SOURCE_DIRS)
  if(NOT IS_DIRECTORY "${SOURCE_DIR}/${REQUIRED_DIR}")
    message(FATAL_ERROR
      "Required publisher package source directory missing: ${REQUIRED_DIR}")
  endif()
endforeach()

foreach(REQUIRED_BUILD_FILE IN LISTS REQUIRED_BUILD_FILES)
  if(NOT EXISTS "${BUILD_DIR}/${REQUIRED_BUILD_FILE}")
    message(FATAL_ERROR
      "Required generated package file missing: ${BUILD_DIR}/${REQUIRED_BUILD_FILE}")
  endif()
endforeach()

function(copy_source_file RELATIVE_PATH)
  get_filename_component(PARENT_DIR "${RELATIVE_PATH}" DIRECTORY)
  if(PARENT_DIR)
    file(MAKE_DIRECTORY "${STAGING_DIR}/${PARENT_DIR}")
    file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
         DESTINATION "${STAGING_DIR}/${PARENT_DIR}")
  else()
    file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
         DESTINATION "${STAGING_DIR}")
  endif()
endfunction()

function(copy_source_dir RELATIVE_PATH)
  get_filename_component(PARENT_DIR "${RELATIVE_PATH}" DIRECTORY)
  if(PARENT_DIR)
    file(MAKE_DIRECTORY "${STAGING_DIR}/${PARENT_DIR}")
    set(DESTINATION_DIR "${STAGING_DIR}/${PARENT_DIR}")
  else()
    set(DESTINATION_DIR "${STAGING_DIR}")
  endif()

  file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
       DESTINATION "${DESTINATION_DIR}"
       PATTERN ".git" EXCLUDE
       PATTERN ".gitignore" EXCLUDE
       PATTERN ".gitattributes" EXCLUDE
       PATTERN ".qtcreator" EXCLUDE
       PATTERN ".idea" EXCLUDE
       PATTERN ".vscode" EXCLUDE
       PATTERN "build" EXCLUDE
       PATTERN "cmake-build-*" EXCLUDE
       PATTERN "CMakeFiles" EXCLUDE
       PATTERN "CMakeCache.txt" EXCLUDE
       PATTERN "packages" EXCLUDE
       PATTERN "*.aux" EXCLUDE
       PATTERN "*.log" EXCLUDE
       PATTERN "*.out" EXCLUDE
       PATTERN "*.toc" EXCLUDE
       PATTERN "*.idx" EXCLUDE
       PATTERN "*.ind" EXCLUDE
       PATTERN "*.ilg" EXCLUDE
       PATTERN "*.fls" EXCLUDE
       PATTERN "*.fdb_latexmk" EXCLUDE
       PATTERN "*.synctex.gz" EXCLUDE)
endfunction()

# Generated PDFs for publisher/reviewer reading.
file(COPY "${BUILD_DIR}/snodec-book.pdf" DESTINATION "${STAGING_DIR}/pdf")
file(COPY "${BUILD_DIR}/book-proposal-package.pdf"
     DESTINATION "${STAGING_DIR}/pdf")

# Required manuscript/proposal sources and build metadata.
foreach(REQUIRED_FILE IN LISTS REQUIRED_SOURCE_FILES)
  copy_source_file("${REQUIRED_FILE}")
endforeach()

foreach(REQUIRED_DIR IN LISTS REQUIRED_SOURCE_DIRS)
  copy_source_dir("${REQUIRED_DIR}")
endforeach()

# Optional high-level publisher-facing orientation files.
foreach(OPTIONAL_FILE IN ITEMS
        "README.md"
        "STRUCTURE.md"
        "LICENSE"
        "LICENSE.md"
        "COPYING"
        "CHANGELOG.md")
  if(EXISTS "${SOURCE_DIR}/${OPTIONAL_FILE}")
    copy_source_file("${OPTIONAL_FILE}")
  endif()
endforeach()

# Optional source-support infrastructure used by the current PDF build.
foreach(OPTIONAL_DIR IN ITEMS
        "cmake"
        "scripts"
        "assets"
        "images"
        "verification")
  if(IS_DIRECTORY "${SOURCE_DIR}/${OPTIONAL_DIR}")
    copy_source_dir("${OPTIONAL_DIR}")
  endif()
endforeach()

# Optional additional application material. The main examples/ tree is required
# above because it contains compact chapter examples and the MiniGateway
# source-of-truth material for Chapters 37 and 38.
foreach(OPTIONAL_DIR IN ITEMS
        "apps"
        "src/apps"
        "MiniGateway"
        "minigateway")
  if(IS_DIRECTORY "${SOURCE_DIR}/${OPTIONAL_DIR}")
    copy_source_dir("${OPTIONAL_DIR}")
  endif()
endforeach()

file(WRITE "${STAGING_DIR}/PACKAGE-CONTENTS.txt"
"SNode.C publisher/reviewer package

This archive is intended for publisher/reviewer evaluation. It contains the generated proposal PDF, the generated full manuscript PDF, the exact SNode.C source-version pin, and the clean source material needed to inspect or rebuild the proposal/manuscript package.

Included:
- pdf/snodec-book.pdf
- pdf/book-proposal-package.pdf
- proposal/
- frontmatter/
- chapters/
- parts/
- backmatter/
- backmatter/index.md
- figures/CMakeLists.txt
- figures/src/
- figures/pdf/
- filters/
- latex/
- examples/
- metadata.yaml
- book-files.txt
- SOURCE-VERSION.md
- CMakeLists.txt

Included when present:
- README.md
- STRUCTURE.md
- LICENSE / LICENSE.md / COPYING
- CHANGELOG.md
- cmake/
- scripts/
- assets/
- images/
- verification/
- apps/
- src/apps/
- MiniGateway*/
- minigateway/

Deliberately excluded:
- .git and other VCS metadata
- IDE state such as .qtcreator, .idea, .vscode
- local build directories and CMake cache files
- generated LaTeX/index auxiliary files
- existing package archives

Package file names are generated by the proposal-package target and include a timestamp and version suffix.
")

execute_process(
  COMMAND "${CMAKE_COMMAND}" -E tar czf "${PACKAGE_PATH}" --format=gnutar .
  WORKING_DIRECTORY "${STAGING_DIR}"
  RESULT_VARIABLE TAR_RESULT)

if(NOT TAR_RESULT EQUAL 0)
  message(FATAL_ERROR "Failed to create proposal package: ${PACKAGE_PATH}")
endif()

file(REMOVE_RECURSE "${STAGING_DIR}")
message(STATUS "Created full book proposal package: ${PACKAGE_PATH}")
]==])

add_custom_target(
  proposal-package
  DEPENDS pdf proposal
  COMMAND
    "${CMAKE_COMMAND}" -D "SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}" -D
    "BUILD_DIR=${BUILD_DIR}" -D "PACKAGE_DIR=${PROPOSAL_PACKAGE_DIR}" -P
    "${PROPOSAL_PACKAGE_SCRIPT}"
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  COMMENT "Creating full publisher/reviewer book proposal package"
  VERBATIM)

# Convenience alias for generators/users that prefer underscores in target
# names. Both targets create the same full publisher/reviewer proposal package.
add_custom_target(proposal_package DEPENDS proposal-package)

add_custom_target(
  book-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${BUILD_DIR}"
  VERBATIM)
