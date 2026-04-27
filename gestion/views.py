from django.shortcuts import render

# Create your views here.
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura

def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_Platos': Plato.objects.count(),
        'total_Ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }
    return render(request,'gestion/inicio.html',context)

def lista_clientes (request):
    clientes = Cliente.objects.all()
    return render(request,'gestion/clientes.html', {'clientes':clientes})
 
 
def lista_empleados (request):
    Empleados = Empleado.objects.all()
    return render(request,'gestion/empleados.html', {'empleados':Empleados})

def lista_mesas (request):
    Mesas = Mesa.objects.all()
    return render(request,'gestion/mesas.html',{'mesas':Mesas})

def lista_ordenes (request):
    ordenes = Orden.objects.all()
    return render(request,'gestion/ordenes.html',{'ordenes':ordenes})


def lista_platos (request):
    platos = platos.objects.all()
    return render(request,'gestion/platos.html',{'platos':platos})

def lista_facturas (request):
    facturas = Factura.objects.all()
    return render(request,'gestion/facturas.html',{'facturas':facturas})