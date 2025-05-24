from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/api/auth/register", json={
        "name": "testuser",  # 注意：這裡對應的是 UserRegistrationRequest 裡的 name
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 201

    data = response.json()
    assert "token" in data
    assert "user" in data

    user = data["user"]
    assert user["name"] == "testuser"
    assert user["email"] == "test@example.com"
    assert "id" in user

def test_login_user():
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "user" in data

    user = data["user"]
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test"  # 根據 email 前綴自動產生的名稱
    assert user["id"] == "user_test"  # 根據 email 產生的 user_id


def test_get_current_user():
    # 先登入以取得 access_token
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 呼叫 /api/auth/me 並帶上 Authorization 標頭
    response = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200

    user_data = response.json()
    assert user_data["email"] == "test@example.com"
    assert user_data["name"] == "Test"
    assert user_data["id"] == "user_test"


def test_logout_user():
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "User logged out successfully"

def test_update_user_profile():
    register_resp = client.post("/api/auth/register", json={
        "name": "updateuser",
        "email": "update@example.com",
        "password": "password123"
    })
    assert register_resp.status_code == 201
    token = register_resp.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}
    update_resp = client.put("/me/profile", headers=headers, json={  # <-- 修正這裡
        "username": "updateduser"
    })

    assert update_resp.status_code == 200
    updated_profile = update_resp.json()
    assert updated_profile["username"] == "updateduser"
    assert updated_profile["email"] == "update@example.com"