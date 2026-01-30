from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.paquete import Paquete, PaqueteProducto
from app.models.producto import Producto
from app.schemas.paquete import (
    PaqueteCreate, PaqueteUpdate,
    PaqueteItemCreate, PaqueteItemUpdate
)

router = APIRouter(prefix="/paquetes", tags=["Paquetes (Kits)"])

@router.get("/")
async def listar_paquetes(
    q: Optional[str] = None,
    clase: Optional[str] = None,
    activo: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Paquete)
        if q:
            qlike = f"%{q}%"
            query = query.filter((Paquete.nombre.ilike(qlike)) | (Paquete.descripcion.ilike(qlike)))
        if clase:
            query = query.filter(Paquete.clase.ilike(f"%{clase}%"))
        if activo is not None:
            query = query.filter(Paquete.activo == activo)

        total = query.count()
        paquetes = query.offset(offset).limit(limit).all()

        items = []
        for p in paquetes:
            precio_total = 0.0
            for it in p.items:
                precio_total += float(it.total or 0)
            items.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "clase": p.clase,
                "activo": p.activo,
                "total_items": len(p.items),
                "precio_total": round(precio_total, 2)
            })
        return {"total": total, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{paquete_id}")
async def detalle_paquete(paquete_id: int, db: Session = Depends(get_db)):
    p = db.query(Paquete).filter(Paquete.id == paquete_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    precio_total = 0.0
    items = []
    for it in p.items:
        precio_total += float(it.total or 0)
        items.append({
            "id": it.id,
            "producto_id": it.producto_id,
            "codigo": it.producto.codigo,
            "nombre": it.producto.nombre,
            "cantidad": it.cantidad,
            "precio_unitario": float(it.precio_unitario or 0),
            "total": float(it.total or 0)
        })
    return {
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "clase": p.clase,
        "activo": p.activo,
        "precio_total": round(precio_total, 2),
        "items": items
    }

@router.post("/")
async def crear_paquete(data: PaqueteCreate, db: Session = Depends(get_db)):
    try:
        nuevo = Paquete(
            nombre=data.nombre,
            descripcion=data.descripcion,
            clase=data.clase,
            activo=data.activo if data.activo is not None else True
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {"message": "Paquete creado", "id": nuevo.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{paquete_id}")
async def actualizar_paquete(paquete_id: int, data: PaqueteUpdate, db: Session = Depends(get_db)):
    p = db.query(Paquete).filter(Paquete.id == paquete_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    try:
        if data.nombre is not None:
            p.nombre = data.nombre
        if data.descripcion is not None:
            p.descripcion = data.descripcion
        if data.clase is not None:
            p.clase = data.clase
        if data.activo is not None:
            p.activo = data.activo
        db.commit()
        db.refresh(p)
        return {"message": "Paquete actualizado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{paquete_id}")
async def eliminar_paquete(paquete_id: int, db: Session = Depends(get_db)):
    p = db.query(Paquete).filter(Paquete.id == paquete_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    try:
        db.delete(p)
        db.commit()
        return {"message": "Paquete eliminado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{paquete_id}/items")
async def agregar_item(paquete_id: int, data: PaqueteItemCreate, db: Session = Depends(get_db)):
    p = db.query(Paquete).filter(Paquete.id == paquete_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    prod = db.query(Producto).filter(Producto.id == data.producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    try:
        total = (data.cantidad or 1) * float(data.precio_unitario)
        item = PaqueteProducto(
            paquete_id=p.id,
            producto_id=prod.id,
            cantidad=data.cantidad,
            precio_unitario=data.precio_unitario,
            total=total
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return {"message": "Producto agregado al paquete", "item_id": item.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{paquete_id}/items/{item_id}")
async def actualizar_item(paquete_id: int, item_id: int, data: PaqueteItemUpdate, db: Session = Depends(get_db)):
    item = db.query(PaqueteProducto).filter(
        PaqueteProducto.id == item_id,
        PaqueteProducto.paquete_id == paquete_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    try:
        if data.cantidad is not None:
            item.cantidad = data.cantidad
        if data.precio_unitario is not None:
            item.precio_unitario = data.precio_unitario
        # Recalcular
        item.total = float(item.cantidad) * float(item.precio_unitario)
        db.commit()
        db.refresh(item)
        return {"message": "Item actualizado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{paquete_id}/items/{item_id}")
async def eliminar_item(paquete_id: int, item_id: int, db: Session = Depends(get_db)):
    item = db.query(PaqueteProducto).filter(
        PaqueteProducto.id == item_id,
        PaqueteProducto.paquete_id == paquete_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    try:
        db.delete(item)
        db.commit()
        return {"message": "Item eliminado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
