from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
import base64
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

@api_view(["POST"])

def IdealWeight(heightdata):

    try:

        height=json.loads(heightdata.body)

        weight=str(height*10)

        return JsonResponse("Ideal weight should be:"+weight+" kg",safe=False)

    except ValueError as e:

        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)