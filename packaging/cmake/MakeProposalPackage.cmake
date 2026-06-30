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

# The CI/publisher artifact must be stable and unversioned.  Do not create
# timestamped packages here: wildcard artifact uploads would otherwise collect
# historic packages from previous local or CI runs.
set(PACKAGE_BASENAME "snodec-book-proposal-package")
set(PACKAGE_PATH "${PACKAGE_DIR}/${PACKAGE_BASENAME}.tar.gz")
set(STAGING_ROOT "${PACKAGE_DIR}/.staging")
set(STAGING_DIR "${STAGING_ROOT}/${PACKAGE_BASENAME}")

file(GLOB HISTORIC_PACKAGE_PATHS
     "${PACKAGE_DIR}/snodec-book-proposal-package-*.tar.gz")
if(HISTORIC_PACKAGE_PATHS)
  file(REMOVE ${HISTORIC_PACKAGE_PATHS})
endif()

file(REMOVE "${PACKAGE_PATH}")
file(REMOVE_RECURSE "${STAGING_DIR}")
file(MAKE_DIRECTORY "${STAGING_DIR}")
file(MAKE_DIRECTORY "${STAGING_DIR}/dist/pdf")

set(REQUIRED_SOURCE_FILES
    "CMakeLists.txt"
    "README.md"
    "STRUCTURE.md"
    ".github/workflows/book-package.yml"
    ".github/workflows/companion-examples.yml"
    "ci/check-source-hygiene.sh"
    "ci/build-book-package.sh"
    "ci/build-companion-examples.sh"
    "ci/run-behavior-smoke-tests.sh"
    "ci/run-behavior-smoke-tests.py"
    "production/CMakeLists.txt"
    "production/cmake/SNodeCBookPaths.cmake"
    "production/cmake/SNodeCBookTools.cmake"
    "production/cmake/SNodeCPandocBook.cmake"
    "production/metadata/metadata.yaml"
    "production/metadata/proposal-metadata.yaml"
    "assets/CMakeLists.txt"
    "assets/figures/CMakeLists.txt"
    "companion/CMakeLists.txt"
    "manuscript/CMakeLists.txt"
    "manuscript/book-files.txt"
    "review/CMakeLists.txt"
    "review/proposal/CMakeLists.txt"
    "review/proposal/book-proposal-package.md"
    "review/proposal/evidence-sheet.md"
    "review/proposal/sample-chapters.md"
    "packaging/CMakeLists.txt"
    "packaging/cmake/MakeProposalPackage.cmake"
    "packaging/PACKAGE-CONTENTS.txt"
    "source-baseline/CMakeLists.txt"
    "source-baseline/SOURCE-VERSION.md")

set(REQUIRED_SOURCE_DIRS
    "manuscript/frontmatter"
    "manuscript/chapters"
    "manuscript/parts"
    "manuscript/backmatter"
    "production/filters"
    "production/latex"
    "production/cmake"
    "assets/figures/src"
    "assets/figures/pdf"
    "companion/examples"
    "source-baseline"
    "review/proposal"
    "review/verification"
    "packaging"
    "packaging/cmake"
    "ci"
    ".github/workflows")

set(REQUIRED_BUILD_FILES
    "snodec-book.pdf"
    "book-proposal-package.pdf"
    "book-proposal-sample-package.pdf")

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
       PATTERN ".gitattributes" EXCLUDE
       PATTERN ".qtcreator" EXCLUDE
       PATTERN ".idea" EXCLUDE
       PATTERN ".vscode" EXCLUDE
       PATTERN "build" EXCLUDE
       PATTERN "cmake-build-*" EXCLUDE
       PATTERN "CMakeFiles" EXCLUDE
       PATTERN "CMakeCache.txt" EXCLUDE
       PATTERN "dist/packages" EXCLUDE
       PATTERN ".staging" EXCLUDE
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
file(COPY "${BUILD_DIR}/snodec-book.pdf" DESTINATION "${STAGING_DIR}/dist/pdf")
file(COPY "${BUILD_DIR}/book-proposal-package.pdf"
     DESTINATION "${STAGING_DIR}/dist/pdf")
file(COPY "${BUILD_DIR}/book-proposal-sample-package.pdf"
     DESTINATION "${STAGING_DIR}/dist/pdf")

# Required manuscript/proposal sources and build metadata.
foreach(REQUIRED_FILE IN LISTS REQUIRED_SOURCE_FILES)
  copy_source_file("${REQUIRED_FILE}")
endforeach()

foreach(REQUIRED_DIR IN LISTS REQUIRED_SOURCE_DIRS)
  copy_source_dir("${REQUIRED_DIR}")
endforeach()

# Optional high-level publisher-facing orientation files.
foreach(OPTIONAL_FILE IN ITEMS
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
        "production/scripts")
  if(IS_DIRECTORY "${SOURCE_DIR}/${OPTIONAL_DIR}")
    copy_source_dir("${OPTIONAL_DIR}")
  endif()
endforeach()

execute_process(
  COMMAND "${CMAKE_COMMAND}" -E tar czf "${PACKAGE_PATH}" --format=gnutar .
  WORKING_DIRECTORY "${STAGING_DIR}"
  RESULT_VARIABLE TAR_RESULT)

if(NOT TAR_RESULT EQUAL 0)
  message(FATAL_ERROR "Failed to create proposal package: ${PACKAGE_PATH}")
endif()

file(REMOVE_RECURSE "${STAGING_ROOT}")
message(STATUS "Created full book proposal package: ${PACKAGE_PATH}")
