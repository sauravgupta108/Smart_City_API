from django.shortcuts import render
from django.http import HttpResponse

from .security import Validator as vldtr, Token_handler as tkn, Key_handler as scrt
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
	def post(self, request, format = None):
		credentials = {}
		credentials['user_id'] = request.POST['user_id']
		credentials['password'] = request.POST['password']
		valid, role = vldtr.are_valid(credentials)
		if valid:
			token = tkn().generate_token(credentials['user_id'], role)
			return Response(token)
		else:
			return Response({'details':'Invalid Credentials'}, status = status.HTTP_401_UNAUTHORIZED)
		
	