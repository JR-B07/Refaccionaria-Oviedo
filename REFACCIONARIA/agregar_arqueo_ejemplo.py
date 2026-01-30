"""
Script para agregar un arqueo de caja de ejemplo
Ejecutar con: python agregar_arqueo_ejemplo.py
"""

import sys
import os
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.arqueo_caja import ArqueoCaja
from app.models.usuario import Usuario
from app.models.local import Local

def agregar_arqueo_ejemplo():
    db = SessionLocal()
    try:
        # Verificar que existan usuarios y locales
        usuario = db.query(Usuario).first()
        local = db.query(Local).first()
        
        if not usuario:
            print("❌ No hay usuarios en la base de datos. Crea uno primero.")
            return
        
        if not local:
            print("❌ No hay locales en la base de datos. Crea uno primero.")
            return
        
        # Crear arqueo de ejemplo con datos similares a la imagen
        arqueo = ArqueoCaja(
            caja="CAJA 1",
            local_id=local.id,
            usuario_id=usuario.id,
            turno="Mañana",
            fecha_arqueo=datetime.now(),
            
            # Montos declarados (Requerido)
            efectivo_declarado=1077.26,
            retiros_declarado=45681,
            cheque_declarado=0,
            tarjeta_declarado=0,
            debito_declarado=3462.58,
            deposito_declarado=0,
            credito_declarado=0,
            vale_declarado=100,
            lealtad_declarado=0,
            
            # Montos contados (Disponible)
            efectivo_contado=1077.26,
            retiros_contado=0,
            cheque_contado=0,
            tarjeta_contado=0,
            debito_contado=0,
            deposito_contado=0,
            credito_contado=0,
            vale_contado=0,
            lealtad_contado=0,
            
            observaciones="Arqueo de ejemplo - Apertura de caja del día"
        )
        
        # Calcular diferencias
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
        
        db.add(arqueo)
        db.commit()
        db.refresh(arqueo)
        
        print("✅ Arqueo de ejemplo creado exitosamente!")
        print(f"   ID: {arqueo.id}")
        print(f"   Caja: {arqueo.caja}")
        print(f"   Fecha: {arqueo.fecha_arqueo}")
        print(f"   Total Declarado: ${arqueo.total_declarado:,.2f}")
        print(f"   Total Contado: ${arqueo.total_contado:,.2f}")
        print(f"   Diferencia Total: ${arqueo.diferencia_total:,.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    agregar_arqueo_ejemplo()
