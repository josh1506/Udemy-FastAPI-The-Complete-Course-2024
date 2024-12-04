from fastapi import status
from .utils import *
from routers.user import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@gmail.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "Users"
    assert response.json()["is_active"] == True
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "09123456789"


def test_change_password_success(test_user):
    json_data = {"password": "testpassword", "new_password": "newpassword"}
    response = client.put("/user/update/password", json=json_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_invalid_current_password(test_user):
    json_data = {"password": "wrongpasswordd", "new_password": "newpassword"}
    response = client.put("/user/update/password", json=json_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Authentication failed."}


def test_change_phone_number(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
