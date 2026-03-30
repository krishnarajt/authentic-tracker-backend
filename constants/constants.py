import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/mydb",
)
# Ensure the asyncpg dialect is used even if the URL omits it
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
DB_SCHEMA = os.getenv("DB_SCHEMA", "public")

GOLDAPI_API_KEY = os.getenv("GOLDAPI_API_KEY")
GOLDAPI_API_KEY_2 = os.getenv("GOLDAPI_API_KEY_2")
GOLDAPI_API_KEY_3 = os.getenv("GOLDAPI_API_KEY_3")
GOLDAPI_API_KEY_4 = os.getenv("GOLDAPI_API_KEY_4")
