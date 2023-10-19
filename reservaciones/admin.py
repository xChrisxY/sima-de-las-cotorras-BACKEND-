from django.contrib import admin
from .models import Aventura, Cabaña, Pago, ReservaAventura, ReservaCabaña

# Register your models here.
admin.site.register(Aventura)
admin.site.register(Cabaña)
admin.site.register(Pago)
admin.site.register(ReservaCabaña)
admin.site.register(ReservaAventura)
