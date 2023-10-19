from django.shortcuts import render
from .models import Usuarios, Comments
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import cloudinary.uploader

# Create your views here.
class UserView(View):
      
      @method_decorator(csrf_exempt)
      def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
      def get(self, request, id = 0):
          
          #Comprobamos si nos están pasando un parámetro
          if id > 0:

            usuarios = list(Usuarios.objects.filter(id = id).values())

            if len(usuarios) > 0:
                
                usuario = usuarios[0]  
                datos = {'message' : 'Success', 'Usuario' : usuario}

            else:

                datos = {'messsage' : 'User not found :('} 

            return JsonResponse(datos) 
          
          else:
            
            usuarios = list(Usuarios.objects.values())
            print(usuarios)
            lista = []

            if len(usuarios) > 0:
                
                for i in usuarios:
                   
                  diccionario = {
                    "name" : i['name'],
                    "last_name" : i['last_name'],
                    "phone" : i['phone'],
                    "email" : i['email'],
                    "username" : i['username'],
                    "photo" : str(i['photo'].url)
                  }

                  lista.append(diccionario)
          
                datos = {'message' : 'Success', 'Users' : lista}

            else:
                
                datos = {'message' : 'Users not found :('}

            return JsonResponse(datos)

      def post(self, request):
          
        jasondata = json.loads(request.body)
    
        Usuarios.objects.create(
            name = jasondata['name'], 
            last_name = jasondata['last_name'], 
            phone = jasondata['phone'], 
            email = jasondata['email'],
            username = jasondata['username'],
            password = jasondata['password'],
            photo = jasondata['photo']  
        )
        
        datos = {'message' :  'Success'}

        return JsonResponse(datos)

      def put(self, request, id):
        
        user = list(Usuarios.objects.filter(id = id).values())

        if len(user) > 0:

          jasondata = json.loads(request.body)
          usuario = Usuarios.objects.get(id = id)
          usuario.name = jasondata['name']
          usuario.last_name = jasondata['last_name']
          usuario.phone = jasondata['phone']
          usuario.email = jasondata['email']
          usuario.save()

          datos = {'message' : 'Success'}

        else:

          datos = {'message' : 'User not found :('}

        return JsonResponse(datos)
        

      def delete(self, request, id):
          pass


class CommentaryUserView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)
    
    #Obtener los comentarios
    def get(self, request):
       
      comments = list(Comments.objects.values())
      comentariosFiltro = []

      if len(comments) > 0:

        for i in comments:  

          usuario = Usuarios.objects.get(id = i['usuario_id'])
        
          diccionario = {
            "username": usuario.name, 
            "userphoto": str(usuario.photo.url),
            "comment": i['comment'],
            "date": i['date'].strftime('%Y-%m-%d')
          }

        comentariosFiltro.append(diccionario)

        datos = {'message' : 'Success', 'comments' : comentariosFiltro}
    
      else:

        datos = {'message' : 'Comments not found :('}

      return JsonResponse(datos)
    
    def post(self, request):
       
      jasondata = json.loads(request.body)
      usuario = Usuarios.objects.get(id = jasondata['user_id'])
      
      Comments.objects.create(
        comment = jasondata['comment'],
        usuario = usuario        
      )
         
      datos = {'messsage' : 'Success'}

      return JsonResponse(datos)