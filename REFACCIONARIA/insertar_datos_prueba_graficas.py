#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para insertar datos de prueba en la tabla de ventas
para verificar que las gráficas funcionen correctamente
"""

from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models.venta import Venta, TipoVenta, EstadoVenta
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.usuario import Usuario
from sqlalchemy import func, extract
import random

def crear_clientes_prueba(db):
    """Crear clientes básicos para las ventas de prueba"""
    print("👤 Creando clientes de prueba...")
    
    nombres_clientes = [
        ("Juan", "García", "López"),
        ("María", "Rodríguez", "Martínez"),
        ("Carlos", "López", "González"),
        ("Ana", "Martínez", "Rodríguez"),
        ("Pedro", "González", "García"),
    ]
    
    clientes_creados = 0
    
    for nombre, apellido_p, apellido_m in nombres_clientes:
        cliente = Cliente(
            nombre=nombre,
            apellido_paterno=apellido_p,
            apellido_materno=apellido_m,
            email=f"{nombre.lower()}@example.com",
            telefono="1234567890",
            rfc=f"RCF{random.randint(100000, 999999)}",
            tipo_figura="persona_fisica",
            activo=True,
            local_id=1
        )
        db.add(cliente)
        clientes_creados += 1
    
    db.commit()
    print(f"✅ {clientes_creados} clientes creados")
    return clientes_creados

def insertar_datos_prueba():
    db = SessionLocal()
    
    try:
        print("🔄 Iniciando inserción de datos de prueba...")
        
        # Crear clientes si no existen
        cliente_count = db.query(Cliente).count()
        if cliente_count == 0:
            crear_clientes_prueba(db)
        
        # Obtener usuario admin (necesario para ventas)
        usuario = db.query(Usuario).first()
        if not usuario:
            print("❌ No hay usuarios en la BD")
            return
        
        # Obtener clientes y productos existentes
        clientes = db.query(Cliente).all()
        productos = db.query(Producto).all()
        
        print(f"✅ Usuario: {usuario.nombre_usuario}")
        print(f"✅ Encontrados {len(clientes)} clientes y {len(productos)} productos")
        
        print("📝 Insertando datos de ventas...")
        
        ventas_insertadas = 0
        
        for year in range(2020, 2027):
            # Aproximadamente 10-15 ventas por mes
            for mes in range(1, 13):
                # Determinar cantidad de días en el mes
                if mes in [1, 3, 5, 7, 8, 10, 12]:
                    dias_mes = 31
                elif mes in [4, 6, 9, 11]:
                    dias_mes = 30
                else:  # febrero
                    dias_mes = 29 if year % 4 == 0 else 28
                
                # 10-15 ventas por mes
                ventas_del_mes = random.randint(10, 15)
                
                for i in range(ventas_del_mes):
                    # Fecha aleatoria del mes
                    dia = random.randint(1, dias_mes)
                    fecha = datetime(year, mes, dia)
                    
                    # Seleccionar cliente aleatorio
                    cliente = random.choice(clientes)
                    
                    # Generar monto total entre $100 y $2000
                    monto = random.uniform(100, 2000)
                    subtotal = round(monto, 2)
                    iva_amount = round(subtotal * 0.16, 2)
                    total = round(subtotal + iva_amount, 2)
                    
                    # Crear venta
                    venta = Venta(
                        folio=f"VTA-{year}{mes:02d}{ventas_insertadas:04d}",
                        local_id=1,
                        usuario_id=usuario.id,
                        cliente_id=cliente.id,
                        estado=EstadoVenta.COMPLETADA,
                        tipo_venta=TipoVenta.CONTADO,
                        subtotal=subtotal,
                        iva=iva_amount,
                        total=total,
                        metodo_pago='efectivo',
                        fecha_creacion=fecha,
                        fecha_actualizacion=fecha
                    )
                    
                    db.add(venta)
                    ventas_insertadas += 1
                    
                    if ventas_insertadas % 50 == 0:
                        db.commit()
                        print(f"  ✅ Insertadas {ventas_insertadas} ventas...")
        
        db.commit()
        print(f"\n✅ Inserción completada: {ventas_insertadas} ventas de prueba agregadas")
        
        # Verificar datos por año
        print("\n📊 Resumen de ventas por año:")
        
        resultados = db.query(
            extract('year', Venta.fecha_creacion).label('año'),
            func.count(Venta.id).label('cantidad'),
            func.sum(Venta.total).label('total')
        ).filter(
            Venta.estado == EstadoVenta.COMPLETADA
        ).group_by('año').order_by('año').all()
        
        for resultado in resultados:
            if resultado[0]:
                print(f"  {int(resultado[0])}: {resultado[1]} ventas, Total: ${resultado[2]:,.2f}")
        
        print("\n✨ Datos de prueba listos para verificar gráficas")
        print("🌐 Abre http://localhost:8000/grafica_ventas para ver los datos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insertar_datos_prueba()
