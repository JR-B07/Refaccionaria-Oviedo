#!/usr/bin/env python3
"""Script para agregar paquetes de ejemplo a la base de datos"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

# Agregar el directorio de la app al path
sys.path.insert(0, '/home/user/REFACCIONARIA')

from app.core.config import settings
from app.models.paquete import Paquete, PaqueteProducto
from app.models.base import Base

# Crear conexión a la base de datos
engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)

def agregar_paquetes_ejemplo():
    """Agrega dos paquetes de ejemplo a la base de datos"""
    
    with Session(engine) as session:
        # Verificar si ya existen paquetes
        paquetes_existentes = session.query(Paquete).count()
        if paquetes_existentes > 0:
            print(f"✅ Ya existen {paquetes_existentes} paquetes en la base de datos")
            return
        
        # Crear primer paquete: Kit de Suspensión
        paquete1 = Paquete(
            nombre="Kit Suspensión Delantera",
            clase="Suspensión",
            descripcion="Kit completo de suspensión delantera con amortiguadores, resortes y brazos de control",
            local_id=1
        )
        
        # Crear segundo paquete: Kit de Frenos
        paquete2 = Paquete(
            nombre="Kit Frenos Completo",
            clase="Frenos",
            descripcion="Sistema de frenos completo con pastillas, discos y mangueras de freno",
            local_id=1
        )
        
        session.add(paquete1)
        session.add(paquete2)
        session.commit()
        
        print("✅ Paquetes de ejemplo agregados exitosamente:")
        print(f"   - Kit Suspensión Delantera")
        print(f"   - Kit Frenos Completo")

if __name__ == "__main__":
    try:
        agregar_paquetes_ejemplo()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
