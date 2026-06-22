import pytest


@pytest.mark.parametrize(
    "first_name, middle_name, last_name, email, password, password2, status_code",
    [
        ("Александр", "Сергеевич", "Попов", "test@m.com", "test1234", "test1234", 200),
        (" ", "Сергеевич", "Попов", "test@m.com", "test1234", "test1234", 422),
        ("Александр", "Сергеевич", "Попов", "m.com", "test1234", "test1234", 422),
        ("Александр", "Сергеевич", "Попов", "test@m.com", "test", "test1234", 422),
        ("Александр", "Сергеевич", "Попов", "test@m.com", "test1234", "te4", 422),
        ("Александр", "Сергеевич", "Попов", "test@m.com", "test1234", "test1234", 409),
    ],
)
async def test_register(
    first_name: str,
    middle_name: str,
    last_name: str,
    email: str,
    password: str,
    password2: str,
    status_code: int,
    ac,
):
    response_register = await ac.post(
        "auth/register",
        json={
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert response_register.status_code == status_code
    if response_register.status_code != 200:
        return
    result = response_register.json()
    assert isinstance(result, dict)
    assert result["status"] == "ok"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test12@m.com", "test1234", 404),
        ("test@m.com", "test", 422),
        ("testm.com", "test1234", 422),
        ("test@m.com", "test1234", 200),
    ],
)
async def test_login_and_logout(email: str, password: str, status_code: int, ac):
    response_auth = await ac.post(
        "auth/login", json={"email": email, "password": password}
    )
    assert response_auth.status_code == status_code
    if response_auth.status_code != 200:
        return
    assert ac.cookies["access_token"]

    await ac.post("auth/logout")
    assert "access_token" not in ac.cookies


@pytest.mark.parametrize(
    "user_id, first_name, middle_name, last_name, email, old_password, new_password, new_password2, status_code",
    [
        (
            2,
            "Алекс",
            "Сергеевич",
            "Попов",
            "test_user@example.com",
            None,
            None,
            None,
            200,
        ),
        (2, "Алекс", "Сергеевич", "Попов", "admin@example.com", None, None, None, 409),
        (
            2,
            "Алекс",
            "Сергеевич",
            "Попов",
            "test_user@example.com",
            "stringst",
            "new",
            "new1234",
            422,
        ),
        (
            2,
            "Алекс",
            "Сергеевич",
            "Попов",
            "test_user@example.com",
            "stringst",
            None,
            "new1234",
            422,
        ),
        (
            2,
            "Алекс",
            "Сергеевич",
            "Попов",
            "test_user@example.com",
            "stringst",
            "new1234568",
            "new1234568",
            200,
        ),
        (1, "Алекс", "Сергеевич", "Попов", "test111@m.com", None, None, None, 403),
        (999, "Алекс", "Сергеевич", "Попов", "test111@m.com", None, None, None, 404),
    ],
)
async def test_update(
    user_id: int,
    first_name: str,
    middle_name: str,
    last_name: str,
    email: str,
    old_password: str,
    new_password: str,
    new_password2: str,
    status_code: int,
    user_ac,
):
    response = await user_ac.patch(
        f"auth/user/{user_id}",
        json={
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "email": email,
            "old_password": old_password,
            "new_password": new_password,
            "new_password2": new_password2,
        },
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "ok"


@pytest.mark.parametrize(
    "user_id, first_name, middle_name, last_name, email, old_password, new_password, new_password2, status_code",
    [
        (
            2,
            "Александр",
            "Сергеевич",
            "Попов",
            "test_user@example.com",
            None,
            None,
            None,
            200,
        ),
        (2, "Алекс", "Сергеевич", "Попов", "test@example.com", None, None, None, 200),
        (
            2,
            "Алекс",
            "Сергеевич",
            "Попов",
            "test_user@example.com",
            "new1234568",
            "newPassword",
            "newPassword",
            200,
        ),
    ],
)
async def test_admin(
    user_id: int,
    first_name: str,
    middle_name: str,
    last_name: str,
    email: str,
    old_password: str,
    new_password: str,
    new_password2: str,
    status_code: int,
    admin_ac,
):
    response = await admin_ac.patch(
        f"auth/user/{user_id}",
        json={
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "email": email,
            "old_password": old_password,
            "new_password": new_password,
            "new_password2": new_password2,
        },
    )
    assert response.status_code == status_code
    if response.status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "ok"


@pytest.mark.parametrize(
    "user_id, status_code",
    [
        (999, 404),
        (3, 200),
    ],
)
async def test_delete(user_id: int, status_code: int, admin_ac):
    response = await admin_ac.delete(f"auth/user/{user_id}")
    assert response.status_code == status_code
    if response.status_code != 200:
        return
    result = response.json()
    assert isinstance(result, dict)
    assert result["status"] == "ok"


async def test_login_deleted_user(ac):
    response_auth = await ac.post(
        "auth/login", json={"email": "test@m.com", "password": "test1234"}
    )
    assert response_auth.status_code == 403
