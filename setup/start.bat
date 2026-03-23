@echo off
:: Activates the Python virtual environment (if present) and starts starter.py.

set ROBUS_CORE=%~dp0..
for %%I in ("%ROBUS_CORE%") do set PARENT=%%~dpI

if exist "%ROBUS_CORE%\venv\Scripts\activate.bat" (
    echo Activating venv...
    call "%ROBUS_CORE%\venv\Scripts\activate.bat"
) else if exist "%ROBUS_CORE%\env\Scripts\activate.bat" (
    echo Activating env...
    call "%ROBUS_CORE%\env\Scripts\activate.bat"
) else if exist "%PARENT%\venv\Scripts\activate.bat" (
    echo Activating venv from parent directory...
    call "%PARENT%\venv\Scripts\activate.bat"
) else if exist "%PARENT%\env\Scripts\activate.bat" (
    echo Activating env from parent directory...
    call "%PARENT%\env\Scripts\activate.bat"
) else (
    echo No virtual environment found, using system Python.
)

python "%ROBUS_CORE%\utils\starter.py"
