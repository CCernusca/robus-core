@echo off
:: Activates the Python virtual environment (if present) and starts starter.py.

set ROBUS_CORE=%~dp0..

if exist "%ROBUS_CORE%\venv\Scripts\activate.bat" (
    echo Activating venv...
    call "%ROBUS_CORE%\venv\Scripts\activate.bat"
) else if exist "%ROBUS_CORE%\env\Scripts\activate.bat" (
    echo Activating env...
    call "%ROBUS_CORE%\env\Scripts\activate.bat"
) else (
    echo No virtual environment found, using system Python.
)

python "%ROBUS_CORE%\utils\starter.py"
