# usuarios/auth_backend.py
from django.contrib.auth.hashers import check_password
from .models import Usuario  # Tu modelo personalizado

class UsuarioBackend:
    """
    Permite hacer login usando el modelo Usuario personalizado
    """
    def authenticate(self, request, username=None, password=None):
        """
        username: aquí usamos el email del usuario
        password: la contraseña en texto plano (la compararemos hasheada)
        """
        try:
            # Buscamos al usuario por email (asumimos que el "username" es el email)
            usuario = Usuario.objects.get(email=username)

            # Verificamos que sea estudiante
            if usuario.rol != 'estudiante':
                return None  # No puede iniciar sesión si no es estudiante

            # Verificamos la contraseña (compara texto plano vs hash)
            if check_password(password, usuario.password_hash):
                return usuario  # Éxito: devuelve el usuario
        except Usuario.DoesNotExist:
            return None  # No existe
        return None

    def get_user(self, user_id):
        """
        Django lo usa para recuperar al usuario en cada petición (por id)
        """
        try:
            return Usuario.objects.get(id_usuario=user_id)
        except Usuario.DoesNotExist:
            return None