dotfiles.

Installation:
* Clone the repository in a directory of your choosing passing the --recurse-submodules flag.
* Run `install.py`, passing the directory where you want the dotfiles to be symlinked as an argument. Example: `python install.py ~`

Note: If a file already exists at the location where a symlink is to be installed, the file will be copied to a new directory called backup. It will also maintain the directory structure relative to the directory you provided as an argument. Example: ~/.config/i3/config would be backed up to backup/.config/i3/config if you provided ~ as your installation directory.
