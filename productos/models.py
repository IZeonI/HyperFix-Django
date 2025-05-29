from django.db import models

class Componentes(models.Model):
    tipo = models.CharField(max_length=40, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    imagen_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'componentes'

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    correo = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'

class ProveedorComponente(models.Model):
    pk = models.CompositePrimaryKey('id_proveedor', 'id_componente')
    id_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='id_proveedor')
    id_componente = models.ForeignKey('Componentes', models.DO_NOTHING, db_column='id_componente')

    class Meta:
        managed = False
        db_table = 'proveedor_componente'
