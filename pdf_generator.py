# pdf_generator.py
# Creates a professional PDF invoice.
# Created by Okewu Jeremiah

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

# -------------------- CURRENCY SYMBOLS --------------------

CURRENCY_SYMBOLS = {
    "NGN": "NGN ",
    "USD": "$",
    "GBP": "GBP ",
    "EUR": "EUR ",
    "GHS": "GHS ",
    "KES": "KSh ",
    "ZAR": "R",
    "CAD": "CA$",
    "AUD": "A$",
    "INR": "INR ",
    "JPY": "JPY ",
    "CNY": "CNY ",
    "AED": "AED ",
    "SAR": "SAR ",
    "XOF": "CFA ",
    "XAF": "FCFA ",
    "CHF": "CHF ",
    "BRL": "R$",
    "SGD": "S$",
    "NZD": "NZ$",
    "UGX": "USh ",
    "TZS": "TSh ",
    "RWF": "RF ",
    "EGP": "EGP ",
    "MAD": "MAD ",
    "TRY": "TRY ",
    "MXN": "MX$",
    "PHP": "PHP ",
    "PKR": "PKR ",
    "BDT": "BDT ",
    "KRW": "KRW ",
    "THB": "THB ",
    "IDR": "Rp ",
    "MYR": "RM ",
    "HKD": "HK$",
    "SEK": "SEK ",
    "NOK": "NOK ",
    "DKK": "DKK ",
    "PLN": "PLN ",
}

# -------------------- PDF TRANSLATIONS --------------------

PDF_TEXT = {
    "English": {
        "invoice": "INVOICE",
        "bill_to": "BILL TO",
        "description": "Description",
        "qty": "Qty",
        "unit_price": "Unit price",
        "amount": "Amount",
        "subtotal": "Subtotal",
        "discount": "Discount",
        "tax": "Tax",
        "total": "TOTAL DUE",
        "issue": "Issue date",
        "due": "Due date",
        "notes": "Notes",
        "payment": "Payment details",
        "exchange": "Exchange rate",
        "currency": "Currency",
    },
    "Español": {
        "invoice": "FACTURA",
        "bill_to": "FACTURAR A",
        "description": "Descripción",
        "qty": "Cant.",
        "unit_price": "Precio unitario",
        "amount": "Importe",
        "subtotal": "Subtotal",
        "discount": "Descuento",
        "tax": "Impuesto",
        "total": "TOTAL A PAGAR",
        "issue": "Fecha de emisión",
        "due": "Fecha de vencimiento",
        "notes": "Notas",
        "payment": "Datos de pago",
        "exchange": "Tipo de cambio",
        "currency": "Moneda",
    },
    "Português": {
        "invoice": "FATURA",
        "bill_to": "FATURAR PARA",
        "description": "Descrição",
        "qty": "Qtd.",
        "unit_price": "Preço unitário",
        "amount": "Valor",
        "subtotal": "Subtotal",
        "discount": "Desconto",
        "tax": "Imposto",
        "total": "TOTAL A PAGAR",
        "issue": "Data de emissão",
        "due": "Data de vencimento",
        "notes": "Notas",
        "payment": "Dados de pagamento",
        "exchange": "Taxa de câmbio",
        "currency": "Moeda",
    },
    "Français": {
        "invoice": "FACTURE",
        "bill_to": "FACTURER À",
        "description": "Description",
        "qty": "Qté",
        "unit_price": "Prix unitaire",
        "amount": "Montant",
        "subtotal": "Sous-total",
        "discount": "Remise",
        "tax": "Taxe",
        "total": "TOTAL À PAYER",
        "issue": "Date d'émission",
        "due": "Date d'échéance",
        "notes": "Notes",
        "payment": "Informations de paiement",
        "exchange": "Taux de change",
        "currency": "Devise",
    },
    "Deutsch": {
        "invoice": "RECHNUNG",
        "bill_to": "RECHNUNG AN",
        "description": "Beschreibung",
        "qty": "Menge",
        "unit_price": "Einzelpreis",
        "amount": "Betrag",
        "subtotal": "Zwischensumme",
        "discount": "Rabatt",
        "tax": "Steuer",
        "total": "GESAMTBETRAG",
        "issue": "Ausstellungsdatum",
        "due": "Fälligkeitsdatum",
        "notes": "Hinweise",
        "payment": "Zahlungsdetails",
        "exchange": "Wechselkurs",
        "currency": "Währung",
    },
}

# -------------------- PROFESSIONAL COLOURS --------------------

NAVY = colors.HexColor("#183153")
TEAL = colors.HexColor("#167568")
PALE = colors.HexColor("#EDF5F3")
LIGHT = colors.HexColor("#E1E7EF")
DARK = colors.HexColor("#263445")
MUTED = colors.HexColor("#68778A")


def money(amount, currency):
    """Format an amount using the selected currency."""
    symbol = CURRENCY_SYMBOLS.get(currency, f"{currency} ")
    return f"{symbol}{float(amount):,.2f}"


def paragraph(text, style):
    """Safely display user-entered text inside a PDF paragraph."""
    text = escape(str(text or "")).replace("\n", "<br/>")
    return Paragraph(text, style)


def generate_invoice_pdf(data):
    """Create a PDF invoice from the dictionary supplied by app.py."""

    language = data.get("language", "English")
    labels = PDF_TEXT.get(language, PDF_TEXT["English"])

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title=f"Invoice {data.get('invoice_number', '')}",
        author="Okewu Jeremiah",
    )

    # -------------------- PDF TEXT STYLES --------------------

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="InvoiceTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=30,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=DARK,
            spaceAfter=2,
        )
    )

    styles.add(
        ParagraphStyle(
            name="MutedSmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=MUTED,
            spaceAfter=2,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=DARK,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCellRight",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=DARK,
            alignment=TA_RIGHT,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TotalLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TotalValue",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=TEAL,
            alignment=TA_RIGHT,
        )
    )

    story = []

    # -------------------- BUSINESS HEADER --------------------

    business_name = data.get("business_name", "")
    logo_bytes = data.get("logo_bytes")

    logo = None

    if logo_bytes:
        try:
            logo = Image(
                BytesIO(logo_bytes),
                width=27 * mm,
                height=22 * mm,
                kind="proportional",
            )
            logo.hAlign = "LEFT"
        except Exception:
            logo = None

    business_lines = [
        data.get("business_address", ""),
        data.get("business_phone", ""),
        data.get("business_email", ""),
        data.get("business_website", ""),
    ]

    business_text = "<br/>".join(
        escape(str(value))
        for value in business_lines
        if str(value or "").strip()
    )

    left_header = []

    if logo:
        left_header.append(logo)

    left_header.append(
        Paragraph(
            f"<b>{escape(str(business_name))}</b>",
            styles["SectionTitle"],
        )
    )

    if business_text:
        left_header.append(
            Paragraph(business_text, styles["MutedSmall"])
        )

    title_block = [
        Paragraph(labels["invoice"], styles["InvoiceTitle"]),
        Paragraph(
            f"<b>#{escape(str(data.get('invoice_number', '')))}</b>",
            styles["BodySmall"],
        ),
        Spacer(1, 3 * mm),
        Paragraph(
            f"{labels['issue']}: {escape(str(data.get('issue_date', '')))}",
            styles["MutedSmall"],
        ),
        Paragraph(
            f"{labels['due']}: {escape(str(data.get('due_date', '')))}",
            styles["MutedSmall"],
        ),
    ]

    header = Table(
        [[left_header, title_block]],
        colWidths=[91 * mm, 79 * mm],
    )

    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ("LINEBELOW", (0, 0), (-1, -1), 1.4, NAVY),
            ]
        )
    )

    story.append(header)
    story.append(Spacer(1, 7 * mm))

    # -------------------- CUSTOMER INFORMATION --------------------

    customer_lines = [
        data.get("customer_name", ""),
        data.get("customer_address", ""),
        data.get("customer_phone", ""),
        data.get("customer_email", ""),
    ]

    customer_text = "<br/>".join(
        escape(str(value))
        for value in customer_lines
        if str(value or "").strip()
    )

    customer_block = [
        Paragraph(labels["bill_to"], styles["SectionTitle"]),
        Paragraph(customer_text or "—", styles["BodySmall"]),
    ]

    currency = data.get("currency", "NGN")
    exchange_rate = data.get("exchange_rate")

    details_block = [
        Paragraph(
            f"<b>{labels['currency']}:</b> {escape(str(currency))}",
            styles["BodySmall"],
        )
    ]

    if (
        exchange_rate is not None
        and data.get("source_currency") != currency
    ):
        details_block.append(
            Paragraph(
                f"{labels['exchange']}: 1 "
                f"{escape(str(data.get('source_currency')))} = "
                f"{float(exchange_rate):,.6f} {escape(str(currency))}",
                styles["MutedSmall"],
            )
        )

    details = Table(
        [[customer_block, details_block]],
        colWidths=[105 * mm, 65 * mm],
    )

    details.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FA")),
                ("BOX", (0, 0), (-1, -1), 0.6, LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(details)
    story.append(Spacer(1, 7 * mm))

    # -------------------- PRODUCT TABLE --------------------

    item_data = [
        [
            Paragraph(labels["description"], styles["TableHeader"]),
            Paragraph(labels["qty"], styles["TableHeader"]),
            Paragraph(labels["unit_price"], styles["TableHeader"]),
            Paragraph(labels["amount"], styles["TableHeader"]),
        ]
    ]

    for item in data.get("items", []):
        quantity = float(item.get("quantity", 0))
        quantity_text = f"{quantity:,.3f}".rstrip("0").rstrip(".")

        item_data.append(
            [
                Paragraph(
                    escape(str(item.get("description") or "Item")),
                    styles["TableCell"],
                ),
                Paragraph(quantity_text, styles["TableCellRight"]),
                Paragraph(
                    money(item.get("unit_price", 0), currency),
                    styles["TableCellRight"],
                ),
                Paragraph(
                    money(item.get("line_total", 0), currency),
                    styles["TableCellRight"],
                ),
            ]
        )

    items_table = Table(
        item_data,
        colWidths=[76 * mm, 18 * mm, 37 * mm, 39 * mm],
        repeatRows=1,
    )

    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.35, LIGHT),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F8FAFC")],
                ),
            ]
        )
    )

    story.append(items_table)
    story.append(Spacer(1, 5 * mm))

    # -------------------- TOTALS --------------------

    summary_rows = [
        [
            Paragraph(labels["subtotal"], styles["BodySmall"]),
            Paragraph(
                money(data.get("subtotal", 0), currency),
                styles["TableCellRight"],
            ),
        ],
        [
            Paragraph(labels["discount"], styles["BodySmall"]),
            Paragraph(
                f"-{money(data.get('discount', 0), currency)}",
                styles["TableCellRight"],
            ),
        ],
        [
            Paragraph(
                f"{labels['tax']} "
                f"({float(data.get('tax_percentage', 0)):.2f}%)",
                styles["BodySmall"],
            ),
            Paragraph(
                money(data.get("tax", 0), currency),
                styles["TableCellRight"],
            ),
        ],
    ]

    summary = Table(
        summary_rows,
        colWidths=[40 * mm, 42 * mm],
        hAlign="RIGHT",
    )

    summary.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEABOVE", (0, 0), (-1, 0), 0.6, LIGHT),
            ]
        )
    )

    story.append(summary)

    total = Table(
        [
            [
                Paragraph(labels["total"], styles["TotalLabel"]),
                Paragraph(
                    money(data.get("total", 0), currency),
                    styles["TotalValue"],
                ),
            ]
        ],
        colWidths=[82 * mm],
        hAlign="RIGHT",
    )

    total.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.7, LIGHT),
                ("LINEBEFORE", (0, 0), (0, -1), 4, TEAL),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    story.append(total)

    # -------------------- NOTES AND PAYMENT --------------------

    notes = str(data.get("notes") or "").strip()
    payment = str(data.get("payment_details") or "").strip()

    if notes:
        story.extend(
            [
                Spacer(1, 7 * mm),
                Paragraph(labels["notes"], styles["SectionTitle"]),
                paragraph(notes, styles["BodySmall"]),
            ]
        )

    if payment:
        story.extend(
            [
                Spacer(1, 3 * mm),
                Paragraph(labels["payment"], styles["SectionTitle"]),
                paragraph(payment, styles["BodySmall"]),
            ]
        )

    # -------------------- FOOTER --------------------

    def add_footer(canvas, document):
        canvas.saveState()

        canvas.setStrokeColor(LIGHT)
        canvas.setLineWidth(0.5)
        canvas.line(
            20 * mm,
            13 * mm,
            A4[0] - 20 * mm,
            13 * mm,
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(
            20 * mm,
            8.5 * mm,
            "Created by Okewu Jeremiah",
        )
        canvas.drawRightString(
            A4[0] - 20 * mm,
            8.5 * mm,
            f"Page {document.page}",
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer,
    )

    return buffer.getvalue()