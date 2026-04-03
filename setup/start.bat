@echo off
:: Activates the Python virtual environment (if present) and starts starter.py.

set ROBUS_CORE=%~dp0..
for %%I in ("%ROBUS_CORE%") do set PARENT=%%~dpI

set ACTIVATE=
set VENV_PATH=

call :find_venv "%ROBUS_CORE%\venv"
call :find_venv "%ROBUS_CORE%\env"
call :find_venv "%PARENT%venv"
call :find_venv "%PARENT%env"

if defined ACTIVATE (
    echo Activating venv: %VENV_PATH%
    call "%ACTIVATE%"
) else (
    echo No virtual environment found. Checked:
    echo   %ROBUS_CORE%\venv
    echo   %ROBUS_CORE%\env
    echo   %PARENT%venv
    echo   %PARENT%env
    echo Using system Python.
)

:: Run Redis setup script if present
set SETUP_SCRIPT=%ROBUS_CORE%\setup\setup_redis.bat
if exist "%SETUP_SCRIPT%" (
    echo Running Redis setup: %SETUP_SCRIPT%
    call "%SETUP_SCRIPT%"
) else (
    echo No setup_redis.bat found at %SETUP_SCRIPT%
)

python "%ROBUS_CORE%\utils\starter.py"
goto :eof

:find_venv
if defined ACTIVATE goto :eof
if exist "%~1\Scripts\activate.bat" (
    set ACTIVATE=%~1\Scripts\activate.bat
    set VENV_PATH=%~1
    goto :eof
)
if exist "%~1\bin\activate.bat" (
    set ACTIVATE=%~1\bin\activate.bat
    set VENV_PATH=%~1
    goto :eof
)
goto :eof
