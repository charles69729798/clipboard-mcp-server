#!/usr/bin/env python3
"""
Simple Clipboard MCP Server
Win+Shift+S로 캡처한 이미지를 Claude가 바로 분석
+ 특정 창 실시간 캡처 기능
+ Claude 내장 비전으로 한글 텍스트 인식
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image
from PIL import ImageGrab
import pygetwindow as gw
import io

# MCP 서버 생성
mcp = FastMCP("Clipboard Image Server", dependencies=["Pillow", "pygetwindow"])

@mcp.tool()
def paste_clipboard_image() -> Image:
    """
    클립보드의 이미지를 가져옵니다.
    Win+Shift+S나 Ctrl+C로 복사한 이미지를 즉시 분석할 수 있습니다.
    """
    try:
        # 클립보드에서 이미지 가져오기
        img = ImageGrab.grabclipboard()

        if img is None:
            raise ValueError("클립보드에 이미지가 없습니다. Win+Shift+S로 화면을 캡처하거나 이미지를 Ctrl+C로 복사하세요.")

        if isinstance(img, list):
            raise ValueError(f"클립보드에 파일 경로가 있습니다: {img}. 이미지를 직접 복사하세요.")

        # PNG 형식으로 저장
        buffer = io.BytesIO()

        # 이미지 크기가 너무 크면 리사이즈 (4K 해상도까지 허용)
        max_size = 3840  # 4K 해상도
        if img.width > max_size or img.height > max_size:
            ratio = min(max_size / img.width, max_size / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            # LANCZOS: 최고 품질
            from PIL import Image as PILImage
            img = img.resize(new_size, PILImage.Resampling.LANCZOS)

        # compress_level=1로 속도와 품질 균형
        img.save(buffer, format="PNG", optimize=False, compress_level=1)

        return Image(data=buffer.getvalue(), format="png")

    except Exception as e:
        raise RuntimeError(f"클립보드 읽기 실패: {str(e)}")

@mcp.tool()
def list_windows() -> str:
    """
    현재 열려있는 모든 창의 목록을 반환합니다.
    HWP, Excel, 브라우저 등 실행 중인 프로그램의 창을 확인할 수 있습니다.
    """
    try:
        windows = gw.getAllWindows()

        # 의미있는 창만 필터링 (제목이 있고, 보이는 창)
        visible_windows = [
            w for w in windows
            if w.title and w.title.strip() and w.visible
        ]

        if not visible_windows:
            return "열린 창이 없습니다."

        result = ["현재 열린 창 목록:\n"]
        for i, win in enumerate(visible_windows, 1):
            result.append(f"{i}. {win.title}")
            result.append(f"   크기: {win.width}x{win.height}, 위치: ({win.left}, {win.top})")

        return "\n".join(result)

    except Exception as e:
        return f"창 목록 가져오기 실패: {str(e)}"


@mcp.tool()
def capture_window(window_title: str) -> Image:
    """
    특정 창의 스크린샷을 캡처합니다.

    Args:
        window_title: 캡처할 창의 제목 (일부만 입력해도 됨)
                     예: "한글", "Excel", "Chrome", ".hwp"

    Returns:
        캡처된 창의 이미지
    """
    try:
        # 창 찾기 (제목에 window_title이 포함된 창)
        windows = gw.getWindowsWithTitle(window_title)

        if not windows:
            raise ValueError(f"'{window_title}'이 포함된 창을 찾을 수 없습니다. list_windows로 확인하세요.")

        # 첫 번째 매칭된 창 선택
        window = windows[0]

        # 창이 최소화되어 있으면 복원
        if window.isMinimized:
            window.restore()

        # 창을 맨 앞으로
        window.activate()

        # 잠시 대기 (창이 활성화되는 시간)
        import time
        time.sleep(0.2)

        # 창 영역 캡처
        left, top = window.left, window.top
        right, bottom = left + window.width, top + window.height

        img = ImageGrab.grab(bbox=(left, top, right, bottom))

        # PNG 형식으로 저장
        buffer = io.BytesIO()

        # 이미지 크기가 너무 크면 리사이즈 (4K 해상도까지 허용)
        max_size = 3840  # 4K 해상도
        if img.width > max_size or img.height > max_size:
            ratio = min(max_size / img.width, max_size / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            # LANCZOS: 최고 품질
            from PIL import Image as PILImage
            img = img.resize(new_size, PILImage.Resampling.LANCZOS)

        # compress_level=1로 속도와 품질 균형
        img.save(buffer, format="PNG", optimize=False, compress_level=1)

        return Image(data=buffer.getvalue(), format="png")

    except Exception as e:
        raise RuntimeError(f"창 캡처 실패: {str(e)}")


if __name__ == "__main__":
    mcp.run()
