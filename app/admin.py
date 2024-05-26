from django.contrib import admin
from .models import Marca, Producto, Contacto, Boleta

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["marca", "nombre", "codigo", "precio"]
    list_editable = ["precio"]
    search_fields = ["nombre"]
    list_filter = ["marca"]
    list_per_page = 8

admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)
admin.site.register(Boleta)


