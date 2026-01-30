from django.contrib import admin
from .models import Inventario

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = (
        'ubicacion',
        'cod_ean',
        'cod_sistema',
        'descripcion',
        'conteo_01',
        'conteo_02',
        'diferencia'
    )
    search_fields = ('cod_ean', 'cod_sistema', 'descripcion')
    list_filter = ('ubicacion', 'categoria')
