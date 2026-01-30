"""
Utilidad para generar tickets/recibos formateados para impresora térmica
"""
from datetime import datetime
from typing import List, Dict, Optional

# Intentar importar qrcode si está disponible
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

class TicketPrinter:

    @classmethod
    def generate_header(cls) -> str:
        # Encabezado similar al ejemplo de la imagen
        header = [
            cls.center_text("REFACCIONARIA OVIEDO"),
            cls.center_text("LIBRAMIENTO SUR #171-B"),
            cls.center_text("COL MAGISTERIAL CP 37900"),
            cls.center_text("SAN LUIS DE LA PAZ, GTO."),
            cls.center_text("WhatsApp: 468 113 2367"),
            cls.line_separator("-")
        ]
        return "\n".join(header)

    @classmethod
    def generate_promociones(cls) -> str:
        promo = cls.get_promocion_aleatoria_from_db()
        if promo:
            lines = [cls.line_separator("-"), cls.center_text("Promociones:")]
            for linea in cls.wrap_text(promo, cls.TICKET_WIDTH):
                lines.append(cls.center_text(linea))
            return "\n".join(lines)
        return ""

    @classmethod
    def generate_politicas(cls) -> str:
        politicas = [cls.line_separator("-"), cls.center_text("POLITICAS DE DEVOLUCION")]
        for politica in cls.POLITICAS_DEVOLUCION:
            politicas.append(cls.center_text(politica))
        politicas.append(cls.line_separator("-"))
        return "\n".join(politicas)
    @staticmethod
    def center_text(text: str, width: int = 40) -> str:
        if not text:
            return ""
        return text.center(width)

    @staticmethod
    def line_separator(char: str = "-", width: int = 40) -> str:
        return char * width

    @staticmethod
    def wrap_text(text: str, width: int = 40) -> list:
        # Divide el texto en líneas de máximo 'width' caracteres
        if not text:
            return []
        words = text.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 > width:
                lines.append(current)
                current = word
            else:
                if current:
                    current += " "
                current += word
        if current:
            lines.append(current)
        return lines
    @staticmethod
    def get_promocion_aleatoria_from_db() -> str:
        """Obtiene una promoción activa aleatoria desde la base de datos."""
        try:
            from app.models.promocion import Promocion
            from app.core.database import SessionLocal
            import random
            db = SessionLocal()
            promos = db.query(Promocion).filter(Promocion.activa == True).all()
            db.close()
            if promos:
                return random.choice(promos).descripcion
            return None
        except Exception as e:
            return None

    # Generador de tickets para impresora térmica (80mm)
    TICKET_WIDTH = 40
    EMPRESA_NOMBRE = "REFACCIONARIA"
    EMPRESA_SLOGAN = "OVIEDO"
    EMPRESA_LEMA = "NUESTRA EXPERIENCIA MARCA LA DIFERENCIA"
    POLITICAS_DEVOLUCION = [
        "A) EL PRODUCTO DEBE SER DEVUELTO",
        "   EN UN PERIODO DE 30 DIAS",
        "",
        "B) LAS PARTES ELECTRICAS SERÁN",
        "   REVISADAS POR UN ESPECIALISTA Y",
        "   SU DEVOLUCIÓN DEPENDERÁ DE SU",
        "   DIAGNOSTICO FINAL",
        "",
        "C) AL NO SER FABRICANTES",
        "   DEPENDEMOS DE LAS POLÍTICAS DE",
        "   ELLOS PARA PODER EMITIR UNA",
        "   RESOLUCIÓN DE GARANTÍA, GRACIAS",
        "   POR SU COMPRENSIÓN"
    ]

    @classmethod
    def generate_venta_rapida_ticket(
        cls,
        folio: str,
        items: List[Dict],
        subtotal: float,
        descuento: float,
        total: float,
        efectivo: float = 0.0,
        cambio: float = 0.0,
        fecha: Optional[datetime] = None,
        vendedor: Optional[str] = None,
        cliente: str = "PÚBLICO GENERAL",
        rfc: str = "PÚBLICO GENERAL"
    ) -> str:
        if fecha is None:
            fecha = datetime.now()
        lines = []
        # Logo y encabezado
        logo_ascii = [
            "      _______   _______   _______   ",
            "     /       \\ /       \\ /       \\  ",
            "    |  ( )  | |  ( )  | |  ( )  |  ",
            "    |_______| |_______| |_______|  ",
            "   REFACCIONARIA OVIEDO           "
        ]
        for l in logo_ascii:
            lines.append(cls.center_text(l))
        lines.append("")
        lines.append(cls.center_text("REFACCIONARIA OVIEDO"))
        lines.append(cls.center_text("LIBRAMIENTO SUR #171-B"))
        # Marca visual para verificar salto de línea
        lines.append(cls.center_text("--- AQUI TERMINA LINEA 1 ---"))
        lines.append(cls.center_text("COL MAGISTERIAL CP 37900"))
        lines.append(cls.center_text("SAN LUIS DE LA PAZ, GTO."))
        lines.append(cls.center_text("--- AQUI TERMINA LINEA 2 ---"))
        lines.append(cls.center_text("WhatsApp: 468 113 2367"))
        lines.append(cls.line_separator("-"))
        lines.append("")
        lines.append(cls.center_text("COMPROBANTE DE VENTA"))
        lines.append("")
        lines.append(f"Cliente: {cliente}")
        lines.append(f"RFC: {rfc}")
        lines.append("")
        lines.append(f"Folio: {folio}")
        lines.append(f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M:%S')} (TS: {datetime.now().strftime('%H:%M:%S')})")
        if vendedor:
            lines.append(f"Vendedor: {vendedor}")
        lines.append(cls.line_separator("-"))
        # Artículos
        lines.append(cls.center_text("ARTICULOS"))
        lines.append("{:<20} {:>4} {:>9} {:>9}".format("", "Cant", "Precio U.", "Total"))
        for item in items:
            desc = item.get("descripcion", "")[:20]
            cant = str(item.get("cantidad", 1))
            precio = f"${item.get('precio', 0.0):.2f}"
            monto = item.get("cantidad", 1) * item.get("precio", 0.0)
            total_item = f"${monto:.2f}"
            lines.append("{:<20} {:>4} {:>9} {:>9}".format(desc, cant, precio, total_item))
            lines.append(cls.line_separator("-"))
            # Totales alineados a la derecha
            lines.append(f"{'Subtotal:':<12}{'':>10}${subtotal:>8.2f}")
            lines.append(f"{'Descuento:':<12}{'':>10}${descuento:>8.2f}")
            lines.append(f"{'Subtotal:':<12}{'':>10}${subtotal:>8.2f}")
            iva = total - subtotal + descuento
            lines.append(f"{'IVA:':<12}{'':>10}${iva:>8.2f}")
            lines.append(cls.line_separator("-"))
            lines.append(f"{'TOTAL:':<12}{'':>10}${total:>8.2f}")
            lines.append(cls.line_separator("-"))
            # Formas de pago
            if efectivo > 0:
                lines.append(f"{'EFECTIVO:':<12}{'':>10}${efectivo:>8.2f}")
                if cambio > 0:
                    lines.append(f"{'CAMBIO:':<12}{'':>10}${cambio:>8.2f}")
            else:
                lines.append(f"{'Formas de Pago:':<12}{'':>10}")
                lines.append(f"{'TARJETA:':<12}{'':>10}${total:>8.2f}")
            lines.append(cls.line_separator("-"))
            # Mensaje de facturación
            lines.append("")
            lines.append(cls.center_text("SOLICITE SU FACTURA UNICAMENTE EN EL TRANSCURSO DEL MES DE EMISIÓN DE ÉSTE TICKET"))
            lines.append(cls.center_text(f"Vendedor: {vendedor}" if vendedor else ""))
            lines.append(cls.line_separator("-"))
            # Lema
            lines.append(cls.center_text(f'"{cls.EMPRESA_LEMA}"'))
            # Promociones
            promo = cls.get_promocion_aleatoria_from_db()
            if promo:
                lines.append(cls.line_separator("-"))
                lines.append(cls.center_text("Promociones:"))
                for linea in cls.wrap_text(promo, cls.TICKET_WIDTH):
                    lines.append(cls.center_text(linea))
            # Políticas de devolución
            lines.append(cls.line_separator("-"))
            lines.append(cls.center_text("POLITICAS DE DEVOLUCION"))
            for politica in cls.POLITICAS_DEVOLUCION:
                lines.append(cls.center_text(politica))
            lines.append(cls.line_separator("-"))
            # Pie de página
            lines.append("")
            lines.append(cls.center_text("¡GRACIAS POR SU COMPRA!"))
            lines.append("")
            return "\n".join(lines)
        lines.append(f"{'Descuento:':<15} ${descuento:>8.2f}")
        lines.append(f"{'Subtotal:':<15} ${subtotal:>8.2f}")
        iva = total - subtotal + descuento
        lines.append(f"{'IVA:':<15} ${iva:>8.2f}")
        lines.append("")
        lines.append(f"{'TOTAL:':<15} ${total:>8.2f}")
        lines.append(cls.line_separator("-"))
        # Formas de pago
        if efectivo > 0:
            lines.append(f"{'EFECTIVO:':<15} ${efectivo:>8.2f}")
            if cambio > 0:
                lines.append(f"{'CAMBIO:':<15} ${cambio:>8.2f}")
        else:
            lines.append(f"{'Formas de Pago:':<15}")
            lines.append(f"{'TARJETA:':<10} ${total:>8.2f}")
        lines.append(cls.line_separator("-"))
        # Mensaje de facturación
        lines.append("")
        lines.append(cls.center_text("SOLICITE SU FACTURA UNICAMENTE EN EL TRANSCURSO DEL"))
        lines.append(cls.center_text("MES DE EMISIÓN DE ÉSTE TICKET"))
        if vendedor:
            lines.append(f"Vendedor: {vendedor}")
        # Logo
        logo_ascii = [
            "      _______   _______   _______   ",
            "     /       \ /       \ /       \  ",
            "    |  ( )  | |  ( )  | |  ( )  |  ",
            "    |_______| |_______| |_______|  ",
            "   REFACCIONARIA OVIEDO           "
        ]
        for l in logo_ascii:
            lines.append(cls.center_text(l))
        lines.append("")
        lines.append(cls.center_text(f'"{cls.EMPRESA_LEMA}"'))
        # Promociones
        promo = cls.get_promocion_aleatoria_from_db()
        if promo:
            lines.append(cls.line_separator("-"))
            lines.append(cls.center_text("Promociones:"))
            for linea in cls.wrap_text(promo, cls.TICKET_WIDTH):
                lines.append(cls.center_text(linea))
        # Políticas de devolución
        lines.append(cls.line_separator("-"))
        lines.append(cls.center_text("POLITICAS DE DEVOLUCION"))
        for politica in cls.POLITICAS_DEVOLUCION:
            lines.append(cls.center_text(politica))
        lines.append(cls.line_separator("-"))
        # Pie de página
        lines.append("")
        lines.append(cls.center_text("¡GRACIAS POR SU COMPRA!"))
        lines.append("")
        return "\n".join(lines)
        
        # Detalles de artículos
        lines.append("")
        lines.append("ARTÍCULOS")
        lines.append(cls.line_separator("-"))
        
        for articulo in articulos:
            nombre = articulo.get("nombre", "")[:37]
            cantidad = articulo.get("cantidad", 1)
            precio = articulo.get("precio", 0.0)
            monto = cantidad * precio
            
            lines.append(f"{nombre}")
            lines.append(f"  {cantidad}x ${precio:.2f} = ${monto:.2f}")
        
        lines.append(cls.line_separator("-"))
        
        # Totales
        lines.append("")
        subtotal_str = f"Subtotal: ${subtotal:.2f}"
        lines.append(subtotal_str.rjust(cls.TICKET_WIDTH))
        
        if descuento > 0:
            descuento_str = f"Descuento: -${descuento:.2f}"
            lines.append(descuento_str.rjust(cls.TICKET_WIDTH))
        
        if impuesto > 0:
            impuesto_str = f"IVA: ${impuesto:.2f}"
            lines.append(impuesto_str.rjust(cls.TICKET_WIDTH))
        
        lines.append(cls.line_separator("="))
        total_str = f"TOTAL: ${total:.2f}"
        lines.append(cls.center_text(total_str))
        lines.append(cls.line_separator("="))
        
        # Promociones
        lines.append(cls.generate_promociones())
        
        # Políticas de devolución
        lines.append(cls.generate_politicas())
        
        # QR Code
        if incluir_qr:
            lines.append("")
            lines.append(cls.center_text("[Código QR]"))
            lines.append(cls.center_text(f"Folio: {folio}"))
        
        # Pie de página
        lines.append("")
        lines.append("")
        lines.append(cls.center_text("¡GRACIAS POR SU COMPRA!"))
        lines.append("")
        
        return "\n".join(lines)
    
    @classmethod
    def generate_venta_rapida_ticket(
        cls,
        folio: str,
        items: List[Dict],  # [{"descripcion": str, "cantidad": int, "precio": float}, ...]
        subtotal: float,
        descuento: float,
        total: float,
        efectivo: float = 0.0,
        cambio: float = 0.0,
        fecha: Optional[datetime] = None,
        vendedor: Optional[str] = None
    ) -> str:
        """
        Genera un ticket para venta rápida (punto de venta)
        
        Args:
            folio: Número de folio
            items: Lista de items vendidos
            subtotal: Subtotal
            descuento: Descuento
            total: Total a pagar
            efectivo: Cantidad en efectivo recibida
            cambio: Cambio a devolver
            fecha: Fecha del ticket
            vendedor: Vendedor que realizó la venta
        
        Returns:
            String con el formato del ticket
        """
        if fecha is None:
            fecha = datetime.now()
        
        lines = []
        
        # Encabezado
        lines.append(cls.generate_header())
        
        # Información básica
        lines.append("")
        lines.append(f"Folio: {folio}")
        lines.append(f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M:%S')}")
        if vendedor:
            lines.append(f"Vendedor: {vendedor}")
        lines.append(cls.line_separator())
        
        # Detalles de items
        lines.append("")
        lines.append("DESCRIPCIÓN          CANT   PRECIO   TOTAL")
        lines.append(cls.line_separator("-"))
        
        for item in items:
            desc = item.get("descripcion", "")[:20].ljust(20)
            cant = str(item.get("cantidad", 1)).rjust(4)
            precio = f"${item.get('precio', 0.0):>6.2f}"
            monto = item.get("cantidad", 1) * item.get("precio", 0.0)
            total_item = f"${monto:>6.2f}"
            
            lines.append(f"{desc} {cant} {precio} {total_item}")
        
        lines.append(cls.line_separator("-"))
        
        # Totales
        lines.append("")
        lines.append(f"Subtotal:            ${subtotal:>10.2f}".rjust(cls.TICKET_WIDTH))
        if descuento > 0:
            lines.append(f"Descuento:          -${descuento:>10.2f}".rjust(cls.TICKET_WIDTH))
        lines.append(cls.line_separator("="))
        lines.append(f"TOTAL:               ${total:>10.2f}".rjust(cls.TICKET_WIDTH))
        lines.append(cls.line_separator("="))
        
        # Pago
        if efectivo > 0:
            lines.append("")
            lines.append(f"Efectivo:            ${efectivo:>10.2f}".rjust(cls.TICKET_WIDTH))
            if cambio > 0:
                lines.append(f"Cambio:              ${cambio:>10.2f}".rjust(cls.TICKET_WIDTH))
        
        # Promociones
        lines.append(cls.generate_promociones())
        
        # Políticas de devolución
        lines.append(cls.generate_politicas())
        
        # Pie de página
        lines.append("")
        lines.append("")
        lines.append(cls.center_text("¡GRACIAS POR SU COMPRA!"))
        lines.append("")
        
        return "\n".join(lines)
