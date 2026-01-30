"""
Script para agregar las columnas de retiros a la tabla arqueos_caja
"""
import pymysql
import sys
from app.core.config import settings

def main():
    try:
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos...")
        connection = pymysql.connect(
            host=settings.MYSQL_SERVER,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DB,
            port=settings.MYSQL_PORT
        )
        
        cursor = connection.cursor()
        
        # Verificar si las columnas ya existen
        print("\n🔍 Verificando si las columnas ya existen...")
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
              AND TABLE_NAME = 'arqueos_caja' 
              AND COLUMN_NAME IN ('retiros_declarado', 'retiros_contado', 'diferencia_retiros')
        """, (settings.MYSQL_DB,))
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        if len(existing_columns) == 3:
            print("✅ Las columnas de retiros ya existen. No es necesario migrar.")
            return
        
        print(f"📊 Columnas existentes: {existing_columns}")
        print("➕ Agregando columnas faltantes...")
        
        # Agregar columnas si no existen
        if 'retiros_declarado' not in existing_columns:
            print("   - Agregando retiros_declarado...")
            cursor.execute("""
                ALTER TABLE arqueos_caja 
                ADD COLUMN retiros_declarado DECIMAL(12,2) DEFAULT 0.00 AFTER efectivo_declarado
            """)
        
        if 'retiros_contado' not in existing_columns:
            print("   - Agregando retiros_contado...")
            cursor.execute("""
                ALTER TABLE arqueos_caja 
                ADD COLUMN retiros_contado DECIMAL(12,2) DEFAULT 0.00 AFTER efectivo_contado
            """)
        
        if 'diferencia_retiros' not in existing_columns:
            print("   - Agregando diferencia_retiros...")
            cursor.execute("""
                ALTER TABLE arqueos_caja 
                ADD COLUMN diferencia_retiros DECIMAL(12,2) DEFAULT 0.00 AFTER diferencia_efectivo
            """)
        
        # Confirmar cambios
        connection.commit()
        
        # Verificar las columnas agregadas
        print("\n✅ Verificando columnas agregadas:")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, COLUMN_DEFAULT, ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
              AND TABLE_NAME = 'arqueos_caja' 
              AND COLUMN_NAME LIKE '%%retiros%%'
            ORDER BY ORDINAL_POSITION
        """, (settings.MYSQL_DB,))
        
        for row in cursor.fetchall():
            print(f"   ✓ {row[0]} ({row[1]}) - Default: {row[2]} - Posición: {row[3]}")
        
        print("\n🎉 ¡Migración completada exitosamente!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
