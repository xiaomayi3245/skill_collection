# YOLO6 智慧視覺技能 (yolo-vision)

讓龍蝦擁有 YOLO6 即時物件偵測能力——傳照片就能數人頭、辨識物品。

## 安裝步驟

### 第一步：安裝 Python 和 YOLO6

（Windows 用 PowerShell，Mac/Linux 用終端機）

1. 確認 Python 3.10+：

```powershell
python --version
```

2. 安裝 YOLO6：

```powershell
pip install ultralytics
```

3. 驗證安裝：

```powershell
python -c "from ultralytics import YOLO; print('OK')"
```

### 第二步：安裝到龍蝦

**方式一：複製資料夾（推薦）**

把整個 `yolo-vision` 資料夾複製到 `~/.openclaw/workspace/skills/`

```powershell
cp -r yolo-vision ~/.openclaw/workspace/skills/
```

**方式二：手動建立**

```powershell
mkdir ~/.openclaw/workspace/skills/yolo-vision
```

然後把裡面的檔案都複製進去。

### 第三步：重啟龍蝦

```powershell
openclaw gateway restart
```

### 第四步：測試

傳任意一張照片到 LINE，說「幫我分析這張照片有什麼」

## 常見問題

**Q: python 指令找不到？**
A: Windows 試試 `python3` 或到 [python.org](https://www.python.org/) 重新安裝，記得勾選「Add to PATH」

**Q: pip install 報錯？**
A: 試試 `python -m pip install ultralytics`

**Q: 偵測結果不準？**
A: 確保照片光線充足，物件不要太小。也可以換更大的模型：把 `detect.py` 裡的 `yolo6n` 改成 `yolo6s`

## 檔案說明

| 檔案 | 用途 |
|------|------|
| `SKILL.md` | 技能定義（龍蝦讀這個來了解技能） |
| `detect.py` | 照片偵測腳本 |
| `webcam_monitor.py` | Webcam 監控腳本 |
| `live_detect.py` | 即時偵測視窗腳本 |
| `detect_test.py` | 快速測試腳本 |
| `install_check.py` | 安裝環境檢查腳本 |
