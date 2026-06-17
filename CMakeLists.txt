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

function(make_pandoc_target target_name output_file)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BUILD_DIR}"
    COMMAND
      "${PANDOC}" ${ARGN} --syntax-highlighting=idiomatic --from
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
      "${PANDOC}" ${ARGN} --syntax-highlighting=idiomatic --from
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

add_custom_target(book ALL DEPENDS pdf)

add_custom_target(all-books DEPENDS pdf pdf-existing tex tex-existing proposal)

# -----------------------------------------------------------------------------
# Publisher/reviewer package
# -----------------------------------------------------------------------------
# Create a clean package containing the proposal material and the current book
# manuscript source. The package is written to ./packages and named with a
# timestamp plus an incrementing two-digit version number, for example:
#
# snodec-book-proposal-package-20260616-214530-v03.tar.gz
#
# Usage:
#
# cmake --build build --target proposal-package cmake --build build --target
# package-proposal
#
# This target intentionally copies only selected source/manuscript files and
# directories. It does not package .git, build trees, CMake/Ninja state, editor
# settings, or the packages directory itself.
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

# Compute next two-digit version number from all existing package files.
file(GLOB EXISTING_PACKAGES
     "${PACKAGE_DIR}/snodec-book-proposal-package-*-v[0-9][0-9].tar.gz")

set(NEXT_VERSION 1)
foreach(PACKAGE_FILE IN LISTS EXISTING_PACKAGES)
  get_filename_component(PACKAGE_NAME "${PACKAGE_FILE}" NAME)
  if(PACKAGE_NAME MATCHES "-v([0-9][0-9])\\.tar\\.gz$")
    set(CURRENT_VERSION "${CMAKE_MATCH_1}")
    string(REGEX REPLACE "^0+" "" CURRENT_VERSION_NUMBER "${CURRENT_VERSION}")
    if(CURRENT_VERSION_NUMBER STREQUAL "")
      set(CURRENT_VERSION_NUMBER 0)
    endif()
    math(EXPR CANDIDATE_VERSION "${CURRENT_VERSION_NUMBER} + 1")
    if(CANDIDATE_VERSION GREATER NEXT_VERSION)
      set(NEXT_VERSION "${CANDIDATE_VERSION}")
    endif()
  endif()
endforeach()

if(NEXT_VERSION GREATER 99)
  message(FATAL_ERROR "Package version would exceed v99")
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

set(STAGING_PARENT "${CMAKE_CURRENT_BINARY_DIR}/${PACKAGE_BASENAME}-stage")
set(STAGING_ROOT "${STAGING_PARENT}/${PACKAGE_BASENAME}")
file(REMOVE_RECURSE "${STAGING_PARENT}")
file(MAKE_DIRECTORY "${STAGING_ROOT}")

function(copy_required_file RELATIVE_PATH)
  if(NOT EXISTS "${SOURCE_DIR}/${RELATIVE_PATH}")
    message(FATAL_ERROR "Required package file missing: ${RELATIVE_PATH}")
  endif()
  get_filename_component(RELATIVE_DIR "${RELATIVE_PATH}" DIRECTORY)
  if(NOT RELATIVE_DIR STREQUAL "")
    file(MAKE_DIRECTORY "${STAGING_ROOT}/${RELATIVE_DIR}")
  endif()
  file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
       DESTINATION "${STAGING_ROOT}/${RELATIVE_DIR}")
endfunction()

function(copy_optional_file RELATIVE_PATH)
  if(EXISTS "${SOURCE_DIR}/${RELATIVE_PATH}")
    get_filename_component(RELATIVE_DIR "${RELATIVE_PATH}" DIRECTORY)
    if(NOT RELATIVE_DIR STREQUAL "")
      file(MAKE_DIRECTORY "${STAGING_ROOT}/${RELATIVE_DIR}")
    endif()
    file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
         DESTINATION "${STAGING_ROOT}/${RELATIVE_DIR}")
  endif()
endfunction()

function(copy_required_directory RELATIVE_PATH)
  if(NOT IS_DIRECTORY "${SOURCE_DIR}/${RELATIVE_PATH}")
    message(FATAL_ERROR "Required package directory missing: ${RELATIVE_PATH}")
  endif()
  get_filename_component(RELATIVE_DIR "${RELATIVE_PATH}" DIRECTORY)
  if(NOT RELATIVE_DIR STREQUAL "")
    file(MAKE_DIRECTORY "${STAGING_ROOT}/${RELATIVE_DIR}")
  endif()
  file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
       DESTINATION "${STAGING_ROOT}/${RELATIVE_DIR}")
endfunction()

function(copy_optional_directory RELATIVE_PATH)
  if(IS_DIRECTORY "${SOURCE_DIR}/${RELATIVE_PATH}")
    get_filename_component(RELATIVE_DIR "${RELATIVE_PATH}" DIRECTORY)
    if(NOT RELATIVE_DIR STREQUAL "")
      file(MAKE_DIRECTORY "${STAGING_ROOT}/${RELATIVE_DIR}")
    endif()
    file(COPY "${SOURCE_DIR}/${RELATIVE_PATH}"
         DESTINATION "${STAGING_ROOT}/${RELATIVE_DIR}")
  endif()
endfunction()

# Required manuscript/proposal source.
copy_required_file("metadata.yaml")
copy_required_file("CMakeLists.txt")
copy_required_file("book-files.txt")
copy_required_file("book-files-existing-only.txt")
copy_required_directory("parts")
copy_required_directory("chapters")
copy_required_directory("proposal")

# Useful project-level files, copied when present.
copy_optional_file("README.md")
copy_optional_file("STRUCTURE.md")
copy_optional_file("Makefile")
copy_optional_file(".gitignore")

# Example sources used by the manuscript, copied when present.
copy_optional_directory("examples")

# Generated PDFs are optional. Put them below generated/ so they are clearly not
# source files.
file(MAKE_DIRECTORY "${STAGING_ROOT}/generated")
foreach(GENERATED_FILE IN ITEMS
        "snodec-book.pdf"
        "snodec-book-existing-only.pdf"
        "book-proposal-package.pdf")
  if(EXISTS "${BUILD_DIR}/${GENERATED_FILE}")
    file(COPY "${BUILD_DIR}/${GENERATED_FILE}"
         DESTINATION "${STAGING_ROOT}/generated")
  endif()
endforeach()

# Remove accidental local/build state from copied trees, especially from examples/.
foreach(UNWANTED_DIR IN ITEMS
        ".git"
        ".gitignore"
        ".qtcreator"
        "build"
        "CMakeFiles"
        "cmake-build-debug"
        "cmake-build-release"
        "packages")
  if(EXISTS "${STAGING_ROOT}/${UNWANTED_DIR}")
    file(REMOVE_RECURSE "${STAGING_ROOT}/${UNWANTED_DIR}")
  endif()
endforeach()

file(GLOB_RECURSE UNWANTED_DIRS LIST_DIRECTORIES true
     "${STAGING_ROOT}/*/.git"
     "${STAGING_ROOT}/*/.gitignore"
     "${STAGING_ROOT}/*/.qtcreator"
     "${STAGING_ROOT}/*/build"
     "${STAGING_ROOT}/*/CMakeFiles"
     "${STAGING_ROOT}/*/cmake-build-debug"
     "${STAGING_ROOT}/*/cmake-build-release")
foreach(UNWANTED_DIR IN LISTS UNWANTED_DIRS)
  if(IS_DIRECTORY "${UNWANTED_DIR}")
    file(REMOVE_RECURSE "${UNWANTED_DIR}")
  endif()
endforeach()

file(GLOB_RECURSE UNWANTED_FILES
     "${STAGING_ROOT}/CMakeCache.txt"
     "${STAGING_ROOT}/build.ninja"
     "${STAGING_ROOT}/cmake_install.cmake"
     "${STAGING_ROOT}/qtcsettings.cmake"
     "${STAGING_ROOT}/*/CMakeCache.txt"
     "${STAGING_ROOT}/*/build.ninja"
     "${STAGING_ROOT}/*/cmake_install.cmake"
     "${STAGING_ROOT}/*/qtcsettings.cmake"
     "${STAGING_ROOT}/*~"
     "${STAGING_ROOT}/.*.swp"
     "${STAGING_ROOT}/*/.DS_Store")
foreach(UNWANTED_FILE IN LISTS UNWANTED_FILES)
  if(EXISTS "${UNWANTED_FILE}")
    file(REMOVE "${UNWANTED_FILE}")
  endif()
endforeach()

# Hard guard: do not ever create the previous proposal-only package again.
foreach(REQUIRED_STAGED_PATH IN ITEMS parts chapters proposal)
  if(NOT IS_DIRECTORY "${STAGING_ROOT}/${REQUIRED_STAGED_PATH}")
    message(FATAL_ERROR
            "Package staging lacks ${REQUIRED_STAGED_PATH}/. Refusing to create incomplete package.")
  endif()
endforeach()

file(WRITE "${STAGING_ROOT}/PACKAGE-CONTENTS.txt"
"SNode.C publisher/reviewer proposal package\n\nThis archive contains the current manuscript source and proposal material.\n\nIncluded:\n- README.md and STRUCTURE.md, when present\n- metadata.yaml\n- CMakeLists.txt and Makefile, when present\n- book-files.txt and book-files-existing-only.txt\n- parts/\n- chapters/\n- proposal/\n- examples/, when present\n- generated/*.pdf, when already built\n\nExcluded:\n- .git/\n- build trees and CMake/Ninja local state\n- packages/\n- editor/workspace files\n\nGenerated package: ${PACKAGE_BASENAME}.tar.gz\n")

execute_process(
  COMMAND "${CMAKE_COMMAND}" -E tar czf "${PACKAGE_PATH}" --format=gnutar "${PACKAGE_BASENAME}"
  WORKING_DIRECTORY "${STAGING_PARENT}"
  RESULT_VARIABLE TAR_RESULT)

if(NOT TAR_RESULT EQUAL 0)
  message(FATAL_ERROR "Failed to create package: ${PACKAGE_PATH}")
endif()

file(REMOVE_RECURSE "${STAGING_PARENT}")
message(STATUS "Created publisher/reviewer package: ${PACKAGE_PATH}")
]==])

add_custom_target(
  proposal-package
  COMMAND
    "${CMAKE_COMMAND}" -D "SOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}" -D
    "BUILD_DIR=${BUILD_DIR}" -D "PACKAGE_DIR=${PROPOSAL_PACKAGE_DIR}" -P
    "${PROPOSAL_PACKAGE_SCRIPT}"
  WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
  COMMENT
    "Creating publisher/reviewer package with proposal and manuscript source"
  VERBATIM)

add_custom_target(package-proposal DEPENDS proposal-package)
add_custom_target(proposal_package DEPENDS proposal-package)

add_custom_target(proposal-package-with-pdf DEPENDS proposal proposal-package)

add_custom_target(
  book-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${BUILD_DIR}"
  VERBATIM)
