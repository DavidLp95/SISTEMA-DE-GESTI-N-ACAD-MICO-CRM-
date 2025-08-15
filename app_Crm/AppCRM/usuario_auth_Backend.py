# usuarios/auth_backend.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario  # Tu modelo personalizado

class UsuarioBackend(BaseBackend):
    # 'Permite hacer login usando el modelo Usuario personalizado'

    def authenticate(self, request, username=None, password=None):
        
        # username: aquí usamos el email del usuario
        # password: la contraseña en texto plano (la compararemos hasheada)
        # 
        try:
            # Buscamos al usuario por email (asumimos que el "username" es el email)
            usuario = Usuario.objects.get(email=username)

            # Permitir login a estudiantes para el frontend y administradores para el admin
            if usuario.rol not in ['estudiante', 'admin']:
                print(f"Usuario con rol '{usuario.rol}' no autorizado")
                return None  # Solo estudiantes y administradores pueden iniciar sesión
            
            if usuario.password_hash == password:
                
                return usuario
            elif check_password(password, usuario.password_hash):
                
                return usuario
            
            # # Verificamos la contraseña (compara texto plano vs hash)
            # if check_password(password, usuario.password_hash):
            #     return usuario  # Éxito: devuelve el usuario
        except Usuario.DoesNotExist:
            
            return None  # No existe
        return None

    def get_user(self, user_id):
        # Django lo usa para recuperar al usuario en cada petición (por id)
        
        try:
            return Usuario.objects.get(id_usuario=user_id)
        except Usuario.DoesNotExist:
            return None