# API de Cierres de Caja - Documentación

## Archivos Creados

### 1. **Frontend** - `app/static/cajas_cierre.html`
Interfaz visual para consultar cierres de caja con:
- Filtros por: Caja, Rango de fechas, Vendedor
- Tabla con columnas: CAJA, VENDEDOR, APERTURA, HORA, CIERRE, HORA
- Validación de fechas
- Información de sucursal
- Diseño responsivo

### 2. **Schema** - `app/schemas/cierre_caja.py`
Define la estructura de datos para:
- `CierreCajaResponse`: Un cierre individual
- `CierreCajaListResponse`: Lista de cierres con total

### 3. **Servicio** - `app/services/cierre_caja_service.py`
Lógica de negocio con métodos:
- `obtener_cierres()`: Obtiene cierres con filtros opcionales
- `obtener_estadisticas_cierre()`: Calcula estadísticas de cierres

### 4. **Endpoint** - `app/api/v1/endpoints/reportes.py` (actualizado)
Nuevo endpoint:
- `GET /api/v1/reportes/cierres-caja`

## Uso

### En Frontend
```javascript
// La página se conecta automáticamente al endpoint
// Solo necesita:
// 1. Token en localStorage (se verifica automáticamente)
// 2. Completar los filtros requeridos (fechas mínimo)
// 3. Hacer clic en "Buscar"
```

### En Backend
```python
# El endpoint se integra automáticamente con la API
# Acceso:
# GET /api/v1/reportes/cierres-caja?fecha_inicio=2025-01-01&fecha_fin=2025-01-31
# Parámetros opcionales: &caja=XXX&vendedor=YYY&local_id=1
```

## Flujo de Datos

1. **Usuario** selecciona filtros y presiona "Buscar"
2. **Frontend** valida fechas y envía petición GET
3. **Backend** (CierreCajaService) consulta base de datos
4. **API** retorna JSON con lista de cierres
5. **Frontend** renderiza tabla dinámicamente

## Respuesta de API

```json
{
  "total": 15,
  "cierres": [
    {
      "caja": "VENTAS01",
      "vendedor": "REINALDO OVIEDO CALIXTRO",
      "apertura": "05/01/2026",
      "hora_apertura": "09:12",
      "cierre": "05/01/2026",
      "hora_cierre": "18:20"
    }
  ]
}
```

## Notas Importantes

- Los datos se obtienen de la tabla `ventas` agrupados por caja y vendedor
- Las fechas se formatean automáticamente a DD/MM/YYYY
- Las horas se extraen del campo `fecha_creacion` de las ventas
- Los filtros son opcionales excepto las fechas
- La búsqueda es case-insensitive (ilike)

## Próximos Pasos (Opcional)

- [ ] Agregar paginación
- [ ] Agregar exportación a PDF/Excel
- [ ] Agregar estadísticas en gráficos
- [ ] Agregar detalle de ventas por cierre
- [ ] Crear endpoint para estadísticas de cierre
