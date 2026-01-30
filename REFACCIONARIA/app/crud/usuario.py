# app/crud/usuario.py
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash

class CRUDUsuario:
    def obtener_por_id(self, db: Session, id: int) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.id == id).first()
    
    def obtener_por_nombre_usuario(self, db: Session, nombre_usuario: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    
    def obtener_por_email(self, db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    def obtener_activos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return db.query(Usuario).filter(Usuario.estado == "activo").offset(skip).limit(limit).all()
    
    def obtener_por_local(self, db: Session, local_id: int) -> List[Usuario]:
        return db.query(Usuario).filter(Usuario.local_id == local_id).all()
    
    def crear(self, db: Session, usuario: UsuarioCreate) -> Usuario:
        # Verificar que no exista el nombre de usuario o email
        if self.obtener_por_nombre_usuario(db, usuario.nombre_usuario):
            raise ValueError("El nombre de usuario ya existe")
        
        if self.obtener_por_email(db, usuario.email):
            raise ValueError("El email ya está registrado")
        
        # Crear usuario
        db_usuario = Usuario(
            nombre=usuario.nombre,
            apellido_paterno=usuario.apellido_paterno,
            apellido_materno=usuario.apellido_materno,
            email=usuario.email,
            telefono=usuario.telefono,
            nombre_usuario=usuario.nombre_usuario,
            clave_hash=get_password_hash(usuario.clave_acceso),
            rol=usuario.rol,
            local_id=usuario.local_id
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def actualizar(self, db: Session, id: int, usuario_update: UsuarioUpdate) -> Optional[Usuario]:
        db_usuario = self.obtener_por_id(db, id)
        if not db_usuario:
            return None
        
        update_data = usuario_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_usuario, field, value)
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def cambiar_clave(self, db: Session, id: int, nueva_clave: str) -> Optional[Usuario]:
        db_usuario = self.obtener_por_id(db, id)
        if not db_usuario:
            return None
        
        db_usuario.clave_hash = get_password_hash(nueva_clave)
        db_usuario.debe_cambiar_clave = False
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def eliminar(self, db: Session, id: int) -> bool:
        db_usuario = self.obtener_por_id(db, id)
        if not db_usuario:
            return False
        
        db.delete(db_usuario)
        db.commit()
        return True
    
    def desactivar(self, db: Session, id: int) -> Optional[Usuario]:
        db_usuario = self.obtener_por_id(db, id)
        if not db_usuario:
            return None
        
        db_usuario.estado = "inactivo"
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    def registrar_login(self, db: Session, usuario: Usuario, exitoso: bool = True) -> Usuario:
        from datetime import datetime
        
        if exitoso:
            usuario.ultimo_login = datetime.utcnow()
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = None
        else:
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos >= 5:
                from datetime import timedelta
                usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=15)
        
        db.commit()
        db.refresh(usuario)
        return usuario

usuario_crud = CRUDUsuario()