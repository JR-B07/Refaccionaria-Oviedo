#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos con datos por defecto
Verifica si existen productos y paquetes, y los carga si es necesario
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raiz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from app.database import SessionLocal, engine
    from app.models import Base, Producto, Paquete
    from sqlalchemy import text
except ImportError as e:
    print(f"[ERROR] No se pudieron importar los modulos: {e}")
    print("Asegurate de estar en el directorio correcto y tener instaladas las dependencias")
    sys.exit(1)


def verificar_conexion_db():
    """Verifica que la conexion a la base de datos sea posible"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Conexion a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"✗ Error conectando a la base de datos: {e}")
        return False


def crear_tablas():
    """Crea las tablas de la base de datos si no existen"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Tablas de la base de datos verificadas/creadas")
        return True
    except Exception as e:
        print(f"✗ Error creando tablas: {e}")
        return False


def contar_productos():
    """Cuenta los productos existentes"""
    try:
        db = SessionLocal()
        count = db.query(Producto).count()
        db.close()
        return count
    except Exception as e:
        print(f"Advertencia al contar productos: {e}")
        return -1


def contar_paquetes():
    """Cuenta los paquetes existentes"""
    try:
        db = SessionLocal()
        count = db.query(Paquete).count()
        db.close()
        return count
    except Exception as e:
        print(f"Advertencia al contar paquetes: {e}")
        return -1


def cargar_productos_iniciales():
    """Carga los productos iniciales si la tabla esta vacia"""
    db = SessionLocal()
    try:
        # Definir los 100 productos
        productos_data = [
            {"codigo": "001", "nombre": "Aceite Motor 5W30", "marca": "Valvoline", "categoria": "Fluidos", 
             "descripcion": "Aceite mineral sintético para motores", "precio_compra": 25.00, "precio_venta": 35.00, "stock_minimo": 10},
            {"codigo": "002", "nombre": "Filtro Aire Cabina", "marca": "Mann", "categoria": "Filtros",
             "descripcion": "Filtro de aire para cabina", "precio_compra": 15.00, "precio_venta": 22.50, "stock_minimo": 5},
            {"codigo": "003", "nombre": "Pastillas Freno Delantera", "marca": "Brembo", "categoria": "Frenos",
             "descripcion": "Juego de pastillas de freno delantera", "precio_compra": 45.00, "precio_venta": 65.00, "stock_minimo": 3},
            {"codigo": "004", "nombre": "Bateria 12V 70A", "marca": "Bosch", "categoria": "Electricidad",
             "descripcion": "Bateria de 70 Ah, 12 voltios", "precio_compra": 120.00, "precio_venta": 180.00, "stock_minimo": 2},
            {"codigo": "005", "nombre": "Limpiaparabrisas", "marca": "Bosch", "categoria": "Limpieza",
             "descripcion": "Juego de escobillas limpiaparabrisas", "precio_compra": 12.00, "precio_venta": 18.00, "stock_minimo": 5},
            {"codigo": "006", "nombre": "Cilindro Maestro Freno", "marca": "ATE", "categoria": "Frenos",
             "descripcion": "Cilindro maestro de freno", "precio_compra": 85.00, "precio_venta": 125.00, "stock_minimo": 2},
            {"codigo": "007", "nombre": "Discos Freno", "marca": "Brembo", "categoria": "Frenos",
             "descripcion": "Par de discos de freno ventilados", "precio_compra": 75.00, "precio_venta": 110.00, "stock_minimo": 2},
            {"codigo": "008", "nombre": "Amortiguador Delantera", "marca": "KYB", "categoria": "Suspension",
             "descripcion": "Amortiguador hidraulico delantero", "precio_compra": 95.00, "precio_venta": 140.00, "stock_minimo": 2},
            {"codigo": "009", "nombre": "Correa Serpentina", "marca": "Gates", "categoria": "Motor",
             "descripcion": "Correa serpentina para motor", "precio_compra": 30.00, "precio_venta": 45.00, "stock_minimo": 5},
            {"codigo": "010", "nombre": "Bujia Encendido", "marca": "NGK", "categoria": "Electricidad",
             "descripcion": "Juego de 4 bujias de encendido", "precio_compra": 20.00, "precio_venta": 30.00, "stock_minimo": 10},
        ]

        # Agregar productos
        for prod in productos_data:
            p = Producto(**prod)
            db.add(p)
        
        db.commit()
        print(f"✓ Se cargaron {len(productos_data)} productos iniciales")
        return True
    except Exception as e:
        db.rollback()
        print(f"✗ Error cargando productos: {e}")
        return False
    finally:
        db.close()


def cargar_paquetes_iniciales():
    """Carga los paquetes iniciales si la tabla esta vacia"""
    db = SessionLocal()
    try:
        paquetes_data = [
            {"nombre": "Kit Suspension Delantera", "clase": "Suspension", "descripcion": "Conjunto completo de suspension delantera"},
            {"nombre": "Kit Frenos Completo", "clase": "Frenos", "descripcion": "Sistema completo de frenos delantera y trasera"},
            {"nombre": "Kit Mantenimiento Motor", "clase": "Motor", "descripcion": "Paquete de mantenimiento completo del motor"},
            {"nombre": "Kit Iluminacion", "clase": "Electricidad", "descripcion": "Juego completo de luces del vehiculo"},
            {"nombre": "Kit Embrague", "clase": "Transmision", "descripcion": "Kit completo de embrague y volante"},
        ]
        
        for paq in paquetes_data:
            from app.models import Paquete
            p = Paquete(**paq)
            db.add(p)
        
        db.commit()
        print(f"✓ Se cargaron {len(paquetes_data)} paquetes iniciales")
        return True
    except Exception as e:
        db.rollback()
        print(f"✗ Error cargando paquetes: {e}")
        return False
    finally:
        db.close()


def main():
    """Funcion principal"""
    print("\n" + "="*50)
    print("  INICIALIZACION DE BASE DE DATOS")
    print("="*50 + "\n")
    
    # Verificar conexion
    if not verificar_conexion_db():
        print("\n[ERROR] No se puede conectar a la base de datos")
        sys.exit(1)
    
    # Crear tablas
    if not crear_tablas():
        print("\n[ERROR] No se pudieron crear las tablas")
        sys.exit(1)
    
    # Verificar y cargar datos
    print("\nVerificando estado de datos...")
    num_productos = contar_productos()
    num_paquetes = contar_paquetes()
    
    print(f"  - Productos: {num_productos}")
    print(f"  - Paquetes: {num_paquetes}\n")
    
    # Cargar productos si es necesario
    if num_productos == 0:
        print("Cargando productos iniciales...")
        cargar_productos_iniciales()
    else:
        print(f"✓ Hay {num_productos} productos en la base de datos")
    
    # Cargar paquetes si es necesario
    if num_paquetes == 0:
        print("Cargando paquetes iniciales...")
        cargar_paquetes_iniciales()
    else:
        print(f"✓ Hay {num_paquetes} paquetes en la base de datos")
    
    print("\n" + "="*50)
    print("  BASE DE DATOS LISTA")
    print("="*50 + "\n")
    print("La aplicacion esta lista para iniciar")


if __name__ == "__main__":
    main()
