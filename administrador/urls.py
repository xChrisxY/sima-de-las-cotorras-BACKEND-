from django.urls import path
from .views import AdminView, GestionarIngresos, GestionEgreso, verificarSesion

urlpatterns = [

      path('administrador/', AdminView.as_view(), name="vista_administrador"),
      path('administrador/<int:id>', AdminView.as_view(), name="update_administrador"),
      path('login-admin/', AdminView.as_view(), name="login_admin"),
      path('administrador/agregar-ingreso/', GestionarIngresos.as_view(), name="publicar_ingresos"),
      path('administrador/verificar-sesion/', verificarSesion, name="verificar_sesión"), # Para probar la función
      path('administrador/ingresos/', GestionarIngresos.as_view(), name="ver_ingresos"),
      path('administrador/egresos/', GestionEgreso.as_view(), name="operar_egreso"),

]