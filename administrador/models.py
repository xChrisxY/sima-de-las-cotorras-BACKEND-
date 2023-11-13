from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingreso(models.Model):
      
      OPCIONES_INGRESOS = [
            
            ('Restaurante', 'Restaurante'),
            ('Transporte', 'Transporte'),
            ('Hospedaje', 'Hospedaje de Cabañas'),
            ('Aventuras', 'Servicio de Aventuras')  
            
      ]

      tipo = models.CharField(max_length=100, choices=OPCIONES_INGRESOS)      
      descripcion = models.TextField(max_length=200)
      monto = models.DecimalField(max_digits=10, decimal_places=2)
      fecha = models.DateField(auto_now=True)   

      def __str__(self):
            return f"{self.tipo} = {self.descripcion}"

class Egreso(models.Model):
      
      OPCIONES_EGRESOS = [
            
            ('Transporte', 'Egreso por Transporte'),
            ('Alquiler', 'Alquiler'),
            ('Compras', 'Compras'),
            ('Trabajadores', 'Pago a Trabajadores'),  
            ('Mantenimiento', 'Mantenimiento por Aventuras')
            
      ]
      
      tipo = models.CharField(max_length=100, choices=OPCIONES_EGRESOS)
      descripcion = models.TextField(max_length=200)
      monto = models.DecimalField(max_digits=10, decimal_places=2)
      fecha = models.DateField(auto_now=True)
      
      def __str__(self):
            return f"{self.tipo} = {self.descripcion}"