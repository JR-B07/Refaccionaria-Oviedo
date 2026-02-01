from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models.producto import Producto

router = APIRouter()
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.models.producto import Producto

router = APIRouter()

# Endpoint para obtener un producto por id
@router.get("/{producto_id}", tags=["Productos"])
async def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "id": prod.id,
        "codigo": prod.codigo,
        "codigo_barras": prod.codigo_barras,
        "nombre": prod.nombre,
        "descripcion": prod.descripcion,
        "marca": prod.marca,
        "modelo": prod.modelo,
        "categoria": prod.categoria,
        "precio_compra": float(prod.precio_compra) if prod.precio_compra is not None else None,
        "precio_venta": float(prod.precio_venta) if prod.precio_venta is not None else None,
        "precio_venta_credito": float(prod.precio_venta_credito) if prod.precio_venta_credito is not None else None,
        "stock_minimo": prod.stock_minimo,
        "stock_total": prod.stock_total,
        "ubicacion_estante": prod.ubicacion_estante,
        "ubicacion_fila": prod.ubicacion_fila,
        "ubicacion_columna": prod.ubicacion_columna
    }
# Schema para editar producto
class ProductoUpdate(BaseModel):
    codigo: Optional[str] = None
    codigo_barras: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    categoria: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    precio_venta_credito: Optional[float] = None
    stock_minimo: Optional[int] = None
    stock_total: Optional[int] = None
    ubicacion_estante: Optional[str] = None
    ubicacion_fila: Optional[str] = None
    ubicacion_columna: Optional[str] = None

# Endpoint para editar producto
@router.put("/{producto_id}", tags=["Productos"])
async def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Actualizar solo los campos que fueron explícitamente enviados
    update_data = producto.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prod, field, value)
    
    db.commit()
    db.refresh(prod)
    return {"message": "Producto actualizado", "id": prod.id}



# Schema para crear producto
class ProductoCreate(BaseModel):
    codigo: str
    codigo_barras: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    categoria: Optional[str] = None
    precio_compra: float
    precio_venta: float
    precio_venta_credito: Optional[float] = None
    stock_minimo: Optional[int] = 5
    ubicacion_estante: Optional[str] = None
    ubicacion_fila: Optional[str] = None
    ubicacion_columna: Optional[str] = None


# Schema para editar producto
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    categoria: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    precio_venta_credito: Optional[float] = None
    stock_minimo: Optional[int] = None
    stock_total: Optional[int] = None
    ubicacion_estante: Optional[str] = None
    ubicacion_fila: Optional[str] = None
    ubicacion_columna: Optional[str] = None


# --- Listado de productos filtrado por sucursal del usuario autenticado ---
@router.get("/", tags=["Productos"])
async def listar_productos(
    q: Optional[str] = None,
    codigo: Optional[str] = None,
    marca: Optional[str] = None,
    categoria: Optional[str] = None,
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None,
    stock_minimo: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Listar todos los productos (sin autenticación)
    """
    try:
        query = db.query(Producto)
        
        # Búsqueda general
        if q:
            qlike = f"%{q}%"
            query = query.filter(
                (Producto.nombre.ilike(qlike)) |
                (Producto.codigo.ilike(qlike)) |
                (Producto.marca.ilike(qlike)) |
                (Producto.descripcion.ilike(qlike))
            )
        # Filtros específicos
        if codigo:
            query = query.filter(Producto.codigo.ilike(f"%{codigo}%"))
        if marca:
            mlike = f"%{marca}%"
            query = query.filter(
                or_(
                    Producto.marca.ilike(mlike),
                    Producto.nombre.ilike(mlike),
                    Producto.descripcion.ilike(mlike)
                )
            )
        if categoria:
            query = query.filter(Producto.categoria.ilike(f"%{categoria}%"))
        if precio_min is not None:
            query = query.filter(Producto.precio_venta >= precio_min)
        if precio_max is not None:
            query = query.filter(Producto.precio_venta <= precio_max)
        # Si quieres filtrar por stock_minimo, deberías unir con InventarioLocal aquí
        # pero para acceso público, lo omitimos o puedes ajustar según tu modelo
        
        total = query.count()
        items = query.offset(offset).limit(limit).all()

        result = []
        for p in items:
            result.append({
                "id": p.id,
                "codigo": p.codigo,
                "codigo_barras": p.codigo_barras,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "marca": p.marca,
                "modelo": p.modelo,
                "categoria": p.categoria,
                "precio_compra": float(p.precio_compra) if p.precio_compra is not None else None,
                "precio_venta": float(p.precio_venta) if p.precio_venta is not None else None,
                "stock_total": p.stock_total,
                # No mostramos stock_local porque no hay sucursal
            })

        return {"total": total, "items": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", tags=["Productos"])
async def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto."""
    try:
        # Verificar que el código no exista
        existe = db.query(Producto).filter(Producto.codigo == producto.codigo).first()
        if existe:
            raise HTTPException(status_code=400, detail=f"Ya existe un producto con el código '{producto.codigo}'")
        
        # Verificar código de barras si se proporciona
        if producto.codigo_barras:
            existe_cb = db.query(Producto).filter(Producto.codigo_barras == producto.codigo_barras).first()
            if existe_cb:
                raise HTTPException(status_code=400, detail=f"Ya existe un producto con el código de barras '{producto.codigo_barras}'")
        
        # Crear el producto
        nuevo_producto = Producto(
            codigo=producto.codigo,
            codigo_barras=producto.codigo_barras,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            marca=producto.marca,
            modelo=producto.modelo,
            categoria=producto.categoria,
            precio_compra=producto.precio_compra,
            precio_venta=producto.precio_venta,
            precio_venta_credito=producto.precio_venta_credito,
            stock_total=0,  # Inicia en 0
            stock_minimo=producto.stock_minimo or 5,
            ubicacion_estante=producto.ubicacion_estante,
            ubicacion_fila=producto.ubicacion_fila,
            ubicacion_columna=producto.ubicacion_columna
        )
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto)
        # Si no se proporcionó código de barras, lo generamos
        if not nuevo_producto.codigo_barras:
            nuevo_producto.codigo_barras = f"PROD-{nuevo_producto.id:06d}"
            db.commit()
            db.refresh(nuevo_producto)
        return {
            "message": "Producto creado exitosamente",
            "id": nuevo_producto.id,
            "codigo": nuevo_producto.codigo,
            "nombre": nuevo_producto.nombre,
            "codigo_barras": nuevo_producto.codigo_barras
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el producto: {str(e)}")


@router.get("/{producto_id}", tags=["Productos"])
async def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener un producto por su ID."""
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "id": prod.id,
        "codigo": prod.codigo,
        "codigo_barras": prod.codigo_barras,
        "nombre": prod.nombre,
        "descripcion": prod.descripcion,
        "marca": prod.marca,
        "modelo": prod.modelo,
        "categoria": prod.categoria,
        "precio_compra": float(prod.precio_compra) if prod.precio_compra is not None else None,
        "precio_venta": float(prod.precio_venta) if prod.precio_venta is not None else None,
        "stock_minimo": prod.stock_minimo,
        "stock_total": prod.stock_total,
        "ubicacion_estante": prod.ubicacion_estante,
        "ubicacion_fila": prod.ubicacion_fila,
        "ubicacion_columna": prod.ubicacion_columna
    }

@router.put("/{producto_id}", tags=["Productos"])
async def editar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    """Editar un producto existente."""
    try:
        prod = db.query(Producto).filter(Producto.id == producto_id).first()
        if not prod:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        for field, value in producto.dict(exclude_unset=True).items():
            setattr(prod, field, value)
        db.commit()
        db.refresh(prod)
        return {
            "message": "Producto editado exitosamente",
            "id": prod.id,
            "codigo": prod.codigo,
            "nombre": prod.nombre
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al editar el producto: {str(e)}")

