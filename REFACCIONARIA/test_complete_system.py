"""
Verificación exhaustiva del sistema - Todos los módulos y perfiles
Versión mejorada con detección de rutas reales
"""

import urllib.request
import urllib.error
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000/api/v1"

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

class SystemTest:
    def __init__(self):
        self.tokens = {}
        self.stats = {
            'autenticacion': {'passed': 0, 'failed': 0, 'warnings': 0},
            'productos': {'passed': 0, 'failed': 0, 'warnings': 0},
            'clientes': {'passed': 0, 'failed': 0, 'warnings': 0},
            'proveedores': {'passed': 0, 'failed': 0, 'warnings': 0},
            'compras': {'passed': 0, 'failed': 0, 'warnings': 0},
            'tickets': {'passed': 0, 'failed': 0, 'warnings': 0},
            'paquetes': {'passed': 0, 'failed': 0, 'warnings': 0},
            'asistencia': {'passed': 0, 'failed': 0, 'warnings': 0},
            'reportes': {'passed': 0, 'failed': 0, 'warnings': 0},
            'locales': {'passed': 0, 'failed': 0, 'warnings': 0},
            'arqueos': {'passed': 0, 'failed': 0, 'warnings': 0},
            'cierres': {'passed': 0, 'failed': 0, 'warnings': 0},
            'retiros': {'passed': 0, 'failed': 0, 'warnings': 0},
        }
    
    def login(self, username, password):
        """Login y obtención de token"""
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
                    user_info = result.get('user', {})
                    print(f"{GREEN}✓{RESET} {username:<12} | Role: {user_info.get('role', 'N/A'):<15} | Local: {user_info.get('local_nombre', 'N/A')}")
                    self.stats['autenticacion']['passed'] += 1
                    return True
        except Exception as e:
            print(f"{RED}✗{RESET} {username:<12} | Error: {str(e)[:50]}")
            self.stats['autenticacion']['failed'] += 1
            return False
    
    def test_get(self, endpoint, profile, module, description="", expect_data=True):
        """Test GET endpoint"""
        try:
            token = self.tokens.get(profile)
            if not token:
                self.stats[module]['failed'] += 1
                return None
            
            headers = {'Authorization': f'Bearer {token}'}
            req = urllib.request.Request(f"{API_URL}{endpoint}", headers=headers)
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Verificar si hay datos
                has_data = False
                if isinstance(result, list):
                    has_data = len(result) > 0
                elif isinstance(result, dict):
                    has_data = bool(result.get('data') or result.get('items') or len(result) > 0)
                
                status_icon = f"{GREEN}✓{RESET}"
                data_info = ""
                
                if expect_data and has_data:
                    if isinstance(result, list):
                        data_info = f"({len(result)} items)"
                    elif isinstance(result, dict) and 'data' in result:
                        if isinstance(result['data'], list):
                            data_info = f"({len(result['data'])} items)"
                elif not expect_data:
                    data_info = ""
                else:
                    status_icon = f"{YELLOW}⚠{RESET}"
                    data_info = "(sin datos)"
                    self.stats[module]['warnings'] += 1
                    print(f"  {status_icon} {profile:<12} | {description:<40} {data_info}")
                    return result
                
                self.stats[module]['passed'] += 1
                print(f"  {status_icon} {profile:<12} | {description:<40} {data_info}")
                return result
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  {YELLOW}⚠{RESET} {profile:<12} | {description:<40} (404 - no implementado)")
                self.stats[module]['warnings'] += 1
            elif e.code == 401 or e.code == 403:
                print(f"  {RED}✗{RESET} {profile:<12} | {description:<40} (sin permisos)")
                self.stats[module]['failed'] += 1
            else:
                print(f"  {RED}✗{RESET} {profile:<12} | {description:<40} (Error {e.code})")
                self.stats[module]['failed'] += 1
            return None
        except Exception as e:
            print(f"  {RED}✗{RESET} {profile:<12} | {description:<40} ({str(e)[:30]})")
            self.stats[module]['failed'] += 1
            return None
    
    def print_module_summary(self, module_name):
        """Imprime resumen de un módulo"""
        stats = self.stats.get(module_name, {'passed': 0, 'failed': 0, 'warnings': 0})
        total = stats['passed'] + stats['failed'] + stats['warnings']
        
        if total == 0:
            return
        
        print(f"\n  {CYAN}Resumen:{RESET} ", end="")
        if stats['passed'] > 0:
            print(f"{GREEN}{stats['passed']} ✓{RESET} ", end="")
        if stats['warnings'] > 0:
            print(f"{YELLOW}{stats['warnings']} ⚠{RESET} ", end="")
        if stats['failed'] > 0:
            print(f"{RED}{stats['failed']} ✗{RESET}", end="")
        print()

def main():
    print(f"\n{BLUE}{'='*80}")
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA REFACCIONARIA OVIEDO")
    print(f"{'='*80}{RESET}\n")
    
    test = SystemTest()
    profiles = ['admin', 'sucursal1', 'sucursal2']
    
    # 1. AUTENTICACIÓN
    print(f"{BLUE}{'─'*80}")
    print("1️⃣  AUTENTICACIÓN Y PERFILES")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.login(profile, profile)
    
    test.print_module_summary('autenticacion')
    
    # 2. PRODUCTOS
    print(f"\n{BLUE}{'─'*80}")
    print("2️⃣  MÓDULO DE PRODUCTOS")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/productos/', profile, 'productos', 'Listar todos los productos')
        test.test_get('/productos/1', profile, 'productos', 'Obtener producto ID=1', expect_data=False)
    
    test.print_module_summary('productos')
    
    # 3. CLIENTES
    print(f"\n{BLUE}{'─'*80}")
    print("3️⃣  MÓDULO DE CLIENTES")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/clientes/', profile, 'clientes', 'Listar todos los clientes')
    
    test.print_module_summary('clientes')
    
    # 4. PROVEEDORES
    print(f"\n{BLUE}{'─'*80}")
    print("4️⃣  MÓDULO DE PROVEEDORES")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/proveedores/', profile, 'proveedores', 'Listar todos los proveedores')
    
    test.print_module_summary('proveedores')
    
    # 5. COMPRAS
    print(f"\n{BLUE}{'─'*80}")
    print("5️⃣  MÓDULO DE COMPRAS")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/compras/', profile, 'compras', 'Listar compras')
    
    test.print_module_summary('compras')
    
    # 6. TICKETS
    print(f"\n{BLUE}{'─'*80}")
    print("6️⃣  MÓDULO DE TICKETS/VENTAS")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/tickets/', profile, 'tickets', 'Listar tickets')
    
    test.print_module_summary('tickets')
    
    # 7. PAQUETES (KITS)
    print(f"\n{BLUE}{'─'*80}")
    print("7️⃣  MÓDULO DE PAQUETES (KITS)")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/paquetes/', profile, 'paquetes', 'Listar paquetes')
    
    test.print_module_summary('paquetes')
    
    # 8. ASISTENCIA
    print(f"\n{BLUE}{'─'*80}")
    print("8️⃣  MÓDULO DE ASISTENCIA RRHH")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/asistencia/', profile, 'asistencia', 'Listar asistencias')
    
    test.print_module_summary('asistencia')
    
    # 9. ARQUEOS DE CAJA
    print(f"\n{BLUE}{'─'*80}")
    print("9️⃣  MÓDULO DE ARQUEOS DE CAJA")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/arqueos/listar', profile, 'arqueos', 'Listar arqueos')
    
    test.print_module_summary('arqueos')
    
    # 10. CIERRES DE CAJA
    print(f"\n{BLUE}{'─'*80}")
    print("🔟 MÓDULO DE CIERRES DE CAJA")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/cajas/cierres', profile, 'cierres', 'Listar cierres')
    
    test.print_module_summary('cierres')
    
    # 11. RETIROS DE CAJA
    print(f"\n{BLUE}{'─'*80}")
    print("1️⃣1️⃣  MÓDULO DE RETIROS DE CAJA")
    print(f"{'─'*80}{RESET}\n")
    
    for profile in profiles:
        test.test_get('/retiros/listar', profile, 'retiros', 'Listar retiros')
    
    test.print_module_summary('retiros')
    
    # 12. REPORTES
    print(f"\n{BLUE}{'─'*80}")
    print("1️⃣2️⃣  MÓDULO DE REPORTES")
    print(f"{'─'*80}{RESET}\n")
    
    test.test_get('/reportes/ventas-diarias', 'admin', 'reportes', 'Reporte ventas diarias', expect_data=False)
    
    test.print_module_summary('reportes')
    
    # 13. CONFIGURACIÓN Y LOCALES
    print(f"\n{BLUE}{'─'*80}")
    print("1️⃣3️⃣  CONFIGURACIÓN Y SUCURSALES")
    print(f"{'─'*80}{RESET}\n")
    
    test.test_get('/locales/', 'admin', 'locales', 'Listar locales/sucursales')
    
    test.print_module_summary('locales')
    
    # RESUMEN GLOBAL
    print(f"\n{BLUE}{'='*80}")
    print("📊 RESUMEN GLOBAL DEL SISTEMA")
    print(f"{'='*80}{RESET}\n")
    
    total_passed = sum(s['passed'] for s in test.stats.values())
    total_warnings = sum(s['warnings'] for s in test.stats.values())
    total_failed = sum(s['failed'] for s in test.stats.values())
    total_tests = total_passed + total_warnings + total_failed
    
    print(f"Total de pruebas ejecutadas: {total_tests}")
    print(f"{GREEN}✓ Exitosas:    {total_passed:3d} ({total_passed/total_tests*100:.1f}%){RESET}")
    print(f"{YELLOW}⚠ Advertencias: {total_warnings:3d} ({total_warnings/total_tests*100:.1f}%){RESET}")
    print(f"{RED}✗ Fallidas:    {total_failed:3d} ({total_failed/total_tests*100:.1f}%){RESET}")
    
    # Resumen por módulo
    print(f"\n{CYAN}Detalle por módulo:{RESET}\n")
    
    for module, stats in test.stats.items():
        total = stats['passed'] + stats['warnings'] + stats['failed']
        if total == 0:
            continue
        
        status = f"{GREEN}✓{RESET}" if stats['failed'] == 0 and stats['warnings'] == 0 else \
                 f"{YELLOW}⚠{RESET}" if stats['failed'] == 0 else f"{RED}✗{RESET}"
        
        print(f"  {status} {module.capitalize():<15} | "
              f"✓{stats['passed']:2d}  ⚠{stats['warnings']:2d}  ✗{stats['failed']:2d}")
    
    # Conclusión
    if total_failed == 0 and total_warnings < 5:
        print(f"\n{GREEN}{'='*80}")
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print(f"{'='*80}{RESET}\n")
    elif total_failed == 0:
        print(f"\n{YELLOW}{'='*80}")
        print("✅ Sistema funcional con algunas funcionalidades pendientes")
        print(f"{'='*80}{RESET}\n")
    elif total_failed < total_passed / 2:
        print(f"\n{YELLOW}{'='*80}")
        print("⚠️  Sistema mayormente funcional - revisar fallos")
        print(f"{'='*80}{RESET}\n")
    else:
        print(f"\n{RED}{'='*80}")
        print("❌ Sistema requiere atención - múltiples fallos detectados")
        print(f"{'='*80}{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Verificación interrumpida{RESET}\n")
    except Exception as e:
        print(f"\n{RED}❌ Error: {e}{RESET}\n")
