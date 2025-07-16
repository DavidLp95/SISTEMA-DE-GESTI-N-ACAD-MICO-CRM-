from django.shortcuts import render #muestra archivos html
from django.http import HttpResponse #muestra funciones o respuestas predeterminadas

# Create your views here.


def hola(request):
    return render(request,'AppCRM/index.html')
