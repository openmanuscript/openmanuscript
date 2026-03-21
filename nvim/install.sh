echo $HOME

mkdir -p $HOME/.config/nvim/lua/openmanuscript

cp init.lua $HOME/.config/nvim/init.lua
cp manuscript.lua $HOME/.config/nvim/lua/openmanuscript
cp sidebar.lua $HOME/.config/nvim/lua/openmanuscript

ls -la $HOME/.config/nvim
ls -la $HOME/.config/nvim/lua/openmanuscript
