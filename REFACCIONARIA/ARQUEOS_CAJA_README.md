# ARQUEOS DE CAJA - Documentación

## 📋 Descripción
La funcionalidad **Arqueos de Caja** permite registrar y auditar la conciliación de dinero entre los montos declarados en el sistema y los montos físicamente contados en las cajas.

## 🎯 Características Principales

### 1. **Registro de Arqueos**
- Crear nuevos arqueos de caja para cada turno o cierre de turno
- Registrar montos por forma de pago (Efectivo, Cheque, Tarjeta, Débito, Depósito, Crédito, Vale, Lealtad)
- Documentar observaciones sobre discrepancias

### 2. **Comparación Automática**
- Captura de montos **declarados** (según sistema)
- Captura de montos **contados** (verificación física)
- Cálculo automático de **diferencias** por forma de pago
- Cálculo automático de **diferencia total**

### 3. **Listado y Filtrado**
- Ver todos los arqueos realizados
- Filtrar por caja y local
- Visualizar estado de reconciliación

### 4. **Estados de Arqueo**
- **Equilibrado**: Cuando la diferencia total es $0
- **Discrepancia**: Cuando hay diferencia entre lo contado y lo declarado
- **Reconciliado**: Cuando ha sido revisado y validado

## 🏗️ Estructura Técnica

### Base de Datos - Tabla `arqueos_caja`
```sql
- id (Primary Key)
- caja (String): Identificador de la caja
- local_id (FK): Referencia al local
- usuario_id (FK): Usuario que realizó el arqueo
- fecha_arqueo (DateTime): Fecha y hora del arqueo
- turno (String): Mañana/Tarde/Noche
- efectivo_declarado, cheque_declarado, ... (Numeric)
- efectivo_contado, cheque_contado, ... (Numeric)
- diferencia_efectivo, diferencia_cheque, ... (Numeric - Calculadas automáticamente)
- total_declarado, total_contado, diferencia_total (Numeric)
- observaciones (Text)
- reconciliado (Boolean)
- responsable_reconciliacion (String)
```

### Archivos Implementados

#### Backend
- **Modelo**: [app/models/arqueo_caja.py](../app/models/arqueo_caja.py)
- **Schema**: [app/schemas/arqueo_caja.py](../app/schemas/arqueo_caja.py)
- **Service**: [app/services/arqueo_caja_service.py](../app/services/arqueo_caja_service.py)
- **CRUD**: [app/crud/arqueo_caja.py](../app/crud/arqueo_caja.py)
- **Endpoint API**: [app/api/v1/endpoints/arqueos_caja.py](../app/api/v1/endpoints/arqueos_caja.py)

#### Frontend
- **Vista**: [app/static/arqueos_caja.html](../app/static/arqueos_caja.html)

## 🔌 Endpoints API

### Crear Arqueo
```http
POST /api/v1/arqueos/caja
Content-Type: application/json

{
  "caja": "Caja 1",
  "local_id": 1,
  "usuario_id": 1,
  "turno": "Mañana",
  "efectivo_declarado": 5000,
  "efectivo_contado": 5050,
  ...
  "observaciones": "Diferencia en efectivo"
}
```

### Obtener Arqueo
```http
GET /api/v1/arqueos/caja/{id}
```

### Listar Arqueos
```http
GET /api/v1/arqueos/listar?caja=Caja%201&local_id=1
```

### Actualizar Arqueo
```http
PUT /api/v1/arqueos/caja/{id}
Content-Type: application/json

{
  "efectivo_contado": 5075,
  "reconciliado": true,
  "responsable_reconciliacion": "Gerente"
}
```

### Eliminar Arqueo
```http
DELETE /api/v1/arqueos/caja/{id}
```

## 🎨 Interfaz de Usuario

### Tab 1: Listar Arqueos
- Tabla con todos los arqueos registrados
- Filtros por caja y local
- Visualización de diferencias y estados
- Opciones para ver detalle y eliminar

### Tab 2: Nuevo Arqueo
- Formulario completo para crear un nuevo arqueo
- Secciones separadas para:
  - Información general
  - Montos declarados
  - Montos contados
  - Cálculo automático de diferencias
  - Observaciones
- Totales en tiempo real
- Botones para guardar o limpiar

### Tab 3: Reportes
- Resumen general de arqueos (en desarrollo)
- Estadísticas por caja
- Tendencias de discrepancias

## 🔐 Permisos y Roles

Recomendado para usuarios con roles:
- **Cajerero**: Crear y ver sus propios arqueos
- **Gerente de Caja**: Crear, ver, actualizar y reconciliar todos los arqueos
- **Administrador**: Acceso completo

## 📊 Ejemplo de Flujo de Uso

1. **Fin de turno del cajerero**: 
   - Navega a "ARQUEOS DE CAJA"
   - Click en "Nuevo Arqueo"
   - Ingresa los montos contados físicamente

2. **Sistema calcula automáticamente**:
   - Las diferencias por forma de pago
   - El total de discrepancia

3. **Revisión del gerente**:
   - Ver el arqueo en la lista
   - Revisar las diferencias
   - Si es correcto, marcar como reconciliado

4. **Auditoría**:
   - Acceso a histórico completo
   - Trazabilidad de quién realizó cada arqueo
   - Documentación de observaciones

## ⚙️ Configuración Inicial

Para usar esta funcionalidad:

1. ✅ Las migraciones de base de datos se crean automáticamente
2. ✅ El endpoint está registrado en la API
3. ✅ La vista HTML está disponible en `/static/arqueos_caja.html`
4. Integrar en el menú principal del dashboard

## 📝 Notas Importantes

- Los cálculos de diferencias se realizan automáticamente al guardar
- Las diferencias pueden ser positivas (sobrante) o negativas (faltante)
- Es posible reconciliar manualmente un arqueo aunque haya diferencias (con justificación en observaciones)
- Se registra automáticamente el usuario que realiza el arqueo

## 🔄 Integración con Otros Módulos

- **Cierres de Caja**: Los arqueos preceden a los cierres de caja
- **Reportes**: Se puede extraer información de arqueos para auditoría
- **Usuarios**: Se registra qué usuario realizó cada arqueo

## 🐛 Troubleshooting

### Problema: Errores de conexión a la API
**Solución**: Verificar que el servidor está corriendo y que `app/api/v1/api.py` incluye el import de `arqueos_caja_module`

### Problema: No aparecen los locales en el selector
**Solución**: Asegurarse de que existen registros en la tabla `locales`

### Problema: Las diferencias no se calculan
**Solución**: Verificar que los campos de entrada contienen valores numéricos válidos

## 📞 Soporte

Para reportar problemas o sugerir mejoras, consultar con el equipo de desarrollo.
