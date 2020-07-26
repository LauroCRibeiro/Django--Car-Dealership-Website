from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('dealers', views.dealers,name='dealers'),
    path('brands', views.brands,name='brands'),
    path('brand/<int:brand_id>', views.brand_product,name='brand_product'),
    path('dealer/<int:dealer_id>', views.dealer_product,name='dealer_product'),
    path('detail/<int:product_id>', views.product_detail,name='product_detail'),
    path('register', views.register,name='register'),
    path('login', views.login,name='login'),
    path('profile', views.profile,name='profile'),
    path('logout', views.logout,name='logout'),
    path('send-enquiry', views.send_enquiry,name='send_enquiry'),
]