#!/usr/bin/env python3
"""
Script de prueba para el nuevo sistema de generación de tickets
con promociones y políticas de devolución

Uso:
    python test_ticket_nuevo_diseño.py
"""

import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.ticket_printer import TicketPrinter
from datetime import datetime

def demo_ticket_simple():
    """Demuestra la generación de un ticket simple"""
    print("=" * 80)
    print("DEMO 1: Ticket Simple")
    print("=" * 80)
    print()
    
    articulos = [
        {"nombre": "Kit de frenos cerámicos", "cantidad": 1, "precio": 850.00},
        {"nombre": "Aceite sintético 5W-30", "cantidad": 2, "precio": 320.00},
        {"nombre": "Filtro de aire", "cantidad": 1, "precio": 180.00}
    ]
    
    ticket = TicketPrinter.generate_ticket(
        folio="VZ7314",
        cliente="Refaccionaria Norte",
        articulos=articulos,
        subtotal=1870.00,
        descuento=100.00,
        impuesto=276.40,
        total=2046.40,
        vendedor="Carlos Mendoza",
        incluir_qr=False
    )
    
    print(ticket)
    print()

def demo_venta_rapida():
    """Demuestra un ticket de venta rápida (punto de venta)"""
    print("=" * 80)
    print("DEMO 2: Venta Rápida - Punto de Venta")
    print("=" * 80)
    print()
    
    items = [
        {"descripcion": "Bujías Iridio", "cantidad": 4, "precio": 120.00},
        {"descripcion": "Aditivo Combustible", "cantidad": 1, "precio": 250.00},
        {"descripcion": "Limpiador de Inyectores", "cantidad": 2, "precio": 180.00}
    ]
    
    ticket = TicketPrinter.generate_venta_rapida_ticket(
        folio="VZ7315",
        items=items,
        subtotal=1430.00,
        descuento=143.00,
        total=1287.00,
        efectivo=1300.00,
        cambio=13.00,
        vendedor="María González"
    )
    
    print(ticket)
    print()

def demo_solo_promociones():
    """Demuestra la sección de promociones"""
    print("=" * 80)
    print("DEMO 3: Solo Sección de Promociones")
    print("=" * 80)
    print()
    
    promociones = TicketPrinter.generate_promociones()
    print(promociones)
    print()

def demo_solo_politicas():
    """Demuestra la sección de políticas"""
    print("=" * 80)
    print("DEMO 4: Solo Sección de Políticas de Devolución")
    print("=" * 80)
    print()
    
    politicas = TicketPrinter.generate_politicas()
    print(politicas)
    print()

def demo_encabezado():
    """Demuestra el encabezado"""
    print("=" * 80)
    print("DEMO 5: Encabezado")
    print("=" * 80)
    print()
    
    encabezado = TicketPrinter.generate_header()
    print(encabezado)
    print()

def test_width():
    """Prueba el ancho del ticket"""
    print("=" * 80)
    print("DEMO 6: Prueba de Ancho (debe tener 40 caracteres)")
    print("=" * 80)
    print()
    
    line = TicketPrinter.line_separator()
    print(f"Línea: |{line}|")
    print(f"Longitud: {len(line)} caracteres")
    print()
    
    centered = TicketPrinter.center_text("REFACCIONARIA OVIEDO")
    print(f"Texto centrado: |{centered}|")
    print(f"Longitud: {len(centered)} caracteres")
    print()

def guardar_ejemplo_en_archivo():
    """Guarda un ejemplo de ticket en un archivo"""
    print("=" * 80)
    print("DEMO 7: Guardando ejemplo en archivo")
    print("=" * 80)
    print()
    
    items = [
        {"descripcion": "Producto A", "cantidad": 2, "precio": 500.00},
        {"descripcion": "Producto B", "cantidad": 1, "precio": 300.00},
    ]
    
    ticket = TicketPrinter.generate_venta_rapida_ticket(
        folio="VZ0001",
        items=items,
        subtotal=1300.00,
        descuento=50.00,
        total=1250.00,
        vendedor="Test Vendedor"
    )
    
    # Guardar en archivo
    archivo = Path(__file__).parent / "ticket_ejemplo.txt"
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(ticket)
    
    print(f"✓ Ticket guardado en: {archivo}")
    print()

def main():
    """Ejecuta todas las demostraciones"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  SISTEMA DE GENERACIÓN DE TICKETS - REFACCIONARIA OVIEDO  ".center(78) + "║")
    print("║" + "  Nuevas Características: Promociones y Políticas de Devolución  ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    try:
        demo_ticket_simple()
        input("Presiona ENTER para continuar con la demo 2...")
        demo_venta_rapida()
        input("Presiona ENTER para continuar con la demo 3...")
        demo_solo_promociones()
        input("Presiona ENTER para continuar con la demo 4...")
        demo_solo_politicas()
        input("Presiona ENTER para continuar con la demo 5...")
        demo_encabezado()
        input("Presiona ENTER para continuar con la demo 6...")
        test_width()
        input("Presiona ENTER para continuar con la demo 7...")
        guardar_ejemplo_en_archivo()
        
        print("\n" + "=" * 80)
        print("✓ Todas las demostraciones completadas exitosamente")
        print("=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Demostración cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
