import pytest
import requests
from app_tools_zxw.Errors.api_errors import ErrorCode

BASE_URL = "http://0.0.0.0:8101"  # 替换为实际的测试服务器URL

phone = "13800138099"
username = "testuser188"


def test_注册_手机():
    # 测试正常注册
    response = requests.post(f"{BASE_URL}/api/account/register-phone/", json={
        "phone": phone,
        "sms_code": "123456",
        "role_name": "user_app",
        "app_name": "test_app"
    })

    print(response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 测试重复注册
    response = requests.post(f"{BASE_URL}/api/account/register-phone/", json={
        "phone": phone,
        "sms_code": "123456",
        "role_name": "user_app",
        "app_name": "test_app"
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == ErrorCode.手机号已注册


def test_登录_手机():
    # 测试正确登录
    response = requests.post(f"{BASE_URL}/api/account/login-phone/", json={
        "phone": phone,
        "sms_code": "123456"
    })
    print(response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 测试错误登录
    response = requests.post(f"{BASE_URL}/api/account/login-phone/", json={
        "phone": phone,
        "sms_code": "wrong_code"
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == ErrorCode.无效的手机号或验证码


def test_注册():
    # 测试正常注册
    response = requests.post(f"{BASE_URL}/api/account/register/", json={
        "username": username,
        "password": "testpassword",
        "role_name": "user_app",
        "app_name": "test_app"
    })
    print(response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 测试重复注册
    response = requests.post(f"{BASE_URL}/api/account/register/", json={
        "username": username,
        "password": "testpassword",
        "role_name": "user",
        "app_name": "test_app"
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == ErrorCode.用户名已注册


def test_登录():
    # 测试正确登录
    response = requests.post(f"{BASE_URL}/api/account/login/", json={
        "username": username,
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 测试错误登录
    response = requests.post(f"{BASE_URL}/api/account/login/", json={
        "username": username,
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == ErrorCode.无效的用户名或密码


def test_获取_登录二维码URL():
    response = requests.post(f"{BASE_URL}/wechat/qr-login/get-qrcode", json={
        "WECHAT_REDIRECT_URI": "http://example.com/callback"
    })
    assert response.status_code == 200
    assert "qr_code_url" in response.json()


# 注意：微信一键登录的测试可能需要模拟微信API的响应，这里只是一个简单的示例
def test_一键登录():
    # 这里假设我们有一个有效的微信code
    response = requests.post(f"{BASE_URL}/wechat/qr-login/login/", params={
        "code": "valid_wechat_code",
        "app_name": "test_app"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    # 测试无效的code
    response = requests.post(f"{BASE_URL}/wechat/qr-login/login/", params={
        "code": "invalid_wechat_code",
        "app_name": "test_app"
    })
    assert response.status_code == 400
    assert response.json()["detail"]["error_code"] == ErrorCode.微信登录失败
