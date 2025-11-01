# 🚀 빠른 설치 가이드

## 간단 3단계 설치

### 1단계: 패키지 설치
```
install.bat 더블클릭
```
- 가상환경 생성
- 필요한 Python 패키지 자동 설치

### 2단계: Claude Code 설정
```
setup_claude_config.bat 더블클릭
```
- Claude Code 설정 파일 자동 업데이트
- 또는 수동으로 설정 추가

### 3단계: Claude Code 재시작
- Claude Code 완전히 종료 후 재실행
- MCP 서버 자동 로드됨

---

## ✅ 설치 확인

Claude Code에서 다음을 입력해보세요:
```
클립보드 이미지 보여줘
```

작동하면 성공! 🎉

---

## 🎯 사용 예시

### 1. 화면 캡처 후 분석
```
1. Win+Shift+S로 화면 캡처
2. "클립보드 이미지 보여줘"
3. Claude가 즉시 분석!
```

### 2. 특정 창 캡처
```
"현재 열린 창 목록 보여줘"
"한글 창 캡처해줘"
"Excel 창 캡처해서 표 추출해줘"
```

---

## 🔧 문제 해결

### MCP 서버가 로드되지 않을 때
1. Claude Code 완전히 종료 (작업 관리자에서도 확인)
2. `.claude.json` 파일 경로 확인:
   - Windows: `C:\Users\사용자명\.claude.json`
3. 경로에 백슬래시가 두 개씩인지 확인 (`\\`)
4. Claude Code 재시작

### 클립보드 이미지가 인식 안 될 때
- Win+Shift+S로 다시 캡처
- 이미지를 직접 복사했는지 확인 (파일 경로 복사 X)

### Python 오류가 날 때
```
.venv\Scripts\python.exe --version
```
Python 3.8 이상인지 확인

---

## 📞 더 자세한 정보
`README.md` 파일 참조
