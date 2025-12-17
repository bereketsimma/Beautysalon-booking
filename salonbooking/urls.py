from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('api/services/', views.ServiceListAPIView.as_view(), name='service-list'),
    path('api/staff/', views.StaffListAPIView.as_view(), name='staff-list'),

    # List staff filtered by service (GET)

    path('api/completed-jobs/', views.CompletedJobListAPIView.as_view(), name='completed-job-list'),
    path('api/completed-jobs/service/<int:service_id>/', views.CompletedJobByServiceAPIView.as_view(), name='completed-job-by-service'),
    path('api/staff-by-service/service/<int:service_id>/', views.StaffByServiceAPIView.as_view(), name='staff-by-service'),


    # List staff filtered by service (GET)
    path('api/appointments/', views.AppointmentListCreateAPIView.as_view(), name='appointment-list-create'),
    path('api/register/', views.RegisterAPI.as_view()),
    path('api/login/',views.LoginAPI.as_view()),

]