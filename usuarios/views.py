from django.shortcuts import render
from .models import Usuarios, Comments
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login
import json
import cloudinary.uploader
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from decouple import config
import base64

# Create your views here.
class UserView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):

        # Comprobamos si nos están pasando un parámetro
        if id > 0:

            print(request.session.get('user_id', None))

            if request.session.get('user_id', None) is not None:

                user_id = request.session.get('user_id', None)

                usuarios = list(Usuarios.objects.filter(id=user_id).values())

                if len(usuarios) > 0:

                    usuario = usuarios[0]

                    informacion_usuario = {

                        "name": usuario['name'],
                        "last_name": usuario['last_name'],
                        "phone": usuario['phone'],
                        "email": usuario['email'],
                        "username": usuario['username'],
                        "photo": str(usuario['photo'].url)

                    }

                    datos = {'message': 'Success',
                             'Usuario': informacion_usuario}

                else:

                    datos = {'messsage': 'User not found :('}

            else:

                datos = {'messsage': 'User not found :('}

            return JsonResponse(datos)

        else:

            usuarios = list(Usuarios.objects.values())
            print(usuarios)
            lista = []

            if len(usuarios) > 0:

                for i in usuarios:

                    diccionario = {
                        "name": i['name'],
                        "last_name": i['last_name'],
                        "phone": i['phone'],
                        "email": i['email'],
                        "username": i['username'],
                        "photo": str(i['photo'].url)
                    }

                    lista.append(diccionario)

                datos = {'message': 'Success', 'Users': lista}

            else:

                datos = {'message': 'Users not found :('}

            return JsonResponse(datos)

    def post(self, request):

        jasondata = json.loads(request.body)

        # ========= Método de autenticación =========
        
        if len(jasondata) == 2:

            try:

                if 'username' in jasondata and 'password' in jasondata:

                    # Traemos la lista de los usuarios
                    usuarios = list(Usuarios.objects.values())
                    user = None

                    for usuario in usuarios:

                        if (usuario['username'] == jasondata['username'] and usuario['password'] == jasondata['password']):
                            user = usuario
                            break

                    if user is not None:

                        payload = {

                            'username': usuario['username'],
                            'id': usuario['id'],
                            'exp': datetime.utcnow() + timedelta(days=1)
                            
                        }

                        secret_key = config('JWT_SECRET_KEY')

                        token = jwt.encode(
                            payload, secret_key, algorithm="HS256")

                        datos = {
                            'message': "El usuario se ha autenticado correctamente", "token": token}

                        return JsonResponse(datos, status=200)

                    else:

                        datos = {
                            'message': "El usuario NO se ha autenticado correctamente"}

                        return JsonResponse(datos, status=401)

                else:

                    return HttpResponse('Faltan datos de autenticación', status=400)

            except json.JSONDecodeError:

                return HttpResponse('Datos JSON inválidos', status=400)

        # ====== Método para crear un nuevo usuario =====
        else:
                                                                                                             
            try:
                
                jasondata = json.loads(request.body)   
                
                imagen_base_64 = jasondata['imagen']                         
                
                upload_result = cloudinary.uploader.upload(
                    
                   imagen_base_64,
                   folder="proyecto"
                    
                )                
                
                # Creamos el usuario en la base de datos
                usuario = Usuarios.objects.create(
                    name=jasondata['nombre'],
                    last_name=jasondata['apellidos'],
                    phone=jasondata['telefono'],
                    email=jasondata['correo'],
                    username=jasondata['usuario'],
                    password=jasondata['contraseña'],
                    photo=upload_result["url"]
                )

                # Creamos el token para el usuario dado de alta
                print("Ya se ha creado el usuario")
                usuario_id = usuario.id
                username = usuario.username
                payload = {

                    'username': username,
                    'id': usuario_id,
                    'exp': datetime.utcnow() + timedelta(days=1)
                            
               }

                secret_key = config('JWT_SECRET_KEY')

                token = jwt.encode(payload, secret_key, algorithm="HS256")

                datos = {'message': "El usuario se ha autenticado correctamente", "token": token}                            
                return JsonResponse(datos, status = 200)
                
            except :
                print("Hubo un error")
                datos = {'message':  "Not found"}                        
                return JsonResponse(datos, status = 400)

    def put(self, request, id):

        user = list(Usuarios.objects.filter(id=id).values())

        if len(user) > 0:

            jasondata = json.loads(request.body)
            usuario = Usuarios.objects.get(id=id)
            usuario.name = jasondata['name']
            usuario.last_name = jasondata['last_name']
            usuario.phone = jasondata['phone']
            usuario.email = jasondata['email']
            usuario.save()

            datos = {'message': 'Success'}

        else:

            datos = {'message': 'User not found :('}

        return JsonResponse(datos)

    def delete(self, request, id):
        pass


# ====== Este método es para verificar la autenticación del usuario =====
def verificarSesion(request):

    token = request.META.get('HTTP_AUTHORIZATION')
    secret_key = config('JWT_SECRET_KEY')

    if token is None:

        return JsonResponse({'message': 'Token JWT faltante'}, status=401)

    try:

        payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        usuario = Usuarios.objects.get(id=payload['id'])
        
        informacion_usuario = {
            
            "id" : usuario.id,
            "username" : usuario.username,
            "email" : usuario.email,
            "phone" : usuario.phone,
            "photo" : str(usuario.photo.url)
                        
        }

        return JsonResponse({'message': 'El usuario está autenticado correctamente', 'usuario' : informacion_usuario}, status=200)

    except (jwt.ExpiredSignatureError, jwt.DecodeError):

        print("Ha ocurrido un error al momento de decodificar el token")

        return JsonResponse({'message': 'Token JWT inválido o expirado'}, status=201)


class CommentaryUserView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Obtener los comentarios
    def get(self, request, id=0):

        comments = list(Comments.objects.values())

        comentariosFiltro = []

        if len(comments) > 0:

            for i in comments:

                usuario = Usuarios.objects.get(id=i['usuario_id'])

                diccionario = {
                    "username": usuario.name,
                    "userphoto": str(usuario.photo.url),
                    "comment": i['comment'],
                    "date": i['date'].strftime('%Y-%m-%d')
                }

                comentariosFiltro.append(diccionario)

            datos = {'message': 'Success', 'comments': comentariosFiltro}

        else:

            datos = {'message': 'Comments not found :('}

        return JsonResponse(datos)

    # Publicar un nuevo comentario
    def post(self, request):

        jsondata = json.loads(request.body)

        token = request.META.get('HTTP_AUTHORIZATION')
        secret_key = config('JWT_SECRET_KEY')

        print(f"El token es: {token}")

        if token is None:

            return JsonResponse({'message': 'Token JWT faltante'}, status=401)

        try:

            payload = jwt.decode(token, secret_key, algorithms=['HS256'])

            usuario = Usuarios.objects.get(id=payload['id'])

            # Creamos el comentario y lo almacenamos en la base de datos
            Comments.objects.create(
                comment=jsondata['comment'],
                usuario=usuario
            )

            return JsonResponse({'message': 'El comentario se ha publicado correctamente'}, status=200)

        except (jwt.ExpiredSignatureError, jwt.DecodeError):

            print("Ha ocurrido un error al momento de decodificar el token")

            return JsonResponse({'message': 'Token JWT inválido o expirado'}, status=201)
