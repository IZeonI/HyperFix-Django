from django.db import models
from ventas.models import TicketServicio

class Servicio(models.Model):
    servicio = models.CharField(max_length=25, blank=True, null=True)
    costo = models.IntegerField(blank=True, null=True)
    rfc_empleado = models.ForeignKey('empleados.Empleados', models.DO_NOTHING, db_column='rfc_empleado', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicio'

