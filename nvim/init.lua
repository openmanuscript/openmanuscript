-- ~/.config/nvim/init.lua
-- Neovim configuration for OpenManuscript

-- colorscheme (dark background, bright text)
vim.cmd("colorscheme habamax")

-- basic settings
vim.opt.number         = false
vim.opt.relativenumber = false
vim.opt.wrap           = true
vim.opt.linebreak      = true
vim.opt.scrolloff      = 8
vim.opt.signcolumn     = "no"
vim.opt.updatetime     = 300
vim.opt.termguicolors  = true
vim.opt.textwidth      = 80
vim.opt.signcolumn     = "yes"

-- use spaces, not tabs
vim.opt.expandtab  = true
vim.opt.shiftwidth = 4
vim.opt.tabstop    = 4

-- spelling
vim.opt.spell     = true
vim.opt.spelllang = "en_us"
vim.opt.spellfile = "./spell/vim." .. vim.o.encoding .. ".add"
vim.cmd("syntax spell toplevel")
vim.api.nvim_set_hl(0, "SpellBad", { underline = true, cterm = { underline = true } })
vim.api.nvim_set_hl(0, "SpellCap", {})

-- remap 
local options = {}
vim.keymap.set('i', 'kj', "<Esc>", options)

-- leader key
vim.g.mapleader = " "

-- load the openmanuscript plugin
local sidebar = require("openmanuscript.sidebar")

-- global keybinding: Ctrl+m toggles the sidebar
vim.keymap.set("n", "<C-m>", function()
    sidebar.toggle()
end, { noremap = true, silent = true, desc = "Toggle OpenManuscript sidebar" })

-- user commands
vim.api.nvim_create_user_command("OmsOpen", function(opts)
    local path = opts.args ~= "" and opts.args or nil
    sidebar.open(path)
end, { nargs = "?", complete = "file", desc = "Open the OpenManuscript sidebar" })

vim.api.nvim_create_user_command("OmsClose", function()
    sidebar.close()
end, { desc = "Close the OpenManuscript sidebar" })

vim.api.nvim_create_user_command("OmsToggle", function()
    sidebar.toggle()
end, { desc = "Toggle the OpenManuscript sidebar" })

-- ---------------------------------------------------------------------------
-- if nvim is opened with a .yaml file that contains 'manuscript:',
-- treat it as an OpenManuscript project: open the sidebar automatically
-- and show a blank buffer in the main window instead of the raw yaml.
-- ---------------------------------------------------------------------------
vim.api.nvim_create_autocmd("VimEnter", {
    callback = function()
        local args = vim.fn.argv()
        if #args ~= 1 then return end

        local filepath = vim.fn.fnamemodify(args[1], ":p")

        if not filepath:match("%.yaml$") then return end
        if vim.fn.filereadable(filepath) ~= 1 then return end

        local lines = vim.fn.readfile(filepath, "", 10)
        local is_manuscript = false
        for _, line in ipairs(lines) do
            if line:match("^manuscript%s*:") then
                is_manuscript = true
                break
            end
        end
        if not is_manuscript then return end

        vim.cmd("enew")
        vim.bo.buftype  = "nofile"
        vim.bo.swapfile = false

        sidebar.open(filepath)
    end,
    desc = "Auto-open OpenManuscript sidebar when launched with a manuscript yaml"
})
