from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from .models import Aventura, Cabaña, Pago, ReservaCabaña, ReservaAventura
from usuarios.models import Usuarios
from datetime import datetime
import json
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

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
            
            #Creando el pago del usuario
            
            jasondata = json.loads(request.body)
            
            # Obtenemos el id del pago para poder instanciarlo
            pago = Pago.objects.create(
                  
                  monto = jasondata['pago']['monto'],
                  numero_transaccion = jasondata['pago']['numero_transaccion']
                  
            )
            
            pago_id = pago.id
            
            #Creando el registro de la reservación
            aventura_a_reservar = Aventura.objects.get(id = jasondata['aventura'])
            usuario = Usuarios.objects.get(id = jasondata['usuario'])
            pago_del_usuario = Pago.objects.get(id = pago_id)
            fecha_de_reservacion = datetime.strptime(jasondata['fecha_reservacion'],"%Y-%M-%d").strftime('%Y-%m-%d')
            
            ReservaAventura.objects.create(
                  
                  fecha = fecha_de_reservacion,
                  aventura = aventura_a_reservar,
                  usuario = usuario,      
                  pago = pago_del_usuario            
                  
            )
            
            datos = {'Message' : 'Success'}
            
            return JsonResponse(datos)

class ReservacionesCabañas(View):

      @method_decorator(csrf_exempt)
      def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)      
  
      def get(self, request):
            pass
      
      
      def post(self, request):
            pass


class CreatecCheckoutSessionView(View):
      
      @method_decorator(csrf_exempt)
      def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
      def post(self, request):
            
            YOUR_DOMAIN = "http://127.0.0.1:5173"
            
            try:
                  checkout_session = stripe.checkout.Session.create(
                  line_items=[
                  {
                          # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1O3lzsB4lOKww4uzEGAjK0Do',
                        'quantity': 1,
                  },
                  ],
                  mode='payment',
                        success_url=YOUR_DOMAIN + '?success=true',
                        cancel_url=YOUR_DOMAIN + '?canceled=true',
                  )
                  
                  data = {'id' : checkout_session.id}
                  
                  return redirect(checkout_session.url)
            
            except Exception as e:
                  
                  data = {'error' : 'Something went wrong when creating stripe checkout session'}
                  
                  return JsonResponse(data, safe=False)


class AventurasView(View):
      
      @method_decorator(csrf_exempt)
      def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
  
      def get(self, request):
            
            try:
                  aventuras = list(Aventura.objects.values())
                  lista_de_aventuras = []
            
                  for aventura in aventuras:
                        
                        informacion_aventura = {
                              
                              "id_aventura" : aventura['id'],
                              "nombre" : aventura['nombre'],
                              "descripcion" : aventura['descripcion'],
                              "precio" : "{:.2f}".format(aventura['precio'].to_decimal())
                              
                        }     
                  
                        lista_de_aventuras.append(informacion_aventura)
            
                  data = {'message': 'Success', 'aventuras': lista_de_aventuras}
            
                  return JsonResponse(data)
                  
            except Exception as e:
                  
                  data = {'message' : 'Fatal error'}
                  
                  return JsonResponse(data)