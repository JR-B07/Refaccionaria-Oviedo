# app/api/v1/endpoints/auth.py - VERSIÓN COMPLETA Y FUNCIONAL
from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import bcrypt

from app.core.database import get_db
from app.crud.usuario import usuario_crud
from app.core.security import create_access_token, verify_token

router = APIRouter()

# Modelos Pydantic
class LoginRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    id: int
    username: str
    name: str
    role: str
    local_id: Optional[int] = None
    local_nombre: Optional[str] = None

class LoginResponse(BaseModel):
    success: bool
    message: str
    access_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[UserInfo] = None

# Nota: la verificación/creación de tokens y hashing de contraseñas
# se realiza a través de `app.core.security` (create_access_token, verify_token).
# Por ahora usamos SHA256 simple (temporal para desarrollo).


# Endpoints
@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login usando la base de datos de usuarios."""
    db_user = usuario_crud.obtener_por_nombre_usuario(db, login_data.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

    # Comparar con bcrypt
    try:
        if not bcrypt.checkpw(login_data.password.encode(), db_user.clave_hash.encode()):
            # Registrar intento fallido
            try:
                usuario_crud.registrar_login(db, db_user, exitoso=False)
            except Exception:
                pass
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")
    except Exception as e:
        print(f"Error verificando contraseña: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

    # Login exitoso
    try:
        usuario_crud.registrar_login(db, db_user, exitoso=True)
    except Exception:
        pass

    # Obtener nombre de la sucursal
    local_nombre = None
    if db_user.local_id and hasattr(db_user, 'local') and db_user.local:
        local_nombre = db_user.local.nombre

    token_data = {
        "sub": db_user.nombre_usuario,
        "id": db_user.id,
        "role": getattr(db_user.rol, 'value', str(db_user.rol)) if db_user.rol else "vendedor",
        "local_id": db_user.local_id,
        "local_nombre": local_nombre
    }

    access_token = create_access_token(token_data)

    # Construir nombre completo
    nombre_completo = db_user.nombre or ""
    if db_user.apellido_paterno:
        nombre_completo += f" {db_user.apellido_paterno}"
    if db_user.apellido_materno:
        nombre_completo += f" {db_user.apellido_materno}"

    user_info = {
        "id": db_user.id,
        "username": db_user.nombre_usuario,
        "name": nombre_completo.strip(),
        "role": getattr(db_user.rol, 'value', str(db_user.rol)) if db_user.rol else "vendedor",
        "local_id": db_user.local_id,
        "local_nombre": local_nombre
    }

    return {
        "success": True,
        "message": "Acceso concedido",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info
    }

@router.get("/logout")
async def logout():
    """Cerrar sesión"""
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/me")
def _get_token_from_header(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Extrae el token del header `Authorization: Bearer <token>` o devuelve None."""
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return authorization


async def get_current_user(token: str = Depends(_get_token_from_header), db: Session = Depends(get_db)):
    """Obtener información del usuario actual"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    username = payload.get("sub")
    db_user = usuario_crud.obtener_por_nombre_usuario(db, username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return db_user

@router.get("/test-token")
async def test_token(token: str = Depends(_get_token_from_header)):
    """Endpoint para probar tokens"""
    if not token:
        return {"valid": False, "reason": "no token provided"}
    payload = verify_token(token)
    if payload:
        return {"valid": True, "payload": payload}
    return {"valid": False, "reason": "invalid token"}