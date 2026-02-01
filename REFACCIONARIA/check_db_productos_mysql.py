import mysql.connector
from mysql.connector import Error

# Configuración (ajusta según tu entorno)
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Cambia por tu contraseña
    'database': 'refaccionaria_db',
    'port': 3306
}

try:
    conn = mysql.connector.connect(**config)
    if conn.is_connected():
        print('✅ Conexión exitosa a MySQL')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM productos')
        total = cursor.fetchone()[0]
        print(f'Total de productos: {total}')
        if total > 0:
            cursor.execute('SELECT id, codigo, nombre, marca, precio_venta FROM productos LIMIT 5')
            for row in cursor.fetchall():
                print(row)
        else:
            print('No hay productos en la tabla.')
        cursor.close()
    else:
        print('❌ No se pudo conectar a MySQL')
except Error as e:
    print(f'Error de MySQL: {e}')
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
