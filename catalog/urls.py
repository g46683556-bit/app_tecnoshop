from django.urls import path
from .views import *

urlpatterns = [
    path('', catalog, name='catalog'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    # API para FastAPI o Postman
    path('api/productos/', productos_api, name='productos_api'),
    path('exportar/catalogo/pdf/', export_catalog_pdf, name='export_catalog_pdf'),
]