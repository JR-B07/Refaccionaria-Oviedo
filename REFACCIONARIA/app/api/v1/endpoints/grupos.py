from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.grupo import Grupo, GrupoProducto, GrupoAplicacion
from app.models.producto import Producto
from app.schemas.grupo import (
    GrupoCreate, GrupoUpdate,
    GrupoProductoCreate, GrupoProductoUpdate,
    GrupoAplicacionCreate, GrupoAplicacionUpdate
)


router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.get("/")
async def listar_grupos(
    q: Optional[str] = None,
    activo: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Grupo)
        if q:
            qlike = f"%{q}%"
            query = query.filter((Grupo.nombre.ilike(qlike)) | (Grupo.descripcion.ilike(qlike)))
        if activo is not None:
            query = query.filter(Grupo.activo == activo)

        total = query.count()
        grupos = query.offset(offset).limit(limit).all()
        items = [
            {
                "id": g.id,
                "nombre": g.nombre,
                "tipo": g.tipo,
                "descripcion": g.descripcion,
                "activo": g.activo,
            }
            for g in grupos
        ]
        return {"total": total, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{grupo_id}")
async def detalle_grupo(grupo_id: int, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return {
        "id": g.id,
        "nombre": g.nombre,
        "tipo": g.tipo,
        "descripcion": g.descripcion,
        "activo": g.activo,
    }


@router.post("/")
async def crear_grupo(data: GrupoCreate, db: Session = Depends(get_db)):
    try:
        nuevo = Grupo(
            nombre=data.nombre,
            tipo=data.tipo,
            descripcion=data.descripcion,
            activo=data.activo if data.activo is not None else True,
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {"message": "Grupo creado", "id": nuevo.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{grupo_id}")
async def actualizar_grupo(grupo_id: int, data: GrupoUpdate, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    try:
        if data.nombre is not None:
            g.nombre = data.nombre
        if data.tipo is not None:
            g.tipo = data.tipo
        if data.descripcion is not None:
            g.descripcion = data.descripcion
        if data.activo is not None:
            g.activo = data.activo
        db.commit()
        db.refresh(g)
        return {"message": "Grupo actualizado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{grupo_id}")
async def eliminar_grupo(grupo_id: int, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    try:
        db.delete(g)
        db.commit()
        return {"message": "Grupo eliminado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ===== Productos del Grupo =====
@router.get("/{grupo_id}/productos")
async def listar_productos_grupo(grupo_id: int, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    items = []
    for gp in g.productos_rel:
        prod = db.query(Producto).filter(Producto.id == gp.producto_id).first()
        items.append({
            "id": gp.id,
            "producto_id": gp.producto_id,
            "linea": gp.linea,
            "marca": prod.marca if prod else None,
            "caracteristica1": gp.caracteristica1,
            "caracteristica2": gp.caracteristica2,
            "clave": gp.clave or (prod.codigo if prod else None),
            "codigo": prod.codigo if prod else None,
            "nombre": prod.nombre if prod else None,
        })
    return {"total": len(items), "items": items}


@router.post("/{grupo_id}/productos")
async def agregar_producto_grupo(grupo_id: int, data: GrupoProductoCreate, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    prod = db.query(Producto).filter(Producto.id == data.producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    try:
        gp = GrupoProducto(
            grupo_id=g.id,
            producto_id=prod.id,
            linea=data.linea,
            caracteristica1=data.caracteristica1,
            caracteristica2=data.caracteristica2,
            clave=data.clave or prod.codigo
        )
        db.add(gp)
        db.commit()
        db.refresh(gp)
        return {"message": "Producto vinculado al grupo", "id": gp.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{grupo_id}/productos/{gp_id}")
async def actualizar_producto_grupo(grupo_id: int, gp_id: int, data: GrupoProductoUpdate, db: Session = Depends(get_db)):
    gp = db.query(GrupoProducto).filter(GrupoProducto.id == gp_id, GrupoProducto.grupo_id == grupo_id).first()
    if not gp:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    try:
        if data.linea is not None:
            gp.linea = data.linea
        if data.caracteristica1 is not None:
            gp.caracteristica1 = data.caracteristica1
        if data.caracteristica2 is not None:
            gp.caracteristica2 = data.caracteristica2
        if data.clave is not None:
            gp.clave = data.clave
        db.commit()
        db.refresh(gp)
        return {"message": "Relación actualizada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{grupo_id}/productos/{gp_id}")
async def eliminar_producto_grupo(grupo_id: int, gp_id: int, db: Session = Depends(get_db)):
    gp = db.query(GrupoProducto).filter(GrupoProducto.id == gp_id, GrupoProducto.grupo_id == grupo_id).first()
    if not gp:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    try:
        db.delete(gp)
        db.commit()
        return {"message": "Relación eliminada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ===== Aplicaciones del Grupo =====
@router.get("/{grupo_id}/aplicaciones")
async def listar_aplicaciones_grupo(grupo_id: int, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    items = [
        {
            "id": a.id,
            "marca": a.marca,
            "modelo": a.modelo,
            "motor": a.motor,
            "desde": a.desde,
            "hasta": a.hasta,
        }
        for a in g.aplicaciones
    ]
    return {"total": len(items), "items": items}


@router.post("/{grupo_id}/aplicaciones")
async def agregar_aplicacion_grupo(grupo_id: int, data: GrupoAplicacionCreate, db: Session = Depends(get_db)):
    g = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    try:
        a = GrupoAplicacion(
            grupo_id=g.id,
            marca=data.marca,
            modelo=data.modelo,
            motor=data.motor,
            desde=data.desde,
            hasta=data.hasta,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        return {"message": "Aplicación agregada", "id": a.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{grupo_id}/aplicaciones/{app_id}")
async def actualizar_aplicacion_grupo(grupo_id: int, app_id: int, data: GrupoAplicacionUpdate, db: Session = Depends(get_db)):
    a = db.query(GrupoAplicacion).filter(GrupoAplicacion.id == app_id, GrupoAplicacion.grupo_id == grupo_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Aplicación no encontrada")
    try:
        if data.marca is not None:
            a.marca = data.marca
        if data.modelo is not None:
            a.modelo = data.modelo
        if data.motor is not None:
            a.motor = data.motor
        if data.desde is not None:
            a.desde = data.desde
        if data.hasta is not None:
            a.hasta = data.hasta
        db.commit()
        db.refresh(a)
        return {"message": "Aplicación actualizada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{grupo_id}/aplicaciones/{app_id}")
async def eliminar_aplicacion_grupo(grupo_id: int, app_id: int, db: Session = Depends(get_db)):
    a = db.query(GrupoAplicacion).filter(GrupoAplicacion.id == app_id, GrupoAplicacion.grupo_id == grupo_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Aplicación no encontrada")
    try:
        db.delete(a)
        db.commit()
        return {"message": "Aplicación eliminada"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
