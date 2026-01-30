from typing import Optional
from datetime import datetime, date, time

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.asistencia import AsistenciaEmpleado

router = APIRouter()


class RegistroEntrada(BaseModel):
    nombre: str
    sucursal: str
    accion: str = Field(pattern=r"^(Entrada|Comida|Regreso|Salida)$")
    fecha: Optional[date] = None
    hora: Optional[str] = None  # HH:MM


@router.get("/asistencia")
def listar_asistencia(
    sucursal: Optional[str] = Query(None),
    nombre: Optional[str] = Query(None),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    """Devuelve registros de asistencia desde la BD."""
    q = db.query(AsistenciaEmpleado)
    if sucursal:
        q = q.filter(AsistenciaEmpleado.sucursal.ilike(f"%{sucursal}%"))
    if nombre:
        q = q.filter(AsistenciaEmpleado.nombre.ilike(f"%{nombre}%"))
    if fecha_inicio:
        q = q.filter(AsistenciaEmpleado.fecha >= fecha_inicio)
    if fecha_fin:
        q = q.filter(AsistenciaEmpleado.fecha <= fecha_fin)

    q = q.order_by(AsistenciaEmpleado.nombre.asc(), AsistenciaEmpleado.fecha.asc())
    rows = q.all()
    registros = [
        {
            "nombre": r.nombre,
            "sucursal": r.sucursal,
            "fecha": r.fecha.isoformat(),
            "entrada": r.entrada.strftime("%H:%M") if r.entrada else None,
            "comida": r.comida.strftime("%H:%M") if r.comida else None,
            "regreso": r.regreso.strftime("%H:%M") if r.regreso else None,
            "salida": r.salida.strftime("%H:%M") if r.salida else None,
        }
        for r in rows
    ]
    return {"count": len(registros), "data": registros}


@router.post("/asistencia/registrar")
def registrar_asistencia(payload: RegistroEntrada, db: Session = Depends(get_db)):
    """Registra o actualiza un marcaje para `nombre` y `fecha` usando BD."""
    hoy = payload.fecha or date.today()
    h = payload.hora or datetime.now().strftime("%H:%M")
    # convertir a tipo time
    hh, mm = h.split(":")
    hora_t = time(int(hh), int(mm))

    campo = {
        "Entrada": "entrada",
        "Comida": "comida",
        "Regreso": "regreso",
        "Salida": "salida",
    }[payload.accion]

    row = (
        db.query(AsistenciaEmpleado)
        .filter(AsistenciaEmpleado.nombre == payload.nombre)
        .filter(AsistenciaEmpleado.fecha == hoy)
        .first()
    )

    if not row:
        row = AsistenciaEmpleado(
            nombre=payload.nombre,
            sucursal=payload.sucursal,
            fecha=hoy,
        )
        setattr(row, campo, hora_t)
        db.add(row)
        estado = "creado"
    else:
        setattr(row, campo, hora_t)
        row.sucursal = payload.sucursal or row.sucursal
        estado = "actualizado"

    db.commit()
    db.refresh(row)
    return {
        "ok": True,
        "estado": estado,
        "registro": {
            "nombre": row.nombre,
            "sucursal": row.sucursal,
            "fecha": row.fecha.isoformat(),
            "entrada": row.entrada.strftime("%H:%M") if row.entrada else None,
            "comida": row.comida.strftime("%H:%M") if row.comida else None,
            "regreso": row.regreso.strftime("%H:%M") if row.regreso else None,
            "salida": row.salida.strftime("%H:%M") if row.salida else None,
        },
    }
