import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/postgres",
)
os.environ.setdefault("SECRET_KEY", "test-secret")
