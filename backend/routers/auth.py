from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from jose import jwt
from sqlmodel import select

from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
o
from dependencies.database import DBUsersDep
from dependencies.dbsession import SessionDep
from schemas.user import UserCreate, UserPublic, Token, User, UserLogin
from utils.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, validate_constants

# Redis for sends mails
from fastapi import Depends, BackgroundTasks
from arq.connections import ArqRedis
from dependencies.queue_mails import get_redis_pool

# Redis para cachear los datos en RAM
from dependencies.redis_session import RedisClientDep

for value, name in [(SECRET_KEY, 'SECRET_KEY'), (ALGORITHM, 'ALGORITHM'), (ACCESS_TOKEN_EXPIRE_MINUTES, 'ACCESS_TOKEN_EXPIRE_MINUTES')]:
    validate_constants(value, name)
    
# Configuración del Hasher (Bcrypt)
password_hash = PasswordHash((BcryptHasher(),))

# Añadimos prefijo y tags para organizar la documentación autogenerada de FastAPI
router = APIRouter()


# --- FUNCIONES AUXILIARES ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    # Usamos timezone.utc para evitar problemas con servidores en diferentes zonas horarias
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)
        
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- ENDPOINTS ---

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def signup(
    redis_client: RedisClientDep,
    user: UserCreate, 
    session: SessionDep, 
    db: DBUsersDep,
    redis_pool: ArqRedis = Depends(get_redis_pool)
):
    """
    Registra un nuevo usuario y encola un mail de bienvenida.
    """
    user.password = get_password_hash(user.password)
    
    new_user = db.add(redis_client, user, session)
    
    await redis_pool.enqueue_job('send_welcome_email', new_user.email)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(redis_client: RedisClientDep, credentials: UserLogin, session: SessionDep):
    """
    Login Zero-Trust: Mitigación de Timing Attacks y validación de usuarios inactivos.
    """
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    
    error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas", 
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # MITIGACIÓN TIMING ATTACK:
    if not user:
        get_password_hash(credentials.password)
        raise error_exception
        
    if not user.is_active:
        get_password_hash(credentials.password)
        raise error_exception
    
    if not verify_password(credentials.password, user.password):
        raise error_exception
    
    # Generamos el JWT usando el ID del usuario (inmutable), NUNCA el email
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id), 
            "role": user.role
        }, 
        expires_delta=access_token_expires
    )
    
    return {"token": access_token, "token_type": "bearer"}