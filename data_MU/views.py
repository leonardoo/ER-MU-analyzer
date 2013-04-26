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
				
				Tg = TraningGround(owner_citizen=cit)
				Tg.weights_room = request.POST['weights_room']
				Tg.climbing_center = request.POST['climbing_center']
				Tg.shooting_range = request.POST['shooting_range']
				Tg.special_forces = request.POST['special_forces']
				Tg.save()

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
			  'storage':0,
			  'companies':{'RawFood':{4:0,5:0},
						   'RawWeapon':{4:0,5:0},
						   'Weapon':{5:0,6:0,7:0},
						   'Food':{5:0,6:0,7:0}
						}
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
		citizen_data['companies'] = {'RawFood':{4:0,5:0},
									 'RawWeapon':{4:0,5:0},
									 'Weapon':{5:0,6:0,7:0},
									 'Food':{5:0,6:0,7:0}
									 }

		for obj in objects:
			companies = obj.filter(owner_citizen__exact = citizen)
			citizen_data['quantity'] += companies.count()

			if citizen_data['quantity'] >0:
				companies_for_q=companies.filter(quality__gte=4)
				for company in companies_for_q:
					
					t_company = int(company.type_company)
					key = company.get_type_company_display()
					if t_company <=2 or  company.quality > 4:
						citizen_data['companies'][key][company.quality] = company.quantity
						totals['companies'][key][company.quality] += company.quantity

		print citizen_data['companies']
		totals['quantity'] = citizen_data['quantity']
		data.append(citizen_data)

	return render_to_response('data_MU/templates/view_data.html',
			{'profiles':data,
			'totals':totals}
			,context_instance = RequestContext(request))


def data_user(request):
	citizen = Citizen.objects.filter(pk=1)
	objects = [WeaponCompany.objects,FoodCompany.objects,
					RawWeaponCompany.objects,RawFoodCompany.objects]
	data_companies = {
	'RawFood':{},
	'RawWeapon':{},
	'Weapon':{},
	'Food':{}
	}
	for obj in objects:
			companies = obj.filter(owner_citizen__exact = citizen)
			if companies.count() >0:
				for company in companies:
					key = company.get_type_company_display()
					if not company.quantity in data_companies[key]:
						data_companies[key][company.quality] = 0
					data_companies[key][company.quality] = company.quantity

	TG = TraningGround.objects.get(owner_citizen__exact = citizen)
	TG_data = {}
	if(TG != None):
		TG_data = {'TG1':TG.weights_room,
							  'TG2': TG.climbing_center,
							  'TG3': TG.shooting_range,
							  'TG4': TG.special_forces}

	return render_to_response('data_MU/templates/test.html',
			{'companies':data_companies,
			'TG':TG_data}
			,context_instance = RequestContext(request))




def view_user_mu_data(request):

	citizens = Citizen.objects.all()
	data = []

	for citizen in citizens:
		citizen_data = {}
		citizen_data['quantity'] = 0
		objects = [WeaponCompany.objects,FoodCompany.objects,
					RawWeaponCompany.objects,RawFoodCompany.objects]
		citizen_data['storage'] = Storage.objects.get(owner_citizen__exact = citizen).quantity
		totals['storage'] = citizen_data['storage']
		citizen_data['name'] = citizen.name
		citizen_data['id'] = citizen.citizen_id_er
		TG = TraningGround.objects.get(owner_citizen__exact = citizen)
		if(type(TG) == "TraningGround"):
			citizen_data['TG'] = {'TG1':TG.weights_room,
									'TG2': TG.climbing_center,
									'TG3': TG.shooting_range,
									'TG4': TG.special_forces}
		for obj in objects:
			companies = obj.filter(owner_citizen__exact = citizen)
			citizen_data['quantity'] += companies.count()

			citizen_data['companies'] = {'RawFood':{4:0,5:0},
										 'RawWeapon':{4:0,5:0},
										 'Weapon':{5:0,6:0,7:0},
										 'Food':{5:0,6:0,7:0}
										 }
	
			if citizen_data['quantity'] >0:

				for company in companies:
					t_company = int(company.type_company)
					key = company.get_type_company_display()
					if t_company <=2 or  company.quality > 4:
						citizen_data['companies'][key][company.quality] = company.quantity
						totals['companies'][key][company.quality] += company.quantity

		totals['quantity'] = citizen_data['quantity']
		data.append(citizen_data)

	#return render_to_response('data_MU/templates/view_data.html',
	#		{'profiles':data,
	#		'totals':totals}
	#		,context_instance = RequestContext(request))



