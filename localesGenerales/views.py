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