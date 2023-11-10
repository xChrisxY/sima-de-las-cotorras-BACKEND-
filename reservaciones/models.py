from django.db import models
from usuarios.models import Usuarios

# Create your models here.
class Cabaña(models.Model):

      nombre = models.CharField(max_length=200)
      descripcion = models.TextField(max_length=300)
      precio = models.DecimalField(max_digits=6, decimal_places=2)
      price_id = models.CharField(max_length=200)

      def __str__(self):
            return f"{self.descripcion} -- ${self.precio}"

class Aventura(models.Model):

      nombre = models.CharField(max_length=100)
      descripcion = models.TextField(max_length=300)
      precio = models.DecimalField(max_digits=6, decimal_places=2)
      price_id = models.CharField(max_length=200)

      def __str__(self):
            return f"{self.nombre} -- ${self.precio}" 

class Pago(models.Model):

      monto = models.DecimalField(max_digits=6, decimal_places=2)
      fecha = models.DateField(auto_now=True)
      numero_transaccion = models.CharField(max_length=100)

      def __str__(self):
            return f"{self.monto} -- {self.fecha}"

class ReservaCabaña(models.Model):

      fecha_de_reservacion = models.DateField(blank=False, null=False)
      fecha_de_salida = models.DateField(blank=False, null=False)
      usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="reserva_de_cabaña")
      cabaña = models.ForeignKey(Cabaña, on_delete=models.CASCADE, related_name="reserva_de_cabaña")
      pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="pago_de_cabaña")


class ReservaAventura(models.Model):

      fecha = models.DateField(blank=False, null=False)
      aventura = models.ForeignKey(Aventura, on_delete=models.CASCADE, related_name="reserva_de_aventura")
      usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="reservacion_de_usuario")
      pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name="pago_de_aventura")

      def __str__(self):
            return f"Reserva de {self.usuario} por {self.aventura} en la fecha [{self.fecha}]"



      