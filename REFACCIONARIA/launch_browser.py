"""
Lanzador Simple - Abre el sistema en el navegador predeterminado
Alternativa sin dependencias de pywebview
"""

import uvicorn
import webbrowser
import threading
import time
import sys
import os
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}/static/login.html"

def start_server():
    """Inicia el servidor FastAPI"""
    try:
        os.chdir(Path(__file__).parent)
        uvicorn.run(
            "app.main:app",
            host=HOST,
            port=PORT,
            log_level="warning",
            access_log=False
        )
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 70)
    print("🏪 REFACCIONARIA OVIEDO - SISTEMA ERP")
    print("=" * 70)
    print()
    print(f"🚀 Iniciando servidor en {URL}")
    print()
    
    # Iniciar servidor en background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Esperar a que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(3)
    
    # Abrir navegador
    print(f"🌐 Abriendo navegador en {URL}")
    print("📄 Página de login cargada")
    webbrowser.open(URL)
    
    print()
    print("=" * 70)
    print("✅ SISTEMA ACTIVO")
    print("=" * 70)
    print()
    print("📋 Información:")
    print(f"   • URL: {URL}")
    print(f"   • Docs: {URL}/docs")
    print()
    print("⚠️  Para detener el servidor presiona Ctrl+C")
    print()
    
    try:
        # Mantener el servidor corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        print("👋 Servidor detenido")
        sys.exit(0)

if __name__ == "__main__":
    main()
