# app/services/arqueo_caja_service.py
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.arqueo_caja import ArqueoCaja
from app.schemas.arqueo_caja import ArqueoCajaCreate, ArqueoCajaUpdate

class ArqueoCajaService:
    def __init__(self, db: Session):
        self.db = db
    
    def crear_arqueo(self, payload: ArqueoCajaCreate) -> ArqueoCaja:
        """Crea un nuevo arqueo de caja"""
        arqueo = ArqueoCaja(**payload.dict())
        self._calcular_diferencias(arqueo)
        self.db.add(arqueo)
        self.db.commit()
        self.db.refresh(arqueo)
        return arqueo
    
    def _calcular_diferencias(self, arqueo: ArqueoCaja):
        """Calcula las diferencias entre declarado y contado"""
        arqueo.diferencia_efectivo = arqueo.efectivo_contado - arqueo.efectivo_declarado
        arqueo.diferencia_retiros = arqueo.retiros_contado - arqueo.retiros_declarado
        arqueo.diferencia_cheque = arqueo.cheque_contado - arqueo.cheque_declarado
        arqueo.diferencia_tarjeta = arqueo.tarjeta_contado - arqueo.tarjeta_declarado
        arqueo.diferencia_debito = arqueo.debito_contado - arqueo.debito_declarado
        arqueo.diferencia_deposito = arqueo.deposito_contado - arqueo.deposito_declarado
        arqueo.diferencia_credito = arqueo.credito_contado - arqueo.credito_declarado
        arqueo.diferencia_vale = arqueo.vale_contado - arqueo.vale_declarado
        arqueo.diferencia_lealtad = arqueo.lealtad_contado - arqueo.lealtad_declarado
        
        # Calcular totales
        arqueo.total_declarado = (
            arqueo.efectivo_declarado + arqueo.retiros_declarado +
            arqueo.cheque_declarado + arqueo.tarjeta_declarado + 
            arqueo.debito_declarado + arqueo.deposito_declarado + 
            arqueo.credito_declarado + arqueo.vale_declarado + 
            arqueo.lealtad_declarado
        )
        
        arqueo.total_contado = (
            arqueo.efectivo_contado + arqueo.retiros_contado +
            arqueo.cheque_contado + arqueo.tarjeta_contado + 
            arqueo.debito_contado + arqueo.deposito_contado + 
            arqueo.credito_contado + arqueo.vale_contado + 
            arqueo.lealtad_contado
        )
        
        arqueo.diferencia_total = arqueo.total_contado - arqueo.total_declarado
    
    def obtener_arqueo(self, arqueo_id: int) -> ArqueoCaja:
        """Obtiene un arqueo por ID"""
        return self.db.query(ArqueoCaja).filter(ArqueoCaja.id == arqueo_id).first()
    
    def listar_arqueos(self, caja: str = None, local_id: int = None) -> list[ArqueoCaja]:
        """Lista arqueos con filtros opcionales"""
        query = self.db.query(ArqueoCaja)
        if caja:
            query = query.filter(ArqueoCaja.caja == caja)
        if local_id:
            query = query.filter(ArqueoCaja.local_id == local_id)
        return query.order_by(ArqueoCaja.fecha_arqueo.desc()).all()
    
    def actualizar_arqueo(self, arqueo_id: int, payload: ArqueoCajaUpdate) -> ArqueoCaja:
        """Actualiza un arqueo existente"""
        arqueo = self.obtener_arqueo(arqueo_id)
        if not arqueo:
            raise ValueError("Arqueo no encontrado")
        
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(arqueo, field, value)
        
        self._calcular_diferencias(arqueo)
        self.db.commit()
        self.db.refresh(arqueo)
        return arqueo
    
    def eliminar_arqueo(self, arqueo_id: int) -> bool:
        """Elimina un arqueo"""
        arqueo = self.obtener_arqueo(arqueo_id)
        if not arqueo:
            raise ValueError("Arqueo no encontrado")
        self.db.delete(arqueo)
        self.db.commit()
        return True
