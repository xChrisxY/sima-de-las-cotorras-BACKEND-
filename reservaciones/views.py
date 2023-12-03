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

    def get(self, request, id=0):

        print("Estamos pasando por aquí")
      # ==== Obteniendo todas las resrevaciones del usuario === #
        if id > 0:

            reservaciones_aventura = list(ReservaAventura.objects.values())
            reservaciones_del_usuario = []

            for reservacion in reservaciones_aventura:

                if (id == reservacion['usuario_id']):

                    aventura_id = reservacion['aventura_id']
                    pago_id = reservacion['pago_id']

                    aventura = Aventura.objects.get(id=aventura_id)
                    pago = Pago.objects.get(id=pago_id)
                    usuario = Usuarios.objects.get(id=id)

                    informacion_de_reservacion = {

                        "nombre_usuario": usuario.name,
                        "apellido_usuario": usuario.last_name,
                        "nombre_aventura": aventura.nombre,
                        "precio_aventura": "{:.2f}".format(aventura.precio.to_decimal()),
                        "fecha_de_pago": pago.fecha.strftime('%Y-%m-%d'),
                        "fecha_aventura": reservacion['fecha']

                    }

                    reservaciones_del_usuario.append(
                        informacion_de_reservacion)

            return JsonResponse({'message': 'Success', 'reservaciones': reservaciones_del_usuario}, status=200)

        else:

            # Obteniendo todos los usuarios que han reservado
            reservaciones_aventura = list(ReservaAventura.objects.values())
            usuarios_con_reservacion = []

            for reservacion in reservaciones_aventura:

                # Obtenemos el ID de pago, usuario y aventura
                aventura_id = reservacion['aventura_id']
                usuario_id = reservacion['usuario_id']
                pago_id = reservacion['pago_id']

                # Buscamos en las colecciones Usuario, Aventura y Pago los registros correspondientes
                aventura = Aventura.objects.get(id=aventura_id)
                usuario = Usuarios.objects.get(id=usuario_id)
                pago = Pago.objects.get(id=pago_id)                

                # Construimos el diccionario con la información que nos interesa
                informacion_de_reservacion = {

                    "nombre_de_usuario": usuario.name,
                    "apellido_de_usuario": usuario.last_name,
                    "email_usuario" : usuario.email,
                    "telefono_usuario" : usuario.phone,
                    "nombre_servicio": aventura.nombre,                    
                    "pago": "{:.2f}".format(pago.monto.to_decimal()),
                    "fecha_de_pago": pago.fecha.strftime('%Y-%m-%d'),
                    "fecha_reservacion" : reservacion['fecha']

                }

                usuarios_con_reservacion.append(informacion_de_reservacion)

            datos = {
                'message': "Success",
                "usuarios_con_reservacion": usuarios_con_reservacion
            }

        return JsonResponse(datos)

    def post(self, request):

        # === Creando el pago del usuario === #

        jasondata = json.loads(request.body)

        # Obtenemos el id del pago para poder instanciarlo
        pago = Pago.objects.create(

            monto=jasondata['pago']['monto'],
            numero_transaccion=jasondata['pago']['numero_transaccion']

        )

        pago_id = pago.id

        # Creando el registro de la reservación
        aventura_a_reservar = Aventura.objects.get(id=jasondata['aventura'])
        usuario = Usuarios.objects.get(id=jasondata['usuario'])
        pago_del_usuario = Pago.objects.get(id=pago_id)
        fecha_de_reservacion = datetime.strptime(jasondata['fecha_reservacion'], "%Y-%M-%d").strftime('%Y-%m-%d')

        ReservaAventura.objects.create(

            fecha=fecha_de_reservacion,
            aventura=aventura_a_reservar,
            usuario=usuario,
            pago=pago_del_usuario

        )

        datos = {'Message': 'Success'}

        return JsonResponse(datos)


class ReservacionesCabañas(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):

      # Obtenemos las reservaciones del usaurio
        if id > 0:

            reservaciones_cabaña = list(ReservaCabaña.objects.values())
            reservaciones_del_usuario = []

            for reservacion in reservaciones_cabaña:

                if (id == reservacion['usuario_id']):

                    cabaña_id = reservacion['cabaña_id']
                    pago_id = reservacion['pago_id']

                    usuario = Usuarios.objects.get(id=id)
                    cabaña = Cabaña.objects.get(id=cabaña_id)
                    pago = Pago.objects.get(id=pago_id)

                    informacion_reservacion = {

                        "nombre_de_usuario": usuario.name,
                        "apellido_de_usuario": usuario.last_name,
                        "nombre_cabaña": cabaña.nombre,
                        "fecha_de_pago": pago.fecha.strftime('%Y-%m-%d'),
                        "fecha_de_estancia": f"{reservacion['fecha_de_reservacion'].strftime('%Y-%m-%d')} - {reservacion['fecha_de_salida'].strftime('%Y-%m-%d')}",
                        "precio_cabaña" : "{:.2f}".format(pago.monto.to_decimal())                        
                    }

                    reservaciones_del_usuario.append(informacion_reservacion)

            return JsonResponse({'message': 'Success', 'reservaciones': reservaciones_del_usuario}, status=200)

        else:

            reservaciones_cabaña = list(ReservaCabaña.objects.values())
            usuarios_con_reservacion = []

            for reservacion in reservaciones_cabaña:

                usuario_id = reservacion['usuario_id']
                cabaña_id = reservacion['cabaña_id']
                pago_id = reservacion['pago_id']

                usuario = Usuarios.objects.get(id=usuario_id)
                cabaña = Cabaña.objects.get(id=cabaña_id)
                pago = Pago.objects.get(id=pago_id)                                

                informacion_reservacion = {

                    "nombre_de_usuario": usuario.name,
                    "apellido_de_usuario": usuario.last_name,
                    "email_usuario" : usuario.email,
                    "telefono_usuario" : usuario.phone,
                    "nombre_servicio": cabaña.nombre,
                    "fecha_de_pago": pago.fecha.strftime('%Y-%m-%d'),
                    "pago" : "{:.2f}".format(pago.monto.to_decimal()),
                    "fecha_reservacion" : reservacion['fecha_de_reservacion']

                }

                usuarios_con_reservacion.append(informacion_reservacion)

            return JsonResponse({'message': 'Success', 'reservaciones': usuarios_con_reservacion})

      # ====== CREAMOS LA RESERVACIÓN DE LA CABAÑA ====== #

    def post(self, request):

        # Creando el pago del usuario
        jsondata = json.loads(request.body)
        print(jsondata)

        # === Creamos el pago del usuario === #
        pago = Pago.objects.create(

            monto=jsondata['pago']['monto'],
            numero_transaccion=jsondata['pago']['numero_transaccion']

        )

        # Obtenemos el id del pago para instanciarlo
        pago_id = pago.id

        # Obtenemos las demas instancias
        usuario = Usuarios.objects.get(id=jsondata['usuario'])
        cabaña_a_reservar = Cabaña.objects.get(id=jsondata['cabaña'])
        pago = Pago.objects.get(id=pago_id)
        fecha_de_reservacion = datetime.strptime(jsondata['fecha_de_reservacion'], "%Y-%M-%d").strftime('%Y-%m-%d')
        fecha_de_salida = datetime.strptime(jsondata['fecha_de_salida'], "%Y-%M-%d").strftime('%Y-%m-%d')

        # Creamos la reservación
        ReservaCabaña.objects.create(

            fecha_de_reservacion=fecha_de_reservacion,
            fecha_de_salida=fecha_de_salida,
            usuario=usuario,
            cabaña=cabaña_a_reservar,
            pago=pago

        )

        return JsonResponse({'message': 'Success'})


class CreatecCheckoutSessionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, id):   
        
        jsondata = json.loads(request.body)
        
        if (jsondata['servicio'] == 'cabaña'):
            
            #Busquemos para ver si es una cabaña
            cabaña = Cabaña.objects.get(id = id)
            price_id = cabaña.price_id
            print(price_id)
            
        else:    
            
            aventura = Aventura.objects.get(id = id)
            price_id = aventura.price_id
            print(price_id)

        YOUR_DOMAIN = "http://localhost:5173"    
        
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        # price_1O3lzsB4lOKww4uzEGAjK0Do
                        'price': price_id,
                        'quantity' : 1                        
                    },
                ],
                payment_method_types = ["card"],
                mode='payment',
                success_url=YOUR_DOMAIN + f'/actividad-usuario/' + '?success=true',
                cancel_url=YOUR_DOMAIN + '?canceled=true',
            )

            data = {'id': checkout_session.id, "session" : checkout_session.url}

            return JsonResponse(data)

        except Exception as e:
            
            error_info = {
                'error_type': 'InvalidRequestError',
                'error_message': str(e),
            }
            
            print(error_info)

            return JsonResponse(error_info, safe=False)


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

                    "id": aventura['id'],
                    "nombre": aventura['nombre'],
                    "descripcion": aventura['descripcion'],
                    "precio": "{:.2f}".format(aventura['precio'].to_decimal())

                }

                lista_de_aventuras.append(informacion_aventura)

            data = {'message': 'Success', 'aventuras': lista_de_aventuras}

            return JsonResponse(data)

        except Exception as e:

            data = {'message': 'Fatal error'}

            return JsonResponse(data)


class CabañasView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        try:

            cabañas = list(Cabaña.objects.values())

            lista_de_cabañas = []

            for i in cabañas:

                informacion_cabaña = {

                    'id': i['id'],
                    'nombre': i['nombre'],
                    'descripcion': i['descripcion'],
                    'precio': "{:.2f}".format(i['precio'].to_decimal())

                }

                lista_de_cabañas.append(informacion_cabaña)

            datos = {'message': lista_de_cabañas}

            return JsonResponse(datos)

        except Exception as e:

            data = {'message': e}
            
            return JsonResponse(data)
        
def verificarReservacion(request, id, fecha):
    # Aquí comprobamos si la fecha está disponible
        
    reservaciones_cabaña = list(ReservaCabaña.objects.values())    
    reservado = False
    
    for reservacion in reservaciones_cabaña:
        
        if reservacion['cabaña_id'] == id:
                    
            if (str(reservacion['fecha_de_reservacion']) == fecha):
                reservado = True
                break
    
    if reservado:        
                                         
        data = {'message': 'La cabaña está siendo ocupada en esa fecha'}
        return JsonResponse(data, status = 201)
    
    else:
        
        data = {'message': 'La cabaña no está siendo ocupada en esa fecha'}
        return JsonResponse(data, status = 200)
    

