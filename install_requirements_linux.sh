#!/bin/bash

# Function to install pipx
install_pipx() {
    if command -v pipx >/dev/null 2>&1; then
        echo "pipx is already installed."
    else
        case "$(lsb_release -is)" in
            Ubuntu|Debian)
                sudo apt update
                sudo apt install -y pipx
                ;;
            Fedora)
                sudo dnf install -y pipx
                ;;
            Arch)
                sudo pacman -S --noconfirm python-pipx
                ;;
            *)
                python3 -m pip install --user pipx
                ;;
        esac
        pipx ensurepath
        sudo pipx ensurepath --global
    fi
}

# Function to install Poetry via pipx
install_poetry() {
    if pipx list | grep -q poetry; then
        echo "Poetry is already installed."
    else
        pipx install poetry
    fi
}

# Install pipx and Poetry
install_pipx
install_poetry

# Install Poetry dependencies
poetry install
if [ $? -ne 0 ]; then
    echo "Failed to install Poetry dependencies."
    read -p "Press any key to exit..."
    exit 1
fi

# Run setup.py
python3 setup.py

# Prevent the terminal from closing
echo "Script execution finished. Press any key to exit."
read -p ""
