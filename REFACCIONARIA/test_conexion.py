#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test de conexión a la base de datos"""

try:
    from sqlalchemy import text
    from app.core.database import engine
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Conexión exitosa a la BD desde la aplicación")
        print("✅ La API puede conectarse correctamente a MySQL")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("   Verifica que todos los archivos de la app están correctos")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("   Verifica:")
    print("   1. MySQL está corriendo en Laragon")
    print("   2. Credenciales en .env son correctas")
    print("   3. Base de datos refaccionaria_db existe")
