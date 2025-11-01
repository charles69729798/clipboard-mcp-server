"""
클립보드 캡처 테스트 스크립트

사용법:
1. 서버 실행 (start_server.bat)
2. Win+Shift+S로 화면 캡처
3. 이 스크립트 실행
"""

import requests
import base64
from PIL import Image
import io

# 서버 주소
SERVER_URL = "http://localhost:8000"

def test_server():
    """서버 상태 확인"""
    try:
        response = requests.get(f"{SERVER_URL}/")
        print("[OK] Server is running")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"[ERROR] Server is not running: {e}")
        return False

def get_latest_capture():
    """최신 캡처 이미지 가져오기"""
    try:
        response = requests.get(f"{SERVER_URL}/latest")

        if response.status_code == 200:
            data = response.json()
            print(f"\n[OK] Capture found!")
            print(f"Timestamp: {data['timestamp']}")
            print(f"Size: {data['size']}")

            # Base64 디코딩하여 이미지 저장
            img_data = base64.b64decode(data['image'])
            img = Image.open(io.BytesIO(img_data))

            # 테스트 이미지 저장
            output_file = "test_capture.png"
            img.save(output_file)
            print(f"[OK] Image saved to: {output_file}")

            return True
        elif response.status_code == 404:
            print("\n[INFO] No capture found yet")
            print("[INFO] Please capture screen with Win+Shift+S")
            return False
        else:
            print(f"\n[ERROR] Unexpected response: {response.status_code}")
            return False

    except Exception as e:
        print(f"\n[ERROR] Failed to get capture: {e}")
        return False

def check_clipboard():
    """현재 클립보드 상태 확인"""
    try:
        response = requests.get(f"{SERVER_URL}/check")
        data = response.json()

        print("\n[CHECK] Clipboard status:")
        print(f"  Has capture: {data['has_capture']}")
        print(f"  Last timestamp: {data['timestamp']}")
        print(f"  Monitoring: {data['monitoring']}")

    except Exception as e:
        print(f"\n[ERROR] Failed to check: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Clipboard MCP Server - Test Script")
    print("=" * 50)

    # 1. 서버 상태 확인
    if not test_server():
        print("\n[ERROR] Please start server first:")
        print("  > start_server.bat")
        exit(1)

    # 2. 클립보드 상태 확인
    check_clipboard()

    # 3. 최신 캡처 가져오기
    print("\n" + "=" * 50)
    print("Fetching latest capture...")
    print("=" * 50)

    if get_latest_capture():
        print("\n[SUCCESS] Test completed!")
    else:
        print("\n[INFO] Capture screen and run this script again")
