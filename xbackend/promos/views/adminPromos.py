from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.status import *

from promos.services import AdminPromoServices,AdminPromosServices


class AdminPromosAPI(APIView):
  permission_classes = [IsAdminUser,IsAuthenticated]

  def get(self, request):
    params = request.query_params
    try:
      response,status = AdminPromosServices.get(params)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)

  def post(self,request):
    data = request.data
    user = request.user
    try:
      response,status = AdminPromosServices.create(data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class AdminPromoAPI(APIView):
  permission_classes = [IsAdminUser,IsAuthenticated]

  def get(self, request, id):
    try:
      response,status = AdminPromoServices.get(id)
    except Exception as e:
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def put(self, request, id):
    data = request.data
    user = request.user
    try:
      response,status = AdminPromoServices.update(data,user,id)
    except Exception as e:
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def delete(self,request,id):
    user = request.user
    try:
      response,status = AdminPromoServices.delete(user,id)
    except Exception as e:
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

