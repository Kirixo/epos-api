from fastapi.testclient import TestClient

def test_user_registration_success(client: TestClient) -> None:
    # 1. Register a new user
    payload = {
        "email": "api_test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/v1/users/register", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "id" in data

def test_user_registration_duplicate(client: TestClient) -> None:
    payload = {
        "email": "dup_api@example.com",
        "password": "securepassword123"
    }
    # First registration
    response = client.post("/v1/users/register", json=payload)
    assert response.status_code == 201
    
    # Second registration (duplicate)
    response = client.post("/v1/users/register", json=payload)
    assert response.status_code == 400
    assert "email_exists" in str(response.json())

def test_user_login_success(client: TestClient) -> None:
    # Register user
    payload = {
        "email": "login_api@example.com",
        "password": "securepassword123"
    }
    client.post("/v1/users/register", json=payload)
    
    # Login to get token
    login_data = {
        "username": "login_api@example.com",
        "password": "securepassword123"
    }
    response = client.post("/v1/auth/token", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_login_failure(client: TestClient) -> None:
    login_data = {
        "username": "non_existent@example.com",
        "password": "password"
    }
    response = client.post("/v1/auth/token", data=login_data)
    assert response.status_code == 401

def test_get_current_user_profile(client: TestClient) -> None:
    payload = {
        "email": "profile_api@example.com",
        "password": "securepassword123"
    }
    reg_resp = client.post("/v1/users/register", json=payload)
    token = reg_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/v1/users/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == "profile_api@example.com"
    assert "id" in data

def test_update_current_user_profile(client: TestClient) -> None:
    payload = {
        "email": "update_api@example.com",
        "password": "securepassword123"
    }
    reg_resp = client.post("/v1/users/register", json=payload)
    token = reg_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    update_payload = {
        "email": "updated_api@example.com",
        "password": "newsecurepassword123",
        "old_password": "securepassword123"
    }
    response = client.patch("/v1/users/me", json=update_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "updated_api@example.com"

def test_delete_current_user_profile(client: TestClient) -> None:
    payload = {
        "email": "delete_api@example.com",
        "password": "securepassword123"
    }
    reg_resp = client.post("/v1/users/register", json=payload)
    token = reg_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/v1/users/me", headers=headers)
    assert response.status_code == 204
    
    # Try fetching profile after deletion
    response = client.get("/v1/users/me", headers=headers)
    assert response.status_code == 401
