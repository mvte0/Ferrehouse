from django.shortcuts import render, get_object_or_404, redirect
import requests 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from .models import Producto, Contacto, Pedido, Cart, CartItem, Marca, Boleta
from .forms import ContactoForm, ProductoForm, BoletaForm
from django.contrib.auth.decorators import login_required
from transbank.webpay.webpay_plus.transaction import Transaction

#inicio
def index(request):
    return render(request, 'app/index.html')

def base(request):
    return render(request, 'app\base.html')

#TIENDA
def tienda1(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/tienda1.html', data)

def producto(request, producto_id): 
    producto = get_object_or_404(Producto, id=producto_id)
    data ={
        'producto' : producto
    }
    return render(request, 'app/producto.html', data)

#CARRO DE COMPRA
def carrito(request, error=None):
    cart, created = Cart.objects.get_or_create(user=request.user, estado='pendiente')
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.producto.precio * item.cantidad for item in cart_items)
    return render(request, 'app/carrito.html', {'cart_items': cart_items, 'total_price': total_price, 'error': error})

def agregar_al_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))
        producto = get_object_or_404(Producto, id=producto_id)
        
        cart, created = Cart.objects.get_or_create(user=request.user, estado='pendiente')
        cart_item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)
        
        if not created:
            cart_item.cantidad += cantidad
        else:
            cart_item.cantidad = cantidad
        cart_item.save()
        
        return redirect('carrito')

def eliminar_del_carrito(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return JsonResponse({'status': 'ok', 'message': 'Producto eliminado del carrito'})

def actualizar_carrito(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cantidad = int(request.POST.get('cantidad'))
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.cantidad = cantidad
        cart_item.save()
        return JsonResponse({'status': 'ok', 'message': 'Cantidad actualizada'})

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
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contador')
    else:
        form = BoletaForm()
    boletas = Boleta.objects.all()
    return render(request, 'app/CRUD/contador.html', {'form': form, 'boletas': boletas})

def ingreso_boletas(request):
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contador')
    else:
        form = BoletaForm()
    return render(request, 'app/CRUD/contador.html', {'form': form})

# API Transbank
@login_required
def pago_iniciar(request):
    # Obtén el carrito del usuario con estado 'pendiente'
    cart, created = Cart.objects.get_or_create(user=request.user, estado='pendiente')
    carrito = CartItem.objects.filter(cart=cart)
    
    # Calcula el total del carrito
    total = sum(item.producto.precio * item.cantidad for item in carrito)
    
    # Configura la transacción de Webpay
    tx = Transaction()
    response = tx.create(
        buy_order=str(request.user.id) + str(carrito.first().id),
        session_id=request.session.session_key,
        amount=total,
        return_url="http://127.0.0.1:8000/pago_exito/"
    )
    
    if request.method == 'POST':
        # Crear el pedido después de confirmar el pago
        pedido = Pedido.objects.create(user=request.user, total=total)
        for item in carrito:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.producto.precio
            )
        cart.estado = 'completado'
        cart.save()
        return redirect('pago_exito')

    return render(request, 'app/pago_iniciar.html', {'response': response, 'total': total})

def pago_exito(request):
    token = request.GET.get('token_ws')
    tx = Transaction()
    response = tx.commit(token)
    
    if response['response_code'] == 0:  # Transacción exitosa
        # Obtén el carrito pendiente del usuario
        carrito = Cart.objects.filter(user=request.user, estado='pendiente').first()
        if carrito:
            # Actualiza el estado del carrito
            carrito.estado = 'pagado'
            carrito.save()
        
        # Obtén todos los ítems del carrito y realiza cualquier acción adicional necesaria
        cart_items = CartItem.objects.filter(cart=carrito)
        # Aquí puedes añadir lógica adicional, como enviar un email de confirmación
        
        return render(request, 'app/pago_exito.html', {'response': response})
    else:
        return render(request, 'app/pago_error.html', {'response': response})

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