from django.test import TestCase
from app.models import Marca, Producto, Cart, CartItem, Pedido, PedidoItem, Boleta, Contacto
from django.contrib.auth.models import User
from app.forms import ContactoForm, ProductoForm, BoletaForm
from django.urls import reverse

class MarcaModelTest(TestCase):

    def test_create_marca(self):
        marca = Marca.objects.create(nombre="Test Marca")
        self.assertEqual(marca.nombre, "Test Marca")
        self.assertEqual(str(marca), "Test Marca")