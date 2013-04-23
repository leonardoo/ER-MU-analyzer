from .models import *
from django.forms import *

class CitizenForm(ModelForm):
	class Meta:
		model = Citizen