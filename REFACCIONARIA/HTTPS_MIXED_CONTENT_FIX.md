# Guía de Configuración HTTPS y Mixed Content Fix en Railway

## Problema Identificado
El navegador bloquea contenido HTTP cuando la página se carga con HTTPS (Mixed Content error).

## Solución

### 1. Configuración en Railway

En Railway, tu aplicación está desplegada detrás de un reverse proxy que proporciona HTTPS automáticamente.

**Variables de Entorno a Configurar en Railway:**

```
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=<tu_url_de_mysql>
SECRET_KEY=<generar_una_clave_segura>
MYSQL_SERVER=<host_mysql>
MYSQL_USER=<usuario>
MYSQL_PASSWORD=<contraseña>
MYSQL_DB=refaccionaria_db
MYSQL_PORT=3306
```

### 2. Dockerfile (ya está correcto)

El Dockerfile actual está bien configurado:
```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Railway maneja el reverse proxy HTTPS automáticamente.

### 3. Middleware de HTTPS (IMPLEMENTADO)

Se agregó un middleware que:
- Detecta si está en modo producción
- Agrega el header `Strict-Transport-Security` que fuerza HTTPS en futuras solicitudes
- Asegura que todas las conexiones subsecuentes usen HTTPS

### 4. CORS Configurado (IMPLEMENTADO)

Se actualizó CORS para incluir:
- `https://refaccionaria-oviedo-production.up.railway.app`
- `https://refaccionaria-oviedo.up.railway.app`

### 5. URLs en Frontend (IMPLEMENTADO)

Todos los `fetch()` en JavaScript usan rutas relativas (`/api/v1/...`), lo que significa:
- Si la página está en HTTPS, las solicitudes serán HTTPS
- No hay URLs hardcodeadas con HTTP

## Pasos Para Desplegar

1. **Push a tu repositorio:**
   ```bash
   git add .
   git commit -m "Fix: Configure HTTPS and Mixed Content headers"
   git push origin Ricardo
   ```

2. **En Railway Dashboard:**
   - Ve a tu servicio
   - Settings → Environment → Variables
   - Agrega/actualiza `ENVIRONMENT=production`
   - Agrega/actualiza `DEBUG=false`
   - Asegúrate de que `DATABASE_URL` está correctamente configurada
   - El deploy se iniciará automáticamente

3. **Verifica el certificado SSL:**
   - Rails proporciona certificados SSL automáticos
   - La URL debe ser accesible con HTTPS
   - Abre navegador: `https://refaccionaria-oviedo-production.up.railway.app`

## Cómo Verificar que Está Funcionando

1. Abre la página en HTTPS
2. Abre Developer Tools (F12) → Console
3. No debería haber errores de "Mixed Content"
4. Las solicitudes a `/api/v1/...` deberían ser a HTTPS
5. El header `Strict-Transport-Security` debería estar presente en respuestas

## Si Aún Hay Problemas

Si persiste el error de Mixed Content:

1. **Verifica que ENVIRONMENT=production
2. **Revisa los headers de respuesta (en DevTools → Network):**
   - Debería tener: `Strict-Transport-Security: max-age=31536000; includeSubDomains`

3. **Borra el caché del navegador:**
   - Ctrl+Shift+Delete → Borra cookies y datos de sitios

4. **Prueba en incógnito:**
   - Abre Developer Tools en modo incógnito para descartar caché

## Resumen de Cambios Realizados

✅ Archivo: `app/core/config.py`
- Agregado: `ENVIRONMENT` variable
- Actualizado: `BACKEND_CORS_ORIGINS` con URLs de producción
- Actualizado: `DEBUG` para leer desde env.example

✅ Archivo: `app/main.py`
- Agregado: `HTTPSRedirectMiddleware` para producción
- Added: Header `Strict-Transport-Security`

✅ Archivo: `.env.example`
- Creado con configuración completa para producción

✅ Archivo: `app/static/cierre_caja_nuevo.html`
- Solucionado: Error `horaEl is not defined`
- Agregado: Inicialización de fecha y hora correctamente
