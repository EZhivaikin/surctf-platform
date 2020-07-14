from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseRedirectBase
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from teams.models import Availability


class AvailabilityMiddleware(MiddlewareMixin):

	def process_request(selfs, request):
		availability = Availability.objects.order_by('start_at').first()
		if availability is None:
			return
	
		current_time = timezone.now()
		if current_time < availability.start_at:
			if not request.path.startswith(('/rating', '/login', '/logout')):
				if not (request.user.is_superuser):
					return HttpResponseRedirect('/rating')
			
		if current_time > availability.end_at:
			if request.path.startswith('/tasks/send_flag'):
				if not (request.user.is_superuser):
					return HttpResponseRedirect('/rating')