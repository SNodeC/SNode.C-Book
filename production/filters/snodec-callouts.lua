-- SNode.C book semantic callouts for Pandoc.
--
-- Markdown source stays semantic, for example:
--
--   ::: {.snodec-rule title="Runtime-flow rule"}
--   ...
--   :::
--
-- LaTeX/PDF output becomes a tcolorbox. Other output formats keep the Div,
-- with a stable data attribute for later CSS/HTML processing.

local callouts = {
  ["snodec-remember"]  = { env = "snodecrememberbox",  title = "What to remember" },
  ["snodec-note"]      = { env = "snodecnotebox",      title = "Note" },
  ["snodec-warning"]   = { env = "snodecwarningbox",   title = "Warning" },
  ["snodec-rule"]      = { env = "snodecrulebox",      title = "Design rule" },
  ["snodec-checklist"] = { env = "snodecchecklistbox", title = "Checklist" },

  -- Conservative aliases. They map to the same visual vocabulary so the
  -- manuscript does not grow an uncontrolled set of box styles.
  ["snodec-principle"] = { env = "snodecrulebox",      title = "Architectural principle" },
  ["snodec-tip"]       = { env = "snodecnotebox",      title = "Note" },
  ["snodec-danger"]    = { env = "snodecwarningbox",   title = "Warning" }
}

local latex_replacements = {
  ["\\"] = "\\textbackslash{}",
  ["{"]  = "\\{",
  ["}"]  = "\\}",
  ["$"]  = "\\$",
  ["&"]  = "\\&",
  ["#"]  = "\\#",
  ["_"]  = "\\_",
  ["%"]  = "\\%",
  ["~"]  = "\\textasciitilde{}",
  ["^"]  = "\\textasciicircum{}"
}

local function latex_escape(value)
  value = tostring(value or "")
  return (value:gsub("[\\{}$&#_%%~%^]", latex_replacements))
end

local function find_callout_class(div)
  for _, class in ipairs(div.classes) do
    if callouts[class] then
      return class, callouts[class]
    end
  end

  -- Optional attribute form for future use:
  -- ::: {type="rule" title="Boundary rule"}
  local type_attr = div.attributes and div.attributes["type"]
  if type_attr then
    local class = "snodec-" .. type_attr
    if callouts[class] then
      return class, callouts[class]
    end
  end

  return nil, nil
end

local function title_for(div, spec)
  local title = div.attributes and div.attributes["title"]
  if title and title ~= "" then
    return title
  end
  return spec.title
end

function Div(div)
  local class, spec = find_callout_class(div)
  if not spec then
    return nil
  end

  if FORMAT:match("latex") or FORMAT:match("pdf") or FORMAT:match("beamer") then
    local title = latex_escape(title_for(div, spec))
    local blocks = { pandoc.RawBlock("latex", "\\begin{" .. spec.env .. "}{" .. title .. "}") }

    for _, block in ipairs(div.content) do
      table.insert(blocks, block)
    end

    table.insert(blocks, pandoc.RawBlock("latex", "\\end{" .. spec.env .. "}"))
    return blocks
  end

  -- Preserve semantic information for non-LaTeX outputs. This lets later HTML
  -- CSS or EPUB processing style the same source without rewriting chapters.
  div.attributes["data-snodec-callout"] = class
  if not div.attributes["title"] or div.attributes["title"] == "" then
    div.attributes["title"] = spec.title
  end
  return div
end
