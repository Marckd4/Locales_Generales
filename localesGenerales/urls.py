from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('formulario', views.formulario, name='formulario'),
    path('actualizar-conteo/', views.actualizar_conteo, name='actualizar_conteo'),
    path('importar-excel/', views.importar_excel, name='importar_excel'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('editar/<int:pk>/', views.editar_inventario, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_inventario, name='eliminar'),


]
