-- ~/.config/nvim/lua/openmanuscript/sidebar.lua
--
-- Left-side panel showing OpenManuscript chapter/scene hierarchy.
-- Toggle with Ctrl+m. Enter opens scene files in the main window.

local M = {}
local ms = require("openmanuscript.manuscript")

-- ---------------------------------------------------------------------------
-- custom highlight groups for the sidebar
-- override these in your init.lua to match your colorscheme
-- ---------------------------------------------------------------------------
vim.api.nvim_set_hl(0, "OmsTitle",   { fg = "#ffffff", bold = true })
vim.api.nvim_set_hl(0, "OmsChapter", { fg = "#aaaaaa", bold = true })
vim.api.nvim_set_hl(0, "OmsScene",   { fg = "#666666" })
vim.api.nvim_set_hl(0, "OmsMissing", { fg = "#444444" })
vim.api.nvim_set_hl(0, "OmsDivider", { fg = "#333333" })

-- ---------------------------------------------------------------------------
-- state
-- ---------------------------------------------------------------------------
local state = {
    buf       = nil,
    win       = nil,
    yaml_path = nil,
    lines     = {},
    targets   = {},
    width     = 35,
}

-- ---------------------------------------------------------------------------
-- helpers
-- ---------------------------------------------------------------------------

local function is_open()
    return state.win ~= nil
        and vim.api.nvim_win_is_valid(state.win)
end

local function is_valid_buf()
    return state.buf ~= nil
        and vim.api.nvim_buf_is_valid(state.buf)
end

-- ---------------------------------------------------------------------------
-- build the display lines from manuscript data
-- ---------------------------------------------------------------------------
local function build_lines(yaml_path)
    local manuscript, err = ms.parse_yaml(yaml_path)
    if not manuscript then
        return { "Error: " .. (err or "unknown") }, {}
    end

    local lines   = {}
    local targets = {}

    table.insert(lines, " " .. manuscript.title)
    table.insert(targets, false)
    table.insert(lines, string.rep("─", state.width - 2))
    table.insert(targets, false)

    local chapter_num = 0
    for _, chapter in ipairs(manuscript.chapters) do
        if ms.include_chapter(chapter) then
            if ms.is_numbered(chapter) then
                chapter_num = chapter_num + 1
            end

            local label
            if ms.is_numbered(chapter) then
                label = string.format(" Chapter %d: %s", chapter_num, chapter.title)
            else
                label = string.format(" %s", chapter.title)
            end

            local first_scene = nil
            for _, scene_name in ipairs(chapter.scenes) do
                local path = ms.scene_path(yaml_path, scene_name)
                if vim.fn.filereadable(path) == 1 then
                    first_scene = path
                    break
                end
            end

            table.insert(lines, label)
            table.insert(targets, first_scene)

            for _, scene_name in ipairs(chapter.scenes) do
                local path   = ms.scene_path(yaml_path, scene_name)
                local exists = vim.fn.filereadable(path) == 1
                local marker = exists and "  ○ " or "  ✗ "
                table.insert(lines, marker .. scene_name)
                table.insert(targets, exists and path or false)
            end
        end
    end

    table.insert(lines, "")
    table.insert(targets, false)
    table.insert(lines, " [q] close  [r] refresh")
    table.insert(targets, false)

    return lines, targets
end

-- ---------------------------------------------------------------------------
-- create or reuse the sidebar buffer
-- ---------------------------------------------------------------------------
local function get_or_create_buf()
    if is_valid_buf() then
        return state.buf
    end
    local buf = vim.api.nvim_create_buf(false, true)
    vim.api.nvim_buf_set_name(buf, "OpenManuscript")
    vim.bo[buf].buftype    = "nofile"
    vim.bo[buf].bufhidden  = "hide"
    vim.bo[buf].swapfile   = false
    vim.bo[buf].modifiable = false
    vim.bo[buf].filetype   = "openmanuscript"
    state.buf = buf
    return buf
end

-- ---------------------------------------------------------------------------
-- write lines into the sidebar buffer
-- ---------------------------------------------------------------------------
local function render(yaml_path)
    state.yaml_path          = yaml_path
    state.lines, state.targets = build_lines(yaml_path)

    local buf = get_or_create_buf()
    vim.bo[buf].modifiable = true
    vim.api.nvim_buf_set_lines(buf, 0, -1, false, state.lines)
    vim.bo[buf].modifiable = false

    local ns = vim.api.nvim_create_namespace("openmanuscript")
    vim.api.nvim_buf_clear_namespace(buf, ns, 0, -1)

    for i, line in ipairs(state.lines) do
        if line:match("^─+") then
            vim.api.nvim_buf_add_highlight(buf, ns, "OmsDivider", i - 1, 0, -1)
        elseif line:match("^ Chapter") then
            vim.api.nvim_buf_add_highlight(buf, ns, "OmsChapter", i - 1, 0, -1)
        elseif line:match("^ ") and not line:match("^  ") then
            -- manuscript title and footer hint lines
            vim.api.nvim_buf_add_highlight(buf, ns, "OmsTitle", i - 1, 0, -1)
        elseif line:match("^  ○") then
            vim.api.nvim_buf_add_highlight(buf, ns, "OmsScene", i - 1, 0, -1)
        elseif line:match("^  ✗") then
            vim.api.nvim_buf_add_highlight(buf, ns, "OmsMissing", i - 1, 0, -1)
        end
    end
end

-- ---------------------------------------------------------------------------
-- open a file in the previous (main) window
-- ---------------------------------------------------------------------------
local function open_target()
    local sidebar_win = vim.api.nvim_get_current_win()
    local row         = vim.api.nvim_win_get_cursor(sidebar_win)[1]
    local target      = state.targets[row]
    if not target then return end

    local wins     = vim.api.nvim_list_wins()
    local main_win = nil
    for _, w in ipairs(wins) do
        if w ~= sidebar_win then
            main_win = w
            break
        end
    end

    if main_win then
        vim.api.nvim_set_current_win(main_win)
        vim.cmd("edit " .. vim.fn.fnameescape(target))
    else
        vim.cmd("edit " .. vim.fn.fnameescape(target))
    end
end

-- ---------------------------------------------------------------------------
-- set keybindings inside the sidebar buffer
-- ---------------------------------------------------------------------------
local function set_keymaps(buf)
    local opts = { noremap = true, silent = true, buffer = buf }
    vim.keymap.set("n", "<CR>",  open_target, opts)
    vim.keymap.set("n", "o",     open_target, opts)
    vim.keymap.set("n", "q",     function() M.close() end, opts)
    vim.keymap.set("n", "r",     function()
        if state.yaml_path then render(state.yaml_path) end
    end, opts)
    -- vim.keymap.set("n", "<C-m>", function() M.toggle() end, opts)
end

-- ---------------------------------------------------------------------------
-- open the sidebar
-- ---------------------------------------------------------------------------
function M.open(yaml_path)
    yaml_path = yaml_path or ms.find_yaml()
    if not yaml_path then
        vim.notify("OpenManuscript: no manuscript.yaml found", vim.log.levels.WARN)
        return
    end

    local buf = get_or_create_buf()
    render(yaml_path)
    set_keymaps(buf)

    vim.cmd("topleft " .. state.width .. "vsplit")
    local win = vim.api.nvim_get_current_win()
    vim.api.nvim_win_set_buf(win, buf)
    state.win = win

    vim.wo[win].number         = false
    vim.wo[win].relativenumber = false
    vim.wo[win].signcolumn     = "no"
    vim.wo[win].wrap           = false
    vim.wo[win].winfixwidth    = true
    vim.wo[win].cursorline     = true
end

-- ---------------------------------------------------------------------------
-- close the sidebar
-- ---------------------------------------------------------------------------
function M.close()
    if is_open() then
        vim.api.nvim_win_close(state.win, true)
        state.win = nil
    end
end

-- ---------------------------------------------------------------------------
-- toggle the sidebar
-- ---------------------------------------------------------------------------
function M.toggle()
    if is_open() then
        M.close()
    else
        M.open()
    end
end

return M
