from django.urls import path
from . import views

urlpatterns = [
  path('admin/hosts/locations/',views.AdminLocationsAPI.as_view(),name='admin_locations'),
  path('admin/hosts/locations/<int:id>',views.AdminLocationAPI.as_view(),name='admin_location'),
  path('admin/hosts/',views.AdminHostsAPI.as_view(),name='admin_hosts'),
  path('admin/hosts/<int:id>',views.AdminHostAPI.as_view(),name='admin_host'),

  path('hosts/',views.StandardHostAPI.as_view(),name='host'),

  path('hosts/filterlist/',views.HostListAPI.as_view(),name='host_list'),
  
  path('hosts/<int:id>',views.AdditionalHostServices.as_view(),name='host_profile'),
  path('hosts/locations/',views.StandardLocationsView.as_view(),name='locations'),
  path('hosts/locations/<int:id>',views.StandardLocationView.as_view(),name='location')
]