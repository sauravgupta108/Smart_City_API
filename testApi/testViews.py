from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import testModels, testSrlzd

# Create your views here.

def index(request):
	return HttpResponse("App for testing....")
	
class ListPart(APIView):
	def get(self, request, format = None):
		obj = testModels.testapi.objects.all()
		srlzdDta = testSrlzd.SrlzdTestapi(obj, many = True)
		return Response(srlzdDta.data)
		
	def post(self, request, format = None):
		srlzd = testSrlzd.SrlzdTestapi(data=request.data)
		
		if srlzd.is_valid():
			try:
				if srlzd.validity():
					srlzd.save()
					response_data = {'status':'201', 'msg':'Record Added Successfully', 'id':srlzd.data['id'], 'error':'None'}
					return Response(response_data, status = status.HTTP_201_CREATED)
				else:
					return Response({'status':'400', 'error':'Person must born before 2000'}, status=status.HTTP_400_BAD_REQUEST)
			except ValueError:
				return Response({'status':'400', 'error':'Invalid Date (date must be in yyyy-mm-dd)'}, status=status.HTTP_400_BAD_REQUEST)
			
		else:
			return Response({'status':'400', 'error':'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
			
class DetailPart(APIView):
	def get_object(self, pk):
		try:
			objct = testModels.testapi.objects.get(id = pk)
		except: 
			objct = None
		return objct
			
	def get(self, request, pk, format = None):
		dta = self.get_object(pk)
		if dta:
			SRL_DATA = testSrlzd.SrlzdTestapi(dta)
			return Response(SRL_DATA.data)
		else:
			return Response({'error':'404 NOT FOUND'}, status = status.HTTP_404_NOT_FOUND)
	
	def put(self, request, pk, format = None):
		dta = self.get_object(pk)