from django.urls import path
from .views import ReservacionesAventuras, CreatecCheckoutSessionView, AventurasView, CabañasView, ReservacionesCabañas

urlpatterns = [
    
      path('reservaciones-aventura/', ReservacionesAventuras.as_view(), name="get_reservations"),
      path('create-checkout-session/', CreatecCheckoutSessionView.as_view(), name="create-checkout-session"),
      path('aventuras/', AventurasView.as_view(), name="Aventuras"),
      path('cabañas/', CabañasView.as_view(), name="get_cabañas"),
      path('reservaciones-aventura/<int:id>/', ReservacionesAventuras.as_view(), name="view_activity_user"),
      path('reservaciones-cabaña/', ReservacionesCabañas.as_view(), name="get_reservations_cabain"),
      path('reservaciones-cabaña/<int:id>', ReservacionesCabañas.as_view(), name="get_reservations_cabain_by_user"),
    
]
