from django.db import models


class Carrera(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    duracion_meses = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carreras"

    def __str__(self):
        return self.nombre


class Salon(models.Model):
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=150)
    estado = models.CharField(max_length=20, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "salones"

    def __str__(self):
        return self.nombre


class Unidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "unidades"

    def __str__(self):
        return self.nombre


class ModuloAcademico(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "modulos_academicos"

    def __str__(self):
        return self.nombre


class PlantillaAcademica(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT)
    modulo = models.ForeignKey(ModuloAcademico, on_delete=models.PROTECT)
    salon = models.ForeignKey(Salon, on_delete=models.PROTECT)
    turno = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plantillas_academicas"