from fastapi.testclient import TestClient


def _assert_jwt(value: str) -> None:
    assert value.count(".") == 2
    assert value != ""

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
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert "id" in data
    _assert_jwt(data["access_token"])
    _assert_jwt(data["refresh_token"])

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
    assert response.json()["detail"] == "Email already exists"

def test_user_login_success(client: TestClient) -> None:
    # Register user
    payload = {
        "email": "login_api@example.com",
        "password": "securepassword123"
    }
    client.post("/v1/users/register", json=payload)
    
    # Login to get token
    login_data = {
        "email": "login_api@example.com",
        "password": "securepassword123"
    }
    response = client.post("/v1/auth/token", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    _assert_jwt(data["access_token"])
    _assert_jwt(data["refresh_token"])

def test_user_login_failure(client: TestClient) -> None:
    login_data = {
        "email": "non_existent@example.com",
        "password": "password"
    }
    response = client.post("/v1/auth/token", data=login_data)
    assert response.status_code == 401

def test_user_refresh_success(client: TestClient) -> None:
    payload = {
        "email": "refresh_api@example.com",
        "password": "securepassword123"
    }
    reg_resp = client.post("/v1/users/register", json=payload)
    refresh_token = reg_resp.json()["refresh_token"]

    response = client.post("/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    _assert_jwt(data["access_token"])
    _assert_jwt(data["refresh_token"])

    second_response = client.post("/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert second_response.status_code == 401

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
    assert "created_at" in data
    assert "updated_at" in data

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

def test_password_validation_does_not_echo_input(client: TestClient) -> None:
    response = client.post(
        "/v1/users/register",
        json={
            "email": "leak_check@example.com",
            "password": 11111111,
        },
    )
    assert response.status_code == 422
    assert "11111111" not in response.text
    assert '"input"' not in response.text

def test_password_validation_does_not_echo_short_password(client: TestClient) -> None:
    response = client.post(
        "/v1/users/register",
        json={
            "email": "leak_check_short@example.com",
            "password": "11111",
        },
    )
    assert response.status_code == 422
    assert "11111" not in response.text
    assert '"input"' not in response.text
