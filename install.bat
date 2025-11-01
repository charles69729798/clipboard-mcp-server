@echo off
echo ================================================
echo Clipboard MCP Server 설치 스크립트
echo ================================================
echo.

:: 가상환경 확인 및 생성
if not exist ".venv" (
    echo [1/3] 가상환경 생성 중...
    python -m venv .venv
) else (
    echo [1/3] 가상환경이 이미 존재합니다.
)

:: 가상환경 활성화 및 패키지 설치
echo.
echo [2/3] 패키지 설치 중...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install -r requirements.txt

:: pygetwindow 추가 설치 (README에는 없지만 코드에서 사용)
.venv\Scripts\pip.exe install pygetwindow

:: fastmcp 설치
.venv\Scripts\pip.exe install fastmcp

echo.
echo [3/3] 설치 완료!
echo.
echo ================================================
echo 다음 단계:
echo 1. Claude Code 설정 파일 업데이트 필요
echo 2. setup_claude_config.bat 실행
echo ================================================
pause
