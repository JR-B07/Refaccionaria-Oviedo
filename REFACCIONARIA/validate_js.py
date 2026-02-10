#!/usr/bin/env python3
"""
Valida que el archivo HTML no tenga errores de sintaxis básicos en JavaScript
"""
import re

filepath = "c:\\Users\\india\\Documents\\GitHub\\Refaccionaria-Oviedo\\REFACCIONARIA\\app\\static\\productos.html"

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar que no haya try sin catch
    try_blocks = re.findall(r'\btry\s*{', content)
    catch_blocks = re.findall(r'\}\s*catch\s*', content)
    
    print("=" * 60)
    print("VALIDACIÓN DE SINTAXIS JAVASCRIPT")
    print("=" * 60)
    print(f"Try blocks encontrados: {len(try_blocks)}")
    print(f"Catch blocks encontrados: {len(catch_blocks)}")
    
    # Verificar funciones definidas
    functions = re.findall(r'(?:async\s+)?function\s+(\w+)\s*\(', content)
    print(f"\n✓ Funciones definidas ({len(functions)}):")
    for func in sorted(set(functions)):
        print(f"  - {func}")
    
    # Verificar llamadas a funciones
    function_calls = re.findall(r'\b(\w+)\s*\(', content)
    called_functions = set([f for f in function_calls if f not in ['if', 'for', 'while', 'switch', 'catch', 'function', 'async']])
    
    # Funciones llamadas pero no definidas
    undefined_funcs = called_functions - set(functions)
    
    if undefined_funcs:
        print(f"\n⚠️  Funciones llamadas pero NO definidas ({len(undefined_funcs)}):")
        for func in sorted(undefined_funcs):
            if func and len(func) > 2:  # Filtrar funciones muy cortas
                print(f"  - {func}")
    else:
        print("\n✓ Todas las funciones llamadas están definidas")
    
    # Palabras clave que deberían existir
    required = ['switchTab', 'loadGrupos', 'grupoCargar', 'grupoSeleccionarPorSelect']
    print(f"\n✓ Verificando funciones requeridas:")
    for func in required:
        if f'function {func}' in content or f'async function {func}' in content:
            print(f"  ✓ {func} - Definida")
        else:
            print(f"  ❌ {func} - NO encontrada")
    
except Exception as e:
    print(f"Error: {e}")
