from sqlalchemy.orm import Session
from app.models.gasto import Gasto, EstadoGasto
from app.crud.base import CRUDBase
from typing import Optional, List


class CRUDGasto(CRUDBase):
    def get_by_folio(self, db: Session, folio: str) -> Optional[Gasto]:
        """Obtener gasto por folio"""
        return db.query(Gasto).filter(Gasto.folio == folio).first()

    def get_by_estado(self, db: Session, estado: EstadoGasto, skip: int = 0, limit: int = 100) -> List[Gasto]:
        """Obtener gastos por estado"""
        return db.query(Gasto).filter(Gasto.estado == estado).offset(skip).limit(limit).all()

    def get_by_usuario(self, db: Session, usuario: str, skip: int = 0, limit: int = 100) -> List[Gasto]:
        """Obtener gastos por usuario"""
        return db.query(Gasto).filter(Gasto.usuario == usuario).offset(skip).limit(limit).all()

    def get_by_departamento(self, db: Session, departamento: str, skip: int = 0, limit: int = 100) -> List[Gasto]:
        """Obtener gastos por departamento"""
        return db.query(Gasto).filter(Gasto.departamento == departamento).offset(skip).limit(limit).all()

    def get_by_categoria(self, db: Session, categoria: str, skip: int = 0, limit: int = 100) -> List[Gasto]:
        """Obtener gastos por categoría"""
        return db.query(Gasto).filter(Gasto.categoria == categoria).offset(skip).limit(limit).all()

    def get_by_proveedor(self, db: Session, proveedor: str, skip: int = 0, limit: int = 100) -> List[Gasto]:
        """Obtener gastos por proveedor"""
        return db.query(Gasto).filter(Gasto.proveedor == proveedor).offset(skip).limit(limit).all()

    def get_by_sucursal(self, db: Session, sucursal: str, skip: int = 0, limit: int = 100) -> List[Gasto]:
        """Obtener gastos por sucursal"""
        return db.query(Gasto).filter(
            (Gasto.sucursal_origen == sucursal) | (Gasto.sucursal_destino == sucursal)
        ).offset(skip).limit(limit).all()

    def get_monto_total(self, db: Session) -> float:
        """Obtener monto total de gastos"""
        result = db.query(Gasto).with_entities(db.func.sum(Gasto.total)).scalar()
        return result or 0.0

    def get_monto_total_por_estado(self, db: Session, estado: EstadoGasto) -> float:
        """Obtener monto total de gastos por estado"""
        result = db.query(Gasto).filter(Gasto.estado == estado).with_entities(db.func.sum(Gasto.total)).scalar()
        return result or 0.0


gasto = CRUDGasto(Gasto)
