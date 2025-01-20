@echo off

:: Run Python script to check and download libtorch if needed
python3 scripts/check_libtorch.py

:: Call premake to generate Visual Studio project files
call vendor\bin\premake\premake5.exe vs2022

:: Pause to keep the window open
PAUSE
