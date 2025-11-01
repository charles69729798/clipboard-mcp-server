"""
Clipboard Monitoring MCP Server
Win+Shift+S로 캡처한 이미지를 Claude Code가 자동으로 인식하게 해주는 서버
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from PIL import ImageGrab, Image
import base64
import io
from datetime import datetime
import threading
import time

app = FastAPI(title="Clipboard MCP Server")

# 최신 캡처 저장
latest_capture = {
    "image": None,
    "timestamp": None,
    "format": "png"
}

# 클립보드 모니터링 상태
monitoring = {"running": False, "last_hash": None}


def clipboard_monitor():
    """백그라운드에서 클립보드 모니터링"""
    print("[INFO] Clipboard monitoring started...")

    while monitoring["running"]:
        try:
            img = ImageGrab.grabclipboard()

            if img and isinstance(img, Image.Image):
                # 이미지 해시로 중복 체크
                current_hash = hash(img.tobytes())

                if current_hash != monitoring["last_hash"]:
                    # 새 이미지 감지!
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()

                    latest_capture["image"] = img_base64
                    latest_capture["timestamp"] = datetime.now().isoformat()
                    latest_capture["size"] = img.size

                    monitoring["last_hash"] = current_hash

                    print(f"[OK] New capture detected! ({img.size[0]}x{img.size[1]}) - {latest_capture['timestamp']}")

        except Exception as e:
            # 클립보드가 비어있거나 이미지가 아닐 경우
            pass

        time.sleep(0.3)  # 0.3초마다 체크


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 클립보드 모니터링 시작"""
    monitoring["running"] = True
    thread = threading.Thread(target=clipboard_monitor, daemon=True)
    thread.start()
    print("[START] Clipboard MCP Server started!")
    print("[INFO] Press Win+Shift+S to capture screen")


@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 모니터링 중지"""
    monitoring["running"] = False
    print("[STOP] Server shutdown")


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "status": "running",
        "service": "Clipboard MCP Server",
        "has_capture": latest_capture["image"] is not None,
        "last_capture": latest_capture["timestamp"]
    }


@app.get("/latest")
async def get_latest_capture():
    """
    최신 캡처 이미지 가져오기

    Returns:
        - image: base64 인코딩된 PNG 이미지
        - timestamp: 캡처 시각
        - size: [width, height]
    """
    if latest_capture["image"] is None:
        raise HTTPException(
            status_code=404,
            detail="캡처된 이미지가 없습니다. Win+Shift+S로 화면을 캡처하세요."
        )

    return JSONResponse({
        "status": "ok",
        "image": latest_capture["image"],
        "timestamp": latest_capture["timestamp"],
        "size": latest_capture["size"],
        "format": "png"
    })


@app.get("/check")
async def check_clipboard():
    """
    현재 클립보드 상태 확인 (이미지 가져오지 않음)
    """
    return {
        "has_capture": latest_capture["image"] is not None,
        "timestamp": latest_capture["timestamp"],
        "monitoring": monitoring["running"]
    }


@app.delete("/clear")
async def clear_capture():
    """저장된 캡처 삭제"""
    latest_capture["image"] = None
    latest_capture["timestamp"] = None
    monitoring["last_hash"] = None

    return {"status": "cleared"}


@app.get("/clipboard-now")
async def get_clipboard_now():
    """
    현재 클립보드의 이미지를 즉시 가져오기 (모니터링과 별개)
    """
    try:
        img = ImageGrab.grabclipboard()

        if img and isinstance(img, Image.Image):
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            return {
                "status": "ok",
                "image": img_base64,
                "size": img.size,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=404,
                detail="클립보드에 이미지가 없습니다"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
