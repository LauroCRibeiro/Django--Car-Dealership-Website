from django.contrib import admin
from .models import Dealer, Brand, Product,ProductImage,User,Enquiry
# Register your models here.
admin.site.register(Dealer)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(User)
admin.site.register(Enquiry)