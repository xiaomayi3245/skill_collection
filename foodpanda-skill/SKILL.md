---
name: nearby-restaurant-finder
description: 附近高評分餐廳搜尋與點餐決策輔助。當使用者要找「附近評分最高/評論最多/正在營業」的餐廳，或要依預算與類型（如小火鍋）快速挑店時使用。可產出可手動下單清單；不執行登入、付款或代刷。
---

# nearby-restaurant-finder

先給「店名清單（1~5）」讓使用者選，再依選項一次補齊詳細資訊。

## 目標

1. 搜尋指定地址/區域附近餐廳
2. **先輸出店名編號清單（1~5）**
3. 詢問使用者要查哪一間（可回 1/2/3/4/5）
4. 依選擇一次輸出完整欄位（避免來回追問）
5. 明確標示「平台價格/運費以實際頁面為準」

## 安全邊界

- 不要求帳號密碼
- 不處理付款/金流
- 不保證即時價格與庫存（僅建議）

## 最小輸入

- 地址或區域（例：信義區松山路100號）
- 人數（預設 1）
- 每人預算（預設 250）
- 類型偏好（例：小火鍋、便當、拉麵）

## 推薦流程

1. **先找店**：抓附近候選店（Google Maps 或使用者提供清單）
2. **再排序**：
   - 綜合分數 = 評分 + 評論數加權 + 距離加權 + 營業加分
3. **再配餐**：針對前 3 家給出「不超預算」組合

## 排序規則（預設）

- 評分：40%
- 評論數：30%
- 距離：20%
- 營業中：10%

## 命令（可選）

```bash
python scripts/nearby_ranker.py '{"budget_per_person":300,"people":2,"cuisine":"小火鍋","candidates":[{"name":"店A","rating":4.8,"reviews":1200,"distance_km":0.8,"open":true}]}'
```

## 互動與輸出格式（固定）

### 第 1 則：先給可選清單（含關鍵三欄）
先輸出 1~5 候選店，每行至少包含：
- 店名
- 星等（rating）
- 平均消費（estimated_per_person；若無則顯示價位區間）
- 地址（address）

範例：
1. 店名A｜⭐4.8｜人均約260｜某某路xx號
2. 店名B｜⭐4.6｜人均約220｜某某街xx號
...

接著只問一句：
「請回 1/2/3/4/5，我就補齊完整資料。」

### 第 2 則：依使用者編號輸出完整資料（一次到位）
- 店名
- 星等（rating）
- 評論數（reviews）
- 地址（address）
- 訂位/聯絡電話（reservation_phone）
- 是否有 foodpanda 外送（foodpanda_delivery）
- 餐廳網址（restaurant_url）
- 地圖網址（maps_url）
- 招牌菜（signature_dishes）
- 價位（price_level / estimated_per_person）
- 距離（distance_km）
- 預估送達（eta_min，如有）
- 附近停車場（nearby_parking）
- 是否營業中（open）
- 綜合分（score）

### 第 3 則（可選）
使用者若要再比價，才提供 Top 3 點餐建議（每店一組，標示預估總價）。

提醒：實際餐點、價格、運費、優惠以平台頁面為準。

## 參考

- `references/tutorial.md`
- `references/prompt-examples.md`
- `references/usage.md`
- `scripts/foodpanda_helper.py`（舊版配餐引擎，可做第二步配單）
