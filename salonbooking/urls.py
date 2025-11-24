from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('services/', views.services, name='services'),
    path('stylists/', views.stylist, name='stylist_list'),
    path('booking/', views.booking_form, name='booking_form'),     # path('logout/', views.logout_view, name='logout'),
]