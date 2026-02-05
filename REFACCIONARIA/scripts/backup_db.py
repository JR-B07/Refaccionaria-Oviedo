#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para hacer backup de la base de datos Refaccionaria ERP
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("  BACKUP - REFACCIONARIA ERP")
    print("="*60 + "\n")
    
    # Crear carpeta backups si no existe
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    # Nombre del archivo de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"refaccionaria_backup_{timestamp}.sql"
    
    print(f"Creando backup de la base de datos...\n")
    print(f"Archivo: {backup_file}\n")
    
    try:
        # Comando para hacer dump de la base de datos
        cmd = [
            'mysqldump',
            '-u', 'root',
            '-proot',
            '-h', 'localhost',
            'refaccionaria_db',
            '>', str(backup_file)
        ]
        
        # Ejecutar comando
        resultado = os.system(f'mysqldump -u root -proot -h localhost refaccionaria_db > "{backup_file}"')
        
        if resultado == 0:
            print(f"\033[92m✓ Backup creado exitosamente\033[0m\n")
            print(f"   Ubicacion: {backup_file}")
            print(f"   Tamano: {backup_file.stat().st_size / 1024:.2f} KB\n")
            
            print("Backups disponibles:")
            for backup in sorted(backup_dir.glob("*.sql"))[-5:]:  # Mostrar ultimos 5
                size_kb = backup.stat().st_size / 1024
                print(f"  - {backup.name} ({size_kb:.2f} KB)")
            
            print("\nPara restaurar un backup, ejecuta:")
            print(f'  mysql -u root -proot < backups/{backup_file.name}')
        else:
            print(f"\033[91m✗ Error durante el backup\033[0m\n")
            print("Asegurate que:")
            print("  - MySQL este instalado")
            print("  - MySQL este en el PATH")
            print("  - Las credenciales sean correctas")
            sys.exit(1)
            
    except Exception as e:
        print(f"\033[91m✗ Error: {e}\033[0m\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
