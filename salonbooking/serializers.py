from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Appointment, CompletedJob, Customer, Review, Service, Staff


class CustomerRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        customer = Customer.objects.create(
            user=user,
            phone=validated_data.get('phone', '')
        )

        return customer
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'image']

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')  # Show user email in review

    class Meta:
        model = Review
        fields = ['id', 'user_email', 'rating', 'comment', 'created_at']

class StaffSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)  # Include existing reviews

    class Meta:
        model = Staff
        fields = ['id', 'user', 'phone', 'description', 'image', 'services', 'reviews']
class CompletedJobSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    staff_name = serializers.ReadOnlyField(source='staff.user.get_full_name')
    customer_email = serializers.ReadOnlyField(source='customer.email')

    class Meta:
        model = CompletedJob
        fields = ['id', 'service', 'service_name', 'staff', 'staff_name', 
                  'customer', 'customer_email', 'image', 'description', 'rating', 'review', 'date_done']

class AppointmentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    service_name = serializers.ReadOnlyField(source='service.name')
    staff_name = serializers.ReadOnlyField(source='staff.user.get_full_name')

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'user_email', 'service', 'service_name', 'staff', 'staff_name',
                  'date', 'time', 'status', 'created_at']