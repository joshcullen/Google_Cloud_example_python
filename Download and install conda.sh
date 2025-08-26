# Download conda
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-x86_64.sh

# Verify installation
shasum -a 256 Anaconda3-2025.06-0-Linux-x86_64.sh

# Install conda
bash Anaconda3-2025.06-0-Linux-x86_64.sh

# restart Positron to enable Conda envs as being a choice of Python kernel interpreter
# choose interpreter by opening command palette (ctrl/cmd + shift + P or clicking gear symbol in bottom left) and then searching "Python: Select interpreter" and choosing the option with "Conda" in blue text on the right side of menu