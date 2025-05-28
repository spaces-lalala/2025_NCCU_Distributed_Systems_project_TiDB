from fastapi import Header, HTTPException, status
from typing import Optional

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