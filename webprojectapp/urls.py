from django .urls import path 

from . import views

urlpatterns=[
path('',views.home, name='home'),

path('mobiles/', views.mobiles,name='mobiles'),
path('laptops/', views.laptops,name='laptops'),
path('tablets/', views.tablets,name='tablets'),
path('headsets/', views.headsets,name='headsets'),
path('addtocart', views.addtocart,name='addtocart'),
path('buynow', views.buynow,name='buynow'),
path('cart/', views.cart, name='cart'),
path('clearcart/', views.clearcart, name='clearcart'),
path('register', views.register, name='register'),
path('login/', views.login,name='login'),
path('logout/', views.logout, name = 'logout'),
path('payment/', views.payment,name='payment'),
path('ses/', views.setsession),
path('getses/', views.showsession),
path('gallery/',views.gallery,name='gallery'),
path('modals/',views.modals,name='modals')
]