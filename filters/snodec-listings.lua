-- Assign book-specific listings styles to fenced code blocks.
--
-- Purpose:
--   * ```text and unlabeled conceptual sketches render as plain black text.
--   * C++ blocks keep the SNode.C C++ highlighting style.
--   * Shell/configuration-like blocks remain visually code-like but are not
--     highlighted as C++.
--
-- The filter does not change chapter prose. It only adds a listings style
-- attribute when the author did not already specify one explicitly.

local function has_class(el, name)
  for _, class in ipairs(el.classes) do
    if class == name then
      return true
    end
  end
  return false
end

local function has_any_class(el, names)
  for _, name in ipairs(names) do
    if has_class(el, name) then
      return true
    end
  end
  return false
end

function CodeBlock(el)
  -- Respect explicit per-block styling in the manuscript.
  if el.attributes["style"] ~= nil and el.attributes["style"] ~= "" then
    return el
  end

  if has_any_class(el, {"cpp", "c++", "cc", "cxx", "h", "hh", "hpp", "hxx"}) then
    el.attributes["style"] = "snodec-cpp"
    return el
  end

  if has_any_class(el, {"sh", "shell", "bash", "console", "terminal"}) then
    el.attributes["style"] = "snodec-shell"
    return el
  end

  if has_class(el, "cmake") then
    el.attributes["style"] = "snodec-cmake"
    return el
  end

  if has_any_class(el, {"ini", "json", "yaml", "toml", "conf", "config"}) then
    el.attributes["style"] = "snodec-config"
    return el
  end

  -- Pandoc's "text" class is intentionally plain. Unlabeled blocks are also
  -- treated as plain, because the book uses them for conceptual sketches,
  -- directory trees, and output shapes.
  if has_any_class(el, {"text", "plain", "output", "tree"}) or #el.classes == 0 then
    el.attributes["style"] = "snodec-plain"
    return el
  end

  return el
end
