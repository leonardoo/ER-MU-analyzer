# Create your views here.

#app
from .models import *

#django standard
from django.core.validators import URLValidator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import IntegrityError, transaction

#python standard
import utils as util
import re

@transaction.commit_on_success
def add_datauser(request):

	errors={}

	if request.POST:
		#print request.POST
		companies = {}
		prog = re.compile('\D+')
		for i in request.POST.keys():
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
		val = URLValidator()
		try:
		    val(er)
		    if url_citizen.index("erepublik.com/en/citizen/profile/") > -1:
		    	url_citizen = er
		    	er_id = er.spliy("/").pop()
		    	if not util.is_int(er):
		    		error = True
		except Exception, e:
			errors['url'] = "url invalid"

		if util.is_int(er) and int(er) >0 :
			er_id = er
			url_citizen = "http://www.erepublik.com/en/citizen/profile/"+er_id
		else:
			errors['id citizen'] = "id invalid"

		if er_id == 0 and len(url_citizen)>0:
			error = True
		else:
			errors ={}

		if not error:
			try:
				
	
				cit=Citizen(name=name,citizen_id_er=er_id,url_citizen=url_citizen)
				cit.save()
				
				sto=Storage(owner_citizen=cit)
				if(storage <> "" and  util.is_int(storage)):
					sto.quantity=int(storage)
				sto.save()
				for key in companies:
					company = util.get_company(companies[key])
					company.owner_citizen = cit
					company.save()
	
	
			except Exception, e:
				transaction.rollback()
				errors[e.errno]=e.strerror

	return render_to_response('data_MU/templates/add.html',
			{'errors':errors,}
			,context_instance = RequestContext(request))

add_datauser.transactions_per_request = False


def view_data_mu(request):

	citizens = Citizen.objects.all()
	data = []
	totals = {'quantity':0,
			  'storage':0
			}
	for citizen in citizens:
		citizen_data = {}
		citizen_data['quantity'] = 0
		objects = [WeaponCompany.objects,FoodCompany.objects,
					RawWeaponCompany.objects,RawFoodCompany.objects]
		citizen_data['storage'] = Storage.objects.get(owner_citizen__exact = citizen).quantity
		totals['storage'] =citizen_data['storage']
		citizen_data['name'] = citizen.name
		citizen_data['id'] = citizen.citizen_id_er

		for obj in objects:
			companies = obj.filter(owner_citizen__exact = citizen)
			citizen_data['quantity'] += companies.count()

			citizen_data['companies'] = {'RawFood':{4:0,5:0},
										 'RawWeapon':{4:0,5:0},
										 'Weapon':{5:0,6:0,7:0},
										 'Food':{5:0,6:0,7:0}
										 }
	
			if citizen_data['quantity'] >0:
				companies_for_q=companies.filter(quality__gte=4)
				for company in companies_for_q:
					t_company = company.type_company
					key= company.get_type_company_display()
					if t_company <=2:
						citizen_data['companies'][key][company.quality] = company.quantity
					elif company.quality >4:
						citizen_data['companies'][key][company.quality] = company.quantity
		totals['quantity'] = citizen_data['quantity']
		data.append(citizen_data)

	return render_to_response('data_MU/templates/view_data.html',
			{'profiles':data,
			'totals':totals}
			,context_instance = RequestContext(request))






