from django.urls import path
from . import views
from . import views_auth

urlpatterns = [
    path('acceso/', views_auth.proteccion_sesion, name='requiere_acceso'),
    path('ingresar/', views_auth.vista_ingresar, name='ingresar'),
    path('registrar/', views_auth.vista_registrar, name='registrar'),
    path('salir/', views_auth.vista_salir, name='salir'),

    path('', views.inicio, name='inicio'),
    
    # Rutas para ver Listas
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('platos/', views.lista_platos, name='lista_platos'),
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('facturas/', views.lista_facturas, name='lista_facturas'),

    # Rutas para Registrar (Create)
    path('clientes/nuevo/', views.gestionar_registro, {'modelo': 'cliente'}, name='crear_cliente'),
    path('empleados/nuevo/', views.gestionar_registro, {'modelo': 'empleado'}, name='crear_empleado'),
    path('mesas/nuevo/', views.gestionar_registro, {'modelo': 'mesa'}, name='crear_mesa'),
    path('platos/nuevo/', views.gestionar_registro, {'modelo': 'plato'}, name='crear_plato'),
    path('ordenes/nuevo/', views.gestionar_registro, {'modelo': 'orden'}, name='crear_orden'),
    path('facturas/nuevo/', views.gestionar_registro, {'modelo': 'factura'}, name='crear_factura'),


   # ==========================================
    # RUTAS PARA EDITAR (Update)
    # ==========================================
    path('clientes/editar/<int:pk>/', views.gestionar_registro, {'modelo': 'cliente'}, name='editar_cliente'),
    path('empleados/editar/<int:pk>/', views.gestionar_registro, {'modelo': 'empleado'}, name='editar_empleado'),
    path('mesas/editar/<int:pk>/', views.gestionar_registro, {'modelo': 'mesa'}, name='editar_mesa'),
    path('platos/editar/<int:pk>/', views.gestionar_registro, {'modelo': 'plato'}, name='editar_plato'),
    path('ordenes/editar/<int:pk>/', views.gestionar_registro, {'modelo': 'orden'}, name='editar_orden'),
    path('facturas/editar/<int:pk>/', views.gestionar_registro, {'modelo': 'factura'}, name='editar_factura'),

    # ==========================================
    # RUTAS PARA ELIMINAR (Delete)
    # ==========================================
    path('clientes/eliminar/<int:pk>/', views.eliminar_registro, {'modelo': 'cliente'}, name='eliminar_cliente'),
    path('empleados/eliminar/<int:pk>/', views.eliminar_registro, {'modelo': 'empleado'}, name='eliminar_empleado'),
    path('mesas/eliminar/<int:pk>/', views.eliminar_registro, {'modelo': 'mesa'}, name='eliminar_mesa'),
    path('platos/eliminar/<int:pk>/', views.eliminar_registro, {'modelo': 'plato'}, name='eliminar_plato'),
    path('ordenes/eliminar/<int:pk>/', views.eliminar_registro, {'modelo': 'orden'}, name='eliminar_orden'),
    path('facturas/eliminar/<int:pk>/', views.eliminar_registro, {'modelo': 'factura'}, name='eliminar_factura'),
]

