from django.urls import path
from .views import ReservacionesAventuras, CreatecCheckoutSessionView, AventurasView

urlpatterns = [
    
      path('reservaciones/', ReservacionesAventuras.as_view(), name="get_reservations"),
      path('create-checkout-session/', CreatecCheckoutSessionView.as_view(), name="create-checkout-session"),
      path('aventuras/', AventurasView.as_view(), name="Aventuras")
      
    
]
