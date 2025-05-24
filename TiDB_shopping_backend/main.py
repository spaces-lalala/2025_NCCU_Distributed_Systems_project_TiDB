from fastapi import FastAPI, HTTPException, status, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)
from datetime import datetime # For order date
from database import engine, SessionLocal
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Pydantic Models ---

class UserRegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
class LoginResponse(BaseModel):
    message: str = "登入成功！"
    access_token: str  
    token_type: str
    user: UserResponse

class AuthSuccessResponse(BaseModel):
    message: str = "註冊成功！"
    token: str
    user: UserResponse

class UserCreate(BaseModel):
    name: str  # 將 username 改為 name
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
    message: str

class UserProfile(BaseModel):
    id: str
    username: str
    email: EmailStr
    created_at: datetime

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
# --- Order Models (matching frontend TypeScript interfaces) ---
class OrderItemBase(BaseModel):
    productId: str
    productName: str
    quantity: int
    price: float

class OrderBase(BaseModel):
    id: str
    orderNumber: str
    orderDate: str # ISO date string preferred
    totalAmount: float
    status: str # e.g., 'PENDING', 'DELIVERED'
    items: List[OrderItemBase]
    userId: str # Add this to associate order with user

# This will store all orders created during the session for mock purposes
mock_all_users_orders: List[OrderBase] = []

class OrderCreationRequest(BaseModel): # Add this model for creating new orders
    items: List[OrderItemBase]
    totalAmount: float
    # Potentially other fields like shippingAddress, paymentMethod could be added

# Optional: If API were to return { "orders": [...] }
# class OrdersResponse(BaseModel):
#     orders: List[OrderBase]

# --- Mock Authentication ---
async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        print("模擬後端：缺少 Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (missing token)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = authorization.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        print(f"模擬後端：Authorization header 格式錯誤: {authorization}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = parts[1]
    print(f"模擬後端：收到的 Token: {token}")
    
    # Very basic mock token parsing: assumes token is "mocktoken_timestamp_userid"
    try:
        token_parts = token.split('_')
        if len(token_parts) < 3: # Must have at least mocktoken, timestamp, and one part for user_id
            raise ValueError("Token format too short or not a mock token")
        
        # The user_id is everything after the first two parts ("mocktoken" and timestamp)
        mock_user_id_from_token = "_".join(token_parts[2:])
        
        if not mock_user_id_from_token: # Basic check
             raise ValueError("Token user ID part is empty")
        print(f"模擬後端：從 Token 中模擬解析到的 User ID: {mock_user_id_from_token}")
        return mock_user_id_from_token 
    except Exception as e:
        print(f"模擬後端：無法從 Token 中解析 User ID: {e} (Token: {token})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token - cannot parse user id",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 添加缺失的 ProductOut 和 OrderOut 類別

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str]

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str

# 添加缺失的 get_db 函數
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Mock API Endpoints ---

@app.post("/api/auth/register", response_model=AuthSuccessResponse, status_code=status.HTTP_201_CREATED)
async def mock_register_user(registration_data: UserRegistrationRequest):
    """
    Mocks a user registration endpoint.
    """
    print(f"模擬後端：收到註冊請求，資料: {registration_data.model_dump()}")

    mock_user_id = str(uuid.uuid4())  # Generate a unique ID for the user
    mock_token = f"mocktoken_{int(time.time())}_{mock_user_id}"

    mock_user = UserResponse(
        id=mock_user_id,
        name=registration_data.name,
        email=registration_data.email
    )

    # **修正：將使用者資料存入 mock_user_db**
    mock_user_db[mock_user_id] = UserProfile(
        id=mock_user_id,
        username=registration_data.name,
        email=registration_data.email,
        created_at=datetime.now()
    )

    response_data = AuthSuccessResponse(
        token=mock_token,
        user=mock_user
    )

    print(f"模擬後端：回傳成功回應: {response_data.model_dump()}")
    return response_data

@app.post("/api/auth/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def mock_login_user(login_data: UserLoginRequest):
    """
    Mocks a user login endpoint.
    """
    print(f"模擬後端：收到登入請求，資料: {login_data.model_dump()}")

    if not login_data.email or not login_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )

    mock_user_id = f"user_{login_data.email.split('@')[0]}"
    mock_token = f"mocktoken_{int(time.time())}_{mock_user_id}"

    mock_user = UserResponse(
        id=mock_user_id,
        name=login_data.email.split('@')[0].capitalize(),
        email=login_data.email
    )

    response_data = {
        "message": "登入成功！",
        "access_token": mock_token,  # 修改字段名稱
        "token_type": "bearer",
        "user": mock_user
    }

    print(f"模擬後端：登入成功，回傳回應: {response_data}")
    return response_data

@app.post("/api/auth/logout")
def logout():
    """
    Mocks a user logout endpoint.
    """
    # 使用者登出邏輯 (可選，主要由前端清除 token)
    return {"message": "User logged out successfully"}

mock_user_db: Dict[str, "UserProfile"] = {}  # 用 user_id 當 key 儲存 mock 使用者
# --------- /api/auth/me ----------
@app.get("/api/auth/me", response_model=UserResponse)
def get_current_user(current_user_id: str = Depends(get_current_user_id)):
    """
    模擬取得當前登入使用者資訊的 API。
    根據 token 中的 user_id（格式如 'user_username'）來組合 mock user 資訊。
    """
    print(f"模擬後端：使用者 {current_user_id} 請求當前登入資訊...")

    try:
        username = current_user_id.split('_', 1)[1]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid user ID format.")

    # 建立 mock 使用者
    mock_user = UserResponse(
        id=current_user_id,
        name=username.capitalize(),
        email=f"{username}@example.com"
    )

    print(f"模擬後端：回傳當前使用者資訊: {mock_user.model_dump()}")
    return mock_user

# --------- GET /me/profile ----------
@app.get("/me/profile", response_model=UserProfile)
def get_user_profile(current_user_id: str = Depends(get_current_user_id)):
    print(f"模擬後端：使用者 {current_user_id} 請求 profile...")

    user = mock_user_db.get(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="使用者資料不存在")

    return user

# --------- PUT /me/profile ----------
@app.put("/me/profile", response_model=UserProfile)
def update_user_profile(
    update: UserProfileUpdate,
    current_user_id: str = Depends(get_current_user_id)
):
    print(f"模擬後端：使用者 {current_user_id} 請求更新 profile: {update.model_dump()}")
    user = mock_user_db.get(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="使用者資料不存在")

    if update.username:
        user.username = update.username

    return user



@app.get("/api/orders", response_model=List[OrderBase]) # Frontend expects a list of orders directly
async def mock_get_orders_for_user(current_user_id: str = Depends(get_current_user_id)):
    """
    Mocks an endpoint to get orders for the authenticated user.
    Now it filters orders from the global mock_all_users_orders list.
    """
    print(f"模擬後端：使用者 {current_user_id} 請求歷史訂單...")

    # Filter orders from the global list for the current user
    print(f"模擬後端 DEBUG: mock_get_orders_for_user - 當前 mock_all_users_orders (顯示訂單ID和用戶ID): {[(o.id, o.userId) for o in mock_all_users_orders]}") # DEBUG
    user_orders = [order for order in mock_all_users_orders if order.userId == current_user_id]
    print(f"模擬後端 DEBUG: mock_get_orders_for_user - 為使用者 {current_user_id} 篩選到的訂單 (顯示訂單ID): {[o.id for o in user_orders]}") # DEBUG

    # BEGIN: Optional - Add initial mock orders if this is a specific demo user and they have no orders yet
    # This ensures that our main demo user always has some initial orders to show upon first login in a session.
    # These initial orders will also be added to mock_all_users_orders for this user.
    if current_user_id == "user_user" and not user_orders: # Assuming 'user_user' is the ID for 'user@example.com'
        print(f"模擬後端：為主要測試使用者 {current_user_id} 首次初始化模擬訂單...")
        initial_demo_orders = [
            OrderBase(
                id="order_mock_001_user_" + current_user_id[:4],
                orderNumber="ORD-2023-00001",
                orderDate="2023-10-26T10:00:00Z",
                totalAmount=74.99,
                status="DELIVERED",
                items=[
                    OrderItemBase(productId="prod_mock_001", productName="TiDB 官方限量版 T-Shirt", quantity=1, price=25.00),
                    OrderItemBase(productId="prod_mock_002", productName="高效能HTAP資料庫實戰手冊", quantity=1, price=49.99),
                ],
                userId=current_user_id
            ),
            OrderBase(
                id="order_mock_002_user_" + current_user_id[:4],
                orderNumber="ORD-2023-00005",
                orderDate="2023-11-15T14:30:00Z",
                totalAmount=15.00,
                status="SHIPPED",
                items=[
                    OrderItemBase(productId="prod_mock_004", productName="PingCAP 定製鍵帽組", quantity=1, price=15.00),
                ],
                userId=current_user_id
            )
        ]
        mock_all_users_orders.extend(initial_demo_orders) # Add to global list
        user_orders.extend(initial_demo_orders) # Also add to current response
    # END: Optional initial mock orders section

    print(f"模擬後端：為使用者 {current_user_id} 回傳 {len(user_orders)} 筆訂單。")
    return user_orders

@app.post("/api/orders", response_model=OrderBase, status_code=status.HTTP_201_CREATED)
async def mock_create_order(order_data: OrderCreationRequest, current_user_id: str = Depends(get_current_user_id)):
    """
    Mocks an endpoint to create a new order.
    """
    print(f"模擬後端：使用者 {current_user_id} 請求建立新訂單，資料: {order_data.model_dump()}")

    # In a real scenario, you'd validate the order data and create a new order in the database.
    # For this mock, we'll create a new order with a unique ID and the provided items.
    new_order = OrderBase(
        id=f"order_mock_{datetime.now().strftime('%Y%m%d%H%M%S')}_user_{current_user_id[:4]}",
        orderNumber=f"ORD-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
        orderDate=datetime.now().isoformat(),
        totalAmount=order_data.totalAmount,
        status="PENDING",
        items=order_data.items,
        userId=current_user_id
    )
    print(f"模擬後端 DEBUG: mock_create_order - 新建訂單物件: {new_order.model_dump()}") # DEBUG
    mock_all_users_orders.append(new_order)
    print(f"模擬後端 DEBUG: mock_create_order - mock_all_users_orders 目前長度: {len(mock_all_users_orders)}") # DEBUG
    print(f"模擬後端 DEBUG: mock_create_order - mock_all_users_orders 最後一筆訂單的用戶ID: {mock_all_users_orders[-1].userId if mock_all_users_orders else 'N/A'}") # DEBUG
    
    print(f"模擬後端：為使用者 {current_user_id} 建立新訂單，回傳回應: {new_order.model_dump()}")
    return new_order

@app.get("/api/products/{product_id}", response_model=ProductOut)
def get_product_detail(product_id: int, db=Depends(get_db)):
    """
    Mocks an endpoint to get product details by product ID.
    """
    print(f"模擬後端：請求商品詳情，商品ID: {product_id}")

    # In a real app, you would fetch the product from the database.
    # Here, we'll just mock a product detail response.
    mock_product = ProductOut(
        id=product_id,
        name="Mock Product " + str(product_id),
        description="This is a mock product description.",
        price=19.99,
        stock=100,
        category="Mock Category",
        image_url="https://via.placeholder.com/150"
    )

    print(f"模擬後端：回傳商品詳情: {mock_product.model_dump()}")
    return mock_product

@app.get("/api/products/bestsellers", response_model=List[ProductOut])
def get_bestsellers(limit: int = 5, db=Depends(get_db)):
    """
    Mocks an endpoint to get best-selling products.
    """
    print(f"模擬後端：請求熱銷商品，限制數量: {limit}")

    # In a real app, you would query the database for best-selling products.
    # Here, we'll just mock a list of best-selling products.
    mock_bestsellers = [
        ProductOut(
            id=i,
            name="Best Seller Product " + str(i),
            description="This is a best seller product description.",
            price=29.99 + i,
            stock=50 - i * 5,
            category="Best Seller Category",
            image_url="https://via.placeholder.com/150"
        ) for i in range(1, limit + 1)
    ]

    print(f"模擬後端：回傳熱銷商品列表，數量: {len(mock_bestsellers)}")
    return mock_bestsellers

@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order_detail(order_id: int, db=Depends(get_db)):
    """
    Mocks an endpoint to get order details by order ID.
    """
    print(f"模擬後端：請求訂單詳情，訂單ID: {order_id}")

    # In a real app, you would fetch the order from the database.
    # Here, we'll just mock an order detail response.
    mock_order = OrderOut(
        id=order_id,
        orderNumber="ORD-2023-00001",
        orderDate="2023-10-26T10:00:00Z",
        totalAmount=74.99,
        status="DELIVERED",
        items=[
            OrderItemBase(productId="prod_mock_001", productName="TiDB 官方限量版 T-Shirt", quantity=1, price=25.00),
            OrderItemBase(productId="prod_mock_002", productName="高效能HTAP資料庫實戰手冊", quantity=1, price=49.99),
        ],
        userId="user_user" # Mock user ID
    )

    print(f"模擬後端：回傳訂單詳情: {mock_order.model_dump()}")
    return mock_order

# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000")
