
from fastapi import FastAPI, HTTPException, status, Depends, Header,APIRouter,Path

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)
from datetime import datetime # For order date
from database import engine, SessionLocal, get_db
from database import Base
from api import orders, payments, products
from models import order_item, order, product, User, Product, Category
from api import items
from dependencies.auth import get_current_user_id
from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI()
# ------------------------------
# 🔧 CORS 中介層設定
# 這段設定允許前端從不同的網域（如 http://localhost:3000）存取後端 API。
# 開發階段設為允許所有來源（"*"），部署時請改為指定 domain 以確保安全性。
# 官方說明：https://fastapi.tiangolo.com/tutorial/cors/
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(orders.router)
#app.include_router(users.router)
app.include_router(products.router)
app.include_router(payments.router)
app.include_router(items.router)
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
    category_name: Optional[str]
    
class ProductDetailOut(ProductOut):
    # description: Optional[str] = None
    # stock: int
    # category: Optional[CategoryOut] = None
    id: int
    name: str
    price: float
    image_url: Optional[str]
    sold: Optional[int]
    stock: int
    description: Optional[str]
    category_name: Optional[str]
    
class ErrorDetail(BaseModel):
    detail: str

# 添加缺失的 get_db 函數
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
@app.get("/api/products", response_model=List[ProductOut])
def get_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # products = mock_products.copy()
    query = db.query(Product)

    # 篩選分類
    if category:
        cat = db.query(Category).filter(Category.name == category).first()
        if cat:
            query = query.filter(Product.category_name == cat.name)
        else:
            return []

    # 排序
    if sort_by == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort_by == "name_asc":
        query = query.order_by(Product.name.asc())

    products = query.offset(skip).limit(limit).all()
    return products

@app.get("/api/products/bestsellers", response_model=List[ProductOut])
def get_bestsellers(limit: int = 5, db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .order_by(Product.sold.desc())
        .limit(limit)
        .all()
    )
    return products


@app.get("/api/products/{product_id}", response_model=ProductDetailOut, responses={404: {"model": ErrorDetail}})
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    """
    Fetch product details, including description, from the database.
    """
    # 查詢資料庫中的產品
    search_id = f"1{product_id}"
    product = db.query(Product).filter(Product.id == search_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 返回產品詳細資訊，包括 description
    return ProductDetailOut(
    id=product.id,
    name=product.name,
    description=product.description,
    price=product.price,
    image_url=product.image_url,
    sold=product.sold,
    stock=product.stock,
    category_name=product.category_name
)


@app.get("/api/orders/", response_model=List[OrderSummaryOut]) # Frontend expects a list of orders directly
def get_user_orders(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # 這裡應該從資料庫查詢訂單，而不是使用 mock 資料
    # TODO: 實作從資料庫查詢訂單的邏輯
    return []

@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order_detail(
    order_id: int,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # 這裡應該從資料庫查詢特定訂單，而不是使用 mock 資料
    # TODO: 實作從資料庫查詢訂單詳情的邏輯
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/api/orders/", response_model=OrderOut, status_code=201)
def create_order(
    order_data: dict,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # 這裡應該在資料庫中創建訂單，而不是使用 mock 資料
    # TODO: 實作在資料庫中創建訂單的邏輯
    raise HTTPException(status_code=501, detail="Order creation not yet implemented")



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




# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000")
