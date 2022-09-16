from distutils.log import error
from rest_framework.status import *
from rest_framework.exceptions import *

from promos.serializers import PromoResponse
from promos.models import Promo

import datetime

class PromoServices:

  @classmethod
  def get(cls,code):
    try:
      promoObj = Promo.objects.get(code=code)
      today = datetime.datetime.now().date()
      if today<promoObj.expiryDate:
          if promoObj.isActive == True:
            promoResponse = PromoResponse(promoObj)
            response,status = promoResponse.data,HTTP_200_OK
          else:
            response,status = dict(error='Promo code is not active'),HTTP_400_BAD_REQUEST
            return response,status
      else:
        response,status = dict(error='Promo code was expired'),HTTP_400_BAD_REQUEST
    except Promo.DoesNotExist:
      response,status = dict(error='Promo Code invalid'),HTTP_400_BAD_REQUEST
    return response,status