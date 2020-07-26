from django.db import models

# Create your models here.
class Dealer(models.Model):
	name=models.CharField(max_length=50)
	location=models.TextField()

	def __str__(self):
		return self.name


class Brand(models.Model):
	name=models.CharField(max_length=50)
	image=models.ImageField(upload_to ='uploads/')

	def __str__(self):
		return '%s' % (self.name)

class Product(models.Model):
	brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
	dealer_id = models.ForeignKey(Dealer, on_delete=models.CASCADE)
	title=models.CharField(max_length=50)
	description=models.TextField()
	address=models.TextField()
	price=models.CharField(max_length=50,default=0)
	publish=models.BooleanField(default=True)

	def __str__(self):
		return self.title

class ProductImage(models.Model):
	pro_id=models.ForeignKey(Product, on_delete=models.CASCADE)
	pro_img=models.ImageField(upload_to ='uploads/')
	inlines=[
		Product,
	]

	def __str__(self):
		return '{0} {1} {2}'.format(self.pro_id,'-',self.pro_img)

class User(models.Model):
	full_name=models.CharField(max_length=50)
	email=models.EmailField(max_length=50)
	mobile=models.CharField(max_length=50,blank=True)
	username=models.CharField(max_length=50)
	password=models.CharField(max_length=50)

	def __str__(self):
		return '{0}'.format(self.username)

# Enquiry Model
class Enquiry(models.Model):
	product_id=models.CharField(max_length=50,default=0)
	email=models.CharField(max_length=100)
	full_name=models.CharField(max_length=50)
	mobile=models.CharField(max_length=50)
	enquiry_note=models.TextField()

	def __str__(self):
		return '{0} {1}'.format('Enquiry From ',self.email+' '+self.mobile)