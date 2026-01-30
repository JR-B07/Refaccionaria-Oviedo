# app/api/v1/endpoints/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.crud.usuario import usuario_crud
from app.api.deps import get_current_user, require_admin

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any  # <-- Añadir Any aquí

from app.core.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.crud.usuario import usuario_crud
from app.api.deps import get_current_user, require_admin
router = APIRouter()

@router.post("/", response_model=UsuarioResponse)
async def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
) -> Any:
    """
    Crear nuevo usuario (Solo administradores)
    """
    try:
        nuevo_usuario = usuario_crud.crear(db, usuario)
        return nuevo_usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """
    Listar usuarios (con paginación)
    """
    usuarios = usuario_crud.obtener_activos(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Obtener usuario por ID
    """
    usuario = usuario_crud.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
) -> Any:
    """
    Actualizar usuario (Solo administradores)
    """
    usuario = usuario_crud.actualizar(db, usuario_id, usuario_update)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.delete("/{usuario_id}")
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
) -> dict:
    """
    Eliminar usuario (Solo administradores - desactiva en lugar de eliminar)
    """
    usuario = usuario_crud.desactivar(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {"message": "Usuario desactivado exitosamente"}

@router.post("/{usuario_id}/reiniciar-clave")
async def reiniciar_clave_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
) -> dict:
    """
    Reiniciar contraseña de usuario (Solo administradores)
    La nueva contraseña temporal será "Refaccionaria123"
    """
    usuario = usuario_crud.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Establecer contraseña temporal
    usuario_crud.cambiar_clave(db, usuario_id, "Refaccionaria123")
    usuario_crud.actualizar(db, usuario_id, UsuarioUpdate(debe_cambiar_clave=True))
    
    return {"message": "Contraseña reiniciada exitosamente. El usuario deberá cambiarla en su próximo login."}