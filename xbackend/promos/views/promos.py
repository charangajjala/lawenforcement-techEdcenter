from rest_framework.views import APIView
from rest_framework.status import *

from django.http import JsonResponse

from promos.services import PromoServices

class PromoAPI(APIView):

  def get(self,request,code):
    try:
      response,status = PromoServices.get(code)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)