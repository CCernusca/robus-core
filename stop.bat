@echo off
:: Activates the Python virtual environment (if present) and starts starter.py.

set "ROBUS_CORE=%~dp0"
for %%I in ("%ROBUS_CORE%..") do set "PARENT=%%~fI"

set ACTIVATE=
set VENV_PATH=

call :find_venv "%ROBUS_CORE%venv"
call :find_venv "%ROBUS_CORE%env"
call :find_venv "%PARENT%\venv"
call :find_venv "%PARENT%\env"

if defined ACTIVATE (
    echo Activating venv: %VENV_PATH%
    call "%ACTIVATE%"
) else (
    echo No virtual environment found. Checked:
    echo   %ROBUS_CORE%venv
    echo   %ROBUS_CORE%env
    echo   %PARENT%\venv
    echo   %PARENT%\env
    echo Using system Python.
)

python "%ROBUS_CORE%\utils\stop.py"
goto :eof

:find_venv
if defined ACTIVATE goto :eof
set "CHECK_DIR=%~1"
if exist "%CHECK_DIR%\Scripts\activate.bat" (
    set "ACTIVATE=%CHECK_DIR%\Scripts\activate.bat"
    set "VENV_PATH=%CHECK_DIR%"
    goto :eof
)
if exist "%CHECK_DIR%\bin\activate.bat" (
    set "ACTIVATE=%CHECK_DIR%\bin\activate.bat"
    set "VENV_PATH=%CHECK_DIR%"
    goto :eof
)
goto :eof
