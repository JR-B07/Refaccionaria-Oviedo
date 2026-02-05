"""
Script para cargar paquetes/kits de productos
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.paquete import Paquete

def cargar_paquetes():
    db = SessionLocal()
    try:
        paquetes_data = [
            {
                "nombre": "Kit Suspensión Delantera",
                "clase": "Suspensión",
                "descripcion": "Kit completo de suspensión delantera con amortiguadores y resortes"
            },
            {
                "nombre": "Kit Frenos Completo",
                "clase": "Frenos",
                "descripcion": "Sistema de frenos completo con pastillas, discos y mangueras"
            },
            {
                "nombre": "Kit Distribución",
                "clase": "Motor",
                "descripcion": "Kit completo de distribución con bandas, tensores y poleas"
            },
            {
                "nombre": "Kit Embrague",
                "clase": "Transmisión",
                "descripcion": "Kit de embrague con disco, presión y rodamiento"
            },
            {
                "nombre": "Kit Filtración",
                "clase": "Motor",
                "descripcion": "Kit de filtros: aire, aceite, combustible y cabina"
            },
            {
                "nombre": "Kit Iluminación LED",
                "clase": "Sistemas Eléctricos",
                "descripcion": "Kit de luces LED delantera y trasera"
            },
            {
                "nombre": "Kit Correas Serpentinas",
                "clase": "Motor",
                "descripcion": "Kit completo de correas de transmisión"
            },
            {
                "nombre": "Kit Inyectores Gasolina",
                "clase": "Combustible",
                "descripcion": "Kit de inyectores limpios y verificados"
            },
            {
                "nombre": "Kit Sensores Motor",
                "clase": "Sensores",
                "descripcion": "Kit completo de sensores del motor"
            },
            {
                "nombre": "Kit Aditivos Mantenimiento",
                "clase": "Lubricantes",
                "descripcion": "Kit de aditivos para motor, transmisión e inyectores"
            },
            {
                "nombre": "Kit Reparación Radiador",
                "clase": "Refrigeración",
                "descripcion": "Kit con termostato, mangueras y aditivos"
            },
            {
                "nombre": "Kit Sistema de Dirección",
                "clase": "Dirección",
                "descripcion": "Kit con rótulas, terminales y cruceta"
            },
            {
                "nombre": "Kit Frenos ABS",
                "clase": "Frenos",
                "descripcion": "Kit de frenos ABS con sensores incluidos"
            },
            {
                "nombre": "Kit Amortiguadores Traseros",
                "clase": "Suspensión",
                "descripcion": "Pareja de amortiguadores traseros"
            },
            {
                "nombre": "Kit Escape Completo",
                "clase": "Escape",
                "descripcion": "Kit completo de escape: catalizador, silenciador y tubería"
            }
        ]

        print("=" * 60)
        print("CARGANDO PAQUETES (KITS)")
        print("=" * 60)
        
        agregados = 0
        
        for paq_data in paquetes_data:
            # Verificar si ya existe
            existe = db.query(Paquete).filter(Paquete.nombre == paq_data["nombre"]).first()
            
            if existe:
                print(f"⚠️  Ya existe: {paq_data['nombre']}")
                continue
            
            # Crear el paquete
            nuevo_paquete = Paquete(
                nombre=paq_data["nombre"],
                clase=paq_data["clase"],
                descripcion=paq_data.get("descripcion"),
                activo=True
            )
            
            db.add(nuevo_paquete)
            print(f"✅ Agregado: {paq_data['nombre']}")
            agregados += 1
        
        # Confirmar cambios
        db.commit()
        
        print("=" * 60)
        print(f"✅ Paquetes agregados: {agregados}")
        print(f"📊 Total procesados: {len(paquetes_data)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🚀 Iniciando carga de paquetes/kits...\n")
    cargar_paquetes()
    print("\n✅ Proceso completado!\n")
