#!/usr/bin/env python3
"""
YOLO6 Webcam 持續監控腳本
偵測到指定目標時截圖存檔並輸出 JSON 警報。
用法：python webcam_monitor.py [--target person] [--interval 5] [--model yolo26n]
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime


def monitor(target: str = "person", interval: int = 5, model_name: str = "yolo26n"):
    """持續監控 Webcam，偵測到指定目標時輸出警報。"""
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

    # 建立截圖儲存目錄
    save_dir = Path.home() / ".openclaw" / "workspace" / "skills" / "yolo-vision" / "captures"
    save_dir.mkdir(parents=True, exist_ok=True)

    print(json.dumps({
        "status": "monitoring_started",
        "target": target,
        "interval_seconds": interval,
        "model": model_name,
        "message": f"開始監控中，每 {interval} 秒偵測一次，目標：{target}"
    }, ensure_ascii=False), flush=True)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print(json.dumps({"error": "Webcam 讀取失敗，可能已斷線"},
                                 ensure_ascii=False), flush=True)
                break

            # 執行偵測
            results = model(frame, verbose=False)
            result = results[0]
            boxes = result.boxes
            names = result.names

            # 檢查是否偵測到目標
            detected = []
            for box in boxes:
                cls_id = int(box.cls[0])
                label = names[cls_id]
                if label == target:
                    confidence = round(float(box.conf[0]), 2)
                    detected.append({"label": label, "confidence": confidence})

            # 偵測到目標 → 截圖並警報
            if detected:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = save_dir / f"alert_{timestamp}.jpg"

                # 儲存標註後的截圖
                annotated = result.plot()
                cv2.imwrite(str(screenshot_path), annotated)

                alert = {
                    "alert": True,
                    "timestamp": datetime.now().isoformat(),
                    "target": target,
                    "count": len(detected),
                    "details": detected,
                    "screenshot": str(screenshot_path),
                    "message": f"偵測到 {len(detected)} 個 {target}！"
                }
                print(json.dumps(alert, ensure_ascii=False), flush=True)

            # 等待指定間隔
            time.sleep(interval)

    except KeyboardInterrupt:
        print(json.dumps({
            "status": "monitoring_stopped",
            "message": "監控已停止"
        }, ensure_ascii=False), flush=True)
    finally:
        cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO26 Webcam 持續監控")
    parser.add_argument("--target", default="person",
                        help="偵測目標（預設：person）")
    parser.add_argument("--interval", type=int, default=5,
                        help="偵測間隔秒數（預設：5）")
    parser.add_argument("--model", default="yolo26n",
                        choices=["yolo26n", "yolo26s", "yolo26m", "yolo26l"],
                        help="模型大小（預設：yolo26n）")
    args = parser.parse_args()

    monitor(args.target, args.interval, args.model)
