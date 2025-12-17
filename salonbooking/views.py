from .models import CompletedJob, Appointment, Service, Staff,Customer, Review
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import AppointmentSerializer, CompletedJobSerializer, ServiceSerializer, StaffSerializer, CustomerRegisterSerializer
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



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
class LoginAPI(APIView):

    def post(self, request):
        # Get email and password from the request body
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'success': False, 'message': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(username=email, password=password)

        if user:
            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {'email': user.email, 'name': user.first_name}
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'success': False, 'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED)

class ServiceListAPIView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer



def home(request):
      return render(request, 'home.html')



class StaffListAPIView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
class StaffByServiceAPIView(APIView):
    """
    GET: Fetch staff filtered by service ID
    """
    def get(self, request, service_id):
        try:
            # Check if the service exists
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({'detail': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filter staff who can perform the service
        staff_members = Staff.objects.filter(services=service)
        serializer = StaffSerializer(staff_members, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class CompletedJobListAPIView(APIView):
    """
    GET: Fetch all completed jobs
    """
    def get(self, request):
        jobs = CompletedJob.objects.all().order_by('-date_done')
        serializer = CompletedJobSerializer(jobs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CompletedJobByServiceAPIView(APIView):
    """
    GET: Fetch completed jobs filtered by service ID
    """
    def get(self, request, service_id):
        jobs = CompletedJob.objects.filter(service__id=service_id).order_by('-date_done')
        serializer = CompletedJobSerializer(jobs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Log out the user by blacklisting their refresh token
        Request body: {"refresh": "<refresh_token>"}
        """
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)






class AppointmentListCreateAPIView(APIView):
    """
    GET: Fetch all appointments for the logged-in user
    POST: Book a new appointment
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status')  # Optional: filter by status
        appointments = Appointment.objects.filter(user=request.user)
        if status_filter:
            appointments = appointments.filter(status=status_filter)
        appointments = appointments.order_by('-date', '-time')
        serializer = AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Request body:
        {
            "service": 1,
            "staff": 2,
            "date": "2025-12-20",
            "time": "14:30"
        }
        """
        user = request.user
        service_id = request.data.get('service')
        staff_id = request.data.get('staff')
        date = request.data.get('date')
        time = request.data.get('time')

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({'detail': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        staff = None
        if staff_id:
            try:
                staff = Staff.objects.get(id=staff_id)
            except Staff.DoesNotExist:
                return Response({'detail': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)

        appointment = Appointment.objects.create(
            user=user,
            service=service,
            staff=staff,
            date=date,
            time=time
        )

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)








# Booking
# @login_required
# def booking_form(request, service_id=None, stylist_id=None):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.save()
#             return redirect('booking_success')
#     else:
#         initial_data = {}
#         if service_id:
#             initial_data['service'] = service_id
#         if stylist_id:
#             initial_data['stylist'] = stylist_id
#         form = BookingForm(initial=initial_data)
#     return render(request, 'booking_form.html', {'form': form})

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