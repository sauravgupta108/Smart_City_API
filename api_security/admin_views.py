from django.shortcuts import render
from django.http import HttpResponse

import copy

from . import models, model_serializer as MDLSZ

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins as MXN

# Create your views here.
def test(request):
	return HttpResponse('working.....!!!!')
	
class Authentication(APIView):
	def get(self, request, format = None):
		return Response(request.authenticators)
		
	