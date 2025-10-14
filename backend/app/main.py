from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import traceback
from core.database import engine, Base
from models.user_model import User
from routes.user_routes import router
from fastapi import APIRouter


print("Starting application...")
time.sleep(25)

try:


    Base.metadata.create_all(bind=engine)
    print("Database tables created")

    app = FastAPI(title="Proyecto Productiva MVC")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "http://127.0.0.1:4200",
            "http://frontend:4200"  
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    @app.options("/api/users/{path:path}")
    async def options_handler():
        return {"message": "OK"}

    @app.options("/api/users/login")
    async def login_options():
        return {"message": "OK"}

    @app.options("/api/users/register")
    async def register_options():
        return {"message": "OK"}

    app.include_router(router, prefix="/api", tags=["Usuarios"])

    @app.get("/")
    def root():
        return {"message": "API funcionando con estructura MVC 🚀"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    print("Application ready with improved CORS")

except Exception as error:
    print(f"Error during startup: {error}")
    traceback.print_exc()
    
    app = FastAPI(title="Proyecto Productiva MVC - Basic Mode")
    
    # Configuración CORS 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    basic_router = APIRouter(prefix="/users", tags=["Usuarios"])

    @basic_router.post("/register")
    def register_basic():
        return {"message": "Servicio de registro temporalmente no disponible", "status": "error"}

    @basic_router.post("/login")
    def login_basic():
        return {"message": "Servicio de login temporalmente no disponible", "status": "error"}

    app.include_router(basic_router)
    
    print("Running in basic mode - endpoints available but database offline") 