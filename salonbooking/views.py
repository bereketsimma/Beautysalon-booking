from .models import SalonBooking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service, Staff,   Appointment
from .form import RegisterForm, LoginForm, BookingForm
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomerRegisterSerializer
# Create your views here.
class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'get':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')







# Services list
def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

# Stylists list
def stylist(request):
    stylists = Staff.objects.all()
    return render(request, 'stylist_list.html', {'stylists': stylists})



# Booking
@login_required
def booking_form(request, service_id=None, stylist_id=None):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_success')
    else:
        initial_data = {}
        if service_id:
            initial_data['service'] = service_id
        if stylist_id:
            initial_data['stylist'] = stylist_id
        form = BookingForm(initial=initial_data)
    return render(request, 'booking_form.html', {'form': form})

# @login_required
# def add_review(request, stylist_id):
#     stylist = get_object_or_404(Staff, id=stylist_id)

#     if request.method == 'POST':
#         rating = int(request.POST.get('rating'))
#         comment = request.POST.get('comment', '')

#         # Use request.user for the customer
#         review, created = Review.objects.update_or_create(
#             stylist=stylist,
#             customer=request.user,
#             defaults={'rating': rating, 'comment': comment}
#         )

#         messages.success(request, 'Your review has been submitted!')
#         return redirect('staff_list')

#     return render(request, 'core/add_review.html', {'stylist': stylist})
