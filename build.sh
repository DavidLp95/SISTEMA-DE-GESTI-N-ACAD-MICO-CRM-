#!/usr/bin/env bash
# exit on error
set -o errexit

# Cambiar al directorio de la aplicación
cd app_Crm

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate
