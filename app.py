# app.py
# Professional Invoice Generator
# Created by Okewu Jeremiah

import html
import json
import urllib.request
import uuid
from datetime import date, timedelta

import streamlit as st
from pdf_generator import generate_invoice_pdf

st.set_page_config(
    page_title="Invoice Generator",
    page_icon="🧾",
    layout="wide",
)

# -------------------- LANGUAGES --------------------

EN = {
    "tagline": "Create professional invoices, convert currencies, calculate taxes, and download PDFs.",
    "language": "Language",
    "business_info": "Business information",
    "business_name": "Business name",
    "business_email": "Business email",
    "business_phone": "Business phone",
    "business_address": "Business address",
    "website": "Website (optional)",
    "logo": "Business logo",
    "upload_logo": "Upload PNG/JPG logo (maximum 500 KB)",
    "logo_too_large": "Logo exceeds 500 KB. Please select a smaller image.",
    "remove_logo": "Remove logo",
    "customer_info": "Customer information",
    "customer_name": "Customer name",
    "customer_email": "Customer email",
    "customer_phone": "Customer phone",
    "customer_address": "Customer address",
    "invoice_details": "Invoice details",
    "invoice_number": "Invoice number",
    "issue_date": "Issue date",
    "due_date": "Due date",
    "currency_settings": "Currency settings",
    "source_currency": "Currency used for item prices",
    "target_currency": "Currency shown on the invoice",
    "manual_rate": "Enter the exchange rate manually",
    "rate_prompt": "How many {target} equal 1 {source}?",
    "rate_caption": "Rate: 1 {source} = {rate:,.6f} {target}. Verify before issuing.",
    "rate_unavailable": "Online exchange rate unavailable. Enter a verified rate manually.",
    "products": "Products and services",
    "items_caption": "Enter prices in {source}. Invoice totals use {target}.",
    "add_item": "＋ Add product or service",
    "item": "Item",
    "description": "Description",
    "quantity": "Quantity",
    "unit_price": "Unit price",
    "remove": "Remove",
    "line_total": "Line total before conversion",
    "keep_item": "Keep at least one item on the invoice.",
    "discount_tax": "Discount and tax",
    "discount_type": "Discount type",
    "no_discount": "No discount",
    "percentage": "Percentage",
    "fixed_amount": "Fixed amount",
    "discount_percent": "Discount (%)",
    "discount_amount": "Discount amount",
    "tax_percent": "Tax (%)",
    "additional": "Additional information",
    "notes": "Invoice notes",
    "notes_placeholder": "Thank you for your business.",
    "payment_details": "Payment details (optional)",
    "payment_placeholder": "Bank, account name, account number, or payment link",
    "preview": "Invoice preview",
    "enter_business": "Enter your business name to preview the invoice.",
    "preview_rate": "Select a valid exchange rate to preview the invoice.",
    "invoice": "INVOICE",
    "bill_to": "BILL TO",
    "qty": "Qty",
    "amount": "Amount",
    "subtotal": "Subtotal",
    "discount": "Discount",
    "tax": "Tax",
    "total_due": "Total due",
    "download": "Download your invoice",
    "need_business": "Enter your business name before creating the PDF.",
    "need_customer": "Enter the customer's name before creating the PDF.",
    "need_number": "Enter an invoice number before creating the PDF.",
    "need_rate": "A valid exchange rate is required.",
    "download_button": "Download invoice as PDF",
    "pdf_error": "The PDF could not be created.",
    "created_by": "Created by Okewu Jeremiah",
    "phone_code": "Country calling code",
    "phone_number": "Phone number without country code",
}

# Translations override English labels. Untranslated labels safely use English.
TRANSLATIONS = {
    "Español": {
        "tagline": "Crea facturas profesionales, convierte monedas y descarga archivos PDF.",
        "language": "Idioma", "business_info": "Información de la empresa",
        "business_name": "Nombre de la empresa", "business_email": "Correo de la empresa",
        "business_phone": "Teléfono de la empresa", "business_address": "Dirección de la empresa",
        "website": "Sitio web (opcional)", "logo": "Logotipo de la empresa",
        "upload_logo": "Sube un logotipo PNG/JPG (máximo 500 KB)",
        "logo_too_large": "El logotipo supera los 500 KB.",
        "remove_logo": "Eliminar logotipo", "customer_info": "Información del cliente",
        "customer_name": "Nombre del cliente", "customer_email": "Correo del cliente",
        "customer_phone": "Teléfono del cliente", "customer_address": "Dirección del cliente",
        "invoice_details": "Detalles de la factura", "invoice_number": "Número de factura",
        "issue_date": "Fecha de emisión", "due_date": "Fecha de vencimiento",
        "currency_settings": "Configuración de moneda",
        "source_currency": "Moneda de los precios", "target_currency": "Moneda de la factura",
        "manual_rate": "Introducir el tipo de cambio manualmente",
        "products": "Productos y servicios", "item": "Artículo",
        "description": "Descripción", "quantity": "Cantidad", "unit_price": "Precio unitario",
        "remove": "Eliminar", "discount_tax": "Descuento e impuesto",
        "discount_type": "Tipo de descuento", "no_discount": "Sin descuento",
        "percentage": "Porcentaje", "fixed_amount": "Importe fijo",
        "discount_percent": "Descuento (%)", "discount_amount": "Importe del descuento",
        "tax_percent": "Impuesto (%)", "additional": "Información adicional",
        "notes": "Notas de la factura", "payment_details": "Datos de pago (opcional)",
        "preview": "Vista previa de la factura", "invoice": "FACTURA",
        "bill_to": "FACTURAR A", "qty": "Cant.", "amount": "Importe",
        "subtotal": "Subtotal", "discount": "Descuento", "tax": "Impuesto",
        "total_due": "Total a pagar", "download": "Descargar factura",
        "download_button": "Descargar factura en PDF",
        "phone_code": "Código telefónico del país",
        "phone_number": "Número de teléfono sin código",
    },
    "Português": {
        "tagline": "Crie faturas profissionais, converta moedas e baixe arquivos PDF.",
        "language": "Idioma", "business_info": "Informações da empresa",
        "business_name": "Nome da empresa", "business_email": "E-mail da empresa",
        "business_phone": "Telefone da empresa", "business_address": "Endereço da empresa",
        "website": "Site (opcional)", "logo": "Logotipo da empresa",
        "upload_logo": "Envie um logotipo PNG/JPG (máximo 500 KB)",
        "logo_too_large": "O logotipo excede 500 KB.",
        "remove_logo": "Remover logotipo", "customer_info": "Informações do cliente",
        "customer_name": "Nome do cliente", "customer_email": "E-mail do cliente",
        "customer_phone": "Telefone do cliente", "customer_address": "Endereço do cliente",
        "invoice_details": "Detalhes da fatura", "invoice_number": "Número da fatura",
        "issue_date": "Data de emissão", "due_date": "Data de vencimento",
        "currency_settings": "Configurações de moeda",
        "source_currency": "Moeda dos preços", "target_currency": "Moeda da fatura",
        "manual_rate": "Inserir taxa de câmbio manualmente",
        "products": "Produtos e serviços", "item": "Item", "description": "Descrição",
        "quantity": "Quantidade", "unit_price": "Preço unitário", "remove": "Remover",
        "discount_tax": "Desconto e imposto", "discount_type": "Tipo de desconto",
        "no_discount": "Sem desconto", "percentage": "Percentagem",
        "fixed_amount": "Valor fixo", "discount_percent": "Desconto (%)",
        "discount_amount": "Valor do desconto", "tax_percent": "Imposto (%)",
        "additional": "Informações adicionais", "notes": "Notas da fatura",
        "payment_details": "Dados de pagamento (opcional)",
        "preview": "Pré-visualização da fatura", "invoice": "FATURA",
        "bill_to": "FATURAR PARA", "qty": "Qtd.", "amount": "Valor",
        "subtotal": "Subtotal", "discount": "Desconto", "tax": "Imposto",
        "total_due": "Total a pagar", "download": "Baixar sua fatura",
        "download_button": "Baixar fatura em PDF",
        "phone_code": "Código telefônico do país",
        "phone_number": "Número de telefone sem código",
    },
    "Français": {
        "tagline": "Créez des factures professionnelles et téléchargez-les en PDF.",
        "language": "Langue", "business_info": "Informations sur l'entreprise",
        "business_name": "Nom de l'entreprise", "business_email": "E-mail de l'entreprise",
        "business_phone": "Téléphone de l'entreprise", "business_address": "Adresse de l'entreprise",
        "website": "Site web (facultatif)", "logo": "Logo de l'entreprise",
        "upload_logo": "Téléversez un logo PNG/JPG (500 Ko maximum)",
        "logo_too_large": "Le logo dépasse 500 Ko.",
        "remove_logo": "Supprimer le logo", "customer_info": "Informations du client",
        "customer_name": "Nom du client", "customer_email": "E-mail du client",
        "customer_phone": "Téléphone du client", "customer_address": "Adresse du client",
        "invoice_details": "Détails de la facture", "invoice_number": "Numéro de facture",
        "issue_date": "Date d'émission", "due_date": "Date d'échéance",
        "currency_settings": "Paramètres de devise",
        "source_currency": "Devise des prix", "target_currency": "Devise de la facture",
        "manual_rate": "Saisir le taux de change manuellement",
        "products": "Produits et services", "item": "Article", "description": "Description",
        "quantity": "Quantité", "unit_price": "Prix unitaire", "remove": "Supprimer",
        "discount_tax": "Remise et taxe", "discount_type": "Type de remise",
        "no_discount": "Aucune remise", "percentage": "Pourcentage",
        "fixed_amount": "Montant fixe", "discount_percent": "Remise (%)",
        "discount_amount": "Montant de la remise", "tax_percent": "Taxe (%)",
        "additional": "Informations complémentaires", "notes": "Notes de facture",
        "payment_details": "Informations de paiement (facultatif)",
        "preview": "Aperçu de la facture", "invoice": "FACTURE",
        "bill_to": "FACTURER À", "qty": "Qté", "amount": "Montant",
        "subtotal": "Sous-total", "discount": "Remise", "tax": "Taxe",
        "total_due": "Total à payer", "download": "Télécharger la facture",
        "download_button": "Télécharger la facture en PDF",
        "phone_code": "Indicatif téléphonique du pays",
        "phone_number": "Numéro sans indicatif",
    },
    "Deutsch": {
        "tagline": "Erstellen Sie professionelle Rechnungen und laden Sie sie als PDF herunter.",
        "language": "Sprache", "business_info": "Unternehmensdaten",
        "business_name": "Unternehmensname", "business_email": "Unternehmens-E-Mail",
        "business_phone": "Unternehmenstelefon", "business_address": "Unternehmensadresse",
        "website": "Website (optional)", "logo": "Unternehmenslogo",
        "upload_logo": "PNG/JPG-Logo hochladen (maximal 500 KB)",
        "logo_too_large": "Das Logo ist größer als 500 KB.",
        "remove_logo": "Logo entfernen", "customer_info": "Kundendaten",
        "customer_name": "Kundenname", "customer_email": "Kunden-E-Mail",
        "customer_phone": "Kundentelefon", "customer_address": "Kundenadresse",
        "invoice_details": "Rechnungsdetails", "invoice_number": "Rechnungsnummer",
        "issue_date": "Ausstellungsdatum", "due_date": "Fälligkeitsdatum",
        "currency_settings": "Währungseinstellungen",
        "source_currency": "Währung der Artikelpreise", "target_currency": "Rechnungswährung",
        "manual_rate": "Wechselkurs manuell eingeben",
        "products": "Produkte und Dienstleistungen", "item": "Position",
        "description": "Beschreibung", "quantity": "Menge", "unit_price": "Einzelpreis",
        "remove": "Entfernen", "discount_tax": "Rabatt und Steuer",
        "discount_type": "Rabattart", "no_discount": "Kein Rabatt",
        "percentage": "Prozent", "fixed_amount": "Fester Betrag",
        "discount_percent": "Rabatt (%)", "discount_amount": "Rabattbetrag",
        "tax_percent": "Steuer (%)", "additional": "Zusätzliche Informationen",
        "notes": "Rechnungshinweise", "payment_details": "Zahlungsdetails (optional)",
        "preview": "Rechnungsvorschau", "invoice": "RECHNUNG",
        "bill_to": "RECHNUNG AN", "qty": "Menge", "amount": "Betrag",
        "subtotal": "Zwischensumme", "discount": "Rabatt", "tax": "Steuer",
        "total_due": "Gesamtbetrag", "download": "Rechnung herunterladen",
        "download_button": "Rechnung als PDF herunterladen",
        "phone_code": "Ländervorwahl", "phone_number": "Telefonnummer ohne Vorwahl",
    },
}

LANGUAGES = {"English": EN}
LANGUAGES.update(TRANSLATIONS)

# -------------------- COUNTRIES AND CURRENCIES --------------------

COUNTRIES = {
    "Nigeria (+234)": "+234", "United States (+1)": "+1",
    "Canada (+1)": "+1", "United Kingdom (+44)": "+44",
    "Ghana (+233)": "+233", "Kenya (+254)": "+254",
    "South Africa (+27)": "+27", "India (+91)": "+91",
    "Australia (+61)": "+61", "New Zealand (+64)": "+64",
    "Portugal (+351)": "+351", "Brazil (+55)": "+55",
    "Spain (+34)": "+34", "France (+33)": "+33",
    "Germany (+49)": "+49", "Italy (+39)": "+39",
    "Ireland (+353)": "+353", "Netherlands (+31)": "+31",
    "UAE (+971)": "+971", "Saudi Arabia (+966)": "+966",
    "China (+86)": "+86", "Japan (+81)": "+81",
    "Pakistan (+92)": "+92", "Philippines (+63)": "+63",
    "Mexico (+52)": "+52", "Turkey (+90)": "+90",
    "Egypt (+20)": "+20", "Rwanda (+250)": "+250",
    "Uganda (+256)": "+256", "Tanzania (+255)": "+255",
    "Singapore (+65)": "+65", "Malaysia (+60)": "+60",
    "Switzerland (+41)": "+41", "Sweden (+46)": "+46",
    "Norway (+47)": "+47", "Denmark (+45)": "+45",
    "Poland (+48)": "+48",
}

CURRENCIES = {
    "NGN": "Nigerian Naira", "USD": "US Dollar",
    "GBP": "British Pound", "EUR": "Euro", "GHS": "Ghanaian Cedi",
    "KES": "Kenyan Shilling", "ZAR": "South African Rand",
    "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
    "INR": "Indian Rupee", "JPY": "Japanese Yen", "CNY": "Chinese Yuan",
    "AED": "UAE Dirham", "SAR": "Saudi Riyal", "XOF": "West African CFA Franc",
    "XAF": "Central African CFA Franc", "CHF": "Swiss Franc",
    "BRL": "Brazilian Real", "SGD": "Singapore Dollar", "NZD": "New Zealand Dollar",
    "UGX": "Ugandan Shilling", "TZS": "Tanzanian Shilling",
    "RWF": "Rwandan Franc", "EGP": "Egyptian Pound", "MAD": "Moroccan Dirham",
    "TRY": "Turkish Lira", "MXN": "Mexican Peso", "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee", "BDT": "Bangladeshi Taka",
    "KRW": "South Korean Won", "THB": "Thai Baht", "IDR": "Indonesian Rupiah",
    "MYR": "Malaysian Ringgit", "HKD": "Hong Kong Dollar",
    "SEK": "Swedish Krona", "NOK": "Norwegian Krone",
    "DKK": "Danish Krone", "PLN": "Polish Zloty",
}

SYMBOLS = {
    "NGN": "₦", "USD": "$", "GBP": "£", "EUR": "€", "GHS": "GH₵",
    "KES": "KSh ", "ZAR": "R", "CAD": "CA$", "AUD": "A$", "INR": "₹",
    "JPY": "¥", "CNY": "¥", "AED": "AED ", "SAR": "SAR ",
    "XOF": "CFA ", "XAF": "FCFA ", "CHF": "CHF ", "BRL": "R$",
    "SGD": "S$", "NZD": "NZ$", "UGX": "USh ", "TZS": "TSh ",
    "RWF": "RF ", "EGP": "E£", "MAD": "MAD ", "TRY": "₺",
    "MXN": "MX$", "PHP": "₱", "PKR": "Rs ", "BDT": "৳",
    "KRW": "₩", "THB": "฿", "IDR": "Rp ", "MYR": "RM ",
    "HKD": "HK$", "SEK": "kr ", "NOK": "kr ", "DKK": "kr ", "PLN": "zł ",
}


def tr(key, **kwargs):
    language = st.session_state.get("app_language", "English")
    text = LANGUAGES.get(language, EN).get(key, EN.get(key, key))
    return text.format(**kwargs) if kwargs else text


def safe(value):
    return html.escape(str(value or "")).replace("\n", "<br>")


def money(amount, currency):
    return f"{SYMBOLS.get(currency, currency + ' ')}{float(amount):,.2f}"


@st.cache_data(ttl=3600, show_spinner=False)
def get_exchange_rates(base_currency):
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "InvoiceGenerator/1.0"}
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        result = json.loads(response.read().decode("utf-8"))

    if result.get("result") != "success":
        raise ValueError("Exchange-rate service failed.")
    return result["rates"]


def make_item():
    return {
        "id": uuid.uuid4().hex[:10],
        "description": "",
        "quantity": 1.0,
        "unit_price": 0.0,
    }


def phone_input(key_prefix):
    country_names = list(COUNTRIES.keys())
    default_index = country_names.index("Nigeria (+234)")

    country = st.selectbox(
        tr("phone_code"),
        country_names,
        index=default_index,
        key=f"{key_prefix}_country",
    )
    number = st.text_input(
        tr("phone_number"),
        placeholder="8012345678",
        key=f"{key_prefix}_number",
    )

    digits = "".join(char for char in number if char.isdigit())
    return f"{COUNTRIES[country]} {digits}".strip() if digits else ""


# -------------------- DESIGN --------------------

st.markdown("""
<style>
.stApp { background: #F5F7FA; color: #263445; }
.block-container { max-width: 1250px; padding-top: 1.5rem; padding-bottom: 3rem; }
h1, h2, h3 { color: #183153; }
.main-heading { background: #183153; color: white; padding: 24px; border-radius: 12px; margin-bottom: 22px; }
.main-heading h1 { color: white; margin: 0; font-size: 30px; }
.main-heading p { color: #DCE5EF; margin: 8px 0 0; }
.invoice-preview { background: white; border: 1px solid #DCE3EC; border-radius: 10px; padding: 28px; color: #263445; }
.invoice-preview h2 { color: #183153; }
.invoice-preview table { width: 100%; border-collapse: collapse; margin: 20px 0; }
.invoice-preview th { background: #183153; color: white; padding: 11px 8px; text-align: left; }
.invoice-preview td { padding: 11px 8px; border-bottom: 1px solid #E5EAF0; }
.invoice-total { background: #EDF5F3; border-left: 5px solid #167568; padding: 18px; border-radius: 6px; margin-top: 18px; }
.invoice-total strong { color: #167568; font-size: 23px; }
.muted-text { color: #68778A; font-size: 13px; }
.app-footer { text-align: center; color: #68778A; font-size: 12px; padding: 22px 0 5px; }
div.stButton > button { border-radius: 7px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------

if "app_language" not in st.session_state:
    st.session_state.app_language = "English"
if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = [dict(make_item(), description="Example service")]
if "logo_bytes" not in st.session_state:
    st.session_state.logo_bytes = None
if "logo_version" not in st.session_state:
    st.session_state.logo_version = 0

st.selectbox(tr("language"), list(LANGUAGES.keys()), key="app_language")

st.markdown(
    f'<div class="main-heading"><h1>🧾 Invoice Generator</h1>'
    f'<p>{safe(tr("tagline"))}</p></div>',
    unsafe_allow_html=True,
)

# -------------------- BUSINESS INFORMATION --------------------

st.markdown(f"### {tr('business_info')}")
left, right = st.columns(2)

with left:
    business_name = st.text_input(tr("business_name"), key="business_name")
    business_email = st.text_input(tr("business_email"), key="business_email")
    st.markdown(f"**{tr('business_phone')}**")
    business_phone = phone_input("business")

with right:
    business_address = st.text_area(tr("business_address"), key="business_address")
    business_website = st.text_input(tr("website"), key="business_website")

st.markdown(f"#### {tr('logo')}")
uploaded_logo = st.file_uploader(
    tr("upload_logo"),
    type=["png", "jpg", "jpeg"],
    max_upload_size=1,
    key=f"logo_upload_{st.session_state.logo_version}",
)

if uploaded_logo is not None:
    image_bytes = uploaded_logo.getvalue()
    if len(image_bytes) > 500 * 1024:
        st.error(tr("logo_too_large"))
    else:
        st.session_state.logo_bytes = image_bytes

logo_col1, logo_col2 = st.columns([1, 4])
with logo_col1:
    if st.session_state.logo_bytes:
        st.image(st.session_state.logo_bytes, width=120)
with logo_col2:
    if st.session_state.logo_bytes and st.button(tr("remove_logo")):
        st.session_state.logo_bytes = None
        st.session_state.logo_version += 1
        st.rerun()

# -------------------- CUSTOMER INFORMATION --------------------

st.markdown(f"### {tr('customer_info')}")
left, right = st.columns(2)

with left:
    customer_name = st.text_input(tr("customer_name"), key="customer_name")
    customer_email = st.text_input(tr("customer_email"), key="customer_email")
    st.markdown(f"**{tr('customer_phone')}**")
    customer_phone = phone_input("customer")

with right:
    customer_address = st.text_area(tr("customer_address"), key="customer_address")

# -------------------- INVOICE DETAILS --------------------

st.markdown(f"### {tr('invoice_details')}")
col1, col2, col3 = st.columns(3)

with col1:
    invoice_number = st.text_input(
        tr("invoice_number"), value="INV-001", key="invoice_number"
    )
with col2:
    issue_date = st.date_input(tr("issue_date"), value=date.today())
with col3:
    due_date = st.date_input(
        tr("due_date"), value=date.today() + timedelta(days=7)
    )

# -------------------- CURRENCY CONVERSION --------------------

st.markdown(f"### {tr('currency_settings')}")
currency_options = [f"{code} — {name}" for code, name in CURRENCIES.items()]
col1, col2 = st.columns(2)

with col1:
    source_label = st.selectbox(tr("source_currency"), currency_options, index=0)
with col2:
    target_label = st.selectbox(tr("target_currency"), currency_options, index=0)

source_currency = source_label.split(" — ")[0]
target_currency = target_label.split(" — ")[0]

exchange_rate = None
online_rate = None
rate_error = None

if source_currency == target_currency:
    exchange_rate = 1.0
else:
    try:
        online_rate = get_exchange_rates(source_currency).get(target_currency)
    except Exception as error:
        rate_error = str(error)

use_manual_rate = st.checkbox(tr("manual_rate"))

if source_currency == target_currency:
    exchange_rate = 1.0
elif use_manual_rate:
    exchange_rate = st.number_input(
        tr("rate_prompt", target=target_currency, source=source_currency),
        min_value=0.000001,
        value=1.0,
        step=0.1,
        format="%.6f",
    )
elif online_rate is not None:
    exchange_rate = float(online_rate)
    st.caption(
        tr(
            "rate_caption",
            source=source_currency,
            target=target_currency,
            rate=exchange_rate,
        )
    )
else:
    st.warning(tr("rate_unavailable"))
    if rate_error:
        st.caption(f"Rate service detail: {rate_error}")

# -------------------- PRODUCTS AND SERVICES --------------------

st.markdown(f"### {tr('products')}")
st.caption(tr("items_caption", source=source_currency, target=target_currency))

if st.button(tr("add_item")):
    st.session_state.invoice_items.append(make_item())
    st.rerun()

remove_id = None

for index, item in enumerate(st.session_state.invoice_items):
    st.markdown(f"**{tr('item')} {index + 1}**")
    col1, col2, col3, col4 = st.columns([4, 1.5, 2, 1.2])

    with col1:
        item["description"] = st.text_input(
            tr("description"),
            value=item["description"],
            key=f"description_{item['id']}",
        )
    with col2:
        item["quantity"] = st.number_input(
            tr("quantity"),
            min_value=0.001,
            value=float(item["quantity"]),
            step=1.0,
            key=f"quantity_{item['id']}",
        )
    with col3:
        item["unit_price"] = st.number_input(
            f"{tr('unit_price')} ({source_currency})",
            min_value=0.0,
            value=float(item["unit_price"]),
            step=100.0,
            key=f"price_{item['id']}",
        )
    with col4:
        st.write("")
        st.write("")
        if st.button(tr("remove"), key=f"remove_{item['id']}"):
            remove_id = item["id"]

    st.caption(
        f"{tr('line_total')}: "
        f"{money(item['quantity'] * item['unit_price'], source_currency)}"
    )
    st.divider()

if remove_id is not None:
    if len(st.session_state.invoice_items) > 1:
        st.session_state.invoice_items = [
            item for item in st.session_state.invoice_items
            if item["id"] != remove_id
        ]
        st.rerun()
    else:
        st.warning(tr("keep_item"))

# -------------------- DISCOUNT AND TAX --------------------

st.markdown(f"### {tr('discount_tax')}")
col1, col2, col3 = st.columns(3)

discount_labels = {
    "none": tr("no_discount"),
    "percentage": tr("percentage"),
    "fixed": tr("fixed_amount"),
}

with col1:
    discount_type = st.selectbox(
        tr("discount_type"),
        ["none", "percentage", "fixed"],
        format_func=lambda value: discount_labels[value],
    )

with col2:
    if discount_type == "percentage":
        discount_value = st.number_input(
            tr("discount_percent"), min_value=0.0, max_value=100.0, value=0.0
        )
    elif discount_type == "fixed":
        discount_value = st.number_input(
            f"{tr('discount_amount')} ({target_currency})",
            min_value=0.0, value=0.0,
        )
    else:
        discount_value = 0.0

with col3:
    tax_percentage = st.number_input(
        tr("tax_percent"), min_value=0.0, max_value=100.0, value=0.0
    )

# -------------------- NOTES AND PAYMENT DETAILS --------------------

st.markdown(f"### {tr('additional')}")
notes = st.text_area(
    tr("notes"), value=tr("notes_placeholder"),
    placeholder=tr("notes_placeholder"),
)
payment_details = st.text_area(
    tr("payment_details"), placeholder=tr("payment_placeholder")
)

# -------------------- CALCULATE TOTALS --------------------

invoice_ready = exchange_rate is not None and exchange_rate > 0
converted_items = []

if invoice_ready:
    for item in st.session_state.invoice_items:
        converted_price = item["unit_price"] * exchange_rate
        converted_items.append({
            "description": item["description"].strip(),
            "quantity": float(item["quantity"]),
            "unit_price": converted_price,
            "line_total": float(item["quantity"]) * converted_price,
        })

    subtotal = sum(item["line_total"] for item in converted_items)

    if discount_type == "percentage":
        discount_amount = subtotal * discount_value / 100
    elif discount_type == "fixed":
        discount_amount = min(discount_value, subtotal)
    else:
        discount_amount = 0.0

    taxable_amount = max(0.0, subtotal - discount_amount)
    tax_amount = taxable_amount * tax_percentage / 100
    total_due = taxable_amount + tax_amount
else:
    subtotal = discount_amount = tax_amount = total_due = 0.0

# -------------------- INVOICE PREVIEW --------------------

st.markdown(f"### {tr('preview')}")

if not invoice_ready:
    st.info(tr("preview_rate"))
elif not business_name.strip():
    st.info(tr("enter_business"))
else:
    business_lines = "<br>".join(
        safe(value) for value in [
            business_address, business_phone, business_email, business_website
        ] if value.strip()
    )
    customer_lines = "<br>".join(
        safe(value) for value in [
            customer_address, customer_phone, customer_email
        ] if value.strip()
    )

    rows = ""
    for item in converted_items:
        quantity = f"{item['quantity']:,.3f}".rstrip("0").rstrip(".")
        rows += (
            f"<tr><td>{safe(item['description'] or 'Item')}</td>"
            f"<td>{quantity}</td>"
            f"<td>{safe(money(item['unit_price'], target_currency))}</td>"
            f"<td>{safe(money(item['line_total'], target_currency))}</td></tr>"
        )

    if st.session_state.logo_bytes:
        st.image(st.session_state.logo_bytes, width=120)

    preview = f"""
    <div class="invoice-preview">
      <h2>{safe(business_name)}</h2>
      <div class="muted-text">{business_lines}</div>
      <hr>
      <p><strong>{safe(tr('invoice'))}</strong><br>
      {safe(tr('invoice_number'))}: {safe(invoice_number)}<br>
      {safe(tr('issue_date'))}: {issue_date.strftime('%d %b %Y')}<br>
      {safe(tr('due_date'))}: {due_date.strftime('%d %b %Y')}</p>
      <p><strong>{safe(tr('bill_to'))}</strong><br>
      {safe(customer_name or tr('customer_name'))}<br>{customer_lines}</p>
      <table>
        <thead><tr>
          <th>{safe(tr('description'))}</th><th>{safe(tr('qty'))}</th>
          <th>{safe(tr('unit_price'))}</th><th>{safe(tr('amount'))}</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <div style="text-align:right;line-height:2;">
        {safe(tr('subtotal'))}: <strong>{safe(money(subtotal, target_currency))}</strong><br>
        {safe(tr('discount'))}: -{safe(money(discount_amount, target_currency))}<br>
        {safe(tr('tax'))} ({tax_percentage:.2f}%): {safe(money(tax_amount, target_currency))}
      </div>
      <div class="invoice-total">
        <div>{safe(tr('total_due'))}</div>
        <strong>{safe(money(total_due, target_currency))}</strong>
      </div>
      <p><strong>{safe(tr('notes'))}</strong><br>{safe(notes)}</p>
      <p><strong>{safe(tr('payment_details'))}</strong><br>{safe(payment_details)}</p>
      <hr><div class="muted-text">{safe(tr('created_by'))}</div>
    </div>
    """
    st.markdown(preview, unsafe_allow_html=True)

# -------------------- PDF DOWNLOAD --------------------

st.markdown(f"### {tr('download')}")

if not business_name.strip():
    st.warning(tr("need_business"))
elif not customer_name.strip():
    st.warning(tr("need_customer"))
elif not invoice_number.strip():
    st.warning(tr("need_number"))
elif not invoice_ready:
    st.warning(tr("need_rate"))
else:
    pdf_data = {
        "business_name": business_name,
        "business_email": business_email,
        "business_phone": business_phone,
        "business_address": business_address,
        "business_website": business_website,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_phone": customer_phone,
        "customer_address": customer_address,
        "invoice_number": invoice_number,
        "issue_date": issue_date.strftime("%d %b %Y"),
        "due_date": due_date.strftime("%d %b %Y"),
        "source_currency": source_currency,
        "currency": target_currency,
        "exchange_rate": exchange_rate,
        "items": converted_items,
        "subtotal": subtotal,
        "discount": discount_amount,
        "tax_percentage": tax_percentage,
        "tax": tax_amount,
        "total": total_due,
        "notes": notes,
        "payment_details": payment_details,
        "logo_bytes": st.session_state.logo_bytes,
        "language": st.session_state.app_language,
    }

    try:
        pdf_bytes = generate_invoice_pdf(pdf_data)
        safe_number = "".join(
            char for char in invoice_number if char.isalnum() or char in "-_"
        )
        st.download_button(
            label=tr("download_button"),
            data=pdf_bytes,
            file_name=f"Invoice_{safe_number or 'invoice'}.pdf",
            mime="application/pdf",
            type="primary",
        )
    except Exception as error:
        st.error(tr("pdf_error"))
        st.code(str(error))

st.markdown(
    f'<div class="app-footer">Invoice Generator · '
    f'{safe(tr("created_by"))}</div>',
    unsafe_allow_html=True,
)