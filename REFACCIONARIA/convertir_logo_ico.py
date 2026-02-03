"""
Convierte el logo PNG a formato ICO para usar en accesos directos de Windows
Preserva las proporciones de la imagen sin distorsión
"""

from PIL import Image
from pathlib import Path

def convertir_png_a_ico():
    """Convierte logo-refaccionaria.png a logo-refaccionaria.ico preservando proporciones"""
    
    png_path = Path("app/static/images/logo-refaccionaria.png")
    ico_path = Path("logo-refaccionaria.ico")
    
    try:
        # Abrir imagen PNG
        img = Image.open(png_path)
        print(f"📊 Imagen original: {img.size} píxeles ({img.mode})")
        
        # Convertir a RGBA si no lo está
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Crear múltiples tamaños para el ICO (estándar de Windows)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Procesar cada tamaño manteniendo proporción
        icons = []
        for size in icon_sizes:
            # Crear imagen cuadrada con fondo transparente
            square = Image.new('RGBA', size, (255, 255, 255, 0))
            
            # Redimensionar la imagen manteniendo proporción
            img_resized = img.copy()
            img_resized.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Calcular posición central para pegar la imagen
            x = (size[0] - img_resized.width) // 2
            y = (size[1] - img_resized.height) // 2
            
            # Pegar la imagen redimensionada en el centro
            square.paste(img_resized, (x, y), img_resized)
            
            icons.append(square)
        
        # Guardar como ICO
        icons[0].save(ico_path, format='ICO', sizes=icon_sizes, append_images=icons[1:])
        
        print("\n✅ Logo convertido exitosamente")
        print(f"📁 Archivo creado: {ico_path.absolute()}")
        print(f"📏 Tamaños incluidos: {', '.join([f'{w}x{h}' for w, h in icon_sizes])}")
        print("🎨 Proporciones: Preservadas (sin distorsión)")
        
        return True
        
    except ImportError:
        print("❌ Error: Se requiere Pillow")
        print("Instala con: pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ Error al convertir: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🖼️  CONVERTIR LOGO A FORMATO ICO")
    print("=" * 70)
    print()
    
    if convertir_png_a_ico():
        print()
        print("=" * 70)
        print("📋 INSTRUCCIONES PARA CREAR ACCESO DIRECTO:")
        print("=" * 70)
        print()
        print("1. Click derecho en Refaccionaria.bat")
        print("2. Seleccionar 'Crear acceso directo'")
        print("3. Click derecho en el acceso directo → 'Propiedades'")
        print("4. Click en 'Cambiar icono...'")
        print("5. Click en 'Examinar...'")
        print("6. Seleccionar: logo-refaccionaria.ico")
        print("7. Click en 'Aceptar' → 'Aceptar'")
        print("8. Arrastra el acceso directo al Escritorio")
        print()
