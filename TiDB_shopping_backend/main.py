from fastapi import FastAPI, HTTPException, status, Depends, Header
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)

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
        if len(token_parts) < 3 or token_parts[0] != 'mocktoken':
            raise ValueError("Token format incorrect or not a mock token")
        mock_user_id_from_token = token_parts[-1]
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
    """
    print(f"模擬後端：使用者 {current_user_id} 請求歷史訂單...")

    mock_orders_data: List[OrderBase] = []

    # You can have different mock orders for different mock user IDs if needed
    # For simplicity, returning the same mock orders for any authenticated mock user
    if current_user_id: 
        mock_orders_data = [
            OrderBase(
                id="order_mock_001_user_" + current_user_id[:4], # Make order ID somewhat unique to user
                orderNumber="ORD-2023-00001",
                orderDate="2023-10-26T10:00:00Z",
                totalAmount=74.99,
                status="DELIVERED",
                items=[
                    OrderItemBase(productId="prod_mock_001", productName="TiDB 官方限量版 T-Shirt", quantity=1, price=25.00),
                    OrderItemBase(productId="prod_mock_002", productName="高效能HTAP資料庫實戰手冊", quantity=1, price=49.99),
                ]
            ),
            OrderBase(
                id="order_mock_002_user_" + current_user_id[:4],
                orderNumber="ORD-2023-00005",
                orderDate="2023-11-15T14:30:00Z",
                totalAmount=15.00,
                status="SHIPPED",
                items=[
                    OrderItemBase(productId="prod_mock_004", productName="PingCAP 定製鍵帽組", quantity=1, price=15.00),
                ]
            )
        ]
    
    print(f"模擬後端：為使用者 {current_user_id} 回傳 {len(mock_orders_data)} 筆模擬訂單。")
    return mock_orders_data

# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000")
