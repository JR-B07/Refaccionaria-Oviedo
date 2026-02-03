"""
Aplicación de Escritorio - Sistema Refaccionaria Oviedo
Lanza el servidor FastAPI y abre una ventana de escritorio nativa
"""

import webview
import threading
import uvicorn
import sys
import os
from pathlib import Path
import time
import requests

# Configuración
HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}/static/login.html"

# Rutas
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "app" / "static" / "images" / "logo-refaccionaria.png"

class DesktopApp:
    def __init__(self):
        self.server_thread = None
        self.server_running = False
    
    def start_server(self):
        """Inicia el servidor FastAPI en un thread separado"""
        try:
            print("🚀 Iniciando servidor FastAPI...")
            uvicorn.run(
                "app.main:app",
                host=HOST,
                port=PORT,
                log_level="error",
                access_log=False
            )
        except Exception as e:
            print(f"❌ Error al iniciar servidor: {e}")
    
    def wait_for_server(self, timeout=30):
        """Espera a que el servidor esté listo"""
        print("⏳ Esperando que el servidor esté listo...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{URL}/docs", timeout=1)
                if response.status_code == 200:
                    print("✅ Servidor listo")
                    self.server_running = True
                    return True
            except:
                time.sleep(0.5)
        
        print("❌ Tiempo de espera agotado")
        return False
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        print("👋 Cerrando aplicación...")
        self.server_running = False
        os._exit(0)
    
    def run(self):
        """Ejecuta la aplicación de escritorio"""
        # Iniciar servidor en thread separado
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()
        
        # Esperar a que el servidor esté listo
        if not self.wait_for_server():
            print("❌ No se pudo iniciar el servidor")
            sys.exit(1)
        
        # Configurar y crear ventana
        print("🖥️  Abriendo ventana de escritorio...")
        
        # Verificar si existe el logo
        icon_path = str(LOGO_PATH) if LOGO_PATH.exists() else None
        
        # Crear ventana de escritorio
        window = webview.create_window(
            title="Refaccionaria Oviedo - Sistema ERP",
            url=URL,
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            min_size=(1024, 768),
            background_color="#FFFFFF",
            text_select=True
        )
        
        # Iniciar la aplicación
        webview.start(debug=False)
        
        # Cleanup al cerrar
        self.on_closing()

def main():
    """Punto de entrada principal"""
    print("=" * 70)
    print("🏪 REFACCIONARIA OVIEDO - SISTEMA ERP")
    print("=" * 70)
    print()
    
    try:
        app = DesktopApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
