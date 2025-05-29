from django.db import models

class Ticket(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    id_cliente = models.ForeignKey('clientes.Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    rfc_empleado = models.ForeignKey('empleados.Empleados', models.DO_NOTHING, db_column='rfc_empleado', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket'

class TicketComponente(models.Model):
    pk = models.CompositePrimaryKey('id_ticket', 'id_componente')
    id_ticket = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='id_ticket')
    id_componente = models.ForeignKey('productos.Componentes', models.DO_NOTHING, db_column='id_componente')
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_componente'

class TicketServicio(models.Model):
    pk = models.CompositePrimaryKey('id_ticket', 'id_servicio')
    id_ticket = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='id_ticket')
    id_servicio = models.ForeignKey('servicios.Servicio', models.DO_NOTHING, db_column='id_servicio')

    class Meta:
        managed = False
        db_table = 'ticket_servicio'
