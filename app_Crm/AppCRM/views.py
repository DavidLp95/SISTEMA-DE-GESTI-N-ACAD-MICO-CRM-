from django.shortcuts import render #muestra archivos html
from django.http import HttpResponse #muestra funciones o respuestas predeterminadas

# Create your views here.


def pg_inicio(request):
    return render(request,'AppCRM/index.html')

# emplear urls.py para crear las rutas de las vistas----------
def pg_Estudiantes(request):
    return render(request,'AppCRM/Estudiantes.html')

def pg_Docentes(request):
    return render(request,'AppCRM/Docentes.html')

def pg_Clases(request):
    return render(request,'AppCRM/Clases.html')

def pg_Pagos(request):
    return render(request,'AppCRM/Pagos.html')

def Inscripciones(request):
    return render(request,'AppCRM/Inscripciones.html')

