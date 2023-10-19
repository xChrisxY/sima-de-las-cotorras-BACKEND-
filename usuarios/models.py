from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Usuarios(models.Model):

      name = models.CharField(max_length=100)
      last_name = models.CharField(max_length=200)
      phone = models.CharField(max_length=10)
      email = models.EmailField(max_length=50)
      username = models.CharField(max_length=15)      
      password = models.CharField(max_length=10)
      photo = CloudinaryField("Images", folder="proyecto", blank=True)

      def __str__(self):
            return f"{self.name}"

class Comments(models.Model):
      comment = models.TextField(max_length=500)
      date = models.DateField(auto_now=True)
      usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="comment")

      def __str__(self):
            return f"Comment: {self.comment} -- by : {self.usuario}"









