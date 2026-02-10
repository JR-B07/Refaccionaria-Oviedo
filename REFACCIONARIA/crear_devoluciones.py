#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para crear ventas con estado devuelta para testing"""

from app.core.database import SessionLocal
from app.models.venta import Venta
from app.models.usuario import Usuario
from app.models.local import Local
from datetime import datetime, timedelta
import random

db = SessionLocal()

print("=" * 70)
print("VERIFICANDO Y CREANDO VENTAS CON ESTADO 'DEVUELTA'")
print("=" * 70)

# Verificar ventas existentes
ventas_total = db.query(Venta).count()
ventas_devueltas = db.query(Venta).filter(Venta.estado == "devuelta").count()

print(f"\n📊 Estado de la base de datos:")
print(f"  • Total de ventas: {ventas_total}")
print(f"  • Ventas devueltas: {ventas_devueltas}")

if ventas_devueltas > 0:
    print(f"\n✅ Ya hay {ventas_devueltas} ventas con estado 'devuelta'")
else:
    print(f"\n⚠️ No hay ventas con estado 'devuelta'")
    print("\n🔄 Convertiremos algunas ventas existentes a estado 'devuelta' para pruebas...")
    
    # Obtener algunas ventas completadas
    ventas_completadas = db.query(Venta).filter(
        Venta.estado == "completada"
    ).limit(5).all()
    
    if not ventas_completadas:
        print("\n❌ No hay ventas completadas para convertir")
        print("   Necesitas crear algunas ventas primero")
    else:
        print(f"\n✅ Encontradas {len(ventas_completadas)} ventas completadas")
        print("\n📝 Convirtiendo a estado 'devuelta'...")
        
        for i, venta in enumerate(ventas_completadas, 1):
            venta.estado = "devuelta"
            # Actualizar fecha de modificación
            venta.fecha_modificacion = datetime.now() - timedelta(days=random.randint(1, 30))
            
            print(f"  {i}. Venta {venta.folio} → devuelta")
        
        db.commit()
        print(f"\n✅ {len(ventas_completadas)} ventas convertidas a estado 'devuelta'")

# Verificar nuevamente
ventas_devueltas_final = db.query(Venta).filter(Venta.estado == "devuelta").count()
print(f"\n📊 Estado final:")
print(f"  • Ventas devueltas: {ventas_devueltas_final}")

if ventas_devueltas_final > 0:
    print("\n🎉 ¡Listo! Ahora puedes ver datos en el reporte de devoluciones")
    
    # Mostrar algunas ventas devueltas
    ventas_dev = db.query(Venta).filter(Venta.estado == "devuelta").limit(3).all()
    
    print("\n📋 Ejemplos de ventas devueltas:")
    for venta in ventas_dev:
        print(f"\n  • Folio: {venta.folio}")
        print(f"    Total: ${float(venta.total):,.2f}")
        print(f"    Fecha: {venta.fecha_creacion.strftime('%Y-%m-%d')}")

db.close()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO")
print("=" * 70)
