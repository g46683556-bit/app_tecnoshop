from django.shortcuts import render, get_object_or_404
from .models import Catalog

# def catalog(request):
#     # Obtener todos los productos desde la BD
#     productos = Catalog.objects.all()

#     # Filtros recibidos desde GET
#     q = request.GET.get("q")  # palabra clave de búsqueda
#     categorias = request.GET.getlist("categoria")  # lista de checkboxes seleccionados
#     min_precio = request.GET.get("min_precio")
#     max_precio = request.GET.get("max_precio")

#     # Aplicar búsqueda
#     if q:
#         productos = productos.filter(name__icontains=q)  # busca en el nombre

#     # Aplicar filtros
#     if categorias:
#         productos = productos.filter(category__in=categorias)

#     if min_precio:
#         productos = productos.filter(price__gte=min_precio)

#     if max_precio:
#         productos = productos.filter(price__lte=max_precio)

#     return render(request, "pages/catalog.html", {
#         "productos": productos,
#         "categorias_seleccionadas": categorias,
#         "min_precio": min_precio or "",
#         "max_precio": max_precio or "",
#         "q": q or "",
#     })

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


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CatalogSerializer

# @api_view(['GET'])
# def productos_api(request):
#     q = request.GET.get('q', '').strip().lower()
#     productos = Catalog.objects.all()

#     if q:
#         productos = productos.filter(name__icontains=q)

#     serializer = CatalogSerializer(productos, many=True)
#     return Response(serializer.data)

from django.db.models import Q

@api_view(['GET'])
def productos_api(request):
    q = request.GET.get('q', '').strip().lower()
    productos = Catalog.objects.all()

    if q:
        # Buscar coincidencias en el nombre o en la categoría
        productos = productos.filter(
            Q(name__icontains=q) |
            Q(category__icontains=q)
        )

    serializer = CatalogSerializer(productos, many=True)
    return Response(serializer.data)
