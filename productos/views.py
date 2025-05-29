from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Componentes

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('lista_componentes')  
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lista_componentes') 
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def lista_componentes(request):
    componentes = Componentes.objects.all()
    return render(request, 'productos/componentes.html', {'componentes': componentes})

def detalle_producto(request, id):
    componente = get_object_or_404(Componentes, id=id)
    return render(request, 'productos/detalle_producto.html', {
        'componente': componente,
    })

def carrusel_componentes(request):
    componentes = Componentes.objects.order_by('?')[:15]
    return render(request, 'productos/carrusel.html', {
        'componentes': componentes,
    })

@login_required(login_url='login')
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    subtotal = 0
    total_articulos = 0

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Componentes, pk=producto_id)
        total_item = producto.precio * cantidad
        subtotal += total_item
        total_articulos += cantidad
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': total_item
        })

    envio = 150
    total = subtotal + envio

    return render(request, 'productos/carrito.html', {
        'items': items,
        'subtotal': subtotal,
        'envio': envio,
        'total': total,
        'total_articulos': total_articulos
    })

@login_required(login_url='login')
def perfil_usuario(request):
    return render(request, 'productos/perfil.html', {
        'usuario': request.user
    })

def procesar_pago(request):
    # Lógica de pago o redirección
    return HttpResponse("Procesando pago...")

@login_required(login_url='login')
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Componentes, pk=producto_id)
    carrito = request.session.get('carrito', {})
    cantidad_actual = carrito.get(str(producto_id), 0)

    # Leer cantidad enviada en POST, si no hay, usar 1 por defecto
    cantidad_a_agregar = 1
    if request.method == 'POST':
        try:
            cantidad_a_agregar = int(request.POST.get('cantidad', 1))
            if cantidad_a_agregar < 1:
                cantidad_a_agregar = 1
        except ValueError:
            cantidad_a_agregar = 1

    nueva_cantidad = cantidad_actual + cantidad_a_agregar
    # Verificación de stock
    if nueva_cantidad > producto.stock:
        nueva_cantidad = producto.stock

    carrito[str(producto_id)] = nueva_cantidad
    request.session['carrito'] = carrito

    # Redirigir a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'lista_componentes'))


def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
    if producto_id_str in carrito:
        del carrito[producto_id_str]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')

def disminuir_cantidad(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
    
    if producto_id_str in carrito:
        if carrito[producto_id_str] > 1:
            carrito[producto_id_str] -= 1
        else:
            del carrito[producto_id_str]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')
