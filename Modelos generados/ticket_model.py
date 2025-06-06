# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ticket(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    rfc_empleado = models.ForeignKey('Empleados', models.DO_NOTHING, db_column='rfc_empleado', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket'
