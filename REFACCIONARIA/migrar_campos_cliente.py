"""
Script para migrar los nuevos campos a la tabla clientes
Campos a agregar: alias, tipo_figura
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
              AND TABLE_NAME = 'clientes' 
              AND COLUMN_NAME IN ('alias', 'tipo_figura')
        """, (settings.MYSQL_DB,))
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Columnas existentes: {existing_columns}")
        print("➕ Agregando columnas faltantes...")
        
        # Agregar columnas si no existen
        if 'alias' not in existing_columns:
            print("   - Agregando alias...")
            cursor.execute("""
                ALTER TABLE clientes 
                ADD COLUMN alias VARCHAR(100) AFTER nombre
            """)
            cursor.execute("""
                SELECT COUNT(1) 
                FROM INFORMATION_SCHEMA.STATISTICS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'clientes' AND INDEX_NAME = 'idx_clientes_alias'
            """, (settings.MYSQL_DB,))
            has_index = cursor.fetchone()[0]
            if not has_index:
                cursor.execute("""CREATE INDEX idx_clientes_alias ON clientes(alias)""")
        
        if 'tipo_figura' not in existing_columns:
            print("   - Agregando tipo_figura...")
            cursor.execute("""
                ALTER TABLE clientes 
                ADD COLUMN tipo_figura VARCHAR(50) DEFAULT 'Persona Física' AFTER rfc
            """)
        
        # Confirmar cambios
        connection.commit()
        
        # Verificar las columnas agregadas
        print("\n✅ Verificando columnas agregadas:")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, COLUMN_DEFAULT, ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
              AND TABLE_NAME = 'clientes' 
              AND COLUMN_NAME IN ('alias', 'tipo_figura')
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
