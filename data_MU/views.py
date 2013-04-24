# Create your views here.

#django standard
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError, transaction

#python standard
import utils as util
import re

#app
from .models import *

@transaction.atomic
def add_datauser(request):

	if request.POST:
		#print request.POST
		companies = {}
		prog = re.compile('\D+')
		for i in request.POST.keys():
			print i
			if i[:6] == "select" or i[:7] == "quality" or i[:5] == "input":
				result = prog.split(i)
				key = result[1]
				util.set_dict(companies,key,i,request.POST[i])
		if "q_storage" in request.POST:
			storage = request.POST["q_storage"]
		name = request.POST["name"]
		er = request.POST["url_or_id"]
		er_id =0 
		url_citizen = 	""
		error = False
		val = URLValidator(verify_exists=False)
		errors = {}
		try:
		    val(er)
		    if url_citizen.index("erepublik.com/en/citizen/profile/") > -1:
		    	url_citizen = er
		    	er_id = er.spliy("/").pop()
		    	if not util.is_int(er):
		    		error = True
		except ValidationError, e:
			errors['url'] = "url invalid"

		if util.is_int(er) and int(er) >0 and :
			er_id = er
			url_citizen = "http://www.erepublik.com/en/citizen/profile/"+er_id
		else:
			errors['id citizen'] = "id invalid"

		if er_id == 0 and len(url_citizen)>:
			error = True
		else:
			errors ={}

		try:
			with transaction.atomic():
				cit=Citizen(name=name,citizen_id_er=er_id,url_citizen=url_citizen)
				cit.save()
				if(storage <> ""):
					sto=Storage(owner_citizen=cit,quantity=storage)
					sto.save()
				for key in companies:
					company = util.get_company(companies[key])
					company.owner_citizen = cit
					company.save()


		except Exception, e:
			errors[e.errno]=e.strerror

	return render_to_response('data_MU/templates/add.html',
			{'errors':errors,}
			,context_instance = RequestContext(request))

add_datauser.transactions_per_request = False