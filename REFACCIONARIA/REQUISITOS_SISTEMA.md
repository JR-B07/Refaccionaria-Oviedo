# 📊 Requisitos del Sistema - Refaccionaria Oviedo

## 🔍 Análisis de Recursos

Este documento detalla los requisitos de hardware y software para ejecutar el Sistema ERP Refaccionaria Oviedo tanto en instalación local (cliente) como en servidor en la nube (Railway).

---

## 💻 INSTALACIÓN LOCAL (Cliente)

### Requisitos Mínimos

| Componente | Especificación |
|------------|----------------|
| **Procesador** | Intel Core i3 / AMD Ryzen 3 (2 núcleos @ 2.0 GHz) |
| **RAM** | 2 GB disponible |
| **Almacenamiento** | 500 MB libres en disco duro |
| **Sistema Operativo** | Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+ |
| **Python** | 3.8 o superior |
| **Base de Datos** | MySQL 8.0 o superior |
| **Navegador** | Chrome 90+, Firefox 88+, Edge 90+ |
| **Conexión** | No requiere internet (modo local) |

### Requisitos Recomendados

| Componente | Especificación |
|------------|----------------|
| **Procesador** | Intel Core i5 / AMD Ryzen 5 (4 núcleos @ 2.5 GHz) |
| **RAM** | 4 GB disponible |
| **Almacenamiento** | 1 GB libre en SSD |
| **Sistema Operativo** | Windows 10/11 64-bit |
| **Python** | 3.10 o superior |
| **Base de Datos** | MySQL 8.0 con optimización |
| **Navegador** | Última versión de Chrome/Edge |
| **Conexión** | Opcional para actualizaciones |

---

## 📦 Tamaño del Proyecto

| Componente | Tamaño |
|------------|--------|
| **Código Fuente** | ~150-200 MB |
| **Dependencias Python** | ~300-400 MB |
| **Base de Datos (vacía)** | ~50 MB |
| **Base de Datos (1 año datos)** | ~500 MB - 1 GB |
| **Total Estimado** | ~1-2 GB |

---

## 🐍 Consumo de Recursos - Aplicación Python (FastAPI)

### En Reposo (Sin usuarios activos)

| Métrica | Valor |
|---------|-------|
| **CPU** | 0.5% - 2% |
| **RAM** | 80-120 MB |
| **Disco (Lectura/Escritura)** | < 1 MB/s |

### Con Actividad Normal (1-5 usuarios)

| Métrica | Valor |
|---------|-------|
| **CPU** | 5% - 15% |
| **RAM** | 150-250 MB |
| **Disco (Lectura/Escritura)** | 2-5 MB/s |

### Con Actividad Alta (10-20 usuarios)

| Métrica | Valor |
|---------|-------|
| **CPU** | 20% - 40% |
| **RAM** | 300-500 MB |
| **Disco (Lectura/Escritura)** | 10-20 MB/s |

---

## 🗄️ Consumo de Recursos - MySQL

### Configuración Mínima

| Métrica | Valor |
|---------|-------|
| **CPU** | 1% - 5% |
| **RAM** | 200-400 MB |
| **Disco** | Variable según datos |

### Configuración Recomendada

| Métrica | Valor |
|---------|-------|
| **CPU** | 5% - 10% |
| **RAM** | 512 MB - 1 GB |
| **Disco** | SSD recomendado |
| **InnoDB Buffer Pool** | 256-512 MB |

---

## ☁️ RAILWAY (Servidor en la Nube)

### Plan Starter - $5/mes

**Especificaciones:**
- **RAM**: 512 MB
- **CPU**: vCPU compartida
- **Almacenamiento**: Efímero (no persistente)
- **Ancho de banda**: 100 GB/mes
- **Usuarios concurrentes**: 1-5

**✅ Suficiente para:**
- Pruebas y desarrollo
- 1-3 usuarios simultáneos
- Demostración del sistema
- Base de datos externa requerida

**❌ Limitaciones:**
- Sin almacenamiento persistente
- CPU compartida (puede ser lenta)
- No incluye base de datos

---

### Plan Hobby - $20/mes ⭐ RECOMENDADO

**Especificaciones:**
- **RAM**: 8 GB
- **CPU**: 8 vCPUs compartidas
- **Almacenamiento**: 100 GB persistente
- **Ancho de banda**: 500 GB/mes
- **Base de datos**: MySQL/PostgreSQL incluida
- **Usuarios concurrentes**: 20-50

**✅ Suficiente para:**
- Producción pequeña/mediana empresa
- 10-30 usuarios simultáneos
- Almacenamiento de archivos
- Base de datos integrada
- Backups automáticos

**💰 Costo Total Estimado:**
- Aplicación + Base de datos: **$20-30/mes**

---

### Plan Pro - $50/mes

**Especificaciones:**
- **RAM**: Escalable (hasta 32 GB)
- **CPU**: vCPUs dedicadas
- **Almacenamiento**: Escalable
- **Ancho de banda**: Ilimitado
- **Usuarios concurrentes**: 100+

**✅ Ideal para:**
- Empresas grandes
- Alto tráfico
- Múltiples sucursales
- Operación crítica 24/7

---

## 📊 Comparativa de Recursos

### Consumo Total Estimado

| Escenario | CPU | RAM | Disco |
|-----------|-----|-----|-------|
| **Desarrollo (1 usuario)** | 5-10% | 300-500 MB | 1 GB |
| **Producción Local (5 usuarios)** | 15-25% | 500 MB - 1 GB | 2 GB |
| **Railway Starter (3 usuarios)** | Compartida | 512 MB | 500 MB |
| **Railway Hobby (20 usuarios)** | 8 vCPUs | 2-4 GB | 5-10 GB |

---

## 🔧 Optimizaciones para Mejorar Rendimiento

### Aplicación Python

```python
# Configuración recomendada en .env
WORKERS=2  # Para Railway Starter
WORKERS=4  # Para Railway Hobby
MAX_CONNECTIONS=100
TIMEOUT=30
```

### Base de Datos MySQL

```ini
# my.cnf optimizado para recursos limitados
[mysqld]
innodb_buffer_pool_size=256M
max_connections=50
thread_cache_size=8
table_open_cache=400
query_cache_size=32M
```

---

## 💾 Alternativas de Base de Datos para Railway

| Servicio | Plan Gratuito | Costo |
|----------|---------------|-------|
| **PlanetScale** | ✅ 5 GB | $0 - $39/mes |
| **Railway MySQL** | ❌ No | Incluido en Hobby |
| **AWS RDS** | ❌ No | Desde $15/mes |
| **Google Cloud SQL** | ❌ No | Desde $10/mes |
| **Supabase** | ✅ 500 MB | $0 - $25/mes |

**Recomendación:** PlanetScale (plan gratuito) + Railway Starter = **$5/mes total**

---

## 📈 Escalabilidad

### Crecimiento de Recursos según Usuarios

| Usuarios Simultáneos | RAM Recomendada | CPU | Plan Railway |
|----------------------|-----------------|-----|--------------|
| 1-5 | 512 MB - 1 GB | 1-2 vCPUs | Starter |
| 5-20 | 2-4 GB | 2-4 vCPUs | Hobby |
| 20-50 | 4-8 GB | 4-8 vCPUs | Hobby+ |
| 50-100 | 8-16 GB | 8+ vCPUs | Pro |
| 100+ | 16+ GB | 16+ vCPUs | Enterprise |

---

## ✅ Conclusiones

### Para Cliente Local

- ✅ **Equipos de gama baja funcionan perfectamente**
- ✅ **2 GB RAM es suficiente para uso individual**
- ✅ **4 GB RAM recomendado para múltiples usuarios en red local**
- ✅ **No requiere hardware especializado**
- ✅ **Funciona en computadoras de oficina estándar**

### Para Railway

- ✅ **Plan Starter ($5/mes) funciona para demos y pruebas**
- ⭐ **Plan Hobby ($20/mes) ideal para pequeñas empresas**
- ✅ **Sistema optimizado para bajo consumo de recursos**
- 💰 **Costo-beneficio excelente comparado con hosting tradicional**
- 🚀 **Escalable según crecimiento del negocio**

### Optimización General

- 🔥 **Sistema LIGERO**: Consume menos recursos que sistemas similares
- ⚡ **Rápido**: Respuesta < 100ms en operaciones típicas
- 💾 **Eficiente**: Base de datos optimizada con índices
- 🌐 **Flexible**: Funciona tanto local como en la nube
- 📱 **Responsive**: Se adapta a diferentes dispositivos

---

## 🛠️ Herramientas de Monitoreo

### Para medir recursos en tiempo real:

```bash
# Ejecutar análisis de recursos (30 segundos)
python analizar_recursos.py

# Ejecutar análisis extendido (60 segundos)
python analizar_recursos.py 60
```

### Instalar psutil para análisis:

```bash
pip install psutil
```

---

## 📞 Recomendaciones Finales

### Cliente Local (Refaccionaria Física)

1. **Hardware**: Cualquier PC de oficina moderna (últimos 5 años)
2. **Sistema Operativo**: Windows 10/11 64-bit
3. **RAM**: 4 GB mínimo (8 GB ideal)
4. **Disco**: SSD preferible para mejor velocidad
5. **Red**: No requiere internet (100% offline)

### Servidor Railway (Acceso Remoto)

1. **Plan Inicial**: Hobby $20/mes (incluye todo)
2. **Base de Datos**: Incluida en el plan
3. **Escalabilidad**: Aumentar recursos según crecimiento
4. **Backup**: Configurar backups automáticos diarios
5. **Monitoreo**: Usar dashboard de Railway para métricas

---

## 📅 Fecha de Análisis

**Versión**: 1.0  
**Fecha**: 3 de febrero de 2026  
**Sistema**: Refaccionaria Oviedo ERP  
**Framework**: FastAPI + MySQL  

---

**Desarrollado para Refaccionaria Oviedo** 🏪
