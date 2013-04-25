from django.db import models

# Create your models here.

class Citizen(models.Model):

	name = models.CharField(max_length=100)
	citizen_id_er = models.PositiveIntegerField()
	url_citizen = models.URLField()

class Storage(models.Model):

	owner_citizen = models.ForeignKey('citizen')
	quantity = models.PositiveIntegerField(default=0)
	date_update = models.DateField(auto_now=True)

class Company(models.Model):
	TYPES_COMPANIES = {
		("1",'RawFood'),
  		("2",'RawWeapon'),
		("3",'Weapon'),
		("4",'Food'),
	}

	owner_citizen = models.ForeignKey('citizen')
	quality = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	date_update = models.DateField(auto_now=True)
	type_company = models.CharField(max_length=1, choices=TYPES_COMPANIES)

	def cost(self):
		return 0

	def produce(self):
		return 0

	def consume(self):
		return 0


	class Meta:
		abstract = True

class ManufactureCompany(Company):
	class Meta:
		abstract = True

	def produce(self):
		return 100 * self.quality

	def consume(self):
		if self.quality <7:
			return 100 * self.quality
		else:
			return 2000	

class WeaponCompany(ManufactureCompany):

	def produce(self):
		return super(WeaponCompany,self).produce() / 100
		

class FoodCompany(ManufactureCompany):
	pass

class RawCompany(Company):

	class Meta:
		abstract = True

	def produce(self):
		return 35*self.quality


class RawWeaponCompany(RawCompany):
	pass

class RawFoodCompany(RawCompany):
	pass

class MilitaryUnit(models.Model):
	name = models.CharField(max_length=100)
	er_id = models.PositiveIntegerField()
	url_img = models.TextField(null=True,blank=True)
	members = models.ManyToManyField(Citizen, through='MUMembers')

class MUMembers(models.Model):
	person = models.ForeignKey(Citizen)
	mu_group = models.ForeignKey(MilitaryUnit)
	date_joined = models.DateField()
