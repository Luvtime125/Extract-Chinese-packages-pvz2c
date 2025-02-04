import subprocess
import sys
import os

# Function to install a package if not already installed
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully!")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

# List of required libraries
required_libraries = [
    "colorama",
    "json",
    "sys",
    "time",
    "subprocess",
    "zipfile"
]

# Install required libraries
for library in required_libraries:
    install_package(library)

# Finish message
print("\033[32mAll required libraries are installed. Press enter to exit.\033[0m")
input()
