from functools import wraps

from django.shortcuts import redirect

# Qué módulos puede ver cada rol
ACCESO_POR_ROL = {
    'gerente': {'clientes', 'empleados', 'mesas', 'platos', 'ordenes', 'facturas'},
    'staff': {'clientes', 'empleados', 'mesas', 'platos', 'ordenes', 'facturas'},
    'mesero': {'clientes', 'mesas', 'platos', 'ordenes'},
    'contador': {'platos', 'ordenes', 'facturas'},
}

# Nombre de modelo en URLs CRUD → nombre de módulo en ACCESO_POR_ROL
MODULO_POR_MODELO = {
    'cliente': 'clientes',
    'empleado': 'empleados',
    'mesa': 'mesas',
    'plato': 'platos',
    'orden': 'ordenes',
    'factura': 'facturas',
}


def tiene_acceso(perfil, modulo):
    """Retorna True si el perfil tiene acceso al módulo dado."""
    if perfil is None:
        return False
    return modulo in ACCESO_POR_ROL.get(perfil.rol, set())


def requiere_rol(*modulos_permitidos):
    """
    Decorador para vistas. Recibe uno o más nombres de módulo.
    Redirige a 'acceso_denegado' si el usuario no tiene permiso.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                perfil = request.user.perfil
            except Exception:
                return redirect('acceso_denegado')

            rol = perfil.rol
            permitidos = ACCESO_POR_ROL.get(rol, set())

            if not any(m in permitidos for m in modulos_permitidos):
                return redirect('acceso_denegado')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
