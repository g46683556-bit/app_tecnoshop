from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Catalog

class CatalogResource(resources.ModelResource):
    class Meta:
        model = Catalog
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "price",
            "discount_percent",
            "discount_price",
            "stock",
            "image_url",
            "category",
        )

@admin.register(Catalog)
class CatalogAdmin(ImportExportModelAdmin):
    resource_class = CatalogResource
    list_display = ("name", "category", "price", "discount_percent", "final_price", "stock")
    list_filter = ("category",)
    search_fields = ("name",)
