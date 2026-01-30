# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.crud.usuario import usuario_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """
    Obtiene el usuario actual a partir del token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    nombre_usuario: str = payload.get("sub")
    if nombre_usuario is None:
        raise credentials_exception
    
    usuario = usuario_crud.obtener_por_nombre_usuario(db, nombre_usuario=nombre_usuario)
    if usuario is None:
        raise credentials_exception
    
    if usuario.estado != "activo":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return {
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "rol": usuario.rol.value,
        "local_id": usuario.local_id
    }

async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Requiere que el usuario sea administrador
    """
    if current_user["rol"] != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes"
        )
    return current_user

async def require_gerente(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Requiere que el usuario sea gerente o administrador
    """
    if current_user["rol"] not in ["administrador", "gerente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes"
        )
    return current_user