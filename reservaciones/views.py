from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Aventura, Cabaña, Pago, ReservaCabaña, ReservaAventura
from usuarios.models import Usuarios
import json
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class ReservacionesAventuras(View):
      
      @method_decorator(csrf_exempt)
      def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

      def get(self, request):
            
            #Obteniendo todos los usuarios que han reservado
            reservaciones_aventura = list(ReservaAventura.objects.values())
            usuarios_con_reservacion = []
            
            for reservacion in reservaciones_aventura:
                  
                  #Obtenemos el ID de pago, usuario y aventura
                  aventura_id = reservacion['aventura_id']
                  usuario_id = reservacion['usuario_id']
                  pago_id = reservacion['pago_id']
                  
                  #Buscamos en las colecciones Usuario, Aventura y Pago los registros correspondientes
                  aventura = Aventura.objects.get(id = aventura_id)
                  usuario =  Usuarios.objects.get(id = usuario_id)
                  pago = Pago.objects.get(id = pago_id)
                  
                  #Construimos el diccionario con la información que nos interesa
                  informacion_de_reservacion = {
                        
                        "nombre_usuario" : usuario.name,
                        "apellido_usuario" : usuario.last_name,
                        "nombre_aventura" : aventura.nombre,
                        "pago" : "{:.2f}".format(pago.monto.to_decimal()),
                        "fecha_de_pago" : pago.fecha.strftime('%Y-%m-%d')
                        
                  }
                  
                  usuarios_con_reservacion.append(informacion_de_reservacion)                  
            
            datos = {
                  'message' : "Success",
                  "usuarios_con_reservacion" : usuarios_con_reservacion
            }
            
            return JsonResponse(datos)

      def post(self, request):
            pass

      def put(self, request):
            pass

      def delete(self, request):
            pass

