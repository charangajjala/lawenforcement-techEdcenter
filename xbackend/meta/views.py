import io

from classes.models import Class

from django.http import HttpResponse,JsonResponse
from django.template.loader import get_template
from django.core.mail import send_mail,EmailMessage
from django.conf import settings

from django_tex.core import compile_template_to_pdf
from django_tex.shortcuts import render_to_pdf

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

import xhtml2pdf.pisa as pisa

from weasyprint import HTML, CSS

import jinja2
import os
from jinja2 import Template

from classes.models import Invoice,Roster

class RenderToPdf:

  @staticmethod
  def render(path: str,params: dict):
    template = get_template(path)
    html = template.render(params)
    response = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf8')),response)
    if not pdf.err:
        return HttpResponse(response.getvalue(),content_type='text/html')
    else:
      return HttpResponse("error Rendering pdf",status=400)

#if required else dont use it
def render_pdf_view(path: str,params: dict):
  template = get_template(path)
  html = template.render(params)
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'filename="invoice.pdf"'
  pisa_status = pisa.CreatePDF(html,dest=response)
  if pisa_status.err:
    return HttpResponse('We had some error <pre>'+html+'</pre>')
  else:
    return response

class PdfView(APIView):
  permission_classes=[IsAuthenticated]
  
  # xhtml2pdf genarator
  # def post(self,request,id):
  #   user = request.user
    # invoiceObj = Invoice.objects.get(invoiceNum=id)
    # rosterObjs = Roster.objects.filter(invoice=invoiceObj)
    # params = {'invoice':invoiceObj,'rosters':rosterObjs}
    # pdfInHttpResponse = RenderToPdf.render("./invoice.html",params)
  #   if pdfInHttpResponse:
  #       response = HttpResponse(pdfInHttpResponse, content_type='application/pdf')
  #       filename = 'invoice.pdf'
  #       content = "inline; filename='%s'" %(filename)
  #       download = request.GET.get("download")
  #       if download:
  #           content = 'attachment; filename="%s"' %(filename)
  #       response['Content-Disposition'] = content
  #       return response
  #   else:
  #     return HttpResponse("Not found")

  # latex pdf genarator
  def post(self,request,id):
    template_name = 'invoice.tex'
    context = {'foo':'bar'}
    response = render_to_pdf(request,template_name,context,filename='invoice.pdf')
    return response

  #weasyprint pdf genarator
  # def post(self,request,id):
  #   template = get_template('invoice2.html')

  #   invoiceObj = Invoice.objects.get(invoiceNum=id)
  #   rosterObjs = Roster.objects.filter(invoice=invoiceObj)
  #   params = {'invoice':invoiceObj,'rosters':rosterObjs}

  #   html_template = template.render(params)
  #   response = HttpResponse(content_type='application/pdf')
  #   response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
  #   html = HTML(string=html_template)
  #   html.write_pdf(response,stylesheets=[CSS('static/invoice.css')])
  #   return response 

class Contact(APIView):
  @classmethod
  def post(self,request):
      data = request.data
      subject = str(data.get('subject'))
      message= str(data.get('message'))
      whencesoever = str(data.get('email'))
      email = EmailMessage(
        subject=subject,
        body = message,
        from_email = whencesoever,
        to=[settings.EMAIL_HOST_USER],
      )
      email.send()
      response,status = dict(message = 'Email sent successfully'),HTTP_200_OK
      return JsonResponse(response,status=status)


class ClassFlyer(APIView):

  # def post(self,request,id):
  #   template_name = 'flyer.tex'
  #   classObj = Class.objects.get(id=id)
  #   context = {'cls':classObj.course.title}
    # response = render_to_pdf(request,template_name,context,filename='flyer.pdf')
  #   return response

  def post(self,request,id):
    template_name = 'flyer.tex'
    classObj = Class.objects.get(id=id)

    latex_jinja_env = jinja2.Environment(
      block_start_string = '\BLOCK{',
      block_end_string = '}',
      variable_start_string = '\VAR{',
      variable_end_string = '}',
      comment_start_string = '\#{',
      comment_end_string = '}',
      line_statement_prefix = '%%',
      line_comment_prefix = '%#',
      trim_blocks = True,
      autoescape = False,
      loader = jinja2.FileSystemLoader(os.path.abspath('C:/Users/jampu/Desktop/backend/xbackend/templates/'))
    )
    template = latex_jinja_env.get_template(template_name)
    rendered_template = template.render(cls=classObj)
    with open('C:/Users/jampu/Desktop/backend/xbackend/templates/mainflyer.tex','w') as static_flyer:
      static_flyer.write(rendered_template)
    response = render_to_pdf(request,template_name='mainflyer.tex',filename='flyer.pdf')
    return response