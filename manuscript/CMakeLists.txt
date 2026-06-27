set(BOOK_FILE_LIST "${MANUSCRIPT_DIR}/book-files.txt")
set(BOOK_METADATA_FILE "${PRODUCTION_DIR}/metadata/metadata.yaml")

file(STRINGS "${BOOK_FILE_LIST}" BOOK_FILES)

# Reconfigure automatically when the manuscript file list changes. The Pandoc
# input list is read at configure time and baked into the build rules.
set_property(
  DIRECTORY
  APPEND
  PROPERTY CMAKE_CONFIGURE_DEPENDS "${BOOK_FILE_LIST}")

snodec_add_pandoc_pdf_target(pdf "snodec-book" --metadata-file
                             "${BOOK_METADATA_FILE}" ${BOOK_FILES})

snodec_add_pandoc_tex_target(tex "snodec-book" --metadata-file
                             "${BOOK_METADATA_FILE}" ${BOOK_FILES})

# The main manuscript PDF requires generated figure PDFs because the Markdown
# sources include assets/figures/pdf/fig-*.pdf.
add_dependencies(pdf figures)

add_custom_target(book ALL DEPENDS pdf)
