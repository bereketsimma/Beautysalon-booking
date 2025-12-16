from django.urls import path
from . import views
from .views import login_user

urlpatterns = [
    path('', views.home, name='home'),
    # path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('services/', views.services, name='services'),
    path('stylists/', views.stylist, name='stylist_list'),
    path('booking/', views.booking_form, name='booking_form'),  
    path('api/register/', views.RegisterAPI.as_view()),
    path('api/login/',views.login_user, name='login_user'),

]