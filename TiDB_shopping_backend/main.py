
from fastapi import FastAPI, HTTPException, status, Depends, Header,APIRouter,Path

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)
from datetime import datetime # For order date
from database import engine, SessionLocal, get_db
from database import Base
from api import orders, payments, product
from models import order_item, order, User, Product, Category
from api import items
from dependencies.auth import get_current_user_id
from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(redirect_slashes=False)
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
app.include_router(product.router)
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

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"sub": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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


# 產品相關路由已移至 api/product.py 模組

# 訂單相關路由已移至 api/orders.py 模組







# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000")
