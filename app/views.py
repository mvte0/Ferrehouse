from django.shortcuts import render, get_object_or_404, redirect
import requests 
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from .models import Producto, Contacto, Pedido, Cart, CartItem, Marca, Boleta
from .forms import ContactoForm, ProductoForm, BoletaForm
from django.contrib.auth.decorators import login_required
from transbank.webpay.webpay_plus.transaction import Transaction

def iniciar_pago(request):
    buy_order = 'orden12345'  # Debe ser único por cada transacción
    session_id = 'session12345'
    amount = 10000  # Monto de la transacción
    return_url = 'http://localhost:8000/pago/exito/'  # URL a donde será redirigido el usuario después del pago

    tx = Transaction(webpay_plus_commons=settings.TRANSBANK_ENVIRONMENT)
    response = tx.create(buy_order, session_id, amount, return_url)

    return render(request, 'pago/iniciar.html', {
        'url_tbk': response['url'],
        'token_tbk': response['token']
    })

def pago_exito(request):
    token = request.GET.get('token_ws')
    tx = Transaction(webpay_plus_commons=settings.TRANSBANK_ENVIRONMENT)
    response = tx.commit(token)

    if response['response_code'] == 0:
        # Pago exitoso
        return render(request, 'pago/exito.html', {'response': response})
    else:
        # Error en el pago
        return render(request, 'pago/error.html', {'response': response})

# Create your views here.
def index(request):
    return render(request, 'app/index.html')

def base(request):
    return render(request, 'app\base.html')

#TIENDA
def tienda(request):
    productos = Producto.objects.all()
    print(productos)
    data = {
        'productos': productos
    }
    return render(request, 'app/tienda.html', data)

def producto(request, producto_id): 
    producto = get_object_or_404(Producto, id=producto_id)
    data ={
        'producto' : producto
    }
    return render(request, 'app/producto.html', data)

#CARRO DE COMPRA
@login_required
def agregar_al_carrito(request):
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    producto = get_object_or_404(Producto, id=producto_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)
    
    if not created:
        cart_item.quantity += cantidad
    else:
        cart_item.quantity = cantidad
    cart_item.save()
    
    return JsonResponse({'status': 'ok'})

@login_required
def eliminar_del_carrito(request):
    cart_item_id = request.POST.get('cart_item_id')
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    
    return JsonResponse({'status': 'ok'})

@login_required
def actualizar_carrito(request):
    cart_item_id = request.POST.get('cart_item_id')
    cantidad = int(request.POST.get('cantidad'))
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity = cantidad
    cart_item.save()
    
    return JsonResponse({'status': 'ok'})

@login_required
def carrito(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = 0
    for item in cart_items:
        item.total_price = item.producto.precio * item.quantity
        total_price += item.total_price
    
    return render(request, 'app/carrito.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

#INFO
def contacto(request):
    mensaje = ""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "Contacto guardado con éxito"
        else:
            mensaje = "Hubo un error en el formulario"
    else:
        form = ContactoForm()
    
    return render(request, 'app/contacto.html', {'form': form, 'mensaje': mensaje})

def login(request): 
    return render(request, 'app/login.html')

def nosotros(request): 
    return render(request, 'app/nosotros.html')

def recuperarcontraseña(request): 
    return render(request, 'app/recuperar-contraseña.html')

def registro(request): 
    return render(request, 'app/registro.html')

#EMPLEADOS
def bodeguero(request):
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()
    marcas = Marca.objects.all()
    form = None
    edit_producto_id = None

    if 'edit_producto_id' in request.GET:
        edit_producto_id = request.GET.get('edit_producto_id')
        producto = get_object_or_404(Producto, id=edit_producto_id)
        form = ProductoForm(instance=producto)

    if request.method == 'POST':
        if 'add-product' in request.POST:
            add_form = ProductoForm(request.POST, request.FILES)
            if add_form.is_valid():
                add_form.save()
                return redirect('bodeguero')
        elif 'edit-product' in request.POST:
            edit_producto_id = request.POST.get('edit_producto_id')
            producto = get_object_or_404(Producto, id=edit_producto_id)
            form = ProductoForm(request.POST, request.FILES, instance=producto)
            if form.is_valid():
                form.save()
                return redirect('bodeguero')
        elif 'delete-product' in request.POST:
            delete_producto_id = request.POST.get('delete_producto_id')
            print(f"ID de producto a eliminar recibido: {delete_producto_id}")  # Línea de depuración
            if delete_producto_id:  # Verificar que delete_producto_id no esté vacío
                producto = get_object_or_404(Producto, id=delete_producto_id)
                producto.delete()
                return redirect('bodeguero')
            else:
                print("ID de producto a eliminar no recibido o está vacío.")  # Mensaje de depuración

    add_form = ProductoForm()

    return render(request, 'app/CRUD/bodeguero.html', {
        'pedidos': pedidos,
        'productos': productos,
        'form': form,
        'edit_producto_id': edit_producto_id,
        'add_form': add_form,
        'marcas': marcas,
    })

def contador(request):
    return render(request, 'app/CRUD/contador.html')

def ingreso_boletas(request):
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingreso_boletas')
    else:
        form = BoletaForm()
    boletas = Boleta.objects.all()
    return render(request, 'ingreso_boletas.html', {'form': form, 'boletas': boletas})

#APIS
def indicadores(request):
    try:
        response = requests.get('https://mindicador.cl/api')
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {}
        error_message = f'Error al obtener los indicadores: {e}'
        return render(request, 'app/indicadores.html', {'data': data, 'error_message': error_message})
    
    return render(request, 'app/indicadores.html', {'data': data})