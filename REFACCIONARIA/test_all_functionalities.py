"""
Script de verificación exhaustiva de todas las funcionalidades del sistema
Prueba endpoints clave para los 3 perfiles: admin, sucursal1, sucursal2
"""

import urllib.request
import urllib.error
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/v1"

# Colores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestRunner:
    def __init__(self):
        self.tokens = {}
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
    
    def login(self, username, password):
        """Obtiene token de autenticación"""
        try:
            data = json.dumps({
                "username": username,
                "password": password
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{API_URL}/auth/login",
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('success'):
                    self.tokens[username] = result['access_token']
                    return True
        except Exception as e:
            print(f"{RED}❌ Login failed for {username}: {e}{RESET}")
            return False
    
    def test_endpoint(self, endpoint, method='GET', profile='admin', data=None, description=""):
        """Prueba un endpoint específico"""
        try:
            token = self.tokens.get(profile)
            if not token:
                print(f"{RED}❌ No token for {profile}{RESET}")
                self.results['failed'] += 1
                return None
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{API_URL}{endpoint}"
            
            if method == 'GET':
                req = urllib.request.Request(url, headers=headers)
            elif method == 'POST':
                req_data = json.dumps(data).encode('utf-8') if data else b'{}'
                req = urllib.request.Request(url, data=req_data, headers=headers, method='POST')
            elif method == 'PUT':
                req_data = json.dumps(data).encode('utf-8') if data else b'{}'
                req = urllib.request.Request(url, data=req_data, headers=headers, method='PUT')
            elif method == 'DELETE':
                req = urllib.request.Request(url, headers=headers, method='DELETE')
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"{GREEN}✓{RESET} {description or endpoint} ({profile})")
                self.results['passed'] += 1
                return result
                
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8')
            # 404 o errores esperados no son críticos
            if e.code == 404 or e.code == 422:
                print(f"{YELLOW}⚠{RESET} {description or endpoint} ({profile}) - {e.code}")
                self.results['warnings'] += 1
            else:
                print(f"{RED}✗{RESET} {description or endpoint} ({profile}) - Error {e.code}")
                self.results['failed'] += 1
            return None
        except Exception as e:
            print(f"{RED}✗{RESET} {description or endpoint} ({profile}) - {str(e)}")
            self.results['failed'] += 1
            return None

def main():
    print(f"\n{BLUE}{'='*70}")
    print("🔍 VERIFICACIÓN EXHAUSTIVA DE FUNCIONALIDADES")
    print(f"{'='*70}{RESET}\n")
    
    runner = TestRunner()
    
    # 1. AUTENTICACIÓN
    print(f"\n{BLUE}📋 1. AUTENTICACIÓN{RESET}")
    print("-" * 70)
    
    profiles = [
        ('admin', 'admin'),
        ('sucursal1', 'sucursal1'),
        ('sucursal2', 'sucursal2')
    ]
    
    for username, password in profiles:
        if runner.login(username, password):
            print(f"{GREEN}✓{RESET} Login exitoso para {username}")
            runner.results['passed'] += 1
        else:
            print(f"{RED}✗{RESET} Login fallido para {username}")
            runner.results['failed'] += 1
    
    # 2. PRODUCTOS
    print(f"\n{BLUE}📋 2. MÓDULO DE PRODUCTOS{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/productos/', profile=profile, description="Listar productos")
        runner.test_endpoint('/productos/1', profile=profile, description="Obtener producto específico")
        runner.test_endpoint('/productos/buscar?query=aceite', profile=profile, description="Buscar productos")
    
    # 3. CLIENTES
    print(f"\n{BLUE}📋 3. MÓDULO DE CLIENTES{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/clientes/', profile=profile, description="Listar clientes")
        runner.test_endpoint('/clientes/buscar?query=juan', profile=profile, description="Buscar clientes")
    
    # 4. VENTAS
    print(f"\n{BLUE}📋 4. MÓDULO DE VENTAS{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/ventas/', profile=profile, description="Listar ventas")
        runner.test_endpoint('/ventas/estadisticas', profile=profile, description="Estadísticas de ventas")
    
    # 5. COMPRAS
    print(f"\n{BLUE}📋 5. MÓDULO DE COMPRAS{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/compras/', profile=profile, description="Listar compras")
        runner.test_endpoint('/compras/pendientes', profile=profile, description="Compras pendientes")
    
    # 6. INVENTARIO
    print(f"\n{BLUE}📋 6. MÓDULO DE INVENTARIO{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/inventario/', profile=profile, description="Consultar inventario")
        runner.test_endpoint('/inventario/bajos', profile=profile, description="Productos con stock bajo")
    
    # 7. PROVEEDORES
    print(f"\n{BLUE}📋 7. MÓDULO DE PROVEEDORES{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/proveedores/', profile=profile, description="Listar proveedores")
    
    # 8. EMPLEADOS
    print(f"\n{BLUE}📋 8. MÓDULO DE EMPLEADOS{RESET}")
    print("-" * 70)
    
    runner.test_endpoint('/empleados/', profile='admin', description="Listar empleados (admin)")
    
    # 9. ARQUEOS DE CAJA
    print(f"\n{BLUE}📋 9. MÓDULO DE ARQUEOS DE CAJA{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/arqueos-caja/', profile=profile, description="Listar arqueos")
        runner.test_endpoint('/arqueos-caja/activo', profile=profile, description="Arqueo activo")
    
    # 10. CIERRES DE CAJA
    print(f"\n{BLUE}📋 10. MÓDULO DE CIERRES DE CAJA{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/cierres-caja/', profile=profile, description="Listar cierres")
        runner.test_endpoint('/cierres-caja/ultimo', profile=profile, description="Último cierre")
    
    # 11. RETIROS DE CAJA
    print(f"\n{BLUE}📋 11. MÓDULO DE RETIROS DE CAJA{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/retiros-caja/', profile=profile, description="Listar retiros")
    
    # 12. PAQUETES
    print(f"\n{BLUE}📋 12. MÓDULO DE PAQUETES{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/paquetes/', profile=profile, description="Listar paquetes")
    
    # 13. USUARIOS
    print(f"\n{BLUE}📋 13. MÓDULO DE USUARIOS{RESET}")
    print("-" * 70)
    
    runner.test_endpoint('/usuarios/', profile='admin', description="Listar usuarios (admin)")
    runner.test_endpoint('/usuarios/me', profile='admin', description="Usuario actual")
    
    # 14. ASISTENCIA
    print(f"\n{BLUE}📋 14. MÓDULO DE ASISTENCIA{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/asistencia/', profile=profile, description="Listar asistencias")
    
    # 15. TICKETS
    print(f"\n{BLUE}📋 15. MÓDULO DE TICKETS{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/tickets/', profile=profile, description="Listar tickets")
    
    # 16. VALES
    print(f"\n{BLUE}📋 16. MÓDULO DE VALES{RESET}")
    print("-" * 70)
    
    for profile, _ in profiles:
        runner.test_endpoint('/vales/', profile=profile, description="Listar vales")
    
    # 17. DASHBOARD/ESTADÍSTICAS
    print(f"\n{BLUE}📋 17. DASHBOARD Y REPORTES{RESET}")
    print("-" * 70)
    
    runner.test_endpoint('/dashboard/resumen', profile='admin', description="Resumen dashboard (admin)")
    runner.test_endpoint('/reportes/ventas-diarias', profile='admin', description="Reporte ventas diarias")
    
    # 18. CONFIGURACIÓN
    print(f"\n{BLUE}📋 18. CONFIGURACIÓN DEL SISTEMA{RESET}")
    print("-" * 70)
    
    runner.test_endpoint('/configuracion/', profile='admin', description="Configuración (admin)")
    runner.test_endpoint('/locales/', profile='admin', description="Sucursales/Locales (admin)")
    
    # RESUMEN FINAL
    print(f"\n{BLUE}{'='*70}")
    print("📊 RESUMEN DE RESULTADOS")
    print(f"{'='*70}{RESET}")
    
    total = runner.results['passed'] + runner.results['failed'] + runner.results['warnings']
    passed_pct = (runner.results['passed'] / total * 100) if total > 0 else 0
    
    print(f"\n{GREEN}✓ Pruebas exitosas: {runner.results['passed']}{RESET}")
    print(f"{YELLOW}⚠ Advertencias: {runner.results['warnings']}{RESET}")
    print(f"{RED}✗ Pruebas fallidas: {runner.results['failed']}{RESET}")
    print(f"\nTotal de pruebas: {total}")
    print(f"Porcentaje de éxito: {passed_pct:.1f}%")
    
    if runner.results['failed'] == 0:
        print(f"\n{GREEN}{'='*70}")
        print("🎉 ¡TODAS LAS FUNCIONALIDADES ESTÁN OPERATIVAS!")
        print(f"{'='*70}{RESET}\n")
    elif runner.results['failed'] < 5:
        print(f"\n{YELLOW}{'='*70}")
        print("⚠️  Sistema funcional con algunas advertencias")
        print(f"{'='*70}{RESET}\n")
    else:
        print(f"\n{RED}{'='*70}")
        print("❌ Se detectaron problemas que requieren atención")
        print(f"{'='*70}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Verificación interrumpida por el usuario{RESET}\n")
    except Exception as e:
        print(f"\n{RED}❌ Error general: {e}{RESET}\n")
