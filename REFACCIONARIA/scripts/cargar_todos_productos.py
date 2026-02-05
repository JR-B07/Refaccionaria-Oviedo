"""
Script para cargar TODOS los productos (99 productos completo)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.producto import Producto

def cargar_todos_productos():
    db = SessionLocal()
    try:
        # Lista completa de 99 productos
        productos = [
            { "codigo": "LS-T1126 HS", "nombre": "EMPAQUE DE PLOMO", "marca": "DC", "categoria": "FORD / MAZDA / MERCURY", "descripcion": "CENTRAL AUT. CHEVROLET EQ", "precio_compra": 45.00, "precio_venta": 65.00, "stock_minimo": 5 },
            { "codigo": "TF-214", "nombre": "EMPAQUE DE TRANSMISION", "marca": "DCA", "categoria": "TOYOTA, SCION, LEXUS", "descripcion": "CHEVROLET COLORADO", "precio_compra": 85.00, "precio_venta": 120.00, "stock_minimo": 3 },
            { "codigo": "B-9293", "nombre": "BOMBA DE AGUA", "marca": "BW AUTOMOTIVE", "categoria": "NISSAN", "descripcion": "NISSAN AVRIO 1.6", "precio_compra": 350.00, "precio_venta": 495.00, "stock_minimo": 2 },
            { "codigo": "HA-1190-1", "nombre": "TORNILLO DE CARROCERIA", "marca": "DORL", "categoria": "CHEVROLET", "descripcion": "Tornillo de carrocería", "precio_compra": 8.50, "precio_venta": 15.00, "stock_minimo": 50 },
            { "codigo": "BE-39570-VL", "nombre": "RETEN CIGUENAL", "marca": "TF VICTOR", "categoria": "NISSAN", "descripcion": "AEROSSTAR, EXPLORER", "precio_compra": 65.00, "precio_venta": 95.00, "stock_minimo": 10 },
            { "codigo": "SE-T-R-0", "nombre": "SELLO DE SILICONE SHOCK", "marca": "TOWI", "categoria": "VW", "descripcion": "VW. CORRADO 92-2.8R, POINTER", "precio_compra": 25.00, "precio_venta": 40.00, "stock_minimo": 15 },
            { "codigo": "4BX7002 020", "nombre": "EMPAQUE DE BRIDA", "marca": "MAHLE", "categoria": "Universal", "descripcion": "Empaque de brida universal", "precio_compra": 12.00, "precio_venta": 22.00, "stock_minimo": 20 },
            { "codigo": "CL-95", "nombre": "ABRAZADERA CHECA", "marca": "TF MICUNI", "categoria": "VW", "descripcion": "VW. CORRADO 92-2.8R", "precio_compra": 18.00, "precio_venta": 30.00, "stock_minimo": 25 },
            { "codigo": "NEZ-7430050-5M", "nombre": "DRENAJE CRILCA", "marca": "EBAO", "categoria": "CHEVROLET, PONTIAC", "descripcion": "MINI COOPER", "precio_compra": 55.00, "precio_venta": 85.00, "stock_minimo": 8 },
            { "codigo": "MYY-2BBI38", "nombre": "VALVO DE INFLADORES", "marca": "KNT", "categoria": "Universal", "descripcion": "Válvula infladores universal", "precio_compra": 5.00, "precio_venta": 10.00, "stock_minimo": 100 },
            { "codigo": "32017", "nombre": "AMORTIGUADORES", "marca": "KYB", "categoria": "DODGE", "descripcion": "DODGE NITRO TODAV R", "precio_compra": 580.00, "precio_venta": 850.00, "stock_minimo": 4 },
            { "codigo": "D89HHT00650", "nombre": "FILTRO AIRE", "marca": "BOSCH", "categoria": "Universal", "descripcion": "Filtro de aire", "precio_compra": 95.00, "precio_venta": 145.00, "stock_minimo": 6 },
            { "codigo": "CD-1948N", "nombre": "BANDA DE TIEMPO", "marca": "KANADIAN", "categoria": "FORD", "descripcion": "FORD CONTOUR 1.6 2.0, MINI COOPER", "precio_compra": 185.00, "precio_venta": 275.00, "stock_minimo": 3 },
            { "codigo": "FE-3803", "nombre": "JOYA DE DISTRIBUCION", "marca": "UTAGAVAS IDEM", "categoria": "Universal", "descripcion": "Joya de distribución", "precio_compra": 125.00, "precio_venta": 185.00, "stock_minimo": 5 },
            { "codigo": "3499-040", "nombre": "ANILLOS", "marca": "GAMBER", "categoria": "AUDI", "descripcion": "AUDI A3 1.4 (1.3-17)", "precio_compra": 420.00, "precio_venta": 620.00, "stock_minimo": 2 },
            { "codigo": "14891", "nombre": "CADENA DISTRIBUCION", "marca": "HASTINGS", "categoria": "BUICK", "descripcion": "BUICK CENTURY 3.8", "precio_compra": 285.00, "precio_venta": 425.00, "stock_minimo": 3 },
            { "codigo": "V5-31457 LE", "nombre": "EMPAQUE MULTIPLE", "marca": "VS", "categoria": "ACURA", "descripcion": "ACURA CL 2.2, 2.3DN", "precio_compra": 95.00, "precio_venta": 145.00, "stock_minimo": 8 },
            { "codigo": "RE-213", "nombre": "BALEROS DE DIRECCION", "marca": "VSPPARTS", "categoria": "BUICK", "descripcion": "BUICK ENCORE 1.4", "precio_compra": 165.00, "precio_venta": 245.00, "stock_minimo": 6 },
            { "codigo": "VS-50213", "nombre": "EMPAQUE MULTIPLE", "marca": "VS", "categoria": "ACURA CL 2.2 SOHN", "descripcion": "ACURA", "precio_compra": 88.00, "precio_venta": 135.00, "stock_minimo": 8 },
            { "codigo": "PE-2100", "nombre": "BALEROS", "marca": "VSPPARTS", "categoria": "BUICK ENCORE 1.4 (1.3", "descripcion": "BUICK", "precio_compra": 160.00, "precio_venta": 240.00, "stock_minimo": 6 },
            { "codigo": "FP-3421", "nombre": "FILTRO DE ACEITE", "marca": "FRAM", "categoria": "Universal", "descripcion": "Filtro de aceite para motores", "precio_compra": 45.00, "precio_venta": 75.00, "stock_minimo": 15 },
            { "codigo": "BK-8892", "nombre": "BALATA DELANTERA", "marca": "BENDIX", "categoria": "NISSAN", "descripcion": "NISSAN SENTRA, TSURU", "precio_compra": 280.00, "precio_venta": 420.00, "stock_minimo": 8 },
            { "codigo": "RT-5521", "nombre": "ROTULA SUSPENSION", "marca": "MOOG", "categoria": "CHEVROLET", "descripcion": "CHEVROLET SPARK, AVEO", "precio_compra": 195.00, "precio_venta": 295.00, "stock_minimo": 10 },
            { "codigo": "AM-7734", "nombre": "AMORTIGUADOR DELANTERO", "marca": "MONROE", "categoria": "FORD", "descripcion": "FORD FOCUS, FIESTA", "precio_compra": 520.00, "precio_venta": 780.00, "stock_minimo": 4 },
            { "codigo": "TB-9045", "nombre": "TERMINAL DIRECCION", "marca": "TRW", "categoria": "VW", "descripcion": "VW GOL, POLO", "precio_compra": 165.00, "precio_venta": 250.00, "stock_minimo": 12 },
            { "codigo": "CR-2156", "nombre": "CRUCETA", "marca": "GKN", "categoria": "Universal", "descripcion": "Cruceta cardan universal", "precio_compra": 225.00, "precio_venta": 340.00, "stock_minimo": 6 },
            { "codigo": "FG-8821", "nombre": "FILTRO GASOLINA", "marca": "WIX", "categoria": "Toyota", "descripcion": "TOYOTA COROLLA, YARIS", "precio_compra": 85.00, "precio_venta": 135.00, "stock_minimo": 10 },
            { "codigo": "BJ-4432", "nombre": "BUJIA", "marca": "NGK", "categoria": "Universal", "descripcion": "Bujía de encendido", "precio_compra": 42.00, "precio_venta": 68.00, "stock_minimo": 40 },
            { "codigo": "CV-6789", "nombre": "CABLE DE BUJIA", "marca": "BERU", "categoria": "CHEVROLET", "descripcion": "CHEVROLET CHEVY, ASTRA", "precio_compra": 320.00, "precio_venta": 480.00, "stock_minimo": 5 },
            { "codigo": "PS-3344", "nombre": "PASTILLAS FRENO", "marca": "ATE", "categoria": "NISSAN", "descripcion": "NISSAN TIIDA, VERSA", "precio_compra": 310.00, "precio_venta": 465.00, "stock_minimo": 8 },
            { "codigo": "DF-7712", "nombre": "DISCO FRENO", "marca": "BREMBO", "categoria": "VW", "descripcion": "VW JETTA, GOLF", "precio_compra": 680.00, "precio_venta": 1020.00, "stock_minimo": 4 },
            { "codigo": "BR-5523", "nombre": "BOMBA FRENO", "marca": "ATE", "categoria": "FORD", "descripcion": "FORD RANGER, F-150", "precio_compra": 1250.00, "precio_venta": 1875.00, "stock_minimo": 2 },
            { "codigo": "RF-8834", "nombre": "REFACCIONES CARBURADOR", "marca": "NIEHOFF", "categoria": "Universal", "descripcion": "Kit reparación carburador", "precio_compra": 145.00, "precio_venta": 225.00, "stock_minimo": 8 },
            { "codigo": "TC-4521", "nombre": "TAPA COMBUSTIBLE", "marca": "STANT", "categoria": "Universal", "descripcion": "Tapa de tanque combustible", "precio_compra": 85.00, "precio_venta": 135.00, "stock_minimo": 15 },
            { "codigo": "TR-9921", "nombre": "TERMOSTATO", "marca": "GATES", "categoria": "CHEVROLET", "descripcion": "CHEVROLET SILVERADO", "precio_compra": 165.00, "precio_venta": 250.00, "stock_minimo": 10 },
            { "codigo": "MG-3387", "nombre": "MANGUERA RADIADOR", "marca": "DAYCO", "categoria": "NISSAN", "descripcion": "NISSAN PLATINA, CLIO", "precio_compra": 125.00, "precio_venta": 190.00, "stock_minimo": 8 },
            { "codigo": "RD-6654", "nombre": "RADIADOR", "marca": "VALEO", "categoria": "FORD", "descripcion": "FORD ESCORT, IKON", "precio_compra": 1850.00, "precio_venta": 2775.00, "stock_minimo": 2 },
            { "codigo": "VT-7788", "nombre": "VENTILADOR", "marca": "SPAL", "categoria": "Universal", "descripcion": "Ventilador eléctrico 12V", "precio_compra": 580.00, "precio_venta": 870.00, "stock_minimo": 3 },
            { "codigo": "BP-4455", "nombre": "BOMBA DE AGUA", "marca": "DOLZ", "categoria": "VW", "descripcion": "VW BEETLE, COMBI", "precio_compra": 385.00, "precio_venta": 580.00, "stock_minimo": 5 },
            { "codigo": "KD-9988", "nombre": "KIT DISTRIBUCION", "marca": "GATES", "categoria": "CHEVROLET", "descripcion": "CHEVROLET CAPTIVA", "precio_compra": 1450.00, "precio_venta": 2175.00, "stock_minimo": 2 },
            { "codigo": "DN-5633", "nombre": "DINAMO", "marca": "BOSCH", "categoria": "Sistemas Eléctricos", "descripcion": "Dinamo para cargador de batería", "precio_compra": 1200.00, "precio_venta": 1800.00, "stock_minimo": 2 },
            { "codigo": "BT-7722", "nombre": "BATERIA", "marca": "OPTIMA", "categoria": "Sistemas Eléctricos", "descripcion": "Batería 12V 800A", "precio_compra": 850.00, "precio_venta": 1275.00, "stock_minimo": 3 },
            { "codigo": "AR-8811", "nombre": "ARRANCADOR", "marca": "DELPHI", "categoria": "Sistemas Eléctricos", "descripcion": "Motor de arranque", "precio_compra": 580.00, "precio_venta": 870.00, "stock_minimo": 2 },
            { "codigo": "BG-4456", "nombre": "BOBINA ENCENDIDO", "marca": "LUCAS", "categoria": "Sistemas Eléctricos", "descripcion": "Bobina de encendido", "precio_compra": 225.00, "precio_venta": 340.00, "stock_minimo": 5 },
            { "codigo": "RG-3344", "nombre": "REGULADOR VOLTAJE", "marca": "BOSCH", "categoria": "Sistemas Eléctricos", "descripcion": "Regulador de voltaje del alternador", "precio_compra": 185.00, "precio_venta": 280.00, "stock_minimo": 6 },
            { "codigo": "ALT-9988", "nombre": "ALTERNADOR", "marca": "BOSCH", "categoria": "Sistemas Eléctricos", "descripcion": "Alternador 120A", "precio_compra": 1350.00, "precio_venta": 2025.00, "stock_minimo": 2 },
            { "codigo": "LT-5544", "nombre": "LIQUIDO TRANSMISION", "marca": "CASTROL", "categoria": "Transmisión", "descripcion": "Aceite para transmisión automática", "precio_compra": 125.00, "precio_venta": 190.00, "stock_minimo": 8 },
            { "codigo": "KE-2211", "nombre": "KIT EMBRAGUE", "marca": "SACHS", "categoria": "Transmisión", "descripcion": "Kit completo de embrague", "precio_compra": 850.00, "precio_venta": 1275.00, "stock_minimo": 2 },
            { "codigo": "DE-3322", "nombre": "DISCO EMBRAGUE", "marca": "SACHS", "categoria": "Transmisión", "descripcion": "Disco de embrague", "precio_compra": 320.00, "precio_venta": 480.00, "stock_minimo": 4 },
            { "codigo": "PR-4433", "nombre": "PRESION DISCO", "marca": "SACHS", "categoria": "Transmisión", "descripcion": "Plato de presión de embrague", "precio_compra": 285.00, "precio_venta": 430.00, "stock_minimo": 4 },
            { "codigo": "RO-5544", "nombre": "RODAMIENTO PRESION", "marca": "FAG", "categoria": "Transmisión", "descripcion": "Rodamiento de presión del embrague", "precio_compra": 165.00, "precio_venta": 250.00, "stock_minimo": 6 },
            { "codigo": "BG-6655", "nombre": "BOMBA GASOLINA", "marca": "PIERCE", "categoria": "Combustible", "descripcion": "Bomba de gasolina eléctrica", "precio_compra": 425.00, "precio_venta": 640.00, "stock_minimo": 3 },
            { "codigo": "RG-7766", "nombre": "REGULADOR PRESION", "marca": "PIERCE", "categoria": "Combustible", "descripcion": "Regulador de presión de combustible", "precio_compra": 185.00, "precio_venta": 280.00, "stock_minimo": 5 },
            { "codigo": "IN-8877", "nombre": "INYECTOR GASOLINA", "marca": "SIEMENS", "categoria": "Combustible", "descripcion": "Inyector de gasolina", "precio_compra": 280.00, "precio_venta": 420.00, "stock_minimo": 6 },
            { "codigo": "RL-9988", "nombre": "RIEL INYECTORES", "marca": "SIEMENS", "categoria": "Combustible", "descripcion": "Riel de inyectores", "precio_compra": 350.00, "precio_venta": 525.00, "stock_minimo": 2 },
            { "codigo": "AC-10W30", "nombre": "ACEITE 10W-30", "marca": "CASTROL", "categoria": "Lubricantes", "descripcion": "Aceite mineral para motores", "precio_compra": 85.00, "precio_venta": 128.00, "stock_minimo": 20 },
            { "codigo": "AC-15W40", "nombre": "ACEITE 15W-40", "marca": "MOBIL", "categoria": "Lubricantes", "descripcion": "Aceite semisintético", "precio_compra": 105.00, "precio_venta": 158.00, "stock_minimo": 20 },
            { "codigo": "AC-5W30", "nombre": "ACEITE 5W-30", "marca": "SHELL", "categoria": "Lubricantes", "descripcion": "Aceite sintético para climas fríos", "precio_compra": 145.00, "precio_venta": 218.00, "stock_minimo": 15 },
            { "codigo": "GR-9000", "nombre": "GRASA MULTIPROPÓSITO", "marca": "TIMKEN", "categoria": "Lubricantes", "descripcion": "Grasa para cojinetes y articulaciones", "precio_compra": 35.00, "precio_venta": 53.00, "stock_minimo": 25 },
            { "codigo": "LH-2000", "nombre": "LIQUIDO HIDRAULICO", "marca": "SHELL", "categoria": "Lubricantes", "descripcion": "Fluido hidráulico ISO VG 46", "precio_compra": 125.00, "precio_venta": 190.00, "stock_minimo": 8 },
            { "codigo": "CV-1234", "nombre": "CORREA VENTILADOR", "marca": "GATES", "categoria": "Correas y Bandas", "descripcion": "Correa del ventilador", "precio_compra": 95.00, "precio_venta": 145.00, "stock_minimo": 10 },
            { "codigo": "CA-5678", "nombre": "CORREA ALTERNADOR", "marca": "DAYCO", "categoria": "Correas y Bandas", "descripcion": "Correa del alternador", "precio_compra": 105.00, "precio_venta": 160.00, "stock_minimo": 10 },
            { "codigo": "CC-9012", "nombre": "CORREA COMPRESOR", "marca": "BANDO", "categoria": "Correas y Bandas", "descripcion": "Correa del compresor de aire acondicionado", "precio_compra": 115.00, "precio_venta": 175.00, "stock_minimo": 8 },
            { "codigo": "BS-3456", "nombre": "BANDA SERPENTINA", "marca": "CONTINENTAL", "categoria": "Correas y Bandas", "descripcion": "Banda serpentina múltiple", "precio_compra": 225.00, "precio_venta": 340.00, "stock_minimo": 5 },
            { "codigo": "TR-1111", "nombre": "TORNILLO RUEDA", "marca": "DIN", "categoria": "Tuercas y Tornillos", "descripcion": "Tornillo para rueda métrica", "precio_compra": 3.50, "precio_venta": 6.00, "stock_minimo": 100 },
            { "codigo": "TU-2222", "nombre": "TUERCA RUEDA", "marca": "DIN", "categoria": "Tuercas y Tornillos", "descripcion": "Tuerca de rueda", "precio_compra": 2.50, "precio_venta": 4.50, "stock_minimo": 100 },
            { "codigo": "PE-3333", "nombre": "PERNO CABEZAL", "marca": "GRADE 8", "categoria": "Tuercas y Tornillos", "descripcion": "Perno de cabezal de cilindros", "precio_compra": 15.00, "precio_venta": 28.00, "stock_minimo": 40 },
            { "codigo": "TO-4444", "nombre": "TORNILLO TAPA VALVULA", "marca": "DIN", "categoria": "Tuercas y Tornillos", "descripcion": "Tornillo para tapa de válvulas", "precio_compra": 4.00, "precio_venta": 7.00, "stock_minimo": 80 },
            { "codigo": "SO-1001", "nombre": "SENSOR OXIGENO", "marca": "NGK", "categoria": "Sensores", "descripcion": "Sensor lambda para sistema OBD", "precio_compra": 285.00, "precio_venta": 428.00, "stock_minimo": 5 },
            { "codigo": "ST-2002", "nombre": "SENSOR TEMPERATURA", "marca": "BERU", "categoria": "Sensores", "descripcion": "Sensor de temperatura del motor", "precio_compra": 145.00, "precio_venta": 218.00, "stock_minimo": 8 },
            { "codigo": "SF-3003", "nombre": "SENSOR FLUJO AIRE", "marca": "DELPHI", "categoria": "Sensores", "descripcion": "Sensor MAF de flujo de aire", "precio_compra": 325.00, "precio_venta": 488.00, "stock_minimo": 4 },
            { "codigo": "SP-4004", "nombre": "SENSOR PRESION ACEITE", "marca": "DELPHI", "categoria": "Sensores", "descripcion": "Sensor de presión de aceite", "precio_compra": 95.00, "precio_venta": 143.00, "stock_minimo": 10 },
            { "codigo": "MH-1001", "nombre": "MANGUERA AGUA MOTOR", "marca": "CONTITECH", "categoria": "Mangueras", "descripcion": "Manguera de radiador superior", "precio_compra": 85.00, "precio_venta": 128.00, "stock_minimo": 8 },
            { "codigo": "MH-2002", "nombre": "MANGUERA FRENO", "marca": "CONTITECH", "categoria": "Mangueras", "descripcion": "Manguera de freno reforzada", "precio_compra": 125.00, "precio_venta": 190.00, "stock_minimo": 6 },
            { "codigo": "MH-3003", "nombre": "MANGUERA COMBUSTIBLE", "marca": "CONTITECH", "categoria": "Mangueras", "descripcion": "Manguera para línea de combustible", "precio_compra": 75.00, "precio_venta": 115.00, "stock_minimo": 10 },
            { "codigo": "MH-4004", "nombre": "MANGUERA AIRE COMPRIMIDO", "marca": "CONTITECH", "categoria": "Mangueras", "descripcion": "Manguera para aire comprimido", "precio_compra": 95.00, "precio_venta": 145.00, "stock_minimo": 8 },
            { "codigo": "CP-5001", "nombre": "CILINDRO PRINCIPAL FRENO", "marca": "ATE", "categoria": "Sistema de Frenos", "descripcion": "Cilindro maestro de freno", "precio_compra": 385.00, "precio_venta": 580.00, "stock_minimo": 3 },
            { "codigo": "CP-5002", "nombre": "CILINDRO RUEDA FRENO", "marca": "ATE", "categoria": "Sistema de Frenos", "descripcion": "Cilindro de freno de rueda", "precio_compra": 145.00, "precio_venta": 218.00, "stock_minimo": 8 },
            { "codigo": "RJ-6001", "nombre": "RÓTULA INFERIOR", "marca": "MOOG", "categoria": "Suspensión", "descripcion": "Rótula inferior de dirección", "precio_compra": 165.00, "precio_venta": 248.00, "stock_minimo": 6 },
            { "codigo": "RJ-6002", "nombre": "RÓTULA SUPERIOR", "marca": "MOOG", "categoria": "Suspensión", "descripcion": "Rótula superior de dirección", "precio_compra": 175.00, "precio_venta": 263.00, "stock_minimo": 6 },
            { "codigo": "BR-7001", "nombre": "BRAZO SUSPENSIÓN", "marca": "MOOG", "categoria": "Suspensión", "descripcion": "Brazo de control inferior", "precio_compra": 285.00, "precio_venta": 428.00, "stock_minimo": 4 },
            { "codigo": "BR-7002", "nombre": "BARRA ESTABILIZADORA", "marca": "MOOG", "categoria": "Suspensión", "descripcion": "Barra estabilizadora delantera", "precio_compra": 425.00, "precio_venta": 638.00, "stock_minimo": 3 },
            { "codigo": "JN-8001", "nombre": "JUNTA HOMOCINÉTICA", "marca": "GKN", "categoria": "Transmisión", "descripcion": "Junta triple de tracción", "precio_compra": 520.00, "precio_venta": 780.00, "stock_minimo": 3 },
            { "codigo": "JN-8002", "nombre": "JUNTA TELESCÓPICA", "marca": "GKN", "categoria": "Transmisión", "descripcion": "Junta telescópica de cardan", "precio_compra": 385.00, "precio_venta": 578.00, "stock_minimo": 3 },
            { "codigo": "CM-9001", "nombre": "CASQUILLO MOTOR", "marca": "MAHLE", "categoria": "Motor", "descripcion": "Casquillo de bloque de motor", "precio_compra": 35.00, "precio_venta": 53.00, "stock_minimo": 20 },
            { "codigo": "PC-9002", "nombre": "PISTON COMPLETO", "marca": "MAHLE", "categoria": "Motor", "descripcion": "Pistón con anillos incluidos", "precio_compra": 285.00, "precio_venta": 428.00, "stock_minimo": 4 },
            { "codigo": "BL-9003", "nombre": "BLOQUE MOTOR", "marca": "MAHLE", "categoria": "Motor", "descripcion": "Bloque de cilindros remanufacturado", "precio_compra": 3200.00, "precio_venta": 4800.00, "stock_minimo": 1 },
            { "codigo": "JG-9004", "nombre": "JUNTA CILINDRO", "marca": "MAHLE", "categoria": "Motor", "descripcion": "Junta de culata de cilindros", "precio_compra": 165.00, "precio_venta": 248.00, "stock_minimo": 8 },
            { "codigo": "VV-9005", "nombre": "VALVULA ESCAPE", "marca": "MAHLE", "categoria": "Motor", "descripcion": "Válvula de escape de motor", "precio_compra": 95.00, "precio_venta": 143.00, "stock_minimo": 15 },
            { "codigo": "VA-9006", "nombre": "VALVULA ADMISION", "marca": "MAHLE", "categoria": "Motor", "descripcion": "Válvula de admisión de motor", "precio_compra": 95.00, "precio_venta": 143.00, "stock_minimo": 15 },
            { "codigo": "AC-1001", "nombre": "ADAPTADOR CARBURADOR", "marca": "EDELBROCK", "categoria": "Accesorios", "descripcion": "Adaptador múltiple de carburador", "precio_compra": 225.00, "precio_venta": 338.00, "stock_minimo": 5 },
            { "codigo": "AC-1002", "nombre": "TUBO ESCAPE", "marca": "FLOWMASTER", "categoria": "Accesorios", "descripcion": "Tubo de escape silenciador", "precio_compra": 385.00, "precio_venta": 578.00, "stock_minimo": 3 },
            { "codigo": "AC-1003", "nombre": "CATALIZADOR", "marca": "WALKER", "categoria": "Accesorios", "descripcion": "Convertidor catalítico OEM", "precio_compra": 1200.00, "precio_venta": 1800.00, "stock_minimo": 2 },
            { "codigo": "AC-1004", "nombre": "SILENCIADOR INTERMEDIO", "marca": "WALKER", "categoria": "Accesorios", "descripcion": "Silenciador de tubo central", "precio_compra": 425.00, "precio_venta": 638.00, "stock_minimo": 3 },
            { "codigo": "AC-1005", "nombre": "TAPAS DISTRIBUIDOR", "marca": "ACCEL", "categoria": "Accesorios", "descripcion": "Tapa de distribuidor de encendido", "precio_compra": 145.00, "precio_venta": 218.00, "stock_minimo": 10 },
            { "codigo": "AC-1006", "nombre": "ROTOR DISTRIBUIDOR", "marca": "ACCEL", "categoria": "Accesorios", "descripcion": "Rotor de distribuidor", "precio_compra": 125.00, "precio_venta": 188.00, "stock_minimo": 12 },
            { "codigo": "AC-1007", "nombre": "ESCOBILLAS ALTERNADOR", "marca": "BOSCH", "categoria": "Accesorios", "descripcion": "Escobillas de carbón para alternador", "precio_compra": 65.00, "precio_venta": 98.00, "stock_minimo": 20 },
            { "codigo": "AC-1008", "nombre": "RECUBRIMIENTO RADIADOR", "marca": "DORMAN", "categoria": "Accesorios", "descripcion": "Tapa frontal de radiador", "precio_compra": 185.00, "precio_venta": 278.00, "stock_minimo": 5 },
            { "codigo": "AC-1009", "nombre": "VENTILADOR ELECTROVENTILADOR", "marca": "SPAL", "categoria": "Accesorios", "descripcion": "Ventilador eléctrico universal", "precio_compra": 425.00, "precio_venta": 638.00, "stock_minimo": 3 },
            { "codigo": "AC-1010", "nombre": "RELOJ DE GASOLINA", "marca": "AUTOMETER", "categoria": "Accesorios", "descripcion": "Indicador de nivel de combustible", "precio_compra": 185.00, "precio_venta": 278.00, "stock_minimo": 8 }
        ]

        print("=" * 60)
        print("CARGANDO TODOS LOS PRODUCTOS (99 PRODUCTOS)")
        print("=" * 60)
        
        agregados = 0
        existentes = 0
        
        for prod_data in productos:
            # Verificar si ya existe
            existe = db.query(Producto).filter(Producto.codigo == prod_data["codigo"]).first()
            
            if existe:
                print(f"⚠️  Ya existe: {prod_data['codigo']} - {prod_data['nombre']}")
                existentes += 1
                continue
            
            # Crear el producto
            nuevo_producto = Producto(
                codigo=prod_data["codigo"],
                nombre=prod_data["nombre"],
                descripcion=prod_data.get("descripcion"),
                marca=prod_data.get("marca"),
                categoria=prod_data.get("categoria"),
                precio_compra=prod_data["precio_compra"],
                precio_venta=prod_data["precio_venta"],
                stock_total=0,  # Inicialmente sin stock
                stock_minimo=prod_data.get("stock_minimo", 5)
            )
            
            db.add(nuevo_producto)
            print(f"✅ Agregado: {prod_data['codigo']} - {prod_data['nombre']}")
            agregados += 1
        
        # Confirmar cambios
        db.commit()
        
        print("=" * 60)
        print(f"✅ Productos agregados: {agregados}")
        print(f"⚠️  Productos que ya existían: {existentes}")
        print(f"📊 Total procesados: {len(productos)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🚀 Iniciando carga de TODOS los productos...\n")
    cargar_todos_productos()
    print("\n✅ Proceso completado!\n")
