from django.db import models

class Empleados(models.Model):
    rfc_empleado = models.CharField(primary_key=True, max_length=13)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=40, blank=True, null=True)
    puesto = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleados'
