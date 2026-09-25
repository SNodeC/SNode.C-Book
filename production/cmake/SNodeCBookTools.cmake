# Tool configuration for the SNode.C book build.

set(PANDOC
    pandoc
    CACHE STRING "Pandoc executable")
set(PDF_ENGINE
    xelatex
    CACHE STRING "Pandoc PDF engine")
set(MAKEINDEX
    makeindex
    CACHE STRING "MakeIndex executable")

set(PANDOC_FROM "markdown+raw_tex+fenced_code_attributes")

set(PANDOC_CROSSREF_FILTER
    pandoc-crossref
    CACHE STRING "Pandoc cross-reference filter executable")

set(PANDOC_CALLOUT_FILTER
    "${PRODUCTION_DIR}/filters/snodec-callouts.lua"
    CACHE STRING "Pandoc Lua filter for SNode.C semantic callouts")

set(PANDOC_LISTINGS_FILTER
    "${PRODUCTION_DIR}/filters/snodec-listings.lua"
    CACHE STRING "Pandoc Lua filter for book-specific listings styles")

# Use the same parsed ABI check for direct CMake builds and the CI workflow.
execute_process(
  COMMAND python3 "${SNODEC_BOOK_ROOT}/ci/check-publication-tools.py"
          --pandoc "${PANDOC}" --crossref "${PANDOC_CROSSREF_FILTER}"
  RESULT_VARIABLE publication_tools_result)
if(NOT publication_tools_result EQUAL 0)
  message(FATAL_ERROR "Incompatible publication tools; use Pandoc 3.9.0.2 with pandoc-crossref v0.3.24a")
endif()
