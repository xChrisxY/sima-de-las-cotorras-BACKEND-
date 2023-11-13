from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from .models import Egreso, Ingreso
from decouple import config
import jwt
from datetime import datetime, timedelta

# Create your views here.
class AdminView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # === Obtener los datos del administrador === #
    def get(self, request):

        administrador = list(User.objects.filter(id=1).values())

        if len(administrador) > 0:

            admin = administrador[0]
            datos = {'message': 'Succes', 'administrador': admin}

        else:

            datos = {'message': 'Admin not found'}

        return JsonResponse(datos)

    # ==== Login y autenticación ==== #
    def post(self, request):

        jsondata = json.loads(request.body)

        if len(jsondata) == 1:

            jsondata = json.loads(request.body)
            newPassword = jsondata['new_password']

            if newPassword:

                user = User.objects.get(id=1)

                user.set_password(newPassword)
                user.save()

                datos = {'message': 'Se pudo cambiar la contraseña'}
                return JsonResponse(datos)

            else:

                datos = {'message': 'No se pudo cambiar la contraseña'}
                return JsonResponse(datos)

        # === Método de autenticación === #
        else:

            try:
              
                usuario = jsondata['username']
                contraseña = jsondata['password']

                user = authenticate(username = usuario, password = contraseña)

                if user is None:

                    datos = {'message': 'Username or password incorrect'}
                    return JsonResponse(datos, status = 201)

                else:

                    # === Procedemos a crear el JWT === #
                    
                    payload = {

                      'username': user.username,
                      'id': user.id,
                      'exp': datetime.utcnow() + timedelta(days=1)
                            
                    }

                    secret_key = config('JWT_SECRET_KEY')

                    token = jwt.encode(payload, secret_key, algorithm="HS256")

                    datos = {'message': "El usuario se ha autenticado correctamente", "token": token}

                    return JsonResponse(datos, status=200)                         

            except:

                return JsonResponse({'message': "Faltan datos de autenticación"}, status = 400)

    # === Actualizar los datos del usuario === #
    def put(self, request, id):

        print(request.body)

        administrador = list(User.objects.filter(id=id).values())

        if len(administrador) > 0:

            jsondata = json.loads(request.body)
            admin = User.objects.get(id=id)
            admin.first_name = jsondata['first_name']
            admin.last_name = jsondata['last_name']
            admin.email = jsondata['email']
            admin.username = jsondata['username']
            admin.password = jsondata['password']
            admin.save()

            datos = {'message': 'Success'}

        else:

            datos = {'message': 'Admin not found'}

        return JsonResponse(datos)


class GestionarIngresos(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
      
    def get(self, request):
      # ==== Verificamos si el usuario está autenticado === #
        resultado_verificacion = verificarSesion(request)
                
        if resultado_verificacion.status_code != 200:
            
            return resultado_verificacion
        
        lista_de_ingresos = []
        
        ingresos = list(Ingreso.objects.values())
        
        for ingreso in ingresos:
            
            informacion_ingreso = {
                
                "id" : ingreso['id'],
                "categoria" : ingreso['tipo'],
                "monto" : "{:.2f}".format(ingreso['monto'].to_decimal()),
                "fecha" : ingreso['fecha'].strftime('%Y-%m-%d')
                                
            }
            
            lista_de_ingresos.append(informacion_ingreso)        
        
        return JsonResponse({'message': 'success', 'Ingresos' : lista_de_ingresos}, status = 200)
        

    def post(self, request):
      
      # ==== Verificamos si el usuario está autenticado === #
        resultado_verificacion = verificarSesion(request)
                
        if resultado_verificacion.status_code != 200:
            
            return resultado_verificacion
        
        # === Vamos a agregar un nuevo ingreso === # 
        jsondata = json.loads(request.body)      
      
        try:
            
            tipo = jsondata['tipo']
            descripcion = jsondata['descripcion']
            monto = jsondata['monto']        
            
            Ingreso.objects.create(
            
            tipo = tipo,
            descripcion = descripcion,
            monto = monto
            
            )        
            
            return JsonResponse({'message': 'Income created succesfully'})
        
        except Exception as e:

            return JsonResponse({'message' : 'Error inesperado'}, status = 500)            
    
    def put(self, request):
      pass
    
    def delete(self, request):
      pass
    
    
class GestionEgreso(View):
  
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
            
    def get(self, request):
        
        resultado_verificacion = verificarSesion(request)
                
        if resultado_verificacion.status_code != 200:
            
            return resultado_verificacion
        
        lista_de_egresos = []
        
        egresos = list(Ingreso.objects.values())
        
        for egreso in egresos:
            
            informacion_egreso = {
                
                "id" : egreso['id'],
                "categoria" : egreso['tipo'],
                "monto" : "{:.2f}".format(egreso['monto'].to_decimal()),
                "fecha" : egreso['fecha'].strftime('%Y-%m-%d')
                                
            }
            
            lista_de_egresos.append(informacion_egreso)        
        
        return JsonResponse({'message': 'success', 'egresos' : lista_de_egresos}, status = 200)
    
    def post(self, request):
            # ==== Verificamos si el usuario está autenticado === #
        resultado_verificacion = verificarSesion(request)
                
        if resultado_verificacion.status_code != 200:
            
            return resultado_verificacion
        
        # === Vamos a agregar un nuevo ingreso === # 
        jsondata = json.loads(request.body)      
      
        try:
            
            tipo = jsondata['tipo']
            descripcion = jsondata['descripcion']
            monto = jsondata['monto']        
            
            Egreso.objects.create(  
            
            tipo = tipo,
            descripcion = descripcion,
            monto = monto
            
            )        
            
            return JsonResponse({'message': 'Income created succesfully'})
        
        except Exception as e:

            return JsonResponse({'message' : 'Error inesperado'}, status = 500)  
    
    def put(self, request):
      pass
    
    def delete(self, request):
      pass
    

# === Método para verificar la sesión del usuario administrador
def verificarSesion(request):

    token = request.META.get('HTTP_AUTHORIZATION')
    secret_key = config('JWT_SECRET_KEY')

    if token is None:

        return JsonResponse({'message': 'Token JWT faltante'}, status=401)

    try:

        payload = jwt.decode(token, secret_key, algorithms=['HS256'])        

        usuario = User.objects.get(id=payload['id'])
        
        informacion_usuario = {
            
            "id" : usuario.id,
            "username" : usuario.username,
            "email" : usuario.email,                        
                        
        }
        
        datos = {'message': 'El usuario está autenticado correctamente', 'usuario' : informacion_usuario}

        return JsonResponse(datos, status=200)
      
    except (jwt.ExpiredSignatureError):

        print("Ha ocurrido un error al momento de decodificar el token")

        return JsonResponse({'message': 'Token JWT expirado'}, status=401)
      
    except jwt.DecodeError:
      
        print("Ha ocurrido un error al momento de decodificar el token")
        
        return JsonResponse({'message': 'Error en la verificación del token'}, status = 401)
      
    except User.DoesNotExist:
      
        return JsonResponse({'message': 'El usuario no existe'}, status = 401)
      
    except Exception as e:
        return JsonResponse({'message' : 'Error inesperado'}, status = 500)
      


    
