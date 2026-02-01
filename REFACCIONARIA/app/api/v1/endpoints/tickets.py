print("[DEBUG] Importando endpoints/tickets.py...")
# app/api/v1/endpoints/tickets.py
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.ticket import (
    TicketResponse,
    TicketCreate,
    TicketUpdate,
    TicketImpresion,
    EstatusTicket
)
from app.utils.ticket_printer import TicketPrinter

router = APIRouter()
print("[DEBUG] Router de tickets inicializado")

# ============= MODELOS =============
class ItemTicket(BaseModel):
    """Modelo para un item en el ticket"""
    descripcion: str
    cantidad: int = 1
    precio: float

class GenerarTicketRequest(BaseModel):
    """Solicitud para generar formato de ticket con promociones y políticas"""
    folio: str
    cliente: Optional[str] = None
    items: List[ItemTicket]
    subtotal: float
    descuento: float = 0.0
    impuesto: float = 0.0
    total: float
    vendedor: Optional[str] = None
    incluir_qr: bool = True

class GenerarTicketResponse(BaseModel):
    """Respuesta con el formato del ticket"""
    folio: str
    contenido_ticket: str
    exito: bool

# ============= DATOS =============
tickets_db = [
    {
        "id": 1,
        "folio": "VZ7314",
        "partidas": 3,
        "articulo": "Kit de frenos cerámicos",
        "cliente": "Refaccionaria Norte",
        "fecha": datetime(2026, 1, 7),
        "estatus": "Pendiente",
        "created_at": datetime(2026, 1, 7),
        "updated_at": None
    },
    {
        "id": 2,
        "folio": "VZ7315",
        "partidas": 2,
        "articulo": "Amortiguador delantero",
        "cliente": "Autoexpress Juárez",
        "fecha": datetime(2026, 1, 6),
        "estatus": "Parcial",
        "created_at": datetime(2026, 1, 6),
        "updated_at": None
    },
    {
        "id": 3,
        "folio": "VZ7316",
        "partidas": 1,
        "articulo": "Batería AGM 70Ah",
        "cliente": "Cliente mostrador",
        "fecha": datetime(2026, 1, 6),
        "estatus": "Pendiente",
        "created_at": datetime(2026, 1, 6),
        "updated_at": None
    },
    {
        "id": 4,
        "folio": "VZ7317",
        "partidas": 4,
        "articulo": "Juego de bujías iridio",
        "cliente": "Flotilla Gómez",
        "fecha": datetime(2026, 1, 5),
        "estatus": "Entregado",
        "created_at": datetime(2026, 1, 5),
        "updated_at": datetime(2026, 1, 6)
    }
]

@router.get("/", response_model=List[TicketResponse], tags=["Tickets"])
def listar_tickets(
    estatus: Optional[str] = None,
    buscar: Optional[str] = None
):
    """
    Obtiene lista de tickets pendientes.
    
    - **estatus**: Filtrar por estatus (Pendiente, Parcial, Entregado)
    - **buscar**: Buscar por folio, cliente o artículo
    """
    resultado = tickets_db.copy()
    
    # Filtrar por estatus
    if estatus:
        resultado = [t for t in resultado if t["estatus"] == estatus]
    
    # Filtrar por búsqueda
    if buscar:
        buscar_lower = buscar.lower()
        resultado = [
            t for t in resultado
            if buscar_lower in t["folio"].lower()
            or buscar_lower in t["cliente"].lower()
            or buscar_lower in t["articulo"].lower()
        ]
    
    return resultado

@router.post("/imprimir", response_model=TicketImpresion, tags=["Tickets"])
def imprimir_ticket(folio: str = Query(..., description="Folio del ticket a imprimir")):
    """
    Envía un ticket a la impresora.
    
    - **folio**: Folio del ticket a imprimir
    """
    ticket = next((t for t in tickets_db if t["folio"].upper() == folio.upper()), None)
    if not ticket:
        return TicketImpresion(
            folio=folio,
            exito=False,
            mensaje=f"Ticket {folio} no encontrado"
        )
    
    # Aquí iría la lógica real de impresión
    # Por ahora simulamos éxito
    return TicketImpresion(
        folio=folio,
        exito=True,
        mensaje=f"Ticket {folio} enviado a la impresora correctamente"
    )

# Endpoints específicos (van antes de genéricos)
@router.post("/generar-formato", response_model=GenerarTicketResponse, tags=["Tickets"])
def generar_formato_ticket(datos: GenerarTicketRequest):
    """
    Genera el formato completo del ticket con promociones y políticas de devolución.
    """
    try:
        # Convertir items a formato que TicketPrinter espera
        articulos = [
            {
                "descripcion": item.descripcion,
                "cantidad": item.cantidad,
                "precio": item.precio
            }
            for item in datos.items
        ]
        
        # Generar ticket con todas las secciones
        contenido = TicketPrinter.generate_venta_rapida_ticket(
            folio=datos.folio,
            items=articulos,
            subtotal=datos.subtotal,
            descuento=datos.descuento,
            total=datos.total,
            vendedor=datos.vendedor,
            fecha=datetime.now()
        )
        
        return GenerarTicketResponse(
            folio=datos.folio,
            contenido_ticket=contenido,
            exito=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al generar ticket: {str(e)}"
        )

@router.get("/diseño/promociones", tags=["Tickets"])
def obtener_promociones():
    """
    Obtiene la lista de promociones actuales que aparecen en los tickets.
    """
    return {
        "promociones": TicketPrinter.PROMOCIONES,
        "titulo": "Promociones:"
    }

@router.get("/diseño/politicas", tags=["Tickets"])
def obtener_politicas_devolucion():
    """
    Obtiene la lista de políticas de devolución que aparecen en los tickets.
    """
    return {
        "politicas": TicketPrinter.POLITICAS_DEVOLUCION,
        "titulo": "Políticas de devolución:"
    }

# Endpoints genéricos (van después de específicos)
@router.post("/crear", response_model=TicketResponse, status_code=status.HTTP_201_CREATED, tags=["Tickets"])
def crear_ticket(ticket: TicketCreate):
    """Crea un nuevo ticket."""
    # Verificar que el folio no exista
    if any(t["folio"].upper() == ticket.folio.upper() for t in tickets_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un ticket con el folio {ticket.folio}"
        )
    
    nuevo_id = max([t["id"] for t in tickets_db], default=0) + 1
    nuevo_ticket = {
        "id": nuevo_id,
        "folio": ticket.folio,
        "partidas": ticket.partidas,
        "articulo": ticket.articulo,
        "cliente": ticket.cliente,
        "fecha": ticket.fecha,
        "estatus": ticket.estatus,
        "created_at": datetime.now(),
        "updated_at": None
    }
    
    tickets_db.append(nuevo_ticket)
    return nuevo_ticket

@router.patch("/{folio}", response_model=TicketResponse, tags=["Tickets"])
def actualizar_ticket(folio: str, datos: TicketUpdate):
    """
    Actualiza el estatus u otros datos de un ticket.
    
    - **folio**: Folio del ticket
    - **datos**: Datos a actualizar (estatus, partidas, artículo)
    """
    ticket = next((t for t in tickets_db if t["folio"].upper() == folio.upper()), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {folio} no encontrado"
        )
    
    # Actualizar campos proporcionados
    if datos.estatus is not None:
        ticket["estatus"] = datos.estatus
    if datos.partidas is not None:
        ticket["partidas"] = datos.partidas
    if datos.articulo is not None:
        ticket["articulo"] = datos.articulo
    
    ticket["updated_at"] = datetime.now()
    
    return ticket

@router.post("/{folio}/entregar", response_model=TicketResponse, tags=["Tickets"])
def marcar_entregado(folio: str):
    """
    Marca un ticket como entregado.
    
    - **folio**: Folio del ticket a marcar como entregado
    """
    ticket = next((t for t in tickets_db if t["folio"].upper() == folio.upper()), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {folio} no encontrado"
        )
    
    ticket["estatus"] = "Entregado"
    ticket["updated_at"] = datetime.now()
    
    return ticket

@router.get("/{folio}/obtener-formato", tags=["Tickets"])
def obtener_formato_ticket(folio: str):
    """
    Obtiene el formato formateado de un ticket existente.
    
    - **folio**: Folio del ticket
    """
    ticket = next((t for t in tickets_db if t["folio"].upper() == folio.upper()), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket con folio {folio} no encontrado"
        )
    
    # Generar formato del ticket
    contenido = TicketPrinter.generate_ticket(
        folio=ticket["folio"],
        cliente=ticket.get("cliente", ""),
        articulos=[
            {
                "nombre": ticket["articulo"],
                "cantidad": ticket["partidas"],
                "precio": 0.0  # Estos datos deberían venir de la base de datos
            }
        ],
        subtotal=0.0,
        fecha=ticket["fecha"]
    )
    
    return GenerarTicketResponse(
        folio=folio,
        contenido_ticket=contenido,
        exito=True
    )

@router.get("/{folio}", response_model=TicketResponse, tags=["Tickets"])
def obtener_ticket(folio: str):
    """Obtiene un ticket específico por folio."""
    ticket = next((t for t in tickets_db if t["folio"].upper() == folio.upper()), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket con folio {folio} no encontrado"
        )
    return ticket
