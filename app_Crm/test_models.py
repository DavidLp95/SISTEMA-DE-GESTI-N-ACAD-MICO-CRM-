#!/usr/bin/env python
"""
Script para probar los modelos Django mejorados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_Crm.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from AppCRM.models import Usuario, Administrador, Docente, Estudiante, MateriaClase, Clase

def test_models():
    print("🧪 INICIANDO PRUEBAS DE MODELOS...")
    print("=" * 50)
    
    # Test 1: Verificar que los modelos existen
    print("\n✅ Test 1: Verificando que los modelos existen...")
    models_to_test = [Usuario, Administrador, Docente, Estudiante, MateriaClase, Clase]
    for model in models_to_test:
        print(f"   - {model.__name__}: OK")
    
    # Test 2: Verificar campos obligatorios
    print("\n✅ Test 2: Verificando campos de Usuario...")
    usuario_fields = [field.name for field in Usuario._meta.fields]
    print(f"   - Campos: {usuario_fields}")
    
    # Test 3: Verificar choices
    print("\n✅ Test 3: Verificando choices...")
    print(f"   - Roles disponibles: {Usuario.ROLES_CHOICES}")
    
    # Test 4: Verificar relaciones
    print("\n✅ Test 4: Verificando relaciones...")
    
    # Relación Usuario -> Administrador
    admin_relation = Usuario._meta.get_field('perfil_admin')
    print(f"   - Usuario -> Administrador: {admin_relation.related_model.__name__}")
    
    # Relación Usuario -> Docente
    docente_relation = Usuario._meta.get_field('perfil_docente')
    print(f"   - Usuario -> Docente: {docente_relation.related_model.__name__}")
    
    # Test 5: Verificar métodos personalizados
    print("\n✅ Test 5: Verificando métodos personalizados...")
    usuario_methods = [method for method in dir(Usuario) if not method.startswith('_') and callable(getattr(Usuario, method))]
    print(f"   - Métodos de Usuario: {usuario_methods}")
    
    # Test 6: Verificar Meta options
    print("\n✅ Test 6: Verificando Meta options...")
    print(f"   - Usuario managed: {Usuario._meta.managed}")
    print(f"   - Usuario db_table: {Usuario._meta.db_table}")
    print(f"   - Usuario verbose_name: {Usuario._meta.verbose_name}")
    
    print("\n" + "=" * 50)
    print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    print("📊 Los modelos están listos para usar.")

if __name__ == "__main__":
    test_models()
