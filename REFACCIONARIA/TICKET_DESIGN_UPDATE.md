# 🧾 Actualización de Diseño de Tickets - Refaccionaria Oviedo

## 📋 Descripción de Cambios

Se ha actualizado el diseño de los tickets/recibos para incluir:

1. **Sección de Promociones**
   - Lavado y diagnóstico de inyectores por solo $50 c/u
   - Ubicada después de los totales del ticket

2. **Sección de Políticas de Devolución**
   - Política A: Período de devolución de 30 días
   - Política B: Inspección de partes eléctricas por especialista
   - Política C: Dependencia de políticas de fabricantes
   - Ubicada después de promociones

3. **Encabezado Mejorado**
   - Nombre de la empresa: REFACCIONARIA OVIEDO
   - Lema: "NUESTRA EXPERIENCIA MARCA LA DIFERENCIA"

## 📁 Archivos Creados/Modificados

### 1. `app/utils/ticket_printer.py` (Nuevo)
Utilidad centralizada para generar tickets formateados.

**Clases principales:**
- `TicketPrinter`: Generador de tickets con métodos estáticos

**Métodos principales:**
- `generate_header()`: Genera el encabezado con logo y lema
- `generate_promociones()`: Genera la sección de promociones
- `generate_politicas()`: Genera la sección de políticas de devolución
- `generate_ticket()`: Genera un ticket completo
- `generate_venta_rapida_ticket()`: Genera un ticket de venta rápida con todas las secciones

### 2. `app/api/v1/endpoints/tickets.py` (Modificado)
Se agregaron nuevos endpoints para generar y obtener tickets con el nuevo formato.

**Nuevos Endpoints:**

#### `POST /tickets/generar-formato`
Genera el formato completo del ticket con promociones y políticas.

**Request:**
```json
{
  "folio": "VZ0001",
  "cliente": "Cliente XYZ",
  "items": [
    {
      "descripcion": "Kit de frenos",
      "cantidad": 2,
      "precio": 500.00
    }
  ],
  "subtotal": 1000.00,
  "descuento": 100.00,
  "impuesto": 144.00,
  "total": 1044.00,
  "vendedor": "Juan Pérez",
  "incluir_qr": true
}
```

**Response:**
```json
{
  "folio": "VZ0001",
  "contenido_ticket": "... contenido formateado del ticket ...",
  "exito": true
}
```

#### `GET /tickets/{folio}/obtener-formato`
Obtiene el formato formateado de un ticket existente.

**Response:** `GenerarTicketResponse`

#### `GET /tickets/diseño/promociones`
Obtiene la lista de promociones actuales.

**Response:**
```json
{
  "promociones": [
    "LAVADO Y DIAGNÓSTICO DE",
    "INYECTORES POR SOLO $50 C/U"
  ],
  "titulo": "Promociones:"
}
```

#### `GET /tickets/diseño/politicas`
Obtiene la lista de políticas de devolución.

**Response:**
```json
{
  "politicas": [
    "A) EL PRODUCTO DEBE SER DEVUELTO EN UN PERIODO DE 30 DIAS",
    "B) LAS PARTES ELECTRICAS SERÁN REVISADAS POR UN ESPECIALISTA...",
    "C) AL NO SER FABRICANTES DEPENDEMOS DE LAS POLÍTICAS DE ELLOS..."
  ],
  "titulo": "Políticas de devolución:"
}
```

### 3. `app/static/preview_ticket.html` (Nuevo)
Página web para visualizar y probar la generación de tickets.

**Características:**
- Vista previa en tiempo real
- Editor de artículos
- Cálculo automático de totales
- Funcionalidad de impresión
- Simulación del formato del ticket

## 🎯 Cómo Usar

### Opción 1: API REST

```python
import requests

# Datos del ticket
datos = {
    "folio": "VZ0001",
    "cliente": "Cliente Test",
    "items": [
        {"descripcion": "Producto A", "cantidad": 1, "precio": 500},
        {"descripcion": "Producto B", "cantidad": 2, "precio": 300}
    ],
    "subtotal": 1100,
    "descuento": 50,
    "impuesto": 168,
    "total": 1218,
    "vendedor": "Vendedor XYZ"
}

# Realizar solicitud
response = requests.post(
    "http://localhost:8000/api/v1/tickets/generar-formato",
    json=datos
)

# Obtener resultado
ticket = response.json()
print(ticket["contenido_ticket"])
```

### Opción 2: Interfaz Web

1. Acceder a: `http://localhost:8000/preview_ticket.html`
2. Llenar los datos del ticket
3. Hacer clic en "Generar Vista Previa"
4. Imprimir o enviar a impresora térmica

### Opción 3: En Código Python

```python
from app.utils.ticket_printer import TicketPrinter

# Datos
items = [
    {"descripcion": "Kit de frenos", "cantidad": 2, "precio": 500},
    {"descripcion": "Aceite 5W-30", "cantidad": 1, "precio": 300}
]

# Generar ticket
ticket = TicketPrinter.generate_venta_rapida_ticket(
    folio="VZ0001",
    items=items,
    subtotal=1300,
    descuento=100,
    total=1200,
    vendedor="Juan Pérez"
)

# Imprimir o guardar
print(ticket)
```

## 📊 Estructura del Ticket

```
════════════════════════════════════════
         REFACCIONARIA OVIEDO
   NUESTRA EXPERIENCIA MARCA
        LA DIFERENCIA
════════════════════════════════════════

Folio: VZ0001
Fecha: 22/01/2026 10:30:45
Vendedor: Juan Pérez
Cliente: Cliente XYZ
────────────────────────────────────────

ARTÍCULOS
────────────────────────────────────────
Kit de frenos
  2x $500.00 = $1000.00
────────────────────────────────────────

                    Subtotal: $1000.00
                   Descuento: -$100.00
════════════════════════════════════════
                     TOTAL: $900.00
════════════════════════════════════════

Promociones:
────────────────────────────────────────
LAVADO Y DIAGNÓSTICO DE
INYECTORES POR SOLO $50 C/U
────────────────────────────────────────

Políticas de devolución:
────────────────────────────────────────
A) EL PRODUCTO DEBE SER DEVUELTO
   EN UN PERIODO DE 30 DIAS

B) LAS PARTES ELECTRICAS SERÁN
   REVISADAS POR UN ESPECIALISTA Y
   SU DEVOLUCIÓN DEPENDERÁ DE SU
   DIAGNOSTICO FINAL

C) AL NO SER FABRICANTES
   DEPENDEMOS DE LAS POLÍTICAS DE
   ELLOS PARA PODER EMITIR UNA
   RESOLUCIÓN DE GARANTÍA, GRACIAS
   POR SU COMPRENSIÓN
────────────────────────────────────────


      ¡GRACIAS POR SU COMPRA!

```

## 🔄 Modificaciones a Promociones y Políticas

Para actualizar las promociones o políticas de devolución, editar:

**En `app/utils/ticket_printer.py`:**

```python
class TicketPrinter:
    # Modificar estas listas
    PROMOCIONES = [
        "NUEVA PROMOCIÓN LÍNEA 1",
        "NUEVA PROMOCIÓN LÍNEA 2"
    ]
    
    POLITICAS_DEVOLUCION = [
        "Nueva política línea 1",
        "Nueva política línea 2",
        # ...
    ]
```

## 🖨️ Compatibilidad

El formato está optimizado para:
- ✅ Impresoras térmicas de 80mm
- ✅ Impresoras estándar (con ajuste de márgenes)
- ✅ Visualización en pantalla
- ✅ Impresoras de 58mm (ajustar TICKET_WIDTH a 30-35)

## 🧪 Pruebas

### Acceso a vista previa interactiva:
```
http://localhost:8000/preview_ticket.html
```

### Endpoint de prueba con curl:
```bash
curl -X POST "http://localhost:8000/api/v1/tickets/generar-formato" \
  -H "Content-Type: application/json" \
  -d '{
    "folio": "VZ0001",
    "cliente": "Test Cliente",
    "items": [
      {"descripcion": "Producto Test", "cantidad": 1, "precio": 100}
    ],
    "subtotal": 100,
    "descuento": 0,
    "impuesto": 16,
    "total": 116,
    "vendedor": "Test Vendedor"
  }'
```

## 📝 Notas Importantes

1. El formato está diseñado para ser enviado directamente a impresoras térmicas
2. Las dimensiones están optimizadas para 80mm de ancho
3. Los datos de promociones y políticas se pueden configurar dinámicamente
4. El QR es opcional pero puede integrarse con bibliotecas como `python-qrcode`

## 🔗 Integración con Sistema Existente

Para integrar con el sistema de ventas actual:

1. En el endpoint de venta rápida, agregar:
   ```python
   from app.utils.ticket_printer import TicketPrinter
   
   ticket_formato = TicketPrinter.generate_venta_rapida_ticket(...)
   # Enviar a impresora
   ```

2. En el frontend, usar:
   ```javascript
   // Llamar API
   fetch('/api/v1/tickets/generar-formato', {
       method: 'POST',
       body: JSON.stringify(datosTicket)
   })
   ```

---

**Versión:** 1.0  
**Fecha:** 22 de Enero de 2026  
**Empresa:** Refaccionaria Oviedo
