---
name: firecrawl
description: Web search and scraping via Firecrawl API. Use when you need to search the web, scrape websites (including JS-heavy pages), crawl entire sites, or extract structured data from web pages. Requires FIRECRAWL_API_KEY environment variable. 透過 Firecrawl API 進行網頁搜尋與爬取。
read_when:
  - 爬取
  - 抓取網頁
  - 網頁搜尋
  - 擷取資料
  - scrape
  - crawl
  - 網站內容
  - 抓PTT
  - 爬蝦皮
  - 抓新聞
---

# Firecrawl

Web search and scraping via Firecrawl API.
透過 Firecrawl API 進行網頁搜尋與爬取。

## AI Instructions｜給 AI 的執行指示
- **執行方式：** 本技能不是虛擬指令，必須使用 Python 執行 `scripts/` 目錄下的腳本。
- **相對路徑：** 當您要呼叫腳本時，請以絕對路徑或進入本技能目錄後執行 `python scripts/search.py` 等指令。
- **環境變數：** 執行前，請確保系統已設定 `FIRECRAWL_API_KEY`。在 Windows (PowerShell) 環境中可透過 `$env:FIRECRAWL_API_KEY` 檢查與設定。

## Prerequisites｜前置需求

Set `FIRECRAWL_API_KEY` in your environment or `.env` file.
For Windows (PowerShell):

```powershell
$env:FIRECRAWL_API_KEY="fc-df783b3657894f3abd602a75d001cdd9"
```

For Linux/Mac (Bash):

```bash
export FIRECRAWL_API_KEY="fc-df783b3657894f3abd602a75d001cdd9"
```

## Quick Start｜快速開始

### Search the web｜搜尋網頁

```bash
python scripts/search.py "your search query" --limit 10
```

**繁體中文範例：**

```bash
# 搜尋台灣相關新聞
python scripts/search.py "台積電 最新財報 2026" --limit 5

# 搜尋特定技術主題
python scripts/search.py "React Server Components 教學" --limit 10

# 搜尋產品資訊
python scripts/search.py "iPhone 17 規格比較" --limit 5
```

### Scrape a single page｜爬取單一頁面

```bash
python scripts/scrape.py "https://example.com"
```

**繁體中文範例：**

```bash
# 爬取政府公開資料頁面
python scripts/scrape.py "https://data.gov.tw"

# 爬取新聞文章
python scripts/scrape.py "https://technews.tw/some-article"

# 爬取電商產品頁面（含 JS 渲染內容）
python scripts/scrape.py "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=12345678"
```

### Crawl an entire site｜整站爬取

```bash
python scripts/crawl.py "https://example.com" --max-pages 50
```

**繁體中文範例：**

```bash
# 爬取公司官網所有頁面
python scripts/crawl.py "https://www.example.com.tw" --max-pages 100

# 爬取技術文件站（限制頁數避免過量）
python scripts/crawl.py "https://docs.some-service.com" --max-pages 30

# 爬取部落格全站文章
python scripts/crawl.py "https://blog.example.com.tw" --max-pages 50
```

## Common Use Cases｜常見使用情境

以下列出使用者可能提出的需求與對應操作方式：

| 使用者需求 | 操作方式 | 指令範例 |
|---|---|---|
| 「幫我查一下最新的 AI 新聞」 | `search.py` | `python scripts/search.py "AI 人工智慧 最新新聞 2026" --limit 10` |
| 「把這個網頁的內容抓下來」 | `scrape.py` | `python scripts/scrape.py "https://target-url.com"` |
| 「幫我爬整個網站的資料」 | `crawl.py` | `python scripts/crawl.py "https://target-site.com" --max-pages 50` |
| 「抓取這個頁面的表格資料」 | `scrape.py`（搭配結構化擷取） | `python scripts/scrape.py "https://page-with-tables.com"` |
| 「搜尋蝦皮上某產品的價格」 | `search.py` | `python scripts/search.py "蝦皮 AirPods Pro 價格" --limit 5` |
| 「把這個技術文件站的內容都下載下來」 | `crawl.py` | `python scripts/crawl.py "https://docs.example.com" --max-pages 100` |

## Workflow Tips｜操作建議

1. **先搜尋再爬取**：不確定目標 URL 時，先用 `search.py` 找到正確頁面，再用 `scrape.py` 擷取完整內容。
2. **控制爬取範圍**：使用 `--max-pages` 參數避免整站爬取時耗費過多配額。
3. **JS 重度頁面**：Firecrawl 能處理 JavaScript 渲染的頁面（如 SPA 應用程式），適合爬取現代前端框架建構的網站。
4. **結構化資料擷取**：從網頁中擷取特定欄位（如價格、標題、日期）時，可搭配 API 的 extract 功能。

## API Reference

See [references/api.md](references/api.md) for detailed API documentation and advanced options.
詳細的 API 文件與進階選項請參閱 [references/api.md](references/api.md)。

## Scripts

- `scripts/search.py` - Search the web with Firecrawl
- `scripts/scrape.py` - Scrape a single URL
- `scripts/crawl.py` - Crawl an entire website