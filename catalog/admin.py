# from django.contrib import admin
# from .models import Catalog

# # @admin.register(Catalog)
# # class CatalogAdmin(admin.ModelAdmin):
# #     list_display = ("nombre", "categoria", "precio")
# #     list_filter = ("categoria",)
# #     search_fields = ("nombre",)

# admin.site.register(Catalog)

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Catalog


# Definir el recurso de importación/exportación
class CatalogResource(resources.ModelResource):
    class Meta:
        model = Catalog
        # (Opcional) Puedes elegir qué campos importar/exportar:
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "image_url",
            "category",
        )


# Registrar el modelo con la funcionalidad de import/export
@admin.register(Catalog)
class CatalogAdmin(ImportExportModelAdmin):
    resource_class = CatalogResource
    list_display = ("name", "category", "price", "stock")
    list_filter = ("category",)
    search_fields = ("name",)
