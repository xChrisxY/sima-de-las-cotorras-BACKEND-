from django.urls import path
from .views import AdminView

urlpatterns = [

      path('administrador/', AdminView.as_view(), name="vista_administrador"),
      path('administrador/<int:id>', AdminView.as_view(), name="update_administrador"),
      path('login-admin/', AdminView.as_view(), name="login_admin")

]