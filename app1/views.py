from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
import base64
from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from .models import Service
# Create your views here.

def basic_auth(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token_type, _, credentials = auth_header.partition(' ')

    username, password = base64.b64decode(credentials).split(':')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(status=401)

    password_valid = user.check_password(password)

    if token_type != 'Basic' or not password_valid:
        return HttpResponse(status=401)
    return HttpResponse("Authentification successful")

def index(request):
    context = {}
    portfolios = []
    for serv in Service.objects.all():
        portfolios.append(serv.portfolio)
    context['portfolios'] = portfolios
    return render(request, 'admin/edit_inline/index.html', context)

def login(request):

   context={}
   context.update(csrf(request))
   if(request.POST):
      username=request.POST.get('username','')
      password=request.POST.get('password','')
      user=auth.authenticate(username=username,password=password)
      if user is not None:
         auth.login(request, user)
         return redirect('/after_login')
      else:
         login_error = "Authentication problem: user is not found."
         context['login_error'] = login_error
         return render(request,'admin/edit_inline/login.html/', context)
   else:
      return render(request, 'admin/edit_inline/login.html/', context)

def logout(request):
   auth.logout(request)
   return redirect('/login')

@api_view(["POST"])

def IdealWeight(heightdata):

    try:

        height=json.loads(heightdata.body)

        weight=str(height*10)

        return JsonResponse("Ideal weight should be:"+weight+" kg",safe=False)

    except ValueError as e:

        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
