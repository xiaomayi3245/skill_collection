#!/usr/bin/env python3
"""
YOLO6 安裝環境檢查腳本
逐項檢查所有必要條件，回報安裝狀態。
用法：python install_check.py [--webcam]
加上 --webcam 會額外測試攝影機。
"""

import sys
import argparse


def check_python_version():
    """檢查 Python 版本 >= 3.10"""
    v = sys.version_info
    version_str = f"{v.major}.{v.minor}.{v.micro}"
    if v.major >= 3 and v.minor >= 10:
        print(f"  Python 版本：{version_str}")
        return True
    else:
        print(f"  Python 版本：{version_str}（需要 3.10 以上）")
        print("    建議：到 https://www.python.org/ 下載最新版 Python")
        return False


def check_ultralytics():
    """檢查 ultralytics 是否安裝"""
    try:
        import ultralytics
        print(f"  ultralytics 版本：{ultralytics.__version__}")
        return True
    except ImportError:
        print("  ultralytics 未安裝")
        print("    建議：執行 pip install ultralytics")
        return False


def check_yolo_model():
    """檢查 YOLO 模型是否可載入"""
    try:
        from ultralytics import YOLO
        model = YOLO("yolo6n.pt")
        print(f"  YOLO6 模型：yolo6n.pt 可正常載入")
        return True
    except ImportError:
        print("  YOLO 模型：無法載入（ultralytics 未安裝）")
        print("    建議：先安裝 ultralytics")
        return False
    except Exception as e:
        print(f"  YOLO 模型：載入失敗（{e}）")
        print("    建議：檢查網路連線，模型會在首次使用時自動下載")
        return False


def check_opencv():
    """檢查 OpenCV 是否可用"""
    try:
        import cv2
        print(f"  OpenCV 版本：{cv2.__version__}")
        return True
    except ImportError:
        print("  OpenCV 未安裝")
        print("    建議：執行 pip install opencv-python")
        return False


def check_webcam():
    """檢查 Webcam 是否可開啟"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print("  Webcam：正常運作")
                return True
            else:
                print("  Webcam：可開啟但無法讀取畫面")
                print("    建議：檢查攝影機驅動程式")
                return False
        else:
            print("  Webcam：無法開啟")
            print("    建議：確認攝影機已連接，且未被其他程式佔用")
            return False
    except ImportError:
        print("  Webcam：無法檢查（OpenCV 未安裝）")
        return False


def check_gpu():
    """檢查 GPU 是否可用（CUDA）"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"  GPU 加速：可用（{gpu_name}）")
            return True
        else:
            print("  GPU 加速：不可用（將使用 CPU，速度較慢但仍可運作）")
            print("    說明：如有 NVIDIA 顯卡，可安裝 CUDA 版 PyTorch 加速")
            return False
    except ImportError:
        print("  GPU 加速：無法檢查（PyTorch 未安裝）")
        return False


def main(test_webcam: bool = False):
    """執行所有環境檢查。"""
    print("=" * 50)
    print("YOLO6 智慧視覺 — 安裝環境檢查")
    print("=" * 50)

    results = {}

    # 必要檢查項目
    checks = [
        ("Python 版本", check_python_version, True),
        ("ultralytics 套件", check_ultralytics, True),
        ("YOLO 模型", check_yolo_model, True),
        ("OpenCV", check_opencv, True),
        ("GPU 加速（CUDA）", check_gpu, False),
    ]

    if test_webcam:
        checks.append(("Webcam 攝影機", check_webcam, False))

    passed = 0
    failed = 0
    optional_failed = 0

    for name, check_func, required in checks:
        tag = "必要" if required else "選配"
        print(f"\n[{tag}] {name}")
        ok = check_func()
        if ok:
            passed += 1
        elif required:
            failed += 1
        else:
            optional_failed += 1

    # 總結
    print("\n" + "=" * 50)
    print("檢查結果總結")
    print("=" * 50)
    print(f"  通過：{passed} 項")
    if failed > 0:
        print(f"  未通過（必要）：{failed} 項")
    if optional_failed > 0:
        print(f"  未通過（選配）：{optional_failed} 項")

    if failed == 0:
        print("\n所有必要條件都已滿足，可以開始使用 YOLO6 智慧視覺技能！")
    else:
        print("\n有必要條件尚未滿足，請依照上方建議安裝後再試。")

    print("=" * 50)
    return failed == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO6 安裝環境檢查")
    parser.add_argument("--webcam", action="store_true",
                        help="額外測試 Webcam 攝影機")
    args = parser.parse_args()

    ok = main(test_webcam=args.webcam)
    sys.exit(0 if ok else 1)
