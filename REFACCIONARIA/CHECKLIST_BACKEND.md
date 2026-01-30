# ⚙️ CHECKLIST DE CONFIGURACIÓN - SISTEMA DE 2 SUCURSALES

## 🔐 LOGIN (Backend)

El endpoint de login DEBE retornar `local_id`:

```python
# app/api/v1/auth.py (o similar)

@router.post("/login")
def login(credentials: LoginSchema):
    user = db.query(Usuario).filter(
        Usuario.nombre_usuario == credentials.username
    ).first()
    
    if not user:
        raise HTTPException(status_code=401)
    
    # Verificar contraseña...
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.nombre_usuario,
            "name": user.nombre,
            "email": user.email,
            "local_id": user.local_id,  # ✅ IMPORTANTE
            "rol": user.rol.value
        }
    }
```

## 📋 MODELOS (Backend)

### Usuario
```python
class Usuario(ModeloBase):
    __tablename__ = "usuarios"
    
    nombre_usuario = Column(String(50), unique=True)
    clave_hash = Column(String(255))
    local_id = Column(Integer, ForeignKey("locales.id"))  # ✅
    
    # Relación
    local = relationship("Local", back_populates="usuarios")
```

### Local
```python
class Local(ModeloBase):
    __tablename__ = "locales"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))  # "REFACCIONARIA OVIEDO"
    
    # Relaciones
    usuarios = relationship("Usuario")
    ventas = relationship("Venta")
    cierres_caja = relationship("CierreCaja")
    arqueos = relationship("Arqueo")
```

### Venta
```python
class Venta(ModeloBase):
    __tablename__ = "ventas"
    
    folio = Column(String(20))
    fecha = Column(DateTime)
    local_id = Column(Integer, ForeignKey("locales.id"))  # ✅ NUEVO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    # ... otros campos
    
    local = relationship("Local", back_populates="ventas")
```

### CierreCaja
```python
class CierreCaja(ModeloBase):
    __tablename__ = "cierre_caja"
    
    folio = Column(String(20))
    local_id = Column(Integer, ForeignKey("locales.id"))  # ✅ YA EXISTE
    # ... otros campos
```

### Arqueo (si no existe)
```python
class Arqueo(ModeloBase):
    __tablename__ = "arqueos"
    
    folio = Column(String(20))
    fecha = Column(DateTime)
    local_id = Column(Integer, ForeignKey("locales.id"))  # ✅
    caja = Column(String(50))
    efectivo = Column(Float)
    # ... otros campos
```

## 🔗 ENDPOINTS API

### Login
```
POST /api/v1/auth/login
Body: { username, password }
Response: { access_token, user: { id, local_id, ... } }
```

### Ventas
```
GET /api/v1/ventas?local_id=1
POST /api/v1/ventas
Body: { folio, local_id, ... }  ← Incluir local_id
```

### Cierres
```
GET /api/v1/cajas/cierres?local_id=1
POST /api/v1/cajas/cierres
Body: { local_id, ... }
```

### Arqueos
```
GET /api/v1/arqueos?local_id=1
POST /api/v1/arqueos
Body: { local_id, caja, ... }
```

### Locales
```
GET /api/v1/locales/listar
Response: [{ id: 1, nombre: "REFACCIONARIA OVIEDO" }, ...]
```

## 📊 DATOS INICIALES (Insertar en BD)

```sql
-- Locales
INSERT INTO locales (id, nombre, direccion, telefono, email) VALUES
(1, 'REFACCIONARIA OVIEDO', 'Calle 1, #100', '5551234567', 'oviedo@refac.com'),
(2, 'REFACCIÓN PARA OVIEDO', 'Avenida 2, #200', '5559876543', 'paraoviedo@refac.com');

-- Usuarios (ejemplo)
INSERT INTO usuarios (id, nombre, nombre_usuario, clave_hash, local_id, rol) VALUES
(1, 'Juan Pérez', 'juan', 'hash...', 1, 'vendedor'),
(2, 'María García', 'maria', 'hash...', 2, 'vendedor'),
(3, 'Admin', 'admin', 'hash...', 1, 'administrador');

-- Productos (SIN local_id - compartidos)
INSERT INTO productos (id, clave, descripcion, precio) VALUES
(1, 'ACE001', 'Aceite de Motor 20W50', 250.00),
(2, 'BUJ001', 'Bujía NGK', 45.00);
```

## 🧪 TEST

### 1. Verificar que Usuario tiene local_id
```python
from app.models import Usuario
user = db.query(Usuario).first()
print(user.local_id)  # Debe ser 1 o 2
```

### 2. Verificar login retorna local_id
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"juan", "password":"pass"}'
  
# Response debe incluir:
# { "user": { "local_id": 1, ... } }
```

### 3. Verificar localStorage después de login
```javascript
// En la consola del navegador
console.log(JSON.parse(localStorage.user).local_id);
// Debe mostrar: 1 o 2
```

### 4. Verificar que selector carga sucursales
```javascript
// En la página nueva_venta.html
inicializarSelectorSucursal('sucursalSelect');
console.log(document.getElementById('sucursalSelect').options);
// Debe mostrar 2 opciones
```

## 🐛 TROUBLESHOOTING

### Problema: El selector no se carga
```
✓ Verificar: <script src="componentes/selector-sucursal.js"></script> existe
✓ Verificar: El archivo no tiene errores de sintaxis
✓ Verificar: El select tiene id="sucursalSelect" (o el id correcto)
```

### Problema: Nueva venta no guarda local_id
```
✓ Verificar: obtenerLocalIdSeleccionado() retorna número
✓ Verificar: El POST incluye local_id en los datos
✓ Verificar: Backend acepta local_id en POST /ventas
```

### Problema: Cierres no se filtran por sucursal
```
✓ Verificar: API retorna ?local_id en query string
✓ Verificar: Backend filtra CierreCaja.local_id == local_id
✓ Verificar: localStorage.user.local_id está correcto
```

### Problema: Usuario ve datos de ambas sucursales
```
✓ Verificar: localStorage.user.local_id es único por usuario
✓ Verificar: Backend filtra por local_id en TODOS los endpoints
✓ Verificar: No hay un "GET /api/v1/ventas" sin filtro
```

## ✅ CHECKLIST FINAL

- [ ] Modelos tienen local_id agregado
- [ ] Login retorna local_id en response
- [ ] localStorage.user contiene local_id
- [ ] Endpoints filtran por local_id
- [ ] nueva_venta.html carga selector
- [ ] nueva_venta.html guarda local_id
- [ ] cajas_cierre.html muestra dos tablas
- [ ] cajas_cierre.html selector cambia pestaña
- [ ] arqueos_caja.html carga locales
- [ ] Prueba: Crear venta en sucursal 1 → Verificar en listado
- [ ] Prueba: Cambiar a sucursal 2 → Ver datos diferentes

---

**¡Cuando todo esté ✅, tu sistema estará completamente funcional para 2 sucursales!**

Fecha: 26 de enero de 2026
