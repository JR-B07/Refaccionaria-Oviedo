# app/api/v1/endpoints/auth.py - VERSIÓN COMPLETA Y FUNCIONAL
from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import traceback
from pathlib import Path
from sqlalchemy.orm import Session
import hashlib

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
@router.post("/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login usando la base de datos de usuarios."""
    try:
        db_user = usuario_crud.obtener_por_nombre_usuario(db, login_data.username)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

        # Comparar hash SHA256
        password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
        if password_hash != db_user.clave_hash:
            # Registrar intento fallido si existe la función en el CRUD
            try:
                usuario_crud.registrar_login(db, db_user, exitoso=False)
            except Exception:
                pass
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos")

        # Login exitoso
        try:
            usuario_crud.registrar_login(db, db_user, exitoso=True)
        except Exception:
            pass

        # Obtener nombre de la sucursal
        local_nombre = None
        if db_user.local_id and db_user.local:
            local_nombre = db_user.local.nombre

        token_data = {
            "sub": db_user.nombre_usuario,
            "id": db_user.id,
            "role": getattr(db_user.rol, 'value', str(db_user.rol)),
            "local_id": db_user.local_id,
            "local_nombre": local_nombre
        }

        access_token = create_access_token(token_data)

        user_info = {
            "id": db_user.id,
            "username": db_user.nombre_usuario,
            "name": db_user.nombre_completo,
            "role": getattr(db_user.rol, 'value', str(db_user.rol)),
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
    except HTTPException:
        raise
    except Exception as e:
        error_text = "\n".join([
            "❌ Error en login:",
            str(e),
            traceback.format_exc()
        ])
        try:
            log_path = Path(__file__).resolve().parents[3] / "login_error.log"
            log_path.write_text(error_text, encoding="utf-8")
        except Exception:
            pass
        print(error_text)
        raise HTTPException(status_code=500, detail=str(e))

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