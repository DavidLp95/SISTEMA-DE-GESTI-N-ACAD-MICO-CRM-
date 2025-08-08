from django.shortcuts import render, redirect #muestra archivos html
from django.http import HttpResponse #muestra funciones o respuestas predeterminadas
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from AppCRM.models import Usuario  # Import the Usuario model
from django.contrib import messages
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # autenticacion del usuario usando el backend 
        user = authenticate(request, username= email, password =password ) 

        if user is not None:
            # verifica que sea el estudiante
            if user.rol == 'estudiante':
                # inicio de sesion
                login(request, user)
                return redirect('perfilEstudiante') #dashboard
            else:
                messages.error(request, 'Solo ingreso a estudiantes. ')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
        
    return render(request,'AppCRM/Inscripciones.html')





def recuperar_contraseña(request):
    return render(request, 'AppCRM/recuperar.html')






# interface personalizada login estudiantes:

@login_required
def perfilEstudiante(request):
    # aqui modificamos los datos que se veran en el perfil personalizado 
    user = request.user
    estudiante = None
    if hasattr(user, 'estudiante'):
        estudiante = user.estudiante  # Assuming a OneToOneField from Usuario to Estudiante
    # return render(request, 'AppCRM/perfilEstudiante.html', {'usuario': user, 'estudiante': estudiante})
    return render(request, 'AppCRM/perfilEstudiante.html', {'usuario':'usuario'})


# # funcion cierre de sesion del usuario 
# def logout_view(request):
#     logout(request)
#     return redirect('Inscripciones.html')






