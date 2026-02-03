"""
Launcher mejorado con icono y configuración avanzada
Cierra la ventana de terminal de Python una vez que la interfaz se abre
"""

import webview
import threading
import uvicorn
import sys
import os
from pathlib import Path
import time
import requests
import webbrowser
import subprocess
from io import BytesIO

# Configuración
HOST = "127.0.0.1"
PORT = 8000
SERVER_URL = f"http://{HOST}:{PORT}"
APP_URL = f"{SERVER_URL}/static/login.html"

# Rutas
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "app" / "static" / "images" / "logo-refaccionaria.png"

class API:
    """API para comunicación entre la ventana y el backend"""
    
    def open_external(self, url):
        """Abre URL en navegador externo"""
        webbrowser.open(url)
    
    def get_version(self):
        """Obtiene la versión del sistema"""
        return "1.0.0"

class RefaccionariaDesktop:
    def __init__(self):
        self.server_thread = None
        self.server_running = False
        self.window = None
        self.api = API()
    
    def start_server(self):
        """Inicia el servidor FastAPI"""
        try:
            # Cambiar al directorio correcto
            os.chdir(BASE_DIR)
            
            # Suprimir mensajes de salida
            import subprocess
            import sys
            
            # Configurar uvicorn con log_level más silencioso
            config = uvicorn.Config(
                "app.main:app",
                host=HOST,
                port=PORT,
                log_level="critical",
                access_log=False,
                reload=False,
                use_colors=False
            )
            server = uvicorn.Server(config)
            server.run()
        except Exception as e:
            # Silenciosamente continuar si hay errores
            pass
    
    def check_server(self, timeout=30):
        """Verifica que el servidor esté activo"""
        start = time.time()
        
        while time.time() - start < timeout:
            try:
                response = requests.get(f"{SERVER_URL}/docs", timeout=1)
                if response.status_code == 200:
                    self.server_running = True
                    return True
            except:
                time.sleep(0.3)
        
        return False
    
    def on_loaded(self):
        """Callback cuando la ventana carga completamente"""
        # Cerrar la ventana de consola de Python
        self.hide_console()
    
    def hide_console(self):
        """Oculta/minimiza la ventana de consola de Python"""
        try:
            # En Windows, usa Windows API para minimizar la ventana de consola
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                # SW_MINIMIZE = 6
                ctypes.windll.user32.ShowWindow(hwnd, 6)
        except:
            pass
    
    def on_closing(self):
        """Callback cuando se cierra la ventana"""
        self.server_running = False
        try:
            # Intentar cerrar limpiamente
            requests.post(f"{SERVER_URL}/shutdown", timeout=1)
        except:
            pass
        os._exit(0)
    
    def run(self):
        """Ejecuta la aplicación"""
        # Iniciar servidor en background silenciosamente
        self.server_thread = threading.Thread(
            target=self.start_server,
            daemon=True,
            name="FastAPI-Server"
        )
        self.server_thread.start()
        
        # Esperar a que el servidor esté listo
        if not self.check_server():
            sys.exit(1)
        
        # Configurar ventana
        try:
            # Crear ventana principal
            self.window = webview.create_window(
                title="Refaccionaria Oviedo - Sistema ERP v1.0",
                url=APP_URL,
                width=1440,
                height=900,
                resizable=True,
                fullscreen=False,
                min_size=(1024, 768),
                background_color="#FFFFFF",
                text_select=True,
                confirm_close=False,
                js_api=self.api
            )
            
            # Eventos
            self.window.events.loaded += self.on_loaded
            self.window.events.closing += self.on_closing
            
            # Iniciar ventana
            webview.start(
                debug=False,
                http_server=False,
                private_mode=False
            )
            
        except Exception as e:
            sys.exit(1)

def main():
    """Punto de entrada"""
    try:
        # Verificar que estemos en el directorio correcto
        if not Path("app").exists():
            sys.exit(1)
        
        # Iniciar aplicación sin mostrar mensajes
        app = RefaccionariaDesktop()
        app.run()
        
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
