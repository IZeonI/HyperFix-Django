from django.shortcuts import render, get_object_or_404
from .models import Componentes

def lista_componentes(request):
    componentes = Componentes.objects.all()
    return render(request, 'productos/componentes.html', {'componentes': componentes})

def detalle_producto(request, id):
    componente = get_object_or_404(Componentes, id=id)
    return render(request, 'productos/detalle_producto.html', {'componente': componente})