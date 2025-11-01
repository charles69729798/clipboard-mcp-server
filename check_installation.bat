@echo off
echo ================================================
echo Clipboard MCP Server 설치 상태 확인
echo ================================================
echo.

echo [1/3] Python 버전 확인
.venv\Scripts\python.exe --version
echo.

echo [2/3] 설치된 패키지 확인
.venv\Scripts\pip.exe list | findstr /I "fastmcp pillow pygetwindow"
echo.

echo [3/3] MCP 서버 테스트
echo Python으로 서버 임포트 테스트 중...
.venv\Scripts\python.exe -c "import mcp.server.fastmcp; print('✅ fastmcp 임포트 성공')" 2>nul || echo ❌ fastmcp 설치 필요
.venv\Scripts\python.exe -c "from PIL import ImageGrab; print('✅ Pillow 임포트 성공')" 2>nul || echo ❌ Pillow 설치 필요
.venv\Scripts\python.exe -c "import pygetwindow; print('✅ pygetwindow 임포트 성공')" 2>nul || echo ❌ pygetwindow 설치 필요

echo.
echo ================================================
echo 테스트 완료!
echo ================================================
echo.
echo 모든 패키지가 설치되어 있으면:
echo   - Claude Code를 재시작하세요
echo   - "클립보드 이미지 보여줘" 입력해보세요
echo.
echo 누락된 패키지가 있으면:
echo   - install.bat 실행하세요
echo.
pause
