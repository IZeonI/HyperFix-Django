from django.shortcuts import render

from .models import Componentes

def lista_componentes(request):
    componentes = Componentes.objects.all()
    return render(request, 'productos/componentes.html', {'componentes': componentes})