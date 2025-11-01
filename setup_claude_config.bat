@echo off
setlocal enabledelayedexpansion
echo ================================================
echo Claude Code 설정 자동 업데이트
echo ================================================
echo.

:: 현재 디렉토리 경로 가져오기
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

:: Python 경로 설정
set "PYTHON_PATH=%CURRENT_DIR%\.venv\Scripts\python.exe"
set "SCRIPT_PATH=%CURRENT_DIR%\clipboard_mcp.py"

:: 경로에서 백슬래시를 JSON용 이중 백슬래시로 변환
set "JSON_PYTHON_PATH=%PYTHON_PATH:\=\\%"
set "JSON_SCRIPT_PATH=%SCRIPT_PATH:\=\\%"

:: Claude 설정 파일 경로
set "CLAUDE_CONFIG=%USERPROFILE%\.claude.json"

echo 현재 경로: %CURRENT_DIR%
echo Python: %PYTHON_PATH%
echo Script: %SCRIPT_PATH%
echo.
echo Claude 설정 파일: %CLAUDE_CONFIG%
echo.

:: 설정 파일이 없으면 생성
if not exist "%CLAUDE_CONFIG%" (
    echo Claude 설정 파일이 없습니다. 새로 생성합니다...
    (
        echo {
        echo   "mcpServers": {
        echo     "clipboard-image": {
        echo       "type": "stdio",
        echo       "command": "%JSON_PYTHON_PATH%",
        echo       "args": [
        echo         "%JSON_SCRIPT_PATH%"
        echo       ],
        echo       "env": {}
        echo     }
        echo   }
        echo }
    ) > "%CLAUDE_CONFIG%"
    echo.
    echo ✅ 설정 파일이 생성되었습니다!
) else (
    echo.
    echo ⚠️  설정 파일이 이미 존재합니다.
    echo.
    echo 다음 내용을 %CLAUDE_CONFIG% 파일에 추가하세요:
    echo.
    echo "clipboard-image": {
    echo   "type": "stdio",
    echo   "command": "%JSON_PYTHON_PATH%",
    echo   "args": [
    echo     "%JSON_SCRIPT_PATH%"
    echo   ],
    echo   "env": {}
    echo }
    echo.
)

echo.
echo ================================================
echo 설정 완료!
echo Claude Code를 재시작하세요.
echo ================================================
pause
