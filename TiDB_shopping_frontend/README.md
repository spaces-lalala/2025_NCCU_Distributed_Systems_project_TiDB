# TiDB 購物網站前端開發與測試指南

本文檔提供了啟動 TiDB 購物網站前端開發環境、訪問不同頁面以及進行功能測試的指引。

## 1. 前提條件

在開始之前，請確保您已滿足以下條件：

1.  **Node.js 與 npm (或 yarn)**: 已安裝，用於運行前端 Vue.js 專案。建議使用 Node.js LTS 版本。
2.  **Python**: 已安裝 (建議版本 3.10+)，用於運行後端模擬伺服器 (FastAPI)。
3.  **Git**: 已安裝，用於版本控制。
4.  **程式碼編輯器**: 例如 VS Code。
5.  **前端依賴**:
    *   克隆專案後，在 `TiDB_shopping_frontend` 目錄下執行 `npm install` (或 `yarn install`) 來安裝所有必要的套件。
6.  **後端依賴與設定**:
    *   後端程式碼位於 `TiDB_shopping_backend` 目錄。
    *   建議在該目錄下建立 Python 虛擬環境。
    *   執行 `pip install -r requirements.txt` 來安裝後端依賴。

## 2. 啟動開發環境

要進行前端開發與測試，您通常需要同時運行後端模擬伺服器和前端開發伺服器。請開啟兩個終端機視窗。

### 終端機 1: 啟動後端模擬伺服器 (Mock Backend)

1.  開啟一個新的終端機。
2.  導航到後端專案目錄：
    ```bash
    cd path/to/your/project/2025_NCCU_Distributed_Systems_project_TiDB/TiDB_shopping_backend
    ```
3.  (可選但建議) 啟用 Python 虛擬環境：
    *   Windows: `.\venv\Scripts\activate` (假設虛擬環境名為 venv)
    *   macOS/Linux: `source venv/bin/activate` (假設虛擬環境名為 venv)
4.  啟動 FastAPI 模擬後端伺服器：
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    *   伺服器將在 `http://127.0.0.1:8000` 上運行。
    *   此伺服器目前主要用於模擬 API 端點，例如使用者註冊。
    *   **保持此終端機開啟運行。**

### 終端機 2: 啟動前端開發伺服器 (Vite)

1.  開啟第二個新的終端機。
2.  導航到前端專案目錄：
    ```bash
    cd path/to/your/project/2025_NCCU_Distributed_Systems_project_TiDB/TiDB_shopping_frontend
    ```
3.  啟動 Vite 前端開發伺服器：
    ```bash
    npm run dev
    ```
    *   Vite 會提供一個本地訪問網址，通常是 `http://localhost:5002`(如果預設端口被佔用)。請注意終端機輸出的確切網址。
    *   此命令會啟動帶有熱模塊替換 (HMR) 的開發伺服器，方便開發。
    *   **保持此終端機開啟運行。**

**重要提示：**
*   前端 `vite.config.ts` 中已配置代理 (proxy)，將所有 `/api/...` 開頭的請求轉發到 `http://localhost:8000` (即後端模擬伺服器)。這使得前端可以直接呼叫 `/api/auth/register` 這樣的路徑，而 Vite 會在開發時將其正確路由到後端。

## 3. 訪問與測試網站功能

### 3.1 測試使用者註冊與登入功能

1.  **訪問頁面**:
    *   在瀏覽器中打開前端開發伺服器提供的網址 (例如 `http://localhost:5002`)。
    *   導航到註冊頁面 (`/register`) 或登入頁面 (`/login`)。

2.  **執行操作 (註冊)**:
    *   打開瀏覽器開發者工具 (通常按 `F12`)，並切換到「網路 (Network)」和「主控台 (Console)」分頁。
    *   在註冊表單 (`/register`) 中填寫新的使用者資訊，例如:
        *   會員名稱: `NewUserOne`
        *   Email: `newuser1@example.com`
        *   密碼: `password123` (或您選擇的任何密碼)
        *   確認密碼: `password123` (與密碼一致)
    *   點擊「註冊」按鈕。
    *   **預期行為 (成功註冊)**:
        *   應顯示成功提示訊息 (例如 "使用者註冊成功 (模擬)! 請使用您註冊的密碼登入。")。
        *   頁面應自動跳轉到登入頁面 (`/login`)。
        *   在瀏覽器 Console 中，您可以看到 `[AuthService - MOCK] Simulating registration success for: newuser1@example.com` 以及當前所有已註冊用戶的 Email 列表。
    *   **測試重複註冊**:
        *   再次嘗試使用 `newuser1@example.com` 或預設的 `existeduser@example.com` 進行註冊。
        *   **預期行為**: 應顯示錯誤訊息 "此 Email 地址已被註冊。"。

3.  **執行操作 (登入)**:
    *   在登入表單 (`/login`) 中嘗試以下操作:
        *   **使用剛註冊的帳號登入**: 輸入 `newuser1@example.com` 和您設定的密碼。
        *   **使用預設帳號登入**: 輸入 `user@example.com` 和密碼 `password123`。
        *   **嘗試錯誤密碼**: 使用已註冊的 Email 和一個錯誤的密碼。
    *   **預期行為 (成功登入)**:
        *   應顯示成功提示訊息 (例如 "登入成功 (模擬)!")。
        *   頁面應自動跳轉到首頁 (`/`) 或之前嘗試訪問的頁面。
        *   導航欄應更新，顯示會員相關連結 (如「會員中心」、「登出」)。
        *   在瀏覽器 Console 中，您可以看到 `[AuthService - MOCK] Simulating login success for: <email@example.com>`。
    *   **預期行為 (登入失敗)**:
        *   應顯示錯誤訊息 "Email 或密碼錯誤 (模擬)。"。

4.  **觀察結果與預期行為 (通用)**:

    *   **前端介面**:
        *   表單驗證：嘗試提交空表單、格式錯誤的 Email、不一致的密碼 (註冊時)，應能看到相應的錯誤提示。
    *   **瀏覽器開發者工具 - 網路 (Network) 分頁**:
        *   註冊時，應看到一個向 `/api/auth/register` 發出的 `POST` 請求。請求的 Payload (負載) 應包含您輸入的 `name`, `email`, `password`。
        *   登入時，應看到一個向 `/api/auth/login` 發出的 `POST` 請求。請求的 Payload (負載) 應包含您輸入的 `email`, `password`。
        *   成功時，請求狀態碼應為 `200 OK` (依後端實現而定，目前模擬後端是 `200 OK`，雖然真實後端註冊成功可能是 `201 Created`)。
        *   成功註冊時，回應 (Response) 內容應為模擬後端回傳的 JSON，包含 `message` (例如：`{"message":"使用者註冊成功 (模擬)! 請使用您註冊的密碼登入。"}`)。
        *   成功登入時，回應 (Response) 內容應為模擬後端回傳的 JSON，包含 `token`, `user` 物件, 和 `message` (例如：`{"token":"mock-jwt-token-for-user@example.com-167...","user":{"id":"mock-id-user@example.com","name":"普通用戶A","email":"user@example.com"},"message":"登入成功 (模擬)!"}`)
    *   **瀏覽器開發者工具 - 主控台 (Console) 分頁**:
        *   不應有紅色 JavaScript 錯誤。
        *   可能會看到一些 `console.log` 的調試輸出，有助於追蹤流程。
    *   **終端機 1 (模擬後端伺服器)**:
        *   應看到 FastAPI 伺服器輸出的日誌，顯示收到 `POST /auth/register` 請求以及請求的詳細資訊。
        *   應看到模擬後端中 `print()` 語句輸出的內容，例如 "接收到的註冊資料..."。

### 3.2 訪問其他主要頁面 (未來功能)

隨著開發進度，您可以通過以下路徑訪問網站的其他主要頁面：

*   **首頁**: `/`
*   **商品列表頁**: `/products`
*   **商品詳情頁**: `/product/:id` (例如: `/product/1`)
*   **購物車頁**: `/cart`
*   **登入頁**: `/login`
*   **會員中心**: `/profile` (通常需要登入後訪問)
*   **熱銷排行榜**: `/bestsellers`
*   **結帳頁**: `/checkout` (通常需要登入且購物車有商品)
*   **訂單完成頁**: `/order-confirmation` (通常在下單成功後跳轉至此)

**測試這些未來功能時，請注意：**

*   確保相關的後端 API 端點已在模擬後端 (`TiDB_shopping_backend/main.py`) 中實現或有佔位邏輯。
*   檢查前端的服務層 (`TiDB_shopping_frontend/src/services/`) 是否有對應的 API 呼叫函數。
*   觀察前端元件 (`TiDB_shopping_frontend/src/views/` 和 `TiDB_shopping_frontend/src/components/`) 的渲染是否符合預期。
*   利用瀏覽器開發者工具進行調試。

## 4. 專案結構概覽 (前端)

*   `public/`: 靜態資源，會被直接複製到打包輸出的根目錄。
*   `src/`: 主要的原始碼目錄。
    *   `assets/`: 靜態資源 (圖片、字體等)，會被 Vite 處理和打包。
    *   `components/`: 可複用的 Vue 元件。
    *   `router/`: Vue Router 的設定 (`index.ts`)。
    *   `services/`: API 呼叫服務 (例如 `authService.ts`)。
    *   `store/`: Pinia 狀態管理 (如果使用)。
    *   `types/`: TypeScript 型別定義 (例如 `auth.ts`)。
    *   `views/`: 頁面級 Vue 元件 (例如 `HomePage.vue`, `RegisterPage.vue`)。
    *   `App.vue`: 根 Vue 元件。
    *   `main.ts`: Vue 應用程式的入口點。
*   `vite.config.ts`: Vite 的配置文件，包含代理設定。
*   `tsconfig.json`: TypeScript 的配置文件。
*   `package.json`: 專案依賴與腳本。

## 5. 其他注意事項

*   **程式碼風格**: 專案使用 ESLint 和 Prettier (或 Ruff) 進行程式碼檢查與格式化。建議在提交程式碼前運行 `npm run lint` 和 `npm run format`。
*   **版本控制**: 定期提交您的變更到 Git，並撰寫清晰的提交訊息。
*   **除錯**: 善用瀏覽器開發者工具和 Vue Devtools (瀏覽器擴充功能) 進行除錯。

祝您開發愉快！ 