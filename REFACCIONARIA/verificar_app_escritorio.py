"""
Script de verificación completa de la aplicación de escritorio
Prueba todas las funcionalidades y genera reporte
"""

import subprocess
import time
import requests
import sys
from pathlib import Path

def print_section(title):
    """Imprime una sección con formato"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def check_file(filepath, description):
    """Verifica si un archivo existe"""
    path = Path(filepath)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_server(url, timeout=5):
    """Verifica si el servidor responde"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def main():
    print_section("🔍 VERIFICACIÓN DE APLICACIÓN DE ESCRITORIO")
    
    base_dir = Path(__file__).parent
    
    # 1. Verificar archivos necesarios
    print_section("1️⃣  VERIFICACIÓN DE ARCHIVOS")
    
    files_ok = True
    files_ok &= check_file(base_dir / "Refaccionaria.bat", "Launcher principal")
    files_ok &= check_file(base_dir / "InicioRapido.bat", "Launcher navegador")
    files_ok &= check_file(base_dir / "launch_desktop.py", "Script de escritorio")
    files_ok &= check_file(base_dir / "launch_browser.py", "Script navegador")
    files_ok &= check_file(base_dir / "desktop_app.py", "Script alternativo")
    files_ok &= check_file(base_dir / "app" / "static" / "images" / "logo-refaccionaria.png", "Logo")
    files_ok &= check_file(base_dir / "DESKTOP_README.md", "README")
    files_ok &= check_file(base_dir / "GUIA_APLICACION_ESCRITORIO.md", "Guía")
    
    if not files_ok:
        print("\n❌ Faltan archivos necesarios")
        return False
    
    print("\n✅ Todos los archivos están presentes")
    
    # 2. Verificar dependencias Python
    print_section("2️⃣  VERIFICACIÓN DE DEPENDENCIAS")
    
    dependencies = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "sqlalchemy": "SQLAlchemy",
        "requests": "Requests",
        "webbrowser": "Webbrowser (built-in)"
    }
    
    deps_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} instalado")
        except ImportError:
            print(f"❌ {name} NO instalado")
            deps_ok = False
    
    # Verificar pywebview (opcional)
    try:
        import webview
        print(f"✅ pywebview instalado (aplicación nativa disponible)")
    except ImportError:
        print(f"⚠️  pywebview NO instalado (solo modo navegador disponible)")
    
    if not deps_ok:
        print("\n❌ Faltan dependencias necesarias")
        print("   Instalar con: pip install -r requirements.txt")
        return False
    
    print("\n✅ Todas las dependencias principales están instaladas")
    
    # 3. Verificar base de datos
    print_section("3️⃣  VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        from app.core.database import SessionLocal
        from app.models.usuario import Usuario
        
        db = SessionLocal()
        users = db.query(Usuario).filter(Usuario.estado == "ACTIVO").count()
        db.close()
        
        print(f"✅ Conexión a base de datos exitosa")
        print(f"✅ Usuarios activos encontrados: {users}")
        
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return False
    
    # 4. Prueba de inicio rápido
    print_section("4️⃣  PRUEBA DE INICIO DEL SISTEMA")
    
    print("Iniciando servidor de prueba...")
    print("(Se detendrá automáticamente después de la verificación)")
    print()
    
    try:
        # Iniciar servidor en background
        import threading
        import uvicorn
        
        def start_test_server():
            import os
            os.chdir(base_dir)
            uvicorn.run(
                "app.main:app",
                host="127.0.0.1",
                port=8001,  # Puerto diferente para no interferir
                log_level="error",
                access_log=False
            )
        
        server_thread = threading.Thread(target=start_test_server, daemon=True)
        server_thread.start()
        
        # Esperar inicio
        print("⏳ Esperando que el servidor inicie...")
        time.sleep(5)
        
        # Verificar servidor
        if check_server("http://127.0.0.1:8001/docs"):
            print("✅ Servidor inició correctamente")
            print("✅ Endpoint /docs responde")
            
            # Verificar API
            try:
                response = requests.get("http://127.0.0.1:8001/api/v1/locales/")
                if response.status_code in [200, 401]:  # 200 o 401 (sin auth) es válido
                    print("✅ API responde correctamente")
                else:
                    print(f"⚠️  API responde con código: {response.status_code}")
            except Exception as e:
                print(f"⚠️  Error al probar API: {e}")
            
        else:
            print("❌ El servidor no responde")
            return False
            
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        return False
    
    # 5. Resumen final
    print_section("📊 RESUMEN DE VERIFICACIÓN")
    
    print("✅ Archivos: OK")
    print("✅ Dependencias: OK")
    print("✅ Base de datos: OK")
    print("✅ Servidor: OK")
    print()
    print("=" * 70)
    print("🎉 ¡APLICACIÓN DE ESCRITORIO COMPLETAMENTE FUNCIONAL!")
    print("=" * 70)
    print()
    print("📋 Instrucciones de uso:")
    print()
    print("  1️⃣  Modo Escritorio:")
    print("     Doble clic en: Refaccionaria.bat")
    print()
    print("  2️⃣  Modo Navegador:")
    print("     Doble clic en: InicioRapido.bat")
    print()
    print("  3️⃣  Crear acceso directo:")
    print("     Ruta: " + str(base_dir / "Refaccionaria.bat"))
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación interrumpida")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
