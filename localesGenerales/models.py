
from django.db import models
from django.utils import timezone

class Inventario(models.Model):
    ubicacion = models.CharField(max_length=100)
    cod_ean = models.CharField(max_length=50)
    cod_dun = models.CharField(max_length=50)
    cod_sistema = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    conteo_01 = models.IntegerField()
    conteo_02 = models.IntegerField()
    diferencia = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        self.diferencia = self.conteo_02 - self.conteo_01
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cod_sistema} - {self.descripcion}"
    
    
    creado = models.DateTimeField(default=timezone.now)
