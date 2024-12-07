from datetime import timedelta

from jose import jwt

from routers.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from .utils import *

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existing_user = authenticate_user("wrong_username", "testpassword", db)
    assert non_existing_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongtestpassword", db)
    assert wrong_password_user is False


def test_create_access_token(test_user):
    token_expiration = timedelta(minutes=20)
    token = create_access_token(test_user.username, test_user.id, test_user.role, token_expiration)
    assert token is not None
    assert isinstance(token, str)

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
    assert payload["sub"] == test_user.username
    assert payload["id"] == test_user.id
    assert payload["role"] == test_user.role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)
    assert user is not None
    assert user == {"username": "testuser", "id": 1, "role": "admin"}

