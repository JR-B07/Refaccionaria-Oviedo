# start.py
import sys
import os

# Añadir directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    import uvicorn
    
    print("=" * 60)
    print("🚀 SISTEMA DE REFACCIONARIA ERP")
    print("=" * 60)
    print("📊 Versión: 1.0.0")
    print("🌐 URL: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("🔐 Login: http://127.0.0.1:8000/login")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n📋 Verificando estructura...")
    
    # Verificar estructura de directorios
    required = [
        "app/__init__.py",
        "app/main.py",
        "app/api/__init__.py",
        "app/api/v1/__init__.py",
        "app/api/v1/api.py",
        "app/api/v1/endpoints/__init__.py",
        "app/api/v1/endpoints/auth.py"
    ]
    
    for file in required:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NO EXISTE")
    
    input("\nPresiona Enter para salir...")