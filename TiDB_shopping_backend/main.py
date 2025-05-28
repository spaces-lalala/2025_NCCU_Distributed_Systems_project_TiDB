
from fastapi import FastAPI, HTTPException, status, Depends, Header,APIRouter,Path

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)
from datetime import datetime # For order date
from database import engine, SessionLocal, get_db
from models import Base, User
from sqlalchemy.orm import Session
from utils import hash_password
import uuid
from utils import verify_password, hash_password
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Optional


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
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class ShippingAddressModel(BaseModel):
    address: str
    city: str
    postal_code: str
    country: str

class OrderItemOut(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]

class OrderSummaryOut(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    item_count: int
# -------------------- JWT-based Authentication --------------------

# Secret key for signing JWTs
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

# 添加缺失的 ProductOut 和 OrderOut 類別

class CategoryOut(BaseModel):
    id: int
    name: str

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None
    sold: Optional[int]
    
class ProductDetailOut(ProductOut):
    description: Optional[str] = None
    stock: int
    category: Optional[CategoryOut] = None

class ErrorDetail(BaseModel):
    detail: str
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
def register_user(
    registration_data: UserRegistrationRequest,
    db: Session = Depends(get_db)
):
    # 檢查 email 是否已註冊
    existing_user = db.query(User).filter(User.email == registration_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email 已註冊")

    # 雜湊密碼
    hashed_pw = hash_password(registration_data.password)

    # 建立新 User
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        name=registration_data.name,
        email=registration_data.email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 產生 JWT Token
    token = create_access_token(user_id)

    # 回傳格式
    return AuthSuccessResponse(
        message= "註冊成功！",
        token=token,
        user=UserResponse(
            id=user_id,
            name=new_user.name,
            email=new_user.email
        )
    )

@app.post("/api/auth/login", response_model=AuthSuccessResponse, status_code=status.HTTP_200_OK)
def login_user(login_data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="帳號不存在")

    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="密碼錯誤")

    token = create_access_token(user.id)

    return AuthSuccessResponse(
        message="登入成功！",
        token=token,
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email
        )
    )


@app.post("/api/auth/logout")
def logout():
    """
    Mocks a user logout endpoint.
    """
    # 使用者登出邏輯 (可選，主要由前端清除 token)
    return {"message": "User logged out successfully"}

# --------- /api/auth/me ----------
@app.get("/api/auth/me", response_model=UserResponse)
def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    print(f"後端查詢：使用者 {current_user_id} 請求當前登入資訊...")

    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="使用者不存在")

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email
    )

# --------- GET /me/profile ----------
@app.get("/me/profile", response_model=UserProfile)
def get_current_user(current_user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="使用者不存在")

    return UserResponse(id=user.id, name=user.name, email=user.email)

# --------- PUT /me/profile ----------
@app.put("/me/profile", response_model=UserProfile)
def update_user_profile(
    update: UserProfileUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="使用者資料不存在")

    if update.username:
        user.name = update.username

    db.commit()
    db.refresh(user)
    return UserProfile(username=user.name)


# --------- Products Router  ----------
from products import mock_categories, mock_products
@app.get("/api/products", response_model=List[ProductOut])
def get_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    sort_by: Optional[str] = None
):
    products = mock_products.copy()

    # 篩選分類
    if category:
        cat = next((c for c in mock_categories if c["name"] == category), None)
        if cat:
            products = [p for p in products if p["category_id"] == cat["id"]]
        else:
            products = []

    # 排序
    if sort_by == "price_asc":
        products.sort(key=lambda x: x["price"])
    elif sort_by == "price_desc":
        products.sort(key=lambda x: -x["price"])
    elif sort_by == "name_asc":
        products.sort(key=lambda x: x["name"])

    # 分頁
    paginated = products[skip: skip + limit]

    return paginated

@app.get("/api/products/bestsellers", response_model=List[ProductOut])
def get_bestsellers(limit: int = 5):
    top_products = sorted(mock_products, key=lambda x: -x["sold"])[:limit]
    return top_products

@app.get("/api/products/{product_id}", response_model=ProductDetailOut, responses={404: {"model": ErrorDetail}})
def get_product_detail(product_id: int = Path(..., ge=1)):
    product = next((p for p in mock_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category = next((c for c in mock_categories if c["id"] == product["category_id"]), None)
    product_detail = {
        **product,
        "category": category
    }
    return product_detail


@app.get("/api/orders/", response_model=List[OrderSummaryOut]) # Frontend expects a list of orders directly
def get_user_orders(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    orders = [o for o in mock_orders if o["user_id"] == current_user.id]
    if status:
        orders = [o for o in orders if o["status"] == status]

    summaries = [
        {
            "id": o["id"],
            "total_amount": o["total_amount"],
            "status": o["status"],
            "created_at": o["created_at"],
            "item_count": sum(item["quantity"] for item in o["items"])
        }
        for o in orders[skip: skip + limit]
    ]
    return summaries

@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order_detail(
    order_id: int,
    current_user: dict = Depends(get_current_user)
):
    order = next((o for o in mock_orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return order

@app.post("/api/orders/", response_model=OrderOut, status_code=201)
def create_order(
    order_data: dict,
    current_user: dict = Depends(get_current_user)
):
    global order_id_seq
    items = order_data["items"]
    shipping = order_data["shipping_address"]
    payment_method = order_data["payment_method"]

    order_items = []
    total = 0

    for item in items:
        product = next((p for p in mock_products if p["id"] == item["product_id"]), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product["stock"] < item["quantity"]:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        product["stock"] -= item["quantity"]
        total += product["price"] * item["quantity"]
        order_items.append({
            "product_id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": item["quantity"]
        })

    order = {
        "id": order_id_seq,
        "user_id": current_user.id,
        "total_amount": total,
        "status": "paid",
        "created_at": datetime.now(),
        "items": order_items,
        "shipping": shipping,
        "payment_method": payment_method
    }
    order_id_seq += 1
    mock_orders.append(order)

    return order

# @app.get("/api/products/{product_id}", response_model=ProductOut)
# def get_product_detail(product_id: int, db=Depends(get_db)):
#     """
#     Mocks an endpoint to get product details by product ID.
#     """
#     print(f"模擬後端：請求商品詳情，商品ID: {product_id}")

#     # In a real app, you would fetch the product from the database.
#     # Here, we'll just mock a product detail response.
#     mock_product = ProductOut(
#         id=product_id,
#         name="Mock Product " + str(product_id),
#         description="This is a mock product description.",
#         price=19.99,
#         stock=100,
#         category="Mock Category",
#         image_url="https://via.placeholder.com/150"
#     )

#     print(f"模擬後端：回傳商品詳情: {mock_product.model_dump()}")
#     return mock_product

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

# @app.get("/api/orders/{order_id}", response_model=OrderOut)
# def get_order_detail(order_id: int, db=Depends(get_db)):
#     """
#     Mocks an endpoint to get order details by order ID.
#     """
#     print(f"模擬後端：請求訂單詳情，訂單ID: {order_id}")

#     # In a real app, you would fetch the order from the database.
#     # Here, we'll just mock an order detail response.
#     mock_order = OrderOut(
#         id=order_id,
#         orderNumber="ORD-2023-00001",
#         orderDate="2023-10-26T10:00:00Z",
#         totalAmount=74.99,
#         status="DELIVERED",
#         items=[
#             OrderItemBase(productId="prod_mock_001", productName="TiDB 官方限量版 T-Shirt", quantity=1, price=25.00),
#             OrderItemBase(productId="prod_mock_002", productName="高效能HTAP資料庫實戰手冊", quantity=1, price=49.99),
#         ],
#         userId="user_user" # Mock user ID
#     )

#     print(f"模擬後端：回傳訂單詳情: {mock_order.model_dump()}")
#     return mock_order

mock_product_catalog = {
    "prod_mock_001": {"productName": "TiDB 官方限量版 T-Shirt", "price": 25.00, "image": "@/assets/images/tidb-shirt.png"},
    "prod_mock_002": {"productName": "高效能HTAP資料庫實戰手冊", "price": 49.99, "image": "@/assets/images/HTAP.png"},
    "prod_mock_003": {"productName": "TiDB 雲服務體驗券 (1個月)", "price": 0.00, "image": "@/assets/images/cloud.png"},
    "prod_mock_004": {"productName": "PingCAP 定製鍵帽組", "price": 15.00, "image": "@/assets/images/pingcap.png"},
    "prod_mock_005": {"productName": "TiDB牌純棉被", "price": 400.00, "image": "@/assets/images/tidbquilt.png"},
}


#注意這裡可能會發生錯誤所以先註解掉，後端人記得要接到這裡，這裡是熱銷排行榜

# @app.get("/api/products/bestsellers", response_model=List[BestSellerProduct])
# async def mock_get_best_sellers():
#     """
#     從所有訂單中統計出最熱銷的商品。
#     """
#     print("模擬後端：統計熱銷商品中...")

#     # 統計每個商品的銷量
#     sales_counter: dict[str, dict] = {}  # { productId: { name, totalSold, price, image } }

#     for order in mock_all_users_orders:
#         for item in order.items:
#             pid = item.productId
#             if pid not in sales_counter:
#                 product_info = mock_product_catalog.get(pid, {})
#                 sales_counter[pid] = {
#                     "productId": pid,
#                     "productName": item.productName,
#                     "totalSold": 0,
#                     "price": product_info.get("price", item.price),
#                     "image": product_info.get("image", ""),
#                 }
#             sales_counter[pid]["totalSold"] += item.quantity

#     sorted_products = sorted(sales_counter.values(), key=lambda x: x["totalSold"], reverse=True)

#     print(f"模擬後端：共統計出 {len(sorted_products)} 項商品")
#     return sorted_products


# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000")
