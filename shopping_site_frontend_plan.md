# 購物網站前端計畫書

## 1. 專案目標

開發一個現代化、響應式且使用者友善的購物網站前端，用於展示與 TiDB 資料庫整合的後端服務。此前端應用需包含使用者身份驗證、商品瀏覽、購物車管理、訂單處理及會員資訊查詢等核心電商功能。

## 2. 技術棧選擇

本專案旨在展示 TiDB 的特性，因此前後端技術的選擇都考慮了高效能、現代化以及良好的開發體驗。

### 2.1. 前端技術棧 (Frontend Technology Stack)

前端將採用 **Vue.js (版本 3+)** 作為核心框架，搭配其生態系統中的推薦工具，以建構一個響應式且互動的使用者介面。

*   **核心框架 (Core Framework):** Vue.js 3
*   **狀態管理 (State Management):** Pinia (Vue.js 3 官方推薦)
*   **路由管理 (Routing):** Vue Router
*   **打包工具 (Build Tool):** Vite
*   **程式語言 (Programming Language):** TypeScript
*   **HTTP 客戶端 (HTTP Client):** Axios
*   **UI 元件庫/CSS 框架 (UI Component Library/CSS Framework):** Element Plus (一套完整且美觀的 Vue 3 UI 元件庫，有助於快速開發)

### 2.2. 後端技術棧摘要 (Backend Technology Stack Summary)

雖然本計畫書主要聚焦於前端，但為了完整呈現專案背景，後端將採用以下技術棧與 TiDB 整合：

*   **Web 框架 (Web Framework):** FastAPI (基於 Python 3.10+)
*   **ORM (Object-Relational Mapper):** Tortoise ORM (支援異步操作)
*   **資料庫驅動 (Database Driver for TiDB/MySQL):** `aiomysql` 或 `asyncmy` (支援異步操作)
*   **核心資料庫 (Core Database):** TiDB (與 MySQL 協議兼容)

這樣的組合確保了從前端到資料庫的整個流程都能高效地利用異步特性，以應對高並發場景，充分發揮 TiDB 的效能優勢。

## 3. 網站功能模組規劃

### 3.1. 首頁 (Home Page)

*   **功能:**
    *   網站 Logo 與導航欄。
    *   輪播圖或特色商品展示區。
    *   初始 3 個商品列表展示 (圖片、名稱、價格)。
    *   熱銷排行榜入口。
    *   頁腳 (Footer)。
*   **元件:** `Navbar`, `HeroSection`/`Carousel`, `ProductCard`, `BestsellerTeaser`, `Footer`

### 3.2. 商品列表頁 (Product List Page)

*   **功能:** 展示所有/分類商品、篩選器、排序、分頁。
*   **元件:** `ProductCard`, `FilterSidebar`, `SortDropdown`, `Pagination`

### 3.3. 商品詳情頁 (Product Detail Page)

*   **功能:** 單一商品詳細資訊 (圖片集、名稱、描述、規格、價格)、數量選擇、「加入購物車」按鈕、相關商品推薦 (可選)。
*   **元件:** `ProductImageGallery`, `ProductInfo`, `QuantitySelector`, `AddToCartButton`, `RelatedProducts`

### 3.4. 使用者登入/註冊頁 (Login/Register Page)

*   **功能:** 登入表單、註冊表單。
*   **元件:** `LoginForm`, `RegisterForm`

### 3.5. 會員中心 (Member Profile Page)

*   **功能:**
    *   查看/編輯會員基本資訊。
    *   查看歷史訂單列表 (訂單編號、日期、總金額、狀態)。
    *   查看訂單詳情。
    *   登出按鈕。
*   **元件:** `ProfileForm`, `OrderHistoryTable`, `OrderDetailView`

### 3.6. 購物車頁 (Shopping Cart Page)

*   **功能:** 展示購物車商品 (縮圖、名稱、單價、数量、小計)、修改數量、移除商品、顯示總金額、「前往結帳」按鈕。
*   **元件:** `CartItem`, `CartSummary`, `CheckoutButton`

### 3.7. 結帳頁 (Checkout Page)

*   **功能:** 填寫收貨人資訊、選擇配送/支付方式 (初期可模擬支付)、訂單摘要預覽、「確認下單」按鈕。
*   **元件:** `ShippingAddressForm`, `ShippingMethodSelector`, `PaymentMethodSelector`, `OrderSummaryPreview`, `PlaceOrderButton`

### 3.8. 訂單完成頁 (Order Confirmation Page)

*   **功能:** 顯示訂單成功訊息、訂單編號、感謝訊息、返回/查看訂單連結。
*   **元件:** `ConfirmationMessage`

### 3.9. 熱銷排行榜頁 (Best Sellers Page)

*   **功能:** 展示銷量最高的商品列表 (總體排行)。
*   **元件:** `ProductCard`, `RankingList`

## 4. Demo 初始資料與內容設定

為了確保 DEMO 過程的順暢性並有效展示網站功能，預計需要以下初始資料。這些資料應在後端 API 啟動時預載入到 TiDB 資料庫中，或者由前端在特定情況下使用 mock data。

### 4.1. 初始商品資料 (至少 3-5 個)

以下為建議的初始商品範例，用於填充商品列表和首頁展示：

1.  **商品一:**
    *   **名稱:** 「TiDB 官方限量版 T-Shirt」
    *   **描述:** 「舒適純棉，印有 TiDB Logo，開發者必備信仰充值潮服。」
    *   **價格:** 25.00 (美元)
    *   **庫存:** 100
    *   **圖片:** (建議使用 TiDB 相關的 Logo 或吉祥物圖片，或通用 T-Shirt 佔位圖)
    *   **分類:** 服裝
2.  **商品二:**
    *   **名稱:** 「高效能HTAP資料庫實戰手冊」
    *   **描述:** 「深入淺出 TiDB 架構與應用，從入門到精通，解鎖數據潛能。」
    *   **價格:** 49.99 (美元)
    *   **庫存:** 50
    *   **圖片:** (書籍封面佔位圖，可帶有 TiDB 或資料庫相關元素)
    *   **分類:** 書籍
3.  **商品三:**
    *   **名稱:** 「TiDB 雲服務體驗券 (1個月)」
    *   **描述:** 「免費體驗 TiDB Cloud Developer Tier 一個月，輕鬆部署與管理您的 TiDB 叢集。」
    *   **價格:** 0.00 (美元) (或設為小額，如 1.00 美元)
    *   **庫存:** 200
    *   **圖片:** (雲服務或 TiDB Cloud Logo 相關示意圖)
    *   **分類:** 服務
4.  **商品四 (可選，增加豐富度):**
    *   **名稱:** 「PingCAP 定製鍵帽組」
    *   **描述:** 「機械鍵盤愛好者福音，PingCAP 特色設計，為您的鍵盤增添個性。」
    *   **價格:** 15.00 (美元)
    *   **庫存:** 75
    *   **圖片:** (鍵帽示意圖)
    *   **分類:** 配件

*   **商品圖片處理:** 初期 DEMO 可使用 placeholder.com 等服務生成佔位圖片，或尋找一些版權友好的通用商品圖片。關鍵是尺寸統一，避免影響佈局。

### 4.2. 預設使用者帳號 (至少 1-2 個)

為了方便 DEMO 時快速登入並展示會員功能，建議預設以下使用者帳號：

1.  **使用者一 (普通用戶):**
    *   **用戶名/Email:** `user@example.com`
    *   **密碼:** `password123` (DEMO 環境密碼可簡單，真實環境需加強)
    *   **會員資料 (可選預填):** 姓名 - 「普通用戶A」, 收貨地址等。
2.  **使用者二 (可選，用於展示不同用戶數據):**
    *   **用戶名/Email:** `testuser@example.com`
    *   **密碼:** `password123`

### 4.3. 初始訂單資料 (可選, 每個預設用戶 0-2 筆)

若希望在 DEMO 初期即展示「歷史訂單」功能，可以為預設用戶創建一些初始訂單數據。

*   例如，為 `user@example.com` 創建一筆已完成訂單，包含上述的「TiDB 官方限量版 T-Shirt」和「高效能HTAP資料庫實戰手冊」。
*   訂單狀態、創建時間等也應一併設定。
*   這部分資料的創建可能需要在後端 API 實現後手動操作或編寫腳本生成。

### 4.4. 熱銷排行榜初始邏輯

*   由於初期訂單量可能為零或極少，熱銷排行榜可能無法直接展示。考慮以下策略：
    *   **策略一 (後端處理):** 如果後端 API (`GET /api/products/bestsellers`) 在沒有足夠訂單數據時，可以返回預設的幾個熱門商品 (例如基於預設庫存量或手動指定)。
    *   **策略二 (前端展示):** 如果 API 返回空列表，前端可以展示一個「暫無熱銷商品」的提示，或者預設展示所有商品中的前幾個。
    *   為了更好展示 TiDB，**策略一**更優，因為這樣可以模擬從資料庫查詢並排序的過程。

## 5. 狀態管理策略

*   **使用者認證狀態:** 儲存登入狀態 (token, 使用者資訊)，可使用 `localStorage`。
*   **購物車狀態:** 購物車內容**完全由前端使用 `localStorage` 管理**。在使用者點擊「確認下單」時，才將購物車內容一次性提交給後端 API。
*   **商品資料:** API 獲取的資料，依需求在元件內或全域狀態管理。
*   **全域 UI 狀態:** 載入中狀態、通知訊息等。

## 6. API 整合點 (前端需呼叫的後端 API 範例)

*   **商品 (Products):**
    *   `GET /api/products`
    *   `GET /api/products/{product_id}`
    *   `GET /api/products/bestsellers`
*   **使用者認證 (Auth):**
    *   `POST /api/auth/login`
    *   `POST /api/auth/register`
    *   `POST /api/auth/logout`
    *   `GET /api/auth/me`
*   **會員 (Users/Profile):**
    *   `GET /api/users/me/profile`
    *   `PUT /api/users/me/profile`
*   **購物車 (Cart):** (購物車主要由前端管理，結帳時提交訂單)
*   **訂單 (Orders):**
    *   `POST /api/orders` (此時會傳遞購物車內所有商品資訊)
    *   `GET /api/orders`
    *   `GET /api/orders/{order_id}`

## 7. UI/UX 設計考量

*   響應式設計。
*   直觀的導航。
*   清晰的視覺層次。
*   一致的設計風格。
*   易於操作的表單。
*   載入狀態與回饋。

## 8. 開發階段與時程 (初步預估)

以下為前端開發的詳細階段、主要任務及初步時程預估。此處時程主要考量前端獨立開發與串接 API 的時間，後端 API 開發時程需另行安排，但前後端可並行開發以縮短總體時程。

### 階段一: 環境搭建與基礎架構 (預計 0.5 - 1 週)

*   **任務 1.1: 前端專案初始化**
    *   使用 Vite 建立 Vue.js 3 + TypeScript 專案。
    *   配置 ESLint, Prettier 以確保程式碼風格一致。
*   **任務 1.2: 核心依賴整合**
    *   整合 Vue Router 進行路由管理。
    *   整合 Pinia 進行狀態管理。
    *   整合 Axios 並設定基礎實例 (例如，設定 API base URL)。
    *   整合 Element Plus UI 元件庫，並進行全域或按需引入配置。
*   **任務 1.3: 基本佈局與通用元件**
    *   建立網站主要佈局 (如包含導航欄 `Navbar` 和頁腳 `Footer` 的 `App.vue`)。
    *   開發基礎通用元件 (如自定義按鈕 `AppButton`, 輸入框 `AppInput` - 若 Element Plus 不完全滿足需求)。
*   **任務 1.4: 專案結構與路由初步定義**
    *   規劃 `src` 目錄結構 (如 `components`, `views`, `router`, `store`, `services`, `assets`, `types`)。
    *   定義主要頁面的路由佔位 (如首頁、商品列表、商品詳情、購物車、登入、會員中心、熱銷榜)。

### 階段二: 核心功能開發 - 商品展示與購物車 (預計 1.5 - 2.5 週)

*   **任務 2.1: 首頁商品展示**
    *   開發 `ProductCard.vue` 元件用於展示單個商品 (圖片、名稱、價格)。
    *   在首頁 (`HomePage.vue`) 實現初始 3 個商品的靜態展示或從 API 獲取 (連接 `GET /api/products`，可先用 mock data)。
    *   實現首頁熱銷排行榜入口的跳轉連結。
*   **任務 2.2: 商品列表頁**
    *   開發 `ProductListPage.vue`。
    *   連接 `GET /api/products` API 以獲取並展示所有商品列表。
    *   實現分頁功能 (若 API 支持)。
    *   (快速開發階段可暫緩篩選與排序功能，或僅做簡單前端篩選)。
*   **任務 2.3: 商品詳情頁**
    *   開發 `ProductDetailPage.vue`。
    *   連接 `GET /api/products/{product_id}` API 以獲取並展示商品詳細資訊。
    *   實現數量選擇功能。
    *   實現「加入購物車」按鈕邏輯。
*   **任務 2.4: 購物車基礎功能 (基於 `localStorage` 和 Pinia)**
    *   建立 `cart.ts` store (Pinia) 管理購物車狀態。
    *   實現加入商品到購物車的邏輯 (更新 `localStorage` 和 Pinia store)。
    *   開發 `CartPage.vue` 以展示購物車商品列表。
    *   實現修改購物車商品數量、移除商品的功能。
    *   計算並顯示購物車總金額。

### 階段三: 核心功能開發 - 使用者認證與訂單 (預計 1.5 - 2 週)

*   **任務 3.1: 使用者註冊**
    *   開發 `RegisterPage.vue` 包含註冊表單。
    *   連接 `POST /api/auth/register` API 提交註冊資訊。
    *   處理註冊成功與失敗的提示。
*   **任務 3.2: 使用者登入**
    *   開發 `LoginPage.vue` 包含登入表單。
    *   連接 `POST /api/auth/login` API 提交登入資訊。
    *   處理登入成功 (儲存 token 到 `localStorage` 和 Pinia store, 更新 UI 狀態) 與失敗的提示。
    *   實現路由守衛 (Navigation Guards) 保護需要登入才能訪問的頁面。
*   **任務 3.3: 會員中心 - 基本資訊與登出**
    *   開發 `MemberProfilePage.vue` 基礎框架。
    *   連接 `GET /api/auth/me` 或 `GET /api/users/me/profile` API 獲取並展示會員基本資訊。
    *   (DEMO 階段可暫緩編輯會員資訊功能)。
    *   實現登出功能 (清除 token, 重置 Pinia store, 跳轉到登入頁，連接 `POST /api/auth/logout` - 若後端需要)。
*   **任務 3.4: 結帳流程與下單**
    *   在 `CartPage.vue` 或新建 `CheckoutPage.vue` 實現結帳流程。
    *   (DEMO 階段可簡化收貨地址、配送/支付方式的選擇，或使用預設值)。
    *   實現「確認下單」按鈕邏輯，收集購物車資訊和必要的用戶資訊。
    *   連接 `POST /api/orders` API 提交訂單，並清空購物車。
    *   跳轉到訂單完成頁。
*   **任務 3.5: 訂單完成頁**
    *   開發 `OrderConfirmationPage.vue` 顯示成功訊息和訂單編號 (從 API 回應獲取)。

### 階段四: 進階功能與整體測試 (預計 1 - 1.5 週)

*   **任務 4.1: 會員中心 - 歷史訂單**
    *   在 `MemberProfilePage.vue` 中開發歷史訂單列表區塊。
    *   連接 `GET /api/orders` API 獲取並展示會員的歷史訂單。
    *   (DEMO 階段可暫緩訂單詳情頁，或僅簡單展示訂單主要資訊)。
*   **任務 4.2: 熱銷排行榜頁**
    *   開發 `BestSellersPage.vue`。
    *   連接 `GET /api/products/bestsellers` API 獲取並展示熱銷商品列表。
*   **任務 4.3: 整體流程測試與 UI/UX 調整**
    *   完整測試所有核心購物流程、使用者認證流程、會員功能。
    *   根據測試結果進行 UI/UX 細部調整和 Bug 修復。
    *   確保響應式設計在不同螢幕尺寸下的基本可用性。
*   **任務 4.4: DEMO 準備**
    *   準備 DEMO 腳本和初始資料 (確保商品、使用者帳號等符合 DEMO 需求)。
    *   最終確認所有功能點均能良好運作以展示 TiDB 特性。

*(註：以上時程為純前端開發預估，實際進度會受後端 API 開發進度、設計稿複雜度及團隊協作等因素影響。為快速 DEMO，部分非核心細節功能已標註為可暫緩或簡化。)*

## 9. 未來可擴展功能 (選填)

*   商品評論與評分。
*   商品搜尋。
*   優惠券與促銷。
*   多語言支援。
*   客服整合。
*   後台管理系統。

## 10. Demo 展示重點與 TiDB 關聯

本 DEMO 購物網站旨在直觀、有效地展示 TiDB 作為現代化分散式資料庫的關鍵特性和優勢。前端的每一個核心功能和互動流程，都應被設計為能夠引導觀眾理解後端 TiDB 所扮演的角色。以下列出主要的展示重點及其與 TiDB 的關聯：

### 10.1. 高併發下的穩定商品瀏覽與快速響應
*   **前端操作:**
    *   使用者快速瀏覽商品列表頁，進行分頁操作 (若有)。
    *   同時模擬多個使用者訪問網站，進行商品瀏覽。
    *   點擊進入商品詳情頁。
*   **TiDB 關聯展示:**
    *   **高效讀取 (Read Performance):** 強調 TiDB 即使在大量商品數據 (可口頭擴展說明，例如"假設我們有數百萬 SKU") 和高併發讀取請求下，依然能快速返回商品資訊，保持頁面載入流暢。
    *   **水平擴展 (Horizontal Scalability):** 說明 TiDB 的分散式架構允許透過增加節點來線性提升讀取處理能力，應對未來業務增長。
    *   **SQL 兼容性:** 前端透過標準的後端 API (如 RESTful) 查詢商品，後端則使用標準 SQL 與 TiDB 交互，展示 TiDB 對 MySQL 協議和常用 SQL 的良好兼容性，降低開發和遷移成本。

### 10.2. 即時庫存查詢與準確性 (商品詳情頁)
*   **前端操作:**
    *   在商品詳情頁查看商品庫存狀態 (例如："僅剩 N 件"或"庫存充足")。
*   **TiDB 關聯展示:**
    *   **即時一致性 (Real-time Consistency):** 強調 TiDB 作為支援 ACID 事務的分散式資料庫，能夠確保庫存數據的強一致性。使用者看到的庫存是即時且準確的。
    *   **(可擴展討論):** 如果後續有多人同時下單同一緊俏商品，可以討論 TiDB 如何透過事務機制保證庫存不會超賣 (這部分可能需要後端邏輯配合說明)。

### 10.3. 流暢的購物車操作與可靠的訂單生成
*   **前端操作:**
    *   使用者將商品加入購物車、修改數量、移除商品。
    *   使用者點擊「確認下單」，提交訂單。
    *   系統快速生成訂單並顯示訂單成功頁面。
*   **TiDB 關聯展示:**
    *   **交易處理能力 (Transactional Workloads - OLTP):** 下單操作是典型的 OLTP 場景，涉及多個數據表的寫入和更新 (如訂單表、訂單商品表、可能還有庫存更新)。展示 TiDB 處理這類交易的原子性、一致性、隔離性和持久性 (ACID)。
    *   **高可用性 (High Availability):** 說明 TiDB 的多副本和 Raft 共識機制確保了即使部分節點故障，資料依然安全，交易依然可以成功提交，保障了核心交易流程的穩定性。

### 10.4. 會員歷史訂單的快速查詢與展示
*   **前端操作:**
    *   使用者登入後，在會員中心查看自己的歷史訂單列表。
*   **TiDB 關聯展示:**
    *   **複雜查詢能力 (Complex Queries):** 查詢歷史訂單通常涉及使用者表、訂單表、訂單商品表等多個表的關聯查詢。展示 TiDB 處理這類 JOIN 操作和過濾條件的能力。
    *   **數據一致性:** 使用者看到的歷史訂單是準確且完整的。

### 10.5. 熱銷商品排行榜的即時分析
*   **前端操作:**
    *   使用者訪問熱銷商品排行榜頁面。
*   **TiDB 關聯展示:**
    *   **HTAP (Hybrid Transactional/Analytical Processing):** 這是 TiDB 的核心特色之一。熱銷排行榜的生成需要對交易數據 (如訂單表、訂單商品表) 進行即時的聚合分析 (例如按銷量排序)。展示 TiDB 如何在同一份數據上同時高效支持交易處理 (OLTP) 和即時分析 (Real-time OLAP)，而無需複雜的 ETL 過程將數據同步到專門的分析資料庫。
    *   **(可簡化說明):** 即使我們的 DEMO 熱銷榜邏輯相對簡單，也要強調 TiDB 具備處理更複雜即時分析的能力，例如結合時間窗口、用戶畫像等進行更精細的推薦或排行。

### 10.6. (總體強調) 彈性擴展與簡化運維
*   **DEMO 場景:** 雖然前端無法直接展示，但在口頭介紹或輔助材料中可以強調。
*   **TiDB 關聯展示:**
    *   **線上擴展/縮容 (Online Scaling):** 說明 TiDB 可以根據業務負載變化，在線平滑地增加或減少節點，而幾乎不影響服務。
    *   **自動故障轉移 (Automatic Failover):** 再次強調高可用性，運維人員無需過多手動干預。
    *   **MySQL 兼容性帶來的生態便利:** 方便使用各種現有的 MySQL 工具鏈。

透過將前端操作與背後 TiDB 的能力巧妙地聯繫起來，可以讓技術觀眾和潛在用戶更深刻地理解 TiDB 的實際價值和應用場景。