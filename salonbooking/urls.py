from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('services/', views.services, name='services'),
    path('stylists/', views.stylist, name='stylist_list'),
    path('booking/', views.booking_form, name='booking_form'),  
    path('api/register/', views.RegisterAPI.as_view()),
    path('api/login/',views.loginAPI.as_view()),

]