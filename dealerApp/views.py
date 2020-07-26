from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.core import serializers
import json,pprint
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Count
from .models import Brand,Product,ProductImage,User,Dealer,Enquiry
# Create your views here.
def index(request):
	car_name=''
	products=Product.objects.all().order_by('-id')
	if request.GET and request.GET['q']:
		products=Product.objects.filter(title__contains=request.GET['q'])
	product_data=[]
	for product in products:
		product_image=ProductImage.objects.filter(pro_id=product.id)[:1].get()
		product_data.append({
				'product':product,
				'product_img':product_image
			})
	# return HttpResponse(products)
	if 'carname' in request.GET:
		car_name=request.GET['carname']
	return render(request,'index.html',{'carname':car_name,'products':product_data})

def dealers(request):
	all_dealers=Dealer.objects.all()
	dealer_data=[]
	for d in all_dealers:
		count_cars=Product.objects.filter(dealer_id=d.id).count()
		dealer_data.append({
				'dealer':d,
				'total_cars':count_cars
			})
	return render(request,'dealers.html',{'dealers':dealer_data})

def brands(request):
	brands=Brand.objects.all()
	brand_data=[]
	for b in brands:
		count_cars=Product.objects.filter(brand_id=b.id).count()
		brand_data.append({
				'brand':b,
				'total_cars':count_cars
			})
	return render(request,'brands.html',{'brands':brand_data})

def brand_product(request,brand_id):
	brand_products=Product.objects.select_related('brand_id').filter(brand_id=brand_id,publish=True).order_by('-pk').all()
	pro_images=[]
	for product in brand_products:
		product_images=ProductImage.objects.filter(pro_id=product.id)[0]
		pro_images.append({
			'product':product,
			'product_images':product_images
		})
	return render(request,'brand-products.html',{'products':pro_images,'brand_id':brand_id})

# Specific Dealer Products
def dealer_product(request,dealer_id):
	dealer_products=Product.objects.select_related('dealer_id').filter(dealer_id=dealer_id,publish=True).order_by('-pk').all()
	pro_images=[]
	for product in dealer_products:
		product_images=ProductImage.objects.filter(pro_id=product.id)[0]
		pro_images.append({
			'product':product,
			'product_images':product_images
		})
	# return HttpResponse(pro_images)
	return render(request,'dealer-products.html',{'products':pro_images,'dealer_id':dealer_id})

# Product Detail Page
def product_detail(request,product_id):
	detail=Product.objects.select_related('dealer_id','brand_id').get(pk=product_id)
	user_data=False
	if 'userSession' in request.session:
		user_data=json.loads(request.session['userData'])
		user_id=user_data[0]['pk']
		user_data=User.objects.get(pk=user_id)
	product_imgs=ProductImage.objects.filter(pro_id=detail.id).all()
	return render(request,'product-detail.html',{'detail':detail,'product_imgs':product_imgs,'user_detail':user_data})

# User Register
def register(request):
	if request.method=='POST':
		full_name=request.POST['full_name']
		username=request.POST['username']
		email=request.POST['email']
		mobile=request.POST['mobile']
		password=request.POST['password']
		# Username and Password Validation
		if len(username)==0 and len(password)==0:
			messages.add_message(request, messages.ERROR, 'Invalid Username/Password!!')
			return redirect('register')
		# Save User Data
		user_save=User(full_name=full_name,username=username,email=email,password=password)
		user_save.save()
		messages.add_message(request, messages.SUCCESS, 'Thanks for Register.')
	# Load Template
	return render(request,'registration/register.html')

# User Login
def login(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		check_user = User.objects.filter(username=username,password=password).exists()
		if(check_user==True):
			user_data=User.objects.filter(username=username,password=password)
			request.session['userData']=serializers.serialize('json',user_data)
			request.session['userSession']=True
			return redirect('profile')
	return render(request,'registration/login.html')

# User Profile
def profile(request):
	if 'userSession' not in request.session:
		return redirect('login')
	user_data=json.loads(request.session['userData'])
	user_id=user_data[0]['pk']
	user_data=User.objects.get(pk=user_id)
	if request.method=='POST':
		user_data.email=request.POST['email']
		user_data.full_name=request.POST['full_name']
		user_data.mobile=request.POST['mobile']
		user_data.save()
		messages.add_message(request,messages.SUCCESS,'Data has been updated')
	return render(request,'registration/profile.html',{'user_data':user_data})

# User Logout
def logout(request):
	del request.session['userSession']
	del request.session['userData']
	return redirect('login')

# Send Enquiry
def send_enquiry(request):
	if request.method=='POST':
		product_id=request.POST['product_id']
		email=request.POST['email']
		full_name=request.POST['full_name']
		mobile=request.POST['mobile']
		enquiry_note=request.POST['enquiry_note']
		product_detail=Product.objects.get(pk=product_id)
		# Send Email
		send_mail(
			'Enquiry Message',
			enquiry_note,
			'admin@example.com',
			['projectsplaza@gmail.com'],
			fail_silently=False
		)
		# Save Data in Enquiry Model
		enquiry=Enquiry(
				product_id=product_id,
				email=email,
				full_name=full_name,
				mobile=mobile,
				enquiry_note=enquiry_note
			)
		enquiry.save()
		messages.add_message(request, messages.SUCCESS, 'Your enquiry has been sent.')
		return redirect('/detail/'+product_id)

