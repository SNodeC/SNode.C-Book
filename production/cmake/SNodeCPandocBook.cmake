# Shared Pandoc/XeLaTeX build helpers for the SNode.C book.

function(snodec_add_pandoc_tex_target_with_division target_name output_file top_level_division)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BOOK_BUILD_DIR}"
    COMMAND
      "${PANDOC}" ${ARGN} --lua-filter "${PANDOC_LISTINGS_FILTER}" --lua-filter
      "${PANDOC_CALLOUT_FILTER}" --filter "${PANDOC_CROSSREF_FILTER}"
      --syntax-highlighting=idiomatic --from "${PANDOC_FROM}"
      --top-level-division=${top_level_division} --standalone
      --resource-path "${SNODEC_BOOK_ROOT}:${ASSETS_DIR}"
      -o "${BOOK_BUILD_DIR}/${output_file}.tex"
    WORKING_DIRECTORY "${SNODEC_BOOK_ROOT}"
    VERBATIM)
endfunction()

function(snodec_add_pandoc_pdf_target_with_division target_name output_file top_level_division)
  add_custom_target(
    ${target_name}
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${BOOK_BUILD_DIR}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${DIST_PDF_DIR}"
    COMMAND
      "${PANDOC}" ${ARGN} --lua-filter "${PANDOC_LISTINGS_FILTER}" --lua-filter
      "${PANDOC_CALLOUT_FILTER}" --filter "${PANDOC_CROSSREF_FILTER}"
      --syntax-highlighting=idiomatic --from "${PANDOC_FROM}"
      --top-level-division=${top_level_division} --standalone
      --resource-path "${SNODEC_BOOK_ROOT}:${ASSETS_DIR}"
      -o "${BOOK_BUILD_DIR}/${output_file}.tex"
    # Keep LaTeX auxiliary files between ordinary builds.  Cross-references are
    # resolved through the .aux file; deleting it at the start of every target
    # invocation makes each CMake build look like a first LaTeX pass again and
    # reprints transient "undefined reference" warnings in IDE build output.
    # Use the top-level `book-clean` target when a deliberately clean rebuild is
    # wanted.
    COMMAND "${PDF_ENGINE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${BOOK_BUILD_DIR}" "${BOOK_BUILD_DIR}/${output_file}.tex"
    COMMAND "${CMAKE_COMMAND}" -E chdir "${BOOK_BUILD_DIR}" "${MAKEINDEX}"
            "${output_file}.idx"
    COMMAND "${PDF_ENGINE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${BOOK_BUILD_DIR}" "${BOOK_BUILD_DIR}/${output_file}.tex"
    COMMAND "${PDF_ENGINE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${BOOK_BUILD_DIR}" "${BOOK_BUILD_DIR}/${output_file}.tex"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
            "${BOOK_BUILD_DIR}/${output_file}.pdf"
            "${DIST_PDF_DIR}/${output_file}.pdf"
    WORKING_DIRECTORY "${SNODEC_BOOK_ROOT}"
    VERBATIM)
endfunction()

function(snodec_add_pandoc_tex_target target_name output_file)
  snodec_add_pandoc_tex_target_with_division(${target_name} ${output_file} part ${ARGN})
endfunction()

function(snodec_add_pandoc_pdf_target target_name output_file)
  snodec_add_pandoc_pdf_target_with_division(${target_name} ${output_file} part ${ARGN})
endfunction()

# Backward-compatible helper names used by earlier iterations of this repository.
function(make_pandoc_target target_name output_file)
  snodec_add_pandoc_tex_target(${target_name} ${output_file} ${ARGN})
endfunction()

function(make_pandoc_pdf_target target_name output_file)
  snodec_add_pandoc_pdf_target(${target_name} ${output_file} ${ARGN})
endfunction()
