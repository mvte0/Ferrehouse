from django.test import TestCase
from django.contrib.auth.models import User
from .models import Marca, Producto, Cart, CartItem, Pedido, PedidoItem, Boleta, Contacto
from .forms import ContactoForm, ProductoForm, BoletaForm
from django.urls import reverse

class MarcaModelTest(TestCase):

    def test_create_marca(self):
        marca = Marca.objects.create(nombre="Test Marca")
        self.assertEqual(marca.nombre, "Test Marca")
        self.assertEqual(str(marca), "Test Marca")

class ProductoModelTest(TestCase):

    def setUp(self):
        self.marca = Marca.objects.create(nombre="Test Marca")

    def test_create_producto(self):
        producto = Producto.objects.create(
            marca=self.marca,
            nombre="Test Producto",
            codigo=123456,
            descripcion="Descripción de prueba",
            precio=1000.00
        )
        self.assertEqual(producto.nombre, "Test Producto")
        self.assertEqual(producto.marca.nombre, "Test Marca")
        self.assertEqual(str(producto), "Test Producto")

class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_cart(self):
        cart = Cart.objects.create(user=self.user, estado='pendiente')
        self.assertEqual(cart.user.username, 'testuser')
        self.assertEqual(cart.estado, 'pendiente')
        self.assertEqual(str(cart), f"{self.user} - pendiente")

class CartItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.marca = Marca.objects.create(nombre="Test Marca")
        self.producto = Producto.objects.create(
            marca=self.marca,
            nombre="Test Producto",
            codigo=123456,
            descripcion="Descripción de prueba",
            precio=1000.00
        )
        self.cart = Cart.objects.create(user=self.user, estado='pendiente')

    def test_create_cart_item(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            producto=self.producto,
            cantidad=2
        )
        self.assertEqual(cart_item.cantidad, 2)
        self.assertEqual(cart_item.producto.nombre, "Test Producto")
        self.assertEqual(cart_item.total_price, 2000.00)
        self.assertEqual(str(cart_item), "2 x Test Producto")

class PedidoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_pedido(self):
        pedido = Pedido.objects.create(
            user=self.user,
            total=2000.00,
            estado='pendiente'
        )
        self.assertEqual(pedido.user.username, 'testuser')
        self.assertEqual(pedido.total, 2000.00)
        self.assertEqual(pedido.estado, 'pendiente')

class PedidoItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.marca = Marca.objects.create(nombre="Test Marca")
        self.producto = Producto.objects.create(
            marca=self.marca,
            nombre="Test Producto",
            codigo=123456,
            descripcion="Descripción de prueba",
            precio=1000.00
        )
        self.pedido = Pedido.objects.create(
            user=self.user,
            total=2000.00,
            estado='pendiente'
        )

    def test_create_pedido_item(self):
        pedido_item = PedidoItem.objects.create(
            pedido=self.pedido,
            producto=self.producto,
            cantidad=2,
            precio=1000.00
        )
        self.assertEqual(pedido_item.cantidad, 2)
        self.assertEqual(pedido_item.producto.nombre, "Test Producto")
        self.assertEqual(pedido_item.precio, 1000.00)

class BoletaModelTest(TestCase):

    def test_create_boleta(self):
        boleta = Boleta.objects.create(
            id_boleta='12345',
            cliente='Test Cliente',
            monto=5000.00,
            fecha='2024-06-18'
        )
        self.assertEqual(boleta.id_boleta, '12345')
        self.assertEqual(boleta.cliente, 'Test Cliente')
        self.assertEqual(boleta.monto, 5000.00)
        self.assertEqual(str(boleta), '12345 - Test Cliente')

class ContactoModelTest(TestCase):

    def test_create_contacto(self):
        contacto = Contacto.objects.create(
            nombre='Juan Pérez',
            rut='12345678-9',
            motivo=1,
            mensaje='Este es un mensaje de prueba.'
        )
        self.assertEqual(contacto.nombre, 'Juan Pérez')
        self.assertEqual(contacto.rut, '12345678-9')
        self.assertEqual(contacto.motivo, 1)
        self.assertEqual(contacto.mensaje, 'Este es un mensaje de prueba.')
        self.assertEqual(str(contacto), 'Juan Pérez')

class ContactoFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'nombre': 'Juan Pérez',
            'rut': '12345678-9',
            'motivo': 1,
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'nombre': '',
            'rut': '',
            'motivo': '',
            'mensaje': ''
        }
        form = ContactoForm(data=data)
        self.assertFalse(form.is_valid())

class ProductoFormTest(TestCase):

    def test_valid_form(self):
        marca = Marca.objects.create(nombre="Test Marca")
        data = {
            'marca': marca.id,
            'nombre': 'Test Producto',
            'codigo': 123456,
            'descripcion': 'Descripción de prueba',
            'precio': 1000.00
        }
        form = ProductoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'nombre': '',
            'codigo': '',
            'descripcion': '',
            'precio': ''
        }
        form = ProductoForm(data=data)
        self.assertFalse(form.is_valid())

class BoletaFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'id_boleta': '12345',
            'cliente': 'Test Cliente',
            'monto': 5000.00,
            'fecha': '2024-06-18'
        }
        form = BoletaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'id_boleta': '',
            'cliente': '',
            'monto': '',
            'fecha': ''
        }
        form = BoletaForm(data=data)
        self.assertFalse(form.is_valid())

class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.marca = Marca.objects.create(nombre="Test Marca")
        self.producto = Producto.objects.create(
            marca=self.marca,
            nombre="Test Producto",
            codigo=123456,
            descripcion="Descripción de prueba",
            precio=1000.00
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inicio')

    def test_contacto_view(self):
        response = self.client.get(reverse('contacto'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contacto')

    def test_tienda_view(self):
        response = self.client.get(reverse('tienda'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tienda')

    def test_producto_detail_view(self):
        response = self.client.get(reverse('producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Producto')

    def test_carrito_view(self):
        response = self.client.get(reverse('carrito'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carrito')

    def test_agregar_al_carrito_view(self):
        response = self.client.post(reverse('agregar_al_carrito'), {'producto_id': self.producto.id, 'cantidad': 2})
        self.assertEqual(response.status_code, 302)  # Redirección después de añadir al carrito

    def test_eliminar_del_carrito_view(self):
        cart = Cart.objects.create(user=self.user, estado='pendiente')
        cart_item = CartItem.objects.create(cart=cart, producto=self.producto, cantidad=2)
        response = self.client.post(reverse('eliminar_del_carrito'), {'cart_item_id': cart_item.id})
        self.assertEqual(response.status_code, 200)

    def test_actualizar_carrito_view(self):
        cart = Cart.objects.create(user=self.user, estado='pendiente')
        cart_item = CartItem.objects.create(cart=cart, producto=self.producto, cantidad=2)
        response = self.client.post(reverse('actualizar_carrito'), {'cart_item_id': cart_item.id, 'cantidad': 3})
        self.assertEqual(response.status_code, 200)
