from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "ontology_lookup_service_data_pipeline"
VERSION = "1.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

PGADMIN_DEFAULT_EMAIL = config("PGADMIN_DEFAULT_EMAIL", cast=str)
PGADMIN_DEFAULT_PASSWORD = config("PGADMIN_DEFAULT_PASSWORD", cast=str, default="admin")
SERVER_PORT = config("SERVER_PORT", cast=str, default="5050")

DEFAULT_ONTOLOGY = config("DEFAULT_ONTOLOGY", cast=str)

OLS_API_URL = config("OLS_API_URL", cast=str)
OLS_API_MAX_ITEMS_PER_REQUEST = config("OLS_API_MAX_ITEMS_PER_REQUEST", cast=int)

MESH_DB_URL = config("MESH_DB_URL", cast=str)
