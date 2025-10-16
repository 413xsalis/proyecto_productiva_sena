from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import traceback
import os
from models.user_model import User
from core.database import engine, Base
from routes.user_routes import router as user_router
from routes.excel_routes import router as excel_router
from core.config import ALLOWED_ORIGINS, DEBUG, UPLOAD_DIR

print("🚀 Iniciando aplicación FastAPI...")
print(f"📊 Entorno: {os.getenv('ENVIRONMENT', 'development')}")

time.sleep(10)

try:
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas de la base de datos creadas")

    # Crear directorio de uploads
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    print(f"✅ Directorio de uploads: {UPLOAD_DIR}")

    # Crear aplicación
    app = FastAPI(
        title="Proyecto SENA Productiva",
        description="Sistema de gestión con FastAPI + Angular + MySQL",
        version="1.0.0",
        debug=DEBUG
    )

    # Configurar CORS MEJORADO
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    # Manejar preflight OPTIONS requests
    @app.middleware("http")
    async def add_cors_headers(request, call_next):
        response = await call_next(request)
        if request.method == "OPTIONS":
            response.headers["Access-Control-Allow-Origin"] = ", ".join(ALLOWED_ORIGINS)
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    # Incluir routers
    app.include_router(user_router, prefix="/api", tags=["Usuarios"])
    app.include_router(excel_router, prefix="/api", tags=["Archivos Excel"])

    # Rutas básicas
    @app.get("/")
    def root():
        return {"message": "API Proyecto SENA Productiva 🚀", "version": "1.0.0"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "database": "connected"}

    print("✅ Aplicación FastAPI configurada correctamente")
    print(f"🌐 CORS habilitado para: {ALLOWED_ORIGINS}")

except Exception as error:
    print(f"❌ Error durante el inicio: {error}")
    traceback.print_exc()
    
    app = FastAPI(title="Proyecto SENA - Modo Emergencia")
    
    @app.get("/")
    def root_emergency():
        return {"message": "⚠️ Modo emergencia - Revisar configuración"}