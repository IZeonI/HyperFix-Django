# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Empleados(models.Model):
    rfc_empleado = models.CharField(primary_key=True, max_length=13)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=40, blank=True, null=True)
    puesto = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleados'
