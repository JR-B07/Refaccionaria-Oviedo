#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificación - Correcciones del Sistema de Refaccionaria
Verifica que todas las correcciones hayan sido aplicadas correctamente
"""

import os
import sys
from pathlib import Path

def verificar_archivo_existe(ruta):
    """Verifica que un archivo existe"""
    existe = os.path.exists(ruta)
    estado = "✅" if existe else "❌"
    print(f"{estado} {ruta}: {'Existe' if existe else 'NO existe'}")
    return existe

def verificar_contenido(ruta, buscar_texto):
    """Verifica que un archivo contiene cierto texto"""
    if not os.path.exists(ruta):
        print(f"❌ Archivo no existe: {ruta}")
        return False
    
    with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
        contenido = f.read()
        encontrado = buscar_texto in contenido
        
    estado = "✅" if encontrado else "❌"
    print(f"{estado} {ruta}: {'Contiene' if encontrado else 'NO contiene'} '{buscar_texto[:50]}...'")
    return encontrado

def main():
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE CORRECCIONES APLICADAS")
    print("   Refaccionaria Oviedo - 6 de febrero de 2026")
    print("=" * 70)
    print()
    
    ruta_base = Path(__file__).parent
    
    # 1. Verificar favicon.ico
    print("📋 1. FAVICON.ICO")
    print("-" * 70)
    verificar_archivo_existe(ruta_base / "app" / "static" / "favicon.ico")
    print()
    
    # 2. Verificar correcciones en usuarios.py
    print("📋 2. USUARIOS.PY - Importaciones duplicadas")
    print("-" * 70)
    usuarios_py = ruta_base / "app" / "api" / "v1" / "endpoints" / "usuarios.py"
    
    with open(usuarios_py, 'r', encoding='utf-8') as f:
        contenido = f.read()
        lineas_from_fastapi = contenido.count("from fastapi import")
        lineas_router = contenido.count("router = APIRouter()")
    
    estado_imports = "✅" if lineas_from_fastapi == 1 else "❌"
    estado_router = "✅" if lineas_router == 1 else "❌"
    
    print(f"{estado_imports} ImportError 'from fastapi': {lineas_from_fastapi} (debe ser 1)")
    print(f"{estado_router} 'router = APIRouter()': {lineas_router} (debe ser 1)")
    print()
    
    # 3. Verificar correcciones en vales_venta.html
    print("📋 3. VALES_VENTA.HTML - URLs corregidas")
    print("-" * 70)
    vales_html = ruta_base / "app" / "static" / "vales_venta.html"
    verificar_contenido(vales_html, "new URL('/api/v1/usuarios/'")
    verificar_contenido(vales_html, "url.searchParams.append('skip'")
    verificar_contenido(vales_html, "new URL('/api/v1/vales-venta'")
    print()
    
    # 4. Verificar correcciones en cajas_cierre.html
    print("📋 4. CAJAS_CIERRE.HTML - URLs corregidas")
    print("-" * 70)
    cajas_html = ruta_base / "app" / "static" / "cajas_cierre.html"
    verificar_contenido(cajas_html, "new URL('/api/v1/reportes/cierres-caja/estadisticas'")
    verificar_contenido(cajas_html, "new URL('/api/v1/reportes/cierres-caja'")
    print()
    
    # 5. Verificar correcciones en devolucionesdetalladas.html
    print("📋 5. DEVOLUCIONESDETALLADAS.HTML - URLs corregidas")
    print("-" * 70)
    devoluciones_html = ruta_base / "app" / "static" / "devolucionesdetalladas.html"
    verificar_contenido(devoluciones_html, "new URL('/api/v1/reportes/devoluciones-detalladas'")
    print()
    
    # 6. Verificar correcciones en arqueos_caja.html
    print("📋 6. ARQUEOS_CAJA.HTML - URLs corregidas")
    print("-" * 70)
    arqueos_html = ruta_base / "app" / "static" / "arqueos_caja.html"
    
    # Verificar que NO tenga espacios raros
    with open(arqueos_html, 'r', encoding='utf-8') as f:
        contenido = f.read()
        tiene_espacios_raros = " /arqueos/caja / " in contenido
        
    estado_espacios = "❌" if tiene_espacios_raros else "✅"
    print(f"{estado_espacios} Sin espacios anómalos en URL: {'Tiene' if tiene_espacios_raros else 'Correcto'}")
    
    verificar_contenido(arqueos_html, '${API_BASE}/arqueos/caja/${id}')
    print()
    
    # 7. Resumen final
    print("=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("📝 ACCIONES SIGUIENTES:")
    print()
    print("1. Reiniciar el servidor:")
    print("   python run.py")
    print()
    print("2. Abrir el navegador:")
    print("   http://localhost:8000")
    print()
    print("3. Revisar la consola (F12):")
    print("   - No debe haber errores 500")
    print("   - No debe haber error 404 de favicon.ico")
    print()
    print("4. Probar funcionalidades:")
    print("   - Cargar lista de vendedores")
    print("   - Cargar vales de venta")
    print("   - Generar reportes de cierres")
    print()

if __name__ == "__main__":
    main()
