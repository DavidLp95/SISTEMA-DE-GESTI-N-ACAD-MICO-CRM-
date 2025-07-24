from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Usuario, Administrador, Docente, Estudiante,
    MateriaClase, Clase, Inscripcion, Calificacion, Pago
)


# ========================================
# CONFIGURACIÓN PARA USUARIO
# ========================================

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'id_usuario', 'nombre', 'email', 'rol', 
        'edad_display', 'fecha_nacimiento'
    ]
    list_filter = ['rol']
    search_fields = ['nombre', 'email']
    ordering = ['nombre']
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email', 'fecha_nacimiento')
        }),
        ('Credenciales', {
            'fields': ('password_hash', 'rol'),
            'classes': ('collapse',)
        })
    )
    
    def edad_display(self, obj):
        """Muestra la edad calculada"""
        return f"{obj.edad} años"
    edad_display.short_description = 'Edad'


# ========================================
# CONFIGURACIÓN PARA ADMINISTRADOR
# ========================================

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ['id_adimin', 'id_usuario', 'puesto']
    list_filter = ['puesto']
    search_fields = ['id_usuario__nombre', 'puesto']
    raw_id_fields = ['id_usuario']
    
    fieldsets = (
        ('Información del Administrador', {
            'fields': ('id_usuario', 'puesto')
        }),
    )


# ========================================
# CONFIGURACIÓN PARA DOCENTE
# ========================================

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = [
        'id_docente', 'nombre_docente', 'departamento', 
        'especialidad', 'id_usuario', 'clases_count_display'
    ]
    list_filter = ['departamento', 'especialidad']
    search_fields = ['nombre_docente', 'departamento', 'especialidad', 'id_usuario__nombre']
    raw_id_fields = ['id_usuario']
    
    fieldsets = (
        ('Información del Docente', {
            'fields': ('id_usuario', 'nombre_docente')
        }),
        ('Información Académica', {
            'fields': ('departamento', 'especialidad')
        })
    )
    
    def clases_count_display(self, obj):
        """Cuenta las clases asignadas al docente"""
        return obj.clases_count()
    clases_count_display.short_description = 'Clases Asignadas'


# ========================================
# CONFIGURACIÓN PARA ESTUDIANTE
# ========================================

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = [
        'id_estudiante', 'id_usuario', 'matricula', 'carrera'
    ]
    list_filter = ['carrera']
    search_fields = ['id_usuario__nombre', 'matricula', 'carrera']
    raw_id_fields = ['id_usuario']
    
    fieldsets = (
        ('Información del Estudiante', {
            'fields': ('id_usuario', 'matricula')
        }),
        ('Información Académica', {
            'fields': ('carrera',)
        })
    )


# ========================================
# CONFIGURACIÓN PARA MATERIA
# ========================================

@admin.register(MateriaClase)
class MateriaClaseAdmin(admin.ModelAdmin):
    list_display = [
        'id_materia_clases', 'codigo_materia', 'nombre_materia', 'clases_count_display'
    ]
    search_fields = ['nombre_materia', 'codigo_materia']
    ordering = ['codigo_materia']
    
    fieldsets = (
        ('Información de la Materia', {
            'fields': ('codigo_materia', 'nombre_materia')
        }),
    )
    
    def clases_count_display(self, obj):
        """Cuenta las clases de esta materia"""
        return obj.clases_count()
    clases_count_display.short_description = 'Clases Disponibles'


# ========================================
# CONFIGURACIÓN PARA CLASE
# ========================================

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = [
        'id_clases', 'materia_display', 'docente_display', 'horario', 
        'aula_clase', 'estudiantes_inscritos_display'
    ]
    search_fields = ['horario', 'aula_clase']
    list_filter = ['materia', 'docente']
    
    fieldsets = (
        ('Información de la Clase', {
            'fields': ('materia', 'docente')
        }),
        ('Horario y Ubicación', {
            'fields': ('horario', 'aula_clase')
        })
    )
    
    def materia_display(self, obj):
        """Muestra la materia relacionada"""
        materia_obj = obj.get_materia_objeto()
        return materia_obj.codigo_materia if materia_obj else f"ID: {obj.materia}"
    materia_display.short_description = 'Materia'
    
    def docente_display(self, obj):
        """Muestra el docente relacionado"""
        docente_obj = obj.get_docente_objeto()
        return docente_obj.nombre_docente if docente_obj else f"ID: {obj.docente}"
    docente_display.short_description = 'Docente'
    
    def estudiantes_inscritos_display(self, obj):
        """Muestra estudiantes inscritos"""
        count = obj.estudiantes_inscritos_count()
        return format_html(
            '<span style="color: green;">{}</span>',
            count
        )
    estudiantes_inscritos_display.short_description = 'Estudiantes Inscritos'


# ========================================
# CONFIGURACIÓN PARA INSCRIPCIÓN
# ========================================

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = [
        'id_inscripcion', 'id_estudiante', 'clase_display', 'fecha_inscripcion'
    ]
    list_filter = ['fecha_inscripcion']
    search_fields = ['id_estudiante__nombre']
    raw_id_fields = ['id_estudiante']
    date_hierarchy = 'fecha_inscripcion'
    
    fieldsets = (
        ('Información de Inscripción', {
            'fields': ('id_estudiante', 'clase')
        }),
    )
    
    def clase_display(self, obj):
        """Muestra la clase relacionada"""
        clase_obj = obj.get_clase_objeto()
        if clase_obj:
            materia_obj = clase_obj.get_materia_objeto()
            return f"{materia_obj.codigo_materia if materia_obj else 'Materia'} - {clase_obj.horario}"
        return f"Clase ID: {obj.clase}"
    clase_display.short_description = 'Clase'


# ========================================
# CONFIGURACIÓN PARA CALIFICACIÓN
# ========================================

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = [
        'id_calificaciones', 'id_estudiante', 'clase_display', 
        'nota_display', 'tipo_evaluacion'
    ]
    list_filter = ['tipo_evaluacion']
    search_fields = ['id_estudiante__nombre']
    raw_id_fields = ['id_estudiante']
    
    fieldsets = (
        ('Información de Calificación', {
            'fields': ('id_estudiante', 'clase')
        }),
        ('Evaluación', {
            'fields': ('tipo_evaluacion', 'notas')
        })
    )
    
    def clase_display(self, obj):
        """Muestra la clase relacionada"""
        clase_obj = obj.get_clase_objeto()
        if clase_obj:
            materia_obj = clase_obj.get_materia_objeto()
            return f"{materia_obj.codigo_materia if materia_obj else 'Materia'} - {clase_obj.horario}"
        return f"Clase ID: {obj.clase}"
    clase_display.short_description = 'Clase'
    
    def nota_display(self, obj):
        """Muestra la nota con color según aprobación"""
        color = 'green' if obj.aprobado else 'red'
        status = '✓ Aprobado' if obj.aprobado else '✗ Reprobado'
        return format_html(
            '<span style="color: {};">{} ({})</span>',
            color, obj.notas, status
        )
    nota_display.short_description = 'Calificación'


# ========================================
# CONFIGURACIÓN PARA PAGO
# ========================================

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = [
        'id_pagos', 'id_transacion', 'monto_display', 
        'estado_pago_display', 'metodo_pago', 'fecha_pago'
    ]
    list_filter = [
        'estado_pago', 'metodo_pago', 'moneda', 'fecha_pago'
    ]
    search_fields = ['id_transacion', 'id_pagos__id_usuario__nombre']
    date_hierarchy = 'fecha_pago'
    
    fieldsets = (
        ('Información del Pago', {
            'fields': ('id_pagos', 'id_transacion')
        }),
        ('Detalles del Pago', {
            'fields': ('monto', 'moneda', 'metodo_pago', 'descripcion')
        }),
        ('Estado', {
            'fields': ('estado_pago',)
        })
    )
    
    def monto_display(self, obj):
        """Muestra el monto formateado"""
        return f"{obj.moneda} ${obj.monto:,.2f}"
    monto_display.short_description = 'Monto'
    
    def estado_pago_display(self, obj):
        """Muestra el estado con color"""
        colors = {
            'completado': 'green',
            'pendiente': 'orange',
            'fallido': 'red',
            'reembolsado': 'blue'
        }
        color = colors.get(obj.estado_pago, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color, obj.estado_pago.title()
        )
    estado_pago_display.short_description = 'Estado'


# ========================================
# PERSONALIZACIÓN DEL ADMIN PRINCIPAL
# ========================================

# Personalizar el título del admin
admin.site.site_header = "CRM Universitario - Administración"
admin.site.site_title = "CRM Universitario"
admin.site.index_title = "Panel de Administración del Sistema CRM"
