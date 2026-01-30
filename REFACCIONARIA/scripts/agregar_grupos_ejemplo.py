"""
Script para agregar 2 grupos de ejemplo con productos existentes
"""
import sys
sys.path.insert(0, '/Users/india/Desktop/REFACCIONARIA')

from app.core.database import SessionLocal
from app.models.producto import Producto
from app.models.grupo import Grupo, GrupoProducto, GrupoAplicacion
from sqlalchemy import func

session = SessionLocal()

try:
    # 1. Obtener productos existentes
    total_productos = session.query(func.count(Producto.id)).scalar()
    print(f"✓ Total de productos en BD: {total_productos}")
    
    productos = session.query(Producto).limit(20).all()
    print(f"✓ Primeros 20 productos:")
    for i, p in enumerate(productos[:20]):
        print(f"  {i+1}. ID: {p.id:3} | Código: {p.codigo:12} | Nombre: {p.nombre[:40]:40} | Marca: {p.marca}")
    
    if len(productos) < 4:
        print("❌ No hay suficientes productos (se necesitan al menos 4)")
        sys.exit(1)
    
    # 2. Crear primer grupo: "Kits Suspensión"
    print("\n📦 Creando Grupo 1: 'Kits Suspensión'...")
    grupo1 = Grupo(
        nombre="Kits Suspensión",
        tipo="Compatibilidad",
        descripcion="Kits completos de suspensión delantera y trasera",
        activo=True
    )
    session.add(grupo1)
    session.flush()  # Para obtener el ID
    print(f"  ✓ Grupo creado con ID: {grupo1.id}")
    
    # Agregar 4 productos al grupo 1
    productos_seleccionados_g1 = productos[:4]
    for idx, p in enumerate(productos_seleccionados_g1):
        gp = GrupoProducto(
            grupo_id=grupo1.id,
            producto_id=p.id,
            linea=f"SUS-{idx+1:03d}-A",
            caracteristica1="Suspensión trasera",
            caracteristica2="Amortiguador reforzado",
            clave=f"SUSP-{idx+1}"
        )
        session.add(gp)
        print(f"  ✓ Agregado: {p.nombre} (linea: {gp.linea})")
    
    # Agregar 2 aplicaciones al grupo 1
    apps1 = [
        {"marca": "Nissan", "modelo": "Tsuru", "motor": "GA16DE", "desde": 1991, "hasta": 2017},
        {"marca": "Nissan", "modelo": "Sentra", "motor": "QG18DE", "desde": 2006, "hasta": 2012}
    ]
    for app in apps1:
        ga = GrupoAplicacion(
            grupo_id=grupo1.id,
            marca=app["marca"],
            modelo=app["modelo"],
            motor=app["motor"],
            desde=app["desde"],
            hasta=app["hasta"]
        )
        session.add(ga)
        print(f"  ✓ Aplicación: {app['marca']} {app['modelo']} ({app['motor']}) {app['desde']}-{app['hasta']}")
    
    # 3. Crear segundo grupo: "Sistemas de Frenos"
    print("\n📦 Creando Grupo 2: 'Sistemas de Frenos'...")
    grupo2 = Grupo(
        nombre="Sistemas de Frenos",
        tipo="Componentes",
        descripcion="Pastillas, discos y componentes de frenos",
        activo=True
    )
    session.add(grupo2)
    session.flush()
    print(f"  ✓ Grupo creado con ID: {grupo2.id}")
    
    # Agregar 4 productos al grupo 2
    productos_seleccionados_g2 = productos[4:8] if len(productos) >= 8 else productos[4:]
    for idx, p in enumerate(productos_seleccionados_g2):
        gp = GrupoProducto(
            grupo_id=grupo2.id,
            producto_id=p.id,
            linea=f"FREN-{idx+1:03d}-B",
            caracteristica1="Sistema ABS compatible",
            caracteristica2="Bajo ruido",
            clave=f"FRENO-{idx+1}"
        )
        session.add(gp)
        print(f"  ✓ Agregado: {p.nombre} (linea: {gp.linea})")
    
    # Agregar 2 aplicaciones al grupo 2
    apps2 = [
        {"marca": "Honda", "modelo": "Civic", "motor": "K20Z3", "desde": 2006, "hasta": 2011},
        {"marca": "Mazda", "modelo": "3", "motor": "L3VE", "desde": 2004, "hasta": 2009}
    ]
    for app in apps2:
        ga = GrupoAplicacion(
            grupo_id=grupo2.id,
            marca=app["marca"],
            modelo=app["modelo"],
            motor=app["motor"],
            desde=app["desde"],
            hasta=app["hasta"]
        )
        session.add(ga)
        print(f"  ✓ Aplicación: {app['marca']} {app['modelo']} ({app['motor']}) {app['desde']}-{app['hasta']}")
    
    # Commit
    session.commit()
    print("\n✅ ¡Grupos de ejemplo creados exitosamente!")
    
    # Verificación
    print("\n📊 Verificación:")
    g1 = session.query(Grupo).filter_by(nombre="Kits Suspensión").first()
    g2 = session.query(Grupo).filter_by(nombre="Sistemas de Frenos").first()
    
    print(f"\nGrupo 1: {g1.nombre}")
    print(f"  Productos: {len(g1.productos_rel)}")
    print(f"  Aplicaciones: {len(g1.aplicaciones)}")
    
    print(f"\nGrupo 2: {g2.nombre}")
    print(f"  Productos: {len(g2.productos_rel)}")
    print(f"  Aplicaciones: {len(g2.aplicaciones)}")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    session.close()
