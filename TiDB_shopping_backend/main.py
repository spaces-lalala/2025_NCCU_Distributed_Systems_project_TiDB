from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import uuid # For generating a mock user ID
import time # For generating a mock token (very basic)

app = FastAPI()

# --- Pydantic Models ---

class UserRegistrationRequest(BaseModel):
    name: str
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

# --- Mock API Endpoint ---

@app.post("/auth/register", response_model=AuthSuccessResponse, status_code=status.HTTP_201_CREATED)
async def mock_register_user(registration_data: UserRegistrationRequest):
    """
    Mocks a user registration endpoint.
    It receives user data and returns a simulated success response.
    Does NOT interact with any database.
    """
    print(f"模擬後端：收到註冊請求，資料: {registration_data.model_dump()}")

    # Simulate creating a new user
    mock_user_id = str(uuid.uuid4())
    mock_token = f"mock_jwt_token_{int(time.time())}_{mock_user_id[:8]}"

    mock_user = UserResponse(
        id=mock_user_id,
        name=registration_data.name,
        email=registration_data.email
    )

    response_data = AuthSuccessResponse(
        token=mock_token,
        user=mock_user
    )
    
    print(f"模擬後端：回傳成功回應: {response_data.model_dump()}")
    return response_data

# --- Optional: Root endpoint for testing if the server is up ---
@app.get("/")
async def read_root():
    return {"message": "模擬後端伺服器已啟動"}

if __name__ == "__main__":
    import uvicorn
    # It's better to run uvicorn from the command line for more options
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("請從終端機執行: uvicorn TiDB_shopping_backend.main:app --reload --port 8000") 