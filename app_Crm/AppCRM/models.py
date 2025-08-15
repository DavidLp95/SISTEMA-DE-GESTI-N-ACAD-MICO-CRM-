# Modelos Django para Sistema CRM Universitario
# Basados exactamente en la estructura de la base de datos usando inspectdb

from django.db import models
from decimal import Decimal


# ========================================
# MODELO BASE DE USUARIO
# ========================================

class Usuario(models.Model):
    """
    Modelo base para todos los usuarios del sistema CRM
    """
    ROLES_CHOICES = [
        ('admin', 'Administrador'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.CharField(max_length=100, verbose_name="Email")
    password_hash = models.CharField(max_length=100, verbose_name="Hash de contraseña")
    rol = models.CharField(max_length=100, verbose_name="Rol del usuario")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="ultimo login ")
    is_staff = models.BooleanField(default=False, verbose_name="Es personal administrativo")
    is_superuser = models.BooleanField(default=False, verbose_name="Es superusuario")

    class Meta:
        managed = True
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    @property
    def edad(self):
        """Calcula la edad del usuario"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    
    @property
    def is_authenticated(self):
        """Siempre True para usuarios válidos"""
        return True
    
    @property
    def is_anonymous(self):
        """Siempre False para usuarios válidos"""
        return False
    
    @property
    def is_active(self):
        """True si el usuario está activo"""
        return True
    
    def get_username(self):
        """Devuelve el email como username"""
        return self.email
    
    # funciones necesarioas para que el usuario/administrador  pueda iniciar sesión 
    def has_perm(self, perm, obj=None):
        """¿Tiene el usuario un permiso específico?"""
        return self.is_superuser
    
    def has_perms(self, perm_list, obj=None):
        """¿Tiene el usuario todos los permisos especificados?"""
        return all(self.has_perm(perm, obj) for perm in perm_list)
    
    def has_module_perms(self, app_label):
        """¿Tiene el usuario permisos para ver la app?"""
        return self.is_superuser or self.is_staff
# ========================================
# MODELOS DE ROLES ESPECÍFICOS
# ========================================

class Administrador(models.Model):
    """
    Perfil específico para administradores
    """
    id_adimin = models.AutoField(primary_key=True)  # Como está en DB real (con typo)
    id_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.DO_NOTHING,
        db_column='id_usuario',
        related_name='administrador_perfil'
    )
    puesto = models.CharField(max_length=100, verbose_name="Puesto administrativo")

    class Meta:
        managed = True
        db_table = 'admin'
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return f"Admin: {self.id_usuario.nombre} - {self.puesto}"


class Docente(models.Model):
    """
    Perfil específico para docentes
    """
    id_docente = models.CharField(primary_key=True, max_length=100)
    nombre_docente = models.CharField(max_length=100, verbose_name="Nombre del docente")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='id_usuario',
        related_name='docente_perfil'
    )

    class Meta:
        managed = True
        db_table = 'docente'
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return f"Prof. {self.nombre_docente} - {self.especialidad}"

    def clases_count(self):
        """Cuenta las clases asignadas al docente"""
        return Clase.objects.filter(docente=self.id_docente).count()


class Estudiante(models.Model):
    """
    Perfil específico para estudiantes
    """
    id_estudiante = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='id_usuario',
        related_name='estudiante_perfil'
    )
    matricula = models.CharField(max_length=100, verbose_name="Número de matrícula")
    carrera = models.CharField(max_length=100, verbose_name="Carrera")

    class Meta:
        managed = True
        db_table = 'estudiante'
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.id_usuario.nombre} - {self.matricula}"


# ========================================
# MODELOS ACADÉMICOS
# ========================================

class MateriaClase(models.Model):
    """
    Materias/Asignaturas disponibles
    """
    id_materia_clases = models.IntegerField(primary_key=True)
    nombre_materia = models.CharField(max_length=100, verbose_name="Nombre de la materia")
    codigo_materia = models.CharField(max_length=100, verbose_name="Código de materia")

    class Meta:
        managed = True
        db_table = 'materia_clases'
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['codigo_materia']

    def __str__(self):
        return f"{self.codigo_materia} - {self.nombre_materia}"

    def clases_count(self):
        """Cuenta las clases de esta materia"""
        return Clase.objects.filter(materia=self.id_materia_clases).count()


class Clase(models.Model):
    """
    Clases específicas (grupos) de las materias
    """
    id_clases = models.IntegerField(primary_key=True)  # Como está en DB real
    materia = models.IntegerField(verbose_name="ID Materia")  # Campo integer como en DB
    docente = models.IntegerField(verbose_name="ID Docente", null=True, blank=True)  # Campo integer como en DB
    horario = models.CharField(max_length=100, verbose_name="Horario")
    aula_clase = models.CharField(max_length=70, verbose_name="Aula")

    class Meta:
        managed = True
        db_table = 'clases'
        verbose_name = "Clase"
        verbose_name_plural = "Clases"

    def __str__(self):
        materia_obj = MateriaClase.objects.filter(id_materia_clases=self.materia).first()
        materia_nombre = materia_obj.codigo_materia if materia_obj else f"Materia {self.materia}"
        return f"{materia_nombre} - {self.horario} - {self.aula_clase}"

    def get_materia_objeto(self):
        """Obtiene el objeto materia relacionado"""
        return MateriaClase.objects.filter(id_materia_clases=self.materia).first()

    def get_docente_objeto(self):
        """Obtiene el objeto docente relacionado"""
        if self.docente:
            return Docente.objects.filter(id_docente=self.docente).first()
        return None

    def estudiantes_inscritos_count(self):
        """Cuenta los estudiantes inscritos en esta clase"""
        return Inscripcion.objects.filter(clase=self.id_clases).count()


# ========================================
# MODELOS TRANSACCIONALES
# ========================================

class Inscripcion(models.Model):
    """
    Inscripciones de estudiantes en clases
    """
    id_inscripcion = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='id_estudiante',
        related_name='inscripciones'
    )
    clase = models.IntegerField(verbose_name="ID Clase")  # Campo integer como en DB
    fecha_inscripcion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'inscripcion'
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"{self.id_estudiante.nombre} en Clase {self.clase}"

    def get_clase_objeto(self):
        """Obtiene el objeto clase relacionado"""
        return Clase.objects.filter(id_clases=self.clase).first()


class Calificacion(models.Model):
    """
    Calificaciones de los estudiantes
    """
    TIPOS_EVALUACION = [
        ('parcial', 'Examen Parcial'),
        ('final', 'Examen Final'),
        ('tarea', 'Tarea'),
        ('proyecto', 'Proyecto'),
        ('quiz', 'Quiz'),
    ]

    id_calificaciones = models.IntegerField(primary_key=True)  # Como está en DB real
    id_estudiante = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='id_estudiante',
        related_name='calificaciones'
    )
    clase = models.IntegerField(verbose_name="ID Clase")  # Campo integer como en DB
    notas = models.DecimalField(max_digits=65535, decimal_places=65535, verbose_name="Calificación")  # Como en DB
    tipo_evaluacion = models.CharField(max_length=50, verbose_name="Tipo de evaluación")

    class Meta:
        managed = True
        db_table = 'calificacione'
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        return f"{self.id_estudiante.nombre} - Clase {self.clase} - {self.notas}"

    @property
    def aprobado(self):
        """Verifica si la calificación es aprobatoria (>= 7.0)"""
        return self.notas >= Decimal('7.0')

    def get_clase_objeto(self):
        """Obtiene el objeto clase relacionado"""
        return Clase.objects.filter(id_clases=self.clase).first()


class Pago(models.Model):
    """
    Pagos realizados por los estudiantes
    """
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    METODOS_PAGO = [
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Efectivo'),
        ('cheque', 'Cheque'),
    ]

    id_pagos = models.OneToOneField(
        Estudiante,
        on_delete=models.DO_NOTHING,
        db_column='id_pagos',
        primary_key=True,
        related_name='pago'
    )
    id_usuario = models.IntegerField()  # Como está en DB real
    id_transacion = models.CharField(max_length=255, verbose_name="ID de transacción")  # Con typo como DB
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    moneda = models.CharField(max_length=20, verbose_name="Moneda")
    estado_pago = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del pago")
    fecha_pago = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pagos'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.id_transacion} - {self.id_pagos.id_usuario.nombre} - ${self.monto}"

    def get_usuario_objeto(self):
        """Obtiene el objeto usuario relacionado"""
        return Usuario.objects.filter(id_usuario=self.id_usuario).first()
