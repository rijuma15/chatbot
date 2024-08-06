import subprocess
import os

# List of packages to include in requirements.txt
packages = ["chainlit", "google-generativeai", "langchain_community"]

# Absolute path to pip in the virtual environment
pip_path = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'pip.exe')

# Get the installed packages
installed_packages = subprocess.check_output([pip_path, "freeze"]).decode("utf-8")

# Filter the packages and write to requirements.txt
with open("requirements.txt", "w") as f:
    for package in packages:
        for line in installed_packages.split("\n"):
            if line.startswith(package):
                f.write(line + "\n")
