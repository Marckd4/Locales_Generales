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
