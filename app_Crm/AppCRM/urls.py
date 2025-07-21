from django.urls import path
from . import views



urlpatterns = [
    path ('', views.pg_inicio, name='pg_inicio'), #aqui se da visibilidad a los links de la aplicacion ESTE ES EL INDEX.HTML
    path (' Estudiantes/', views.pg_Estudiantes, name='pg_Estudiantes'),
    path ('Docentes/', views.pg_Docentes, name='pg_Docentes'),
    path ('clases/', views.pg_Clases, name='pg_Clases'),
    path ('pagos/', views.pg_Pagos, name='pg_Pagos'),
    path ('inscripciones/', views.Inscripciones, name='Inscripciones'),


]