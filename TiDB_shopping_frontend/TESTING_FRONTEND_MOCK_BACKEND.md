# 如何使用模擬後端測試前端註冊功能

本文檔說明瞭如何啟動模擬後端伺服器和前端開發伺服器，以測試前端的註冊功能。

## 前提條件

1.  **Node.js 和 npm/yarn**: 已安裝用於執行前端專案。
2.  **Python**: 已安裝用於執行後端模擬伺服器 (FastAPI)。
3.  **前端依賴**: 已在 `TiDB_shopping_frontend` 目錄下執行 `npm install` (或 `yarn install`)。
4.  **後端依賴**: 已在 `TiDB_shopping_backend` 目錄下建立虛擬環境並執行 `pip install -r requirements.txt`。

## 測試步驟

您需要開啟兩個終端機視窗。

### 終端機 1: 啟動模擬後端伺服器

1.  開啟一個新的終端機。
2.  導航到後端專案目錄：
    ```bash
    cd path/to/your/project/2025_NCCU_Distributed_Systems_project_TiDB/TiDB_shopping_backend
    ```
3.  啟用 Python 虛擬環境 (如果已建立)：
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`
4.  啟動 FastAPI 模擬後端伺服器：
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    *   伺服器將在 `http://127.0.0.1:8000` 上運行。
    *   **保持此終端機開啟。**

### 終端機 2: 啟動前端開發伺服器

1.  開啟第二個新的終端機。
2.  導航到前端專案目錄：
    ```bash
    cd path/to/your/project/2025_NCCU_Distributed_Systems_project_TiDB/TiDB_shopping_frontend
    ```
3.  確認 `vite.config.ts` 中的代理設定正確無誤：
    *   `target` 應指向 `http://localhost:8000` (模擬後端)。
    *   應包含 `rewrite: (path) => path.replace(/^\/api/, '')` 以移除 `/api` 前綴。
    ```typescript
    // vite.config.ts (部分內容)
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        },
      }
    }
    ```
4.  啟動 Vite 前端開發伺服器：
    ```bash
    npm run dev
    ```
    *   Vite 會提供一個本地訪問網址 (例如 `http://localhost:5173`)。
    *   **保持此終端機開啟。**

### 在瀏覽器中執行測試

1.  打開您的網頁瀏覽器。
2.  訪問前端的註冊頁面 (例如 `http://localhost:5173/register`)。
3.  打開瀏覽器開發者工具 (通常按 `F12`)，並切換到「網路 (Network)」和「主控台 (Console)」分頁。
4.  在註冊表單中填寫以下資訊：
    *   會員名稱 (例如：`TestUser`)
    *   Email (例如：`test@example.com`)
    *   密碼 (例如：`password123`)
    *   確認密碼 (再次輸入 `password123`)
5.  點擊「註冊」按鈕。

### 觀察結果

*   **前端介面**:
    *   是否顯示成功提示訊息？
    *   頁面是否跳轉到登入頁？
*   **瀏覽器開發者工具 - 網路 (Network) 分頁**:
    *   是否有向 `/api/auth/register` 發出的 `POST` 請求？
    *   請求狀態碼是否為 `201 Created`？
    *   回應 (Response) 內容是否為模擬後端回傳的 JSON (包含 `token`, `user` 物件)？
*   **瀏覽器開發者工具 - 主控台 (Console) 分頁**:
    *   是否有 JavaScript 錯誤？
    *   是否有 `console.log` 的調試輸出？
*   **終端機 1 (模擬後端伺服器)**:
    *   是否看到模擬後端 `print` 語句輸出的日誌，表明已收到請求並回傳了回應？

如果所有觀察結果均符合預期，則表示前端註冊功能與模擬後端的整合測試成功。 