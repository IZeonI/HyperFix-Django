from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib import messages
from .models import Componentes
from clientes.models import Cliente
from ventas.models import Ticket, TicketComponente
from empleados.models import Empleados
from .forms import DatosClienteForm

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('completar_datos_cliente')  
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def completar_datos_cliente(request):
    if request.method == 'POST':
        form = DatosClienteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            correo = form.cleaned_data['correo']

            # Actualizar datos del modelo User
            user = request.user
            user.first_name = nombre
            user.last_name = apellido
            user.email = correo
            user.save()

            # Registrar en tabla Cliente
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo
            )

            return redirect('lista_componentes') 
    else:
        form = DatosClienteForm()

    return render(request, 'usuarios/completar_datos_cliente.html', {'form': form})

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

@login_required
def procesar_pago(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "El carrito está vacío.")
        return redirect('ver_carrito')

    # Obtener cliente asociado al usuario actual
    try:
        cliente = Cliente.objects.get(nombre=request.user.first_name)
    except Cliente.DoesNotExist:
        return HttpResponse("Cliente no encontrado. Completa tus datos primero.")

    # Obtener empleado fijo
    try:
        empleado = Empleados.objects.get(rfc_empleado='ABCD123456EFG')
    except Empleados.DoesNotExist:
        return HttpResponse("Empleado no encontrado.")

    # Calcular total
    subtotal = 0
    for producto_id, cantidad in carrito.items():
        producto = Componentes.objects.get(pk=producto_id)
        subtotal += producto.precio * cantidad
    envio = 150
    total = subtotal + envio

    # Crear ticket
    ticket = Ticket.objects.create(
        fecha=timezone.now(),
        total=total,
        id_cliente=cliente,
        rfc_empleado=empleado
    )

    # Guardar detalles en TicketComponente
    for producto_id, cantidad in carrito.items():
        producto = Componentes.objects.get(pk=producto_id)
        TicketComponente.objects.create(
            id_ticket=ticket,
            id_componente=producto,
            cantidad=cantidad
        )

    # Limpiar carrito
    request.session['carrito'] = {}

    messages.success(request, "Pago procesado correctamente. Gracias por su compra.")

    return redirect('ver_carrito')

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
