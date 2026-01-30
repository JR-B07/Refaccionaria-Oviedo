# Plan para cambiar "ventasdetalladas" a "devolucionesdetalladas"

## Información Recopilada:
- Archivo HTML `app/static/ventasdetalladas.html` ya contiene contenido para "Devoluciones Detalladas"
- Rutas en `app/main.py`: `/ventasdetalladas` y `/reporte-ventas-detalladas` apuntan al archivo HTML
- Menú en `app/static/reportes.html`: Opción "Devoluciones Detalladas" navega a '/reporte-devoluciones' (pero debería ser '/reporte-devoluciones-detalladas')
- API endpoint ya existe: `/api/v1/reportes/devoluciones-detalladas`
- Schema `app/schemas/devoluciones_detalladas.py` ya existe

## Plan:
1. Renombrar archivo HTML de `ventasdetalladas.html` a `devolucionesdetalladas.html`
2. Actualizar rutas en `app/main.py` para usar el nuevo nombre de archivo y rutas relacionadas con devoluciones
3. Actualizar navegación en `app/static/reportes.html` para apuntar a la ruta correcta
4. Verificar que no haya otras referencias que necesiten actualización

## Pasos a seguir:
- [ ] Renombrar archivo HTML
- [ ] Actualizar rutas en main.py
- [ ] Actualizar navegación en reportes.html
- [ ] Verificar funcionamiento
