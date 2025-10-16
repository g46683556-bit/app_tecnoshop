from django.shortcuts import render, get_object_or_404
from .models import Catalog
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CatalogSerializer
from django.db.models import Q
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Catalog
from .serializers import CatalogSerializer


def catalog(request):
    productos = Catalog.objects.all()

    # Filtros
    q = request.GET.get("q")
    categorias = request.GET.getlist("categoria")
    min_precio = request.GET.get("min_precio")
    max_precio = request.GET.get("max_precio")

    # Aplicar filtros
    if q:
        productos = productos.filter(name__icontains=q)

    if categorias:
        productos = productos.filter(category__in=categorias)

    if min_precio:
        productos = productos.filter(price__gte=min_precio)

    if max_precio:
        productos = productos.filter(price__lte=max_precio)

    # 🟢 Obtener todas las categorías definidas en el modelo
    categorias_disponibles = Catalog.CATEGORIES

    return render(request, "pages/catalog.html", {
        "productos": productos,
        "categorias_disponibles": categorias_disponibles,  # ← importante
        "categorias_seleccionadas": categorias,
        "min_precio": min_precio or "",
        "max_precio": max_precio or "",
        "q": q or "",
    })

def product_detail(request, slug):
    product = get_object_or_404(Catalog, slug=slug)

    # Obtener productos sugeridos de la misma categoría, excluyendo el actual
    suggested_products = Catalog.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]  # Limita a 4 sugerencias

    return render(request, 'pages/product_detail.html', {
        'product': product,
        'suggested_products': suggested_products,
        'show_navbar': True,
    })




@api_view(['GET'])
def productos_api(request):
    q = request.GET.get('q', '').strip().lower()
    ofertas = request.GET.get('ofertas', '').lower() == 'true'
    productos = Catalog.objects.all()

    if q:
        productos = productos.filter(
            Q(name__icontains=q) |
            Q(category__icontains=q)
        )

    if ofertas:
        productos = productos.filter(
            Q(discount_percent__gt=0) | Q(discount_price__isnull=False)
        )

    serializer = CatalogSerializer(productos, many=True)
    return Response(serializer.data)





def export_catalog_pdf(request):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="Catálogo de Productos",
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.wordWrap = "CJK"  # permite el ajuste de línea
    desc_style = ParagraphStyle(
        'desc_style',
        parent=normal,
        fontSize=9,
        leading=11,
        spaceAfter=4,
    )

    story = []

    # Encabezado principal
    story.append(Paragraph("Catálogo de Productos", styles["Title"]))
    story.append(Spacer(1, 20))

    # Obtener productos y agrupar por categoría
    productos = Catalog.objects.all().order_by("category", "name")
    categorias = {}
    for p in productos:
        categorias.setdefault(p.category, []).append(p)

    for categoria, items in categorias.items():
        story.append(Paragraph(f"{categoria.capitalize()}", styles["Heading2"]))
        story.append(Spacer(1, 10))

        data = [["Imagen", "Nombre", "Descripción", "Precio (S/.)", "Stock"]]

        for item in items:
            # Imagen pequeña o guion si no hay
            img = "—"
            if item.image_url:
                try:
                    img_data = requests.get(item.image_url, timeout=3).content
                    img_temp = BytesIO(img_data)
                    img = RLImage(img_temp, width=45, height=45)
                except:
                    pass

            name_par = Paragraph(item.name, desc_style)
            desc_par = Paragraph(item.description or "—", desc_style)
            price_par = Paragraph(f"S/ {item.price:.2f}", desc_style)
            stock_par = Paragraph(str(item.stock), desc_style)

            data.append([img, name_par, desc_par, price_par, stock_par])

        # Crear tabla
        table = Table(
            data,
            colWidths=[60, 100, 200, 60, 40],
            repeatRows=1  # para repetir encabezados si se extiende a otra página
        )

        # Estilos de tabla
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))

        story.append(table)
        story.append(Spacer(1, 20))

    # Generar PDF
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="catalogo.pdf"'
    response.write(pdf)
    return response