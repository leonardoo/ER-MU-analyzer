from .models import WeaponCompany,FoodCompany, RawFoodCompany,RawWeaponCompany
def set_dict(dic,key,data,value):
	if key not in dic:
		dic[key]={}

	company = dic[key]

	if data[:6] == "select":
		company["company"] = value
	elif data[:7] == "quality":
		company["quality"] = value
	elif data[:5] == "input":
		company["quantity"] = value

def is_int(a):
	"""Returns true if a is an interger"""
	try:
		int (a)
		return True
	except:
		return False

def get_company(company):
	
	if int(company["company"]) == 1:
		fabric = RawFoodCompany(type_company=1)
	elif int(company["company"]) == 2:
		fabric = RawWeaponCompany(type_company=2)
	elif int(company["company"]) == 3:
		fabric = WeaponCompany(type_company=3)
	else:
		fabric = FoodCompany(type_company=4)


	if (company["company"] == 1 or company["company"] == 2) and company["quality"] > 5:

	    fabric.quality = 5
	else:
		fabric.quality = company["quality"]

	if company["quantity"]<0:
		company["quantity"]=0

	fabric.quantity = company["quantity"]

	return fabric