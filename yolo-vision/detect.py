#!/usr/bin/env python3
"""
YOLO26 照片物件偵測腳本
用法：python detect.py <照片路徑> [--model yolo26n.pt]
輸出：JSON 格式的偵測結果
"""

import sys
import json
import argparse
from pathlib import Path


def detect(image_path: str, model_name: str = "yolo26n") -> dict:
    """對指定照片執行 YOLO26 物件偵測，回傳結構化結果。"""
    # 檢查檔案是否存在
    img = Path(image_path)
    if not img.exists():
        return {"error": f"找不到檔案：{image_path}"}

    # 載入模型（首次會自動下載）
    try:
        from ultralytics import YOLO
        model = YOLO(f"{model_name}.pt")
    except ImportError:
        return {"error": "ultralytics 未安裝，請執行：pip install ultralytics"}
    except Exception as e:
        return {"error": f"模型載入失敗：{e}"}

    # 執行偵測
    try:
        results = model(str(img), verbose=False)
    except Exception as e:
        return {"error": f"偵測過程發生錯誤：{e}"}

    # 解析結果
    result = results[0]
    boxes = result.boxes
    names = result.names

    # 統計每種物件的數量
    summary = {}
    details = []
    for box in boxes:
        cls_id = int(box.cls[0])
        label = names[cls_id]
        confidence = round(float(box.conf[0]), 2)
        x1, y1, x2, y2 = [round(float(v), 1) for v in box.xyxy[0]]
        summary[label] = summary.get(label, 0) + 1
        details.append({
            "label": label,
            "confidence": confidence,
            "bbox": [x1, y1, x2, y2]
        })

    # 儲存標註後的照片
    output_path = img.parent / f"{img.stem}_detected{img.suffix}"
    try:
        annotated = result.plot()
        import cv2
        cv2.imwrite(str(output_path), annotated)
    except Exception:
        output_path = None

    return {
        "total_objects": len(details),
        "summary": summary,
        "details": details,
        "output_image": str(output_path) if output_path else None
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO26 照片物件偵測")
    parser.add_argument("image", help="照片檔案路徑")
    parser.add_argument("--model", default="yolo26n",
                        choices=["yolo26n", "yolo26s", "yolo26m", "yolo26l"],
                        help="模型大小（預設：yolo26n，最快）")
    args = parser.parse_args()

    result = detect(args.image, args.model)
    print(json.dumps(result, ensure_ascii=False, indent=2))
