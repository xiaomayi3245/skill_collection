# skill_collection


- 每一次安裝完可以請openclaw 檢視skill的優劣，可以使用以下Prompt：

```
我安裝了一個 SKILL，在 "C:\Users\user.openclaw\workspace\skills\XXX" ，你審核其功能與預期執行項目，給我一個評分報告，若需要優化請列出
```

- 評分後，可以請OpenClaw 直接幫忙修改，可以使用以下Prompt：
```
請直接幫我修改 
```
修改完後，再重新評分，可以使用以下Prompt：
```
請重新評分
```

# 如何使用 SKILL：proactive-agent-skill
在對話框中依序使用以下Prompt：
1. "讓AI變得更主動"
2. 每天中午12:30 幫我備份以下檔案及目錄內所有檔案及子目錄到"C:\\WorkspaceOpenClaw\\(backup_everyday)" 目錄下，並以當天日期為目錄，複製到該目錄下：
C:\\Users\user.openclaw\\openclaw.json，C:\\Users\user\\.openclaw\\workspace
