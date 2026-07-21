"""Autenticacion del usuario.
"""
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from schemas.user import User
from dependencies.dbsession import SessionDep
from sqlmodel import select
from utils.constants import SECRET_KEY, ALGORITHM, validate_constants

for value, name in [(SECRET_KEY, 'SECRET_KEY'), (ALGORITHM, 'ALGORITHM')]:
    validate_constants(value, name)

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: SessionDep = None
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        role = payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    request = getattr(session, "_request", None)
    if hasattr(request, "state"):
        request.state.user_id = user_id
        request.state.user_role = role

    user = session.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User inactive")
    return user

def require_role(required_role: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role != required_role and required_role != "any":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker