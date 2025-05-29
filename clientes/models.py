from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=40, blank=True, null=True)
    correo = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'

class Equipo(models.Model):
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    tipo_equipo = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipo'
