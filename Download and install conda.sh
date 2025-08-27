# Download conda
curl -O https://repo.anaconda.com/archive/Anaconda3-2025.06-0-Linux-x86_64.sh

# Verify installation
shasum -a 256 Anaconda3-2025.06-0-Linux-x86_64.sh

# Install conda
bash Anaconda3-2025.06-0-Linux-x86_64.sh

# restart Positron by closing the folder to enable Conda env as being a choice of Python kernel interpreter (click folder button in topright and select "Close Folder")
# choose interpreter by clicking on "Python 3.12.11 (Global)" button in top right of window, then select "New Interpreter Session..." and then choose Python 3.13.5 (Conda:base)