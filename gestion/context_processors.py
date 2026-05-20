from .models import Perfil


def perfil_cuenta(request):
    """Expone `perfil_cuenta` en plantillas sin asumir que existe (evita excepciones)."""
    if not request.user.is_authenticated:
        return {'perfil_cuenta': None}
    try:
        return {'perfil_cuenta': request.user.perfil}
    except Perfil.DoesNotExist:
        return {'perfil_cuenta': None}
