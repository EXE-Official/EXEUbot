@echo off

:: Check if the virtual enviroment exist
if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
)

:: Start EXEUbot.py using Python
python EXEUbot.py

pause
