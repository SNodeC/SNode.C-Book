# Tool configuration for the SNode.C book build.

include(FetchContent)
if(POLICY CMP0135)
    cmake_policy(SET CMP0135 NEW)
endif()

# One installation policy for fresh terminal, IDE and CI builds. Explicit paths
# still override the managed tools; bare legacy defaults select the managed
# pair.
if(NOT DEFINED PANDOC OR PANDOC STREQUAL "pandoc")
    FetchContent_Declare(
        book_pandoc
        URL https://github.com/jgm/pandoc/releases/download/3.9.0.2/pandoc-3.9.0.2-linux-amd64.tar.gz
        URL_HASH
            SHA256=a69abfababda8a56969a254b09f9553a7be89ddec00d4e0fe9fd585d71a67508
    )
    FetchContent_MakeAvailable(book_pandoc)
    set(PANDOC
        "${book_pandoc_SOURCE_DIR}/bin/pandoc"
        CACHE FILEPATH "Pandoc executable" FORCE
    )
endif()
if(NOT DEFINED PANDOC_CROSSREF_FILTER OR PANDOC_CROSSREF_FILTER STREQUAL
                                         "pandoc-crossref"
)
    FetchContent_Declare(
        book_crossref
        URL https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.24a/pandoc-crossref-Linux-X64.tar.xz
        URL_HASH
            SHA256=afaa8867ab8d908b7e5ad1b96f62eedea6a5d3e89ee14e152cd72e67f535a728
    )
    FetchContent_MakeAvailable(book_crossref)
    set(PANDOC_CROSSREF_FILTER
        "${book_crossref_SOURCE_DIR}/pandoc-crossref"
        CACHE FILEPATH "Pandoc cross-reference filter executable" FORCE
    )
endif()
set(PDF_ENGINE
    xelatex
    CACHE STRING "Pandoc PDF engine"
)
set(MAKEINDEX
    makeindex
    CACHE STRING "MakeIndex executable"
)

set(PANDOC_FROM "markdown+raw_tex+fenced_code_attributes")

set(PANDOC_CALLOUT_FILTER
    "${PRODUCTION_DIR}/filters/snodec-callouts.lua"
    CACHE STRING "Pandoc Lua filter for SNode.C semantic callouts"
)

set(PANDOC_LISTINGS_FILTER
    "${PRODUCTION_DIR}/filters/snodec-listings.lua"
    CACHE STRING "Pandoc Lua filter for book-specific listings styles"
)

# Use the same parsed ABI check for direct CMake builds and the CI workflow.
execute_process(
    COMMAND python3 "${SNODEC_BOOK_ROOT}/ci/check-publication-tools.py" --pandoc
            "${PANDOC}" --crossref "${PANDOC_CROSSREF_FILTER}"
    RESULT_VARIABLE publication_tools_result
)
if(NOT publication_tools_result EQUAL 0)
    message(
        FATAL_ERROR
            "Incompatible publication tools; use Pandoc 3.9.0.2 with pandoc-crossref v0.3.24a"
    )
endif()
