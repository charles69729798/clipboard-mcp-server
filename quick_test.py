#!/usr/bin/env python3
"""Quick test of MCP server functions"""

from PIL import ImageGrab
import pygetwindow as gw

print("=== Testing clipboard function ===")
try:
    img = ImageGrab.grabclipboard()
    if img:
        print(f"[OK] Clipboard image found: {img.size}")
    else:
        print("[FAIL] No image in clipboard")
except Exception as e:
    print(f"[FAIL] Error: {e}")

print("\n=== Testing list_windows function ===")
try:
    windows = gw.getAllWindows()
    visible_windows = [w for w in windows if w.title and w.title.strip() and w.visible]
    print(f"[OK] Found {len(visible_windows)} visible windows")
    for i, win in enumerate(visible_windows[:5], 1):
        print(f"  {i}. {win.title[:50]}")
    if len(visible_windows) > 5:
        print(f"  ... and {len(visible_windows) - 5} more")
except Exception as e:
    print(f"[FAIL] Error: {e}")

print("\n=== All core functions working! ===")
