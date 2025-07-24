# Modelos Django para Sistema CRM Universitario
# Basados exactamente en la estructura de la base de datos

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
    email = models.CharField(max_length=100, verbose_name="Email")  # Como está en DB real
    password_hash = models.CharField(max_length=100, verbose_name="Hash de contraseña")  # Tamaño como DB real
    rol = models.CharField(max_length=100, verbose_name="Rol del usuario")  # Tamaño como DB real
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    # Estos campos no existen en DB real, los haremos opcionales
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True, blank=True)
    esta_activo = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        managed = True  # Django manejará esta tabla
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['nombre']

    def __str__(self):
        rol_display = dict(self.ROLES_CHOICES).get(self.rol, self.rol)
        return f"{self.nombre} ({rol_display})"

    @property
    def edad(self):
        """Calcula la edad del usuario"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))


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
        on_delete=models.CASCADE,  # Si se elimina el usuario, se elimina el admin
        related_name='perfil_admin',
        db_column='id_usuario'  # Nombre exacto en DB
    )
    puesto = models.CharField(max_length=100, verbose_name="Puesto administrativo")
    # nivel_acceso no existe en DB real

    class Meta:
        managed = True
        db_table = 'admin'
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return f"Admin: {self.usuario.nombre} - {self.puesto}"


class Docente(models.Model):
    """
    Perfil específico para docentes
    """
    id_docente = models.CharField(primary_key=True, max_length=100)
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_docente'
    )
    nombre_docente = models.CharField(max_length=100, verbose_name="Nombre del docente")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad")
    fecha_ingreso = models.DateField(null=True, blank=True, verbose_name="Fecha de ingreso")

    class Meta:
        managed = True
        db_table = 'docente'
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

    def __str__(self):
        return f"Prof. {self.nombre_docente} - {self.especialidad}"


class Estudiante(models.Model):
    """
    Perfil específico para estudiantes
    """
    id_estudiante = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_estudiante'
    )
    matricula = models.CharField(max_length=100, unique=True, verbose_name="Número de matrícula")
    carrera = models.CharField(max_length=100, verbose_name="Carrera")
    semestre_actual = models.IntegerField(default=1, verbose_name="Semestre actual")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de ingreso")

    class Meta:
        managed = True
        db_table = 'estudiante'
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.usuario.nombre} - {self.matricula}"


# ========================================
# MODELOS ACADÉMICOS
# ========================================

class MateriaClase(models.Model):
    """
    Materias/Asignaturas disponibles
    """
    id_materia_clases = models.IntegerField(primary_key=True)  # Coincidir con DB real
    nombre_materia = models.CharField(max_length=100, verbose_name="Nombre de la materia")
    codigo_materia = models.CharField(max_length=100, verbose_name="Código de materia")
    creditos = models.IntegerField(default=3, verbose_name="Créditos", null=True, blank=True)  # No existe en DB real
    descripcion = models.TextField(blank=True, verbose_name="Descripción", null=True)  # No existe en DB real

    class Meta:
        managed = True
        db_table = 'materia_clases'
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ['codigo_materia']

    def __str__(self):
        return f"{self.codigo_materia} - {self.nombre_materia}"


class Clase(models.Model):
    """
    Clases específicas (grupos) de las materias
    """
    id_clase = models.AutoField(primary_key=True)  # Renombrado para claridad
    materia = models.ForeignKey(
        MateriaClase,
        on_delete=models.CASCADE,  # Si se elimina la materia, se eliminan sus clases
        related_name='clases'
    )
    docente = models.ForeignKey(
        Docente,
        on_delete=models.SET_NULL,  # Si se elimina el docente, la clase queda sin asignar
        null=True,
        related_name='clases_asignadas'
    )
    horario = models.CharField(max_length=100, verbose_name="Horario")
    aula_clase = models.CharField(max_length=70, verbose_name="Aula")
    cupo_maximo = models.IntegerField(default=30, verbose_name="Cupo máximo")
    periodo_academico = models.CharField(max_length=20, verbose_name="Período académico")

    class Meta:
        managed = True
        db_table = 'clases'
        verbose_name = "Clase"
        verbose_name_plural = "Clases"

    def __str__(self):
        return f"{self.materia.codigo_materia} - {self.horario} - {self.aula_clase}"

    @property
    def estudiantes_inscritos(self):
        """Cuenta los estudiantes inscritos en esta clase"""
        return self.inscripciones.count()

    @property
    def tiene_cupo(self):
        """Verifica si hay cupo disponible"""
        return self.estudiantes_inscritos < self.cupo_maximo


# ========================================
# MODELOS TRANSACCIONALES
# ========================================

class Inscripcion(models.Model):
    """
    Inscripciones de estudiantes en clases
    """
    id_inscripcion = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(
        Usuario,  # Usando Usuario directamente para simplificar
        on_delete=models.CASCADE,
        related_name='inscripciones',
        limit_choices_to={'rol': 'estudiante'}  # Solo estudiantes
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activa', 'Activa'),
            ('retirada', 'Retirada'),
            ('completada', 'Completada')
        ],
        default='activa'
    )

    class Meta:
        managed = True
        db_table = 'inscripcion'
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ['estudiante', 'clase']  # Un estudiante no puede inscribirse dos veces a la misma clase

    def __str__(self):
        return f"{self.estudiante.nombre} en {self.clase}"


class Calificacion(models.Model):  # Singular, no plural
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

    id_calificacion = models.AutoField(primary_key=True)  # Singular
    estudiante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='calificaciones',
        limit_choices_to={'rol': 'estudiante'}
    )
    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='calificaciones'
    )
    nota = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Calificación")
    tipo_evaluacion = models.CharField(max_length=20, choices=TIPOS_EVALUACION)
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        managed = True
        db_table = 'calificacione'  # Mantenemos el nombre original de la tabla
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

    def __str__(self):
        return f"{self.estudiante.nombre} - {self.clase} - {self.nota}"

    @property
    def aprobado(self):
        """Verifica si la calificación es aprobatoria (>= 7.0)"""
        return self.nota >= Decimal('7.0')


class Pago(models.Model):  # Singular
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

    estudiante = models.OneToOneField(
        Estudiante,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='pago'
    )
    id_transaccion = models.CharField(max_length=255, unique=True, verbose_name="ID de transacción")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    moneda = models.CharField(max_length=20, default='DOP', verbose_name="Moneda")
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, blank=True, null=True)
    descripcion = models.TextField(blank=True, verbose_name="Descripción del pago")
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'pagos'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.id_transaccion} - {self.estudiante.usuario.nombre} - ${self.monto}"

    @property
    def esta_vencido(self):
        """Verifica si el pago está vencido"""
        if not self.fecha_vencimiento:
            return False
        from datetime import date
        return date.today() > self.fecha_vencimiento and self.estado_pago == 'pendiente'
