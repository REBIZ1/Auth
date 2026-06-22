import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient, ASGITransport
from sqlalchemy import update, create_engine

from models import UserOrm
from src.core.config import settings
from src.core.database import async_session_maker
from src.core.db_manager import DBManager
from src.main import app

engine = create_engine(settings.DB_URL.replace("+asyncpg", ""))


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    """
    Проверяет, что приложение запущено в тестовом режиме
    """
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session")
async def db() -> DBManager:
    """
    Фикстура для получения DBManager с новой сессией на каждый тест
    """
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def clear_db(check_test_mode):
    """
    Очищает БД
    """
    with engine.begin() as conn:
        conn.exec_driver_sql("DROP SCHEMA public CASCADE")
        conn.exec_driver_sql("CREATE SCHEMA public")


@pytest.fixture(scope="session", autouse=True)
def run_alembic_migrations(check_test_mode, clear_db):
    """
    Заполняет БД тестовыми данными
    """
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")
    yield


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    """
    Создает асинхронный http клиент для тестирования.
    Использует ASGITransport, что позволяет выполнять запросы напрямую
    к приложению без запуска реального http сервера
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_admin_and_user(run_alembic_migrations, ac, db):
    """
    Регистрирует тестового администратора и пользователя
    """
    response = await ac.post(
        "/auth/register",
        json={
            "first_name": "first_name",
            "middle_name": "middle_name",
            "last_name": "last_name",
            "email": "admin@example.com",
            "password": "stringst",
            "password2": "stringst",
        },
    )
    assert response.status_code == 200

    user = await db.users.get_one(email="admin@example.com")
    if user:
        await db.session.execute(
            update(UserOrm).where(UserOrm.id == user.id).values(role_id=3)
        )
        await db.commit()

    response = await ac.post(
        "/auth/register",
        json={
            "first_name": "first_name",
            "middle_name": "middle_name",
            "last_name": "last_name",
            "email": "test_user@example.com",
            "password": "stringst",
            "password2": "stringst",
        },
    )
    assert response.status_code == 200


@pytest.fixture(scope="session")
async def admin_ac(register_admin_and_user, ac):
    """
    Аутентификация тестового администратора
    """
    await ac.post(
        "/auth/login", json={"email": "admin@example.com", "password": "stringst"}
    )
    assert ac.cookies["access_token"]
    yield ac


@pytest.fixture(scope="session")
async def user_ac(register_admin_and_user, ac):
    """
    Аутентификация тестового пользователя
    """
    await ac.post(
        "/auth/login", json={"email": "test_user@example.com", "password": "stringst"}
    )
    assert ac.cookies["access_token"]
    yield ac
