import pytest
import requests

# 假设测试服务器的基础URL
BASE_URL = "http://0.0.0.0:8101"

username = "testuser894"


@pytest.fixture(scope="module")
def test_user():
    # 创建测试用户
    user_data = {
        "username": username,
        "password": "testpassword",
        "email": "test@example.com",
        "phone": "12345678901",
        "role_name": "testrole",
        "app_name": "testapp"
    }
    response = requests.post(f"{BASE_URL}/api/account/register/", json=user_data)
    return response.json()


@pytest.fixture(scope="module")
def auth_token(test_user):
    # 登录并获取认证token
    login_data = {
        "username": username,
        "password": "testpassword"
    }
    response = requests.post(f"{BASE_URL}/api/account/login/", json=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]


def test_分配或创建角色(test_user, auth_token):
    data = {
        "user_id": 1,
        "role_name": "newrole",
        "app_name": "testapp"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/api/roles/assign-role/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "角色分配成功"}


def test_验证角色_from_header(auth_token):
    data = {
        "role_name": "testrole",
        "app_name": "testapp"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/api/roles/role-auth/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": True}


def test_无效token():
    data = {
        "role_name": "testrole",
        "app_name": "testapp"
    }
    invalid_token = "invalid_token"

    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = requests.post(f"{BASE_URL}/api/roles/role-auth/", headers=headers, json=data)
    print(response.json())
    print(response.status_code)
    assert response.status_code == 500


def test_无效角色(auth_token):
    data = {
        "role_name": "nonexistent_role",
        "app_name": "testapp"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/api/roles/role-auth/", json=data, headers=headers)
    assert response.status_code == 403
