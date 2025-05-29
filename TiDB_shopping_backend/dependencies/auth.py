from fastapi import Header, HTTPException, status
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime

# JWT settings (should match main.py)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# --- JWT Authentication ---
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
    
    # JWT token validation
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError("Token payload missing 'sub' field")
        
        print(f"模擬後端：從 JWT Token 中解析到的 User ID: {user_id}")
        return user_id
    except JWTError as e:
        print(f"模擬後端：JWT Token 驗證失敗: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"模擬後端：驗證 Token 時發生未知錯誤: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Mock API Endpoints ---