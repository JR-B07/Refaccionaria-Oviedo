# run.py (en la raíz)
import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("🚀 INICIANDO SISTEMA DE REFACCIONARIA")
    print("=" * 50)
    
    # Verificar estructura
    required_dirs = ["app", "app/core", "app/api/v1/endpoints"]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Falta directorio: {dir_path}")
            return
    
    # Comando para ejecutar
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--log-level", "debug"
    ]
    
    print(f"📂 Directorio: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print(f"🔧 Comando: {' '.join(cmd)}")
    print("=" * 50)
    print("✅ Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()