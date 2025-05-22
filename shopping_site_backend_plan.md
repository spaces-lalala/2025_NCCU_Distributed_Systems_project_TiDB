# TiDB 購物網站後端開發計畫書

## 1. 專案目標回顧

本專案旨在開發一個現代化、高效能的購物網站，後端系統需與 TiDB 資料庫深度整合，為前端應用提供穩定、快速且可擴展的 API 服務。後端開發的核心目標是實現使用者認證、商品管理、購物車到訂單的完整流程處理、會員資訊管理等功能，並特別關注如何利用 TiDB 的特性來應對高並發讀寫、即時數據分析等場景。

## 2. 後端技術棧

*   **Web 框架 (Web Framework):** FastAPI (基於 Python 3.10+)
*   **ORM (Object-Relational Mapper):** Tortoise ORM (支援異步操作)
*   **資料庫驅動 (Database Driver for TiDB/MySQL):** `aiomysql` 或 `asyncmy` (支援異步操作)
*   **核心資料庫 (Core Database):** TiDB (與 MySQL 協議兼容)
*   **資料驗證 (Data Validation):** Pydantic
*   **認證機制 (Authentication):** JWT (JSON Web Tokens)
*   **環境管理 (Environment Management):** `conda` / `venv`
*   **版本控制 (Version Control):** `git`

## 3. TiDB 資料庫結構設計

以下為建議的 TiDB 資料庫表結構。所有表名建議使用小寫複數形式。

### 3.1. `users` (使用者表)

| 欄位名稱          | 資料類型             | 約束/備註                                  |
| ----------------- | -------------------- | ------------------------------------------ |
| `id`              | INT / BIGINT         | PRIMARY KEY, AUTO_INCREMENT                |
| `username`        | VARCHAR(255)         | UNIQUE, NOT NULL                           |
| `email`           | VARCHAR(255)         | UNIQUE, NOT NULL                           |
| `hashed_password` | VARCHAR(255)         | NOT NULL                                   |
| `created_at`      | TIMESTAMP / DATETIME | DEFAULT CURRENT_TIMESTAMP                  |
| `updated_at`      | TIMESTAMP / DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### 3.2. `categories` (商品分類表 - 可選但建議)

| 欄位名稱    | 資料類型     | 約束/備註                                  |
| ----------- | ------------ | ------------------------------------------ |
| `id`        | INT          | PRIMARY KEY, AUTO_INCREMENT                |
| `name`      | VARCHAR(255) | UNIQUE, NOT NULL                           |
| `description` | TEXT         |                                            |
| `created_at`| TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                  |
| `updated_at`| TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### 3.3. `products` (商品表)

| 欄位名稱      | 資料類型             | 約束/備註                                  |
| ------------- | -------------------- | ------------------------------------------ |
| `id`          | INT / BIGINT         | PRIMARY KEY, AUTO_INCREMENT                |
| `name`        | VARCHAR(255)         | NOT NULL                                   |
| `description` | TEXT                 |                                            |
| `price`       | DECIMAL(10, 2)       | NOT NULL                                   |
| `stock`       | INT                  | NOT NULL, DEFAULT 0                        |
| `image_url`   | VARCHAR(2048)        |                                            |
| `category_id` | INT                  | FOREIGN KEY (references `categories.id`), NULLABLE (如果沒有分類表則不需要) |
| `created_at`  | TIMESTAMP / DATETIME | DEFAULT CURRENT_TIMESTAMP                  |
| `updated_at`  | TIMESTAMP / DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### 3.4. `orders` (訂單表)

| 欄位名稱           | 資料類型             | 約束/備註                                  |
| ------------------ | -------------------- | ------------------------------------------ |
| `id`               | INT / BIGINT         | PRIMARY KEY, AUTO_INCREMENT                |
| `user_id`          | INT / BIGINT         | FOREIGN KEY (references `users.id`), NOT NULL |
| `total_amount`     | DECIMAL(10, 2)       | NOT NULL                                   |
| `status`           | VARCHAR(50)          | NOT NULL (e.g., 'pending', 'paid', 'shipped', 'delivered', 'cancelled') |
| `shipping_address` | JSON / TEXT          | (可儲存詳細地址結構)                          |
| `payment_method`   | VARCHAR(100)         | (初期可為模擬)                               |
| `created_at`       | TIMESTAMP / DATETIME | DEFAULT CURRENT_TIMESTAMP                  |
| `updated_at`       | TIMESTAMP / DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### 3.5. `order_items` (訂單商品表 - 訂單與商品的多對多關聯)

| 欄位名稱           | 資料類型       | 約束/備註                                  |
| ------------------ | -------------- | ------------------------------------------ |
| `id`               | INT / BIGINT   | PRIMARY KEY, AUTO_INCREMENT                |
| `order_id`         | INT / BIGINT   | FOREIGN KEY (references `orders.id`), NOT NULL |
| `product_id`       | INT / BIGINT   | FOREIGN KEY (references `products.id`), NOT NULL |
| `quantity`         | INT            | NOT NULL                                   |
| `price_at_purchase`| DECIMAL(10, 2) | NOT NULL (下單時的商品單價)                  |
| `created_at`       | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP                  |

### 3.6. 關聯與索引建議 for TiDB

*   **外鍵 (Foreign Keys):** Tortoise ORM 會處理這些關聯。TiDB 支持外鍵約束，但主要用於元數據，不完全像傳統 MySQL 那樣強制執行。重點是應用層邏輯要保證數據完整性。
*   **主鍵 (Primary Keys):** 自動建立索引。
*   **二級索引 (Secondary Indexes):**
    *   `users.email` (用於登入查詢)
    *   `products.name` (用於商品搜索或排序)
    *   `products.category_id` (如果使用分類)
    *   `orders.user_id` (查詢使用者歷史訂單)
    *   `orders.status` (按狀態篩選訂單)
    *   `order_items.order_id`
    *   `order_items.product_id`

## 4. API 端點設計 (RESTful API)

所有 API 路徑建議以 `/api` 作為前綴。所有請求和回應的 JSON 主體都應使用 Pydantic 模型進行定義和驗證。

### 4.1. 認證 (Auth) - `/api/auth`

*   **`POST /register`**: 使用者註冊
    *   **Request Body**: `UserCreate(username: str, email: EmailStr, password: str)`
    *   **Response Body (Success 201)**: `UserOut(id: int, username: str, email: EmailStr)` & `Message(message: str)`
    *   **Response Body (Error 400/409)**: `ErrorDetail(detail: str)`
    *   **邏輯**: 驗證輸入，檢查 email 和 username 是否已存在，雜湊密碼，存儲使用者。
*   **`POST /login`**: 使用者登入
    *   **Request Body**: `UserLogin(email: EmailStr, password: str)`
    *   **Response Body (Success 200)**: `Token(access_token: str, token_type: str, user: UserOut, message: str)`
    *   **Response Body (Error 400/401)**: `ErrorDetail(detail: str)`
    *   **邏輯**: 驗證使用者憑證，生成 JWT token。
*   **`POST /logout`**: 使用者登出 (可選，主要由前端清除 token)
    *   **Request Body**: (無，依賴 Header 中的 Token)
    *   **Response Body (Success 200)**: `Message(message: str)`
    *   **邏輯**: 如果後端需要追蹤 token 黑名單，則在此處處理。對於簡單 DEMO，可能僅前端操作。
*   **`GET /me`**: 獲取當前登入使用者資訊
    *   **Request Header**: `Authorization: Bearer <token>`
    *   **Response Body (Success 200)**: `UserOut`
    *   **Response Body (Error 401/403)**: `ErrorDetail(detail: str)`
    *   **邏輯**: 驗證 JWT token，返回使用者資訊。

### 4.2. 使用者資料 (Users/Profile) - `/api/users`

*   **`GET /me/profile`**: 獲取當前登入使用者的完整資料 (與 `/api/auth/me` 功能可能重疊，可擇一或合併)
    *   **Request Header**: `Authorization: Bearer <token>`
    *   **Response Body (Success 200)**: `UserProfile(id: int, username: str, email: EmailStr, created_at: datetime, ...)`
    *   **Response Body (Error 401/403)**: `ErrorDetail(detail: str)`
*   **`PUT /me/profile`**: 更新當前登入使用者資料
    *   **Request Header**: `Authorization: Bearer <token>`
    *   **Request Body**: `UserProfileUpdate(username: Optional[str] = None, ...)` (只允許更新特定欄位)
    *   **Response Body (Success 200)**: `UserProfile`
    *   **Response Body (Error 400/401/403)**: `ErrorDetail(detail: str)`

### 4.3. 商品 (Products) - `/api/products`

*   **`GET /`**: 獲取商品列表
    *   **Query Parameters**: `skip: int = 0`, `limit: int = 10`, `category: Optional[str] = None`, `sort_by: Optional[str] = None` (e.g., 'price_asc', 'price_desc', 'name_asc')
    *   **Response Body (Success 200)**: `List[ProductOut(id: int, name: str, price: float, image_url: Optional[str], ...)]`
    *   **邏輯**: 支持分頁、分類篩選、排序。
*   **`GET /{product_id}`**: 獲取單一商品詳情
    *   **Path Parameter**: `product_id: int`
    *   **Response Body (Success 200)**: `ProductDetailOut(id: int, name: str, description: Optional[str], price: float, stock: int, image_url: Optional[str], category: Optional[CategoryOut], ...)`
    *   **Response Body (Error 404)**: `ErrorDetail(detail: "Product not found")`
*   **`GET /bestsellers`**: 獲取熱銷商品列表
    *   **Query Parameters**: `limit: int = 5`
    *   **Response Body (Success 200)**: `List[ProductOut]`
    *   **邏輯**: 根據 `order_items` 表的銷售數量進行聚合分析。

### 4.4. 訂單 (Orders) - `/api/orders` (所有端點需要認證)

*   **`POST /`**: 創建新訂單 (結帳)
    *   **Request Header**: `Authorization: Bearer <token>`
    *   **Request Body**: `OrderCreate(items: List[OrderItemCreate(product_id: int, quantity: int)], shipping_address: ShippingAddressModel, payment_method: str)`
    *   **Response Body (Success 201)**: `OrderOut(id: int, user_id: int, total_amount: float, status: str, created_at: datetime, items: List[OrderItemOut], ...)`
    *   **Response Body (Error 400/401/402/404)**: `ErrorDetail(detail: str)` (e.g., "Insufficient stock", "Product not found")
    *   **邏輯**:
        1.  驗證購物車商品庫存。
        2.  計算總金額。
        3.  **在一個事務 (Transaction) 中**:
            *   創建 `orders` 記錄。
            *   創建 `order_items` 記錄。
            *   更新 `products` 表中的庫存。
        4.  (可選) 模擬支付處理。
*   **`GET /`**: 獲取當前使用者的歷史訂單列表
    *   **Request Header**: `Authorization: Bearer <token>`
    *   **Query Parameters**: `skip: int = 0`, `limit: int = 10`, `status: Optional[str] = None`
    *   **Response Body (Success 200)**: `List[OrderSummaryOut(id: int, total_amount: float, status: str, created_at: datetime, item_count: int)]`
*   **`GET /{order_id}`**: 獲取特定訂單詳情
    *   **Request Header**: `Authorization: Bearer <token>`
    *   **Path Parameter**: `order_id: int`
    *   **Response Body (Success 200)**: `OrderOut` (包含訂單商品詳情)
    *   **Response Body (Error 401/403/404)**: `ErrorDetail(detail: str)`

## 5. 核心業務邏輯與 TiDB 整合

### 5.1. 使用者認證
*   密碼儲存：使用 `passlib` 進行密碼雜湊和驗證。
*   JWT：使用 `python-jose` 生成和驗證 JWT token，包含使用者 ID 和過期時間。Token 在 `Authorization` header 中以 `Bearer <token>` 形式傳遞。

### 5.2. 商品管理
*   庫存管理：在創建訂單時，必須以原子操作檢查並減少商品庫存。如果庫存不足，事務應回滾。
    ```python
    # Tortoise ORM 事務範例
    from tortoise import Tortoise, connections, run_async
    from tortoise.transactions import in_transaction

    async def create_order_transaction(order_data, items_data):
        async with in_transaction() as conn:
            # 1. 檢查所有商品的庫存
            for item in items_data:
                product = await Product.get(id=item.product_id).using_connection(conn)
                if product.stock < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Product {product.name} insufficient stock")
            
            # 2. 創建訂單
            order = await Order.create(**order_data, using_connection=conn)
            
            # 3. 創建訂單項目並更新庫存
            for item in items_data:
                await OrderItem.create(order_id=order.id, **item, using_connection=conn)
                product = await Product.get(id=item.product_id).using_connection(conn)
                product.stock -= item.quantity
                await product.save(using_connection=conn)
            return order
    ```

### 5.3. 訂單處理
*   事務性：訂單創建涉及 `orders` 表、`order_items` 表的寫入以及 `products` 表庫存的更新，必須確保這些操作的原子性。
*   訂單狀態：明確定義訂單狀態的轉換邏輯。

### 5.4. 熱銷排行榜
*   利用 TiDB 的 HTAP 能力，可以直接在最新的交易數據上進行分析。
*   查詢範例 (概念性 SQL，ORM 實現會不同):
    ```sql
    SELECT 
        p.id, 
        p.name, 
        p.price, 
        p.image_url, 
        SUM(oi.quantity) AS total_sold
    FROM 
        products p
    JOIN 
        order_items oi ON p.id = oi.product_id
    JOIN
        orders o ON oi.order_id = o.id
    WHERE 
        o.status NOT IN ('cancelled', 'pending_payment') -- 可根據業務定義哪些算有效銷量
    GROUP BY 
        p.id, p.name, p.price, p.image_url
    ORDER BY 
        total_sold DESC
    LIMIT 10;
    ```
*   Tortoise ORM 可以使用 annotate 和 aggregate 實現類似功能。

## 6. 初始資料載入 (Data Seeding)

*   **需求**: 根據前端企劃書第 4 節，需預載入商品資料和預設使用者帳號。
*   **實現方式**:
    *   編寫一個 Python 腳本，使用 Tortoise ORM 連接到 TiDB 並插入初始數據。
    *   或者，在 FastAPI 應用啟動時通過 `startup` 事件觸發數據載入邏輯 (僅限於開發環境或首次部署)。
    *   商品圖片：可使用 placeholder 服務或預先準備好的圖片 URL。
*   **範例資料 (參考前端企劃書)**:
    *   至少 3-5 個商品 (如 TiDB T-Shirt, HTAP 手冊等)。
    *   至少 1-2 個預設使用者 (如 `user@example.com` / `password123`)。

## 7. TiDB 特性應用與展示 (後端視角)

*   **高並發讀取**:
    *   API 設計：商品列表和詳情 API 應設計為無狀態且高效查詢。
    *   TiDB 角色：TiDB 的分散式架構和 Raft 共識確保了讀取操作的低延遲和高吞吐量。後端應充分利用異步 ORM 減少 I/O 等待。
*   **強一致性與 ACID 事務**:
    *   API 設計：訂單創建 (`POST /api/orders`) 和任何涉及庫存變更的操作必須在單個 ACID 事務中完成。
    *   TiDB 角色：TiDB 提供完整的 ACID 支持，確保數據在併發操作下的一致性和可靠性。
*   **HTAP (Hybrid Transactional/Analytical Processing)**:
    *   API 設計：熱銷排行榜 (`GET /api/products/bestsellers`) API 直接查詢最新的交易數據，無需複雜的 ETL。
    *   TiDB 角色：TiDB 的 TiFlash (列式存儲副本) 能夠加速分析型查詢，同時不影響 OLTP 負載。後端查詢應設計得能夠觸發 TiFlash (如果配置了)。
*   **水平擴展與高可用性**:
    *   後端應用設計：保持應用無狀態，方便水平擴展。
    *   TiDB 角色：TiDB 本身支持在線擴展/縮容和自動故障轉移。後端應用能從中受益，無需複雜的應用層 HA 邏輯。

## 8. 安全性考量

*   **輸入驗證**: 所有 API 的請求參數和 Body 都必須使用 Pydantic 模型進行嚴格驗證。
*   **身份驗證與授權**:
    *   使用 JWT 進行無狀態身份驗證。
    *   敏感操作的 API 端點需檢查 token 的有效性及使用者的權限。
*   **SQL 注入防範**: 使用 Tortoise ORM 可以有效避免 SQL 注入風險。
*   **密碼安全**: 使用 `passlib` 等庫對密碼進行加鹽雜湊。
*   **HTTPS**: 在生產環境部署時，必須使用 HTTPS。
*   **依賴安全**: 定期檢查並更新專案依賴，避免已知的安全漏洞。

## 9. 錯誤處理與日誌

*   **統一錯誤回應**: 使用 FastAPI 的 `RequestValidationError` 和自定義 `HTTPException` 處理程序，返回結構化的 JSON 錯誤回應。
    ```json
    // 成功
    { "data": { ... } } 
    // 或
    { "message": "操作成功" }

    // 失敗
    { "detail": "錯誤訊息" }
    // 或
    { "detail": [ { "loc": ["body", "field_name"], "msg": "錯誤描述", "type": "validation_error" } ] }
    ```
*   **日誌記錄**:
    *   使用 Python 標準的 `logging` 模組。
    *   記錄重要的應用事件、錯誤、API 請求和回應 (可選，注意敏感資訊過濾)。
    *   配置日誌級別 (DEBUG, INFO, WARNING, ERROR, CRITICAL)。

## 10. 開發階段建議

建議後端開發與前端開發並行，並按以下階段推進：

1.  **階段一: 基礎架構與核心認證 (配合前端階段一、二)**
    *   TiDB 環境搭建與連接配置。
    *   定義核心資料庫模型 (`users`, `products`)。
    *   實現使用者註冊 (`POST /api/auth/register`) 和登入 (`POST /api/auth/login`) API。
    *   實現獲取商品列表 (`GET /api/products`) 和商品詳情 (`GET /api/products/{product_id}`) API (初期可不含複雜篩選排序)。
    *   實現數據預載入腳本。
2.  **階段二: 訂單流程與會員功能 (配合前端階段二、三)**
    *   實現創建訂單 (`POST /api/orders`) API，包含完整的庫存檢查和事務處理。
    *   實現獲取使用者歷史訂單 (`GET /api/orders`) 和訂單詳情 (`GET /api/orders/{order_id}`) API。
    *   實現獲取/更新使用者資料 (`GET /api/users/me/profile`, `PUT /api/users/me/profile`) API。
3.  **階段三: 進階功能與優化 (配合前端階段四)**
    *   實現熱銷排行榜 (`GET /api/products/bestsellers`) API。
    *   完善商品列表的篩選、排序、分頁功能。
    *   進行 API 效能測試與優化。
    *   強化安全性措施。
4.  **階段四: 整體測試與部署準備**
    *   與前端進行完整流程的整合測試。
    *   編寫 API 文件 (FastAPI 自動生成 OpenAPI 文件，可補充說明)。
    *   準備生產環境部署配置。

## 11. 測試建議

*   **單元測試 (`pytest`)**:
    *   測試獨立的業務邏輯函數 (例如，服務層的函數)。
    *   Mock 資料庫依賴和外部服務。
*   **整合測試 (`pytest` 與測試資料庫)**:
    *   測試 API 端點的完整行為，包括與 TiDB (測試實例) 的交互。
    *   使用 `HTTPX` 或 FastAPI 的 `TestClient`。
    *   每個測試案例應在獨立的資料庫事務中運行，並在結束後回滾，以保持測試環境的清潔。
*   **效能測試**:
    *   使用 `locust` 或 `k6` 等工具對關鍵 API (如商品列表、下單) 進行壓力測試。

此計畫書為後端開發提供了指導框架，開發過程中可根據實際情況進行調整和細化。 