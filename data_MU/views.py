# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import CitizenForm
def add_datauser(request):

	if request.POST:
		pass

	form = CitizenForm()
	return render_to_response('data_MU/templates/add.html',
			{"form": form}
			,context_instance = RequestContext(request))
