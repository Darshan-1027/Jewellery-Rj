"""
URL configuration for RJJewellery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from RJ import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage),
    path('category/<int:id>/',views.ProductsPage,name='products_by_category'),
    path('login', views.LoginPage, name='login'),
    path('OTP',views.OTPage),
    path('profile',views.ProfilePage),
    path('register',views.RegisterPage),
    path('singleproduct/<int:id>',views.SingleProductPage,name='single_product'),
    path('registerdata',views.RegisterPage),
    path('logincheck',views.LoginPage),
    path('logout',views.Logout),
    path('search',views.Searchdata),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),




    

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

