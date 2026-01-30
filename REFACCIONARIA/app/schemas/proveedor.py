from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProveedorBase(BaseModel):
    clave: str
    nombre: str
    rfc: Optional[str] = None
    web: Optional[str] = None

class ProveedorDireccion(BaseModel):
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    codigo_postal: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = "MEXICO"

class ProveedorCompras(BaseModel):
    contacto_compras_nombre: Optional[str] = None
    contacto_compras_email: Optional[str] = None
    contacto_compras_telefono: Optional[str] = None
    lista_precios_compra: Optional[str] = None
    dias_entrega: Optional[int] = 0
    tipo_moneda: Optional[str] = "pesos"

class ProveedorDescuentos(BaseModel):
    descuento_factura: Optional[Decimal] = 0
    descuento_listas_precio: Optional[Decimal] = 0
    descuento_producto_factura: Optional[Decimal] = 0
    notas_compras: Optional[str] = None

class ProveedorFinanzas(BaseModel):
    contacto_finanzas_nombre: Optional[str] = None
    contacto_finanzas_email: Optional[str] = None
    contacto_finanzas_telefono: Optional[str] = None
    forma_pago: Optional[str] = "contado"
    dias_credito: Optional[int] = 0
    saldo: Optional[Decimal] = 0

class ProveedorCreate(ProveedorBase, ProveedorDireccion, ProveedorCompras, ProveedorDescuentos, ProveedorFinanzas):
    activo: Optional[str] = "ACTIVO"

class ProveedorUpdate(BaseModel):
    clave: Optional[str] = None
    nombre: Optional[str] = None
    rfc: Optional[str] = None
    web: Optional[str] = None
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    codigo_postal: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    contacto_compras_nombre: Optional[str] = None
    contacto_compras_email: Optional[str] = None
    contacto_compras_telefono: Optional[str] = None
    lista_precios_compra: Optional[str] = None
    dias_entrega: Optional[int] = None
    tipo_moneda: Optional[str] = None
    descuento_factura: Optional[Decimal] = None
    descuento_listas_precio: Optional[Decimal] = None
    descuento_producto_factura: Optional[Decimal] = None
    notas_compras: Optional[str] = None
    contacto_finanzas_nombre: Optional[str] = None
    contacto_finanzas_email: Optional[str] = None
    contacto_finanzas_telefono: Optional[str] = None
    forma_pago: Optional[str] = None
    dias_credito: Optional[int] = None
    saldo: Optional[Decimal] = None
    activo: Optional[str] = None

class ProveedorResponse(ProveedorBase, ProveedorDireccion, ProveedorCompras, ProveedorDescuentos, ProveedorFinanzas):
    id: int
    activo: str
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
