#!/usr/bin/env python3
"""
EasyOCR 모델을 미리 다운로드하는 스크립트
"""
import sys
import time

print("EasyOCR 모델 다운로드 시작...")
print("=" * 50)

try:
    print("[1/3] EasyOCR 임포트 중...")
    import easyocr

    print("[2/3] 한국어 + 영어 OCR Reader 초기화 중...")
    print("      (모델 다운로드 시작 - 약 250MB)")
    print("      진행 상황 표시는 비활성화됨 (인코딩 문제)")
    print("      다운로드 중... 3-5분 소요 예상")
    start_time = time.time()

    # 이 부분에서 모델이 자동으로 다운로드됨
    reader = easyocr.Reader(['ko', 'en'], gpu=False, verbose=False)

    elapsed = time.time() - start_time
    print(f"\n[3/3] 완료! (소요 시간: {elapsed:.1f}초)")
    print("=" * 50)
    print("✓ 모델 다운로드 및 초기화 성공")
    print("✓ 이제 OCR을 빠르게 사용할 수 있습니다")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
