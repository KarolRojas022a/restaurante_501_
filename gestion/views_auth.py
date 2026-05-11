from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import IngresoUsuarioForm, RegistroUsuarioForm


def proteccion_sesion(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    return render(request, 'gestion/auth/proteccion_sesion.html')


def vista_ingresar(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = IngresoUsuarioForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('inicio')
    else:
        form = IngresoUsuarioForm(request)
    return render(request, 'gestion/auth/ingresar.html', {'form': form})


def vista_registrar(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingresar')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'gestion/auth/registrar.html', {'form': form})


def vista_salir(request):
    if request.method == 'POST':
        logout(request)
    return redirect('requiere_acceso')
