#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para generar hashes SHA256 de contraseñas.
Usa este script para generar nuevos hashes cuando necesites crear usuarios.
"""

import hashlib
import sys

def generar_hash_sha256(password: str) -> str:
    """Genera hash SHA256 de una contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    print("=" * 80)
    print("GENERADOR DE HASHES SHA256")
    print("=" * 80)
    
    # Contraseñas de ejemplo
    contraseñas_ejemplo = {
        'admin': 'admin',
        'admin123': 'admin123', 
        'sucursal1': 'sucursal1',
        'sucursal2': 'sucursal2',
        'sucursal123': 'sucursal123',
        'password123': 'password123'
    }
    
    print("\nHashes SHA256 de contraseñas comunes:\n")
    for nombre, password in contraseñas_ejemplo.items():
        hash_val = generar_hash_sha256(password)
        print(f"Contraseña: {nombre:15} -> {hash_val}")
    
    print("\n" + "=" * 80)
    print("GENERADOR INTERACTIVO")
    print("=" * 80)
    
    if len(sys.argv) > 1:
        # Si se pasa una contraseña como argumento
        password = sys.argv[1]
        hash_val = generar_hash_sha256(password)
        print(f"\nHash SHA256 de '{password}':")
        print(hash_val)
    else:
        # Modo interactivo
        print("\nIngresa una contraseña para generar su hash SHA256 (o presiona Enter para salir):")
        while True:
            password = input("\nContraseña: ").strip()
            if not password:
                print("Saliendo...")
                break
            hash_val = generar_hash_sha256(password)
            print(f"Hash SHA256: {hash_val}")
