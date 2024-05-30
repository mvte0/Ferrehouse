from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
#Modelos
#PRODUCTOS
class Marca(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
        
class Producto(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    codigo = models.IntegerField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="producto", null=True)
    
    def __str__(self):
        return self.nombre

#CARRO DE COMPRA
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

#PROCESOS
class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    producto = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cliente} - {self.producto}"
    
class Boleta(models.Model):
    id_boleta = models.CharField(max_length=50, unique=True,  primary_key=True)
    cliente = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        return f'{self.id_boleta} - {self.cliente}'

#INFO
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
    
#USUARIOS
class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.user.email
    
class EmployeeProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f'{self.user.email} - {self.user_type}'