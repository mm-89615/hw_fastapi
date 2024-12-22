import os

POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5430")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "pass")

PG_DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
          f"{POSTGRES_PORT}/{POSTGRES_DB}")

TOKEN_TTL_SEC = os.getenv("TOKEN_TTL_SEC", 2 * 24 * 60 * 60)
DEFAULT_ROLE = os.getenv("DEFAULT_ROLE", "user")

ADMIN_NAME = os.getenv("ADMIN_NAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
