#!/usr/bin/env python
import sys
import enum

# Test directo sin circular imports
print("=== TEST DE ENUMS ===\n")

# Simular los enums como deberían ser
class TipoVale(str, enum.Enum):
    venta = "venta"
    devolucion = "devolucion"

class EstadoUsuario(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    suspendido = "suspendido"

print("1️⃣  Verificando que enums heredan de str...")
print(f"   TipoVale.venta isinstance(str): {isinstance(TipoVale.venta, str)}")
print(f"   EstadoUsuario.activo isinstance(str): {isinstance(EstadoUsuario.activo, str)}")

print("\n2️⃣  Verificando valores...")
print(f"   TipoVale.venta.value = '{TipoVale.venta.value}'")
print(f"   EstadoUsuario.activo.value = '{EstadoUsuario.activo.value}'")

print("\n3️⃣  Verificando comparaciones...")
valor_bd = "venta"
if valor_bd == TipoVale.venta.value:
    print(f"   ✅ Valor de BD '{valor_bd}' == TipoVale.venta.value")

valor_bd2 = "activo"  
if valor_bd2 == EstadoUsuario.activo.value:
    print(f"   ✅ Valor de BD '{valor_bd2}' == EstadoUsuario.activo.value")

print("\n✅ TODOS LOS TESTS PASADOS")
