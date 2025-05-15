from fastapi import FastAPI, HTTPException, status, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)
from datetime import datetime # For order date

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

class AuthSuccessResponse(BaseModel):
    message: str = "註冊成功！"
    token: str
    user: UserResponse

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

# --- Mock API Endpoints ---

@app.post("/api/auth/register", response_model=AuthSuccessResponse, status_code=status.HTTP_201_CREATED)
async def mock_register_user(registration_data: UserRegistrationRequest):
    """
    Mocks a user registration endpoint.
    """
    print(f"模擬後端：收到註冊請求，資料: {registration_data.model_dump()}")

    mock_user_id = str(uuid.uuid4()) # Generate a unique ID for the user
    # Ensure the token contains this mock_user_id in a parseable way for get_current_user_id
    mock_token = f"mocktoken_{int(time.time())}_{mock_user_id}" 

    mock_user = UserResponse(
        id=mock_user_id, # UserResponse ID must match the ID in the token
        name=registration_data.name,
        email=registration_data.email
    )

    response_data = AuthSuccessResponse(
        token=mock_token,
        user=mock_user
    )
    
    print(f"模擬後端：回傳成功回應: {response_data.model_dump()}")
    return response_data

@app.post("/api/auth/login", response_model=AuthSuccessResponse, status_code=status.HTTP_200_OK)
async def mock_login_user(login_data: UserLoginRequest):
    """
    Mocks a user login endpoint.
    In a real app, you would validate credentials against a database.
    Here, we'll just mock a successful login if email and password are provided
    and generate a token similar to registration.
    """
    print(f"模擬後端：收到登入請求，資料: {login_data.model_dump()}")

    # Extremely simplified mock validation:
    if not login_data.email or not login_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )

    # In a real scenario, you'd look up the user by email and verify the password.
    # For this mock, we'll generate a new mock_user_id based on email for simplicity
    # or retrieve a stored one if you have a mock user store.
    # To keep it consistent with how get_current_user_id might expect a user ID,
    # let's create a user_id from the email.
    mock_user_id = f"user_{login_data.email.split('@')[0]}" # Simplified user ID

    mock_token = f"mocktoken_{int(time.time())}_{mock_user_id}"

    # Mock user details (in real app, fetch from DB)
    # We don't have the user's name from the login request, so we'll use a placeholder or part of the email.
    mock_user = UserResponse(
        id=mock_user_id,
        name=login_data.email.split('@')[0].capitalize(), # Use part of email as name
        email=login_data.email
    )

    response_data = AuthSuccessResponse(
        message="登入成功！", # Changed message
        token=mock_token,
        user=mock_user
    )
    
    print(f"模擬後端：登入成功，回傳回應: {response_data.model_dump()}")
    return response_data

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

# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000") 
