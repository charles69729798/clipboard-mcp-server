# 📋 Clipboard MCP Server

**Win+Shift+S**로 캡처한 화면을 Claude Code가 즉시 인식하게 해주는 MCP 서버

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 주요 기능

- 🖼️ **클립보드 이미지 자동 인식**: Win+Shift+S로 캡처하면 Claude가 바로 분석
- 🪟 **창 캡처**: 현재 열린 특정 창(HWP, Excel 등)을 직접 캡처
- 📝 **한글 인식 최적화**: PNG 무손실 포맷으로 텍스트 인식률 향상
- 🚀 **간편한 사용**: 별도 저장 없이 캡처하자마자 Claude와 대화

## 🎯 사용 시나리오

```
1. HWP 파일에서 수학식 보는 중
2. Win+Shift+S로 영역 드래그 캡처
3. Claude Code: "클립보드 이미지 보여줘"
4. ✅ Claude가 즉시 수식 분석 & LaTeX 변환!
```

## 📦 설치

### 1. 리포지토리 클론

```bash
git clone https://github.com/charles69729798/clipboard-mcp-server.git
cd clipboard-mcp-server
```

### 2. 가상환경 생성 및 패키지 설치

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Claude Code 설정

`C:\Users\YOUR_USERNAME\.claude.json` 파일에 다음 추가:

```json
{
  "mcpServers": {
    "clipboard-image": {
      "type": "stdio",
      "command": "C:\\clipboard-mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\clipboard-mcp-server\\clipboard_mcp.py"
      ],
      "env": {}
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "clipboard-image": {
      "type": "stdio",
      "command": "/path/to/clipboard-mcp-server/.venv/bin/python",
      "args": [
        "/path/to/clipboard-mcp-server/clipboard_mcp.py"
      ],
      "env": {}
    }
  }
}
```

### 4. Claude Code 재시작

설정 후 Claude Code를 재시작하면 자동으로 MCP 서버가 로드됩니다.

## 💡 사용 방법

### 📸 클립보드 이미지 분석

```
1. Win+Shift+S (Windows) 또는 Cmd+Shift+4 (Mac)로 화면 캡처
2. Claude Code에서 "클립보드 이미지 보여줘" 입력
3. Claude가 즉시 이미지 분석!
```

### 🪟 특정 창 캡처하기

```
# 1단계: 열린 창 목록 확인
사용자: "현재 열린 창 목록 보여줘"
Claude: [list_windows 도구 사용]
  1. 문서1.hwp - 한글
  2. 예산.xlsx - Excel
  3. Chrome - Google
  ...

# 2단계: 원하는 창 캡처
사용자: "한글 창 캡처해줘"
Claude: [capture_window 도구 사용하여 HWP 창 캡처 및 분석]
```

## 🛠️ 제공 도구

### 1. `paste_clipboard_image()`
클립보드의 이미지를 가져와 Claude가 분석할 수 있게 합니다.

**사용 예시:**
- "클립보드 이미지 분석해줘"
- "방금 캡처한 수식 LaTeX로 변환해줘"
- "이미지 속 텍스트 추출해줘"

### 2. `list_windows()`
현재 열려있는 모든 창의 목록을 반환합니다.

**반환 정보:**
- 창 제목
- 크기 (width x height)
- 위치 (x, y)

### 3. `capture_window(window_title)`
특정 창을 찾아서 스크린샷을 캡처합니다.

**매개변수:**
- `window_title`: 창 제목의 일부 (예: "한글", "Excel", ".hwp")

**예시:**
```python
capture_window("한글")      # "한글"이 포함된 창 캡처
capture_window(".hwp")      # .hwp 확장자 파일이 열린 창 캡처
capture_window("Excel")     # Excel 창 캡처
```

## 📋 실제 사용 사례

### 예시 1: 수학 문제 풀이

```
사용자: [수식 캡처] "이 미분방정식 풀어줘"
Claude: [이미지 분석]
  "dy/dx + 2y = e^x

  이것은 1차 선형 미분방정식입니다.
  풀이:
  1. 적분인자: μ(x) = e^(2x)
  2. 일반해: y = (e^x)/3 + Ce^(-2x)
  ..."
```

### 예시 2: 표 데이터 추출

```
사용자: [Excel 표 캡처] "이 표를 마크다운으로 변환해줘"
Claude: [변환 결과 제공]
```

### 예시 3: 실시간 문서 검토

```
사용자: "한글 문서 열린 창 캡처해서 오타 찾아줘"
Claude: [HWP 창 캡처 후 텍스트 분석 및 오타 지적]
```

## 🔧 기술 스택

- **FastMCP**: MCP (Model Context Protocol) 서버 프레임워크
- **Pillow (PIL)**: 이미지 처리 및 클립보드 접근
- **pygetwindow**: Windows 창 관리
- **Python 3.8+**

## 📝 작동 원리

```
┌──────────────┐
│   사용자      │
│ Win+Shift+S  │  → 화면 드래그 캡처
└──────────────┘
       ↓
┌──────────────┐
│   Windows    │
│  Clipboard   │  ← 자동으로 이미지 저장
└──────────────┘
       ↓
┌──────────────┐
│  MCP Server  │
│ (clipboard_  │  ← ImageGrab.grabclipboard()
│  mcp.py)     │
└──────────────┘
       ↓
┌──────────────┐
│ Claude Code  │  ← paste_clipboard_image() 호출
└──────────────┘
       ↓
   이미지 분석!
```

## ⚙️ 고급 설정

### 이미지 크기 제한 변경

`clipboard_mcp.py` 파일의 37번째 줄에서 조정:

```python
max_size = 2048  # 기본값: 2048px (Claude 제한 고려)
```

### 리샘플링 방법 변경

고품질 이미지가 필요한 경우 41번째 줄:

```python
img = img.resize(new_size, Image.Resampling.LANCZOS)  # LANCZOS 권장
```

## 🐛 문제 해결

### MCP 서버가 로드되지 않을 때

```bash
# .claude.json 파일 경로 확인
# Windows: C:\Users\YOUR_USERNAME\.claude.json
# macOS: ~/.claude.json

# 절대 경로가 정확한지 확인
# 경로에 한글이 있으면 이스케이프 처리 필요
```

### 클립보드 이미지가 인식되지 않을 때

```python
# test_clipboard.py 실행하여 확인
python test_clipboard.py

# 출력 예상:
# "Test image copied to clipboard!"
# "Successfully read back image: (400, 200)"
```

### 창 캡처가 작동하지 않을 때

- 캡처하려는 창이 최소화되어 있지 않은지 확인
- 관리자 권한으로 실행 중인 프로그램은 캡처가 제한될 수 있음
- `list_windows()`로 정확한 창 제목 확인 후 사용

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

## 🙏 감사

- [Anthropic Claude](https://www.anthropic.com/claude) - AI 어시스턴트
- [FastMCP](https://github.com/anthropics/fastmcp) - MCP 서버 프레임워크
- [Pillow](https://python-pillow.org/) - 이미지 처리 라이브러리

## 📞 문의

문제가 있거나 제안사항이 있으면 [Issues](https://github.com/charles69729798/clipboard-mcp-server/issues)에 등록해주세요!

---

⭐ 도움이 되셨다면 Star를 눌러주세요!
