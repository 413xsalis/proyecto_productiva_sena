import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@db:3306/productiva_db")
SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-por-defecto")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configuración de CORS - AGREGAR 127.0.0.1
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:80",
    "http://127.0.0.1", 
    "http://127.0.0.1:80",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://frontend:80",
    "http://frontend:4200"
]

# Configuración de archivos
UPLOAD_DIR = "uploads/excel"
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.xls', '.xlsx'}