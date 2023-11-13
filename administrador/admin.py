from django.contrib import admin
from .models import Egreso, Ingreso

# Register your models here.
admin.site.register(Egreso)
admin.site.register(Ingreso)