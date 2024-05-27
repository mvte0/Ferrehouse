from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
        
class Producto(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    codigo = models.IntegerField()
    descripcion = models.TextField()
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to="producto", null=True)
    
    def __str__(self):
        return self.nombre


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

opciones_motivos = [
    [0, "reclamo"],
    [1, "sugerencia"],
    [2, "ayuda"],
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    rut = models.CharField(max_length=10)
    motivo = models.IntegerField(choices=opciones_motivos)
    mensaje = models.TextField()
    
    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    producto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cliente} - {self.producto}"
    
class Boleta(models.Model):
    id_boleta = models.CharField(max_length=50, primary_key=True)
    cliente = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        return self.id_boleta
    
    