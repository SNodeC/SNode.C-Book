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

add_custom_target(
  book-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${BUILD_DIR}"
  VERBATIM)
