#!/usr/bin/env python3
"""
YOLO6 快速測試腳本
拍照或指定照片路徑，跑一次偵測並印出結果。
用法：python detect_test.py [照片路徑]
若不指定照片路徑，會自動用 Webcam 拍一張。
"""

import sys
import json
from pathlib import Path


def quick_test(image_path: str = None):
    """快速測試 YOLO6 偵測功能。"""
    # 如果沒有指定照片，用 Webcam 拍一張
    if image_path is None:
        try:
            import cv2
        except ImportError:
            print("OpenCV 未安裝，請指定照片路徑或執行：pip install opencv-python")
            sys.exit(1)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("無法開啟 Webcam，請改為指定照片路徑：python detect_test.py 照片.jpg")
            sys.exit(1)

        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("Webcam 拍照失敗。")
            sys.exit(1)

        image_path = "test_capture.jpg"
        cv2.imwrite(image_path, frame)
        print(f"已從 Webcam 拍攝測試照片：{image_path}")

    # 呼叫 detect.py 的偵測函式
    from detect import detect
    result = detect(image_path)

    # 印出結果
    print("\n" + "=" * 50)
    print("YOLO6 偵測結果")
    print("=" * 50)

    if "error" in result:
        print(f"錯誤：{result['error']}")
        sys.exit(1)

    print(f"偵測到 {result['total_objects']} 個物件")
    print(f"\n物件統計：")
    for label, count in result["summary"].items():
        print(f"  - {label}: {count} 個")

    if result["output_image"]:
        print(f"\n標註照片已存至：{result['output_image']}")

    print("=" * 50)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    quick_test(path)
