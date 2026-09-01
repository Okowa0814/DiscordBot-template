# DiscordBot Template

一個基於 [discord.py](https://discordpy.readthedocs.io/) 的 Discord Bot 範本，採 Cog 模組化架構，內建幾個常用功能，開箱即用。

## 功能

- **Anti-Bot 誘捕頻道**（`cogs/anti_bot.py`）：在指定頻道發言的成員會被自動踢出，用來抓誤觸誘捕頻道的機器人帳號。
- **動態語音頻道**（`cogs/voice_manager.py`）：成員加入指定的「建立頻道」時，自動建立一個專屬語音頻道並移動過去；頻道淨空後自動刪除。
- **自助身份組**（`cogs/role_selector.py`）：管理員用 `/setup_roles` 指令產生按鈕面板，成員點按鈕即可自行領取/取消身份組。
- **新成員歡迎**（`cogs/welcome.py`）：有新成員加入伺服器時，在系統訊息頻道發送歡迎訊息。

## 環境需求

- Docker / Docker Compose

## 設定環境變數

複製範例檔並填入實際值：

```bash
cp .env.example .env
```

編輯 `.env`：

```
DISCORD_TOKEN=你的 Bot Token
CREATE_CHANNEL_ID=觸發動態語音頻道建立的頻道 ID（選填）
TRAP_CHANNEL_ID=誘捕頻道 ID（選填）
```

| 變數 | 說明 | 必填 |
|---|---|---|
| `DISCORD_TOKEN` | 在 [Discord Developer Portal](https://discord.com/developers/applications) 的 Bot 頁面取得 | 是 |
| `CREATE_CHANNEL_ID` | 語音頻道 ID，不填則停用動態語音頻道功能 | 否 |
| `TRAP_CHANNEL_ID` | 文字頻道 ID，不填則停用 Anti-Bot 功能 | 否 |

> 取得頻道 ID：Discord 用戶端開啟「開發者模式」（設定 → 進階），右鍵頻道 → 複製頻道 ID。

## 啟動（Docker）

```bash
docker compose up -d --build
```

查看日誌：

```bash
docker compose logs -f
```

停止：

```bash
docker compose down
```

修改程式碼或依賴後，重新建置：

```bash
docker compose up -d --build
```

## 需要的 Discord 權限 / Intents

- Bot 需要在 Developer Portal 的 Bot 分頁開啟以下 **Privileged Gateway Intents**：
  - `SERVER MEMBERS INTENT`
  - `MESSAGE CONTENT INTENT`
- 伺服器端建議賦予 Bot：管理身份組、管理頻道、踢出成員、移動成員（語音）等權限，且 Bot 身份組需高於它要管理的身份組。

## 專案結構

```
.
├── main.py                 # 進入點，載入所有 cogs
├── cogs/
│   ├── anti_bot.py          # 誘捕頻道踢人
│   ├── voice_manager.py     # 動態語音頻道
│   ├── role_selector.py     # 自助身份組按鈕
│   └── welcome.py           # 新成員歡迎訊息
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## 新增功能

在 `cogs/` 底下新增一個 `.py` 檔案，並實作 `async def setup(bot): await bot.add_cog(...)`，`main.py` 啟動時會自動掃描並載入，無需額外註冊。
