#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar el estado de los datos en la base de datos.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def get_database_url() -> str:
    """Construir URL de conexión a base de datos"""
    user = os.getenv("MYSQL_USER", "root").strip()
    password = os.getenv("MYSQL_PASSWORD", "").strip()
    host = os.getenv("MYSQL_SERVER", "localhost").strip()
    port = os.getenv("MYSQL_PORT", "3306").strip()
    database = os.getenv("MYSQL_DB", "refaccionaria_db").strip()
    
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    else:
        return f"mysql+pymysql://{user}@{host}:{port}/{database}"

try:
    print("=" * 80)
    print("VERIFICACIÓN DE DATOS EN BASE DE DATOS")
    print("=" * 80)
    
    database_url = get_database_url()
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        tablas_verificar = [
            ("locales", "Sucursales/Locales"),
            ("usuarios", "Usuarios"),
            ("productos", "Productos"),
            ("clientes", "Clientes"),
            ("proveedores", "Proveedores"),
            ("marcas", "Marcas"),
            ("ventas", "Ventas"),
            ("compras", "Compras"),
            ("gastos", "Gastos"),
            ("inventario_local", "Inventario por Local"),
            ("paquetes", "Paquetes"),
            ("grupos", "Grupos"),
            ("promociones", "Promociones"),
            ("arqueos_caja", "Arqueos de Caja"),
            ("cierres_caja", "Cierres de Caja"),
            ("retiros_caja", "Retiros de Caja"),
        ]
        
        print("\n📊 RESUMEN DE DATOS\n")
        print(f"{'Tabla':<25} | {'Descripción':<30} | {'Registros':<10}")
        print("-" * 80)
        
        datos_faltantes = []
        datos_existentes = []
        
        for tabla, descripcion in tablas_verificar:
            try:
                query = text(f"SELECT COUNT(*) FROM {tabla}")
                result = connection.execute(query)
                count = result.fetchone()[0]
                
                status = "✅" if count > 0 else "⚠️ "
                print(f"{status} {tabla:<23} | {descripcion:<30} | {count:<10}")
                
                if count == 0:
                    datos_faltantes.append((tabla, descripcion))
                else:
                    datos_existentes.append((tabla, descripcion, count))
                    
            except Exception as e:
                print(f"❌ {tabla:<23} | Error: {str(e)[:40]}")
        
        print("\n" + "=" * 80)
        print("RESUMEN")
        print("=" * 80)
        
        if datos_faltantes:
            print(f"\n⚠️  TABLAS VACÍAS ({len(datos_faltantes)}):")
            for tabla, desc in datos_faltantes:
                print(f"   - {desc} ({tabla})")
        
        if datos_existentes:
            print(f"\n✅ TABLAS CON DATOS ({len(datos_existentes)}):")
            for tabla, desc, count in datos_existentes:
                print(f"   - {desc} ({tabla}): {count} registros")
        
        print("\n" + "=" * 80)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
