from django.urls import path
from . import views

urlpatterns = [
  path('promos/<str:code>/',views.PromoAPI.as_view(),name='promo'),
  path('admin/promos/',views.AdminPromosAPI.as_view(),name='admin_promos'),
  path('admin/promos/<int:id>/',views.AdminPromoAPI.as_view(),name='admin_promo'),
]
