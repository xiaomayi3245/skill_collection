---
name: disk-audit
description: Windows 磁碟常態盤點/整理：掃描指定資料夾的大檔、重複檔、最近修改檔；產生報告並可選擇性整理到歸檔資料夾（預設只讀、不刪檔）。
read_when:
  - 使用者要求清理磁碟空間或找出大檔案
  - 盤點硬碟容量或整理特定資料夾
  - 尋找重複檔案
---

# Disk Audit（磁碟盤點/整理）

目標：在 Windows 主機上定期盤點檔案（容量、最近修改、類型分佈、重複檔候選），並在**確認**後做「整理/歸檔」（預設不刪檔）。

## 給 AI 助理的指示 (AI Instructions)
1. **主動詢問設定：** 若使用者未提供以下「4 個設定」，請在執行 `scripts/scan.ps1` 之前，先主動詢問使用者要掃描哪個目錄、大檔門檻為何。
2. **動態生成整理腳本：** 目前目錄下僅有 `scan.ps1`。若使用者決定要執行歸檔、整理或移動檔案，AI 應根據使用者的規則，動態生成 PowerShell 腳本或建立 `scripts/organize.ps1` 來完成操作，且必須遵守下方的安全原則。

## 安全原則（很重要）
- 預設只做 **掃描 + 產生報告**。
- **不刪檔**。需要刪除時，一律改為移到回收桶或移到 quarantine 資料夾，且要二次確認。
- 掃描範圍必須明確：避免掃到 Windows 系統目錄。

## 你需要先決定的 4 個設定（讓我幫你填）
1) 掃描根目錄（例：`C:\Users\user\Downloads`、`D:\Videos`）
2) 排除目錄（例：`node_modules`、`.git`、`Windows`、`Program Files`）
3) 大檔門檻（例：500MB / 1GB）
4) 整理策略（先只報告，或整理到 `D:\Archive\{YYYY-MM}`）

## 產出
- 盤點報告會存到：`workspace/reports/disk-audit/YYYY-MM-DD.md`
- 報告內容：
  - Top N 大檔
  - 最近 7 天修改最多的資料夾/檔案
  - 依副檔名統計
  - 重複檔候選（以大小 + 雜湊）

## 執行方式（給助理用）
### 1) 先跑掃描（只讀）
- 用 `scripts/scan.ps1` 產生 JSON 與 Markdown 報告。

### 2) （可選）整理/歸檔
- 用 `scripts/organize.ps1`（目前尚未建立，需由 AI 協助使用者確認規則後動態建立或執行指令）。

## 腳本
- `scripts/scan.ps1`：掃描 + 報告（只讀）
- `scripts/lib.ps1`：共用函式 (目前尚未建立，若需要可由 AI 動態生成)

