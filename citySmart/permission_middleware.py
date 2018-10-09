from rest_framework.response import Response
from django.http import HttpResponse

from api_security.security import Validator as vldt

class check_permission(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, func, args, kwargs):
		app_name = request.path_info.split('/')[1]
		
		if app_name == 'citysmart':
			try:
				key = request.GET["key"]
				client_id = request.GET["client_id"]
			except KeyError:
				return HttpResponse(str({"details":"Key and client_id required."}), status = 400)

			if not vldt().has_permission(key, client_id, request.method):
				return HttpResponse(str({'details': 'Not Authorized.'}), status = 403)

		return None

	'''def process_exception(self, request, exp):
		return HttpResponse("self.i")'''