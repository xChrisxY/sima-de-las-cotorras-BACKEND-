from django.urls import path
from .views import ReservacionesAventuras

urlpatterns = [
    
      path('reservaciones/', ReservacionesAventuras.as_view(), name="get_reservations")
      
    
]
