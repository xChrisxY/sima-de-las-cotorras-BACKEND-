from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import UserView, CommentaryUserView


urlpatterns = [

      path('usuarios/', UserView.as_view(), name="get_users"),
      path('usuarios/<int:id>', UserView.as_view(), name="modificar_usuario"),
      path('usuarios-opinions/', CommentaryUserView.as_view(), name="commentary_sections"),
      

] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)