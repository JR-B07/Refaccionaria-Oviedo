from sqlalchemy.orm import Session
from app.models.promocion import Promocion
from app.schemas.promocion import PromocionCreate, PromocionUpdate
from typing import List, Optional

def get_promociones(db: Session, skip: int = 0, limit: int = 100) -> List[Promocion]:
    return db.query(Promocion).offset(skip).limit(limit).all()

def get_promocion(db: Session, promocion_id: int) -> Optional[Promocion]:
    return db.query(Promocion).filter(Promocion.id == promocion_id).first()

def create_promocion(db: Session, promocion: PromocionCreate) -> Promocion:
    db_promocion = Promocion(descripcion=promocion.descripcion, activa=promocion.activa)
    db.add(db_promocion)
    db.commit()
    db.refresh(db_promocion)
    return db_promocion

def update_promocion(db: Session, promocion_id: int, promocion: PromocionUpdate) -> Optional[Promocion]:
    db_promocion = get_promocion(db, promocion_id)
    if not db_promocion:
        return None
    if promocion.descripcion is not None:
        db_promocion.descripcion = promocion.descripcion
    if promocion.activa is not None:
        db_promocion.activa = promocion.activa
    db.commit()
    db.refresh(db_promocion)
    return db_promocion

def delete_promocion(db: Session, promocion_id: int) -> bool:
    db_promocion = get_promocion(db, promocion_id)
    if not db_promocion:
        return False
    db.delete(db_promocion)
    db.commit()
    return True
