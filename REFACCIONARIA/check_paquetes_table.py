"""Script para verificar si las tablas de paquetes existen en la base de datos"""
import sys
from sqlalchemy import inspect, text
from app.core.database import engine, SessionLocal

def verificar_tablas():
    inspector = inspect(engine)
    tablas = inspector.get_table_names()
    
    print("=== Tablas disponibles en la base de datos ===")
    for tabla in sorted(tablas):
        print(f"  - {tabla}")
    
    print("\n=== Verificando tablas de paquetes ===")
    if "paquetes" in tablas:
        print("✓ Tabla 'paquetes' existe")
        # Mostrar columnas
        columnas = inspector.get_columns("paquetes")
        print("  Columnas:")
        for col in columnas:
            print(f"    - {col['name']} ({col['type']})")
    else:
        print("✗ Tabla 'paquetes' NO existe")
    
    if "paquete_productos" in tablas:
        print("\n✓ Tabla 'paquete_productos' existe")
        columnas = inspector.get_columns("paquete_productos")
        print("  Columnas:")
        for col in columnas:
            print(f"    - {col['name']} ({col['type']})")
    else:
        print("\n✗ Tabla 'paquete_productos' NO existe")
    
    # Contar registros si existen las tablas
    if "paquetes" in tablas:
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT COUNT(*) as count FROM paquetes")).fetchone()
            print(f"\n  Total de paquetes: {result[0]}")
        except Exception as e:
            print(f"\n  Error al contar paquetes: {e}")
        finally:
            db.close()

if __name__ == "__main__":
    try:
        verificar_tablas()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
