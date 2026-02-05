#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar y resetear Refaccionaria ERP
ADVERTENCIA: Este script elimina todos los datos de la base de datos
"""

import os
import sys
from pathlib import Path

def print_warning(text):
    print(f"\033[91m{text}\033[0m")

def print_success(text):
    print(f"\033[92m{text}\033[0m")

def main():
    print("\n" + "="*60)
    print("  LIMPIAR BASE DE DATOS - REFACCIONARIA ERP")
    print("="*60 + "\n")
    
    print_warning("⚠️  ADVERTENCIA: Este script eliminara TODOS los datos de la base de datos")
    print("   No se puede deshacer esta accion\n")
    
    respuesta = input("¿Deseas continuar? (SI/NO): ").strip().upper()
    
    if respuesta != "SI":
        print("Operacion cancelada\n")
        return
    
    # Confirmacion adicional
    respuesta = input("¿ESTA SEGURO? Esto borrara todos los datos (SI/NO): ").strip().upper()
    
    if respuesta != "SI":
        print("Operacion cancelada\n")
        return
    
    print("\nProcediendo con la limpieza...\n")
    
    try:
        from app.database import engine
        from app.models import Base
        
        print("Eliminando tablas...")
        Base.metadata.drop_all(bind=engine)
        print_success("Tablas eliminadas\n")
        
        print("Recreando tablas...")
        Base.metadata.create_all(bind=engine)
        print_success("Tablas recreadas\n")
        
        # Limpiar archivos de log
        if Path("server.log").exists():
            Path("server.log").unlink()
            print("Limpiado server.log")
        
        # Limpiar directorio de logs
        if Path("logs").exists():
            import shutil
            shutil.rmtree("logs")
            Path("logs").mkdir()
            print("Limpiado directorio logs/")
        
        print("\n" + "="*60)
        print_success("✓ Base de datos limpiada exitosamente")
        print("="*60 + "\n")
        
        print("Proximos pasos:")
        print("1. Ejecuta: python scripts/inicializar_datos.py")
        print("   Para cargar datos iniciales")
        print("2. O ejecuta Refaccionaria.bat para iniciar desde cero\n")
        
    except Exception as e:
        print_warning(f"\n✗ Error durante la limpieza: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
