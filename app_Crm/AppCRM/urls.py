from django.urls import path
from . import views



urlpatterns = [
    path ('', views.hola, name='hola'), #aqui se da visibilidad a los links de la aplicacion 


]