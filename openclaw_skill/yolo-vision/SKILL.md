---
name: yolo-vision
description: 使用 YOLO26 深度學習模型進行即時物件偵測。可以分析照片中的物件種類與數量、進行 Webcam 即時監控、以及開啟偵測視窗。支援 80 種常見物件（人、車、動物、家具、電子產品等）。
read_when:
  - 幫我看這張照片有什麼
  - 這張照片裡有幾個人
  - 幫我辨識照片中的物品
  - 分析這張圖片
  - 開啟 Webcam 監控
  - 有人經過就通知我
  - 幫我數一下照片裡有幾隻狗
  - 這張照片裡有哪些東西
---

# yolo-vision (影像物件偵測)

使用 YOLO26 深度學習模型進行即時物件偵測。支援 80 種常見物件（人、車、動物、家具、電子產品等）。

## 給 AI 助理的執行指示 (AI Instructions)

1. **環境檢查：** 執行前，請先執行 `python -c "import ultralytics"` 確認套件是否已安裝。若未安裝，請主動詢問使用者是否同意執行 `pip install ultralytics`。
2. **照片處理流程 (照片偵測)：**
   - 當使用者傳送圖片附件時，請先將圖片儲存至 `workspace/temp_yolo_image.jpg`。
   - 然後使用 `exec` 執行：`python scripts/detect.py C:\Users\user\.openclaw\workspace\temp_yolo_image.jpg` (或使用絕對路徑 `C:\Users\user\.openclaw\workspace\skills\yolo-vision\detect.py`)。
   - 讀取輸出的 JSON 結果，將其轉化為口語化回報給使用者。
   - 執行完畢後，刪除暫存的圖片檔案以節省空間。
3. **Webcam 監控處理：**
   - 若使用者要求開啟 Webcam 監控，必須使用 `exec` 並設定 `background: true`（或透過 `process` 工具背景執行），以免阻斷當前的對話。
   - 指令範例：`python C:\Users\user\.openclaw\workspace\skills\yolo-vision\webcam_monitor.py --target person --interval 5`

## 功能列表

- **照片物件偵測**：傳入照片，辨識所有物件並回報種類、數量、位置
- **物件計數**：數出照片中特定物件的數量（例如「有幾個人」）
- **物件分類**：列出照片中所有偵測到的物件類別
- **Webcam 監控**：持續監控攝影機，偵測到指定目標時自動警報

## 執行方式

### 照片偵測
```powershell
python C:\Users\user\.openclaw\workspace\skills\yolo-vision\detect.py "C:\Users\user\.openclaw\workspace\temp_yolo_image.jpg"
```
讀取輸出的 JSON 結果，用口語化方式回報給使用者。
若有標註後的照片（output_image），也一併傳回。

### Webcam 監控
```powershell
# 請確保以背景模式 (background: true) 執行
python C:\Users\user\.openclaw\workspace\skills\yolo-vision\webcam_monitor.py --target person --interval 5
```
偵測到目標時會輸出 JSON 警報，將警報內容通知使用者。

### 可選參數
- `--model`：模型大小（yolo26n / yolo26s / yolo26m / yolo26l），預設 yolo26n（最快）

## 需要的設定
- Python 3.10 或以上
- `pip install ultralytics`（包含 YOLO26 和 OpenCV）
- 模型檔案會在首次執行時自動下載（約 6MB ~ 50MB）