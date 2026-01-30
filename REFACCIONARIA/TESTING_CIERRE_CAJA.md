# Testing Checklist - Nuevo Cierre de Caja

## Prueba Rápida Manual

### 1. Verificar Visibilidad del Botón
- [ ] Navegar a `/static/cajas_cierre.html`
- [ ] Verificar que el botón "➕ Nuevo Cierre" aparece en la esquina superior derecha
- [ ] Hacer clic en el botón

### 2. Verificar Formulario de Nuevo Cierre
- [ ] La página `/static/cierre_caja_nuevo.html` se abre correctamente
- [ ] Se muestran los datos del cierre:
  - Caja (editable)
  - Fecha actual
  - Hora actual
  - Vendedor (del usuario logueado)
  - Sucursal (REFACCIONARIA OVIEDO)

### 3. Probar Checkboxes y Cálculos
- [ ] Hacer clic en checkbox "Efectivo"
- [ ] Ingresar valor: 1000
- [ ] Verificar que "Total ingresos (sin retiros)" = $1,000.00
- [ ] Verificar que "Total cierre (ingresos - retiros)" = $1,000.00
- [ ] Hacer clic en checkbox "Cheque"
- [ ] Ingresar valor: 500
- [ ] Verificar que "Total ingresos (sin retiros)" = $1,500.00
- [ ] Hacer clic en checkbox "Retiros"
- [ ] Ingresar valor: 200
- [ ] Verificar que "Total cierre (ingresos - retiros)" = $1,300.00

### 4. Probar Guardado
- [ ] Hacer clic en botón "Procesar"
- [ ] Verificar que se muestra alerta con:
  - "Cierre creado con éxito"
  - Número de folio (ID)
  - Total del cierre
- [ ] Verificar que se redirige a `/static/cajas_cierre.html`

### 5. Verificar BD (Opcional)
```sql
SELECT * FROM cierres_caja ORDER BY id DESC LIMIT 1;
```
Verificar que la fila contiene:
- `caja`: VENTAS01 (o el ingresado)
- `efectivo`: 1000
- `cheque`: 500
- `retiros`: 200
- `total_ingresos`: 1500
- `total_cierre`: 1300
- `usuario_id`: ID del usuario logueado
- `local_id`: Local del usuario

### 6. Probar Botón Cancelar
- [ ] Hacer clic nuevamente en "Nuevo Cierre"
- [ ] Hacer clic en botón "Cancelar"
- [ ] Verificar que vuelve a `/static/cajas_cierre.html` sin guardar

---

## Archivos Modificados/Creados

```
✓ app/models/cierre_caja.py (NUEVO)
✓ app/schemas/cierre_caja.py (ACTUALIZADO)
✓ app/services/cierre_caja_service.py (ACTUALIZADO)
✓ app/api/v1/endpoints/cierres_caja.py (NUEVO)
✓ app/api/v1/api.py (ACTUALIZADO - import router)
✓ app/core/database.py (ACTUALIZADO - import model)
✓ app/main.py (ACTUALIZADO - ruta GET /cajas-cierre)
✓ app/static/cajas_cierre.html (ACTUALIZADO - botón)
✓ app/static/cierre_caja_nuevo.html (NUEVO)
✓ scripts/create_cierres_caja_table.sql (NUEVO - para referencia)
✓ CIERRE_CAJA_NUEVO_RESUMEN.md (NUEVO - documentación)
```

---

## Notas Técnicas

- El endpoint POST `/api/v1/cajas/cierres` acepta JSON con montos
- Los totales se calculan en el backend (no se confía en valores del cliente)
- Se requiere autenticación (token en localStorage)
- El usuario_id y local_id se obtienen del objeto user en localStorage
- La tabla `cierres_caja` se crea automáticamente al iniciar la app
- Se usan transacciones para garantizar consistencia de datos

---

## Potenciales Errores y Soluciones

| Error | Solución |
|-------|----------|
| "No fue posible crear el cierre: 404" | El endpoint no está registrado, verificar que `cierres_caja_module.router` está en `api.py` |
| "No fue posible crear el cierre: 401" | Falta autenticación, verificar token en localStorage |
| Tabla no existe en BD | Ejecutar SQL o reiniciar app para que SQLAlchemy cree la tabla |
| Botón no aparece | Verificar que cajas_cierre.html tiene el botón en la sección sucursal-info |
| Cálculos no actualizan | Verificar JavaScript en cierre_caja_nuevo.html, función recalcular() |

---

## Integración con Menú

Para acceder desde el menú principal:
1. Dashboard → Cajas → Cierres de Caja → [Botón "Nuevo Cierre"]

La navegación está completamente integrada.
