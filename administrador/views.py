from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User

# Create your views here.
class AdminView(View):

      @method_decorator(csrf_exempt)
      def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
      def get(self, request):
          
          administrador = list(User.objects.filter(id = 1).values())

          if len(administrador) > 0:
              
              admin = administrador[0]
              datos = {'message' : 'Succes', 'administrador' : admin}

          else:
              datos = {'message' : 'Admin not found'}

          return JsonResponse(datos)
      
      # Login y autenticación
      def post(self, request):
          
          jsondata = json.loads(request.body)

          if len(jsondata) == 1:
             
            jsondata = json.loads(request.body)
            newPassword = jsondata['new_password']

            if newPassword:

              user = User.objects.get(id = 1)

              user.set_password(newPassword)          
              user.save()

              datos = {'message': 'Se pudo cambiar la contraseña'}
              return JsonResponse(datos)

            else:

              datos = {'message': 'No se pudo cambiar la contraseña'}
              return JsonResponse(datos)
          
          else:
             
            user = authenticate(username = jsondata['username'], password = jsondata['password'])

            if user is None:
                
              datos = {'message': 'Username or password incorrect'}

            else:

              datos = {'message': 'Success'}

            return JsonResponse(datos)
      
      def put(self, request, id):
          
          print(request.body)

          administrador = list(User.objects.filter(id = id).values())

          if len(administrador) > 0:
              
            jsondata = json.loads(request.body)
            admin = User.objects.get(id = id)
            admin.first_name = jsondata['first_name']
            admin.last_name = jsondata['last_name']
            admin.email = jsondata['email']
            admin.username = jsondata['username']
            admin.password = jsondata['password']
            admin.save()

            datos = {'message' : 'Success'}
      
          else:
              
            datos = {'message' : 'Admin not found'}

          return JsonResponse(datos)
              





