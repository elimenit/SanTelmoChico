from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import select
import os
from dotenv import load_dotenv

from dependencies.dbsession import SessionDep
from schemas.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM', 'HS256')

# Le indicamos a FastAPI dónde está el endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), session: SessionDep = None):
    """
    Zero Trust Core: Desconfiamos de cada petición. Validamos la firma del JWT,
    la caducidad y la existencia del usuario en la base de datos en tiempo real.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # En Zero Trust no basta con que el token sea válido, el usuario aún debe existir y estar activo
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
        
    # Mitigación: Si implementas un Soft Delete, verifica aquí si `user.is_active` es True
    
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    """Validación estricta de Roles (RBAC)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilegios insuficientes"
        )
    return current_users