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
from .serializers import  CustomerRegisterSerializer
from django.contrib.auth.models import User 
from .models import Customer
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if username or email exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create Customer linked to User
        # phone will remain null since user doesn't enter it
        customer, created = Customer.objects.get_or_create(user=user)

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )
class loginAPI(APIView):
    
    def login_user(request):
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'success': False, 'message': 'Email and password required'}, status=400)

            user = authenticate(username=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {'email': user.email, 'name': user.first_name}
                })
            else:
                return Response({'success': False, 'message': 'Invalid credentials'}, status=401)
def home(request):
      return render(request, 'home.html')

# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Redirect to home after registration
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})



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
