#!/usr/bin/env python3
"""
Clipboard MCP Server 자동 설치 스크립트
이 스크립트 하나만 실행하면 모든 설치가 완료됩니다.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def print_step(step, message):
    """단계별 메시지 출력"""
    print(f"\n{'='*60}")
    print(f"[{step}] {message}")
    print('='*60)

def run_command(cmd, description):
    """명령어 실행"""
    print(f"\n실행 중: {description}")
    print(f"명령어: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 오류 발생:\n{result.stderr}")
        return False
    print(f"✅ 완료: {description}")
    return True

def main():
    print("="*60)
    print("  📋 Clipboard MCP Server 자동 설치")
    print("="*60)
    
    # 1. 현재 경로 확인
    script_dir = Path(__file__).parent.absolute()
    venv_dir = script_dir / ".venv"
    
    print(f"\n작업 경로: {script_dir}")
    
    # 2. 가상환경 생성
    print_step("1/4", "가상환경 생성")
    if venv_dir.exists():
        print("✅ 가상환경이 이미 존재합니다.")
    else:
        if not run_command([sys.executable, "-m", "venv", str(venv_dir)], 
                          "가상환경 생성"):
            print("\n❌ 설치 실패: 가상환경을 생성할 수 없습니다.")
            return False
    
    # 3. pip 업그레이드
    print_step("2/4", "pip 업그레이드")
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    if not run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
                      "pip 업그레이드"):
        print("\n⚠️ pip 업그레이드 실패 (계속 진행)")
    
    # 4. 패키지 설치
    print_step("3/4", "필수 패키지 설치")
    packages = [
        "fastmcp>=0.1.0",
        "pillow>=10.0.0",
        "pygetwindow>=0.0.9",
    ]
    
    for package in packages:
        if not run_command([str(pip_exe), "install", package],
                          f"{package} 설치"):
            print(f"\n❌ 설치 실패: {package}")
            return False
    
    # 5. Claude Code 설정
    print_step("4/4", "Claude Code 설정")
    
    if sys.platform == "win32":
        claude_config = Path.home() / ".claude.json"
        python_path = str(python_exe).replace("\\", "\\\\")
        script_path = str(script_dir / "clipboard_mcp.py").replace("\\", "\\\\")
    else:
        claude_config = Path.home() / ".claude.json"
        python_path = str(python_exe)
        script_path = str(script_dir / "clipboard_mcp.py")
    
    mcp_config = {
        "clipboard-image": {
            "type": "stdio",
            "command": python_path,
            "args": [script_path],
            "env": {}
        }
    }
    
    # 기존 설정 파일 읽기 또는 새로 생성
    if claude_config.exists():
        try:
            with open(claude_config, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            if "mcpServers" not in config:
                config["mcpServers"] = {}
            
            config["mcpServers"]["clipboard-image"] = mcp_config["clipboard-image"]
            
            with open(claude_config, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ 기존 설정 파일 업데이트: {claude_config}")
        except Exception as e:
            print(f"⚠️ 설정 파일 업데이트 실패: {e}")
            print(f"\n다음 내용을 {claude_config}에 수동으로 추가하세요:")
            print(json.dumps({"mcpServers": mcp_config}, indent=2))
    else:
        try:
            config = {"mcpServers": mcp_config}
            with open(claude_config, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            print(f"✅ 새 설정 파일 생성: {claude_config}")
        except Exception as e:
            print(f"⚠️ 설정 파일 생성 실패: {e}")
            print(f"\n다음 내용으로 {claude_config}를 생성하세요:")
            print(json.dumps(config, indent=2))
    
    # 설치 완료
    print("\n" + "="*60)
    print("  ✅ 설치 완료!")
    print("="*60)
    print("\n다음 단계:")
    print("1. Claude Code를 완전히 종료하세요 (작업 관리자에서도 확인)")
    print("2. Claude Code를 다시 실행하세요")
    print("3. '클립보드 이미지 보여줘' 또는 '현재 열린 창 목록 보여줘'를 입력해보세요")
    print("\n🎉 작동하면 성공입니다!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        input("\n아무 키나 눌러 종료...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n사용자가 취소했습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        input("\n아무 키나 눌러 종료...")
        sys.exit(1)
