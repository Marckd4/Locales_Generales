from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from localesGenerales.forms import ProductoForm
from .models import Inventario

def index(request):
    productos = Inventario.objects.all()
    
    return render(
        request,'index.html',context={'inventario':productos})
    


def error_404_view(request, exception):
    return render(request, '404.html', status=404)


def formulario(request):
    if request.method =='POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/localesGenerales')
            
    else:
        form = ProductoForm
        
    return render( request, 'producto_form.html',{'form': form})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Inventario

@csrf_exempt
def actualizar_conteo(request):
    if request.method == "POST":
        item_id = request.POST.get("id")
        campo = request.POST.get("campo")
        valor = request.POST.get("valor")

        item = Inventario.objects.get(id=item_id)
        setattr(item, campo, valor)
        item.save()

        return JsonResponse({
            "diferencia": item.diferencia
        })


def to_int(valor):
    try:
        if valor in (None, '', ' '):
            return 0
        return int(valor)
    except (ValueError, TypeError):
        return 0
    
    
    
import openpyxl
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inventario

def importar_excel(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']

        if not archivo.name.endswith('.xlsx'):
            messages.error(request, "El archivo debe ser .xlsx")
            return redirect('importar_excel')

        wb = openpyxl.load_workbook(archivo, data_only=True)
        hoja = wb.active

        for fila in hoja.iter_rows(min_row=2, values_only=True):
            Inventario.objects.update_or_create(
                cod_sistema=str(fila[3]).strip() if fila[3] else '',
                defaults={
                    'ubicacion': fila[0] or '',
                    'cod_ean': fila[1] or '',
                    'cod_dun': fila[2] or '',
                    'descripcion': fila[4] or '',
                    'categoria': fila[5] or '',
                    'conteo_01': to_int(fila[6]),
                    'conteo_02': to_int(fila[7]),
                }
            )

        messages.success(request, "Excel importado correctamente")
        return redirect('index')

    return render(request, 'importar_excel.html')




import openpyxl
from django.http import HttpResponse
from .models import Inventario

def exportar_excel(request):
    # Crear libro y hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventario"

    # Cabeceras
    columnas = [
        'Ubicación',
        'Cod EAN',
        'Cod DUN',
        'Cod Sistema',
        'Descripción',
        'Categoría',
        'Conteo 01',
        'Conteo 02',
        'Diferencia',
        'Fecha Creación',
    ]
    ws.append(columnas)

    # Datos
    for item in Inventario.objects.all().order_by('id'):
        ws.append([
            item.ubicacion,
            item.cod_ean,
            item.cod_dun,
            item.cod_sistema,
            item.descripcion,
            item.categoria,
            item.conteo_01,
            item.conteo_02,
            item.diferencia,
            item.creado.strftime('%d-%m-%Y %H:%M'),
        ])

    # Respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=inventario.xlsx'

    wb.save(response)
    return response
