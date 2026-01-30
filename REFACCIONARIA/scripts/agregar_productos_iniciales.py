"""
Script para agregar productos iniciales a la base de datos
Basado en el listado de productos de la refaccionaria
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.producto import Producto
from sqlalchemy import text

def agregar_productos():
    db = SessionLocal()
    try:
        # Productos del listado visible en la imagen
        productos = [
            {
                "codigo": "LS-T1126 HS",
                "nombre": "EMPAQUE DE PLOMO",
                "marca": "DC",
                "categoria": "FORD / MAZDA / MERCURY",
                "descripcion": "CENTRAL AUT. CHEVROLET EQ...",
                "precio_compra": 45.00,
                "precio_venta": 65.00,
                "stock_minimo": 5
            },
            {
                "codigo": "TF-214",
                "nombre": "EMPAQUE DE TRANSMISION",
                "marca": "DCA",
                "categoria": "TOYOTA, SCION, LEXUS",
                "descripcion": "CHEVROLET COLORADO...",
                "precio_compra": 85.00,
                "precio_venta": 120.00,
                "stock_minimo": 3
            },
            {
                "codigo": "B-9293",
                "nombre": "BOMBA DE AGUA",
                "marca": "BW AUTOMOTIVE",
                "categoria": "NISSAN AVRIO 1.6 1.6...",
                "descripcion": "Bomba de agua para diversos modelos",
                "precio_compra": 350.00,
                "precio_venta": 495.00,
                "stock_minimo": 2
            },
            {
                "codigo": "HA-1190-1",
                "nombre": "TORNILLO DE CARROCERIA",
                "marca": "DORL",
                "categoria": "CHEVROLET",
                "descripcion": "Tornillo de carrocería universal",
                "precio_compra": 8.50,
                "precio_venta": 15.00,
                "stock_minimo": 50
            },
            {
                "codigo": "BE-39570-VL",
                "nombre": "RETEN CIGUEÑAL",
                "marca": "TF VICTOR",
                "categoria": "NISSAN",
                "descripcion": "AEROSSTAR, EXPLORER...",
                "precio_compra": 65.00,
                "precio_venta": 95.00,
                "stock_minimo": 10
            },
            {
                "codigo": "SE-T-R-0",
                "nombre": "SELLO DE SILICONE SHOCK",
                "marca": "TOWI",
                "categoria": "VW. CORRADO 92-2.8R...",
                "descripcion": "VW. POINTER (4-1.8 S...",
                "precio_compra": 25.00,
                "precio_venta": 40.00,
                "stock_minimo": 15
            },
            {
                "codigo": "4BX7002 020",
                "nombre": "EMPAQUE DE BRIDA",
                "marca": "MAHLE",
                "categoria": "Universal",
                "descripcion": "Empaque de brida universal",
                "precio_compra": 12.00,
                "precio_venta": 22.00,
                "stock_minimo": 20
            },
            {
                "codigo": "CL-95",
                "nombre": "ABRAZAD CHECA",
                "marca": "TF MICUNI",
                "categoria": "VW. CORRADO 92-2.8R...",
                "descripcion": "VW. POINTER (4-1.8 S...",
                "precio_compra": 18.00,
                "precio_venta": 30.00,
                "stock_minimo": 25
            },
            {
                "codigo": "NEZ-7430050-5M",
                "nombre": "DRENAJE CRILCA",
                "marca": "EBAO",
                "categoria": "CHEVROLET, PONTIAC...",
                "descripcion": "MINI COOPER",
                "precio_compra": 55.00,
                "precio_venta": 85.00,
                "stock_minimo": 8
            },
            {
                "codigo": "MYY-2BBI38",
                "nombre": "VALVO DE INFLADORES",
                "marca": "KNT",
                "categoria": "Universal",
                "descripcion": "Válvula de infladores universal",
                "precio_compra": 5.00,
                "precio_venta": 10.00,
                "stock_minimo": 100
            },
            {
                "codigo": "32017",
                "nombre": "AMORTIGUADORES",
                "marca": "KYB",
                "categoria": "DODGE, NITRO TODAV R...",
                "descripcion": "Amortiguador trasero",
                "precio_compra": 580.00,
                "precio_venta": 850.00,
                "stock_minimo": 4
            },
            {
                "codigo": "D89HHT00650",
                "nombre": "FILTRO ACCIDENTE",
                "marca": "BOSH",
                "categoria": "Universal",
                "descripcion": "Filtro de accidente",
                "precio_compra": 95.00,
                "precio_venta": 145.00,
                "stock_minimo": 6
            },
            {
                "codigo": "CD-1948N",
                "nombre": "BANDA DE TIEMPO",
                "marca": "KANADIAN",
                "categoria": "FORD CONTOUR 1.6 2.0...",
                "descripcion": "DUR. MINI COOPER 1.6 1...",
                "precio_compra": 185.00,
                "precio_venta": 275.00,
                "stock_minimo": 3
            },
            {
                "codigo": "FE-3803",
                "nombre": "JOYA DE DISTRIBUCION",
                "marca": "UTAGAVAS IDEM",
                "categoria": "Universal",
                "descripcion": "Joya de distribución universal",
                "precio_compra": 125.00,
                "precio_venta": 185.00,
                "stock_minimo": 5
            },
            {
                "codigo": "3499-040",
                "nombre": "ARILLOS",
                "marca": "GAMBER",
                "categoria": "AUDI A3 1.4 (1.3-17)...",
                "descripcion": "Anillos para pistón",
                "precio_compra": 420.00,
                "precio_venta": 620.00,
                "stock_minimo": 2
            },
            {
                "codigo": "14891",
                "nombre": "CADENA DE SILOCOADO",
                "marca": "HASTINGS",
                "categoria": "BUICK CENTURY 3.8...",
                "descripcion": "Cadena de distribución",
                "precio_compra": 285.00,
                "precio_venta": 425.00,
                "stock_minimo": 3
            },
            {
                "codigo": "V5-31457 LE",
                "nombre": "EMPAQUE MULTIPLE",
                "marca": "VS",
                "categoria": "ACURA CL 2.2, 2.3DN...",
                "descripcion": "Empaque múltiple",
                "precio_compra": 95.00,
                "precio_venta": 145.00,
                "stock_minimo": 8
            },
            {
                "codigo": "RE-213",
                "nombre": "BALAS DE TIERRO",
                "marca": "VSPPARTS",
                "categoria": "BUICK ENCORE 1.4 (1.3...",
                "descripcion": "Baleros de dirección",
                "precio_compra": 165.00,
                "precio_venta": 245.00,
                "stock_minimo": 6
            }
        ]

        print("=" * 60)
        print("AGREGANDO PRODUCTOS A LA BASE DE DATOS")
        print("=" * 60)
        
        productos_agregados = 0
        productos_existentes = 0
        
        for prod_data in productos:
            # Verificar si ya existe
            existe = db.query(Producto).filter(Producto.codigo == prod_data["codigo"]).first()
            
            if existe:
                print(f"⚠️  Ya existe: {prod_data['codigo']} - {prod_data['nombre']}")
                productos_existentes += 1
                continue
            
            # Crear el producto
            nuevo_producto = Producto(
                codigo=prod_data["codigo"],
                nombre=prod_data["nombre"],
                descripcion=prod_data.get("descripcion"),
                marca=prod_data.get("marca"),
                categoria=prod_data.get("categoria"),
                precio_compra=prod_data["precio_compra"],
                precio_venta=prod_data["precio_venta"],
                stock_total=0,  # Inicialmente sin stock
                stock_minimo=prod_data.get("stock_minimo", 5)
            )
            
            db.add(nuevo_producto)
            print(f"✅ Agregado: {prod_data['codigo']} - {prod_data['nombre']}")
            productos_agregados += 1
        
        # Confirmar cambios
        db.commit()
        
        print("=" * 60)
        print(f"✅ Productos agregados: {productos_agregados}")
        print(f"⚠️  Productos que ya existían: {productos_existentes}")
        print(f"📊 Total procesados: {len(productos)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🚀 Iniciando carga de productos...\n")
    agregar_productos()
    print("\n✅ Proceso completado!\n")
