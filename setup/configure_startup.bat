@echo off
set TASK_NAME=RobusNodeStarter
set STARTER="%~dp0..\setup\start.bat"

schtasks /create ^
 /tn "%TASK_NAME%" ^
 /tr "cmd /c \"cd /d %STARTER%\"" ^
 /sc onlogon /f

if %errorlevel% == 0 (
    echo Startup task "%TASK_NAME%" created.
) else (
    echo Failed to create startup task. Try running as Administrator.
)

pause
