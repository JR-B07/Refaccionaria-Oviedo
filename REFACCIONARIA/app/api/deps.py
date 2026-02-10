# app/api/deps.py
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.crud.usuario import usuario_crud
from typing import Optional

def extract_token_from_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extrae el token del header Authorization: Bearer <token>
    """
    if not authorization:
        return None
    
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None

async def get_current_user(
    authorization: Optional[str] = Header(None),
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
    
    # Extraer token
    token = extract_token_from_header(authorization)
    if not token:
        raise credentials_exception
    
    # Verificar token
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
        "nombre": usuario.nombre_completo,
        "rol": usuario.rol.value if usuario.rol else "vendedor",
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
