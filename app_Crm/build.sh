#!/usr/bin/env bash
# exit on error
set -o errexit

# Hacer este archivo ejecutable
chmod +x build.sh

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate
