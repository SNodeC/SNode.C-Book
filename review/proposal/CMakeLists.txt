set(BOOK_METADATA_FILE "${PRODUCTION_DIR}/metadata/metadata.yaml")

snodec_add_pandoc_pdf_target(
  proposal
  "book-proposal-package"
  --metadata-file "${BOOK_METADATA_FILE}"
  "${CMAKE_CURRENT_SOURCE_DIR}/book-proposal-package.md"
  "${CMAKE_CURRENT_SOURCE_DIR}/evidence-sheet.md")
