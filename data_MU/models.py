from django.db import models

# Create your models here.

class Citizen(models.Model):

	name = models.CharField(max_length=100)
	er_id = models.PositiveIntegerField()

class Storage(models.Model):

	owner_citizen = models.ForeignKey('citizen')
	date_update = models.DateField(auto_now=True)

class Company(models.Model):
	owner_citizen = models.ForeignKey('citizen')
	quality = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	date_update = models.DateField(auto_now=True)	

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
	def produce(self):
		return 35*self.quality


class RawWeaponCompany(RawCompany):
	pass

class RawFoodCompany(RawCompany):
	pass

class MilitaryUnit(models.Model):
	name = models.CharField(max_length=100)
	er_id = models.PositiveIntegerField()
	ulr_img = models.TextField(null=True,blank=True)
	members = models.ManyToManyField(Citizen, through='Membership')

class MUMembers(models.Model):
	person = models.ForeignKey(Citizen)
	mu_group = models.ForeignKey(MilitaryUnit)
	date_joined = models.DateField()
