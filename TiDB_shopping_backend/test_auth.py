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
#---------------products.py---------------- #
def test_get_all_products_default():
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # 預設 limit 是 10


def test_get_all_products_with_pagination():
    response = client.get("/api/products/?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_all_products_filter_by_category():
    response = client.get("/api/products/?category=1")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["id"] in [1, 2]  # category_id = 1 的商品


def test_get_all_products_sort_by_price_desc():
    response = client.get("/api/products/?sort_by=price_desc")
    assert response.status_code == 200
    data = response.json()
    prices = [item["price"] for item in data]
    assert prices == sorted(prices, reverse=True)


def test_get_product_detail_success():
    response = client.get("/api/products/2")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert "name" in data
    assert "price" in data


def test_get_product_detail_not_found():
    response = client.get("/api/products/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"


def test_get_bestsellers_limit():
    response = client.get("/api/products/bestsellers?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["sold"] >= data[1]["sold"]

#----------test orders -----------------#
def get_auth_token():
    # 註冊並登入使用者以獲得 token
    email = "orderuser@example.com"
    password = "password123"
    client.post("/api/auth/register", json={
        "name": "OrderUser",
        "email": email,
        "password": password
    })
    login_resp = client.post("/api/auth/login", json={"email": email, "password": password})
    return login_resp.json()["access_token"]

def test_create_order_success():
    token = get_auth_token()

    order_payload = {
        "items": [
            {"product_id": 1, "quantity": 2},  # 庫存 100，2 是足夠的
            {"product_id": 3, "quantity": 1},  # 庫存 30
        ],
        "shipping_address": {
            "address": "台北市信義區",
            "city": "台北市",
            "postal_code": "110",
            "country": "台灣"
        },
        "payment_method": "credit_card"
    }

    response = client.post(
        "/api/orders/",
        json=order_payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "total_amount" in data
    assert len(data["items"]) == 2

def test_create_order_insufficient_stock():
    token = get_auth_token()

    order_payload = {
        "items": [
            {"product_id": 2, "quantity": 1000},  # 庫存只有 50，不足
        ],
        "shipping_address": {
            "address": "台北市信義區",
            "city": "台北市",
            "postal_code": "110",
            "country": "台灣"
        },
        "payment_method": "credit_card"
    }

    response = client.post(
        "/api/orders/",
        json=order_payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Insufficient stock"

def test_get_order_history():
    token = get_auth_token()

    response = client.get(
        "/api/orders/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_order_detail_success():
    token = get_auth_token()
    order_id = 1  # 假設這筆訂單存在且屬於該用戶

    response = client.get(
        f"/api/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data and data["id"] == order_id
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_order_detail_unauthorized():
    token = "testtoken"
    order_id = 9999  # 假設不存在或不屬於該用戶

    response = client.get(
        f"/api/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in (401, 403, 404)
