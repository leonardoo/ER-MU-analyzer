from .models import WeaponCompany,FoodCompany, RawFoodCompany,RawWeaponCompany

def set_dict(dic,key,data,value):
	pk =key+data 
	if pk not in dic:
		dic[pk]={}

	company = dic[pk]

	company["company"]=key
	company["quality"]=data
	company["quantity"]=value



def is_int(a):
	"""Returns true if a is an interger"""
	try:
		int (a)
		return True
	except:
		return False

def get_company(company):
	
	if company["company"] == "rawfood":
		fabric = RawFoodCompany(type_company=1)
	elif company["company"] == "rawweapon":
		fabric = RawWeaponCompany(type_company=2)
	elif company["company"] == "weapon":
		fabric = FoodCompany(type_company=3)
	elif company["company"] == "food":
		fabric = WeaponCompany(type_company=4)


	if "raw" in company["company"] and int(company["quality"]) > 5:

	    fabric.quality = 5
	else:
		fabric.quality = company["quality"]

	if company["quantity"]<0:
		company["quantity"]=0

	fabric.quantity = company["quantity"]

	return fabric