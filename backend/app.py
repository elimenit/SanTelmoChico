"""Aplicacion Principal.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.audit import AuditMiddleware
from dependencies.database import init_db
from routers.routes import api_router

import os
from dotenv import load_dotenv
from sqlmodel import Session, select

load_dotenv()

from dependencies.dbsession import engine
from schemas.user import User
from routers.auth import get_password_hash 

# Redis + ARQ
from arq import create_pool
from config.redis_config import redis_settings
import dependencies.queue_mails as queue_deps 

admin_email = os.getenv("FIRST_SUPERUSER_EMAIL")
admin_pass = os.getenv("FIRST_SUPERUSER_PASSWORD")

if not admin_email or not admin_pass:
    raise ValueError("❌ Las variables FIRST_SUPERUSER_EMAIL y FIRST_SUPERUSER_PASSWORD no están configuradas.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicación - Zero Trust Mode")
    init_db()   
    
    with Session(engine) as session:
        admin_exists = session.exec(
            select(User).where(User.role == "admin")
        ).first()
        
        if not admin_exists:
            print(f"🛠 Creando administrador inicial: {admin_email}")
            first_admin = User(
                email=admin_email,
                username="admin",
                role="admin",
                is_active=True,
                password=get_password_hash(admin_pass)
            )
            session.add(first_admin)
            session.commit()
            print(f"✅ Administrador inicial creado con éxito: {admin_email}")
        else:
            print(f"👤 Administrador ya existe: {admin_email}")
    
    print("🔌 Conectando a Redis para cola de tareas...")
    queue_deps.redis_pool = await create_pool(redis_settings)
    print("✅ Pool de Redis inicializado.")

    yield 
    print("🛑 Apagando aplicación...")
    if queue_deps.redis_pool:
        await queue_deps.redis_pool.close()
        print("🛑 Pool de Redis cerrado de forma segura.")

app = FastAPI(
    title="Santelmo Chico - Backend Zero Trust",
    lifespan=lifespan,
    version="1.0.0"
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],           # Cambia en producción por tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuditMiddleware)

app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "zero-trust"}