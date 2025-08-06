from django.contrib.auth import get_user_model

User = get_user_model()

# Mostrar TODOS los usuarios
print("Todos los usuarios:")
for user in User.objects.all():
    print(f" - Username: {user.username}, Es superusuario: {user.is_superuser}")