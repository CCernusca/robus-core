@echo off
:: Configures Windows Task Scheduler to run starter.py at user logon.

set TASK_NAME=RobusNodeStarter
set STARTER=%~dp0..\utils\starter.py

schtasks /create /tn "%TASK_NAME%" /tr "python \"%STARTER%\"" /sc onlogon /f

if %errorlevel% == 0 (
    echo Startup task "%TASK_NAME%" created. starter.py will launch at next logon.
) else (
    echo Failed to create startup task. Try running as Administrator.
)

pause
