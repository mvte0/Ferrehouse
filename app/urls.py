from django.urls import path, include
from . import views
from .views import (index, base, carrito, contacto, login, nosotros, 
                    producto, recuperarcontraseña, registro, tienda,
                    contador, bodeguero)

urlpatterns = [
    path('index/', index, name="index"),
    path('base/', base, name="base"),
    path('carrito/', carrito, name="carrito"),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('contacto/', contacto, name="contacto"),
    path('login/', login, name="login"),
    path('nosotros/', nosotros, name="nosotros"),
    path('producto/<int:producto_id>/', producto, name="producto"),
    path('recuperarcontraseña/', recuperarcontraseña, name="recuperarcontraseña"),
    path('registro/', registro, name="registro"),
    path('tienda/', tienda, name="tienda"),
    path('contador/', contador, name="contador"),
    path('bodeguero/', bodeguero, name="bodeguero"),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('ingreso_boletas/', views.ingreso_boletas, name='ingreso_boletas')
]