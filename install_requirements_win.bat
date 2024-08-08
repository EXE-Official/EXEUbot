@echo off

:: Install Scoop
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
powershell -Command "Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression"
if %errorlevel% neq 0 (
    echo Scoop is already installed or there was an error during installation.
) else (
    echo Scoop installed successfully.
)

:: Install pipx via Scoop
scoop install pipx
pipx ensurepath
if %errorlevel% neq 0 (
    echo pipx is already installed or there was an error during installation.
) else (
    echo pipx installed successfully.
)

:: Install Poetry via pipx
pipx install poetry
if %errorlevel% neq 0 (
    echo Poetry is already installed or there was an error during installation.
) else (
    echo Poetry installed successfully.
)

:: Install Poetry dependencies
poetry install
if %errorlevel% neq 0 (
    echo Failed to install Poetry dependencies.
    pause
    exit /b %errorlevel%
)

:: Run setup.py
python setup.py

:: Prevent the terminal from closing
echo Script execution finished. Press any key to exit.
pause /k
