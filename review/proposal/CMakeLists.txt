set(PROPOSAL_METADATA_FILE "${PRODUCTION_DIR}/metadata/proposal-metadata.yaml")
set(PROPOSAL_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/book-proposal-package.md")
set(EVIDENCE_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/evidence-sheet.md")
set(SAMPLE_INTRO "${CMAKE_CURRENT_SOURCE_DIR}/sample-chapters.md")

set(PROPOSAL_SAMPLE_CHAPTERS
    "${MANUSCRIPT_DIR}/chapters/01-why-snodec-exists.md"
    "${MANUSCRIPT_DIR}/chapters/03-your-first-working-program-the-echo-pair.md"
    "${MANUSCRIPT_DIR}/chapters/23-server-sent-events-and-real-time-http.md"
    "${MANUSCRIPT_DIR}/chapters/35-building-minigateway.md"
    "${MANUSCRIPT_DIR}/chapters/37-architectural-judgment-choosing-the-right-layer-and-boundary.md")

snodec_add_pandoc_pdf_target_with_division(
  proposal
  "book-proposal-package"
  section
  --metadata-file "${PROPOSAL_METADATA_FILE}"
  "${PROPOSAL_SOURCE}"
  "${EVIDENCE_SOURCE}")

# Alias with an explicit document role. The historical target name `proposal`
# remains available for existing workflows.
add_custom_target(proposal-pdf DEPENDS proposal)

snodec_add_pandoc_pdf_target_with_division(
  proposal-sample-pdf
  "book-proposal-sample-package"
  section
  --metadata-file "${PROPOSAL_METADATA_FILE}"
  "${PROPOSAL_SOURCE}"
  "${EVIDENCE_SOURCE}"
  "${SAMPLE_INTRO}"
  ${PROPOSAL_SAMPLE_CHAPTERS})
