from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/<str:error>/', views.carrito, name='carrito_con_error'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login, name='login'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('producto/<int:producto_id>/', views.producto, name='producto'),
    path('recuperarcontraseña/', views.recuperarcontraseña, name='recuperarcontraseña'),
    path('tienda1/', views.tienda1, name='tienda'),
    path('contador/', views.contador, name='contador'),
    path('bodeguero/', views.bodeguero, name='bodeguero'),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('ingreso_boletas/', views.ingreso_boletas, name='ingreso_boletas'),
    path('pago_iniciar/', views.pago_iniciar, name='pago_iniciar'),
    path('pago_exito/', views.pago_exito, name='pago_exito'),
]
