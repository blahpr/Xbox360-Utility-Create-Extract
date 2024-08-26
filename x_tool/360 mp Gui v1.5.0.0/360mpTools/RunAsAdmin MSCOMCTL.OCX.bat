@echo off
setlocal

set "file=%~dp0mscomctl.ocx"

if not exist "%file%" (
    echo mscomctl.ocx not found in the current directory.
    pause
    exit /b
)

regsvr32 "%file%"

:end
endlocal
