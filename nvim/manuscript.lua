-- ~/.config/nvim/lua/openmanuscript/manuscript.lua
--
-- Reads manuscript.yaml and returns structured data.
-- Uses a minimal hand-written YAML parser sufficient for
-- the OpenManuscript format (no external dependencies needed).

local M = {}

function M.find_yaml(start_dir)
    local dir = start_dir or vim.fn.expand("%:p:h")
    if dir == "" then
        dir = vim.fn.getcwd()
    end

    local prev = nil
    while dir ~= prev do
        local candidate = dir .. "/manuscript.yaml"
        if vim.fn.filereadable(candidate) == 1 then
            return candidate
        end
        prev = dir
        dir = vim.fn.fnamemodify(dir, ":h")
    end

    return nil
end

function M.parse_yaml(filepath)
    local lines = vim.fn.readfile(filepath)
    if not lines then
        return nil, "Could not read file: " .. filepath
    end

    local manuscript = {
        title    = "",
        chapters = {}
    }

    local in_manuscript   = false
    local in_chapters     = false
    local current_chapter = nil

    for _, line in ipairs(lines) do
        if line:match("^manuscript%s*:") then
            in_manuscript = true

        elseif in_manuscript and not in_chapters and line:match("^%s+title%s*:%s*(.+)") then
            local title = line:match("^%s+title%s*:%s*(.+)")
            manuscript.title = title:gsub('"', ''):gsub("'", ""):gsub("%s+$", "")

        elseif in_manuscript and line:match("^%s+chapters%s*:") then
            in_chapters = true

        elseif in_chapters and (line:match("^%s+%-$") or line:match("^%s+%-%s*$")) then
            if current_chapter then
                table.insert(manuscript.chapters, current_chapter)
            end
            current_chapter = {
                title  = "",
                scenes = {},
                tags   = {},
                pov    = "",
                type   = "chapter",
                state  = ""
            }

        elseif current_chapter then
            local title = line:match("^%s+title%s*:%s*(.+)")
            if title then
                current_chapter.title = title:gsub('"', ''):gsub("'", ""):gsub("%s+$", "")
            end

            local pov = line:match("^%s+pov%s*:%s*(.+)")
            if pov then
                current_chapter.pov = pov:gsub('"', ''):gsub("'", ""):gsub("%s+$", "")
            end

            local chaptype = line:match("^%s+type%s*:%s*(.+)")
            if chaptype then
                current_chapter.type = chaptype:gsub('"', ''):gsub("'", ""):gsub("%s+$", "")
            end

            local state = line:match("^%s+state%s*:%s*(.+)")
            if state then
                current_chapter.state = state:gsub('"', ''):gsub("'", ""):gsub("%s+$", "")
            end

            local scenes_str = line:match("^%s+scenes%s*:%s*%[(.-)%]")
            if scenes_str then
                for scene in scenes_str:gmatch('[^,]+') do
                    scene = scene:gsub('"', ''):gsub("'", ""):gsub("^%s+", ""):gsub("%s+$", "")
                    if scene ~= "" then
                        table.insert(current_chapter.scenes, scene)
                    end
                end
            end

            local tags_str = line:match("^%s+tags%s*:%s*%[(.-)%]")
            if tags_str then
                for tag in tags_str:gmatch('[^,]+') do
                    tag = tag:gsub('"', ''):gsub("'", ""):gsub("^%s+", ""):gsub("%s+$", "")
                    if tag ~= "" then
                        table.insert(current_chapter.tags, tag)
                    end
                end
            end
        end
    end

    if current_chapter then
        table.insert(manuscript.chapters, current_chapter)
    end

    return manuscript, nil
end

function M.scenes_dir(yaml_path)
    return vim.fn.fnamemodify(yaml_path, ":h") .. "/scenes"
end

function M.scene_path(yaml_path, scene_name)
    local sdir = M.scenes_dir(yaml_path)
    if scene_name:match("%.md$") then
        return sdir .. "/" .. scene_name
    end
    return sdir .. "/" .. scene_name .. ".md"
end

function M.include_chapter(chapter)
    local state = chapter.state or ""
    return state == "" or state == "on"
end

function M.is_numbered(chapter)
    local t = (chapter.type or "chapter"):lower()
    return t ~= "quote" and t ~= "synopsis"
end

return M
