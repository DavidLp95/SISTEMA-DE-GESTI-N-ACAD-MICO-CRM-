
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AppCRM.urls')), #conectar las rutas del proyecto a la del proyecto general 
]
