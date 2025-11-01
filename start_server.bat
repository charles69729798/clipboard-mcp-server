@echo off
chcp 65001 > nul
echo ================================
echo Clipboard MCP Server
echo ================================
echo.
echo [INFO] Starting server...
echo [INFO] Press Ctrl+C to stop
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat
python main.py

pause
