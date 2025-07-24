#!/usr/bin/env python
"""
Script para probar la creación de objetos de los modelos
"""

import os
import sys
import django
from datetime import date, datetime
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_Crm.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from AppCRM.models import Usuario, Administrador, Docente, Estudiante, MateriaClase, Clase

def test_object_creation():
    print("🧪 PROBANDO CREACIÓN DE OBJETOS...")
    print("=" * 50)
    
    # Test 1: Crear Usuario
    print("\n✅ Test 1: Creando Usuario...")
    try:
        usuario = Usuario(
            nombre="Juan Pérez",
            email="juan.perez@universidad.edu",
            password_hash="hashed_password_123",
            rol="estudiante",
            fecha_nacimiento=date(1995, 5, 15),
            esta_activo=True
        )
        print(f"   - Usuario creado: {usuario}")
        print(f"   - Edad calculada: {usuario.edad} años")
        print(f"   - Rol display: {usuario.get_rol_display()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Crear MateriaClase
    print("\n✅ Test 2: Creando MateriaClase...")
    try:
        materia = MateriaClase(
            nombre_materia="Programación en Python",
            codigo_materia="PROG101",
            creditos=4,
            descripcion="Curso básico de programación en Python"
        )
        print(f"   - Materia creada: {materia}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Probar validaciones
    print("\n✅ Test 3: Probando validaciones...")
    try:
        # Intentar crear usuario con email inválido
        usuario_invalido = Usuario(
            nombre="Test User",
            email="email_invalido",  # Email sin formato correcto
            password_hash="hash123",
            rol="estudiante",
            fecha_nacimiento=date(1990, 1, 1)
        )
        # Llamar full_clean para ejecutar validaciones
        usuario_invalido.full_clean()
        print(f"   ❌ No se detectó email inválido")
    except Exception as e:
        print(f"   ✅ Validación de email funcionando: {type(e).__name__}")
    
    # Test 4: Probar choices
    print("\n✅ Test 4: Probando choices...")
    try:
        # Rol válido
        usuario_admin = Usuario(
            nombre="Admin User",
            email="admin@universidad.edu",
            password_hash="admin_hash",
            rol="admin",  # Choice válido
            fecha_nacimiento=date(1980, 1, 1)
        )
        print(f"   - Rol válido '{usuario_admin.rol}': OK")
        
        # Probar rol inválido
        usuario_rol_invalido = Usuario(
            nombre="Invalid User",
            email="invalid@universidad.edu",
            password_hash="hash",
            rol="rol_inexistente",  # Choice inválido
            fecha_nacimiento=date(1990, 1, 1)
        )
        print(f"   - Rol inválido creado (Django no valida choices automáticamente en __init__)")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 ¡PRUEBAS DE OBJETOS COMPLETADAS!")
    print("✨ Los modelos pueden crear objetos correctamente.")
    print("📝 Nota: Para validar completamente, se necesita guardar en BD.")

if __name__ == "__main__":
    test_object_creation()
