# Figure build rules for the SNode.C book.
#
# Figure source files live in figures/src and are named fig-*.tex. They are
# compiled to PDF files in figures/pdf so Pandoc can include them from Markdown
# as ordinary image files.  A PDF contact sheet is generated from the rendered
# figure PDFs and is part of the `figures` target.

if(NOT DEFINED BUILD_DIR)
  set(BUILD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../build")
endif()

set(FIGURE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(FIGURE_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/pdf")
set(FIGURE_BUILD_ROOT "${BUILD_DIR}/figures")
set(FIGURE_CONTACT_BUILD_DIR "${FIGURE_BUILD_ROOT}/contact-sheet")
set(FIGURE_CONTACT_TEX "${FIGURE_CONTACT_BUILD_DIR}/figures-contact-sheet.tex")
set(FIGURE_CONTACT_PDF "${FIGURE_OUTPUT_DIR}/figures-contact-sheet.pdf")

file(GLOB FIGURE_SOURCES CONFIGURE_DEPENDS "${FIGURE_SOURCE_DIR}/fig-*.tex")
file(GLOB FIGURE_SUPPORT_FILES CONFIGURE_DEPENDS "${FIGURE_SOURCE_DIR}/*.tex")
if(FIGURE_SUPPORT_FILES AND FIGURE_SOURCES)
  list(REMOVE_ITEM FIGURE_SUPPORT_FILES ${FIGURE_SOURCES})
endif()

set(FIGURE_PDFS)

if(FIGURE_SOURCES)
  find_program(XELATEX_EXECUTABLE xelatex)
  if(NOT XELATEX_EXECUTABLE)
    message(
      FATAL_ERROR "xelatex was not found. It is required to build TikZ figures."
    )
  endif()

  foreach(FIGURE_SOURCE IN LISTS FIGURE_SOURCES)
    get_filename_component(FIGURE_NAME "${FIGURE_SOURCE}" NAME_WE)
    set(FIGURE_BUILD_DIR "${FIGURE_BUILD_ROOT}/${FIGURE_NAME}")
    set(FIGURE_PDF "${FIGURE_OUTPUT_DIR}/${FIGURE_NAME}.pdf")

    add_custom_command(
      OUTPUT "${FIGURE_PDF}"
      COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_BUILD_DIR}"
      COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_OUTPUT_DIR}"
      COMMAND "${XELATEX_EXECUTABLE}" -interaction=nonstopmode -halt-on-error
              -output-directory "${FIGURE_BUILD_DIR}" "${FIGURE_SOURCE}"
      COMMAND "${CMAKE_COMMAND}" -E copy_if_different
              "${FIGURE_BUILD_DIR}/${FIGURE_NAME}.pdf" "${FIGURE_PDF}"
      DEPENDS "${FIGURE_SOURCE}" ${FIGURE_SUPPORT_FILES}
      WORKING_DIRECTORY "${FIGURE_SOURCE_DIR}"
      COMMENT "Building TikZ figure ${FIGURE_NAME}"
      VERBATIM)

    list(APPEND FIGURE_PDFS "${FIGURE_PDF}")
  endforeach()

  # Generate an equal-column-width review contact sheet from the rendered
  # figure PDFs.
  #
  # The sheet keeps three figures per row, but every figure is scaled to the
  # same column width.  This preserves a compact overview while making font
  # sizes, line lengths, label density, and visual scale comparable.
  file(MAKE_DIRECTORY "${FIGURE_CONTACT_BUILD_DIR}")
  file(WRITE "${FIGURE_CONTACT_TEX}"
"\\documentclass[a4paper]{article}
\\usepackage[a4paper,margin=12mm]{geometry}
\\usepackage{graphicx}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{microtype}
\\pagestyle{empty}
\\setlength{\\parindent}{0pt}
\\setlength{\\fboxsep}{2pt}
\\setlength{\\fboxrule}{0.4pt}
\\newcommand{\\FigureContactCellWidth}{0.315\\textwidth}
\\begin{document}
{\\Large\\bfseries SNode.C book figure contact sheet}\\par\\vspace{4mm}
{\\small Generated from \\texttt{figures/pdf/fig-*.pdf}.}\\par
{\\small Three figures are shown per row; each figure is scaled to the same column width.}\\par\\vspace{6mm}
")

  set(FIGURE_CONTACT_COLUMN 0)
  foreach(FIGURE_PDF IN LISTS FIGURE_PDFS)
    get_filename_component(FIGURE_FILE_NAME "${FIGURE_PDF}" NAME)
    file(APPEND "${FIGURE_CONTACT_TEX}"
"\\begin{minipage}[t]{\\FigureContactCellWidth}
\\resizebox{\\linewidth}{!}{\\texttt{\\detokenize{${FIGURE_FILE_NAME}}}}\\par\\vspace{1.5mm}
\\centering
\\fbox{\\includegraphics[width=\\dimexpr\\linewidth-2\\fboxsep-2\\fboxrule\\relax]{${FIGURE_PDF}}}\\par
\\end{minipage}")

    math(EXPR FIGURE_CONTACT_COLUMN "${FIGURE_CONTACT_COLUMN} + 1")
    if(FIGURE_CONTACT_COLUMN EQUAL 3)
      file(APPEND "${FIGURE_CONTACT_TEX}" "\\par\\vspace{7mm}\n")
      set(FIGURE_CONTACT_COLUMN 0)
    else()
      file(APPEND "${FIGURE_CONTACT_TEX}" "\\hfill\n")
    endif()
  endforeach()

  if(NOT FIGURE_CONTACT_COLUMN EQUAL 0)
    file(APPEND "${FIGURE_CONTACT_TEX}" "\\par\\vspace{7mm}\n")
  endif()

  file(APPEND "${FIGURE_CONTACT_TEX}" "\\end{document}\n")

  add_custom_command(
    OUTPUT "${FIGURE_CONTACT_PDF}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_CONTACT_BUILD_DIR}"
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_OUTPUT_DIR}"
    COMMAND "${XELATEX_EXECUTABLE}" -interaction=nonstopmode -halt-on-error
            -output-directory "${FIGURE_CONTACT_BUILD_DIR}"
            "${FIGURE_CONTACT_TEX}"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
            "${FIGURE_CONTACT_BUILD_DIR}/figures-contact-sheet.pdf"
            "${FIGURE_CONTACT_PDF}"
    DEPENDS ${FIGURE_PDFS} "${FIGURE_CONTACT_TEX}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    COMMENT "Building figure contact sheet"
    VERBATIM)

  add_custom_target(figures-contact-sheet DEPENDS "${FIGURE_CONTACT_PDF}")
  add_custom_target(figures DEPENDS ${FIGURE_PDFS} figures-contact-sheet)
else()
  add_custom_target(
    figures-contact-sheet
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_OUTPUT_DIR}"
    COMMENT "No TikZ figure sources found; no figure contact sheet generated"
    VERBATIM)

  add_custom_target(
    figures
    COMMAND "${CMAKE_COMMAND}" -E make_directory "${FIGURE_OUTPUT_DIR}"
    DEPENDS figures-contact-sheet
    COMMENT "No TikZ figure sources found"
    VERBATIM)
endif()

add_custom_target(
  figures-clean
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${FIGURE_BUILD_ROOT}"
  COMMAND "${CMAKE_COMMAND}" -E rm -rf "${FIGURE_OUTPUT_DIR}"
  VERBATIM)
