#!/usr/bin/env python3
"""Script para consolidar sucursales en la base de datos"""

import mysql.connector
from mysql.connector import Error

def consolidar_sucursales():
    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='refaccionaria_db'
        )
        
        cursor = conn.cursor()
        
        print("🔄 Iniciando consolidación de sucursales...\n")
        
        # 1. Renombrar "Local Principal" (ID 1) a "REFACCIONARIA OVIEDO"
        print("1️⃣ Renombrando 'Local Principal' a 'REFACCIONARIA OVIEDO'...")
        cursor.execute("""
            UPDATE locales 
            SET nombre = %s 
            WHERE id = 1
        """, ("REFACCIONARIA OVIEDO",))
        print(f"   ✅ Actualizado ID 1: {cursor.rowcount} fila(s) afectada(s)")
        
        # 2. Renombrar "REFACCIÓN PARA OVIEDO" (ID 3) a "FILTROS Y LUBRICANTES"
        print("\n2️⃣ Renombrando 'REFACCIÓN PARA OVIEDO' a 'FILTROS Y LUBRICANTES'...")
        cursor.execute("""
            UPDATE locales 
            SET nombre = %s 
            WHERE id = 3
        """, ("FILTROS Y LUBRICANTES",))
        print(f"   ✅ Actualizado ID 3: {cursor.rowcount} fila(s) afectada(s)")
        
        # 3. Reasignar todos los registros del ID 2 al ID 1
        print("\n3️⃣ Reasignando datos de ID 2 a ID 1...")
        
        # Usuarios
        cursor.execute("UPDATE usuarios SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Usuarios: {cursor.rowcount} actualizado(s)")
        
        # Clientes
        cursor.execute("UPDATE clientes SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Clientes: {cursor.rowcount} actualizado(s)")
        
        # Ventas
        cursor.execute("UPDATE ventas SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Ventas: {cursor.rowcount} actualizado(s)")
        
        # Inventario
        cursor.execute("UPDATE inventario_local SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Inventario: {cursor.rowcount} actualizado(s)")
        
        # Retiros Caja
        cursor.execute("UPDATE retiros_caja SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Retiros Caja: {cursor.rowcount} actualizado(s)")
        
        # Arqueos Caja
        cursor.execute("UPDATE arqueos_caja SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Arqueos Caja: {cursor.rowcount} actualizado(s)")
        
        # Cierres Caja
        cursor.execute("UPDATE cierres_caja SET local_id = 1 WHERE local_id = 2")
        print(f"   ✅ Cierres Caja: {cursor.rowcount} actualizado(s)")
        
        # 4. Reasignar todos los registros del ID 4 al ID 3
        print("\n4️⃣ Reasignando datos de ID 4 a ID 3...")
        
        # Usuarios
        cursor.execute("UPDATE usuarios SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Usuarios: {cursor.rowcount} actualizado(s)")
        
        # Clientes
        cursor.execute("UPDATE clientes SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Clientes: {cursor.rowcount} actualizado(s)")
        
        # Ventas
        cursor.execute("UPDATE ventas SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Ventas: {cursor.rowcount} actualizado(s)")
        
        # Inventario
        cursor.execute("UPDATE inventario_local SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Inventario: {cursor.rowcount} actualizado(s)")
        
        # Retiros Caja
        cursor.execute("UPDATE retiros_caja SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Retiros Caja: {cursor.rowcount} actualizado(s)")
        
        # Arqueos Caja
        cursor.execute("UPDATE arqueos_caja SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Arqueos Caja: {cursor.rowcount} actualizado(s)")
        
        # Cierres Caja
        cursor.execute("UPDATE cierres_caja SET local_id = 3 WHERE local_id = 4")
        print(f"   ✅ Cierres Caja: {cursor.rowcount} actualizado(s)")
        
        # 5. Eliminar sucursales duplicadas
        print("\n5️⃣ Eliminando sucursales duplicadas...")
        
        cursor.execute("DELETE FROM locales WHERE id = 2")
        print(f"   ✅ Eliminado ID 2: {cursor.rowcount} fila(s)")
        
        cursor.execute("DELETE FROM locales WHERE id = 4")
        print(f"   ✅ Eliminado ID 4: {cursor.rowcount} fila(s)")
        
        # Commit de cambios
        conn.commit()
        print("\n✅ Consolidación completada exitosamente")
        
        # Mostrar estado final
        print("\n📋 Estado final de sucursales:")
        cursor.execute("SELECT id, nombre FROM locales ORDER BY id")
        sucursales = cursor.fetchall()
        for suc_id, nombre in sucursales:
            print(f"   - ID {suc_id}: {nombre}")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    consolidar_sucursales()
