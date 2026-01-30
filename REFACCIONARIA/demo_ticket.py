#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script rápido para demostrar ticket completo
"""

from app.utils.ticket_printer import TicketPrinter

items = [
    {'descripcion': 'Kit frenos cerámicos', 'cantidad': 1, 'precio': 850},
    {'descripcion': 'Aceite sintético 5W-30', 'cantidad': 2, 'precio': 320},
    {'descripcion': 'Filtro aire', 'cantidad': 1, 'precio': 180},
]

ticket = TicketPrinter.generate_venta_rapida_ticket(
    folio='VZ0001',
    items=items,
    subtotal=1670,
    descuento=100,
    total=1570,
    vendedor='Juan Pérez'
)

print(ticket)
