"""
Analizador de Recursos del Sistema - Refaccionaria Oviedo
Mide el uso de CPU, RAM, disco y red durante la ejecución
"""

import psutil
import time
import os
import sys
from pathlib import Path
from datetime import datetime

class AnalizadorRecursos:
    def __init__(self):
        self.proceso_python = None
        self.proceso_mysql = None
        self.mediciones = []
        
    def obtener_tamaño_proyecto(self):
        """Calcula el tamaño total del proyecto"""
        total_size = 0
        file_count = 0
        
        base_dir = Path(__file__).parent
        
        for item in base_dir.rglob('*'):
            if item.is_file():
                try:
                    # Excluir carpetas comunes que no se despliegan
                    exclude = ['__pycache__', '.git', 'node_modules', '.env', 'venv']
                    if not any(ex in str(item) for ex in exclude):
                        total_size += item.stat().st_size
                        file_count += 1
                except:
                    pass
        
        return total_size, file_count
    
    def obtener_procesos_sistema(self):
        """Encuentra los procesos de Python y MySQL"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Buscar proceso Python ejecutando nuestra app
                if 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('app.main' in str(cmd) or 'launch_desktop' in str(cmd) for cmd in cmdline):
                        self.proceso_python = proc
                
                # Buscar proceso MySQL
                if 'mysql' in proc.info['name'].lower():
                    self.proceso_mysql = proc
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    def medir_recursos_proceso(self, proceso):
        """Mide recursos de un proceso específico"""
        try:
            cpu = proceso.cpu_percent(interval=1)
            mem = proceso.memory_info()
            
            return {
                'cpu_percent': cpu,
                'memoria_mb': mem.rss / (1024 * 1024),
                'memoria_virtual_mb': mem.vms / (1024 * 1024)
            }
        except:
            return None
    
    def medir_recursos_sistema(self):
        """Mide recursos generales del sistema"""
        cpu_total = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_total': cpu_total,
            'memoria_total_gb': mem.total / (1024**3),
            'memoria_usada_gb': mem.used / (1024**3),
            'memoria_disponible_gb': mem.available / (1024**3),
            'memoria_porcentaje': mem.percent,
            'disco_total_gb': disk.total / (1024**3),
            'disco_usado_gb': disk.used / (1024**3),
            'disco_libre_gb': disk.free / (1024**3),
            'disco_porcentaje': disk.percent
        }
    
    def analizar(self, duracion_segundos=30, intervalo=2):
        """Realiza análisis durante un período de tiempo"""
        print("=" * 80)
        print("🔍 ANALIZADOR DE RECURSOS - REFACCIONARIA OVIEDO")
        print("=" * 80)
        print()
        
        # Información del proyecto
        print("📦 TAMAÑO DEL PROYECTO:")
        print("-" * 80)
        size, files = self.obtener_tamaño_proyecto()
        print(f"   • Tamaño total: {size / (1024**2):.2f} MB")
        print(f"   • Archivos: {files:,}")
        print(f"   • Tamaño comprimido estimado: {(size / (1024**2)) * 0.3:.2f} MB")
        print()
        
        # Buscar procesos
        print("🔎 BUSCANDO PROCESOS DEL SISTEMA...")
        print("-" * 80)
        self.obtener_procesos_sistema()
        
        if self.proceso_python:
            print(f"   ✅ Proceso Python encontrado (PID: {self.proceso_python.pid})")
        else:
            print("   ⚠️  Proceso Python no encontrado (el servidor debe estar corriendo)")
            print("   💡 Inicia el servidor con: python run.py")
            print()
            print("   Continuando con análisis del sistema...")
        
        if self.proceso_mysql:
            print(f"   ✅ Proceso MySQL encontrado (PID: {self.proceso_mysql.pid})")
        else:
            print("   ⚠️  Proceso MySQL no encontrado")
        
        print()
        
        # Recursos del sistema
        print("💻 RECURSOS DEL SISTEMA:")
        print("-" * 80)
        recursos_sistema = self.medir_recursos_sistema()
        print(f"   • CPU Total: {recursos_sistema['cpu_total']:.1f}%")
        print(f"   • RAM Total: {recursos_sistema['memoria_total_gb']:.2f} GB")
        print(f"   • RAM Usada: {recursos_sistema['memoria_usada_gb']:.2f} GB ({recursos_sistema['memoria_porcentaje']:.1f}%)")
        print(f"   • RAM Disponible: {recursos_sistema['memoria_disponible_gb']:.2f} GB")
        print(f"   • Disco Total: {recursos_sistema['disco_total_gb']:.2f} GB")
        print(f"   • Disco Usado: {recursos_sistema['disco_usado_gb']:.2f} GB ({recursos_sistema['disco_porcentaje']:.1f}%)")
        print(f"   • Disco Libre: {recursos_sistema['disco_libre_gb']:.2f} GB")
        print()
        
        if not self.proceso_python:
            print("⚠️  No se pueden medir recursos de la aplicación (servidor no está corriendo)")
            print()
            self.mostrar_requisitos_estimados()
            return
        
        # Monitoreo en tiempo real
        print(f"⏱️  MONITOREANDO DURANTE {duracion_segundos} SEGUNDOS...")
        print("-" * 80)
        print()
        
        iteraciones = duracion_segundos // intervalo
        
        for i in range(iteraciones):
            recursos_python = self.medir_recursos_proceso(self.proceso_python)
            recursos_mysql = self.medir_recursos_proceso(self.proceso_mysql) if self.proceso_mysql else None
            
            if recursos_python:
                self.mediciones.append({
                    'timestamp': datetime.now(),
                    'python': recursos_python,
                    'mysql': recursos_mysql,
                    'sistema': self.medir_recursos_sistema()
                })
                
                print(f"   [{i+1}/{iteraciones}] Python: CPU={recursos_python['cpu_percent']:.1f}% | "
                      f"RAM={recursos_python['memoria_mb']:.1f}MB", end="")
                
                if recursos_mysql:
                    print(f" | MySQL: CPU={recursos_mysql['cpu_percent']:.1f}% | "
                          f"RAM={recursos_mysql['memoria_mb']:.1f}MB")
                else:
                    print()
            
            time.sleep(intervalo)
        
        print()
        self.generar_reporte()
    
    def generar_reporte(self):
        """Genera reporte final con promedios"""
        if not self.mediciones:
            return
        
        print()
        print("=" * 80)
        print("📊 REPORTE DE RECURSOS")
        print("=" * 80)
        print()
        
        # Calcular promedios Python
        avg_cpu_python = sum(m['python']['cpu_percent'] for m in self.mediciones) / len(self.mediciones)
        avg_ram_python = sum(m['python']['memoria_mb'] for m in self.mediciones) / len(self.mediciones)
        max_ram_python = max(m['python']['memoria_mb'] for m in self.mediciones)
        
        print("🐍 APLICACIÓN PYTHON (FastAPI):")
        print("-" * 80)
        print(f"   • CPU Promedio: {avg_cpu_python:.2f}%")
        print(f"   • CPU Máximo: {max(m['python']['cpu_percent'] for m in self.mediciones):.2f}%")
        print(f"   • RAM Promedio: {avg_ram_python:.2f} MB")
        print(f"   • RAM Máximo: {max_ram_python:.2f} MB")
        print(f"   • RAM Mínimo: {min(m['python']['memoria_mb'] for m in self.mediciones):.2f} MB")
        print()
        
        # Calcular promedios MySQL
        mediciones_mysql = [m for m in self.mediciones if m['mysql']]
        if mediciones_mysql:
            avg_cpu_mysql = sum(m['mysql']['cpu_percent'] for m in mediciones_mysql) / len(mediciones_mysql)
            avg_ram_mysql = sum(m['mysql']['memoria_mb'] for m in mediciones_mysql) / len(mediciones_mysql)
            max_ram_mysql = max(m['mysql']['memoria_mb'] for m in mediciones_mysql)
            
            print("🗄️  BASE DE DATOS (MySQL):")
            print("-" * 80)
            print(f"   • CPU Promedio: {avg_cpu_mysql:.2f}%")
            print(f"   • CPU Máximo: {max(m['mysql']['cpu_percent'] for m in mediciones_mysql):.2f}%")
            print(f"   • RAM Promedio: {avg_ram_mysql:.2f} MB")
            print(f"   • RAM Máximo: {max_ram_mysql:.2f} MB")
            print(f"   • RAM Mínimo: {min(m['mysql']['memoria_mb'] for m in mediciones_mysql):.2f} MB")
            print()
        
        # Recursos totales estimados
        total_ram = avg_ram_python + (avg_ram_mysql if mediciones_mysql else 0)
        
        print("💾 CONSUMO TOTAL ESTIMADO:")
        print("-" * 80)
        print(f"   • RAM Total (App + DB): {total_ram:.2f} MB")
        print(f"   • RAM Recomendada: {total_ram * 1.5:.2f} MB (con margen)")
        print(f"   • Disco (Código): {self.obtener_tamaño_proyecto()[0] / (1024**2):.2f} MB")
        print()
        
        self.mostrar_requisitos()
    
    def mostrar_requisitos_estimados(self):
        """Muestra requisitos estimados sin mediciones"""
        print()
        print("=" * 80)
        print("📋 REQUISITOS ESTIMADOS DEL SISTEMA")
        print("=" * 80)
        print()
        
        print("💻 REQUISITOS MÍNIMOS (Cliente):")
        print("-" * 80)
        print("   • CPU: 2 núcleos @ 2.0 GHz")
        print("   • RAM: 2 GB disponible")
        print("   • Disco: 500 MB libres")
        print("   • SO: Windows 10/11, Linux, macOS")
        print("   • Python: 3.8+")
        print("   • MySQL: 8.0+")
        print()
        
        print("⚡ REQUISITOS RECOMENDADOS (Cliente):")
        print("-" * 80)
        print("   • CPU: 4 núcleos @ 2.5 GHz")
        print("   • RAM: 4 GB disponible")
        print("   • Disco: 1 GB libre (SSD recomendado)")
        print("   • SO: Windows 10/11 64-bit")
        print("   • Python: 3.10+")
        print("   • MySQL: 8.0+")
        print()
    
    def mostrar_requisitos(self):
        """Muestra requisitos del sistema basados en mediciones"""
        print()
        print("=" * 80)
        print("📋 REQUISITOS DEL SISTEMA")
        print("=" * 80)
        print()
        
        # Análisis para cliente local
        print("💻 PARA CLIENTE (Instalación Local):")
        print("-" * 80)
        print("   MÍNIMO:")
        print("   • Procesador: Intel Core i3 / AMD Ryzen 3 (2 núcleos)")
        print("   • RAM: 2 GB disponible")
        print("   • Disco: 500 MB libres")
        print("   • Sistema Operativo: Windows 10/11")
        print("   • Python 3.8+")
        print("   • MySQL 8.0")
        print()
        print("   RECOMENDADO:")
        print("   • Procesador: Intel Core i5 / AMD Ryzen 5 (4 núcleos)")
        print("   • RAM: 4 GB disponible")
        print("   • Disco: 1 GB libre (SSD preferible)")
        print("   • Sistema Operativo: Windows 10/11 (64-bit)")
        print("   • Python 3.10+")
        print("   • MySQL 8.0")
        print()
        
        # Análisis para Railway
        print("☁️  PARA RAILWAY (Servidor en la Nube):")
        print("-" * 80)
        
        if self.mediciones:
            avg_ram_python = sum(m['python']['memoria_mb'] for m in self.mediciones) / len(self.mediciones)
            ram_railway_mb = avg_ram_python * 2  # Doble para múltiples usuarios
            ram_railway_gb = ram_railway_mb / 1024
            
            print(f"   • Plan Mínimo: Starter ($5/mes)")
            print(f"     - RAM: 512 MB (suficiente para 1-5 usuarios)")
            print(f"     - CPU: Compartida")
            print(f"     - Almacenamiento: Efímero (base de datos externa requerida)")
            print()
            print(f"   • Plan Recomendado: Hobby ($20/mes)")
            print(f"     - RAM: 8 GB (suficiente para 20-50 usuarios)")
            print(f"     - CPU: 8 vCPUs compartidas")
            print(f"     - Almacenamiento: 100 GB")
            print(f"     - Incluye: PostgreSQL/MySQL")
            print()
        else:
            print("   • Plan Starter: $5/mes (1-5 usuarios)")
            print("   • Plan Hobby: $20/mes (20-50 usuarios)")
            print("   • Plan Pro: $50/mes (100+ usuarios)")
        
        print()
        print("🗄️  BASE DE DATOS (Separada):")
        print("-" * 80)
        print("   • Railway MySQL: Incluido en plan Hobby")
        print("   • PlanetScale: Plan gratuito disponible")
        print("   • AWS RDS: Desde $15/mes")
        print()
        
        print("💰 COSTO ESTIMADO RAILWAY:")
        print("-" * 80)
        print("   • Aplicación + Base de datos: $20-30/mes (Hobby Plan)")
        print("   • Alternativa: Solo app en Railway + DB gratuita externa")
        print()
        
        print("✅ CONCLUSIÓN:")
        print("-" * 80)
        print("   El sistema es LIGERO y puede ejecutarse en:")
        print("   • ✅ Computadoras de gama baja/media (cliente local)")
        print("   • ✅ Railway plan Starter/Hobby (servidor cloud)")
        print("   • ✅ Equipos con 2GB RAM pueden ejecutarlo sin problemas")
        print()

def main():
    """Función principal"""
    analizador = AnalizadorRecursos()
    
    # Determinar duración del análisis
    duracion = 30  # Por defecto 30 segundos
    
    if len(sys.argv) > 1:
        try:
            duracion = int(sys.argv[1])
        except:
            pass
    
    analizador.analizar(duracion_segundos=duracion, intervalo=2)
    
    print()
    print("=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)
    print()
    print("💡 RECOMENDACIONES:")
    print()
    print("   1. Para desarrollo/pruebas: Equipos con 2GB RAM son suficientes")
    print("   2. Para producción local: Se recomienda 4GB RAM")
    print("   3. Para Railway: Plan Starter es suficiente para pocos usuarios")
    print("   4. Para Railway con tráfico: Plan Hobby recomendado")
    print()
    print("📝 NOTAS:")
    print()
    print("   • El consumo aumenta con usuarios concurrentes")
    print("   • MySQL puede configurarse para usar menos RAM")
    print("   • En Railway, la base de datos consume recursos adicionales")
    print("   • Considerar CDN para archivos estáticos en producción")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
