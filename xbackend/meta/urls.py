from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('invoice/download/<int:id>/',views.PdfView.as_view(),name='invoice_download'),
  path('flyer/download/<int:id>/',views.ClassFlyer.as_view(),name='class_flyer'),
  path('contact/',views.Contact.as_view(),name='contact_smtp')
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
