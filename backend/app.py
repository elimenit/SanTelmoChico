"""Aplicación Principal adaptada para ejecución Serverless en Netlify."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from sqlmodel import Session, select

from middleware.audit import AuditMiddleware
from dependencies.database import init_db
from dependencies.dbsession import engine
from schemas.user import User
from routers.auth import get_password_hash 
from routers.routes import api_router

load_dotenv()

admin_email = os.getenv("FIRST_SUPERUSER_EMAIL")
admin_pass = os.getenv("FIRST_SUPERUSER_PASSWORD")

if not admin_email or not admin_pass:
    raise ValueError("❌ Las variables FIRST_SUPERUSER_EMAIL y FIRST_SUPERUSER_PASSWORD no están configuradas.")

_is_initialized = False

def bootstrap_serverless():
    """Inicializa la BD y crea el usuario admin durante el 'Cold Start'."""
    global _is_initialized
    if not _is_initialized:
        try:
            init_db()
            with Session(engine) as session:
                admin_exists = session.exec(
                    select(User).where(User.role == "admin")
                ).first()
                
                if not admin_exists:
                    first_admin = User(
                        email=admin_email,
                        username="admin",
                        role="admin",
                        is_active=True,
                        password=get_password_hash(admin_pass)
                    )
                    session.add(first_admin)
                    session.commit()
            _is_initialized = True
        except Exception as e:
            print(f"⚠️ Error durante el bootstrap serverless: {e}")

app = FastAPI(
    title="Santelmo Chico - Backend Zero Trust (Serverless)",
    version="1.0.0"
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuditMiddleware)

@app.middleware("http")
async def ensure_bootstrap(request, call_next):
    bootstrap_serverless()
    return await call_next(request)

app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "zero-trust-serverless"}

handler = Mangum(app, lifespan="off")