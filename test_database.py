#!/usr/bin/env python3
"""
Script para validar la base de datos consolidada
Verifica:
1. Conexión a MySQL
2. Existencia de las 25 tablas esperadas
3. Relaciones entre tablas (Foreign Keys)
4. Índices importantes
"""

import sys
import pymysql
from pymysql import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv('REFACCIONARIA/.env')

# Configuración de la BD
DB_CONFIG = {
    'host': os.getenv('MYSQL_SERVER', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DB', 'refaccionaria_db'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

# Tablas esperadas según el archivo consolidado
EXPECTED_TABLES = [
    'configuracion_sistema', 'locales', 'usuarios', 'marcas',
    'productos', 'inventario_local', 'clientes', 'proveedores',
    'ventas', 'detalle_ventas', 'compras', 'detalle_compras',
    'traspasos', 'detalle_traspasos', 'gastos', 'arqueos_caja',
    'cierres_caja', 'retiros_caja', 'vales_venta', 'paquetes',
    'paquete_productos', 'grupos', 'grupo_productos',
    'grupo_aplicaciones', 'promociones', 'asistencia_empleados'
]

def test_connection():
    """Prueba la conexión a MySQL"""
    print("🔌 Probando conexión a MySQL...")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print(f"✅ Conexión exitosa a: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_database_exists():
    """Verifica si la base de datos existe"""
    print(f"\n📊 Verificando base de datos '{DB_CONFIG['database']}'...")
    try:
        # Conectar sin especificar base de datos
        config = DB_CONFIG.copy()
        db_name = config.pop('database')
        
        connection = pymysql.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if db_name in databases:
            print(f"✅ Base de datos '{db_name}' existe")
            cursor.close()
            connection.close()
            return True
        else:
            print(f"⚠️  Base de datos '{db_name}' NO existe")
            print(f"   Ejecuta: mysql -u root -p < refaccionaria_db.sql")
            cursor.close()
            connection.close()
            return False
    except Error as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def test_tables():
    """Verifica que todas las tablas esperadas existan"""
    print(f"\n📋 Verificando {len(EXPECTED_TABLES)} tablas...")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"   Tablas encontradas: {len(existing_tables)}")
        
        missing = []
        extra = []
        
        for table in EXPECTED_TABLES:
            if table not in existing_tables:
                missing.append(table)
        
        for table in existing_tables:
            if table not in EXPECTED_TABLES:
                extra.append(table)
        
        if not missing and not extra:
            print("✅ Todas las tablas coinciden perfectamente")
        else:
            if missing:
                print(f"⚠️  Tablas faltantes ({len(missing)}):")
                for t in missing:
                    print(f"   - {t}")
            if extra:
                print(f"⚠️  Tablas extra no esperadas ({len(extra)}):")
                for t in extra:
                    print(f"   - {t}")
        
        cursor.close()
        connection.close()
        return len(missing) == 0
    except Error as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def test_foreign_keys():
    """Verifica que las llaves foráneas estén configuradas"""
    print("\n🔗 Verificando llaves foráneas...")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        query = """
        SELECT 
            TABLE_NAME,
            CONSTRAINT_NAME,
            REFERENCED_TABLE_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s
            AND REFERENCED_TABLE_NAME IS NOT NULL
        ORDER BY TABLE_NAME
        """
        
        cursor.execute(query, (DB_CONFIG['database'],))
        foreign_keys = cursor.fetchall()
        
        print(f"   Llaves foráneas encontradas: {len(foreign_keys)}")
        
        if len(foreign_keys) > 0:
            print("✅ Relaciones entre tablas configuradas correctamente")
            
            # Mostrar algunas relaciones importantes
            print("\n   Relaciones clave:")
            important_tables = ['ventas', 'compras', 'arqueos_caja', 'retiros_caja']
            for table, constraint, ref_table in foreign_keys:
                if table in important_tables:
                    print(f"   - {table} → {ref_table}")
        else:
            print("⚠️  No se encontraron llaves foráneas")
        
        cursor.close()
        connection.close()
        return len(foreign_keys) > 0
    except Error as e:
        print(f"❌ Error verificando llaves foráneas: {e}")
        return False

def test_indexes():
    """Verifica que los índices importantes existan"""
    print("\n🔍 Verificando índices...")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Verificar índices en tablas críticas (por columna, no por nombre exacto)
        critical_indexes = [
            ('ventas', 'folio'),
            ('productos', 'codigo'),
            ('usuarios', 'nombre_usuario'),
            ('retiros_caja', 'folio'),
        ]
        
        found = 0
        missing = 0
        
        for table, column in critical_indexes:
            cursor.execute(f"SHOW INDEX FROM {table} WHERE Column_name = %s", (column,))
            if cursor.fetchone():
                found += 1
            else:
                missing += 1
                print(f"   ⚠️  Sin índice en columna: {table}.{column}")
        
        if missing == 0:
            print(f"✅ Todos los índices críticos presentes ({found} verificados)")
        else:
            print(f"⚠️  {missing} índices faltantes de {len(critical_indexes)}")
        
        cursor.close()
        connection.close()
        return missing == 0
    except Error as e:
        print(f"❌ Error verificando índices: {e}")
        return False

def test_sample_data():
    """Verifica si hay datos de ejemplo"""
    print("\n📦 Verificando datos de ejemplo...")
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Verificar configuración del sistema
        cursor.execute("SELECT COUNT(*) FROM configuracion_sistema")
        config_count = cursor.fetchone()[0]
        
        # Verificar gastos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM gastos")
        gastos_count = cursor.fetchone()[0]
        
        # Verificar promociones
        cursor.execute("SELECT COUNT(*) FROM promociones")
        promo_count = cursor.fetchone()[0]
        
        print(f"   Configuraciones: {config_count}")
        print(f"   Gastos de ejemplo: {gastos_count}")
        print(f"   Promociones: {promo_count}")
        
        if config_count >= 7 and gastos_count >= 5 and promo_count >= 1:
            print("✅ Datos iniciales cargados correctamente")
        else:
            print("⚠️  Algunos datos iniciales pueden faltar")
        
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"❌ Error verificando datos: {e}")
        return False

def main():
    print("=" * 60)
    print("🔬 PRUEBA DE BASE DE DATOS CONSOLIDADA")
    print("   refaccionaria_db.sql")
    print("=" * 60)
    
    tests = [
        ("Conexión MySQL", test_connection),
        ("Base de datos existe", test_database_exists),
        ("Tablas (25 esperadas)", test_tables),
        ("Llaves foráneas", test_foreign_keys),
        ("Índices", test_indexes),
        ("Datos de ejemplo", test_sample_data),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error inesperado en '{name}': {e}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! La base de datos está lista.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron.")
        print("\nPara corregir, ejecuta:")
        print("  mysql -u root -p < refaccionaria_db.sql")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Prueba interrumpida por el usuario")
        sys.exit(1)
