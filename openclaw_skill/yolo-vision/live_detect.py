#!/usr/bin/env python3
"""
YOLO6 即時偵測視窗腳本
開啟 Webcam 即時偵測並在視窗中顯示標註結果。
用法：python live_detect.py [--model yolo26n]
按 Q 鍵退出。
"""

import sys
import json
import time
import argparse


def live_detect(model_name: str = "yolo26n"):
    """開啟 Webcam 即時偵測視窗，每一幀都標註偵測結果。"""
    # 載入模型
    try:
        from ultralytics import YOLO
        model = YOLO(f"{model_name}.pt")
    except ImportError:
        print(json.dumps({"error": "ultralytics 未安裝，請執行：pip install ultralytics"},
                         ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"模型載入失敗：{e}"}, ensure_ascii=False))
        sys.exit(1)

    # 開啟 Webcam
    try:
        import cv2
    except ImportError:
        print(json.dumps({"error": "OpenCV 未安裝，請執行：pip install opencv-python"},
                         ensure_ascii=False))
        sys.exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(json.dumps({"error": "無法開啟 Webcam，請確認攝影機已連接"},
                         ensure_ascii=False))
        sys.exit(1)

    print("YOLO26 即時偵測已啟動，按 Q 鍵退出...")
    prev_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Webcam 讀取失敗，結束偵測。")
                break

            # 執行偵測並取得標註畫面
            results = model(frame, verbose=False)
            annotated = results[0].plot()

            # 計算並顯示 FPS
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time
            cv2.putText(annotated, f"FPS: {fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 顯示視窗
            cv2.imshow("YOLO26 Live Detection", annotated)

            # 按 Q 退出
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("即時偵測已結束。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO26 即時偵測視窗")
    parser.add_argument("--model", default="yolo26n",
                        choices=["yolo26n", "yolo26s", "yolo26m", "yolo26l"],
                        help="模型大小（預設：yolo26n）")
    args = parser.parse_args()

    live_detect(args.model)
